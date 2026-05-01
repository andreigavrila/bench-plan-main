# Implementation Plan — TV & Movie Companion App

> **Deliverable:** Planning-only document for the product defined in `docs/prd/product_prd.md`, `docs/prd/infra_rider_prd.md`, and supporting documents.  
> **Baseline:** Next.js (latest stable) + Supabase.  
> **Architecture:** Fractal feature architecture per `INSTRUCTIONS.md`.

---

## 1. Overview & Goals

Build a personal TV + movie companion that lets users collect, organize, rate, tag, and discover entertainment through taste-aware AI. The app must:

1. Make a user’s taste visible and actionable (status, tags, ratings, AI Scoop).
2. Provide high-quality, taste-aware discovery via Ask, Alchemy, and Explore Similar.
3. Keep user data durable, consistent, and scoped per user/namespace.
4. Preserve the app’s emotional “heart” — warm, opinionated, spoiler-safe AI voice.

---

## 2. Tech Stack & Infrastructure

### 2.1 Runtime & Framework
- **Next.js** (latest stable) with App Router.
- **TypeScript** throughout.
- **React Server Components** as the default; client components only where interactivity is required.

### 2.2 Persistence
- **Supabase** (hosted or local) as the single source of truth.
  - PostgreSQL for relational data.
  - Supabase Auth (or dev-only identity injection) for `user_id`.
  - Row-Level Security (RLS) policies scoped to `(namespace_id, user_id)`.

### 2.3 External Services
- **Content Catalog API** (e.g., TMDB or equivalent) for show metadata, search, cast/crew, streaming providers.
- **AI Provider API** (OpenAI, Anthropic, or equivalent) for Scoop, Ask, Concepts, and Recommendations.

### 2.4 Styling
- CSS-in-JS or Tailwind with a centralized `theme/` directory for tokens (no magic numbers or inline styles in components).

### 2.5 State Management
- Server state → Supabase queries/mutations (cached via React Query or similar).
- Local UI state → React hooks.
- Transient AI session state → React context or Zustand (ephemeral by design).

---

## 3. Repo Structure (Fractal Architecture)

```
src/
├── config/               # Env vars, constants, feature flags
├── theme/                # Design tokens, breakpoints, typography scales
├── components/           # Shared UI primitives (Button, Tile, Chip, Strand, etc.)
├── hooks/                # Global reusable hooks (useAuth, useNamespace, etc.)
├── utils/                # Pure utilities (mergeShows, date parsers, id generators)
├── lib/                  # Initialized clients (supabaseClient, aiClient, catalogClient)
├── types/                # Global TypeScript types derived from PRD schemas
├── pages/                # Top-level routes (Next.js app router segments)
│   ├── layout.tsx        # Root layout with namespace + user providers
│   ├── page.tsx          # Collection Home (default route)
│   ├── find/
│   │   └── page.tsx      # Find/Discover hub (Search / Ask / Alchemy switcher)
│   ├── show/
│   │   └── [id]/
│   │       └── page.tsx  # Show Detail
│   ├── person/
│   │   └── [id]/
│   │       └── page.tsx  # Person Detail
│   └── settings/
│       └── page.tsx      # Settings & Export
└── features/             # Fractal features (co-located hooks, utils, sub-features)
    ├── CollectionHome/
    │   ├── CollectionHome.tsx
    │   ├── hooks/
    │   ├── utils/
    │   └── features/
    │       ├── StatusSection/
    │       ├── FilterSidebar/
    │       └── ShowTile/
    ├── ShowDetail/
    │   ├── ShowDetail.tsx
    │   └── features/
    │       ├── HeaderMedia/
    │       ├── MyRelationshipToolbar/
    │       ├── OverviewScoop/
    │       ├── ExploreSimilar/
    │       ├── RecommendationsStrand/
    │       ├── CastCrewStrand/
    │       └── SeasonsPanel/
    ├── FindHub/
    │   ├── FindHub.tsx
    │   └── features/
    │       ├── Search/
    │       ├── AskChat/
    │       └── Alchemy/
    ├── PersonDetail/
    │   ├── PersonDetail.tsx
    │   └── features/
    │       ├── Filmography/
    │       └── AnalyticsCharts/
    └── Settings/
        ├── Settings.tsx
        └── features/
            ├── ExportData/
            └── ImportData/
```

**Naming rule:** Avoid `index.tsx`. The main file in a directory matches the directory name (e.g., `ShowDetail/ShowDetail.tsx`).

---

## 4. Database Schema (Supabase)

### 4.1 Core Tables

#### `shows`
Stores the merged canonical show + user overlay. Partitioned logically by `user_id` and `namespace_id`.

| Column | Type | Notes |
|--------|------|-------|
| `id` | `uuid` | Primary key (local stable id, not external catalog id) |
| `user_id` | `uuid` | Required. RLS filter target. |
| `namespace_id` | `text` | Required. Build/run isolation. |
| `external_id` | `text` | Catalog identifier for mapping/reconciliation. |
| `title` | `text` | Required. |
| `show_type` | `text` | `"movie" \| "tv" \| "unknown"` |
| `external_ids` | `jsonb` | Optional external identifiers blob. |
| `overview` | `text` | |
| `genres` | `text[]` | Genre names. |
| `tagline` | `text` | |
| `homepage` | `text` | |
| `original_language` | `text` | |
| `spoken_languages` | `text[]` | |
| `languages` | `text[]` | |
| `poster_url` | `text` | |
| `backdrop_url` | `text` | |
| `logo_url` | `text` | Best-rated, prefer English. |
| `network_logos` | `text[]` | Reserved. |
| `vote_average` | `double` | Community score. |
| `popularity` | `double` | |
| `vote_count` | `int` | |
| `last_air_date` | `date` | |
| `first_air_date` | `date` | |
| `release_date` | `date` | |
| `runtime` | `int` | Movie minutes. |
| `budget` | `bigint` | Movie only. |
| `revenue` | `bigint` | Movie only. |
| `series_status` | `text` | TV only. |
| `number_of_episodes` | `int` | TV only. |
| `number_of_seasons` | `int` | TV only. |
| `episode_run_time` | `int[]` | TV only. |
| `last_episode_run_time` | `int` | Reserved. |
| `my_tags` | `text[]` | User tags. |
| `my_tags_update_date` | `timestamptz` | |
| `my_score` | `double` | User rating. |
| `my_score_update_date` | `timestamptz` | |
| `my_status` | `text` | `"active" \| "next" \| "later" \| "done" \| "quit" \| "wait"` |
| `my_status_update_date` | `timestamptz` | |
| `my_interest` | `text` | `"excited" \| "interested"` |
| `my_interest_update_date` | `timestamptz` | |
| `ai_scoop` | `text` | AI-generated personality review. |
| `ai_scoop_update_date` | `timestamptz` | |
| `details_update_date` | `timestamptz` | Refreshed on catalog merge. |
| `creation_date` | `timestamptz` | Set once on first save. |
| `is_test` | `boolean` | Default `false`. |
| `provider_data` | `jsonb` | `{ countries: { [code]: { flatrate?: number[], rent?: number[], buy?: number[] } } }` |

**Indexes:**
- `(namespace_id, user_id, my_status)` for home queries.
- `(namespace_id, user_id, my_tags)` for tag filters.
- `(namespace_id, user_id, external_id)` for catalog mapping.
- `(namespace_id, user_id, my_status_update_date DESC)` for recency sorting.

#### `settings`
Per-user, per-namespace synced settings.

| Column | Type | Notes |
|--------|------|-------|
| `id` | `text` | Primary key; default `"globalSettings"` |
| `user_id` | `uuid` | Required. |
| `namespace_id` | `text` | Required. |
| `user_name` | `text` | Random on first launch. |
| `version` | `double` | Epoch seconds for conflict resolution. |
| `catalog_api_key` | `text` | Optional. Never log/commit. |
| `ai_api_key` | `text` | Optional. Never log/commit. |
| `ai_model` | `text` | Model key/name. |

#### `app_metadata`
Tracks data model version for migrations.

| Column | Type | Notes |
|--------|------|-------|
| `id` | `text` | `"appMetadata"` |
| `namespace_id` | `text` | Required. |
| `data_model_version` | `int` | Default `3`. |

### 4.2 Row-Level Security (RLS)
Every user-owned table must enforce:
- `namespace_id = current_setting('app.namespace_id')` (or equivalent injection)
- `user_id = current_setting('app.user_id')` (or auth.uid())

Server-side queries must set these configuration parameters (or use Supabase `auth.uid()` directly where auth is enabled).

### 4.3 Migrations
- Use Supabase CLI migrations (`supabase/migrations/`) to version schema.
- Include deterministic seed fixtures for tests.
- Each migration must be idempotent and namespace-aware.

---

## 5. Identity, Auth & Isolation

### 5.1 Namespace Isolation
- At build/start time, read `NAMESPACE_ID` from environment.
- Every database read/write includes `namespace_id`.
- Test reset scripts target `DELETE ... WHERE namespace_id = ?` without touching other namespaces.

### 5.2 User Identity (Benchmark-Friendly)
- **Development mode:** inject `user_id` via a dev-only header (`X-User-Id`) or a fixed default user per namespace.
- **Production path:** Supabase Auth (OAuth) wired to the same `user_id` column without schema changes.
- All server routes must gate identity injection so it is disabled in production.

### 5.3 Auth Components
- `useAuth()` hook returns `user_id` and `namespace_id`.
- Root layout wraps children in `AuthProvider` + `NamespaceProvider`.

---

## 6. External Catalog Integration

### 6.1 Client Setup
- Initialize a catalog client in `lib/catalogClient.ts`.
- API key sourced from `settings.catalog_api_key` (user-provided) or env fallback.

### 6.2 Mapping & Merge Strategy
Implement a pure utility `mergeShows(newCatalogShow, existingShow)` with these rules:

1. **ID mapping:** external catalog `id` → `Show.external_id`. Generate a local stable UUID for `Show.id`.
2. **Show type inference:** `name` exists → `tv`; `title` exists → `movie`; else `unknown`.
3. **Image resolution:** map paths to full URLs. Logo selection: best-rated, prefer English.
4. **Non-"my" fields:** `selectFirstNonEmpty(newValue, oldValue)` — never overwrite non-empty with empty/nil.
5. **"My" fields:** resolve by `update_date` timestamp (newer wins).
6. **Post-merge:** set `details_update_date = now()`. Preserve `creation_date`.

### 6.3 Transient Data Strategy
The following are fetched on-demand for UI and **not** persisted:
- `cast`, `crew`, `seasons`, `videos`, `recommendations`, `similar`, `images` galleries.
- Store in React Query cache with a short TTL; safe to clear without data loss.

---

## 7. Core Features Implementation Plan

### 7.1 Collection Home (`page.tsx` default route)

**Feature:** `CollectionHome/CollectionHome.tsx`

**Responsibilities:**
- Display the user’s library grouped by status sections.
- Support filters: All Shows, tags, genre, decade, community score ranges.
- Media-type toggle: All / Movies / TV.

**Status Grouping Logic:**
1. **Active** — `my_status = 'active'` (prominent/larger tiles).
2. **Excited** — `my_status = 'later' AND my_interest = 'excited'`.
3. **Interested** — `my_status = 'later' AND my_interest = 'interested'`.
4. **Other** — collapsed group containing `wait`, `quit`, `done`, and any `later` without interest.

**Sub-features:**
- `FilterSidebar`: renders filter list; dynamically adds tag filters based on existing tags; shows "No tags" filter when applicable.
- `ShowTile`: poster + title + in-collection badge + user rating badge.
- `StatusSection`: renders a grouped section with header and tile grid.

**Empty States:**
- No shows → prompt to Search/Ask.
- Filter yields none → "No results found."

**Server Query:**
```sql
SELECT * FROM shows
WHERE namespace_id = ? AND user_id = ?
  AND my_status IS NOT NULL
  AND (media_type_filter = 'all' OR show_type = ?)
  AND (filter_predicate ...)
ORDER BY my_status_update_date DESC;
```

### 7.2 Search (Find → Search)

**Feature:** `FindHub/features/Search/Search.tsx`

**Responsibilities:**
- Text search by title/keywords against the external catalog.
- Results in a poster grid; in-collection items marked via lookup against local `shows` table by `external_id`.
- Selecting a show opens `/show/[id]`.
- Optional "Search on Launch" behavior controlled by local setting `autoSearch`.

**Data Flow:**
1. User types query → debounced catalog API call.
2. Return catalog results mapped to `Show` shape.
3. Cross-join with local `shows` to overlay `my_status`, `my_score`.
4. Unsaved shows display as transient; saving happens on Detail.

### 7.3 Ask (Find → Ask)

**Feature:** `FindHub/features/AskChat/AskChat.tsx`

**Responsibilities:**
- Chat UI with user/assistant turns.
- Welcome view with 6 random starter prompts; refreshable.
- Mentioned shows strip: horizontally scrollable row of shows extracted from AI response.
- Session context retained; auto-summarize after ~10 turns.

**AI Contract:**
- Input: user message + library context + recent turns (summarized if needed).
- Output modes:
  - **General commentary:** plain text.
  - **Structured mentions:** `{ commentary: string, showList: "Title::externalId::mediaType;;..." }`
- Parse `showList`; resolve each title via catalog API; render selectable tiles in the mentions strip.
- If mapping fails, show title non-interactively or hand off to Search.

**State:**
- Chat history stored in Zustand/React state only (ephemeral, cleared on reset/leave).
- No persistence to Supabase.

**Variants:**
- **General Ask:** started from Find hub.
- **Ask About a Show:** launched from Show Detail with pre-seeded show context.

### 7.4 Alchemy (Find → Alchemy)

**Feature:** `FindHub/features/Alchemy/Alchemy.tsx`

**Flow:**
1. **Select Inputs:** User picks 2+ starting shows (from library + global catalog search).
2. **Conceptualize Shows:** AI generates shared concept catalysts (bullet list, 1–3 words each, max 8 returned).
3. **Select Concepts:** User selects 1–8 concepts (chips UI). Changing inputs clears concepts/results.
4. **Alchemize:** AI returns 6 recommended shows with reasons tied to selected concepts.
5. **Chain:** User can choose "More Alchemy!" using results as new inputs.

**AI Contract:**
- Input: selected shows (titles + IDs) + optional library context.
- Output: bullet list of concepts (multi-show must be shared/common).
- Recommendation output: list of 6 shows with reasons referencing concepts explicitly.

**State:**
- Session-only; cleared when leaving Alchemy.

### 7.5 Show Detail Page (`/show/[id]`)

**Feature:** `ShowDetail/ShowDetail.tsx`

**Narrative hierarchy (must preserve order unless intentionally changed):**
1. **Header Media Carousel** — backdrops/posters/logos/trailers. Graceful fallback if assets missing.
2. **Core Facts Row** — year, runtime/seasons, community score.
3. **My Relationship Toolbar** — status chips, rating slider, tags.
4. **Overview + Scoop Toggle** — factual overview + AI-generated personality review.
5. **Ask About This Show CTA** — seeds Ask with this show.
6. **Genres + Languages**
7. **Traditional Recommendations Strand** — similar/recommended from catalog.
8. **Explore Similar** — Get Concepts → select → Explore Shows.
9. **Streaming Availability** — "Stream It" providers by region.
10. **Cast & Crew** — horizontal strands → links to Person Detail.
11. **Seasons (TV only)** — collapsible/scrollable list.
12. **Budget/Revenue (movies)** — displayed when available.

**My Relationship Controls (Critical Business Rules):**
- **Status Chips:** Active / Interested / Excited / Done / Quit / Wait.
  - Selecting Interested/Excited sets `my_status = 'later'` + `my_interest`.
  - Reselecting active status triggers removal confirmation; on confirm, clear all My Data and delete show row.
- **Rating:** slider/input. Rating an unsaved show auto-saves with `my_status = 'done'`.
- **Tags:** free-form add/remove. Adding a tag to an unsaved show auto-saves with `my_status = 'later'`, `my_interest = 'interested'`.
- All user fields update their respective `update_date` timestamps.

**Scoop ("The Scoop"):**
- Generated on demand via AI if absent or stale (>4 hours since `ai_scoop_update_date`).
- Streams progressively; show "Generating..." state.
- Persisted only if show is in collection (`my_status IS NOT NULL`).
- Structured as a mini blog-post: personal take, stack-up vs reviews, centerpiece paragraph, fit/warnings, verdict.

**Explore Similar (Per-Show Concepts):**
1. Tap **Get Concepts** → AI generates 8 concepts for this single show.
2. Concepts rendered as selectable chips.
3. User selects 1+ concepts.
4. Tap **Explore Shows** → AI returns 5 recommendations grounded to real catalog items.
5. Reasons must explicitly name matched concepts.

**Data Loading:**
- Fetch stored show from Supabase by `id`.
- If not locally saved, fetch from catalog API by `external_id` and render transient.
- Merge on save using `mergeShows()`.

### 7.6 Person Detail Page (`/person/[id]`)

**Feature:** `PersonDetail/PersonDetail.tsx`

**Sections:**
- Image gallery, name, bio.
- Analytics charts: average project ratings, top genres, projects-by-year.
- Filmography grouped by year.
- Credit selection → navigates to `/show/[id]`.

**Data:**
- Fetch person details + credits from catalog API (transient).
- Cross-reference filmography with local `shows` to overlay user ratings/status badges.

### 7.7 Settings & Export (`/settings`)

**Feature:** `Settings/Settings.tsx`

**Sections:**
- **App Settings:** font size (`XS`–`XXL`), search-on-launch toggle.
- **User:** username (synced).
- **AI:** AI provider API key, AI model selection.
- **Integrations:** Content catalog API key.
- **Your Data:**
  - **Export / Backup:** "Export My Data" produces a `.zip` containing JSON backup of all saved shows + My Data + settings. Dates ISO-8601.
  - **Import / Restore:** desired but not currently implemented; leave extensible placeholder.

**Security:** API keys stored in `settings` table (server-side) and never committed to repo.

---

## 8. AI Integration Architecture

### 8.1 AI Client
- `lib/aiClient.ts` wraps the AI provider.
- Support for streaming responses (SSE) for Scoop and Ask.
- Configurable model/key per `settings.ai_model` / `settings.ai_api_key`.

### 8.2 Prompt Orchestration
Create a centralized `features/AIPrompts/` directory (or `lib/prompts/`) containing:

1. **`basePersona.ts`** — shared system prompt defining the warm, opinionated, spoiler-safe TV/movie nerd friend.
2. **`scoopPrompt.ts`** — structured mini-blog-post format with sections: personal take, stack-up, centerpiece, fit/warnings, verdict. Target 150–350 words.
3. **`askPrompt.ts`** — conversational discovery prompt with library context injection.
4. **`askWithMentionsPrompt.ts`** — same as Ask but with strict output format for `showList`.
5. **`conceptsPrompt.ts`** — single-show and multi-show variants. Bullet list only, 1–3 words, no explanations, shared concepts for multi-show.
6. **`recommendationsPrompt.ts`** — concept-based recs for Explore Similar (5) and Alchemy (6). Reasons must cite concepts.

### 8.3 Context Injection
Build a utility `buildAIContext(user_id, namespace_id, options)` that assembles:
- User library: titles, statuses, tags, ratings ( lightweight; limit to ~50 most recent/relevant ).
- Current show context (for Ask About This Show / Scoop / Explore Similar).
- Selected concepts (for Alchemy / Explore Similar).
- Recent conversation turns (for Ask), with summarization after ~10 turns.

### 8.4 Streaming & Parsing
- Scoop: stream text directly into UI.
- Ask with Mentions: stream text; on completion, parse `showList` delimiter pattern and resolve shows asynchronously.
- Concepts: parse bullet list; clean and deduplicate.
- Recommendations: parse list + reasons; resolve each title to catalog item via external ID or title search.

### 8.5 Fallbacks
- If catalog resolution fails for a recommended title → display non-interactive or hand to Search.
- If structured parsing fails → retry once with stricter formatting; else fall back to unstructured text.

### 8.6 Quality Heuristics (Non-blocking Monitoring)
- Log/rescue generic concepts ("good characters") for prompt tuning.
- Ensure recommendation reasons explicitly reference concepts.

---

## 9. Data Behaviors & Business Rules

### 9.1 Collection Membership
A show is "in collection" when `my_status IS NOT NULL`.

### 9.2 Saving Triggers
- Setting any status.
- Choosing an interest chip (Interested/Excited).
- Rating an unsaved show.
- Adding at least one tag to an unsaved show.

### 9.3 Default Values When Saving
- Default status: `Later`
- Default interest: `Interested`
- Exception: first save via rating → `Done`

### 9.4 Removing from Collection
- Trigger: reselect active status + confirm removal.
- Effects: delete row (or clear all My Data); show confirmation warning; track `hideStatusRemovalConfirmation` preference.

### 9.5 Re-adding the Same Show
- Preserve latest My Data.
- Refresh public metadata.
- Merge conflicts resolve by most recent `update_date` per field.

### 9.6 Timestamps
Every My Data field tracks `update_date` for sorting, sync conflict resolution, and AI cache freshness.

### 9.7 AI Data Persistence
| Data | Persisted? | Freshness | Notes |
|------|-----------|-----------|-------|
| AI Scoop | Yes (if in collection) | 4 hours | Regenerate on demand after expiry. |
| Alchemy results/reasons | No | Session only | Cleared on leaving Alchemy. |
| Ask chat history | No | Session only | Cleared on reset/leave. |
| Mentioned shows strip | No | Session only | Derived from current chat context. |

---

## 10. Cross-Cutting Concerns

### 10.1 User Data Ownership
- Export produces a `.zip` with JSON backup.
- All dates ISO-8601.
- Import placeholder ready for future extension.

### 10.2 Data Continuity Across Versions
- `app_metadata.data_model_version` tracks schema version.
- On app upgrade, run migration scripts that bring forward existing saved shows and My Data safely, without user intervention.

### 10.3 Sync (Future-Ready)
- All tables include `user_id` and `namespace_id`.
- Conflict resolution per field using `update_date` (newer wins).
- Duplicate detection by `external_id` + merge rules.

### 10.4 Error Handling & Resilience
- Network failures: surface inline retry; do not crash the session.
- Catalog API failures: degrade gracefully (hide sections, show error state).
- AI API failures: show friendly error; allow retry.

### 10.5 Performance
- Use React Query for caching catalog and Supabase results.
- Debounce search input (~300ms).
- Virtualize long lists (filmography, chat history) where needed.
- Lazy-load heavy Detail sections (seasons, cast/crew analytics).

---

## 11. Development Environment & Tooling

### 11.1 Environment Variables
Create `.env.example`:
```
# Supabase
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=       # server-only

# Default identity / namespace (dev/test only)
DEV_USER_ID=                     # optional; injected in dev mode
NAMESPACE_ID=                    # required; isolates data per build

# AI Provider (optional defaults; user may override in Settings)
AI_PROVIDER_API_KEY=
AI_MODEL=

# Catalog Provider (optional defaults; user may override in Settings)
CATALOG_API_KEY=
```

`.gitignore` must exclude `.env*` except `.env.example`.

### 11.2 Scripts (`package.json`)
- `npm run dev` — start Next.js dev server.
- `npm test` — run unit + integration tests.
- `npm run test:reset` — reset test data for the current `NAMESPACE_ID`.
- `npm run db:migrate` — apply Supabase migrations.
- `npm run db:seed` — seed fixtures for local development.

### 11.3 Testing Strategy
- **Unit tests:** pure utilities (`mergeShows`, prompt builders, parsers) adjacent to source.
- **Integration tests:** API route handlers with injected `namespace_id` and `user_id`.
- **Visual tests:** Storybook or equivalent for `ShowTile`, `ShowDetail` states, `AskChat` bubbles.
- **Destructive test isolation:** every test creates data within its namespace; teardown deletes by namespace only.

---

## 12. Migration Path to Real Auth & Production

- Replace dev identity injection with Supabase Auth OAuth.
- No schema redesign required; `user_id` column already exists and is opaque.
- Gate dev-only identity routes behind `process.env.NODE_ENV !== 'production'`.
- Namespace isolation remains valid for multi-tenant hosting or benchmark runs.

---

## 13. Open Questions & Optional Extensions (Post-MVP)

1. **Next as first-class UI status** — currently modeled (`next`) but not surfaced.
2. **Named custom lists** — beyond tags (e.g., "Weekend Watchlist").
3. **AI Scoop implicit save** — should generating Scoop on an unsaved show save it?
4. **Explicit Unrated state** — vs nil for `my_score`.
5. **Import/Restore from export zip** — UI placeholder exists; backend parser needed.
6. **Save/share Alchemy sessions** — reusable "blends."
7. **myStatus filters in sidebar** — model supports it; add UI filters.

---

## 14. Risk Summary & Mitigations

| Risk | Mitigation |
|------|------------|
| Catalog API rate limits / downtime | Cache aggressively; degrade gracefully; allow user-provided keys. |
| AI streaming complexity | Use stable SSE libraries; implement fallback to non-streaming. |
| Namespace leak / data collision | RLS + server-side parameter injection; test reset scoped to namespace. |
| Prompt drift across surfaces | Centralized prompt files + code review for tone consistency. |
| Schema migration pain | Versioned migrations; `app_metadata` tracking; forward-migrate on boot. |

---

*End of Plan*
