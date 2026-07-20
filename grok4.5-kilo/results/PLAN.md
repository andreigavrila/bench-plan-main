# Implementation Plan: Personal TV + Movie Companion

## 1. Overview

Build a personal entertainment companion for collecting, organizing, rating, and discovering TV/movies. Discovery is taste-aware via library overlays (status, interest, tags, rating, AI Scoop) plus three paths: Search, Ask (chat), and Alchemy/Explore Similar (concept blending).

**Stack (benchmark baseline):**
- **Next.js** (latest stable) — App Router, UI + server boundary
- **Supabase** — server-side source of truth for user data
- **External catalog API** (e.g. TMDB-compatible) — public show/person metadata
- **AI provider** (configurable model + API key) — Scoop, Ask, Concepts, Alchemy

**Non-goals this plan does not implement:** offline-first, social features, real OAuth (dev identity only), Import/Restore UI (optional later), first-class “Next” status in UI.

---

## 2. Architecture Principles

### 2.1 Fractal feature structure (per INSTRUCTIONS.md)

```
src/
├── config/                 # env, constants, feature flags
├── theme/                  # design tokens (no magic numbers in TSX)
├── components/             # shared UI primitives (ShowTile, StatusChips, etc.)
├── hooks/                  # global hooks
├── utils/                  # pure helpers
├── lib/                    # server clients, external APIs, AI
├── types/                  # shared domain types
└── pages/                  # or app/ routes with co-located features
    └── PageName/
        ├── PageName.tsx
        └── features/
            └── FeatureName/
                ├── FeatureName.tsx
                ├── hooks/
                ├── utils/
                └── features/   # nested sub-features
```

- Humble components: TSX = markup + binding; logic in `useFeatureLogic` hooks
- Co-locate feature hooks/utils; main file name matches directory (no `index.tsx`)
- Unit tests adjacent to source

### 2.2 Client / server boundary

| Concern | Location |
|--------|----------|
| Catalog search/details/person | Server routes or server actions (API key never in browser if secret) |
| Collection CRUD | Server API → Supabase; scoped by `(namespace_id, user_id)` |
| AI calls | Server only (keys, library context injection) |
| Local prefs (font, autoSearch, UI flags) | Client storage OK; disposable |
| Cloud settings (username, AI model, keys) | Supabase; optional sync |

**Rule:** Backend is source of truth. Clearing client storage must not lose library/My Data.

### 2.3 Identity & isolation

- **`namespace_id`**: build/run partition; all tables include it; destructive reset scoped to it
- **`user_id`**: opaque stable string on every user-owned row; multi-user-ready schema
- **Dev identity:** `X-User-Id` header and/or fixed default user in dev/test; gated off in production
- Future OAuth swaps identity wiring only — **no schema redesign**

---

## 3. Data Model & Persistence

### 3.1 Supabase tables (conceptual)

**`shows`** (user collection + cached catalog fields for saved items)

| Column group | Fields |
|--------------|--------|
| Partition | `namespace_id`, `user_id` |
| Identity | `id` (catalog id), `title`, `show_type` (`movie` \| `tv`), `external_ids` jsonb |
| Catalog | overview, genres[], tagline, languages, images URLs, vote/popularity, dates, runtime/budget/revenue, TV season/episode fields, `provider_data` jsonb |
| My Data | `my_status`, `my_interest`, `my_tags[]`, `my_score`, `ai_scoop` + each `*_update_date` |
| Meta | `details_update_date`, `creation_date`, `is_test`, updated_at |

Unique constraint: `(namespace_id, user_id, id)` where `my_status IS NOT NULL` defines “in collection” (or equivalent membership rule).

**`cloud_settings`**

- `(namespace_id, user_id)` PK  
- `user_name`, `version` (epoch for conflict), `catalog_api_key`, `ai_api_key`, `ai_model`

**`app_metadata`**

- `(namespace_id)` or global: `data_model_version` (start at 3; migrations forward)

**Optional cache (not required for correctness):** catalog detail cache table keyed by show id with TTL — disposable.

### 3.2 Membership & My Data rules

1. **In collection** ⇔ non-null `my_status`
2. **Save triggers:** set status; pick Interested/Excited; rate unsaved show; add ≥1 tag to unsaved
3. **Defaults:**
   - Save without explicit status → `Later` + `Interested`
   - First save via rating → `Done`
4. **Interest chips:** Interested/Excited set `Later` + that interest
5. **Remove:** clear status (with confirm unless suppressed) → delete row / clear all My Data including scoop
6. **Interest:** only meaningful when status is `Later`; may retain value when leaving Later
7. **Status values in model:** `active`, `next` (hidden), `later`, `done`, `quit`, `wait`
8. **Timestamps:** every user field has update date for sort + conflict (newer wins per field)
9. **Catalog merge:** non-my fields `selectFirstNonEmpty(new, old)`; never empty-over-write; my fields by timestamp; set `details_update_date` on merge; `creation_date` only once

### 3.3 Transient vs persisted AI

| Data | Persist? |
|------|----------|
| AI Scoop | Yes if in collection; 4h freshness |
| Ask history / mentions | Session only |
| Alchemy concepts/results | Session only |
| Explore Similar session state | Session only |

### 3.4 Export

Settings → Export My Data: `.zip` with JSON of all saved shows + My Data; ISO-8601 dates. Import deferred (open question).

### 3.5 Migrations & reset

- SQL migrations under `supabase/migrations/` (or equiv.) for deterministic schema
- `npm run test:reset` deletes/re-seeds data for current `namespace_id` only (no global teardown)
- Schema evolution must migrate existing My Data without user action (continuity)

---

## 4. External Integrations

### 4.1 Catalog provider

Abstract behind `CatalogClient`:

- Search by query → list of lightweight shows  
- Get show details (movie/TV) → full public fields + credits, videos, images, similar/recommended, seasons, providers  
- Get person → bio, images, credits  
- Resolve by external id + media type; title match case-insensitive when validating AI recs  

Config: `CATALOG_API_KEY` (and base URL if needed). Keys in server env; optional per-user key in cloud settings.

### 4.2 AI provider

Abstract behind `AIClient` with surfaces:

1. **Scoop** — structured mini taste-review; stream if supported  
2. **Ask** — chat; structured mentions output  
3. **Concepts** — bullet list 1–3 words; multi-show = shared only  
4. **Concept recs** — Explore Similar (5) / Alchemy (6) with reasons naming concepts  
5. **Summarize** — older chat turns → 1–2 sentence same-persona summary  

Config: `AI_API_KEY`, `AI_MODEL` (+ provider base). Server injects library slice + My Data for taste-awareness.

### 4.3 Recommendation resolution (critical)

For each AI recommendation:

1. Parse `title` + `externalId` + `mediaType`  
2. Lookup catalog by id when present  
3. Accept if title matches case-insensitively  
4. Else non-interactive display and/or Search handoff  
5. Real-show integrity is non-negotiable (quality bar)  

Structured Ask mentions format:

```
Title::externalId::mediaType;;Title2::externalId::mediaType;;...
```

Parse failures: retry once stricter; else unstructured + Search handoff.

---

## 5. AI Voice & Quality Contracts

Single persona across Scoop / Ask / Concepts / Alchemy: **warm TV nerd friend** — joy-forward, opinionated honest, vibe-first spoiler-safe, specific not generic. Search has **no** AI voice.

**Scoop sections:** personal take, stack-up vs reviews, emotional “The Scoop” centerpiece, fit/warnings, Worth it? (~150–350 words). Toggle: “Give me the scoop!” / “Show the scoop” / open title “The Scoop”; progressive “Generating…”; cache 4h; persist only if collected.

**Ask:** friend dialogue; bullets for multi-rec; direct answer in first 3–5 lines; welcome with 6 random starters (refreshable; pool of curated prompts); summarize after ~10 messages; “Ask about this show” seeds show context.

**Concepts:** spoiler-free, evocative, no generics (“good characters” invalid); multi-show shared; select 1–8; changing selection/shows clears downstream.

**Alchemy counts:** 6 recs; **Explore Similar:** 5 recs; reasons cite selected concepts; recent bias allowed but not exclusive.

Quality dimensions for QA: Voice, Taste alignment, Surprise without betrayal, Specificity, Real-show integrity (must = 2).

---

## 6. App Structure & Navigation

### 6.1 Layout shell

```
┌──────────────┬─────────────────────────────────────┐
│ Filters nav  │  Main content                        │
│ - All Shows  │  Home | Detail | Find | Person |     │
│ - Tags…      │  Settings                            │
│ - No tags    │                                      │
│ - Genres…    │                                      │
│ - Decades…  │                                      │
│ - Scores…    │                                      │
│ + Settings   │                                      │
│ + Find       │                                      │
└──────────────┴─────────────────────────────────────┘
```

- Media-type toggle (All / Movies / TV) applies on top of any filter  
- Persist last selected filter in local UI state  
- Find hub mode switcher: **Search | Ask | Alchemy**  
- Settings always reachable  
- Optional “Search on Launch” → open Find/Search on cold start  

### 6.2 Routes (App Router sketch)

| Route | Page |
|-------|------|
| `/` | Collection Home |
| `/show/[id]` | Show Detail |
| `/person/[id]` | Person Detail |
| `/find` | Find hub (mode query or tabs) |
| `/settings` | Settings & Your Data |

Deep links preserve overlay (user version wins everywhere tiles/detail appear).

---

## 7. Feature Breakdown

### Phase 0 — Foundation

1. Scaffold Next.js + TypeScript + lint/theme tokens  
2. `.env.example`, `.gitignore` for secrets  
3. Config module: `NAMESPACE_ID`, `DEFAULT_USER_ID`, Supabase URL/keys, catalog/AI keys  
4. Supabase schema migrations + typed DB client (server)  
5. Dev identity middleware (`X-User-Id` / default user)  
6. Scripts: `dev`, `test`, `test:reset`  
7. Domain types aligned with storage schema (Show, statuses, filters, settings)  
8. Shared primitives: Button, Chip, Modal, PosterImage, Loading/Empty states  

**Exit:** app boots, env-driven, empty collection loads under a namespace/user.

---

### Phase 1 — Catalog + Show Detail (read path)

**Features:**

- Catalog search API integration  
- Show Detail assembly:
  1. Header media carousel (backdrops/posters/logos/trailers; graceful fallback)
  2. Core facts (year, runtime or seasons/episodes) + community score
  3. Overview
  4. Genres + languages
  5. Traditional similar/recommended strand
  6. Streaming providers (“Stream It”)
  7. Cast & Crew strands → Person
  8. Seasons (TV)
  9. Budget vs Revenue (movies when present)
- Person Detail: gallery, bio, filmography by year, lightweight charts (avg ratings, top genres, projects-by-year)
- ShowTile component with poster/title placeholders for in-collection/rating badges

**Co-located structure example:**

```
pages/ShowDetail/
  ShowDetail.tsx
  features/
    HeaderMedia/
    CoreFacts/
    OverviewSection/
    RecommendationsStrand/
    StreamingProviders/
    CastCrew/
    SeasonsStrand/
    BudgetRevenue/
```

**Exit:** browse catalog → detail → person → back to show; no persistence yet for My Data.

---

### Phase 2 — Collection & My Data

**Server services:**

- `CollectionService`: list (filtered), upsert, merge catalog, remove, export JSON  
- Enforcement of save defaults, timestamps, membership  

**UI:**

- Home: status grouping
  1. Active (larger tiles)
  2. Excited (Later + Excited)
  3. Interested (Later + Interested)
  4. Collapsed Other: Wait, Quit, Done, unclassified Later  
- Empty: prompt Search/Ask; filter empty: “No results found”  
- Detail toolbar: Status/Interest chips (Active, Interested, Excited, Done, Quit, Wait)  
- Rating control → unsaved ⇒ auto-save Done  
- Tags chips + picker → unsaved + tag ⇒ Later + Interested  
- Removal confirm (+ count → optional “stop asking”)  
- Sidebar filters: All; per tag + No tags; genre; decade; community score ranges; media toggle  
- Overlay rule: any list (search, AI, home) shows user’s status/tags/rating/scoop when saved  

**Exit:** full collect/maintain journeys 1–5 and 10 (export) work end-to-end against Supabase.

---

### Phase 3 — Find: Search

- Text search → poster grid  
- In-collection + rating badges on tiles  
- Open Detail  
- Honor Search on Launch  

**Exit:** journey “build collection” from Search is smooth.

---

### Phase 4 — AI Scoop + Ask

**Scoop subscale (`ShowDetail/features/AiScoop`):**

- On-demand generation + stream  
- Session/memory cache 4h by show id  
- Persist scoop only if `my_status` set  
- Section structure per voice spec  

**Ask subscale (`Find/features/Ask`):**

- Chat UI user/assistant  
- Starter prompt welcome (6 random from curated set; refresh)  
- Mention parsing → horizontal “mentioned shows” strip  
- Tap → Detail or Search fallback  
- Context window + summarize after ~10 turns  
- Handoff from Detail “Ask about …” with show seed  
- Session clear on leave/reset  

**Shared:** taste context builder (library sample + tags/statuses/ratings); spoiler-safe system prompts; domain guardrails.

**Exit:** journeys 6 + Scoop delight path; quality bar spot-check.

---

### Phase 5 — Concepts, Explore Similar, Alchemy

**Concepts service** (single + multi-show), selection cap 8.

**Show Detail — Explore Similar:**

1. Get Concepts  
2. Select chips (“ingredients you want more of”)  
3. Explore Shows → 5 resolved recs with reasons  
4. Changing concepts clears recs  

**Find — Alchemy:**

1. Pick ≥2 shows (library + global search picker)  
2. Conceptualize Shows  
3. Select ≤8 concepts  
4. ALCHEMIZE! → 6 recs  
5. More Alchemy! chains (use results as new inputs)  
6. Backtrack: change shows → clear concepts/results  

Session-only state machines; no DB for alchemy sessions.

**Exit:** journeys 7–8; resolution integrity tests.

---

### Phase 6 — Settings, Polish, Continuity

- Font size tokens (`XS`–`XXL`) applied via theme  
- Username, AI model, optional user-supplied keys (never commit; prefer env in bench)  
- Catalog API key field  
- Export zip download  
- Data model version + migration path documentation  
- Loading/error/empty polish; tile badges everywhere  
- Accessibility basics (chips, focus, keyboard nav)  

Optional stretch (explicitly out of core if timeboxed): Import/Restore, Next status UI, named lists, save Alchemy blends, sidebar myStatus filters.

---

## 8. Cross-Cutting Business Logic Modules

Implement as pure/domain modules with unit tests (no UI):

| Module | Responsibility |
|--------|----------------|
| `collectionMembership` | save triggers, defaults, removal clears |
| `statusInterestMap` | Interested/Excited ↔ Later + interest |
| `showMerge` | catalog vs my-field merge + timestamps |
| `filterCollection` | tag/genre/decade/score/media filters |
| `homeGrouping` | Active / Excited / Interested / Other |
| `aiResolveShow` | id + title match, fallbacks |
| `aiMentionParse` | `Title::id::type` format + retry policy |
| `scoopFreshness` | 4h validity |
| `exportSnapshot` | ISO dates, zip payload shape |
| `conflictResolve` | per-field newer-wins for sync |

---

## 9. API Surface (server)

Illustrative route groups (App Router route handlers or server actions):

```
/api/catalog/search
/api/catalog/shows/[id]
/api/catalog/people/[id]
/api/collection                 GET list, POST upsert batch
/api/collection/[id]            GET/PATCH/DELETE
/api/collection/export
/api/settings                   GET/PUT cloud settings
/api/ai/scoop
/api/ai/ask
/api/ai/concepts
/api/ai/concept-recs
/api/dev/reset                  namespace-scoped, non-prod
```

All user routes require resolved `user_id` + inject `namespace_id` from env. Anon Supabase key in client only if RLS correctly partitions; prefer server-side Supabase with service role for bench simplicity, **service role never shipped to browser**.

### RLS / access sketch

If using client Supabase:

- Policies filter `namespace_id = current_setting` and `user_id = auth.uid()` (or claim)  
- Bench: server-only access with explicit namespace/user filters is simpler and compliant  

---

## 10. Environment Interface

`.env.example` (names illustrative):

```
# App isolation
NAMESPACE_ID=
DEFAULT_USER_ID=

# Supabase
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=   # server only

# Catalog
CATALOG_API_KEY=
CATALOG_BASE_URL=

# AI
AI_API_KEY=
AI_MODEL=
AI_BASE_URL=

# Mode
NODE_ENV=
ALLOW_DEV_IDENTITY=true
```

No secrets in repo; app runs by filling env only.

---

## 11. Testing Strategy

### 11.1 Unit

- Membership/save/remove defaults  
- Interest/status mapping  
- Merge + conflict timestamps  
- Filters + home grouping  
- Mention parser + resolve matcher  
- Scoop freshness  

### 11.2 Integration

- Collection CRUD under two namespaces → no cross-read  
- Two users same namespace → isolation  
- `test:reset` wipes only current namespace  
- AI resolution preferred path with fixture catalog  
- Export JSON shape  

### 11.3 Manual / golden (quality bar)

- Scoop has required sections + honest tone  
- Ask starters + mention strip  
- Alchemy 6 / Explore 5 with concept-linked reasons  
- Score dims ≥ thresholds (integrity = perfect)  

### 11.4 Visual (preferred)

- Home status groups  
- Detail first-15-seconds hierarchy  
- Find mode switcher  

Scripts: `npm test`, `npm run test:reset`.

---

## 12. Implementation Order (Suggested)

| Step | Work | Depends |
|------|------|---------|
| 0 | Scaffold, env, theme, config | — |
| 1 | Supabase schema + identity + reset | 0 |
| 2 | Catalog client + Detail/Person read UI | 0 |
| 3 | Collection service + Home + My Data controls | 1, 2 |
| 4 | Filters sidebar + media toggle | 3 |
| 5 | Search hub mode | 2, 3 |
| 6 | Scoop | 3 + AI client |
| 7 | Ask + mentions + handoff | 6 patterns |
| 8 | Concepts + Explore Similar | 7 |
| 9 | Alchemy full flow | 8 |
| 10 | Settings, export, font, launch prefs | 3 |
| 11 | Polish, tests, quality pass | all |

---

## 13. UX Hierarchy Notes (Detail)

Preserve narrative order unless intentionally changed:

1. Header media  
2. Core facts + community score  
3. Tag chips  
4. Overview + Scoop toggle  
5. Ask about this show  
6. Genres + languages  
7. Recommendations strand  
8. Explore Similar  
9. Stream It  
10. Cast, Crew  
11. Seasons (TV)  
12. Budget/Revenue (movies)  

Primary actions early (status toolbar, rating, scoop, concepts); long-tail depth down-page. No Alchemy entry on Detail (hidden for now). Inline trailer when possible.

Home captions & empty states should feel inviting (“your taste made visible”), not bureaucratic.

---

## 14. Risk Register & Mitigations

| Risk | Mitigation |
|------|------------|
| AI hallucinated titles | Strict resolve; drop unmatched; Search fallback |
| Structured parse flake | Retry once; degrade gracefully |
| Key leakage | Server-only secrets; RLS; never commit `.env` |
| Namespace collision | Required env `NAMESPACE_ID`; all queries filter |
| Over-busy Detail | Sticky hierarchy; collapsible lower sections |
| Prompt drift / off-brand voice | Shared system prompt core + surface adapters; quality checklist |
| Catalog rate limits | Server cache for details; debounce search |
| Schema drift vs user data | Versioned migrations; never drop my_* without transform |

---

## 15. Success Criteria Checklist

**Product**

- [ ] Full My Data lifecycle (status/interest/tags/rating/scoop) with correct defaults  
- [ ] User overlay everywhere  
- [ ] Home grouped by status + filters + media toggle  
- [ ] Search, Ask, Alchemy modes in Find  
- [ ] Detail hierarchy + Explore Similar + Scoop  
- [ ] Person analytics + filmography  
- [ ] Export zip  
- [ ] AI maps to real shows  

**Infra rider**

- [ ] Next.js + Supabase  
- [ ] `.env.example` + gitignored secrets  
- [ ] `user_id` on all user rows  
- [ ] `namespace_id` isolation + scoped reset  
- [ ] Dev identity; OAuth-ready schema  
- [ ] Server truth; client cache disposable  
- [ ] One-command dev/test/reset  

**Craft**

- [ ] Fractal feature folders, humble components, theme tokens  
- [ ] Unit tests on domain rules  
- [ ] Voice consistency across AI surfaces  

---

## 16. Open Questions (explicitly deferred)

1. First-class **Next** status in UI?  
2. Named custom lists beyond tags?  
3. Scoop on unsaved show → implicit save?  
4. Explicit Unrated vs nil for cleared rating?  
5. Import/Restore from zip?  
6. Persist/share Alchemy blends?  
7. Sidebar myStatus filters?  

Plan assumes current PRD defaults unless product decides otherwise.

---

## 17. Deliverables Summary

| Artifact | Purpose |
|----------|---------|
| Next.js app (App Router) | Product UI + API |
| Supabase migrations | Deterministic schema |
| `.env.example` | Configure without code edits |
| Domain services + tests | Business rules fidelity |
| AI + Catalog adapters | Swappable providers |
| Export pipeline | User data ownership |
| `test:reset` | Benchmark isolation |

**This step produces planning only.** Implementation begins only after this plan is accepted; no application source is created as part of the planning deliverable.
