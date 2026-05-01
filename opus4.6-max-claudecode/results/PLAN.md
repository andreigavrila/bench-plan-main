# Implementation Plan

## 0. Overview

This plan describes how to build a personal TV/movie companion app using **Next.js** (latest stable) and **Supabase** as mandated by the Infrastructure Rider PRD. The app lets users collect, organize, rate, and discover entertainment through traditional browse/search and three AI-powered discovery surfaces (Ask, Alchemy, Explore Similar). An external catalog (TMDB) provides public show data; a configurable AI provider powers the personality-driven discovery features.

The plan is organized into seven phases. Each phase produces a deployable increment. Phases 1–3 establish the foundation (infra, data, catalog integration). Phases 4–6 layer the core product features. Phase 7 covers polish, export, and hardening.

---

## 1. Project Scaffolding & Infrastructure

### 1.1 Repository Bootstrap

- Initialize a Next.js project (App Router, TypeScript, Tailwind CSS).
- Configure ESLint, Prettier, and a `tsconfig.json` with strict mode.
- Create `.env.example` with all required variables (commented):
  ```
  # Supabase
  NEXT_PUBLIC_SUPABASE_URL=
  NEXT_PUBLIC_SUPABASE_ANON_KEY=
  SUPABASE_SERVICE_ROLE_KEY=       # server-only, never exposed to browser

  # Build isolation
  NAMESPACE_ID=                    # unique per build/run

  # External catalog (TMDB)
  TMDB_API_KEY=                    # server-only

  # AI provider
  AI_API_KEY=                      # server-only; overridden by user setting if present
  AI_MODEL=                        # default model identifier

  # Dev identity
  DEV_USER_ID=                     # dev/test only; ignored in production
  ```
- `.gitignore` excludes `.env*` (except `.env.example`), `node_modules`, `.next`.
- Add npm scripts:
  - `dev` — start Next.js dev server.
  - `build` / `start` — production build and serve.
  - `test` — run test suite.
  - `test:reset` — reset test data for the configured namespace.
  - `db:migrate` — apply Supabase migrations.

### 1.2 Supabase Client Setup

- **Browser client** (`lib/supabase/client.ts`): uses `NEXT_PUBLIC_SUPABASE_URL` + `NEXT_PUBLIC_SUPABASE_ANON_KEY`. Created once per page lifecycle via `createBrowserClient`.
- **Server client** (`lib/supabase/server.ts`): uses service role key for server-side operations (API routes, Server Components that need elevated access). Created per-request.
- Both clients are thin wrappers around the official `@supabase/supabase-js` SDK.

### 1.3 Namespace & Identity Middleware

- **Namespace**: Read `NAMESPACE_ID` from environment. Every database query that touches user-owned or test data includes a `namespace_id` predicate. The namespace column is added to all user-scoped tables.
- **User identity**:
  - In dev/test mode: accept `X-User-Id` header or fall back to `DEV_USER_ID` env var. Expose a lightweight dev-only user selector in the UI (gated by `NODE_ENV !== 'production'`).
  - In production mode: the dev injection path is disabled. A real auth provider (e.g., Supabase Auth with Google OAuth) can be wired in by replacing the identity resolution function — no schema changes needed because `user_id` is an opaque string column throughout.
- **Middleware** (`middleware.ts`): On every request, resolve `user_id` and `namespace_id`, attach them to request context (via headers or a server-side context utility). API routes and Server Components read from this context.

### 1.4 Row-Level Security (RLS)

- Enable RLS on all user-scoped tables.
- Policies:
  - `SELECT / INSERT / UPDATE / DELETE` restricted to rows matching the request's `namespace_id` and `user_id`.
  - The service role key bypasses RLS for migrations and the test-reset script.
- This ensures two namespaces or two users can never read or write each other's data, even if application code has a bug.

---

## 2. Database Schema & Migrations

All migrations live in `supabase/migrations/` and are applied with `supabase db push` or the migration script. The schema is designed so replacing Supabase later requires changing the client library calls but not the table structure.

### 2.1 Tables

#### `shows`

The central table. One row per (namespace, user, show).

| Column | Type | Notes |
|---|---|---|
| `id` | `text` | PK component — external catalog ID |
| `namespace_id` | `text` | PK component |
| `user_id` | `text` | PK component |
| `title` | `text NOT NULL` | |
| `show_type` | `text NOT NULL` | `'movie'` / `'tv'` / `'person'` / `'unknown'` |
| `external_ids` | `jsonb` | Optional external identifiers |
| `overview` | `text` | |
| `genres` | `text[]` | Genre display names |
| `tagline` | `text` | |
| `homepage` | `text` | |
| `original_language` | `text` | |
| `spoken_languages` | `text[]` | ISO 639-1 codes |
| `languages` | `text[]` | |
| `poster_url` | `text` | |
| `backdrop_url` | `text` | |
| `logo_url` | `text` | |
| `network_logos` | `text[]` | Reserved |
| `vote_average` | `double precision` | |
| `vote_count` | `integer` | |
| `popularity` | `double precision` | |
| `last_air_date` | `timestamptz` | |
| `first_air_date` | `timestamptz` | |
| `release_date` | `timestamptz` | |
| `runtime` | `integer` | Movies |
| `budget` | `bigint` | Movies |
| `revenue` | `bigint` | Movies |
| `series_status` | `text` | TV |
| `number_of_episodes` | `integer` | TV |
| `number_of_seasons` | `integer` | TV |
| `episode_run_time` | `integer[]` | TV |
| `my_tags` | `text[]` | User tags |
| `my_tags_update_date` | `timestamptz` | |
| `my_score` | `double precision` | User rating |
| `my_score_update_date` | `timestamptz` | |
| `my_status` | `text` | `'active'`/`'later'`/`'done'`/`'quit'`/`'wait'`/`'next'` |
| `my_status_update_date` | `timestamptz` | |
| `my_interest` | `text` | `'interested'`/`'excited'` |
| `my_interest_update_date` | `timestamptz` | |
| `ai_scoop` | `text` | |
| `ai_scoop_update_date` | `timestamptz` | |
| `details_update_date` | `timestamptz` | |
| `creation_date` | `timestamptz` | Set once on first insert |
| `is_test` | `boolean DEFAULT false` | |
| `provider_data` | `jsonb` | `{ countries: { [code]: { flatrate?, rent?, buy? } } }` |

**Primary key**: `(namespace_id, user_id, id)`.

**Indexes**:
- `(namespace_id, user_id, my_status)` — collection home queries.
- `(namespace_id, user_id, my_tags)` — GIN index for tag-based filtering.
- `(namespace_id, user_id, genres)` — GIN index for genre filtering.
- `(namespace_id, user_id, is_test)` — scoped test resets.

#### `cloud_settings`

| Column | Type | Notes |
|---|---|---|
| `id` | `text DEFAULT 'globalSettings'` | PK component |
| `namespace_id` | `text` | PK component |
| `user_id` | `text` | PK component |
| `user_name` | `text` | Random name on first create |
| `version` | `double precision` | Epoch seconds for conflict resolution |
| `catalog_api_key` | `text` | User-entered TMDB key |
| `ai_api_key` | `text` | User-entered AI key |
| `ai_model` | `text` | Model identifier |

**Primary key**: `(namespace_id, user_id, id)`.

#### `app_metadata`

| Column | Type | Notes |
|---|---|---|
| `id` | `text DEFAULT 'metadata'` | PK component |
| `namespace_id` | `text` | PK component |
| `data_model_version` | `integer DEFAULT 3` | Migration tracking |

**Primary key**: `(namespace_id, id)`.

#### `user_preferences`

Stores local/UI settings server-side (so they survive cache clears per infra rider §6.2).

| Column | Type | Notes |
|---|---|---|
| `namespace_id` | `text` | PK component |
| `user_id` | `text` | PK component |
| `auto_search` | `boolean DEFAULT false` | |
| `font_size` | `text DEFAULT 'M'` | XS/S/M/L/XL/XXL |
| `hide_status_removal_confirmation` | `boolean DEFAULT false` | |
| `status_removal_count` | `integer DEFAULT 0` | |
| `last_selected_filter` | `jsonb` | FilterConfiguration |

**Primary key**: `(namespace_id, user_id)`.

### 2.2 Migration Strategy

- Initial migration (`001_initial_schema.sql`) creates all tables, indexes, and RLS policies.
- Future migrations are numbered sequentially.
- `app_metadata.data_model_version` tracks schema version for any application-level migration logic (data transforms that go beyond DDL).
- Seed script (`supabase/seed.sql`) optionally inserts a default user and settings row for the configured namespace.

### 2.3 Test Reset Script

`npm run test:reset` executes:
```sql
DELETE FROM shows WHERE namespace_id = :namespace AND is_test = true;
```
And optionally a full namespace wipe:
```sql
DELETE FROM shows WHERE namespace_id = :namespace;
DELETE FROM cloud_settings WHERE namespace_id = :namespace;
DELETE FROM user_preferences WHERE namespace_id = :namespace;
```
The script reads `NAMESPACE_ID` from env. It uses the service role key (server-only) to bypass RLS.

---

## 3. External Catalog Integration (TMDB)

### 3.1 Server-Side Proxy Layer

All TMDB requests go through Next.js API routes (or server actions) to protect the API key.

**Module**: `lib/tmdb/client.ts`
- Wraps TMDB REST API v3.
- Methods:
  - `searchShows(query, mediaType?)` — multi-search or scoped search.
  - `getShowDetails(id, mediaType)` — full detail including credits, videos, recommendations, similar, providers, images.
  - `getPersonDetails(id)` — person info + combined credits.
  - `getProviders(id, mediaType)` — streaming availability.
  - `getSeason(showId, seasonNumber)` — episode list for TV.

### 3.2 API Routes

| Route | Purpose |
|---|---|
| `GET /api/search?q=&type=` | Proxy search |
| `GET /api/shows/[mediaType]/[id]` | Full detail (catalog + user merge) |
| `GET /api/shows/[mediaType]/[id]/providers` | Streaming availability |
| `GET /api/shows/[mediaType]/[id]/season/[num]` | Season episodes |
| `GET /api/persons/[id]` | Person detail + credits |

### 3.3 Catalog → Show Mapping

**Module**: `lib/tmdb/mapper.ts`

Implements the mapping rules from `storage-schema.md`:

1. Decode TMDB JSON into a fresh `Show` object.
2. Map `id` → `show.id` (as string). Store TMDB ID in `external_ids.tmdb`.
3. Title: prefer `title` (movie) or `name` (TV). Fail if neither exists.
4. Show type: infer from TMDB media type field.
5. Genres: map TMDB genre ID objects to display name strings.
6. Dates: parse from TMDB date strings into ISO-8601 timestamps.
7. Images: construct full URLs from TMDB base URL + file paths. For logos, pick the highest-rated English logo.
8. Providers: restructure TMDB provider response into `ProviderData` shape (IDs only, keyed by country).
9. Transient fields (cast, crew, seasons, videos, recommendations, similar, image galleries) are returned in the API response but not stored in `shows`.

### 3.4 Merge Logic

**Module**: `lib/shows/merge.ts`

When catalog data is fetched for a show that already exists in the user's collection:

- **Non-user fields**: `selectFirstNonEmpty(newValue, existingValue)` — never overwrite a populated field with empty/null.
- **User fields** (`my_*`): compare timestamps; keep the side with the newer `*_update_date`. If only one side has a date, keep that side.
- Set `details_update_date = now()` after merge.
- Never overwrite `creation_date`.

---

## 4. Collection & Data Management

### 4.1 Collection API Routes

| Route | Method | Purpose |
|---|---|---|
| `/api/collection` | `GET` | Fetch user's collection (supports filters, media type toggle) |
| `/api/collection/[id]` | `GET` | Fetch single show from collection |
| `/api/collection/[id]` | `PUT` | Upsert show (save/update) |
| `/api/collection/[id]` | `DELETE` | Remove show from collection |
| `/api/collection/[id]/status` | `PATCH` | Update status + interest |
| `/api/collection/[id]/rating` | `PATCH` | Update rating |
| `/api/collection/[id]/tags` | `PATCH` | Update tags |
| `/api/collection/tags` | `GET` | List all user tags (derived) |
| `/api/collection/filters` | `GET` | Available filters (tags, genres, decades, scores) |

### 4.2 Business Rule Enforcement

All business rules from PRD §5 are enforced server-side in the API layer:

**Save triggers** (§5.2):
- Setting status → save with that status.
- Choosing Interested/Excited → save with `my_status = 'later'`, `my_interest = 'interested'|'excited'`.
- Rating unsaved show → save with `my_status = 'done'` (§5.3 exception).
- Adding tag to unsaved show → save with `my_status = 'later'`, `my_interest = 'interested'`.

**Default values** (§5.3):
- No explicit status on save → `my_status = 'later'`, `my_interest = 'interested'`.
- First save via rating → `my_status = 'done'`.

**Removal** (§5.4):
- `DELETE /api/collection/[id]` removes the row entirely, clearing all user data.
- The confirmation UX (including progressive suppression) is client-side.

**Re-adding** (§5.5):
- If the show already exists, the `PUT` upsert preserves existing user data and merges catalog fields using the merge logic.

**Timestamps** (§5.6):
- Every `PATCH` to a user field sets the corresponding `*_update_date = now()`.

### 4.3 Collection Home Queries

The collection home groups shows by status section. A single query fetches all shows for the user+namespace, and the grouping is done application-side:

1. **Active** — `my_status = 'active'`
2. **Excited** — `my_status = 'later' AND my_interest = 'excited'`
3. **Interested** — `my_status = 'later' AND my_interest = 'interested'`
4. **Other** — `my_status IN ('wait', 'quit', 'done')` plus any `later` without interest

Filters narrow the result set:
- **Tag filter**: `@> ARRAY['tagName']` on `my_tags`.
- **Genre filter**: `@> ARRAY['genreName']` on `genres`.
- **Decade filter**: date range check on `release_date` / `first_air_date`.
- **Community score filter**: range check on `vote_average`.
- **Media type toggle**: `show_type = 'movie'|'tv'` or all.

### 4.4 Export / Backup

`GET /api/collection/export` produces a ZIP file containing:
- `shows.json` — all shows in collection with all fields. Dates encoded ISO-8601.
- `settings.json` — cloud settings and preferences.

The endpoint streams the ZIP to the client for download.

---

## 5. AI Integration

### 5.1 AI Client Abstraction

**Module**: `lib/ai/client.ts`

A provider-agnostic wrapper:
- Accepts a model identifier and API key (from env or user settings).
- Exposes `streamChat(messages, options)` and `generateCompletion(messages, options)`.
- Returns a streaming response for surfaces that need progressive display (Scoop, Ask).
- Designed so swapping providers (OpenAI, Anthropic, etc.) requires only a new adapter, not changes to feature code.

### 5.2 AI Prompt Modules

Each AI surface has a dedicated prompt builder that constructs the system prompt and user messages according to the contracts in `ai_prompting_context.md` and the voice spec in `ai_voice_personality.md`.

**Module**: `lib/ai/prompts/`

#### `ask.ts` — Ask (Chat) Prompts
- **System prompt**: Establishes the persona (fun, chatty TV/movie nerd friend), spoiler-safe default, opinionated honesty, library awareness.
- **Context injection**: Includes user's library summary (statuses, ratings, tags) to make responses taste-aware.
- **Structured output**: Uses the `commentary` + `showList` dual format (`Title::externalId::mediaType;;...`).
- **Show-seeded variant**: When entering Ask from a show detail ("Ask about this show"), the system prompt includes that show's metadata as seed context.

#### `scoop.ts` — AI Scoop Prompts
- **System prompt**: Personality-driven taste review. Must produce sections: personal take, honest stack-up, The Scoop (emotional centerpiece), fit/warnings, verdict.
- **Length target**: 150–350 words.
- **Streaming**: Response is streamed progressively.

#### `concepts.ts` — Concept Generation Prompts
- **Single-show**: Extract concepts from one show's metadata and overview.
- **Multi-show (Alchemy)**: Extract concepts shared across all input shows.
- **Output**: Bullet list only, 1–3 words each, evocative, no plot, no generics.
- **Focus axes**: Structure, tone/vibe, emotional palette, relationship dynamics, craft, genre-flavor.

#### `recommendations.ts` — Concept-Based Recommendations
- **Input**: Selected concepts + optional library context.
- **Output**: List of shows with per-show reasons explicitly referencing concepts.
- **Counts**: 5 for Explore Similar, 6 for Alchemy.
- **Constraint**: Must return external IDs for catalog resolution.

#### `summarize.ts` — Conversation Summarization
- Summarizes older chat turns into 1–2 sentences preserving the persona's tone.
- Applied after ~10 messages in a session.

### 5.3 AI API Routes

| Route | Method | Purpose |
|---|---|---|
| `/api/ai/ask` | `POST` | Ask chat turn (streaming) |
| `/api/ai/scoop` | `POST` | Generate AI Scoop (streaming) |
| `/api/ai/concepts` | `POST` | Generate concepts for 1+ shows |
| `/api/ai/recommendations` | `POST` | Concept-based recommendations |

All AI routes:
- Read the AI API key from user settings first, falling back to the server env var.
- Read the model identifier from user settings first, falling back to env.
- Include the user's library context (fetched server-side) in the prompt when the surface requires taste-awareness.

### 5.4 Show Resolution from AI Output

When AI returns recommended shows:
1. Parse the structured output to extract title, external ID, media type.
2. If an external ID is provided, look up the show in TMDB by that ID. Accept if title matches case-insensitively.
3. If no external ID or lookup fails, search TMDB by title and accept the first matching result.
4. If resolution succeeds, the recommendation becomes a fully interactive show tile with optional transient "reason" text.
5. If resolution fails, display the title as non-interactive text with a "Search for this" fallback link.

### 5.5 AI Scoop Caching

- When scoop is generated for a show **in the collection**: persist `ai_scoop` and `ai_scoop_update_date` to the `shows` row.
- When scoop is generated for a show **not in the collection**: return it to the client but do not persist. If the user then saves the show, the client includes the scoop in the save request.
- Freshness: if `ai_scoop_update_date` is older than 4 hours and the user requests the scoop, regenerate.

---

## 6. UI Architecture & Pages

### 6.1 Layout & Navigation

**Root layout** (`app/layout.tsx`):
- Sidebar (filters/navigation panel) + main content area.
- Sidebar contains: "All Shows" link, dynamically generated tag filter links, data filter links (genre, decade, community score), a "No Tags" link if applicable.
- Top bar or persistent nav: Find/Discover button, Settings button.
- Media type toggle (All / Movies / TV) — global, applies on top of any filter.

**Route structure** (App Router):
```
app/
  layout.tsx              — shell: sidebar + main area + nav
  page.tsx                — Collection Home
  find/
    layout.tsx            — Find/Discover hub with mode switcher
    search/page.tsx       — Search mode
    ask/page.tsx          — Ask mode
    alchemy/page.tsx      — Alchemy mode
  shows/
    [mediaType]/
      [id]/page.tsx       — Show Detail
  persons/
    [id]/page.tsx         — Person Detail
  settings/page.tsx       — Settings & Your Data
```

### 6.2 Shared Components

| Component | Purpose |
|---|---|
| `ShowTile` | Poster + title + in-collection badge + rating badge. Used everywhere shows appear in grids/strands. |
| `ShowGrid` | Responsive poster grid for search results and recommendations. |
| `ShowStrand` | Horizontal scrollable row of `ShowTile`s (recommendations, mentioned shows, credits). |
| `StatusChips` | Toolbar-style status/interest chip bar (Active, Interested, Excited, Wait, Done, Quit). Handles save triggers and removal confirmation. |
| `RatingBar` | Interactive rating slider/control. Handles auto-save on rating. |
| `TagPicker` | Tag display + add/remove picker. Handles auto-save on first tag. |
| `ConceptChips` | Selectable concept chips (max 8 selection). |
| `RemovalConfirmation` | Confirmation dialog for show removal with "don't ask again" option. |
| `MediaTypeToggle` | All / Movies / TV segmented control. |
| `FilterSidebar` | Sidebar filter list with active state. |
| `EmptyState` | Contextual empty states with CTAs. |

### 6.3 Collection Home Page

- Fetches user collection via `GET /api/collection` with current filter and media type.
- Groups results into status sections: Active (larger tiles), Excited, Interested, Other (collapsed by default).
- Each section is a grid of `ShowTile` components.
- Sidebar filter selection updates the query. Active filter is persisted to `user_preferences.last_selected_filter`.
- Empty states: no collection → prompt to Search/Ask. Filter yields nothing → "No results found."

### 6.4 Find/Discover Hub

A shared layout with a mode switcher (tabs or segmented control): **Search** | **Ask** | **Alchemy**.

#### 6.4.1 Search Page
- Text input with live or submit-based search.
- Results displayed as `ShowGrid`.
- In-collection items are marked with a badge on their tile.
- Clicking a tile navigates to Show Detail.
- Auto-opens on launch if `auto_search` setting is true.

#### 6.4.2 Ask Page
- Chat UI: scrollable message list with user/assistant turns.
- Input field at bottom.
- Welcome state: 6 random starter prompts (from a pool of ~80 curated prompts) with a refresh button.
- On send: `POST /api/ai/ask` with message history. Response streams in.
- Mentioned shows appear in a `ShowStrand` below the latest assistant message. Parsed from the structured `showList` format.
- Tapping a mentioned show navigates to Show Detail (or Search if resolution fails).
- Conversation state: held in client-side React state. After ~10 messages, older turns are summarized via `POST /api/ai/ask` with a summarization instruction.
- **Ask About a Show** variant: When launched from Show Detail, the first system message is seeded with that show's context.

#### 6.4.3 Alchemy Page
- Multi-step flow with clear visual progression:
  1. **Select Shows** (2+ required): search bar + selected show chips. Shows can come from library or global catalog search.
  2. **Conceptualize Shows** button → calls `POST /api/ai/concepts` with selected shows → displays `ConceptChips`.
  3. **Select Concepts** (1–8): user taps to select/deselect.
  4. **ALCHEMIZE!** button → calls `POST /api/ai/recommendations` with selected concepts → displays 6 recommendation tiles with reasons.
  5. **More Alchemy!** button: chain another round using result shows as new inputs.
- Backtracking: changing the input shows clears concepts and results.
- Session-only: all Alchemy state is client-side. Leaving the page clears it.

### 6.5 Show Detail Page

Follows the narrative hierarchy from `detail_page_experience.md`:

1. **Header media carousel**: Backdrops, posters, logos. Trailers inline when available. Graceful fallback to poster-only.
2. **Core facts row**: Year, runtime (movies) or seasons/episodes (TV), community score bar.
3. **My Rating bar**: `RatingBar` component. Rating unsaved show triggers auto-save as Done.
4. **Status/Interest toolbar**: `StatusChips` in a sticky toolbar (not in scroll body). Reselecting active status triggers `RemovalConfirmation`.
5. **My Tags**: `TagPicker`. Adding tag to unsaved show triggers auto-save as Later + Interested.
6. **Overview**: Show overview text.
7. **AI Scoop toggle**: "Give me the scoop!" / "Show the scoop" / "The Scoop" header. On tap: calls `POST /api/ai/scoop`, streams response progressively. Shows "Generating..." during load.
8. **Ask about this show** CTA: navigates to Ask page with show context seeded.
9. **Genres + Languages**: Display chips/tags.
10. **Traditional recommendations strand**: `ShowStrand` from TMDB similar/recommended.
11. **Explore Similar**:
    - "Get Concepts" button → `POST /api/ai/concepts` → `ConceptChips`.
    - Select concepts → "Explore Shows" button → `POST /api/ai/recommendations` → 5 recommendation tiles with reasons.
12. **Streaming availability**: Provider logos/links grouped by type (flatrate/rent/buy).
13. **Cast & Crew**: Horizontal `ShowStrand`-style rows. Tapping opens Person Detail.
14. **Seasons** (TV only): Expandable season list with episode details.
15. **Budget vs Revenue** (movies, when available): Simple display or bar visualization.

**State handling**:
- Unsaved show: Scoop generated but not persisted until/unless saved.
- No trailers: header falls back to poster/backdrop.
- No concepts yet: only "Get Concepts" CTA visible in Explore Similar section.

### 6.6 Person Detail Page

- Image gallery, name, bio.
- Analytics charts:
  - Average project ratings (bar or line chart).
  - Top genres (horizontal bar chart).
  - Projects by year (timeline bar chart).
- Filmography: credits grouped by year, each credit is a `ShowTile` that links to Show Detail.

### 6.7 Settings Page

Sections:
- **App Settings**: Font size selector (XS–XXL), "Search on Launch" toggle.
- **User**: Username input (synced via `cloud_settings`).
- **AI**: API key input, model selector. Key stored in `cloud_settings.ai_api_key` (never committed to repo). Warning if using server-provided key.
- **Integrations**: Catalog provider API key input (stored in `cloud_settings.catalog_api_key`).
- **Your Data**:
  - "Export My Data" button → `GET /api/collection/export` → downloads ZIP.
  - Import/Restore: placeholder/disabled with "Coming soon" label (per open questions).

---

## 7. Implementation Phases

### Phase 1: Foundation (Infra + Schema)
**Goal**: Deployable skeleton with namespace/identity isolation, database, and dev tooling.

Tasks:
1. Initialize Next.js project with TypeScript, Tailwind, ESLint.
2. Create `.env.example`, `.gitignore`, npm scripts.
3. Set up Supabase client wrappers (browser + server).
4. Implement namespace + identity middleware.
5. Write initial migration (`001_initial_schema.sql`) for all tables + RLS policies + indexes.
6. Implement test reset script (`npm run test:reset`).
7. Create root layout shell with sidebar placeholder and nav.
8. Verify: app starts, connects to Supabase, middleware resolves user_id + namespace_id.

### Phase 2: Catalog Integration (TMDB)
**Goal**: Search works, show details load from TMDB.

Tasks:
1. Implement TMDB client (`lib/tmdb/client.ts`) with search, detail, person, provider, season methods.
2. Implement catalog-to-Show mapper (`lib/tmdb/mapper.ts`).
3. Build API routes: `/api/search`, `/api/shows/[mediaType]/[id]`, `/api/persons/[id]`, `/api/shows/[mediaType]/[id]/providers`, `/api/shows/[mediaType]/[id]/season/[num]`.
4. Build Search page (`find/search/page.tsx`) with `ShowGrid`.
5. Build Show Detail page with catalog data sections (header, facts, overview, genres, recommendations, providers, cast/crew, seasons, budget/revenue).
6. Build Person Detail page with bio, filmography, analytics charts.
7. Verify: search returns results, detail pages display full catalog data, person pages show credits.

### Phase 3: Collection Management
**Goal**: Users can save, organize, and maintain their show collection.

Tasks:
1. Implement collection API routes (`/api/collection/*`).
2. Implement merge logic (`lib/shows/merge.ts`).
3. Implement all business rules: save triggers, defaults, removal, re-adding, timestamps.
4. Build `StatusChips`, `RatingBar`, `TagPicker`, `RemovalConfirmation` components.
5. Wire status/rating/tag controls into Show Detail page.
6. Build Collection Home page with status grouping, filters, media type toggle.
7. Build `FilterSidebar` with tag filters, genre filters, decade filters, score filters.
8. Add in-collection badge and rating badge to `ShowTile`.
9. Build Settings page (app settings, user, integrations).
10. Implement export endpoint (`GET /api/collection/export`).
11. Verify: full save/update/remove lifecycle, collection home filters, export works.

### Phase 4: AI — Scoop + Ask
**Goal**: AI personality surfaces work (Scoop on detail page, Ask chat).

Tasks:
1. Implement AI client abstraction (`lib/ai/client.ts`) with streaming support.
2. Build Scoop prompt module and API route. Implement streaming response.
3. Wire Scoop toggle into Show Detail page with progressive streaming display and caching logic (4-hour freshness, persistence only for in-collection shows).
4. Build Ask prompt module and API route with structured output (commentary + showList).
5. Implement show resolution from AI output (`lib/ai/resolve.ts`).
6. Build Ask page: chat UI, starter prompts, streaming responses, mentioned shows strand.
7. Implement "Ask about this show" flow from Show Detail.
8. Implement conversation summarization for long sessions.
9. Add AI settings to Settings page (API key, model selector).
10. Verify: Scoop streams on detail page, Ask produces taste-aware chat with interactive show mentions.

### Phase 5: AI — Concepts + Alchemy + Explore Similar
**Goal**: Concept-based discovery fully operational.

Tasks:
1. Build concept generation prompt module (single-show + multi-show variants).
2. Build concept-based recommendation prompt module.
3. Build API routes for concepts and recommendations.
4. Build `ConceptChips` component.
5. Wire Explore Similar into Show Detail: Get Concepts → select → Explore Shows → 5 recommendation tiles.
6. Build Alchemy page: multi-step flow (show selection → conceptualize → select concepts → alchemize → chain).
7. Implement Alchemy chaining (results become new inputs for next round).
8. Verify: concepts are evocative and specific, recommendations cite concepts, Alchemy chains work.

### Phase 6: Polish & Data Sync
**Goal**: Settings sync, edge cases, and UI polish.

Tasks:
1. Implement cloud settings sync (conflict resolution by `version` timestamp).
2. Handle all edge cases:
   - Font size applied across UI.
   - "Search on Launch" behavior.
   - Status removal confirmation progressive suppression.
   - Filter persistence across sessions.
3. Add empty states throughout (no collection, no results, no concepts).
4. Ensure all show tiles everywhere display user overlay (status badge, rating badge) per PRD §4.1 display rule.
5. Polish responsive layout, loading states, error states.
6. Review all AI surfaces against the discovery quality bar (voice adherence, taste alignment, real-show integrity, specificity, surprise).

### Phase 7: Testing & Hardening
**Goal**: Test coverage, security review, final compliance check.

Tasks:
1. Write integration tests for all business rules (save triggers, defaults, removal, merge).
2. Write API route tests for collection CRUD, search, AI endpoints.
3. Write namespace isolation tests (two namespaces cannot see each other's data).
4. Write user isolation tests (two users in same namespace cannot see each other's data).
5. Test destructive reset is scoped to namespace.
6. Test export produces valid ZIP with correct JSON structure.
7. Security review: verify service role key is never exposed to browser, AI/catalog keys are server-only, RLS policies are correct, no secrets in repo.
8. Verify infra rider compliance:
   - `.env.example` is complete and commented.
   - App runs by filling env vars only (no code edits).
   - `npm run dev`, `npm test`, `npm run test:reset` all work.
   - Schema is deterministically reproducible from migrations.
   - OAuth can replace dev identity without schema changes.

---

## 8. Key Architectural Decisions

### 8.1 Server-Side Data as Source of Truth
Per infra rider §6: all user data lives in Supabase. Client-side state is ephemeral. Clearing browser storage loses nothing. This means:
- Collection home, filters, settings — all fetched from server on page load.
- AI session state (Ask chat, Alchemy) is the only client-only state, and it is intentionally ephemeral.

### 8.2 API Routes as the Integration Boundary
All external calls (TMDB, AI provider) go through Next.js API routes. This:
- Protects API keys from browser exposure.
- Centralizes business rule enforcement.
- Makes it straightforward to swap providers.

### 8.3 Namespace Column on Every User-Scoped Table
Rather than schema-per-namespace or database-per-namespace, a simple `namespace_id` column on each table with RLS provides isolation without operational complexity. This is the simplest approach that satisfies the infra rider's isolation requirements.

### 8.4 Opaque `user_id` String
`user_id` is a plain text column with no provider-specific structure. In dev mode it comes from env/header; in production it will come from Supabase Auth (or any OAuth provider). The schema doesn't care — it's just a string.

### 8.5 AI Provider Abstraction
The AI client is a thin adapter layer. The prompt modules produce plain messages. Swapping from one AI provider to another means writing a new adapter (and possibly adjusting model-specific tuning) without changing any feature code.

### 8.6 Streaming for AI Surfaces
Scoop and Ask use server-sent events (or Next.js streaming responses) so users see progressive output rather than waiting for complete generation. This is critical for perceived performance on the Scoop toggle and chat interactions.

---

## 9. Risk Mitigation

| Risk | Mitigation |
|---|---|
| AI hallucinates show titles | Show resolution pipeline: validate against TMDB by external ID first, then title search. Unresolvable titles shown as non-interactive with Search fallback. |
| TMDB rate limits | Server-side caching of catalog data (short TTL). Batch detail fetches where possible. |
| AI structured output parsing fails | Retry once with stricter formatting instructions. Fall back to unstructured commentary + Search handoff. |
| Scoop/Ask responses drift off-brand | Prompt modules encode the voice pillars and guardrails. Discovery quality bar provides a regression rubric. |
| Namespace collision | RLS policies enforce isolation at the database level, independent of application code correctness. |
| Schema migration breaks existing data | `app_metadata.data_model_version` enables application-level migration logic. Migrations are additive where possible. PRD §5.11 requires data continuity across versions. |

---

## 10. Deliverables Summary

| Artifact | Location |
|---|---|
| Next.js application | `src/` or `app/` (App Router) |
| Supabase migrations | `supabase/migrations/` |
| Seed data (optional) | `supabase/seed.sql` |
| Environment template | `.env.example` |
| TMDB integration | `lib/tmdb/` |
| AI integration | `lib/ai/` |
| Collection logic | `lib/shows/` |
| Shared components | `components/` |
| API routes | `app/api/` |
| Tests | `__tests__/` or colocated `*.test.ts` |
| This plan | `results/PLAN.md` |
