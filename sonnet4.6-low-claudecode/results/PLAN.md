# Implementation Plan: TV & Movie Companion App

## Overview

A personal TV/movie companion app built with Next.js + Supabase. Users collect, organize, rate, and discover entertainment via traditional search, AI chat ("Ask"), Alchemy (concept blending), and per-show concept exploration.

---

## Tech Stack

- **Runtime:** Next.js (latest stable) — App Router
- **Database:** Supabase (hosted), accessed via `@supabase/supabase-js`
- **AI:** Configurable provider via environment variables (OpenAI-compatible)
- **External catalog:** TMDB (The Movie Database) via API key
- **Styling:** Tailwind CSS
- **Language:** TypeScript

---

## Phase 1: Project Setup & Infrastructure

### 1.1 Repo Scaffolding
- `npx create-next-app@latest` with TypeScript, Tailwind, App Router
- Configure `.gitignore` to exclude `.env*` (keep `.env.example`)
- Create `.env.example` with all required variables:
  ```
  NEXT_PUBLIC_SUPABASE_URL=        # Supabase project URL
  NEXT_PUBLIC_SUPABASE_ANON_KEY=   # Supabase anon/public key
  SUPABASE_SERVICE_ROLE_KEY=       # Server-only elevated key
  TMDB_API_KEY=                    # TMDB catalog API key
  AI_API_KEY=                      # AI provider API key
  AI_MODEL=                        # AI model name/key
  NEXT_PUBLIC_NAMESPACE_ID=        # Build isolation namespace
  NEXT_PUBLIC_DEV_USER_ID=         # Dev identity injection (dev/test only)
  ```

### 1.2 Supabase Schema (Migrations)
Create `/supabase/migrations/` with repeatable SQL migrations:

**`shows` table**
```sql
CREATE TABLE shows (
  id TEXT NOT NULL,
  namespace_id TEXT NOT NULL,
  user_id TEXT NOT NULL,
  PRIMARY KEY (id, namespace_id, user_id),
  title TEXT NOT NULL,
  show_type TEXT NOT NULL CHECK (show_type IN ('movie','tv','person','unknown')),
  external_ids JSONB,
  overview TEXT,
  genres TEXT[] DEFAULT '{}',
  tagline TEXT,
  homepage TEXT,
  original_language TEXT,
  spoken_languages TEXT[] DEFAULT '{}',
  languages TEXT[] DEFAULT '{}',
  poster_url TEXT,
  backdrop_url TEXT,
  logo_url TEXT,
  network_logos TEXT[] DEFAULT '{}',
  vote_average FLOAT,
  vote_count INT,
  popularity FLOAT,
  last_air_date TIMESTAMPTZ,
  first_air_date TIMESTAMPTZ,
  release_date TIMESTAMPTZ,
  runtime INT,
  budget BIGINT,
  revenue BIGINT,
  series_status TEXT,
  number_of_episodes INT,
  number_of_seasons INT,
  episode_run_time INT[] DEFAULT '{}',
  my_tags TEXT[] DEFAULT '{}',
  my_tags_update_date TIMESTAMPTZ,
  my_score FLOAT,
  my_score_update_date TIMESTAMPTZ,
  my_status TEXT CHECK (my_status IN ('active','next','later','done','quit','wait')),
  my_status_update_date TIMESTAMPTZ,
  my_interest TEXT CHECK (my_interest IN ('excited','interested')),
  my_interest_update_date TIMESTAMPTZ,
  ai_scoop TEXT,
  ai_scoop_update_date TIMESTAMPTZ,
  details_update_date TIMESTAMPTZ,
  creation_date TIMESTAMPTZ DEFAULT NOW(),
  is_test BOOLEAN DEFAULT FALSE,
  provider_data JSONB
);
```

**`cloud_settings` table**
```sql
CREATE TABLE cloud_settings (
  id TEXT DEFAULT 'globalSettings',
  namespace_id TEXT NOT NULL,
  user_id TEXT NOT NULL,
  PRIMARY KEY (id, namespace_id, user_id),
  user_name TEXT NOT NULL,
  version FLOAT,
  catalog_api_key TEXT,
  ai_api_key TEXT,
  ai_model TEXT
);
```

**`app_metadata` table**
```sql
CREATE TABLE app_metadata (
  namespace_id TEXT NOT NULL,
  user_id TEXT NOT NULL,
  PRIMARY KEY (namespace_id, user_id),
  data_model_version INT DEFAULT 3
);
```

Row Level Security (RLS): Enable RLS on all tables. In dev/benchmark mode, use `namespace_id` + `user_id` to partition — server routes enforce this via service role or authenticated sessions.

### 1.3 Scripts
- `npm run dev` — start Next.js dev server
- `npm test` — run test suite
- `npm run test:reset` — DELETE all rows WHERE `namespace_id = $NAMESPACE_ID` and `is_test = TRUE`
- `npm run db:migrate` — apply Supabase migrations

### 1.4 Identity & Namespace Model
- `NEXT_PUBLIC_NAMESPACE_ID` env var is the stable build identifier
- `NEXT_PUBLIC_DEV_USER_ID` injects a default user in dev/test (no OAuth required)
- Server routes accept `X-User-Id` header in development mode as identity injection
- All user-owned records partition on `(namespace_id, user_id)`
- Schema is designed for future OAuth: `user_id` is an opaque UUID string — no provider coupling

---

## Phase 2: Core Data Layer

### 2.1 Supabase Client Setup
- `/lib/supabase/client.ts` — browser client using anon key
- `/lib/supabase/server.ts` — server client using service role key (Next.js server components/routes only)

### 2.2 Show Repository
`/lib/shows/repository.ts`
- `getCollection(userId, namespaceId)` — all shows with a status
- `getShow(id, userId, namespaceId)` — single show
- `upsertShow(show, userId, namespaceId)` — create or merge
- `removeShow(id, userId, namespaceId)` — delete show + all My Data
- `getTags(userId, namespaceId)` — distinct tag list

**Merge logic** (matches PRD §5.5, storage-schema.md merge policy):
- Non-my fields: `selectFirstNonEmpty(newValue, oldValue)` — never overwrite with empty/null
- My fields: resolve by timestamp (newer wins)
- `details_update_date` = NOW() after merge
- `creation_date` set only on first insert

### 2.3 Settings Repository
`/lib/settings/repository.ts`
- `getCloudSettings(userId, namespaceId)`
- `upsertCloudSettings(settings, userId, namespaceId)` — conflict resolution by `version` (epoch seconds, newer wins)

### 2.4 TMDB Catalog Client
`/lib/catalog/tmdb.ts`
- `searchShows(query)` → `Show[]`
- `getShowDetail(id, mediaType)` → full `Show` (with transient fields: cast, crew, seasons, videos, recommendations, similar, images)
- `getPersonDetail(id)` → person with filmography
- `resolveShowById(externalId, mediaType)` → for AI recommendation resolution
- Map TMDB response → internal `Show` shape (title, showType, genres as strings, image URLs, etc.)
- Transient fields (cast, crew, seasons, videos, recommendations, similar) fetched but NOT persisted

---

## Phase 3: App Structure & Navigation

### 3.1 Layout
```
app/
  layout.tsx              # Root layout: nav sidebar + main area
  page.tsx                # Home (collection)
  find/
    page.tsx              # Find/Discover hub (Search | Ask | Alchemy)
  show/[id]/
    page.tsx              # Show Detail
  person/[id]/
    page.tsx              # Person Detail
  settings/
    page.tsx              # Settings & Your Data
```

### 3.2 Navigation Components
- **Sidebar/Nav Panel:**
  - "All Shows" (default filter)
  - Tag filters (one per tag; "No tags" if tagless shows exist)
  - Data filters: genre, decade, community score ranges
  - Media-type toggle: All / Movies / TV
  - "Find/Discover" entry point
  - "Settings" entry point
- **Media-type toggle** persists via `lastSelectedFilter` in UI state

---

## Phase 4: Collection Home

### 4.1 Collection Page (`app/page.tsx`)
- Fetch user collection, apply selected filter + media-type toggle
- Group into status sections:
  1. **Active** — larger tiles
  2. **Excited** (`status=later`, `interest=excited`)
  3. **Interested** (`status=later`, `interest=interested`)
  4. **Other** (Wait, Quit, Done, unclassified Later) — collapsed group
- Show tile: poster, title, status badge, rating indicator (§5.9)
- Empty states: no collection → prompt Search/Ask; filter yields none → "No results found"

### 4.2 Show Tile Component
- Poster image
- Title
- In-collection badge (if `myStatus` exists)
- Rating badge (if `myScore` exists)

---

## Phase 5: Find/Discover Hub

### 5.1 Hub Layout (`app/find/page.tsx`)
- Mode switcher: **Search | Ask | Alchemy**
- Renders active mode panel

### 5.2 Search Mode
- Text input → debounced TMDB search
- Results in poster grid
- In-collection items marked
- Selecting a show → navigate to `/show/[id]`
- "Search on launch" setting: auto-focus if enabled

### 5.3 Ask Mode (AI Chat)
- Chat UI: user/assistant message turns
- Welcome view: 6 random starter prompts; "Refresh" to get new ones
- AI response format: structured `{ commentary, showList }` where `showList` = `"Title::externalId::mediaType;;..."`
- Parse `showList` → resolve each via TMDB → render "Mentioned Shows" horizontal strip
- Tap mentioned show → navigate to Detail (fallback to Search if unresolvable)
- Context management: session-only; after ~10 messages, summarize older turns (maintain persona in summary)
- Reset clears session context
- **Ask About a Show** variant: seeded with show context from Detail page

### 5.4 Alchemy Mode
Flow:
1. **Select shows** — search + add (library or catalog); minimum 2
2. **Conceptualize Shows** → POST `/api/ai/concepts` with multiple shows → returns concept list
3. **Select concepts** — selectable chips, max 8; changing show selection clears concepts + results
4. **ALCHEMIZE!** → POST `/api/ai/recommendations` with concepts → returns 6 shows with reasons
5. **Results** — show tiles with AI reason; **More Alchemy!** button uses results as new inputs (chain)

---

## Phase 6: Show Detail Page

### 6.1 Page (`app/show/[id]/page.tsx`)
Fetch from TMDB (full detail) + merge with stored user data.

**Section order** (per detail_page_experience.md §3):
1. Header media carousel (backdrops/posters/logos; inline trailer if available; fallback gracefully)
2. Core facts row (year, runtime/seasons) + community score
3. Tag chips (My Tags) — in toolbar area
4. Overview text + Scoop toggle
5. "Ask about this show" CTA
6. Genres + languages
7. Traditional recommendations strand (TMDB similar/recommended)
8. Explore Similar (concepts → recs)
9. Streaming availability (providers)
10. Cast & Crew strands
11. Seasons (TV only)
12. Budget/Revenue (movies, when available)

### 6.2 My Relationship Controls
Status chips in toolbar (not scroll body): Active, Interested, Excited, Done, Quit, Wait
- Interested → `status=later, interest=interested`
- Excited → `status=later, interest=excited`
- Reselecting active status → confirmation modal → remove from collection, clear all My Data
  - `hideStatusRemovalConfirmation` suppresses after repeated confirmations

My Rating bar:
- Rating an unsaved show → auto-save as `status=done`

Tags:
- Tag picker; adding first tag to unsaved show → auto-save as `status=later, interest=interested`

### 6.3 AI Scoop
- Toggle button: "Give me the scoop!" / "Show the scoop" / "The Scoop" (based on state)
- On demand: POST `/api/ai/scoop` → streaming response
- Display "Generating…" during stream
- Cache: check `ai_scoop_update_date`; if >4h old, regenerate on next request
- Persist only if show is in collection; otherwise ephemeral for session

### 6.4 Explore Similar
1. **Get Concepts** → POST `/api/ai/concepts` (single show) → 8 concept chips
2. Select 1+ concepts
3. **Explore Shows** → POST `/api/ai/recommendations` (with concepts) → 5 shows with reasons
4. Show results as tiles with reason; tap to navigate to Detail

---

## Phase 7: Person Detail Page

`app/person/[id]/page.tsx`
- Fetch person from TMDB
- Image gallery, name, bio
- Analytics charts: average project ratings, top genres, projects-by-year
- Filmography grouped by year (credit cards)
- Tap credit → navigate to Show Detail

---

## Phase 8: Settings Page

`app/settings/page.tsx`

**App Settings:**
- Font size selector: XS | S | M | L | XL | XXL (persisted to local settings)
- "Search on launch" toggle

**User:**
- Username display/edit (synced via `cloud_settings`)

**AI:**
- AI provider API key input (never committed; stored in `cloud_settings`, server-synced)
- AI model selection
- Note: in benchmark mode, `AI_API_KEY` and `AI_MODEL` env vars take precedence

**Integrations:**
- TMDB API key input (stored in `cloud_settings`)

**Your Data:**
- **Export My Data** — generates `.zip` containing JSON backup of all saved shows + My Data (dates ISO-8601)
- Import/Restore: noted as future feature, not implemented

---

## Phase 9: API Routes (Next.js Route Handlers)

All routes under `app/api/`:

### 9.1 Collection CRUD
- `GET /api/shows` — get collection
- `PUT /api/shows/[id]` — upsert show (merge)
- `DELETE /api/shows/[id]` — remove show

### 9.2 Settings
- `GET /api/settings` — get cloud settings
- `PUT /api/settings` — upsert settings

### 9.3 AI Endpoints
- `POST /api/ai/scoop` — generate Scoop (streaming SSE)
  - Body: `{ showId, showTitle, showOverview, userStatus?, userRating?, userTags? }`
  - Returns: streaming text
- `POST /api/ai/ask` — chat turn
  - Body: `{ message, history, userLibrarySummary, seedShow? }`
  - Returns: `{ commentary, showList }`
- `POST /api/ai/concepts` — extract concepts
  - Body: `{ shows: [{ title, overview, genres }] }`
  - Returns: `{ concepts: string[] }` (8 for single show, larger pool for multi-show)
- `POST /api/ai/recommendations` — concept-based recs
  - Body: `{ concepts: string[], sourceShows: string[], userLibrarySummary }`
  - Returns: `{ recommendations: [{ title, externalId, mediaType, reason }] }`

### 9.4 Catalog Proxy
- `GET /api/catalog/search?q=` — TMDB search (server-proxied to keep API key server-side)
- `GET /api/catalog/show/[id]?type=movie|tv` — full show detail
- `GET /api/catalog/person/[id]` — person detail
- `GET /api/catalog/resolve/[externalId]?type=` — resolve AI-recommended show

### 9.5 Data Export
- `GET /api/export` — returns `.zip` of user's collection as JSON

### 9.6 Identity (Dev Mode)
- All API routes read `X-User-Id` header (dev/test only) or `NEXT_PUBLIC_DEV_USER_ID` env var
- `namespace_id` from `NEXT_PUBLIC_NAMESPACE_ID` env var
- Clearly documented; gated by `NODE_ENV !== 'production'`

---

## Phase 10: AI Prompt Implementation

### Shared System Constraints (all surfaces)
- Stay within TV/movies domain
- Spoiler-safe by default
- Opinionated, honest (acknowledge mixed reception)
- Specific vibe/craft reasoning, not generic genre summaries

### Scoop Prompt
- System: persona as chatty TV/movie nerd friend; mini blog-post format
- Sections: personal take → honest stack-up → "The Scoop" emotional centerpiece → fit/warnings → "Worth it?" verdict
- Length: ~150–350 words; stream progressively

### Ask Prompt
- System: conversational discovery friend; taste-aware via injected library summary
- Include recent conversation turns; summarize older turns in same persona
- Output structured JSON: `{ commentary, showList }` with `showList` in `Title::id::type;;` format
- Parser: strict split on `;;` then `::`, retry with stricter formatting on parse failure

### Concepts Prompt
- Output: bullet list only; 1–3 words per concept; no explanation; no plot/spoilers
- For multi-show: concepts shared across all inputs
- 8 concepts for single-show; larger pool for Alchemy

### Recommendations Prompt
- List of shows with reasons citing specific concepts
- Each reason: ~1–3 sentences
- Must return `externalId` + `mediaType` for catalog resolution
- Fallback: if unresolvable → show non-interactive or hand off to Search

### Conversation Summarization
- After ~10 messages, summarize older turns into 1–2 sentences
- Summary maintains same persona/tone (not sterile system voice)

---

## Phase 11: Catalog Integration (TMDB)

### Show Mapping
- TMDB movie/tv → internal `Show` shape
- `showType`: if `name` field → `tv`; if `title` field → `movie`; else `unknown`
- Genres: map genre IDs → genre name strings
- Images: construct full URLs from TMDB base URL + path
- Logos: pick best-rated English logo deterministically
- Transient fields (cast, crew, seasons, videos, recommendations, similar): decoded for UI, NOT persisted
- External IDs stored in `externalIds` JSONB for AI recommendation resolution

### AI Recommendation Resolution (§5.8)
1. AI returns `{ title, externalId, mediaType }`
2. Call TMDB by `externalId` if provided
3. Accept first result where title matches case-insensitively
4. If found → real selectable Show (can carry AI `reason` as transient text)
5. If not found → show non-interactive or hand off to Search

---

## Phase 12: Data Business Rules Implementation

### Auto-save Triggers (§5.2, §5.3)
| Action | Status | Interest |
|---|---|---|
| Set status explicitly | as selected | as selected (or Interested if Later without explicit interest) |
| Choose Interested chip | Later | Interested |
| Choose Excited chip | Later | Excited |
| Rate unsaved show | Done | — |
| Add tag to unsaved show | Later | Interested |

### Collection Removal (§5.4)
- Reselect active status → confirm → DELETE show row → all My Data cleared
- Warning modal with "don't ask again" option (`hideStatusRemovalConfirmation`)

### Merge on Re-add (§5.5)
- Preserve My Data fields (status, interest, tags, rating, aiScoop)
- Refresh public catalog metadata using `selectFirstNonEmpty`
- Resolve My field conflicts by timestamp (newer wins)

### Timestamps (§5.6)
- Update `my_*_update_date` on every My Data change (used for conflict resolution and AI cache freshness)

---

## Phase 13: State Management

- **Server state:** React Server Components + Server Actions where possible; SWR or React Query for client-side catalog fetches
- **Session state (AI):** React context or local state per session (Ask chat history, Alchemy state, Explore Similar state) — NOT persisted to backend
- **UI state:** localStorage for `hideStatusRemovalConfirmation`, `statusRemovalCountKey`, `lastSelectedFilter`, `autoSearch`, `fontSize`
- **Collection:** fetched server-side; client invalidates on mutation

---

## Phase 14: Testing Infrastructure

### Test Reset
`npm run test:reset` executes:
```sql
DELETE FROM shows WHERE namespace_id = $NAMESPACE_ID AND is_test = TRUE;
DELETE FROM cloud_settings WHERE namespace_id = $NAMESPACE_ID;
```

### Test Strategy
- Unit tests: merge logic, mapping functions, AI output parsers
- Integration tests: API route handlers against real Supabase (test namespace)
- No Docker required; connect to hosted Supabase via env vars

---

## Key Cross-Cutting Constraints

1. **User data always wins** — My fields take precedence over catalog refreshes
2. **Backend is source of truth** — clearing localStorage must not lose collection data
3. **Namespace isolation** — every DB query filters on `namespace_id`
4. **No secrets in client code** — TMDB + AI API keys server-side only; only Supabase anon key is public
5. **OAuth-ready schema** — `user_id` is opaque UUID; no provider coupling; replacing dev injection with real OAuth = config change only
6. **AI outputs actionable** — every recommendation resolves to a real catalog item or degrades gracefully

---

## File Structure (High-Level)

```
/
├── app/
│   ├── layout.tsx
│   ├── page.tsx                    # Collection home
│   ├── find/page.tsx               # Find/Discover hub
│   ├── show/[id]/page.tsx          # Show detail
│   ├── person/[id]/page.tsx        # Person detail
│   ├── settings/page.tsx           # Settings
│   └── api/
│       ├── shows/[id]/route.ts
│       ├── settings/route.ts
│       ├── ai/scoop/route.ts
│       ├── ai/ask/route.ts
│       ├── ai/concepts/route.ts
│       ├── ai/recommendations/route.ts
│       ├── catalog/search/route.ts
│       ├── catalog/show/[id]/route.ts
│       ├── catalog/person/[id]/route.ts
│       ├── catalog/resolve/[id]/route.ts
│       └── export/route.ts
├── components/
│   ├── layout/Sidebar.tsx
│   ├── show/ShowTile.tsx
│   ├── show/StatusChips.tsx
│   ├── show/RatingBar.tsx
│   ├── show/TagPicker.tsx
│   ├── show/ScoopPanel.tsx
│   ├── show/ExploreSimlar.tsx
│   ├── find/SearchPanel.tsx
│   ├── find/AskPanel.tsx
│   ├── find/AlchemyPanel.tsx
│   └── person/PersonDetail.tsx
├── lib/
│   ├── supabase/client.ts
│   ├── supabase/server.ts
│   ├── shows/repository.ts
│   ├── shows/merge.ts
│   ├── settings/repository.ts
│   ├── catalog/tmdb.ts
│   ├── catalog/mapper.ts
│   └── ai/prompts.ts
├── supabase/
│   └── migrations/
│       └── 001_initial_schema.sql
├── .env.example
└── package.json
```

---

## Implementation Order

1. **Phase 1** — Repo setup, env vars, Supabase migrations
2. **Phase 2** — Data layer (Supabase client, Show/Settings repositories, merge logic)
3. **Phase 11** — TMDB catalog client + mapper
4. **Phase 9** — API routes (catalog proxy, collection CRUD, settings)
5. **Phase 3** — App layout + navigation shell
6. **Phase 4** — Collection home
7. **Phase 5.2** — Search mode
8. **Phase 6** — Show Detail (full page with all sections)
9. **Phase 10 + Phase 5.3** — AI prompts + Ask mode
10. **Phase 5.4** — Alchemy mode
11. **Phase 7** — Person detail
12. **Phase 8** — Settings page + data export
13. **Phase 14** — Test reset script + integration tests
