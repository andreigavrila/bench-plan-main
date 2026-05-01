# Implementation Plan

## 1. Project Overview

Build a personal TV + movie companion app that lets users collect, organize, rate, and discover entertainment. The app combines a personal library with AI-powered discovery (conversational Ask, Alchemy concept blending, and per-show Explore Similar). The benchmark build uses **Next.js** with **Supabase** for persistence, with namespace-based build isolation and dev-injected user identity.

---

## 2. Architecture Overview

### 2.1 Tech Stack (Benchmark Baseline)

| Layer | Technology |
|---|---|
| Frontend + Server | Next.js (latest stable) — App Router |
| Persistence | Supabase (hosted preferred, local optional) |
| AI Provider | Configurable via env (API key + model selection) |
| Catalog Provider | Configurable external catalog API (e.g., TMDB) |
| Auth (benchmark) | Dev-injected `user_id` via header or dev selector |
| Styling | Tailwind CSS (or equivalent utility-first approach) |
| Testing | Jest/Vitest + React Testing Library (or Next.js-compatible framework) |

### 2.2 High-Level Architecture

```
┌─────────────────────────────────────────────┐
│              Next.js Application            │
│  ┌──────────┐  ┌──────────┐  ┌───────────┐ │
│  │  Client   │  │  Server  │  │  API      │ │
│  │  (React)  │  │  Actions │  │  Routes   │ │
│  └────┬─────┘  └────┬─────┘  └─────┬─────┘ │
│       │              │              │        │
└───────┼──────────────┼──────────────┼────────┘
        │              │              │
        ▼              ▼              ▼
  ┌──────────┐  ┌──────────┐  ┌──────────────┐
  │ Supabase  │  │ Supabase  │  │ External     │
  │  (DB)     │  │  (RLS)    │  │ Catalog API  │
  └──────────┘  └──────────┘  └──────────────┘
                       │
                       ▼
              ┌────────────────┐
              │  AI Provider   │
              │  (LLM API)     │
              └────────────────┘
```

### 2.3 Isolation Model

- **`namespace_id`**: Per-build/run identifier, injected via env. All persisted data is scoped to this namespace.
- **`user_id`**: Per-user identifier, injected via dev header/selector in benchmark mode. All user-owned records are scoped to `(namespace_id, user_id)`.
- RLS policies in Supabase enforce data isolation at the database level.

---

## 3. Database Schema

### 3.1 Tables

#### `shows`
Stores the canonical show record with both public catalog data and user overlay data.

| Column | Type | Constraints |
|---|---|---|
| `id` | TEXT | PK |
| `namespace_id` | TEXT | NOT NULL |
| `user_id` | TEXT | NOT NULL |
| `title` | TEXT | NOT NULL |
| `show_type` | TEXT | NOT NULL (`movie`/`tv`/`person`/`unknown`) |
| `external_ids` | JSONB | Nullable |
| `overview` | TEXT | Nullable |
| `genres` | TEXT[] | DEFAULT `[]` |
| `tagline` | TEXT | Nullable |
| `homepage` | TEXT | Nullable |
| `original_language` | TEXT | Nullable |
| `spoken_languages` | TEXT[] | DEFAULT `[]` |
| `languages` | TEXT[] | DEFAULT `[]` |
| `poster_url` | TEXT | Nullable |
| `backdrop_url` | TEXT | Nullable |
| `logo_url` | TEXT | Nullable |
| `vote_average` | DOUBLE PRECISION | Nullable |
| `vote_count` | INTEGER | Nullable |
| `popularity` | DOUBLE PRECISION | Nullable |
| `first_air_date` | DATE | Nullable |
| `last_air_date` | DATE | Nullable |
| `release_date` | DATE | Nullable |
| `runtime` | INTEGER | Nullable |
| `budget` | INTEGER | Nullable |
| `revenue` | INTEGER | Nullable |
| `series_status` | TEXT | Nullable |
| `number_of_episodes` | INTEGER | Nullable |
| `number_of_seasons` | INTEGER | Nullable |
| `episode_run_time` | INTEGER[] | DEFAULT `[]` |
| `my_tags` | TEXT[] | DEFAULT `[]` |
| `my_tags_update_date` | TIMESTAMPTZ | Nullable |
| `my_score` | DOUBLE PRECISION | Nullable |
| `my_score_update_date` | TIMESTAMPTZ | Nullable |
| `my_status` | TEXT | Nullable (`active`/`next`/`later`/`done`/`quit`/`wait`) |
| `my_status_update_date` | TIMESTAMPTZ | Nullable |
| `my_interest` | TEXT | Nullable (`excited`/`interested`) |
| `my_interest_update_date` | TIMESTAMPTZ | Nullable |
| `ai_scoop` | TEXT | Nullable |
| `ai_scoop_update_date` | TIMESTAMPTZ | Nullable |
| `provider_data` | JSONB | Nullable |
| `details_update_date` | TIMESTAMPTZ | Nullable |
| `creation_date` | TIMESTAMPTZ | Nullable |
| `is_test` | BOOLEAN | DEFAULT `false` |

**Composite index**: `(namespace_id, user_id, my_status)` for collection queries.
**Composite index**: `(namespace_id, user_id, my_tags)` for tag filter queries.

#### `cloud_settings`
Stores synced app-wide settings.

| Column | Type | Constraints |
|---|---|---|
| `id` | TEXT | PK (default `globalSettings`) |
| `namespace_id` | TEXT | NOT NULL |
| `user_id` | TEXT | NOT NULL |
| `user_name` | TEXT | NOT NULL |
| `version` | BIGINT | NOT NULL (epoch seconds) |
| `catalog_api_key` | TEXT | Nullable |
| `ai_api_key` | TEXT | Nullable |
| `ai_model` | TEXT | NOT NULL |

#### `app_metadata`
Tracks data model version for migrations.

| Column | Type | Constraints |
|---|---|---|
| `id` | TEXT | PK |
| `namespace_id` | TEXT | NOT NULL |
| `data_model_version` | INTEGER | DEFAULT 3 |

### 3.2 Row-Level Security (RLS)

All tables enforce RLS policies scoped to `(namespace_id, user_id)`:
- `SELECT`: `WHERE namespace_id = current_setting('app.namespace_id') AND user_id = current_setting('app.user_id')`
- `INSERT`/`UPDATE`/`DELETE`: same scope
- Dev/test reset operations target a specific namespace only

### 3.3 Migrations

- Use Supabase migration tooling (or equivalent SQL migration framework).
- Migration `001_initial_schema`: creates all tables, indexes, RLS policies.
- Migration `002_seed_metadata`: inserts default `app_metadata` row.
- Seed scripts for test data are namespace-scoped.

---

## 4. Application Structure

### 4.1 Directory Layout

```
src/
├── app/                          # Next.js App Router
│   ├── layout.tsx                # Root layout (providers, nav)
│   ├── page.tsx                  # Home (Collection)
│   ├── find/
│   │   ├── page.tsx              # Find/Discover hub
│   │   ├── search/
│   │   │   └── page.tsx          # Search results
│   │   ├── ask/
│   │   │   └── page.tsx          # Ask chat
│   │   └── alchemy/
│   │       └── page.tsx          # Alchemy session
│   ├── show/[id]/
│   │   └── page.tsx              # Show Detail
│   ├── person/[id]/
│   │   └── page.tsx              # Person Detail
│   └── settings/
│       └── page.tsx              # Settings & Your Data
├── components/
│   ├── layout/
│   │   ├── Sidebar.tsx           # Filters/navigation panel
│   │   ├── TopNav.tsx            # Top navigation (Find, Settings)
│   │   └── MediaTypeToggle.tsx   # All/Movies/TV toggle
│   ├── collection/
│   │   ├── ShowTile.tsx          # Show tile with badges
│   │   ├── ShowGrid.tsx          # Grid of tiles
│   │   ├── StatusSection.tsx     # Grouped status section
│   │   └── EmptyState.tsx        # Empty collection state
│   ├── detail/
│   │   ├── HeaderMedia.tsx       # Backdrop/poster/logo carousel
│   │   ├── CoreFacts.tsx         # Year, runtime, scores
│   │   ├── StatusChips.tsx       # Status/interest controls
│   │   ├── RatingBar.tsx         # My Rating slider
│   │   ├── TagPicker.tsx         # My Tags display + picker
│   │   ├── ScoopSection.tsx      # AI Scoop toggle/stream
│   │   ├── Recommendations.tsx   # Traditional recs strand
│   │   ├── ExploreSimilar.tsx    # Concepts → recs
│   │   ├── StreamingProviders.tsx # Where to watch
│   │   ├── CastCrew.tsx          # Cast/crew strand
│   │   ├── Seasons.tsx           # TV seasons
│   │   └── BudgetRevenue.tsx     # Movie budget/revenue
│   ├── find/
│   │   ├── ModeSwitcher.tsx      # Search/Ask/Alchemy switcher
│   │   ├── SearchInput.tsx       # Search bar
│   │   ├── SearchResults.tsx     # Search results grid
│   │   ├── ChatView.tsx          # Ask chat UI
│   │   ├── WelcomePrompts.tsx    # Ask starter prompts
│   │   ├── MentionedShows.tsx    # Mentioned shows strip
│   │   ├── AlchemyInput.tsx      # Select starting shows
│   │   ├── ConceptSelector.tsx   # Concept chips
│   │   └── AlchemyResults.tsx    # Alchemy recommendations
│   ├── person/
│   │   ├── PersonHeader.tsx      # Image gallery, bio
│   │   ├── PersonAnalytics.tsx   # Charts (ratings, genres, projects)
│   │   └── Filmography.tsx       # Credits by year
│   ├── settings/
│   │   ├── AppSettings.tsx       # Font size, search on launch
│   │   ├── AISettings.tsx        # API key, model selection
│   │   ├── IntegrationSettings.tsx # Catalog API key
│   │   └── DataExport.tsx        # Export My Data
│   └── shared/
│       ├── ImageCarousel.tsx     # Header media carousel
│       ├── ScoreBar.tsx          # Community score visualization
│       └── ConfirmationDialog.tsx # Removal confirmation
├── lib/
│   ├── db/
│   │   ├── supabase.ts           # Supabase client setup
│   │   ├── shows.ts              # Show CRUD + queries
│   │   ├── settings.ts           # Settings CRUD
│   │   └── migrations.ts         # Migration runner
│   ├── api/
│   │   ├── catalog.ts            # External catalog client
│   │   ├── catalog-mapping.ts    # Catalog → Show mapping + merge
│   │   └── streaming.ts          # Streaming provider lookup
│   ├── ai/
│   │   ├── client.ts             # AI provider client
│   │   ├── ask.ts                # Ask chat logic
│   │   ├── scoop.ts              # Scoop generation
│   │   ├── concepts.ts           # Concept extraction
│   │   ├── recommendations.ts    # Concept-based recommendations
│   │   ├── prompts/              # Prompt templates per surface
│   │   │   ├── ask.ts
│   │   │   ├── scoop.ts
│   │   │   ├── concepts.ts
│   │   │   └── recommendations.ts
│   │   └── summarization.ts      # Chat summarization
│   ├── auth/
│   │   ├── dev-identity.ts       # Dev identity injection
│   │   └── middleware.ts         # Request middleware for user_id
│   ├── state/
│   │   ├── store.ts              # Client state (Zustand/Context)
│   │   └── filters.ts            # Filter state management
│   ├── utils/
│   │   ├── merge.ts              # Merge/overwrite policy
│   │   ├── dates.ts              # Timestamp handling
│   │   └── export.ts             # Data export (ZIP/JSON)
│   └── config/
│       ├── env.ts                # Environment variable validation
│       └── constants.ts          # Status types, defaults, etc.
├── types/
│   ├── show.ts                   # Show, ShowType, MyStatus, MyInterest
│   ├── filter.ts                 # FilterConfiguration, FilterType
│   ├── settings.ts               # CloudSettings, LocalSettings
│   ├── ai.ts                     # AI request/response types
│   └── catalog.ts                # Catalog API types
├── middleware.ts                  # Next.js middleware (auth, namespace)
└── styles/
    └── globals.css               # Global styles, Tailwind config
```

### 4.2 Environment Variables

Defined in `.env.example`:

| Variable | Purpose |
|---|---|
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase project URL |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase anon/public key (client-safe) |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase service role key (server-only) |
| `NAMESPACE_ID` | Build/run namespace identifier |
| `DEFAULT_USER_ID` | Dev-mode default user ID |
| `CATALOG_API_KEY` | External catalog API key |
| `CATALOG_BASE_URL` | External catalog base URL |
| `AI_API_KEY` | AI provider API key |
| `AI_MODEL` | Default AI model identifier |
| `AI_BASE_URL` | AI provider base URL (optional, for compatibility) |
| `NODE_ENV` | Environment (development/production/test) |

---

## 5. Implementation Phases

### Phase 1: Foundation & Infrastructure

**Goal**: Working Next.js app connected to Supabase with namespace isolation and dev identity.

**Tasks**:
1. Initialize Next.js project with App Router, TypeScript, Tailwind CSS.
2. Configure Supabase client (anon key for client, service role for server).
3. Create database migrations:
   - `shows` table with all columns, indexes, RLS policies.
   - `cloud_settings` table with RLS.
   - `app_metadata` table.
4. Implement environment variable validation (`lib/config/env.ts`).
5. Implement dev identity injection:
   - Middleware reads `X-User-Id` header or `DEFAULT_USER_ID` env.
   - Sets `user_id` and `namespace_id` on request context.
   - Gated: disabled when `NODE_ENV=production`.
6. Implement basic Supabase CRUD (`lib/db/shows.ts`, `lib/db/settings.ts`).
7. Create `.env.example` and `.gitignore`.
8. Add npm scripts: `dev`, `build`, `test`, `test:reset`.
9. Implement test reset script: deletes all data for current `NAMESPACE_ID`.

**Deliverables**:
- `src/lib/db/supabase.ts`
- `src/lib/db/shows.ts`
- `src/lib/db/settings.ts`
- `src/lib/auth/dev-identity.ts`
- `src/lib/auth/middleware.ts`
- `src/middleware.ts`
- `supabase/migrations/001_initial_schema.sql`
- `.env.example`, `.gitignore`
- `package.json` scripts

---

### Phase 2: Catalog Integration & Data Layer

**Goal**: Fetch shows from external catalog, map to internal schema, persist with merge rules.

**Tasks**:
1. Implement catalog API client (`lib/api/catalog.ts`):
   - Search by query.
   - Fetch show details by ID.
   - Fetch cast/crew, seasons, videos, images, recommendations, similar.
   - Fetch streaming providers.
2. Implement catalog → Show mapping (`lib/api/catalog-mapping.ts`):
   - Map all fields per storage-schema.md rules.
   - Handle date parsing, genre name mapping, image URL construction.
   - Select best logo deterministically.
3. Implement merge/overwrite policy (`lib/utils/merge.ts`):
   - Non-my fields: `selectFirstNonEmpty` (never overwrite non-empty with empty).
   - My fields: resolve by timestamp (newer wins).
   - Set `detailsUpdateDate` on merge.
4. Implement show save/update/delete with namespace + user scoping.
5. Implement collection queries:
   - All shows for user.
   - Filter by status, tags, genre, decade, community score.
   - Media type toggle (all/movies/tv).

**Deliverables**:
- `src/lib/api/catalog.ts`
- `src/lib/api/catalog-mapping.ts`
- `src/lib/utils/merge.ts`
- Updated `src/lib/db/shows.ts` with full query support

---

### Phase 3: Collection Home & Basic UI

**Goal**: Users can view their collection, browse by status, and see show tiles.

**Tasks**:
1. Build root layout with sidebar and main content area.
2. Build sidebar (`components/layout/Sidebar.tsx`):
   - "All Shows" default filter.
   - Tag filters (dynamically generated from user's tags).
   - "No tags" filter if applicable.
   - Data filters: genre, decade, community score ranges.
   - Persist `lastSelectedFilter` in UI state.
3. Build media type toggle (`components/layout/MediaTypeToggle.tsx`).
4. Build collection home page (`app/page.tsx`):
   - Fetch filtered shows from Supabase.
   - Group by status: Active, Excited, Interested, Other (collapsed).
   - Render `StatusSection` for each group.
   - Active section uses larger tiles.
5. Build `ShowTile` component:
   - Poster, title, in-collection indicator, user rating indicator.
   - Click navigates to Show Detail.
6. Build empty states.
7. Implement client-side filter state management (`lib/state/filters.ts`).

**Deliverables**:
- `src/app/layout.tsx`
- `src/app/page.tsx`
- `src/components/layout/Sidebar.tsx`
- `src/components/layout/MediaTypeToggle.tsx`
- `src/components/collection/ShowTile.tsx`
- `src/components/collection/ShowGrid.tsx`
- `src/components/collection/StatusSection.tsx`
- `src/components/collection/EmptyState.tsx`
- `src/lib/state/filters.ts`

---

### Phase 4: Search & Show Detail (Core)

**Goal**: Users can search the catalog and view show details with My Data controls.

**Tasks**:
1. Build Find hub with mode switcher (`app/find/page.tsx`, `components/find/ModeSwitcher.tsx`).
2. Build Search page (`app/find/search/page.tsx`):
   - Search input with debounced query.
   - Results grid with in-collection indicators.
   - Auto-open on launch if `autoSearch` setting is enabled.
3. Build Show Detail page (`app/show/[id]/page.tsx`):
   - Server component fetches show data (catalog + user overlay).
   - Sections in narrative hierarchy order:
     1. Header media carousel (backdrops/posters/logos/videos).
     2. Core facts + community score.
     3. My Tags.
     4. Overview.
     5. Genres + languages.
     6. Traditional recommendations strand.
     7. Streaming availability.
     8. Cast & crew strand.
     9. Seasons (TV only).
     10. Budget/revenue (movies).
4. Build My Data controls on Detail:
   - Status/Interest chips in toolbar (`components/detail/StatusChips.tsx`):
     - Active, Interested, Excited, Done, Quit, Wait.
     - Interested/Excited set status=Later + interest.
     - Reselecting triggers removal confirmation.
   - Rating bar (`components/detail/RatingBar.tsx`):
     - Slider with unrated state.
     - Rating unsaved show auto-saves as Done.
   - Tag picker (`components/detail/TagPicker.tsx`):
     - Free-form tag input.
     - Adding tag to unsaved show auto-saves as Later + Interested.
5. Implement auto-save triggers and default values per PRD §5.2-5.3.
6. Implement removal confirmation with "don't ask again" option.

**Deliverables**:
- `src/app/find/page.tsx`
- `src/app/find/search/page.tsx`
- `src/app/show/[id]/page.tsx`
- `src/components/find/ModeSwitcher.tsx`
- `src/components/find/SearchInput.tsx`
- `src/components/find/SearchResults.tsx`
- `src/components/detail/HeaderMedia.tsx`
- `src/components/detail/CoreFacts.tsx`
- `src/components/detail/StatusChips.tsx`
- `src/components/detail/RatingBar.tsx`
- `src/components/detail/TagPicker.tsx`
- `src/components/detail/Recommendations.tsx`
- `src/components/detail/StreamingProviders.tsx`
- `src/components/detail/CastCrew.tsx`
- `src/components/detail/Seasons.tsx`
- `src/components/detail/BudgetRevenue.tsx`
- `src/components/shared/ConfirmationDialog.tsx`

---

### Phase 5: AI Integration — Scoop & Concepts

**Goal**: AI-powered Scoop generation and concept extraction working.

**Tasks**:
1. Implement AI provider client (`lib/ai/client.ts`):
   - Configurable base URL, API key, model.
   - Streaming support for progressive output.
   - Structured output parsing (for Ask with mentions).
2. Implement prompt templates:
   - Scoop prompt (`lib/ai/prompts/scoop.ts`): personality-driven, spoiler-safe, structured sections.
   - Concept prompt (`lib/ai/prompts/concepts.ts`): 1-3 word evocative bullets, shared for multi-show.
   - Include user library context in prompts (taste-aware).
3. Implement Scoop generation (`lib/ai/scoop.ts`):
   - On-demand from Detail page.
   - Check freshness (4-hour cache via `aiScoopUpdateDate`).
   - Stream response progressively.
   - Persist only if show is in collection.
4. Implement concept extraction (`lib/ai/concepts.ts`):
   - Single-show: "Get Concepts" from Detail.
   - Multi-show: shared concepts for Alchemy.
   - Return bullet list, 1-3 words each, no explanations.
   - Quality constraints: specific, diverse, ordered by strength.
5. Build Scoop UI (`components/detail/ScoopSection.tsx`):
   - Toggle: "Give me the scoop!" → "Show the scoop" → "The Scoop".
   - Streaming display with "Generating..." state.
6. Build Explore Similar UI (`components/detail/ExploreSimilar.tsx`):
   - "Get Concepts" button → concept chips.
   - Select concepts → "Explore Shows" button.

**Deliverables**:
- `src/lib/ai/client.ts`
- `src/lib/ai/scoop.ts`
- `src/lib/ai/concepts.ts`
- `src/lib/ai/prompts/scoop.ts`
- `src/lib/ai/prompts/concepts.ts`
- `src/components/detail/ScoopSection.tsx`
- `src/components/detail/ExploreSimilar.tsx`
- `src/components/shared/ImageCarousel.tsx`

---

### Phase 6: AI Integration — Ask (Chat)

**Goal**: Conversational AI discovery with mentioned shows.

**Tasks**:
1. Implement Ask chat logic (`lib/ai/ask.ts`):
   - Accept user message + conversation history.
   - Include user library context (taste-aware).
   - Support "Ask about this show" with show context seeding.
   - Implement conversation summarization after ~10 messages.
2. Implement structured output parsing for mentioned shows:
   - Parse `Title::externalId::mediaType;;...` format.
   - Resolve mentioned shows to catalog items.
   - Fallback: retry with stricter formatting, then unstructured + search handoff.
3. Implement chat summarization (`lib/ai/summarization.ts`):
   - Summarize older turns into 1-2 sentences.
   - Preserve persona/tone in summaries.
4. Build Ask page (`app/find/ask/page.tsx`):
   - Chat UI with user/assistant turns.
   - Welcome view with 6 random starter prompts (refreshable).
   - Mentioned shows horizontal strip.
   - Streaming responses.
5. Build "Ask about this show" integration from Detail page.
6. Implement session lifecycle: context retained during session, cleared on reset/exit.

**Deliverables**:
- `src/lib/ai/ask.ts`
- `src/lib/ai/summarization.ts`
- `src/lib/ai/prompts/ask.ts`
- `src/app/find/ask/page.tsx`
- `src/components/find/ChatView.tsx`
- `src/components/find/WelcomePrompts.tsx`
- `src/components/find/MentionedShows.tsx`

---

### Phase 7: AI Integration — Alchemy

**Goal**: Multi-show concept blending discovery.

**Tasks**:
1. Implement concept-based recommendations (`lib/ai/recommendations.ts`):
   - Accept selected concepts + user library context.
   - Return 6 recommendations (Alchemy) or 5 (Explore Similar).
   - Each rec includes title, external ID, media type, reason.
   - Reasons explicitly reference selected concepts.
   - Resolve recommendations to real catalog items.
2. Implement Alchemy session logic:
   - Step 1: Select 2+ starting shows (from library + catalog search).
   - Step 2: "Conceptualize Shows" → fetch shared concepts.
   - Step 3: Select up to 8 concepts.
   - Step 4: "ALCHEMIZE!" → fetch recommendations.
   - Step 5: "More Alchemy!" to chain (use results as new inputs).
   - Backtracking: changing shows clears concepts/results.
3. Build Alchemy page (`app/find/alchemy/page.tsx`):
   - Step-based UI with clear progression.
   - Show selector with search integration.
   - Concept chip selector (max 8).
   - Results display with reasons.
   - Chain support.
4. Implement AI recommendation → catalog resolution:
   - Match by external ID, then case-insensitive title.
   - Unresolved titles shown as non-interactive or handed off to Search.

**Deliverables**:
- `src/lib/ai/recommendations.ts`
- `src/lib/ai/prompts/recommendations.ts`
- `src/app/find/alchemy/page.tsx`
- `src/components/find/AlchemyInput.tsx`
- `src/components/find/ConceptSelector.tsx`
- `src/components/find/AlchemyResults.tsx`

---

### Phase 8: Person Detail

**Goal**: Explore cast/crew with filmography and analytics.

**Tasks**:
1. Implement person data fetching from catalog API.
2. Build Person Detail page (`app/person/[id]/page.tsx`):
   - Image gallery, name, bio.
   - Analytics charts:
     - Average project ratings over time.
     - Top genres distribution.
     - Projects by year bar chart.
   - Filmography grouped by year.
   - Credit items link to Show Detail.
3. Integrate Person Detail navigation from Show Detail cast/crew strand.

**Deliverables**:
- `src/app/person/[id]/page.tsx`
- `src/components/person/PersonHeader.tsx`
- `src/components/person/PersonAnalytics.tsx`
- `src/components/person/Filmography.tsx`

---

### Phase 9: Settings & Data Export

**Goal**: App settings, AI configuration, and data export.

**Tasks**:
1. Build Settings page (`app/settings/page.tsx`):
   - App settings: font size selector, search-on-launch toggle.
   - User: display/edit username (synced).
   - AI settings: API key input, model selector (synced).
   - Integration settings: catalog API key input (synced).
2. Implement settings persistence to `cloud_settings` table.
3. Implement local settings persistence (font size, auto search).
4. Build data export (`components/settings/DataExport.tsx`):
   - "Export My Data" button.
   - Generate JSON of all saved shows + My Data.
   - Dates encoded as ISO-8601.
   - Package into ZIP file for download.
5. Implement UI state persistence (hide confirmation, filter state).

**Deliverables**:
- `src/app/settings/page.tsx`
- `src/components/settings/AppSettings.tsx`
- `src/components/settings/AISettings.tsx`
- `src/components/settings/IntegrationSettings.tsx`
- `src/components/settings/DataExport.tsx`
- `src/lib/utils/export.ts`
- Updated `src/lib/db/settings.ts`

---

### Phase 10: Cross-Cutting Concerns & Polish

**Goal**: Ensure all cross-cutting rules are satisfied and the app feels cohesive.

**Tasks**:
1. **User data precedence**: Verify all show displays use user-overlaid data where available.
2. **Tile indicators**: In-collection and user rating badges on all tiles.
3. **Display rule audit**: Every show appearance (lists, search, AI outputs) uses user overlay.
4. **Timestamp tracking**: All my* fields track `*UpdateDate` on every write.
5. **Conflict resolution**: Merge logic handles timestamp-based resolution correctly.
6. **Data continuity**: Implement migration system for future schema changes.
7. **Spoiler safety**: All AI prompts include spoiler-safe instructions by default.
8. **AI guardrails**: Domain restriction (TV/movies only), fallback handling for parse failures.
9. **Error handling**: Graceful degradation for catalog/AI failures.
10. **Loading states**: Skeleton screens and progressive loading throughout.
11. **Responsive design**: Works on desktop and tablet viewports.
12. **Accessibility**: Keyboard navigation, ARIA labels, color contrast.

**Deliverables**:
- Audit and fix passes across all components.
- `src/lib/utils/dates.ts` for timestamp utilities.
- Error boundary components.
- Loading skeleton components.

---

### Phase 11: Testing

**Goal**: Comprehensive test coverage with namespace-scoped destructive testing.

**Tasks**:
1. **Unit tests**:
   - Merge/overwrite policy (`lib/utils/merge.ts`).
   - Catalog mapping (`lib/api/catalog-mapping.ts`).
   - AI output parsing (structured show list format).
   - Auto-save trigger logic.
   - Filter logic.
2. **Integration tests**:
   - Show CRUD with Supabase (namespace-scoped).
   - Collection queries with filters.
   - Settings persistence.
3. **Component tests**:
   - ShowTile rendering with badges.
   - Status chip interactions and auto-save.
   - Rating bar auto-save.
   - Tag picker auto-save.
   - Scoop toggle and streaming display.
   - Alchemy step progression.
4. **E2E tests** (Playwright or equivalent):
   - Full user journey: search → save → tag → rate → view collection.
   - Ask chat session with mentioned shows.
   - Alchemy session with chaining.
   - Data export.
5. **Test infrastructure**:
   - Test reset script clears namespace data.
   - Test fixtures with sample shows.
   - Mock catalog API responses.
   - Mock AI provider responses.
6. **Destructive testing**:
   - Verify namespace isolation (two namespaces don't collide).
   - Verify test reset only affects current namespace.

**Deliverables**:
- `tests/unit/` — unit tests
- `tests/integration/` — integration tests
- `tests/components/` — component tests
- `tests/e2e/` — end-to-end tests
- `tests/fixtures/` — test data
- `tests/mocks/` — API mocks
- `npm run test:reset` script

---

## 6. Key Technical Decisions

### 6.1 State Management
- **Server state**: Supabase as source of truth. Server Components fetch directly.
- **Client state**: React Server Actions for mutations. Optimistic updates where appropriate.
- **Local UI state**: `useState`/`useReducer` for ephemeral state (chat, Alchemy session, filter selection).
- **No offline-first**: Client cache is disposable per infra rider §6.2.

### 6.2 AI Integration Pattern
- All AI calls go through server-side API routes or Server Actions (keeps API keys secret).
- Streaming responses use Next.js streaming (React `Suspense` + `ReadableStream`).
- Structured outputs use a deterministic string format (`Title::id::type;;...`) with retry-on-failure.
- Prompts are modular per surface but share a common system prompt for persona consistency.

### 6.3 Catalog Integration Pattern
- Catalog data is fetched on-demand (no pre-loading or caching required per PRD §3).
- Transient data (cast, crew, seasons, videos, recommendations) is fetched per-request and not persisted.
- Persistent show data is merged on catalog refresh using timestamp-based conflict resolution.

### 6.4 Namespace & User Scoping
- Every database query includes `WHERE namespace_id = ? AND user_id = ?`.
- RLS policies enforce this at the database level as a safety net.
- Dev identity is injected via middleware, gated by `NODE_ENV`.
- Migration to real OAuth only requires replacing the identity injection mechanism.

### 6.5 Data Export Format
- JSON structure mirrors `StorageSnapshot` interface.
- All dates in ISO-8601 format.
- ZIP file contains a single `export.json` file.
- Import/restore is deferred (open question in PRD §10).

---

## 7. Risk & Mitigation

| Risk | Mitigation |
|---|---|
| AI output parsing failures | Retry with stricter instructions; fallback to unstructured + search handoff |
| Catalog API rate limits | Server-side caching of transient data within request lifecycle; graceful degradation |
| Supabase RLS misconfiguration | Test namespace isolation explicitly; use service role only in trusted server code |
| AI prompt drift across model versions | Golden set testing (discovery_quality_bar.md); prompt versioning |
| Merge conflicts in sync | Timestamp-per-field resolution; newer always wins |
| Large token usage for library context | Summarize library for AI prompts; limit to relevant subset (e.g., by genre/status) |

---

## 8. Build & Run Instructions

```bash
# 1. Copy and fill environment variables
cp .env.example .env.local

# 2. Install dependencies
npm install

# 3. Run database migrations
npx supabase db push  # or equivalent migration command

# 4. Start development server
npm run dev

# 5. Run tests
npm test

# 6. Reset test data for current namespace
npm run test:reset
```

---

## 9. Compliance Checklist

### Product PRD
- [x] Status system with Active, Later, Wait, Done, Quit (+ optional Next)
- [x] Interest levels (Interested/Excited) for Later status
- [x] Free-form tags with implicit tag library
- [x] Filters: All Shows, tag filters, data filters (genre, decade, score)
- [x] Media type toggle: All/Movies/TV
- [x] Ask: conversational AI with mentioned shows
- [x] Alchemy: multi-show concept blending with chaining
- [x] Explore Similar: per-show concept extraction → recommendations
- [x] AI Scoop: spoiler-safe, cached (4h), persisted only for collection items
- [x] Person Detail: bio, analytics, filmography
- [x] Auto-save triggers (status, interest, rating, tag)
- [x] Default values on save (Later/Interested; Done on rating)
- [x] Removal confirmation with "don't ask again"
- [x] User data precedence everywhere
- [x] Tile indicators (in-collection, user rating)
- [x] Timestamps on all my* fields
- [x] AI data persistence rules (Scoop persisted, others session-only)
- [x] AI recommendations map to real shows
- [x] Data export as ZIP/JSON
- [x] Settings: font size, search on launch, API keys, model selection

### Infrastructure Rider PRD
- [x] Next.js (latest stable) runtime
- [x] Supabase persistence via official client
- [x] `.env.example` with all variables
- [x] `.gitignore` excludes secrets
- [x] One-command dev/test/reset scripts
- [x] Database migrations for deterministic setup
- [x] `namespace_id` build isolation
- [x] `user_id` on all user-owned records
- [x] Dev identity injection (gated for production)
- [x] OAuth migration path without schema redesign
- [x] Server-side source of truth (disposable client cache)
- [x] Destructive testing without global teardown
- [x] Docker not required
- [x] No secrets committed to repo
