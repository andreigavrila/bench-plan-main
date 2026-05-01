# Implementation Plan

> **Scope:** This is a planning document only. No source files are created here.  
> **Deliverable required by:** `1-START_HERE.md`  
> **Source documents read:** `product_prd.md`, `infra_rider_prd.md`, `supporting_docs/ai_prompting_context.md`, `supporting_docs/ai_voice_personality.md`, `supporting_docs/concept_system.md`, `supporting_docs/detail_page_experience.md`, `supporting_docs/discovery_quality_bar.md`, `supporting_docs/technical_docs/storage-schema.md`, `supporting_docs/technical_docs/storage-schema.ts`

---

## 1. Executive Summary

The product is a **personal TV + movie companion** that lets users build an opinionated watchlist and powers discovery through four paths: Search, AI Chat ("Ask"), concept blending ("Alchemy"), and per-show concept discovery ("Explore Similar"). All user data is owned server-side, scoped by `(namespace_id, user_id)`, and must survive client cache clears without data loss.

---

## 2. Technology Stack

| Layer | Choice | Rationale |
|---|---|---|
| Application runtime | **Next.js (latest stable)** | Mandated by `infra_rider_prd.md` §2 |
| Persistence layer | **Supabase (hosted)** | Mandated by `infra_rider_prd.md` §2; prefers hosted; no Docker assumption |
| Supabase client | `@supabase/supabase-js` | Official library; anon key in browser, service role key server-only |
| AI provider | Pluggable via env var (`AI_API_KEY`, `AI_MODEL`) | Must not be committed; user can override from Settings |
| Content catalog | External API (key via env var) | TMDB or equivalent; provider-agnostic in code |
| Language | TypeScript | Type-safe; schema already expressed in `.ts` |
| Styling | Vanilla CSS / CSS Modules | Per project web standards |

---

## 3. Repository Structure

```
/
├── .env.example                  # Required — all env vars with comments
├── .gitignore                    # Excludes .env* except .env.example
├── next.config.ts
├── package.json
├── tsconfig.json
│
├── supabase/
│   ├── migrations/               # Numbered SQL migration files (deterministic schema)
│   └── seed.sql                  # Optional test fixtures
│
├── scripts/
│   ├── dev.sh (or npm scripts)   # start, test, test:reset
│
├── src/
│   ├── app/                      # Next.js App Router pages + layouts
│   │   ├── layout.tsx
│   │   ├── page.tsx              # Collection Home
│   │   ├── find/
│   │   │   ├── page.tsx          # Find hub (Search/Ask/Alchemy tabs)
│   │   │   ├── search/
│   │   │   ├── ask/
│   │   │   └── alchemy/
│   │   ├── show/[id]/page.tsx    # Show Detail
│   │   ├── person/[id]/page.tsx  # Person Detail
│   │   └── settings/page.tsx
│   │
│   ├── components/               # Reusable UI components
│   │   ├── show/                 # ShowTile, StatusChips, RatingBar, TagPicker, etc.
│   │   ├── ai/                   # ScoopPanel, AskChat, AlchemyFlow, ConceptChips
│   │   ├── layout/               # Sidebar, FilterPanel, NavBar
│   │   └── common/               # MediaCarousel, PosterGrid, PersonCard, etc.
│   │
│   ├── lib/
│   │   ├── supabase/             # Client + server Supabase instances
│   │   ├── catalog/              # External catalog API client (TMDB adapter)
│   │   ├── ai/                   # AI provider client + prompt builders
│   │   └── schema/               # TypeScript types mirroring storage-schema.ts
│   │
│   ├── server/                   # Next.js Route Handlers (API layer)
│   │   ├── shows/                # CRUD for user's collection
│   │   ├── catalog/              # Proxy to external catalog
│   │   ├── ai/                   # Scoop, Ask, Concepts, Alchemy endpoints
│   │   └── settings/             # CloudSettings sync
│   │
│   └── hooks/                    # React hooks (useCollection, useFilter, etc.)
│
└── tests/
    ├── unit/
    ├── integration/
    └── reset.ts                  # Namespace-scoped data reset for test:reset script
```

---

## 4. Environment Variables (`.env.example`)

```bash
# Supabase
NEXT_PUBLIC_SUPABASE_URL=          # Hosted Supabase project URL
NEXT_PUBLIC_SUPABASE_ANON_KEY=     # Anon/public key (safe for browser)
SUPABASE_SERVICE_ROLE_KEY=         # Elevated key — server-only, never expose to client

# External Catalog (e.g., TMDB)
CATALOG_API_KEY=                   # Catalog read API key

# AI Provider
AI_API_KEY=                        # Default AI API key (user may override in Settings)
AI_MODEL=                          # Default model identifier

# Identity & Isolation
NAMESPACE_ID=                      # Stable build/run namespace (UUID or slug)
DEFAULT_USER_ID=                   # Dev-mode fixed user identity

# App mode
NODE_ENV=development               # development | production
```

**Rules:**
- Browser code uses only `NEXT_PUBLIC_*` vars.
- `SUPABASE_SERVICE_ROLE_KEY` and `AI_API_KEY` are passed only through server-side route handlers.
- No secrets committed to repo.

---

## 5. Database Schema (Supabase / PostgreSQL)

### 5.1 Core Tables

#### `shows`
Stores the user-collection record for a show, scoped by `(namespace_id, user_id)`.

```sql
CREATE TABLE shows (
  id                      TEXT NOT NULL,
  namespace_id            TEXT NOT NULL,
  user_id                 TEXT NOT NULL,

  -- Catalog meta
  title                   TEXT NOT NULL,
  show_type               TEXT NOT NULL CHECK (show_type IN ('movie','tv','person','unknown')),
  external_ids            JSONB,
  overview                TEXT,
  genres                  TEXT[]   DEFAULT '{}',
  tagline                 TEXT,
  homepage                TEXT,
  original_language       TEXT,
  spoken_languages        TEXT[]   DEFAULT '{}',
  languages               TEXT[]   DEFAULT '{}',

  -- Images
  poster_url              TEXT,
  backdrop_url            TEXT,
  logo_url                TEXT,
  network_logos           TEXT[]   DEFAULT '{}',

  -- Ratings / popularity
  vote_average            NUMERIC,
  vote_count              INTEGER,
  popularity              NUMERIC,

  -- Dates (ISO-8601 strings)
  release_date            TEXT,
  first_air_date          TEXT,
  last_air_date           TEXT,

  -- Movie-specific
  runtime                 INTEGER,
  budget                  BIGINT,
  revenue                 BIGINT,

  -- TV-specific
  series_status           TEXT,
  number_of_episodes      INTEGER,
  number_of_seasons       INTEGER,
  episode_run_time        INTEGER[] DEFAULT '{}',

  -- User data ("my*")
  my_tags                 TEXT[]   DEFAULT '{}',
  my_tags_update_date     TIMESTAMPTZ,
  my_score                NUMERIC,
  my_score_update_date    TIMESTAMPTZ,
  my_status               TEXT CHECK (my_status IN ('active','next','later','done','quit','wait')),
  my_status_update_date   TIMESTAMPTZ,
  my_interest             TEXT CHECK (my_interest IN ('excited','interested')),
  my_interest_update_date TIMESTAMPTZ,

  -- AI
  ai_scoop                TEXT,
  ai_scoop_update_date    TIMESTAMPTZ,

  -- Management
  details_update_date     TIMESTAMPTZ,
  creation_date           TIMESTAMPTZ DEFAULT NOW(),
  is_test                 BOOLEAN     DEFAULT FALSE,

  -- Providers
  provider_data           JSONB,

  PRIMARY KEY (id, namespace_id, user_id)
);

CREATE INDEX shows_namespace_user ON shows (namespace_id, user_id);
CREATE INDEX shows_my_status      ON shows (namespace_id, user_id, my_status);
CREATE INDEX shows_my_tags        ON shows USING GIN (my_tags);
```

#### `cloud_settings`
```sql
CREATE TABLE cloud_settings (
  id              TEXT    NOT NULL DEFAULT 'globalSettings',
  namespace_id    TEXT    NOT NULL,
  user_id         TEXT    NOT NULL,
  user_name       TEXT    NOT NULL,
  version         NUMERIC NOT NULL,  -- epoch seconds for conflict resolution
  catalog_api_key TEXT,
  ai_api_key      TEXT,
  ai_model        TEXT    NOT NULL DEFAULT '',
  PRIMARY KEY (id, namespace_id, user_id)
);
```

#### `app_metadata`
```sql
CREATE TABLE app_metadata (
  namespace_id        TEXT    NOT NULL,
  user_id             TEXT    NOT NULL,
  data_model_version  INTEGER NOT NULL DEFAULT 3,
  PRIMARY KEY (namespace_id, user_id)
);
```

### 5.2 Row-Level Security (RLS)

All tables enable RLS. In dev mode, user identity is injected via a server-side session variable set from the `DEFAULT_USER_ID` env var. Policy: rows are accessible only where `namespace_id = current_setting('app.namespace_id')` AND `user_id = current_setting('app.user_id')`.

This design means switching to real OAuth later requires only updated auth wiring — no schema redesign.

### 5.3 Migration Strategy

- Migrations live in `supabase/migrations/` as numbered SQL files (e.g., `0001_initial_schema.sql`).
- Running `npm run db:migrate` applies all pending migrations in order.
- `npm run test:reset` deletes all rows where `namespace_id = $NAMESPACE_ID` — no global teardown.
- `is_test = TRUE` rows can also be targeted for finer-grained cleanup.

---

## 6. Identity & Isolation Model

### 6.1 Namespace

A stable `NAMESPACE_ID` (UUID) is set in the environment. Every DB write includes this value. Two builds with different `NAMESPACE_ID`s cannot read each other's data.

### 6.2 User Identity (Dev Mode)

In dev/test mode, a `DEFAULT_USER_ID` env var sets the active user. Server route handlers read this and pass it to Supabase via `set_config('app.user_id', ...)`. The UI may also offer a dev-only "identity selector" dropdown (clearly gated behind `NODE_ENV !== 'production'`).

### 6.3 Production Migration Path

When real OAuth is added:
1. Auth provider returns a JWT with a `sub` claim → becomes `user_id`.
2. Server routes extract `user_id` from the JWT instead of `DEFAULT_USER_ID`.
3. No schema changes needed.

---

## 7. NPM Scripts

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "test": "jest --runInBand",
    "test:reset": "ts-node scripts/reset-namespace.ts",
    "db:migrate": "supabase db push",
    "db:seed": "psql $DATABASE_URL -f supabase/seed.sql"
  }
}
```

---

## 8. Data Layer Architecture

### 8.1 Server Route Handlers (API)

All DB reads/writes happen in Next.js Route Handlers (`/app/api/...`) using the **service role** Supabase client. The browser never holds an elevated key.

Key route groups:

| Route | Purpose |
|---|---|
| `GET /api/shows` | List collection (with filter params) |
| `GET /api/shows/[id]` | Get single show |
| `PUT /api/shows/[id]` | Upsert (create or merge) a show |
| `DELETE /api/shows/[id]` | Remove show + clear My Data |
| `GET /api/catalog/search` | Proxy to external catalog search |
| `GET /api/catalog/[id]` | Proxy to external catalog detail |
| `POST /api/ai/scoop` | Generate/return AI Scoop |
| `POST /api/ai/ask` | Chat turn (with optional show context) |
| `POST /api/ai/concepts` | Generate concepts for 1+ shows |
| `POST /api/ai/recommend` | Concept-based recommendations |
| `GET /api/settings` | Get CloudSettings |
| `PUT /api/settings` | Upsert CloudSettings |

### 8.2 Merge Logic (Show Upsert)

When a show is upserted:
1. Fetch existing record from DB.
2. **Catalog fields** (`overview`, `genres`, `poster_url`, etc.): `selectFirstNonEmpty(newValue, existing)` — never overwrite non-empty with empty/nil.
3. **My fields** (`my_tags`, `my_score`, `my_status`, `my_interest`): compare update timestamps; keep newer value.
4. Set `details_update_date = NOW()`.
5. Preserve `creation_date` from original record.

### 8.3 Client-Side Caching

React state and SWR/React Query patterns are used for in-session caching. These are performance aids only — no user data is stored exclusively client-side. Clearing browser storage retains all data in Supabase.

---

## 9. Show Data Model Details

### 9.1 Status System

| Status | Meaning | Paired interest? |
|---|---|---|
| `active` | Currently watching | No |
| `later` | Saved for later | Yes (interested / excited) |
| `wait` | Paused/waiting | No |
| `done` | Completed | No |
| `quit` | Abandoned | No |
| `next` | Hidden queue item (data model only, not first-class UI) | No |

### 9.2 Saving Triggers & Defaults

| Action | Resulting status | Resulting interest |
|---|---|---|
| Explicit status chip tap | As chosen | As chosen |
| Interested chip | `later` | `interested` |
| Excited chip | `later` | `excited` |
| Add rating (unsaved show) | `done` | — |
| Add tag (unsaved show) | `later` | `interested` |

### 9.3 Removal Semantics

Reselecting the current status triggers a confirmation. On confirm:
- Row deleted from `shows` table (all My Data gone).
- UI: confirmation suppressed after repeated removals (tracked in local UI state: `hideStatusRemovalConfirmation`, `statusRemovalCountKey`).

### 9.4 Tile Indicators

Each Show tile rendering checks:
- `my_status !== null` → show "in collection" badge.
- `my_score !== null` → show user rating badge.

---

## 10. Feature Implementation Plans

### 10.1 Collection Home

**Data:** `GET /api/shows` with `namespace_id + user_id`. Returns all collection shows.

**Rendering:**
- Group by status: Active → Excited (Later+Excited) → Interested (Later+Interested) → Other (Wait/Done/Quit/unclassified Later).
- Active group: larger tiles.
- Media-type toggle (All / Movies / TV) applied on top of status grouping.
- Filter panel (sidebar): All Shows, per-tag filters, genre/decade/score filters.
- "No tags" filter appears only if tagless shows exist.

**Empty states:**
- No shows in collection → prompt to Search or Ask.
- Filter yields nothing → "No results found."

**Local UI state:** `lastSelectedFilter` stored in browser (key-value, not Supabase). Lost on cache clear is acceptable (UI preference, not user data).

### 10.2 Search (Find → Search)

**Data:** `GET /api/catalog/search?q=...` proxies to external catalog API.

**Behavior:**
- Text search, poster grid results.
- Results overlay in-collection status (cross-reference with local collection cache).
- Tap result → Show Detail.
- "Search on launch" setting: if `autoSearch = true`, Find view opens with Search tab active.

**No AI voice** — pure catalog search.

### 10.3 Ask (Find → Ask)

**Data:** `POST /api/ai/ask`

**Chat Flow:**
- Send `{ message, sessionHistory, userLibrary, handoffShow? }`.
- Server builds prompt with AI personality (joy-forward, opinionated, spoiler-safe).
- Response: `{ commentary, showList }` (structured output per `ai_prompting_context.md` §3.2).
- Parse `showList` as `Title::externalId::mediaType;;...`.
- Resolve each to a real catalog show via `GET /api/catalog/[id]`.
- Render "mentioned shows" horizontal strip below chat.

**Welcome state:** 6 randomly selected starter prompts from a pool of 80 (from AI personality spec). Refresh button available.

**Context management:**
- After ~10 messages, older turns are summarized (1–2 sentence summaries, matching chat persona).
- Summary replaces older turns in the context sent to AI.

**"Ask About a Show":**
- Launched from Show Detail with show context pre-seeded.
- Same API endpoint, `handoffShow` field populated.

**Explore Search Chat variant:** shorter, performative, mirrors show's emotional color (per personality spec §4.3).

### 10.4 Alchemy (Find → Alchemy)

**Flow (5 steps):**
1. **Show selection:** User picks ≥2 shows (from library or catalog search).
2. **Conceptualize:** `POST /api/ai/concepts` with selected show IDs. Returns bullet list of shared concepts.
3. **Concept selection:** User selects 1–8 concepts (chips; selecting/unselecting clears downstream results).
4. **Alchemize:** `POST /api/ai/recommend` with selected concepts + show context. Returns 6 recommendations.
5. **Chain:** "More Alchemy!" resets input shows to the 6 results and loops from step 1.

**Recommendation resolution:** Each of the 6 recs must resolve to a real catalog item. Non-resolved items shown as non-interactive.

**Session data:** Not persisted. Cleared on leaving Alchemy.

**UX rules:** Backtracking (changing shows) clears concepts and results. Clear step indicators.

### 10.5 Show Detail Page

**Data:** `GET /api/catalog/[id]` (catalog detail, transient) + local collection state.

**Section order (per `detail_page_experience.md`):**
1. Header media carousel (backdrops/posters/logos/inline trailers; graceful fallback)
2. Core facts row (year, runtime or seasons count) + community score bar
3. My Tags chip list
4. Overview text + Scoop toggle/stream
5. "Ask about this show" CTA
6. Genres + languages
7. Traditional recommendations strand (catalog-provided similar shows)
8. Explore Similar (concepts → recs)
9. Streaming availability (providers)
10. Cast & Crew strands → Person Detail
11. Seasons (TV only)
12. Budget/Revenue (movies, when available)

**Status/interest chips:** In toolbar (sticky), not in scroll body. Reselect = removal confirmation.

**AI Scoop:**
- Toggle copies: "Give me the scoop!" → "Show the scoop" (cached) → "The Scoop" (open).
- `POST /api/ai/scoop` with show context; response streams progressively.
- Freshness rule: if `ai_scoop_update_date` is older than 4 hours, regenerate on next demand.
- Persistence: saved to DB only if show is in collection. Unsaved show = ephemeral scoop.

**Explore Similar:**
- "Get Concepts" → `POST /api/ai/concepts` (single show) → concept chips appear.
- User selects ≥1 concepts → "Explore Shows" → `POST /api/ai/recommend` → 5 recs.
- Recs resolved to real catalog items.

**Transient data** (not persisted): cast, crew, seasons, videos, recommendations, images. Fetched fresh each Detail load.

### 10.6 Person Detail Page

**Data:** `GET /api/catalog/person/[id]` (catalog detail).

**Sections:**
- Image gallery + bio.
- Analytics charts: average project ratings by year, top genres, projects-per-year.
- Filmography grouped by year.
- Tapping a credit → Show Detail for that show.

### 10.7 Settings & Your Data

**Local settings (browser key-value):**
- Font size: `XS | S | M | L | XL | XXL`.
- Search on launch: `autoSearch` boolean.

**Synced settings (via `cloud_settings` in Supabase):**
- Username.
- AI API key + model selection (key never committed; user-supplied or from env).
- Catalog API key.

**Export / Backup:**
- `GET /api/export` returns a `.zip` with a JSON snapshot of all shows + My Data for `(namespace_id, user_id)`.
- JSON uses ISO-8601 dates.
- Import/Restore: documented as future feature, not yet implemented.

---

## 11. AI Integration Architecture

### 11.1 Server-Side AI Client

All AI calls are made from Next.js Route Handlers (never from browser code directly). The route handler:
1. Reads `AI_API_KEY` and `AI_MODEL` from env (or user-supplied values from `cloud_settings`).
2. Builds prompt using persona + surface-specific instructions.
3. Calls AI provider.
4. Returns structured response to browser.

### 11.2 AI Personality (Cross-Cutting)

All prompts must instantiate the **same persona**: fun, chatty TV/movie nerd friend. Tone sliders per spec: 70% friend / 30% critic, 60% hype / 40% measured, spoiler-safe by default, concise by default (lush for Scoop).

Surface-specific adaptations:
- **Scoop:** ~150–350 words; mini blog post; sections: personal take, honest stack-up, the Scoop paragraph (centerpiece), fit/warnings, "Worth it?" gut check.
- **Ask:** 1–3 tight paragraphs + list; low-friction, fast, opinionated.
- **Explore Search Chat:** short, performative, mirrors show's emotional color.
- **Concepts:** bullet list, 1–3 words each, evocative, no explanations.
- **Concept Recs:** ~1–3 sentence reason per rec citing specific concepts.

### 11.3 Structured Output for Ask (Mentioned Shows)

Response format contract:
```
{
  commentary: string,           // User-visible response text
  showList: string              // "Title::externalId::mediaType;;..."
}
```
Parser must be exact-match with renderer. On parse failure: retry once with stricter instructions; otherwise fall back to unstructured commentary + Search handoff.

### 11.4 Recommendation Resolution

For every AI-returned title:
1. Use `externalId` to look up in catalog if present.
2. Verify: catalog result title matches AI title (case-insensitive).
3. If matched: show becomes a selectable Show tile with AI reason as transient text.
4. If not matched: show as non-interactive placeholder or hand to Search.

### 11.5 Concept Generation Counts

| Surface | Input shows | Concepts returned | Recs returned |
|---|---|---|---|
| Explore Similar | 1 | ~8 (larger pool) | 5 |
| Alchemy | ≥2 | Larger pool (concepts shared across all inputs) | 6 |

User selection cap: 8 concepts max in both surfaces.

---

## 12. Cross-Cutting Rules Implementation

| Rule | Implementation approach |
|---|---|
| User's version takes precedence | Merge: My fields resolved by timestamp; catalog fields use selectFirstNonEmpty |
| Discovery must be actionable | All recommendation routes resolve external IDs before returning |
| Taste-aware AI | Library + My Data included in AI context payload for every AI surface |
| Spoiler-safe default | Embedded as constraint in all AI system prompts |
| Implicit saves feel natural | Auto-save on rating/tagging with correct defaults (§9.2) |
| Your data is yours | Export route produces full zip backup |
| Identity is explicit | Every persisted record scoped to `(namespace_id, user_id)` |
| Runs are isolated | `namespace_id` partitions all DB data; `test:reset` deletes by namespace |
| Backend is source of truth | No exclusive client-only persistence; clearing browser storage loses nothing permanent |

---

## 13. Data Sync & Conflict Resolution

- `cloud_settings` uses `version` (epoch seconds) for last-write-wins on synced settings.
- `shows` My fields use per-field update timestamps. On merge: newer timestamp wins.
- Duplicate show detection: same `(id, namespace_id, user_id)` is an UPDATE, not INSERT.
- Cross-device: browser fetches fresh from Supabase on load; no offline persistence required.

---

## 14. Data Model Migration (Future-Proofing)

- `app_metadata.data_model_version` (currently 3) tracks schema generation.
- On app boot, server checks `data_model_version`. If mismatched, runs migration logic.
- Old shows are brought forward into new model automatically (no user intervention).
- Migration scripts live in `supabase/migrations/` with clear version numbers.

---

## 15. Phased Delivery Roadmap

### Phase 1 — Infrastructure & Core Data (Foundation)
- Supabase schema + RLS + migrations.
- `.env.example`, `.gitignore`, npm scripts (dev, test, test:reset).
- Namespace/user identity injection (dev mode).
- Server route handlers for shows CRUD.
- Supabase client setup (anon key browser, service role server).

### Phase 2 — Collection Home + Show Detail (Core UX)
- Collection Home: status-grouped display, filter sidebar, media-type toggle.
- Show Detail: full section layout, status/interest chips, rating bar, tag picker.
- Show tile indicators (in-collection badge, rating badge).
- All auto-save business rules (rating → Done, tag → Later+Interested).
- Removal confirmation flow.

### Phase 3 — Search + Catalog Integration
- External catalog proxy routes.
- Search UI (text input, poster grid, in-collection markers).
- Catalog detail fetch for Show Detail transient data.
- "Search on launch" setting.

### Phase 4 — AI: Scoop + Ask
- AI client (server-side only).
- Scoop: generation, streaming, 4-hour freshness, conditional persistence.
- Ask: chat UI, structured output parsing, mentioned shows strip, welcome prompts, context summarization.
- "Ask About a Show" seeded-context variant.

### Phase 5 — AI: Concepts + Alchemy + Explore Similar
- Concept generation route (single-show + multi-show).
- Concept chip UI (selectable, ≤8 selection cap).
- Explore Similar flow (on Show Detail).
- Alchemy flow: show picker, conceptualize, select, alchemize, chain.
- Recommendation resolution engine.

### Phase 6 — Person Detail + Supporting Features
- Person Detail (gallery, bio, charts, filmography).
- Streaming availability display (providers).
- Seasons strand (TV), Budget/Revenue (movies).
- AI Scoop persistence rules validation.

### Phase 7 — Settings + Export + Polish
- Settings page (all groups).
- CloudSettings sync via Supabase.
- Export/Backup zip route.
- Font size preference, autoSearch setting.
- Dev identity selector (gated behind `NODE_ENV !== 'production'`).
- Data continuity: migration logic on app boot.

### Phase 8 — Tests + QA
- Unit tests for merge logic, auto-save rules, structured output parsing.
- Integration tests for collection CRUD, AI routes (mocked provider).
- Discovery quality checks against `discovery_quality_bar.md` rubric.
- `test:reset` script validation.

---

## 16. Open Questions (From PRD)

These are deferred/optional and should not be implemented without explicit direction:

- **Next status:** Should it become a first-class UI element? (Currently data-model only.)
- **Named custom lists:** Beyond tags (e.g., "Weekend Watchlist").
- **Auto-save on AI Scoop:** Should generating Scoop for an unsaved show implicitly save it?
- **Explicit Unrated state:** vs `my_score = null`.
- **Import/Restore:** From backup zip (not yet implemented).
- **Save/Share Alchemy sessions** as reusable blends.
- **myStatus sidebar filters:** Model supports it; UI spec defers it.

---

## 17. Key Risks & Mitigations

| Risk | Mitigation |
|---|---|
| AI hallucinated show titles | Strict resolution check against catalog by external ID; fallback to non-interactive or Search |
| AI structured output parse failure | Retry with stricter instructions; graceful unstructured fallback |
| Supabase RLS misconfiguration leaking data across namespaces | Unit tests asserting cross-namespace isolation; test:reset validates scoping |
| Cloud settings sync conflict | `version` epoch-seconds field ensures last-write-wins; no silent data loss |
| API key leakage to client bundle | Only `NEXT_PUBLIC_*` vars exposed to browser; service role key server-only |
| Breaking data model changes | `dataModelVersion` migration gate; forward-migration logic required for any schema change |
