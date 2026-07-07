# Implementation Plan: TV & Movie Companion App

## Executive Summary

This plan covers the full implementation of a personal TV + movie companion app that enables users to collect, organize, rate, and discover entertainment through AI-powered discovery. The app is built on **Next.js** with **Supabase** persistence, following fractal architecture with humble components.

The plan is organized into 8 phases, progressing from foundational infrastructure through core data layer, UI shell, feature modules, AI surfaces, and polish.

---

## Phase 0: Project Scaffolding & Infrastructure

### 0.1 Next.js Project Setup

- Initialize Next.js project (latest stable) with TypeScript, App Router, and strict mode.
- Configure ESLint, Prettier, and TypeScript strict checks.
- Set up directory structure per fractal architecture:

```
src/
├── config/              # Global constants, env vars, feature flags
├── theme/               # Design tokens, color palette, typography, spacing
├── components/          # Shared UI primitives (Button, Card, Chip, Modal, etc.)
├── hooks/               # Global hooks (useAuth, useNamespace, useMediaQuery)
├── utils/               # Global pure functions (date formatting, merge helpers)
├── lib/
│   ├── supabase/        # Supabase client factories (browser + server)
│   ├── catalog/         # External catalog API client (TMDB or equivalent)
│   └── ai/              # AI provider client, prompt templates, parsers
├── types/               # Shared TypeScript types and interfaces
└── pages/               # Next.js App Router pages (app/ directory)
    ├── (main)/          # Authenticated layout group
    │   ├── page.tsx     # Collection Home
    │   ├── find/        # Find/Discover hub
    │   ├── show/[id]/   # Show Detail
    │   ├── person/[id]/ # Person Detail
    │   └── settings/    # Settings & Data
    └── layout.tsx       # Root layout with providers
```

### 0.2 Environment & Configuration

- Create `.env.example` with all required variables:

```env
# Supabase
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=  # Server-only, never exposed to browser

# External Catalog (e.g., TMDB)
NEXT_PUBLIC_CATALOG_API_KEY=

# AI Provider
AI_API_KEY=
AI_MODEL=
AI_PROVIDER=  # e.g., "openai", "anthropic"

# Benchmark / Dev
NAMESPACE_ID=
DEV_USER_ID=
NODE_ENV=
```

- `.gitignore` excludes `.env*` except `.env.example`.
- `src/config/env.ts` validates and exports typed environment access. Server-only keys (service role, AI keys) are gated behind server-side checks.

### 0.3 Supabase Schema & Migrations

Create migrations for the following tables:

#### `shows` table
| Column | Type | Notes |
|--------|------|-------|
| `id` | `text` PK | External catalog ID |
| `user_id` | `text` NOT NULL | Owner |
| `namespace_id` | `text` NOT NULL | Build isolation |
| `title` | `text` NOT NULL | |
| `show_type` | `text` NOT NULL | `movie`, `tv`, `person`, `unknown` |
| `external_ids` | `jsonb` | Optional external identifiers |
| `overview` | `text` | |
| `genres` | `text[]` | Genre names |
| `tagline` | `text` | |
| `homepage` | `text` | |
| `original_language` | `text` | |
| `spoken_languages` | `text[]` | ISO 639-1 codes |
| `languages` | `text[]` | |
| `poster_url` | `text` | |
| `backdrop_url` | `text` | |
| `logo_url` | `text` | |
| `network_logos` | `text[]` | |
| `vote_average` | `double precision` | |
| `vote_count` | `integer` | |
| `popularity` | `double precision` | |
| `last_air_date` | `timestamptz` | |
| `first_air_date` | `timestamptz` | |
| `release_date` | `timestamptz` | |
| `runtime` | `integer` | Movie |
| `budget` | `integer` | Movie |
| `revenue` | `integer` | Movie |
| `series_status` | `text` | TV |
| `number_of_episodes` | `integer` | TV |
| `number_of_seasons` | `integer` | TV |
| `episode_run_time` | `integer[]` | TV |
| `my_tags` | `text[]` | User tags |
| `my_tags_update_date` | `timestamptz` | |
| `my_score` | `double precision` | User rating |
| `my_score_update_date` | `timestamptz` | |
| `my_status` | `text` | `active`, `next`, `later`, `done`, `quit`, `wait` |
| `my_status_update_date` | `timestamptz` | |
| `my_interest` | `text` | `excited`, `interested` |
| `my_interest_update_date` | `timestamptz` | |
| `ai_scoop` | `text` | |
| `ai_scoop_update_date` | `timestamptz` | |
| `details_update_date` | `timestamptz` | |
| `creation_date` | `timestamptz` | |
| `is_test` | `boolean` DEFAULT false | |
| `provider_data` | `jsonb` | Provider IDs by region |
| `created_at` | `timestamptz` DEFAULT now() | |
| `updated_at` | `timestamptz` DEFAULT now() | |

Indexes: `(namespace_id, user_id)`, `(namespace_id, user_id, my_status)`, `(namespace_id, user_id, my_tags)`.

RLS policies: All queries scoped to `(namespace_id, user_id)`.

#### `cloud_settings` table
| Column | Type | Notes |
|--------|------|-------|
| `id` | `text` PK | Default `"globalSettings"` |
| `user_id` | `text` NOT NULL | |
| `namespace_id` | `text` NOT NULL | |
| `user_name` | `text` NOT NULL | Random name on first launch |
| `version` | `double precision` | Epoch seconds for conflict resolution |
| `catalog_api_key` | `text` | |
| `ai_api_key` | `text` | |
| `ai_model` | `text` NOT NULL | |
| `created_at` | `timestamptz` DEFAULT now() | |
| `updated_at` | `timestamptz` DEFAULT now() | |

Unique constraint: `(namespace_id, user_id)`.

#### `app_metadata` table
| Column | Type | Notes |
|--------|------|-------|
| `id` | `text` PK | |
| `namespace_id` | `text` NOT NULL | |
| `data_model_version` | `integer` DEFAULT 3 | |

### 0.4 Identity & Namespace System

- **Server-side middleware** (`src/lib/auth/middleware.ts`):
  - In dev/benchmark mode: reads `DEV_USER_ID` from env or accepts `X-User-Id` header.
  - `NAMESPACE_ID` from env or generated per build.
  - Both injected into request context accessible by all server actions and API routes.
  - Gated behind `NODE_ENV !== 'production'` for dev identity injection.
  - Designed so swapping to real OAuth later requires only auth wiring changes, not schema redesign.

- **`useIdentity()` hook** (client-side):
  - Provides `userId` and `namespaceId` to components.
  - In dev mode, may surface a user selector.

### 0.5 Scripts & Developer Experience

- `npm run dev` — Start Next.js dev server.
- `npm run build` — Production build.
- `npm test` — Run test suite (Vitest or Jest + Testing Library).
- `npm run test:reset` — Reset test data for current namespace (calls a server action that deletes all records where `namespace_id = NAMESPACE_ID` and `is_test = true`).
- `npm run db:migrate` — Apply Supabase migrations.
- `npm run db:seed` — Optional seed data for development.
- `npm run lint` — ESLint check.
- `npm run typecheck` — TypeScript type checking.

---

## Phase 1: Core Data Layer

### 1.1 Type Definitions (`src/types/`)

Define all domain types mirroring the storage schema:

- `Show`, `ShowType`, `MyStatusType`, `MyInterestType`
- `ProviderData`, `ProviderTypeIdLists`
- `CloudSettings`, `AppMetadata`
- `FilterType`, `FilterConfiguration`
- `LocalSettings`, `UserDefaultsUIState`
- `StorageSnapshot`

### 1.2 Supabase Client Layer (`src/lib/supabase/`)

- **`client.ts`** — Browser Supabase client (anon key only).
- **`server.ts`** — Server-side client (service role key, used in Server Actions and Route Handlers).
- **`middleware.ts`** — Supabase auth middleware for session refresh.

### 1.3 Data Access Layer (`src/lib/data/`)

Repository pattern with namespace + user scoping on every query:

#### `ShowRepository`
- `getCollection(namespaceId, userId, filters?)` — Fetch user's saved shows with optional filters.
- `getShow(namespaceId, userId, showId)` — Fetch single show.
- `upsertShow(namespaceId, userId, show)` — Insert or merge with merge rules.
- `deleteShow(namespaceId, userId, showId)` — Remove show and all My Data.
- `updateMyStatus(namespaceId, userId, showId, status, interest?)` — Status change with timestamp.
- `updateMyInterest(namespaceId, userId, showId, interest)` — Interest change with timestamp.
- `updateMyTags(namespaceId, userId, showId, tags)` — Tag change with timestamp.
- `updateMyScore(namespaceId, userId, showId, score)` — Rating change with timestamp.
- `updateAiScoop(namespaceId, userId, showId, scoop)` — Scoop cache with timestamp.
- `getAllTags(namespaceId, userId)` — Distinct tags across collection.
- `getByStatus(namespaceId, userId, status)` — Filtered by status.

#### `SettingsRepository`
- `getSettings(namespaceId, userId)` — Fetch cloud settings.
- `upsertSettings(namespaceId, userId, settings)` — Update with version-based conflict resolution.

#### `AppMetadataRepository`
- `getMetadata(namespaceId)` — Fetch current data model version.
- `setMetadata(namespaceId, version)` — Update after migration.

### 1.4 Merge Logic (`src/utils/merge.ts`)

Critical business logic for catalog refresh and sync:

- **`mergeShow(catalogShow, storedShow)`**:
  - Non-my fields: `selectFirstNonEmpty(newValue, oldValue)` — never overwrite non-empty with empty.
  - My fields: resolve by timestamp — newer wins. If only one side has a date, keep that side.
  - `detailsUpdateDate` set to now after merge.
  - `creationDate` preserved from stored show (never overwritten).

- **`mergeSettings(remote, local)`**:
  - Version-based: higher epoch wins.

### 1.5 Auto-Save Business Rules (`src/utils/autoSave.ts`)

Implement the saving trigger matrix:

| Trigger | Default Status | Default Interest | Notes |
|---------|---------------|-----------------|-------|
| Set any status | The chosen status | — | Explicit save |
| Choose Interested/Excited chip | `later` | `interested` or `excited` | Interest implies Later |
| Rate an unsaved show | `done` | — | Rating implies watched |
| Add tag to unsaved show | `later` | `interested` | Tag implies interest |

### 1.6 Filter System (`src/utils/filters.ts`)

Filter types and application logic:

- `all` — No filter.
- `genre` — Match show's genres array.
- `myStatus` — Match `myStatus` field.
- `communityScore` — Range filter on `voteAverage`.
- `decade` — Range filter on release/first air date.
- `myTag` — Match `myTags` array.
- `noTags` — Shows with empty `myTags`.

Media-type toggle (All/Movies/TV) applies on top of any filter.

### 1.7 External Catalog Client (`src/lib/catalog/`)

Abstract interface for the entertainment catalog API:

- `searchShows(query, options?)` — Text search.
- `getShowDetails(externalId, mediaType)` — Full show details.
- `getShowCredits(externalId, mediaType)` — Cast and crew.
- `getShowSeasons(externalId)` — TV seasons/episodes.
- `getShowVideos(externalId, mediaType)` — Trailers, clips.
- `getShowImages(externalId, mediaType)` — Backdrops, posters, logos.
- `getRecommendations(externalId, mediaType)` — Catalog recommendations.
- `getSimilar(externalId, mediaType)` — Similar shows.
- `getProviders(externalId, mediaType)` — Streaming availability.
- `getPersonDetails(personId)` — Person profile.
- `getPersonCredits(personId)` — Filmography.

Each method returns normalized data that maps to the `Show` type via `src/lib/catalog/mappers.ts`.

### 1.8 AI Provider Client (`src/lib/ai/`)

- **`client.ts`** — Provider-agnostic AI client supporting streaming responses.
- **`prompts/`** — Prompt templates per surface (see Phase 5).
- **`parsers/`** — Structured output parsers for mentions, concepts, recommendations.
- **`types.ts`** — AI request/response types.

---

## Phase 2: Shared UI Primitives & Theme

### 2.1 Theme System (`src/theme/`)

- **`tokens.ts`** — Design tokens: colors, spacing, typography scale, border radii, shadows, breakpoints.
- **`fontSize.ts`** — Font size scale (`XS` through `XXL`) mapped to CSS values, driven by user setting.
- **`mediaQueries.ts`** — Responsive breakpoint hooks.

### 2.2 Shared Components (`src/components/`)

All primitives are dumb, style-only components:

- **`ShowTile/`** — Poster card with title, collection badge, user rating badge. Used everywhere shows appear.
- **`ShowGrid/`** — Responsive poster grid layout.
- **`StatusChips/`** — Status/interest chip row (Active, Interested, Excited, Done, Quit, Wait).
- **`RatingSlider/`** — Interactive rating bar/slider.
- **`TagPicker/`** — Tag display + add/remove with autocomplete from existing tags.
- **`MediaCarousel/`** — Backdrop/poster/logo/video carousel for detail headers.
- **`ChipGroup/`** — Selectable chip group (for concepts, filters).
- **`ConfirmDialog/`** — Confirmation modal for destructive actions.
- **`EmptyState/`** — Configurable empty state with icon, title, CTA.
- **`LoadingSpinner/`** — Loading indicator.
- **`StreamingText/`** — Progressive text display for AI streaming responses.
- **`Sidebar/`** — Navigation/filter sidebar.
- **`Navigation/`** — Top-level nav with Find/Discover and Settings entry points.
- **`MediaTypeToggle/`** — All/Movies/TV toggle.

---

## Phase 3: App Shell & Navigation

### 3.1 Root Layout (`src/app/layout.tsx`)

- Theme provider, identity provider, settings provider.
- Font size applied globally from user settings.

### 3.2 Main Layout (`src/app/(main)/layout.tsx`)

- Sidebar with filter navigation.
- Top nav with Find/Discover and Settings entry points.
- Responsive: sidebar collapses on mobile.

### 3.3 Navigation Structure

```
/                          → Collection Home
/find                      → Find/Discover hub (Search/Ask/Alchemy mode switcher)
/find?mode=search          → Search mode
/find?mode=ask             → Ask mode
/find?mode=alchemy         → Alchemy mode
/show/[id]                 → Show Detail
/show/[id]?ask=true        → Show Detail with "Ask about this show" handoff
/person/[id]               → Person Detail
/settings                  → Settings & Data
```

---

## Phase 4: Collection Home

### 4.1 Page: Collection Home (`src/app/(main)/page.tsx`)

**Features:**

#### `CollectionHome/` (page-level feature)
- **`CollectionHome.tsx`** — Orchestrates status-grouped sections.
- **`hooks/useCollection.ts`** — Fetches shows from repository, applies active filter + media type toggle, groups by status.

#### `StatusSections/` (sub-feature)
Groups shows into ordered sections:
1. **Active** — `myStatus === 'active'` (larger tiles).
2. **Excited** — `myStatus === 'later' && myInterest === 'excited'`.
3. **Interested** — `myStatus === 'later' && myInterest === 'interested'`.
4. **Other** — Collapsed group containing Wait, Quit, Done, and unclassified Later items.

Each section: section header with count, `ShowGrid` of `ShowTile` items.

#### `FilterSidebar/` (sub-feature)
- **`FilterSidebar.tsx`** — Renders filter list.
- **`hooks/useFilters.ts`** — Manages filter state, persists `lastSelectedFilter` to local state.
- Filter items:
  - All Shows (default).
  - Tag filters: one per distinct tag, plus "No Tags" if applicable.
  - Data filters: genre (from collection), decade, community score ranges.
- Media type toggle at top: All / Movies / TV.

#### `CollectionEmptyState/` (sub-feature)
- No shows at all: prompt to Search or Ask.
- Filter yields none: "No results found."

### 4.2 Show Tile Behavior

- Displays poster, title.
- **In-collection indicator** when `myStatus` exists.
- **User rating indicator** when `myScore` exists.
- User's version of data always displayed (status, tags, rating).
- Click navigates to Show Detail.

---

## Phase 5: Find/Discover Hub

### 5.1 Page: Find (`src/app/(main)/find/page.tsx`)

**Features:**

#### `FindHub/` (page-level feature)
- **`FindHub.tsx`** — Mode switcher (Search / Ask / Alchemy) + active mode content.
- **`hooks/useFindMode.ts`** — URL-driven mode state.

### 5.2 Search Mode (`features/SearchMode/`)

- **`SearchMode.tsx`** — Search input + results grid.
- **`hooks/useSearch.ts`** — Debounced text search against external catalog.
- Results displayed as `ShowGrid` with `ShowTile` items.
- In-collection items marked with badge.
- Click opens Show Detail.
- Supports "Search on Launch" auto-open from settings.

### 5.3 Ask Mode (`features/AskMode/`)

- **`AskMode.tsx`** — Chat UI with user/assistant turns.
- **`hooks/useAskChat.ts`** — Manages conversation state, sends messages to AI, handles streaming.
- **`hooks/useConversationSummary.ts`** — Summarizes older turns after ~10 messages.

**Chat UI structure:**
- Welcome view: 6 random starter prompts (from a pool of 80), refresh button.
- Message list: user turns + assistant turns with `StreamingText`.
- Input bar at bottom.
- **Mentioned Shows strip**: horizontal row of shows mentioned by AI, parsed from structured output.

**AI Contract (Ask with Mentions):**
- AI outputs structured response:
  ```json
  {
    "commentary": "user-facing text",
    "showList": "Title::externalId::mediaType;;Title2::externalId::mediaType"
  }
  ```
- Parser in `src/lib/ai/parsers/askParser.ts` extracts `commentary` and `showList`.
- `showList` parsed into `Show` references; each resolved against catalog.
- Resolved shows rendered in mentioned shows strip; unresolved shown as non-interactive text.

**Variants:**
- **General Ask**: started from Find hub.
- **Ask About a Show**: launched from Show Detail with `?ask=true&showId=X`. Seeds conversation with show context.

**Conversation Context:**
- Includes user's library (saved shows + My Data) for taste-aware responses.
- Recent turns included directly; older turns summarized.
- Summary preserves persona/tone (not sterile).

### 5.4 Alchemy Mode (`features/AlchemyMode/`)

- **`AlchemyMode.tsx`** — Multi-step wizard UI.
- **`hooks/useAlchemy.ts`** — Manages Alchemy session state.

**Step flow:**

1. **Select Shows** (`features/AlchemyShowSelector/`)
   - Search + library picker. Minimum 2 shows.
   - Selected shows displayed as chips/cards.

2. **Conceptualize** (`features/AlchemyConcepts/`)
   - "Conceptualize Shows" button triggers AI concept extraction.
   - AI receives all selected shows, returns shared concepts.
   - Concepts displayed as selectable chips (max 8).
   - Selecting/unselecting clears downstream results.

3. **Alchemize** (`features/AlchemyResults/`)
   - "ALCHEMIZE!" button triggers AI recommendation generation.
   - AI receives selected concepts + input shows + user library.
   - Returns 6 recommendations with reasons.
   - Each recommendation resolved to real catalog item.
   - "More Alchemy!" button chains another round (results become new inputs).

**Backtracking:** Changing shows clears concepts and results. Changing concepts clears results.

**Session-scoped:** All Alchemy data cleared when leaving the mode.

---

## Phase 6: Show Detail Page

### 6.1 Page: Show Detail (`src/app/(main)/show/[id]/page.tsx`)

**Features:**

#### `ShowDetail/` (page-level feature)
- **`ShowDetail.tsx`** — Orchestrates all sections in narrative hierarchy order.
- **`hooks/useShowDetail.ts`** — Fetches show from collection (if saved) + catalog details (transient data: cast, crew, seasons, videos, recommendations, similar). Merges using merge rules.

### 6.2 Section Features (in narrative order):

#### `HeaderMedia/` (sub-feature)
- Carousel of backdrops, posters, logos.
- Video playback when trailers available (inline, non-blocking).
- Graceful fallback to poster-only when no backdrops/videos.

#### `CoreFacts/` (sub-feature)
- Year, runtime (movies) or seasons/episodes (TV).
- Community score bar.

#### `MyRelationship/` (sub-feature)
- **`MyRelationship.tsx`** — Status chips + rating + tags.
- **`hooks/useMyRelationship.ts`** — Handles auto-save logic:
  - Status chip click → save with chosen status.
  - Interested/Excited chip → save with `later` + interest.
  - Reselect active status → show `ConfirmDialog` → remove from collection (clears all My Data).
  - Rating change on unsaved → auto-save as `done`.
  - Tag add on unsaved → auto-save as `later` + `interested`.
  - `hideStatusRemovalConfirmation` respected; counter tracked.

#### `OverviewSection/` (sub-feature)
- Overview text.
- Scoop toggle (see 6.3).

#### `ScoopSection/` (sub-feature)
- **`ScoopSection.tsx`** — Toggle + streaming Scoop display.
- **`hooks/useScoop.ts`** — Manages Scoop generation and caching.
- Toggle states:
  - No scoop cached: "Give me the scoop!"
  - Cached but < 4 hours old: "Show the scoop"
  - Cached and expired: "Give me the scoop!" (regenerates)
  - Open: "The Scoop" title displayed.
- Streams progressively via `StreamingText`.
- Persisted only if show is in collection.
- AI Scoop contract: mini blog post with personal take, honest stack-up, Scoop centerpiece, fit/warnings, verdict. ~150-350 words.

#### `AskAboutShow/` (sub-feature)
- "Ask about this show" CTA button.
- Navigates to Find hub in Ask mode with show context seeded.

#### `GenresLanguages/` (sub-feature)
- Genre chips + language list.

#### `RecommendationsStrand/` (sub-feature)
- Horizontal scrollable row of catalog recommendations + similar shows.
- Each item is a `ShowTile`; click navigates to Show Detail.

#### `ExploreSimilar/` (sub-feature)
- **`ExploreSimilar.tsx`** — Three-step flow within the detail page.
- **`hooks/useExploreSimilar.ts`** — Manages concept generation and recommendation state.
- Steps:
  1. "Get Concepts" button → AI generates concepts for this single show.
  2. Concepts displayed as selectable chips (1+ selection).
  3. "Explore Shows" button → AI generates 5 recommendations based on selected concepts.
- Recommendations displayed as horizontal strand with reasons.
- Copy hints: "pick the ingredients you want more of."

#### `StreamingProviders/` (sub-feature)
- "Stream It" section showing availability by region.
- Provider logos/names for flatrate, rent, buy.

#### `CastCrew/` (sub-feature)
- Horizontal scrollable strands for cast and crew.
- Each person card: photo, name, character/role.
- Click navigates to Person Detail.

#### `SeasonsSection/` (sub-feature, TV only)
- Season list with episode counts.
- Only rendered when `showType === 'tv'`.

#### `BudgetRevenue/` (sub-feature, movies only)
- Budget vs Revenue display when data available.
- Only rendered for movies with non-null budget/revenue.

---

## Phase 7: Person Detail Page

### 7.1 Page: Person Detail (`src/app/(main)/person/[id]/page.tsx`)

**Features:**

#### `PersonDetail/` (page-level feature)
- **`PersonDetail.tsx`** — Orchestrates person sections.
- **`hooks/usePersonDetail.ts`** — Fetches person profile + filmography from catalog.

#### `PersonHeader/` (sub-feature)
- Image gallery, name, bio.

#### `PersonAnalytics/` (sub-feature)
- Lightweight charts:
  - Average project ratings over time.
  - Top genres distribution.
  - Projects by year.
- Chart library: lightweight charting (e.g., Recharts or similar).

#### `Filmography/` (sub-feature)
- Credits grouped by year.
- Each credit is a `ShowTile`; click navigates to Show Detail.

---

## Phase 8: Settings & Data Management

### 8.1 Page: Settings (`src/app/(main)/settings/page.tsx`)

**Features:**

#### `SettingsPage/` (page-level feature)

#### `AppSettings/` (sub-feature)
- Font size selector (XS through XXL).
- Search on launch toggle.
- Both persisted to local settings.

#### `UserSettings/` (sub-feature)
- Username display/edit.
- Synced via `CloudSettings`.

#### `AISettings/` (sub-feature)
- AI provider API key input (masked).
- AI model selector.
- In benchmark mode: may be provided via env vars. User-entered keys stored in `CloudSettings` but never committed to repo.

#### `IntegrationSettings/` (sub-feature)
- Content catalog provider API key input.
- Stored in `CloudSettings`.

#### `DataExport/` (sub-feature)
- **`DataExport.tsx`** — "Export My Data" button.
- **`hooks/useDataExport.ts`** — Server action that:
  1. Fetches all shows for `(namespace_id, user_id)`.
  2. Serializes to JSON with ISO-8601 dates.
  3. Packages into `.zip` file.
  4. Returns download stream to client.

#### `DataImport/` (sub-feature, future)
- UI placeholder for Import/Restore from export zip.
- Noted as open question; not implemented in v1.

---

## Phase 9: AI Surface Implementation

### 9.1 Prompt Templates (`src/lib/ai/prompts/`)

All prompts enforce shared rules:
- Stay within TV/movies domain.
- Spoiler-safe by default.
- Opinionated and honest.
- Specific, vibe/structure/craft-based reasoning.

#### `scoopPrompt.ts`
- Input: show data + user library context.
- Output: structured Scoop with sections (personal take, stack-up, centerpiece, fit/warnings, verdict).
- Tone: gossipy, vivid, useful. ~150-350 words.

#### `askPrompt.ts`
- Input: user library + conversation history + current message.
- Output: structured `{ commentary, showList }` with `Title::externalId::mediaType;;...` format.
- Tone: friendly dialogue, not essay. Confident picks.

#### `askAboutShowPrompt.ts`
- Input: specific show context + user library + conversation.
- Output: same structured format as Ask.
- Seeds conversation with show details.

#### `conceptPrompt.ts`
- **Single-show variant**: Input is one show. Returns 8 concepts.
- **Multi-show variant (Alchemy)**: Input is 2+ shows. Returns shared concepts across all inputs. Larger pool than single-show.
- Output: bullet list, 1-3 words each, evocative, no explanation, no plot.
- Quality: specific over generic, diverse across axes, ordered by strength.

#### `recommendationPrompt.ts`
- **Explore Similar variant**: Input is selected concepts + single show + library. Returns 5 recs.
- **Alchemy variant**: Input is selected concepts + multiple shows + library. Returns 6 recs.
- Output: list of `{ title, externalId, mediaType, reason }`.
- Reasons explicitly reference selected concepts.
- Bias toward recent but allow classics/hidden gems.

#### `summarizeConversationPrompt.ts`
- Input: older conversation turns.
- Output: 1-2 sentence summary preserving persona/tone.

### 9.2 AI Response Parsers (`src/lib/ai/parsers/`)

#### `askParser.ts`
- Parses structured Ask response.
- Extracts `commentary` (display text) and `showList` (machine-readable).
- Splits `showList` by `;;`, then each entry by `::` to get `[title, externalId, mediaType]`.
- Handles parse failures: retry with stricter formatting, then fallback to unstructured + Search handoff.

#### `conceptParser.ts`
- Parses bullet list into array of concept strings.
- Validates: 1-3 words, no generic concepts flagged.

#### `recommendationParser.ts`
- Parses recommendation list.
- Each rec: title + externalId + mediaType + reason.
- Validates externalId presence for catalog resolution.

### 9.3 Catalog Resolution (`src/lib/ai/resolution.ts`)

When AI returns recommendations:
1. AI outputs `title + externalId + mediaType`.
2. System looks up external catalog by `externalId`.
3. Accepts first result whose title matches case-insensitively.
4. If found: recommendation becomes real selectable `Show` with AI reason as transient text.
5. If not found: title shown as non-interactive or handed off to Search.

### 9.4 Conversation Summarization

- After ~10 messages in Ask, older turns are summarized.
- Summary replaces older turns in context sent to AI.
- Summary preserves persona (not sterile "system summary").
- Triggered automatically by `useAskChat` hook.

---

## Phase 10: Cross-Cutting Concerns

### 10.1 Data Consistency Rules

**User's version takes precedence everywhere:**
- When displaying a show anywhere (lists, search, recommendations, AI outputs), if the user has saved data, display the user-overlaid version.
- User edits always win over refreshed public data.

**Timestamp tracking on every user field:**
- `myStatusUpdateDate`, `myInterestUpdateDate`, `myTagsUpdateDate`, `myScoreUpdateDate`, `aiScoopUpdateDate`.
- Used for sorting, conflict resolution, and cache freshness.

### 10.2 Namespace Isolation

- Every database query includes `WHERE namespace_id = $1`.
- Destructive test operations scoped to namespace.
- Two namespaces never read/write each other's data.
- `test:reset` script deletes all records for current namespace where `is_test = true`.

### 10.3 Error Handling

- Network failures: graceful degradation, retry with backoff.
- AI failures: retry once with stricter formatting, then fallback.
- Catalog API failures: show error state, allow retry.
- Database errors: surface to user with actionable message.

### 10.4 Performance

- Server-side rendering for initial page loads.
- Client-side caching for catalog data (disposable, re-fetchable).
- Debounced search input (300ms).
- Lazy loading for below-fold detail sections.
- Image optimization via Next.js `Image` component.

### 10.5 Testing Strategy

- **Unit tests** for:
  - Merge logic (`mergeShow`, `mergeSettings`).
  - Auto-save business rules.
  - Filter application logic.
  - AI parsers (ask, concept, recommendation).
  - Catalog mappers.
- **Integration tests** for:
  - Data access layer (with Supabase test instance).
  - Server actions.
- **Component tests** for:
  - Status chips interaction.
  - Rating slider auto-save.
  - Tag picker.
  - Filter sidebar.
- **E2E tests** (optional, Playwright):
  - Core user journeys (build collection, rate-to-save, tag-to-save, Ask discovery, Alchemy flow).

### 10.6 Data Migration & Continuity

- `AppMetadata.dataModelVersion` tracks schema version.
- On app startup, check version and run any pending migrations.
- Migrations are additive (add columns, add tables) — never destructive without data export.
- Users never lose collection, ratings, tags, statuses, interest levels, or AI Scoop due to updates.

---

## Phase 11: Polish & Integration

### 11.1 Empty States

- Collection Home (no shows): "Start building your collection" with Search/Ask CTAs.
- Filter yields none: "No results found."
- Search no results: "No shows found for [query]."
- Ask welcome: 6 random starter prompts with refresh.
- Alchemy step 1: "Select at least 2 shows to begin."
- Explore Similar no concepts: "Get Concepts" CTA only.

### 11.2 Confirmation Dialogs

- Status removal: "Remove [show] from your collection? This will clear all your data for this show."
  - Option to suppress after repeated removals (`hideStatusRemovalConfirmation`).
  - Counter tracked (`statusRemovalCountKey`).

### 11.3 Responsive Design

- Mobile: sidebar collapses to hamburger menu, single-column layouts.
- Tablet: sidebar visible, 2-3 column grids.
- Desktop: full sidebar, 4-6 column grids.
- Active shows get larger tiles on all breakpoints.

### 11.4 Accessibility

- Semantic HTML throughout.
- ARIA labels on interactive elements.
- Keyboard navigation for chip groups, grids, carousels.
- Focus management for modals and dialogs.
- Color contrast compliance via theme tokens.

---

## Dependency Graph & Build Order

```
Phase 0: Scaffolding
  ├── 0.1 Next.js setup
  ├── 0.2 Environment config
  ├── 0.3 Supabase schema + migrations
  ├── 0.4 Identity/namespace system
  └── 0.5 Scripts

Phase 1: Core Data Layer (depends on Phase 0)
  ├── 1.1 Type definitions
  ├── 1.2 Supabase clients
  ├── 1.3 Data access layer
  ├── 1.4 Merge logic
  ├── 1.5 Auto-save rules
  ├── 1.6 Filter system
  ├── 1.7 Catalog client
  └── 1.8 AI client

Phase 2: UI Primitives (depends on Phase 0, parallel with Phase 1)
  ├── 2.1 Theme system
  └── 2.2 Shared components

Phase 3: App Shell (depends on Phase 2)
  ├── 3.1 Root layout
  ├── 3.2 Main layout
  └── 3.3 Navigation

Phase 4: Collection Home (depends on Phase 1, 3)
Phase 5: Find/Discover (depends on Phase 1, 3)
Phase 6: Show Detail (depends on Phase 1, 3)
Phase 7: Person Detail (depends on Phase 1, 3)
Phase 8: Settings (depends on Phase 1, 3)

Phase 9: AI Surfaces (depends on Phase 1.8, integrated into Phases 5-6)
Phase 10: Cross-Cutting (ongoing throughout)
Phase 11: Polish (depends on all above)
```

Phases 4-8 can proceed in parallel once Phases 1-3 are complete. Phase 9 is integrated into the features that use AI (Ask, Alchemy, Explore Similar, Scoop).

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| AI structured output parsing failures | Retry with stricter prompts, fallback to unstructured + Search handoff |
| Catalog API rate limits | Client-side caching, request deduplication, graceful degradation |
| Supabase RLS misconfiguration | Comprehensive RLS tests, namespace+user on every query |
| Merge logic data loss | Extensive unit tests covering all merge scenarios |
| AI personality drift | Prompt templates with strict voice pillars, golden set validation |
| Schema migration failures | Version-tracked migrations, additive-only changes, rollback support |

---

## Open Items (from PRD)

These are acknowledged but deferred:

1. **Next status** as first-class UI status — data model supports it, UI does not surface it.
2. **Named custom lists** beyond tags — not in v1 scope.
3. **AI Scoop on unsaved show** auto-save behavior — currently Scoop only persists if in collection.
4. **Unrated state** vs nil — currently nil means unrated.
5. **Import/Restore** from export zip — UI placeholder only, not implemented.
6. **Alchemy session saving/sharing** — not in v1 scope.
7. **myStatus filters in sidebar** — model supports it, not surfaced in v1.

---

## Summary

This plan produces a fully functional TV & movie companion app with:

- **Persistent collection** with status, interest, tags, ratings, and AI Scoop.
- **Three discovery modes**: Search, Ask (conversational AI), and Alchemy (concept blending).
- **Per-show discovery** via Explore Similar with concept selection.
- **AI personality** consistent across all surfaces (Scoop, Ask, Alchemy, Explore Similar).
- **Show Detail** as the single source of truth with full narrative hierarchy.
- **Person Detail** with analytics and filmography.
- **Settings** with data export, font size, and API key management.
- **Benchmark-compliant** infrastructure: namespace isolation, user identity on all records, Supabase persistence, no Docker requirement, OAuth-ready schema.
