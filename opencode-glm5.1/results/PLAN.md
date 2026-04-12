# Implementation Plan

## Overview

A personal TV + movie companion app for collecting, organizing, rating, and discovering entertainment. Users build their version of each show (status, interest, tags, rating, AI scoop), and the app uses that taste profile to power discovery via Search, Ask (AI chat), Alchemy (concept blending), and Explore Similar.

**Stack:** Next.js (latest stable) + Supabase. No Docker required.

---

## 1. Project Setup & Infrastructure

### 1.1 Repo Scaffolding
- Initialize Next.js app with App Router
- Set up TypeScript throughout
- Configure `.env.example` with all required variables:
  - `NEXT_PUBLIC_SUPABASE_URL` — Supabase project URL
  - `NEXT_PUBLIC_SUPABASE_ANON_KEY` — Supabase anon/public key
  - `SUPABASE_SERVICE_ROLE_KEY` — server-only elevated key
  - `NEXT_PUBLIC_NAMESPACE_ID` — build/run namespace identifier
  - `NEXT_PUBLIC_DEFAULT_USER_ID` — dev identity injection
  - `CATALOG_API_KEY` — external catalog provider key (server-side)
  - `AI_API_KEY` — AI provider key (server-side)
  - `AI_MODEL` — AI model identifier
- `.gitignore` excluding `.env*` except `.env.example`
- Scripts: `npm run dev`, `npm test`, `npm run test:reset`

### 1.2 Supabase Setup
- Create Supabase project (hosted preferred; local optional)
- Define migrations for all tables (see Section 2)
- Seed data / fixtures for deterministic test state
- Enable RLS (Row Level Security) scoped by `namespace_id` and `user_id`

### 1.3 Namespace & Identity
- Every API route and DB query scoped by `namespace_id`
- All user-owned records scoped by `user_id`
- Dev-mode identity injection: `X-User-Id` header or `NEXT_PUBLIC_DEFAULT_USER_ID` env var
- Dev-only UI selector to switch users (gated behind `NODE_ENV !== 'production'`)
- Design schema so OAuth migration requires only auth wiring, not schema redesign

---

## 2. Data Model & Persistence

### 2.1 Database Tables

**`shows`** — Core show entity + user overlay
| Column | Type | Notes |
|---|---|---|
| id | text PK | stable catalog identifier |
| namespace_id | text | required, part of partition key |
| user_id | text | required, part of partition key |
| title | text | required |
| show_type | text | "movie" \| "tv" \| "person" \| "unknown" |
| external_ids | jsonb | optional external catalog IDs |
| overview | text | |
| genres | text[] | default {} |
| tagline | text | |
| homepage | text | |
| original_language | text | |
| spoken_languages | text[] | default {} |
| languages | text[] | default {} |
| poster_url | text | |
| backdrop_url | text | |
| logo_url | text | |
| network_logos | text[] | default {} |
| vote_average | float | |
| vote_count | int | |
| popularity | float | |
| last_air_date | timestamptz | |
| first_air_date | timestamptz | |
| release_date | timestamptz | |
| runtime | int | movie |
| budget | bigint | movie |
| revenue | bigint | movie |
| series_status | text | TV |
| number_of_episodes | int | TV |
| number_of_seasons | int | TV |
| episode_run_time | int[] | default {} |
| my_tags | text[] | default {} |
| my_tags_update_date | timestamptz | |
| my_score | float | |
| my_score_update_date | timestamptz | |
| my_status | text | "active"\|"next"\|"later"\|"done"\|"quit"\|"wait" |
| my_status_update_date | timestamptz | |
| my_interest | text | "excited"\|"interested" |
| my_interest_update_date | timestamptz | |
| ai_scoop | text | |
| ai_scoop_update_date | timestamptz | |
| details_update_date | timestamptz | |
| creation_date | timestamptz | set on first create only |
| is_test | boolean | default false |
| provider_data | jsonb | provider IDs by region/country |

Unique constraint: `(namespace_id, user_id, id)`

**`cloud_settings`** — Synced settings
| Column | Type | Notes |
|---|---|---|
| id | text PK | default "globalSettings" |
| namespace_id | text | |
| user_id | text | |
| user_name | text | random name on first launch |
| version | float | epoch seconds for conflict resolution |
| catalog_api_key | text | server-encrypted |
| ai_api_key | text | server-encrypted |
| ai_model | text | model key/name |

**`app_metadata`** — Migration tracking
| Column | Type | Notes |
|---|---|---|
| namespace_id | text PK | |
| data_model_version | int | default 3 |

### 2.2 Local/Client Settings (key-value, not synced)
Stored in localStorage or equivalent:
- `autoSearch` (bool) — Search on launch
- `fontSize` ("XS"|"S"|"M"|"L"|"XL"|"XXL")
- `hideStatusRemovalConfirmation` (bool)
- `statusRemovalCountKey` (int)
- `lastSelectedFilter` (FilterConfiguration JSON)

### 2.3 Merge Rules
When external catalog data merges into existing stored show:
- **Non-my fields:** `selectFirstNonEmpty(new, old)` — never overwrite non-empty with empty/nil
- **My fields:** resolve by timestamp — newer update date wins
- `details_update_date` set to "now" after merge
- `creation_date` immutable after first create

### 2.4 Transient Data (not persisted)
- Cast, crew, seasons, images, videos, recommendations, similar shows
- AI chat history (Ask sessions)
- Alchemy results/reasons
- Mentioned shows strip
- These are fetched on demand and discarded on navigation

### 2.5 Migrations
- Versioned migration files in `supabase/migrations/`
- `app_metadata.data_model_version` tracks current version
- Auto-run migrations on app startup (server-side check)
- Data continuity: existing user data automatically brought forward on upgrade

---

## 3. API Layer (Next.js Server Actions / Route Handlers)

### 3.1 Catalog Proxy Routes
- `GET /api/catalog/search?q=&page=` — proxy search to external catalog (TMDB or equivalent)
- `GET /api/catalog/show/:id` — fetch show details (credits, seasons, videos, recs, similar, providers)
- `GET /api/catalog/person/:id` — fetch person details + filmography

All catalog routes:
- Store API key server-side only
- Map external payload → internal `Show` shape using field mapping rules
- Merge with existing stored show if present

### 3.2 Collection CRUD
- `GET /api/collection` — list shows for `(namespace_id, user_id)` with optional filter params
- `POST /api/collection/show` — save/update a show (set status, rating, tags, etc.)
- `DELETE /api/collection/show/:id` — remove from collection (clears all My Data)
- `PATCH /api/collection/show/:id` — partial update of My Data fields

Auto-save logic enforced server-side:
- Rating unsaved show → status defaults to `Done`
- Adding tag to unsaved show → status defaults to `Later`, interest defaults to `Interested`
- Setting status → always saves
- Choosing interest chip → sets `Later` + interest

### 3.3 AI Routes
- `POST /api/ai/ask` — chat message, returns `{ commentary, showList }`
- `POST /api/ai/scoop` — generate AI Scoop for a show
- `POST /api/ai/concepts` — generate concepts (single or multi-show)
- `POST /api/ai/recommendations` — concept-based recommendations (Explore Similar / Alchemy)

AI routes include:
- User library context (saved shows + My Data) in prompt
- Structured output parsing with retry + fallback
- Mentioned shows parsed from `showList` format: `Title::externalId::mediaType;;...`
- Recommendation → catalog resolution (match external ID, case-insensitive title)
- Streaming support for Scoop progressive display

### 3.4 Settings & Data Routes
- `GET /api/settings` — fetch cloud settings
- `PATCH /api/settings` — update cloud settings
- `GET /api/data/export` — export all user data as JSON (in zip)
- `POST /api/test/reset` — destructive reset scoped to `namespace_id`

### 3.5 Identity Middleware
- Extract `user_id` from auth session (production) or `X-User-Id` header / env var (dev)
- Attach `namespace_id` and `user_id` to request context
- Reject unauthenticated requests in production mode

---

## 4. AI System Design

### 4.1 Prompt Architecture
Each AI surface shares one persona but has surface-specific prompt templates:

**Base personality** (all surfaces): fun, chatty TV/movie nerd friend; joy-forward; opinionated honesty; spoiler-safe; vibe-first; specific not generic.

**Scoop prompt**: structured mini blog-post: personal take → honest stack-up → "The Scoop" centerpiece → fit/warnings → "Worth it?" verdict. ~150-350 words. Cached 4 hours.

**Ask prompt**: conversational, friend-in-dialogue, picks favorites confidently, bulleted lists for multi-recs. Context: user library + current chat history. Older turns summarized after ~10 messages.

**Concepts prompt**: bullet list, 1-3 words each, evocative, no explanation, no plot/spoilers. Multi-show concepts must be shared across all inputs. 8 concepts default. Specificity > genericity.

**Recommendations prompt**: list of shows with 1-3 sentence reasons naming which concepts align. Recent bias but allow classics. Real catalog items with external IDs. 5 recs (Explore Similar) / 6 recs (Alchemy).

### 4.2 Context Assembly
- AI requests include: user's saved shows (titles + statuses + ratings + tags), current show context (for Scoop/Ask-about), selected concepts, recent conversation turns
- Context window managed by summarizing older chat turns into 1-2 sentences (preserving persona tone)

### 4.3 Structured Output & Parsing
- Ask with mentions: parse `Title::externalId::mediaType;;` format from `showList` field
- Concepts: parse bullet list
- Recommendations: parse structured list with title + externalId + mediaType + reason
- Fallback: if parsing fails, retry once with stricter instructions; then fall back to unstructured + Search handoff

### 4.4 AI Recommendation → Real Show Resolution
1. AI returns title + externalId + mediaType
2. System looks up external catalog by externalId
3. Accept first result whose title matches case-insensitively
4. If found → real selectable Show (carry AI reason as transient text)
5. If not found → show non-interactive or hand off to Search

### 4.5 Cache & Freshness
- AI Scoop: cached 4 hours, regenerate on demand after expiry, persist only if show in collection
- Ask chat history: session-only, cleared on reset/leave
- Alchemy results: session-only, cleared on leave
- Concepts: session-only

---

## 5. Frontend Architecture

### 5.1 App Structure (Next.js App Router)
```
app/
  layout.tsx              — root layout, providers
  page.tsx                — Home (Collection)
  find/
    page.tsx              — Find/Discover hub
    search/page.tsx       — Search mode
    ask/page.tsx          — Ask (AI chat) mode
    alchemy/page.tsx      — Alchemy mode
  show/[id]/page.tsx      — Show Detail
  person/[id]/page.tsx    — Person Detail
  settings/page.tsx       — Settings
components/
  collection/             — Home/collection components
  find/                   — Search/Ask/Alchemy components
  show/                   — Show Detail components
  person/                 — Person Detail components
  shared/                 — Reusable UI (tiles, chips, filters, etc.)
  ai/                     — AI-specific components (chat, scoop, concepts)
lib/
  api/                    — client-side API helpers
  supabase/               — Supabase client setup
  ai/                     — AI prompt templates + response parsers
  catalog/                — catalog mapping/merge logic
  types/                  — TypeScript types matching schema
  hooks/                  — React hooks for data fetching/mutation
  utils/                  — helpers
```

### 5.2 State Management
- Server state via React Query / SWR for collection data, show details, settings
- Local state for UI toggles, filter selections, AI session state
- Optimistic updates for status/rating/tag mutations (refetch on server confirmation)
- Client cache is disposable — clearing localStorage never loses data

### 5.3 Key React Hooks
- `useCollection(filter?)` — filtered collection with status grouping
- `useShow(id)` — show detail with merge + user overlay
- `usePerson(id)` — person detail with filmography
- `useAskSession()` — chat state + send message + mentioned shows
- `useAlchemySession()` — step management (shows → concepts → recs → chain)
- `useExploreSimilar(showId)` — concepts + recs for single show
- `useScoop(showId)` — scoop generation + cache
- `useSettings()` — cloud + local settings
- `useFilters()` — filter sidebar state + available filters from collection tags/genres/decades/scores
- `useIdentity()` — current namespace_id + user_id

---

## 6. Feature Implementation Order

### Phase 1: Foundation
1. Project scaffolding, env setup, Supabase migrations
2. Identity middleware (namespace + user_id scoping)
3. Catalog proxy API routes (search + show detail + person detail)
4. Show data mapping (external catalog → internal schema + merge rules)
5. Basic layout shell (sidebar + main area + navigation)

### Phase 2: Collection Core
6. Collection CRUD API + save triggers + auto-save logic + default values
7. Collection Home page with status grouping (Active → Excited → Interested → Other collapsed)
8. Filter sidebar (All Shows, tag filters, genre/decade/score filters, media-type toggle)
9. Show tiles with in-collection + rating badges

### Phase 3: Show Detail
10. Show Detail page — header media carousel, core facts, community score
11. My Relationship controls (status/interest chips, rating bar, tags)
12. Overview + AI Scoop (generate, cache, progressive stream)
13. Traditional recommendations strand
14. Streaming availability section
15. Cast/Crew strands → Person Detail
16. Seasons (TV), Budget/Revenue (movies)
17. "Ask about this show" CTA

### Phase 4: Discovery
18. Search (Find → Search) — text search, poster grid, in-collection markers
19. Ask (Find → Ask) — chat UI, mentioned shows row, starter prompts, conversation summarization
20. Explore Similar — Get Concepts → select → Explore Shows
21. Alchemy — select 2+ shows → Conceptualize → select catalysts → Alchemize → chain

### Phase 5: Person & Settings
22. Person Detail page — image gallery, bio, analytics charts, filmography by year
23. Settings page — font size, search on launch, username, API keys, AI model
24. Export My Data (zip with JSON, ISO-8601 dates)

### Phase 6: Polish & Testing
25. Empty states (no collection, no filter results)
26. Removal confirmation flow (with "stop asking" after repeated removals)
27. Re-add same show flow (merge + timestamp resolution)
28. Destructive test reset (scoped to namespace)
29. End-to-end tests for key user journeys
30. Data migration forward-compatibility (model version tracking)

---

## 7. Key Business Rules Summary

| Rule | Detail |
|---|---|
| Collection membership | Show has assigned `my_status` (non-nil) |
| Save triggers | Setting status, choosing interest chip, rating unsaved, tagging unsaved |
| Default save | Status=Later, Interest=Interested; via rating → Status=Done |
| Removal | Clear status → remove from storage → clear all My Data → warn (suppress after N times) |
| Re-add | Preserve latest My Data, refresh public metadata, merge by timestamp per field |
| User overlay wins | If user has saved version, display user-overlaid data everywhere |
| Interest applies only to Later | If status changes away, interest retained but irrelevant |
| AI Scoop persistence | Only if show is in collection; 4hr cache |
| AI session data | Not persisted; cleared on leave/reset |
| AI recs → real shows | Resolve via externalId + case-insensitive title match |
| Backend is truth | Client cache disposable; clearing local storage loses nothing |
| Namespace isolation | Two namespaces never read/write each other's data |
| User identity | All records scoped to user_id; multi-user ready |

---

## 8. AI Voice & Quality Contract

All AI surfaces must pass the Discovery Quality Bar:

| Dimension | Passing Threshold |
|---|---|
| Voice adherence | ≥1 — warm, playful, opinionated, spoiler-safe |
| Taste alignment | ≥1 — grounded in concepts/library |
| Surprise without betrayal | some unexpected but defensible picks |
| Specificity of reasoning | concrete "because" tied to concepts |
| Real-show integrity | =2 (non-negotiable) — no hallucinated titles |
| **Total** | **≥7/10** |

Key voice rules:
- Search has NO AI voice (straightforward catalog search)
- All other surfaces share one persona: water-cooler gossip + critic brain + hype friend
- Tone sliders: 70% friend / 30% critic; 60% hype / 40% measured
- Concepts: specific > generic ("hopeful absurdity" ✓, "good characters" ✗)
- Concept diversity: cover different axes (structure, vibe, emotion, craft)
- Concept ordering: best "aha" concepts first

---

## 9. Cross-Cutting Concerns

### Security
- Supabase anon key for client; service role key server-only
- API keys for catalog/AI never exposed to client
- RLS policies enforce namespace + user_id partitioning
- Dev identity injection disabled in production

### Performance
- Client caching via React Query/SWR with stale-while-revalidate
- Transient data (credits, seasons, videos) fetched on demand, not persisted
- AI streaming for Scoop progressive display
- Image URLs from catalog (no local image storage)

### Testing
- `npm test` — runs test suite
- `npm run test:reset` — resets data scoped to `namespace_id`
- Destructive tests never require global DB teardown
- Test data marked with `is_test: true`

### Data Continuity
- Migrations versioned in `app_metadata.data_model_version`
- On upgrade, existing shows/My Data brought forward automatically
- User never loses collection/ratings/tags/statuses/scoop due to update

---

## 10. Open Items (from PRD)

- Should Next become first-class UI status?
- Named custom lists beyond tags?
- Should AI Scoop on unsaved show implicitly save it?
- Explicit "Unrated" state vs nil for cleared rating?
- Import/Restore from export zip
- Save/share Alchemy sessions as reusable blends
- Explicit myStatus filters in sidebar
