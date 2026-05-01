# Implementation Plan

## 1. Project Scaffolding & Infrastructure

### 1.1 Repository Setup
- Initialize a Next.js (latest stable) project with TypeScript and App Router.
- Configure ESLint, Prettier, and a `.gitignore` that excludes `.env*` (except `.env.example`).
- Create `.env.example` with all required variables:
  ```
  # Supabase
  NEXT_PUBLIC_SUPABASE_URL=        # Supabase project URL
  NEXT_PUBLIC_SUPABASE_ANON_KEY=   # Supabase anon/public key (safe for browser)
  SUPABASE_SERVICE_ROLE_KEY=       # Server-only elevated key (never exposed to client)

  # Namespace / Build Isolation
  NEXT_PUBLIC_NAMESPACE_ID=        # Stable build/run namespace identifier

  # External Catalog (TMDB)
  TMDB_API_KEY=                    # TMDB v3 API key (server-only)

  # AI Provider
  AI_API_KEY=                      # AI provider API key (server-only by default)
  AI_MODEL=                        # AI model identifier (e.g. claude-sonnet-4-6)

  # Dev Identity (benchmark mode only)
  DEV_USER_ID=                     # Fixed user_id for dev/benchmark mode
  ```
- Add npm scripts:
  - `npm run dev` — start Next.js dev server.
  - `npm test` — run test suite.
  - `npm run test:reset` — reset test data for the current namespace.
  - `npm run db:migrate` — apply database migrations.
  - `npm run db:seed` — seed data for development.

### 1.2 Core Dependencies
- `@supabase/supabase-js` — Supabase client.
- `@supabase/ssr` — Supabase helpers for Next.js server components / route handlers.
- AI SDK (e.g. `@anthropic-ai/sdk` or `ai` from Vercel AI SDK) for streaming AI responses.
- `tailwindcss` — utility-first styling.
- `zustand` or React Context — lightweight client state management for transient UI state (Alchemy session, Ask chat turns, filter selections).
- `zod` — runtime validation for API responses and AI structured outputs.

---

## 2. Database Schema & Migrations

### 2.1 Supabase Schema Design

All tables are partitioned by `namespace_id` and (where applicable) `user_id`. Row-Level Security (RLS) policies enforce isolation.

#### Table: `shows`
Primary persistence for catalog items + user overlay. One row per (namespace, user, show).

| Column | Type | Notes |
|---|---|---|
| `id` | `uuid` | PK, default `gen_random_uuid()` |
| `namespace_id` | `text NOT NULL` | Build isolation partition |
| `user_id` | `text NOT NULL` | User ownership |
| `external_id` | `text NOT NULL` | External catalog ID (e.g. TMDB ID) |
| `show_type` | `text NOT NULL` | `'movie' \| 'tv'` |
| `title` | `text NOT NULL` | |
| `overview` | `text` | |
| `tagline` | `text` | |
| `genres` | `text[]` | Genre display names |
| `homepage` | `text` | |
| `original_language` | `text` | |
| `spoken_languages` | `text[]` | ISO 639-1 codes |
| `languages` | `text[]` | |
| `poster_url` | `text` | Full URL |
| `backdrop_url` | `text` | Full URL |
| `logo_url` | `text` | Full URL |
| `vote_average` | `double precision` | |
| `vote_count` | `integer` | |
| `popularity` | `double precision` | |
| `release_date` | `date` | Movies |
| `first_air_date` | `date` | TV |
| `last_air_date` | `date` | TV |
| `runtime` | `integer` | Movies (minutes) |
| `budget` | `bigint` | Movies |
| `revenue` | `bigint` | Movies |
| `series_status` | `text` | TV |
| `number_of_episodes` | `integer` | TV |
| `number_of_seasons` | `integer` | TV |
| `episode_run_time` | `integer[]` | TV |
| `provider_data` | `jsonb` | `{ countries: { [cc]: { flatrate, rent, buy } } }` |
| `my_status` | `text` | `'active' \| 'later' \| 'done' \| 'quit' \| 'wait' \| 'next'` |
| `my_status_update_date` | `timestamptz` | |
| `my_interest` | `text` | `'interested' \| 'excited'` |
| `my_interest_update_date` | `timestamptz` | |
| `my_tags` | `text[]` | |
| `my_tags_update_date` | `timestamptz` | |
| `my_score` | `double precision` | |
| `my_score_update_date` | `timestamptz` | |
| `ai_scoop` | `text` | |
| `ai_scoop_update_date` | `timestamptz` | |
| `details_update_date` | `timestamptz` | |
| `creation_date` | `timestamptz` | Set on first insert |
| `is_test` | `boolean DEFAULT false` | For test data scoping |

**Unique constraint:** `(namespace_id, user_id, external_id)` — one user-show record per namespace.

**Indexes:**
- `(namespace_id, user_id, my_status)` — Collection Home queries by status.
- `(namespace_id, user_id)` — All-collection queries.
- `(namespace_id, is_test)` — Test data cleanup.

#### Table: `cloud_settings`
Per-user synced settings.

| Column | Type | Notes |
|---|---|---|
| `id` | `text DEFAULT 'globalSettings'` | PK |
| `namespace_id` | `text NOT NULL` | |
| `user_id` | `text NOT NULL` | |
| `user_name` | `text NOT NULL` | Random name on first launch |
| `version` | `double precision` | Epoch seconds for conflict resolution |
| `catalog_api_key` | `text` | Encrypted at rest |
| `ai_api_key` | `text` | Encrypted at rest |
| `ai_model` | `text NOT NULL` | |

**Unique constraint:** `(namespace_id, user_id, id)`.

#### Table: `app_metadata`
Tracks data model version for migrations.

| Column | Type | Notes |
|---|---|---|
| `id` | `serial` | PK |
| `namespace_id` | `text NOT NULL` | |
| `data_model_version` | `integer DEFAULT 3` | |

### 2.2 Row-Level Security (RLS)

Enable RLS on all tables. Policies check:
- `namespace_id` matches the request's namespace (from JWT claim or header).
- `user_id` matches the authenticated/injected user identity.

This ensures complete isolation between builds and between users within a build.

### 2.3 Migration Strategy
- Store migrations in `supabase/migrations/` as numbered SQL files.
- Each migration is idempotent where possible.
- The `npm run db:migrate` script applies migrations via Supabase CLI or direct SQL execution.
- Seed script (`npm run db:seed`) inserts sample shows for development.

### 2.4 Test Data Reset
- `npm run test:reset` deletes all rows where `namespace_id` matches the current build AND `is_test = true`.
- Destructive operations are always scoped to a single namespace; never global teardown.

---

## 3. Identity & Authentication

### 3.1 Benchmark Mode (Dev Identity Injection)
- In development/test mode, user identity is injected via:
  - `DEV_USER_ID` environment variable, OR
  - `X-User-Id` request header accepted by API routes (gated behind `NODE_ENV !== 'production'`), OR
  - A dev-only "user selector" dropdown in the UI.
- A middleware function resolves the current `user_id` from the above sources.
- `namespace_id` is always read from `NEXT_PUBLIC_NAMESPACE_ID`.

### 3.2 Production Migration Path
- `user_id` is stored as an opaque string (`text`), not tied to any auth provider format.
- Swapping the dev identity mechanism for real OAuth (e.g. Supabase Auth with Google) requires only:
  - Replacing the identity resolution middleware.
  - Mapping the OAuth `sub` claim to `user_id`.
  - No schema changes needed.

---

## 4. External Catalog Integration (TMDB)

### 4.1 Server-Side API Layer
All TMDB calls go through Next.js Route Handlers (server-side only) to protect the API key.

**Route Handlers:**

| Route | Purpose |
|---|---|
| `GET /api/search?query=&type=` | Search movies/TV by title |
| `GET /api/shows/[id]?type=` | Full show details (metadata + credits + videos + recommendations + similar + providers) |
| `GET /api/shows/[id]/credits` | Cast & crew |
| `GET /api/shows/[id]/seasons/[num]` | Season episodes (TV) |
| `GET /api/person/[id]` | Person detail + combined credits |
| `GET /api/trending` | Trending for discovery fallbacks |

### 4.2 TMDB Response Mapping
- Map TMDB responses to the `Show` schema using the merge rules from the storage-schema spec.
- Genre IDs are resolved to display names via TMDB's genre list endpoint (cached on startup).
- Image paths are prefixed with TMDB's base image URL to form full URLs.
- Logo selection: pick the highest-rated English logo, or first available.
- Spoken languages mapped from TMDB's `spoken_languages` array.
- Provider data mapped from TMDB's watch/providers endpoint, stored as `{ countries: { [cc]: { flatrate, rent, buy } } }`.

### 4.3 Catalog-to-Collection Merge
When a user views a show already in their collection:
1. Fetch fresh catalog data from TMDB.
2. Merge into stored show using `selectFirstNonEmpty(new, old)` for non-my fields.
3. My fields resolve by timestamp (newer wins).
4. Set `details_update_date` to now.
5. `creation_date` is immutable after first insert.

---

## 5. AI Integration

### 5.1 Architecture
- AI calls go through server-side Route Handlers to protect API keys.
- Use streaming responses where the UI supports progressive display (Scoop, Ask).
- All AI surfaces share one consistent persona: fun, chatty, opinionated TV/movie nerd friend.

### 5.2 AI Route Handlers

| Route | Purpose | Streaming |
|---|---|---|
| `POST /api/ai/ask` | Ask chat conversation | Yes |
| `POST /api/ai/scoop` | Generate AI Scoop for a show | Yes |
| `POST /api/ai/concepts` | Generate concepts (single or multi-show) | No |
| `POST /api/ai/recommend` | Concept-based recommendations (Explore Similar / Alchemy) | No |
| `POST /api/ai/summarize` | Summarize older chat turns | No |

### 5.3 Context Construction

**Shared context** (included in all AI requests where applicable):
- System prompt establishing the persona (warm, opinionated, spoiler-safe, TV/movies only).
- User's library summary: list of saved shows with status, interest, tags, and rating.

**Surface-specific context:**

| Surface | Additional Context |
|---|---|
| **Ask** | Recent conversation turns (last ~10); older turns replaced by persona-consistent summary. |
| **Ask About Show** | Current show metadata seeded as conversation context. |
| **Scoop** | Full show metadata (title, year, genres, overview, community score, cast highlights). |
| **Concepts (single)** | Show metadata for the target show. |
| **Concepts (multi)** | Metadata for all input shows. |
| **Recommendations** | Selected concepts + input show(s) metadata. |

### 5.4 Structured Output Contracts

**Ask with Mentions:**
- AI returns JSON: `{ commentary: string, showList: "Title::externalId::mediaType;;..." }`.
- Parser splits `showList` on `;;`, then each entry on `::`.
- On parse failure: retry once with stricter instructions, then fall back to plain commentary + search handoff.

**Concepts:**
- AI returns a bullet list of 1-3 word concepts.
- Parse bullets into a string array.
- Validate: reject generic concepts ("good characters", "great story").

**Recommendations:**
- AI returns JSON array: `[{ title, externalId, mediaType, reason }]`.
- Each recommendation is resolved against TMDB by ID; title is verified case-insensitively.
- Unresolvable titles shown as non-interactive or handed off to Search.

**Scoop:**
- Streamed as structured markdown with sections: personal take, honest stack-up, The Scoop (emotional centerpiece), fit/warnings, verdict.
- Target: 150-350 words.

### 5.5 Scoop Caching
- Stored in `ai_scoop` column with `ai_scoop_update_date`.
- Considered stale after 4 hours.
- Regenerated on demand when stale.
- Only persisted if the show is in the user's collection; otherwise ephemeral (held in component state).

### 5.6 Conversation Summarization
- After ~10 messages in an Ask session, older turns are replaced with a 1-2 sentence summary.
- Summary preserves the persona tone (not sterile system voice).
- Summaries are generated via the `/api/ai/summarize` endpoint.

---

## 6. Application Structure & Routing

### 6.1 Next.js App Router Layout

```
app/
  layout.tsx              # Root layout: providers, sidebar, nav shell
  page.tsx                # Collection Home
  find/
    layout.tsx            # Find/Discover layout with mode switcher
    search/page.tsx       # Search mode
    ask/page.tsx          # Ask (AI chat) mode
    alchemy/page.tsx      # Alchemy mode
  shows/
    [id]/page.tsx         # Show Detail (query param: type=movie|tv)
  person/
    [id]/page.tsx         # Person Detail
  settings/page.tsx       # Settings & Your Data
  api/
    search/route.ts
    shows/[id]/route.ts
    shows/[id]/credits/route.ts
    shows/[id]/seasons/[num]/route.ts
    person/[id]/route.ts
    trending/route.ts
    ai/ask/route.ts
    ai/scoop/route.ts
    ai/concepts/route.ts
    ai/recommend/route.ts
    ai/summarize/route.ts
    collection/route.ts         # CRUD for user's show collection
    collection/[id]/route.ts    # Single show CRUD
    collection/export/route.ts  # Export zip
    settings/route.ts           # Cloud settings CRUD
    test-reset/route.ts         # Namespace-scoped test data reset
```

### 6.2 Layout & Navigation
- **Sidebar** (left panel): Filter navigation.
  - "All Shows" (default).
  - Tag filters (one per tag; plus "No tags" if tagless shows exist).
  - Data filters: genre, decade, community score ranges.
- **Top bar**: Media-type toggle (All / Movies / TV), Find/Discover entry point, Settings entry point.
- **Main content area**: Renders the current page.

---

## 7. Feature Implementation

### 7.1 Collection Home (`app/page.tsx`)

**Data fetching:** Server component fetches shows from `GET /api/collection` filtered by current sidebar filter + media type toggle.

**Rendering:** Shows grouped into status sections:
1. **Active** — prominent/larger tiles.
2. **Excited** — Later + Excited interest.
3. **Interested** — Later + Interested interest.
4. **Other** (collapsed) — Wait, Quit, Done, and Later without interest.

**Tile component:** Poster image, title, in-collection badge, user rating badge.

**Empty states:**
- No shows: prompt to Search/Ask with clear CTAs.
- Filter yields none: "No results found."

**Interactions:** Clicking a tile navigates to Show Detail.

### 7.2 Search (`app/find/search/page.tsx`)

- Text input with debounced live search against `GET /api/search`.
- Results in a poster grid.
- In-collection shows marked with a badge (cross-reference with user's collection).
- Clicking a result navigates to Show Detail.
- Optional: auto-open on launch if `autoSearch` setting is true.

### 7.3 Ask (`app/find/ask/page.tsx`)

**State:** Client-side state for chat messages (not persisted to DB — session only).

**Welcome view:**
- 6 random starter prompts from a curated pool of ~80 prompts.
- "Refresh" button to get new starters.

**Chat flow:**
1. User types a message.
2. Send to `POST /api/ai/ask` with: user message, recent turns, library context.
3. Stream AI response into the UI.
4. Parse `showList` from response; render mentioned shows as a horizontal scrollable strip.
5. Tapping a mentioned show navigates to Show Detail (or falls back to Search).

**"Ask About a Show" variant:** Initiated from Show Detail's "Ask about..." button. Seeds the conversation with show context and switches to Ask mode.

**Summarization:** After ~10 messages, invoke `/api/ai/summarize` on older turns and replace them in context.

### 7.4 Alchemy (`app/find/alchemy/page.tsx`)

**Multi-step flow (client state, session only):**

1. **Select shows** (2+ required): Search + collection picker. Display selected shows as removable chips/cards.
2. **Conceptualize:** Call `POST /api/ai/concepts` with all selected shows. Display concept chips.
3. **Select concepts** (1-8): Selectable chip UI.
4. **Alchemize:** Call `POST /api/ai/recommend` with selected concepts + shows. Display 6 recommendations with reasons.
5. **Chain ("More Alchemy!"):** Use results as new inputs, return to step 1.

**Backtracking:** Changing shows clears concepts and results. Changing concepts clears results.

**All session data is transient** — cleared when leaving Alchemy.

### 7.5 Show Detail (`app/shows/[id]/page.tsx`)

**Data fetching:** Fetch full show details from TMDB via `GET /api/shows/[id]?type=`. If show is in collection, merge with stored user data.

**Sections (in order):**
1. **Header media carousel** — backdrops, posters, logos, trailers. Graceful fallback to poster-only.
2. **Core facts** — year, runtime/seasons+episodes, community score bar.
3. **My Status + Interest chips** (toolbar) — Active, Interested, Excited, Done, Quit, Wait. Tapping saves; re-tapping triggers removal confirmation.
4. **My Rating** — slider/bar. Rating an unsaved show auto-saves as Done.
5. **My Tags** — chip display + tag picker. Adding a tag to unsaved show auto-saves as Later + Interested.
6. **Overview** — text.
7. **AI Scoop** — toggle button ("Give me the scoop!" / "Show the scoop" / "The Scoop"). Streams progressively. 4-hour freshness.
8. **"Ask about this show"** — CTA button navigating to Ask with show context.
9. **Genres + Languages**.
10. **Traditional recommendations** — horizontal strand of similar/recommended shows from TMDB.
11. **Explore Similar** — "Get Concepts" button -> concept chips -> "Explore Shows" button -> 5 AI recommendations.
12. **Streaming availability** — providers grouped by type (flatrate/rent/buy).
13. **Cast & Crew** — horizontal strands; tapping navigates to Person Detail.
14. **Seasons** (TV only) — expandable season/episode list.
15. **Budget vs Revenue** (movies, when data available).

**Auto-save business rules:**
- Setting any status -> saves to collection.
- Choosing Interested/Excited -> saves as Later + that interest level.
- Rating unsaved show -> saves as Done.
- Adding tag to unsaved show -> saves as Later + Interested.
- Removing status (re-tap active status) -> confirmation dialog -> removes from collection, clears all My Data.
- Confirmation dialog has "don't ask again" after repeated removals (`hideStatusRemovalConfirmation` flag).

### 7.6 Person Detail (`app/person/[id]/page.tsx`)

- Fetch person data from `GET /api/person/[id]`.
- Display: image gallery, name, bio.
- Analytics charts: average project ratings, top genres, projects-by-year (simple chart library or custom SVG).
- Filmography: credits grouped by year, scrollable.
- Tapping a credit navigates to Show Detail.

### 7.7 Settings (`app/settings/page.tsx`)

**Sections:**
- **App:** Font size selector (XS-XXL), Search on launch toggle.
- **User:** Username (editable, synced via `cloud_settings`).
- **AI:** API key input, model selection dropdown.
- **Integrations:** Catalog provider API key input.
- **Your Data:**
  - "Export My Data" button -> generates a `.zip` containing JSON backup of all saved shows and My Data. Dates in ISO-8601.
  - Import/Restore: placeholder for future implementation.

**Persistence:** Settings saved via `PUT /api/settings`. Local-only settings (`autoSearch`, `fontSize`) stored in `localStorage`. Cloud settings stored in `cloud_settings` table.

---

## 8. Collection API (CRUD)

### 8.1 Route Handlers

| Method | Route | Purpose |
|---|---|---|
| `GET` | `/api/collection` | List user's shows (with filters: status, tags, genre, decade, score range, media type) |
| `POST` | `/api/collection` | Add/save a show (upsert with merge rules) |
| `GET` | `/api/collection/[id]` | Get a single saved show |
| `PATCH` | `/api/collection/[id]` | Update My Data fields (status, interest, tags, score, scoop) |
| `DELETE` | `/api/collection/[id]` | Remove show from collection (clears all My Data) |
| `GET` | `/api/collection/export` | Export collection as JSON zip |

### 8.2 Upsert & Merge Logic
- On `POST`, check if `(namespace_id, user_id, external_id)` exists.
- If exists: merge using the rules (non-my fields: `selectFirstNonEmpty`; my fields: newer timestamp wins).
- If new: insert with `creation_date = now()`.
- Always set `details_update_date = now()` on merge.

### 8.3 Filter Queries
- Collection Home queries filter by `namespace_id` + `user_id` + optional filters.
- Tag filters: `WHERE 'tagName' = ANY(my_tags)`.
- Genre filters: `WHERE 'genreName' = ANY(genres)`.
- Decade filters: extract year from `release_date`/`first_air_date`, bucket by decade.
- Score range: `WHERE vote_average BETWEEN x AND y`.
- Media type: `WHERE show_type = 'movie'` or `'tv'`.

### 8.4 Tag Library
- Derived dynamically: `SELECT DISTINCT unnest(my_tags) FROM shows WHERE namespace_id = $1 AND user_id = $2 AND my_status IS NOT NULL`.
- Powers the sidebar tag filter list.

---

## 9. Client State Management

### 9.1 Server State (Supabase-backed)
- Collection data, settings, and cloud state are fetched/mutated via API routes.
- Use Next.js server components for initial data loading where possible.
- Client components use `fetch` with SWR or React Query for cache invalidation and optimistic updates.

### 9.2 Transient Client State (Zustand or Context)
- **Ask session:** chat messages, mentioned shows strip. Cleared on leave/reset.
- **Alchemy session:** selected shows, concepts, results. Cleared on leave.
- **Explore Similar state:** concepts and recommendations per show detail. Cleared on navigation.
- **UI state:** current filter, media type toggle, sidebar open/close.

### 9.3 Local Persistence
- `localStorage` for: `autoSearch`, `fontSize`, `hideStatusRemovalConfirmation`, `statusRemovalCountKey`, `lastSelectedFilter`.

---

## 10. Data Export

- `GET /api/collection/export` fetches all shows for (namespace, user).
- Serializes to JSON with ISO-8601 dates.
- Packages into a `.zip` file using a server-side zip library (e.g. `archiver` or `jszip`).
- Returns the zip as a downloadable response.

---

## 11. Data Model Versioning & Migration

- `app_metadata` table tracks `data_model_version`.
- On application startup (or via middleware), check current version against expected version.
- If mismatch, run forward migrations to bring data up to date.
- Migrations are SQL scripts that transform data in place, preserving all user collections, ratings, tags, statuses, and AI Scoops.
- Users never lose data due to an update.

---

## 12. Testing Strategy

### 12.1 Unit Tests
- Business logic: auto-save rules, merge logic, status transitions, default value assignments.
- AI response parsers: showList parsing, concept extraction, recommendation mapping.
- Filter logic: tag, genre, decade, score filtering.

### 12.2 Integration Tests
- API route handlers: CRUD operations on collection, search proxy, AI endpoints (with mocked AI responses).
- Database operations: upsert/merge, RLS enforcement, namespace isolation.
- Test data uses `is_test = true` flag for clean teardown.

### 12.3 E2E Tests (Optional)
- Critical user journeys: build collection, rate-to-save, tag-to-save, Ask discovery, Alchemy flow.
- Using Playwright or Cypress.

### 12.4 Test Isolation
- Each test run uses the configured `namespace_id`.
- `npm run test:reset` calls `DELETE FROM shows WHERE namespace_id = $1 AND is_test = true` (and similarly for other tables).
- No global teardown required.

---

## 13. Implementation Phases

### Phase 1: Foundation (Infrastructure + Data Layer)
1. Next.js project scaffold with App Router, TypeScript, Tailwind.
2. Supabase setup: tables, RLS policies, migrations.
3. Environment variable interface (`.env.example`).
4. Dev identity injection middleware.
5. Namespace isolation in all queries.
6. Collection CRUD API routes with full merge logic.
7. Basic Supabase client (browser + server).

### Phase 2: Catalog Integration + Core UI Shell
1. TMDB proxy route handlers (search, details, credits, person, providers, trending).
2. TMDB response-to-Show mapping with genre resolution and image URL construction.
3. App layout: sidebar (filters), top nav (media toggle, Find, Settings).
4. Collection Home page with status-grouped sections and tile components.
5. Filter system: all shows, tag filters, genre, decade, score.

### Phase 3: Show Detail + Person Detail
1. Show Detail page with all 15 sections.
2. Auto-save business rules (status, rating, tag triggers).
3. Removal flow with confirmation dialog and "don't ask again".
4. Catalog-to-collection merge on detail view.
5. Person Detail page with filmography and analytics charts.

### Phase 4: Search
1. Search page with debounced text search.
2. Poster grid results with in-collection badges.
3. Search-on-launch setting.

### Phase 5: AI Features
1. AI Scoop: streaming generation, 4-hour cache, toggle UX.
2. Ask: chat UI, streaming responses, mentioned shows strip, starter prompts, summarization.
3. Ask About Show: context seeding from Show Detail.
4. Concepts: single-show and multi-show generation, chip UI.
5. Explore Similar: concept selection -> 5 recommendations.
6. Alchemy: full multi-step flow with chaining.
7. Structured output parsing with retry/fallback logic.
8. Recommendation resolution: TMDB ID lookup + title verification.

### Phase 6: Settings + Export
1. Settings page: font size, search on launch, username, API keys, model selection.
2. Cloud settings sync via Supabase.
3. Export: JSON backup in zip format.
4. Data model versioning and migration check on startup.

### Phase 7: Polish + Testing
1. Empty states and loading states for all views.
2. Responsive design and accessibility.
3. Unit tests for business logic and parsers.
4. Integration tests for API routes and database operations.
5. Test reset script.
6. E2E tests for critical user journeys.

---

## 14. Key Architectural Decisions

1. **Server-side API routes for all external calls** — TMDB key and AI key never reach the browser. Supabase anon key is the only client-exposed credential.

2. **Single `shows` table with user overlay** — Combines catalog data and user data in one row per (namespace, user, show). Simplifies queries and enforces the "user version takes precedence" rule at the data layer.

3. **Namespace + user_id partitioning** — Every query includes both dimensions. RLS enforces this at the Supabase level, making cross-build and cross-user data leaks impossible.

4. **Opaque string user_id** — No provider-specific encoding. OAuth migration requires only middleware changes.

5. **Transient AI session state** — Ask, Alchemy, and Explore Similar sessions live in client memory. No database persistence for chat history or alchemy results, matching the PRD's data persistence rules.

6. **Streaming AI responses** — Scoop and Ask use streaming to avoid blank-screen waits. Concepts and recommendations use standard request/response (smaller payloads).

7. **Declarative merge rules** — Catalog refresh and sync conflict resolution use the same `selectFirstNonEmpty` / timestamp-wins logic, implemented once and reused.

---

## 15. Risk Mitigation

| Risk | Mitigation |
|---|---|
| AI hallucinating show titles | Every recommendation is verified against TMDB by external ID + case-insensitive title match. Unresolvable titles shown non-interactively or handed off to Search. |
| AI structured output parsing failures | Retry once with stricter formatting instructions. Fall back to unstructured commentary + Search handoff. Zod validation on all parsed outputs. |
| TMDB rate limiting | Server-side caching of genre lists and trending. Debounced search. Per-show detail cache with TTL. |
| Namespace data collision | RLS policies + unique constraints on `(namespace_id, user_id, external_id)`. All queries include `namespace_id` as a mandatory filter. |
| Data loss on update | `app_metadata.data_model_version` + forward-only migrations that preserve all user data. |
| API key exposure | TMDB and AI keys are server-only env vars. Supabase service role key is server-only. Only the anon key reaches the client. |
