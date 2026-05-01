# Implementation Plan

## 1. Architecture Overview

### Tech Stack (mandated by Infra Rider)

- **Framework:** Next.js (latest stable) — App Router with React Server Components where beneficial
- **Persistence:** Supabase (hosted preferred, local optional) — Postgres + Row Level Security + Realtime
- **External catalog:** TMDB API (movies + TV) — the PRD is provider-agnostic but TMDB is the standard fit for the described feature set
- **AI provider:** OpenAI-compatible API (configurable model) — used for Ask, Scoop, Concepts, Alchemy, Explore Similar
- **Styling:** Tailwind CSS + shadcn/ui components — fast iteration, accessible defaults
- **State management:** React Server Components for data fetching; lightweight client state (React context or Zustand) for transient UI state (chat sessions, alchemy sessions, filter selections)

### High-Level System Diagram

```
┌──────────────────────────────────────────────────┐
│                    Next.js App                    │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────┐ │
│  │  Pages /     │  │  API Routes  │  │  Server  │ │
│  │  Components  │  │  /api/*      │  │  Actions │ │
│  └──────┬──────┘  └──────┬───────┘  └────┬────┘ │
│         │                │               │       │
│         └────────────┬───┴───────────────┘       │
│                      │                           │
│              ┌───────▼────────┐                  │
│              │  Service Layer │                  │
│              └───┬───────┬───┘                  │
│                  │       │                       │
│          ┌───────▼──┐ ┌──▼────────┐              │
│          │ Supabase │ │ TMDB API  │              │
│          │ Client   │ │ Client    │              │
│          └──────────┘ └───────────┘              │
│                  │                               │
│          ┌───────▼────────┐                      │
│          │  AI Service    │                      │
│          │  (OpenAI etc.) │                      │
│          └────────────────┘                      │
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│                   Supabase                        │
│  ┌────────────┐ ┌──────────┐ ┌────────────────┐ │
│  │  shows     │ │ settings │ │ app_metadata   │ │
│  │  (user +   │ │ (cloud)  │ │ (migrations)   │ │
│  │  catalog)  │ └──────────┘ └────────────────┘ │
│  └────────────┘                                  │
│  RLS policies partition by namespace + user_id   │
└──────────────────────────────────────────────────┘
```

### Key Architectural Decisions

1. **Server-side AI calls only.** AI API keys never reach the browser. All AI interactions go through Next.js API routes/server actions.
2. **Supabase anon key on client; service role key server-only.** Enforced by environment variable scoping (`NEXT_PUBLIC_` prefix rules).
3. **Namespace + user_id partition.** Every user-owned row includes `namespace_id` and `user_id`. Supabase RLS policies enforce isolation.
4. **Catalog data is ephemeral, user data is durable.** TMDB responses are fetched on demand and merged into stored shows. Transient fields (cast, crew, seasons, videos, recommendations, similar, images) are never persisted.
5. **AI sessions are client-side ephemeral state.** Ask chat history, Alchemy session state, and mentioned-shows strips live in React state and are discarded on navigation/reset.

---

## 2. Directory Structure

```
/
├── .env.example                    # All required env vars with comments
├── .gitignore                      # Excludes .env*, node_modules, .next
├── next.config.ts
├── package.json
├── tsconfig.json
├── tailwind.config.ts
│
├── supabase/
│   └── migrations/
│       ├── 001_create_shows.sql
│       ├── 002_create_settings.sql
│       ├── 003_create_app_metadata.sql
│       └── 004_rls_policies.sql
│
├── src/
│   ├── app/                        # Next.js App Router
│   │   ├── layout.tsx              # Root layout (nav, filters sidebar)
│   │   ├── page.tsx                # Collection Home
│   │   ├── find/
│   │   │   ├── layout.tsx          # Find/Discover layout with mode switcher
│   │   │   ├── search/page.tsx     # Search mode
│   │   │   ├── ask/page.tsx        # Ask mode
│   │   │   └── alchemy/page.tsx    # Alchemy mode
│   │   ├── show/[id]/page.tsx      # Show Detail
│   │   ├── person/[id]/page.tsx    # Person Detail
│   │   ├── settings/page.tsx       # Settings & Your Data
│   │   └── api/
│   │       ├── ai/
│   │       │   ├── ask/route.ts        # Ask chat endpoint (streaming)
│   │       │   ├── scoop/route.ts      # Scoop generation (streaming)
│   │       │   ├── concepts/route.ts   # Concept extraction
│   │       │   ├── recommend/route.ts  # Concept-based recommendations
│   │       │   └── summarize/route.ts  # Conversation summarization
│   │       ├── shows/
│   │       │   ├── route.ts            # CRUD for user's show collection
│   │       │   ├── [id]/route.ts       # Single show operations
│   │       │   └── export/route.ts     # Export/backup endpoint
│   │       ├── catalog/
│   │       │   ├── search/route.ts     # TMDB search proxy
│   │       │   ├── show/[id]/route.ts  # TMDB show detail proxy
│   │       │   ├── person/[id]/route.ts # TMDB person detail proxy
│   │       │   └── trending/route.ts   # TMDB trending proxy
│   │       └── settings/route.ts       # CloudSettings CRUD
│   │
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Sidebar.tsx             # Filters/navigation panel
│   │   │   ├── TopNav.tsx              # Global nav bar
│   │   │   └── MediaTypeToggle.tsx     # All / Movies / TV toggle
│   │   ├── collection/
│   │   │   ├── StatusSection.tsx       # Status-grouped show section
│   │   │   ├── ShowTile.tsx            # Poster tile with badges
│   │   │   └── EmptyState.tsx          # Empty collection prompts
│   │   ├── detail/
│   │   │   ├── HeaderMedia.tsx         # Backdrop/poster/logo/trailer carousel
│   │   │   ├── CoreFacts.tsx           # Year, runtime, community score
│   │   │   ├── StatusToolbar.tsx       # Status/interest chip bar
│   │   │   ├── RatingBar.tsx           # User rating slider
│   │   │   ├── TagPicker.tsx           # Tag display + add/remove
│   │   │   ├── Overview.tsx            # Overview text
│   │   │   ├── ScoopSection.tsx        # AI Scoop toggle + streaming display
│   │   │   ├── RecommendationsStrand.tsx  # Traditional similar/recommended
│   │   │   ├── ExploreSimilar.tsx      # Concept chips + AI recs
│   │   │   ├── StreamingProviders.tsx  # Where to watch
│   │   │   ├── CastCrewStrand.tsx      # Horizontal cast/crew
│   │   │   ├── SeasonsSection.tsx      # TV seasons
│   │   │   └── BudgetRevenue.tsx       # Movie financials
│   │   ├── person/
│   │   │   ├── PersonHeader.tsx        # Image gallery, bio
│   │   │   ├── PersonAnalytics.tsx     # Charts (ratings, genres, timeline)
│   │   │   └── Filmography.tsx         # Credits grouped by year
│   │   ├── find/
│   │   │   ├── ModeSwitcher.tsx        # Search / Ask / Alchemy tab bar
│   │   │   ├── SearchResults.tsx       # Poster grid with collection badges
│   │   │   ├── ChatInterface.tsx       # Ask chat UI
│   │   │   ├── MentionedShowsStrip.tsx # Horizontal mentioned shows
│   │   │   ├── StarterPrompts.tsx      # 6 random starter prompts
│   │   │   ├── AlchemyFlow.tsx         # Multi-step alchemy UI
│   │   │   ├── ShowPicker.tsx          # Show selector for Alchemy input
│   │   │   └── ConceptChips.tsx        # Selectable concept chip display
│   │   ├── settings/
│   │   │   ├── SettingsForm.tsx        # All settings controls
│   │   │   └── ExportButton.tsx        # Export My Data
│   │   └── shared/
│   │       ├── ShowGrid.tsx            # Reusable poster grid
│   │       ├── ConfirmDialog.tsx       # Confirmation modal
│   │       └── LoadingStates.tsx       # Skeleton/spinner components
│   │
│   ├── lib/
│   │   ├── supabase/
│   │   │   ├── client.ts              # Browser Supabase client (anon key)
│   │   │   ├── server.ts              # Server Supabase client (service role)
│   │   │   └── types.ts               # Generated DB types
│   │   ├── catalog/
│   │   │   ├── tmdb-client.ts         # TMDB API wrapper
│   │   │   ├── mapper.ts              # TMDB response → Show mapping
│   │   │   └── genre-map.ts           # Genre ID → name lookup
│   │   ├── ai/
│   │   │   ├── client.ts              # AI provider client (server-only)
│   │   │   ├── prompts.ts             # All prompt templates
│   │   │   ├── ask-parser.ts          # Parse structured Ask responses (showList)
│   │   │   └── streaming.ts           # SSE streaming helpers
│   │   ├── shows/
│   │   │   ├── service.ts             # Show CRUD + merge logic
│   │   │   ├── merge.ts              # selectFirstNonEmpty + timestamp merge
│   │   │   ├── defaults.ts           # Default status/interest on save
│   │   │   └── export.ts             # Backup ZIP generation
│   │   ├── identity/
│   │   │   ├── middleware.ts          # Extract user_id + namespace_id
│   │   │   └── dev-auth.ts           # Dev identity injection (X-User-Id header / selector)
│   │   ├── filters/
│   │   │   └── filter-logic.ts        # Filter application logic
│   │   └── utils.ts                   # Date parsing, ISO-8601 helpers
│   │
│   ├── hooks/
│   │   ├── useCollection.ts           # Fetch/mutate user collection
│   │   ├── useAskChat.ts             # Ask session state management
│   │   ├── useAlchemy.ts             # Alchemy session state management
│   │   ├── useExploreSimilar.ts      # Explore Similar state
│   │   └── useFilters.ts             # Active filter state
│   │
│   ├── types/
│   │   ├── show.ts                   # Show, MyStatusType, MyInterestType, etc.
│   │   ├── ai.ts                     # AI request/response types
│   │   ├── catalog.ts                # TMDB response types
│   │   └── filters.ts                # FilterConfiguration, FilterType
│   │
│   └── middleware.ts                 # Next.js middleware: inject identity headers
│
├── scripts/
│   ├── dev.sh                        # Start app
│   ├── test.sh                       # Run tests
│   └── test-reset.sh                 # Reset test data for a namespace
│
└── __tests__/
    ├── unit/
    │   ├── merge.test.ts
    │   ├── defaults.test.ts
    │   ├── ask-parser.test.ts
    │   └── filter-logic.test.ts
    ├── integration/
    │   ├── shows-api.test.ts
    │   ├── ai-api.test.ts
    │   └── catalog-api.test.ts
    └── e2e/
        ├── collection-home.test.ts
        ├── search-and-save.test.ts
        ├── ask-chat.test.ts
        └── alchemy-flow.test.ts
```

---

## 3. Database Schema & Migrations

### Migration 001: `shows` table

```sql
CREATE TABLE shows (
  -- Identity
  id              TEXT        NOT NULL,
  namespace_id    TEXT        NOT NULL,
  user_id         TEXT        NOT NULL,
  title           TEXT        NOT NULL,
  show_type       TEXT        NOT NULL CHECK (show_type IN ('movie', 'tv', 'person', 'unknown')),
  external_ids    JSONB,

  -- Catalog meta
  overview        TEXT,
  genres          TEXT[]      NOT NULL DEFAULT '{}',
  tagline         TEXT,
  homepage        TEXT,
  original_language TEXT,
  spoken_languages TEXT[]     NOT NULL DEFAULT '{}',
  languages       TEXT[]      NOT NULL DEFAULT '{}',

  -- Images
  poster_url      TEXT,
  backdrop_url    TEXT,
  logo_url        TEXT,
  network_logos   TEXT[]      NOT NULL DEFAULT '{}',

  -- Ratings / popularity
  vote_average    DOUBLE PRECISION,
  vote_count      INTEGER,
  popularity      DOUBLE PRECISION,

  -- Dates
  last_air_date   TIMESTAMPTZ,
  first_air_date  TIMESTAMPTZ,
  release_date    TIMESTAMPTZ,

  -- Movie-specific
  runtime         INTEGER,
  budget          INTEGER,
  revenue         INTEGER,

  -- TV-specific
  series_status       TEXT,
  number_of_episodes  INTEGER,
  number_of_seasons   INTEGER,
  episode_run_time    INTEGER[] NOT NULL DEFAULT '{}',
  last_episode_run_time INTEGER,

  -- User data ("my*")
  my_tags             TEXT[]    NOT NULL DEFAULT '{}',
  my_tags_update_date TIMESTAMPTZ,
  my_score            DOUBLE PRECISION,
  my_score_update_date TIMESTAMPTZ,
  my_status           TEXT CHECK (my_status IN ('active', 'next', 'later', 'done', 'quit', 'wait')),
  my_status_update_date TIMESTAMPTZ,
  my_interest         TEXT CHECK (my_interest IN ('excited', 'interested')),
  my_interest_update_date TIMESTAMPTZ,

  -- AI data
  ai_scoop            TEXT,
  ai_scoop_update_date TIMESTAMPTZ,

  -- Management
  details_update_date TIMESTAMPTZ,
  creation_date       TIMESTAMPTZ DEFAULT NOW(),
  is_test             BOOLEAN     NOT NULL DEFAULT FALSE,

  -- Providers
  provider_data       JSONB,

  -- Composite primary key
  PRIMARY KEY (namespace_id, user_id, id)
);

-- Indexes for collection queries
CREATE INDEX idx_shows_user_collection
  ON shows (namespace_id, user_id, my_status)
  WHERE my_status IS NOT NULL;

CREATE INDEX idx_shows_user_tags
  ON shows USING GIN (my_tags)
  WHERE my_status IS NOT NULL;

CREATE INDEX idx_shows_genres
  ON shows USING GIN (genres);

CREATE INDEX idx_shows_test
  ON shows (namespace_id, is_test)
  WHERE is_test = TRUE;
```

### Migration 002: `cloud_settings` table

```sql
CREATE TABLE cloud_settings (
  id              TEXT        NOT NULL DEFAULT 'globalSettings',
  namespace_id    TEXT        NOT NULL,
  user_id         TEXT        NOT NULL,
  user_name       TEXT        NOT NULL,
  version         DOUBLE PRECISION NOT NULL DEFAULT 0,
  catalog_api_key TEXT,
  ai_api_key      TEXT,
  ai_model        TEXT        NOT NULL DEFAULT 'gpt-4o',

  PRIMARY KEY (namespace_id, user_id, id)
);
```

### Migration 003: `app_metadata` table

```sql
CREATE TABLE app_metadata (
  namespace_id        TEXT    NOT NULL,
  data_model_version  INTEGER NOT NULL DEFAULT 3,

  PRIMARY KEY (namespace_id)
);
```

### Migration 004: Row Level Security

```sql
ALTER TABLE shows ENABLE ROW LEVEL SECURITY;
ALTER TABLE cloud_settings ENABLE ROW LEVEL SECURITY;
ALTER TABLE app_metadata ENABLE ROW LEVEL SECURITY;

-- Shows: users can only access their own data within their namespace
CREATE POLICY shows_isolation ON shows
  USING (
    namespace_id = current_setting('app.namespace_id', TRUE)
    AND user_id = current_setting('app.user_id', TRUE)
  );

-- Settings: same isolation
CREATE POLICY settings_isolation ON cloud_settings
  USING (
    namespace_id = current_setting('app.namespace_id', TRUE)
    AND user_id = current_setting('app.user_id', TRUE)
  );

-- Metadata: namespace-level access
CREATE POLICY metadata_isolation ON app_metadata
  USING (
    namespace_id = current_setting('app.namespace_id', TRUE)
  );
```

---

## 4. Environment Variables

### `.env.example`

```bash
# === Supabase ===
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key          # Public/anon key (safe for browser)
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key       # Server-only; never expose to client

# === External Catalog (TMDB) ===
TMDB_API_KEY=your-tmdb-api-key                        # Server-only
TMDB_BASE_URL=https://api.themoviedb.org/3            # Override for testing

# === AI Provider ===
AI_API_KEY=your-openai-api-key                        # Server-only; overridable per-user via settings
AI_MODEL=gpt-4o                                       # Default model; overridable per-user via settings
AI_BASE_URL=https://api.openai.com/v1                 # Override for alternative providers

# === Identity & Isolation ===
NAMESPACE_ID=default                                  # Unique per build/run; partitions all data
DEFAULT_USER_ID=dev-user-001                          # Dev-mode default user
NODE_ENV=development                                  # 'development' enables dev identity injection
```

---

## 5. Identity & Isolation Implementation

### Namespace Injection

- `NAMESPACE_ID` env var is read server-side and attached to every Supabase query via `SET app.namespace_id`.
- Two builds with different `NAMESPACE_ID` values are fully isolated.

### User Identity (Dev Mode)

- **Next.js middleware** (`src/middleware.ts`) checks for `X-User-Id` header. If absent in development mode, falls back to `DEFAULT_USER_ID`.
- A **dev-only user selector** component appears in the top nav when `NODE_ENV=development`, allowing switching between test user IDs.
- In production mode, this mechanism is disabled. The slot is reserved for real OAuth integration later.

### Why This Enables Future OAuth

- `user_id` is an opaque string on every row. Swapping from dev injection to an OAuth `sub` claim requires only wiring the auth middleware — no schema changes.

---

## 6. Data Layer Implementation

### 6.1 Show Service (`lib/shows/service.ts`)

Core operations:

| Operation | Description |
|---|---|
| `getCollection(filters)` | Fetch all shows where `my_status IS NOT NULL`, apply filter/sort |
| `getShow(showId)` | Fetch single show by `(namespace_id, user_id, id)` |
| `saveShow(show)` | Upsert with merge logic (see 6.2) |
| `removeShow(showId)` | Delete row (clears all My Data) |
| `exportCollection()` | Fetch all shows, package as JSON in ZIP |

### 6.2 Merge Logic (`lib/shows/merge.ts`)

When saving a show that already exists:

1. **Non-user fields** (`overview`, `genres`, `poster_url`, etc.): use `selectFirstNonEmpty(newValue, oldValue)` — never overwrite a non-empty stored value with empty/null.
2. **User fields** (`my_status`, `my_tags`, `my_score`, `my_interest`): compare update timestamps; newer wins.
3. **AI data** (`ai_scoop`): compare `ai_scoop_update_date`; newer wins.
4. Set `details_update_date = NOW()` after merge.
5. Preserve `creation_date` from original row.

### 6.3 Auto-Save Defaults (`lib/shows/defaults.ts`)

| Trigger | Default status | Default interest |
|---|---|---|
| Set any status explicitly | As selected | — |
| Choose Interested/Excited chip | `later` | As selected |
| Rate an unsaved show | `done` | — |
| Add tag to unsaved show | `later` | `interested` |
| No explicit status given | `later` | `interested` |

### 6.4 Removal Semantics

- Reselecting active status triggers confirmation dialog.
- On confirm: delete the row entirely (status, interest, tags, rating, AI Scoop all cleared).
- Track `hideStatusRemovalConfirmation` and `statusRemovalCountKey` in local storage to suppress repeated confirmations.

---

## 7. Catalog Integration (TMDB)

### 7.1 API Routes (server-side proxy)

All TMDB calls go through Next.js API routes so the TMDB key stays server-only:

| Route | TMDB Endpoint | Purpose |
|---|---|---|
| `GET /api/catalog/search?q=&type=` | `/search/multi` or `/search/movie` + `/search/tv` | Text search |
| `GET /api/catalog/show/[id]?type=` | `/movie/{id}` or `/tv/{id}` with `append_to_response` | Full show detail (+ credits, videos, recommendations, similar, providers, images) |
| `GET /api/catalog/person/[id]` | `/person/{id}` with `append_to_response=combined_credits,images` | Person detail + filmography |
| `GET /api/catalog/trending` | `/trending/all/week` | Optional: trending content |

### 7.2 TMDB → Show Mapping (`lib/catalog/mapper.ts`)

Follows the merge/mapping strategy from `storage-schema.md`:

- `id`: TMDB ID as string
- `external_ids`: `{ tmdb: "12345" }` for resolution
- `show_type`: infer from TMDB `media_type` field; fallback: has `name` → `tv`, has `title` → `movie`
- `genres`: map TMDB genre IDs to names via `genre-map.ts`
- Images: construct full URLs from TMDB base URL + path
- Logo selection: filter by English, pick highest rated
- `provider_data`: map TMDB watch/providers response into `{ countries: { [code]: { flatrate, rent, buy } } }` using provider IDs only
- Transient fields (cast, crew, seasons, videos, recommendations, similar, images) returned alongside but not persisted

### 7.3 Genre Map

Static lookup table mapping TMDB genre IDs → display names for both movie and TV genres.

---

## 8. AI Service Implementation

### 8.1 Architecture

- Single `lib/ai/client.ts` wraps the AI provider SDK.
- Server-only — never imported in client components.
- Uses the user's configured `ai_api_key` and `ai_model` from `cloud_settings` if set; falls back to `AI_API_KEY` and `AI_MODEL` env vars.
- Supports streaming responses via Server-Sent Events (SSE) for Ask and Scoop.

### 8.2 Prompt Templates (`lib/ai/prompts.ts`)

Each surface has a dedicated prompt builder that injects the required context:

#### Ask (Chat)

- **System prompt:** persona definition (fun, chatty TV/movie nerd friend), voice pillars, spoiler-safe default, stay within TV/movies, structured output format for mentioned shows.
- **Context injected:** user's library summary (titles + statuses + ratings + tags), current show context (if "Ask about this show").
- **Output contract:** JSON with `commentary` (user-facing text) and `showList` (structured `Title::externalId::mediaType;;...` format).
- **Conversation summarization:** after ~10 messages, older turns compressed to 1-2 sentences preserving persona tone.

#### Scoop

- **System prompt:** persona + Scoop-specific instructions (mini blog post of taste: personal take, honest stack-up, The Scoop centerpiece, fit/warnings, verdict).
- **Context injected:** show title, overview, genres, community score, user's rating/status if saved.
- **Output:** 150-350 word personality-driven review, streamed progressively.
- **Freshness:** check `ai_scoop_update_date`; if > 4 hours old, regenerate on demand.

#### Concepts (Single-Show)

- **System prompt:** generate 8 concept ingredients (1-3 words each, evocative, spoiler-free, diverse axes: structure/vibe/emotion/craft).
- **Context injected:** show title, overview, genres.
- **Output:** bullet list of concepts, ordered by strength.

#### Concepts (Multi-Show / Alchemy)

- **System prompt:** same as single-show but concepts must be **shared across all** input shows.
- **Context injected:** all input shows' titles, overviews, genres.
- **Output:** larger pool of shared concept bullets.

#### Concept-Based Recommendations (Explore Similar + Alchemy)

- **System prompt:** recommend real shows with excited reasoning, cite which concepts align, recent bias but allow classics.
- **Context injected:** selected concepts, source show(s), user's library (to avoid re-recommending saved shows).
- **Output contract:** list of `{ title, externalId, mediaType, reason }`. Explore Similar: 5 recs. Alchemy: 6 recs.
- **Resolution:** for each rec, look up TMDB by external ID; accept if title matches case-insensitively. Unresolved titles shown non-interactive or handed off to Search.

### 8.3 Ask Response Parser (`lib/ai/ask-parser.ts`)

Parses the structured `showList` format:
- Split by `;;` to get individual show entries.
- Split each by `::` to get `[title, externalId, mediaType]`.
- For each, attempt TMDB resolution. Resolved shows become interactive tiles in the mentioned-shows strip.
- Fallback: if parsing fails, retry once with stricter formatting instructions. If still fails, treat entire response as unstructured commentary.

### 8.4 Streaming (`lib/ai/streaming.ts`)

- SSE endpoint pattern for Ask and Scoop routes.
- Partial text chunks streamed to client via `ReadableStream`.
- Client uses `EventSource` or `fetch` with streaming reader.
- UI shows "Generating..." placeholder, then progressive text fill.

---

## 9. Feature Implementation Details

### 9.1 Collection Home (`/`)

**Data flow:**
1. Server component fetches `getCollection()` with active filters from URL params or last-selected-filter.
2. Groups shows into status sections: Active → Excited (Later + Excited) → Interested (Later + Interested) → Other (Wait, Quit, Done, unclassified Later).
3. Active section uses larger tiles; others use standard poster tiles.

**Filters (Sidebar):**
- "All Shows" (default)
- One entry per user tag, plus "No tags" if any tagless shows exist
- Genre filters (derived from genres across collection)
- Decade filters
- Community score range filters
- Media-type toggle (All / Movies / TV) applied on top of any filter

**Show Tile:**
- Poster image, title
- In-collection badge (if `my_status` exists)
- User rating badge (if `my_score` exists)
- Click → navigate to `/show/[id]`

**Empty states:**
- No shows at all → "Start building your collection" with links to Search/Ask
- Filter yields no results → "No results found"

### 9.2 Search (`/find/search`)

**Behavior:**
1. Text input with debounced TMDB search via `/api/catalog/search`.
2. Results displayed in poster grid.
3. Each result checked against user's collection — in-collection items get badge.
4. Clicking a result navigates to `/show/[id]`.
5. Optional "Search on Launch" setting: if enabled, redirect to this page on app start.

### 9.3 Ask (`/find/ask`)

**Components:**
- `ChatInterface`: scrollable chat with user/assistant message bubbles.
- `MentionedShowsStrip`: horizontal row of show tiles extracted from AI response.
- `StarterPrompts`: welcome view with 6 random prompts (from a pool); refresh button to re-randomize.

**Flow:**
1. Welcome screen with starter prompts.
2. User types or selects a prompt.
3. Client sends message to `/api/ai/ask` with conversation history + user library context.
4. Response streams in; `showList` parsed and rendered as mentioned-shows strip.
5. After ~10 messages, backend summarizes older turns to control token depth.
6. Session state (messages, mentioned shows) held in React state; cleared on nav away or explicit reset.

**"Ask About This Show" variant:**
- Launched from Show Detail with a CTA button.
- Navigates to `/find/ask?showId=[id]`.
- Seeds the conversation with the show's context (title, overview, user's status/rating/tags).

### 9.4 Alchemy (`/find/alchemy`)

**Multi-step UI (managed by `useAlchemy` hook):**

| Step | UI | Action |
|---|---|---|
| 1. Select shows | `ShowPicker` — search + collection browser, min 2 shows | User picks 2+ shows |
| 2. Conceptualize | Button: "Conceptualize Shows" | Calls `/api/ai/concepts` with multi-show mode |
| 3. Select concepts | `ConceptChips` — selectable chips, max 8 | User picks 1-8 concepts |
| 4. Alchemize | Button: "ALCHEMIZE!" | Calls `/api/ai/recommend` with selected concepts |
| 5. Results | Show cards with AI reasons | User can save, view detail, or chain |
| Chain | Button: "More Alchemy!" | Results become new inputs; back to step 2 |

**Backtracking:** changing show selection clears concepts and results downstream.

### 9.5 Show Detail (`/show/[id]`)

**Data flow:**
1. Fetch from Supabase (user's saved version if exists).
2. Fetch fresh TMDB detail (with `append_to_response` for credits, videos, recommendations, similar, providers, images).
3. Merge TMDB data into saved show (if exists) using merge rules.
4. Render page sections in narrative hierarchy order.

**Section order (per Detail Page Experience Spec):**
1. Header media carousel (backdrops/posters/logos/trailers)
2. Core facts row (year, runtime/seasons) + community score
3. My Tags (tag chips)
4. Overview + Scoop toggle/stream
5. "Ask about this show" CTA
6. Genres + languages
7. Traditional recommendations strand
8. Explore Similar (concepts → recs)
9. Streaming providers ("Stream It")
10. Cast & Crew (horizontal scrollable strands)
11. Seasons (TV only)
12. Budget vs Revenue (movies, when available)

**Status Toolbar (sticky/fixed position):**
- Status chips: Active, Interested, Excited, Done, Quit, Wait
- Selecting Interested/Excited → sets `my_status=later` + `my_interest` accordingly
- Reselecting active status → removal confirmation → delete show from collection
- Rating bar: slider; rating unsaved show auto-saves as `done`

**Scoop UX:**
- Toggle button copy: "Give me the scoop!" (no scoop) / "Show the scoop" (cached) / "The Scoop" (open)
- On toggle: check `ai_scoop_update_date` — if > 4 hours or null, call `/api/ai/scoop` (streaming)
- Show "Generating..." during stream; progressive text fill
- Persist scoop only if show is in collection

**Explore Similar:**
1. "Get Concepts" button → calls `/api/ai/concepts` (single show)
2. Concept chips appear; user selects 1+
3. "Explore Shows" button → calls `/api/ai/recommend` with selected concepts
4. Results rendered as show cards with AI reasons
5. Each rec resolved to a real TMDB show; clickable to navigate to its Detail

**Header media graceful fallback:**
- Trailers available → auto-play muted with poster fallback
- No trailers → backdrop + logo overlay
- No backdrop → poster only

### 9.6 Person Detail (`/person/[id]`)

**Data flow:** fetch from TMDB `/person/{id}` with `combined_credits` and `images`.

**Sections:**
1. Image gallery (profile photos)
2. Name + bio
3. Analytics charts:
   - Average project rating (bar/line chart)
   - Top genres (horizontal bar)
   - Projects by year (timeline)
4. Filmography grouped by year (most recent first)
5. Each credit links to `/show/[id]`

### 9.7 Settings (`/settings`)

**Sections:**

| Section | Fields | Storage |
|---|---|---|
| App | Font size (XS-XXL), Search on launch toggle | Local storage |
| User | Username | `cloud_settings.user_name` |
| AI | API key, Model selection | `cloud_settings.ai_api_key`, `cloud_settings.ai_model` |
| Integrations | Catalog API key | `cloud_settings.catalog_api_key` |
| Your Data | Export My Data button | Triggers `/api/shows/export` |

**Export:** produces `.zip` containing a JSON file with all shows and My Data. Dates encoded ISO-8601. Downloaded via browser.

---

## 10. Implementation Phases

### Phase 1: Foundation (Infrastructure + Data Layer)

**Goal:** Runnable Next.js app with Supabase, identity injection, and core data operations.

**Tasks:**

1. Initialize Next.js project with TypeScript, Tailwind, shadcn/ui.
2. Create `.env.example` and `.gitignore`.
3. Write Supabase migrations (001-004).
4. Implement Supabase client setup (`lib/supabase/client.ts`, `server.ts`).
5. Implement identity middleware (namespace + user_id extraction, dev auth selector).
6. Implement Show service (`lib/shows/service.ts`) with CRUD, merge logic, and auto-save defaults.
7. Implement show API routes (`/api/shows/`).
8. Implement settings API route (`/api/settings`).
9. Write unit tests for merge logic and auto-save defaults.
10. Create npm scripts: `dev`, `test`, `test:reset`.

**Deliverables:** App starts, connects to Supabase, can create/read/update/delete shows via API with namespace/user isolation.

### Phase 2: Catalog Integration + Collection Home

**Goal:** Users can search TMDB, view results, and build a collection displayed on the home page.

**Tasks:**

1. Implement TMDB client (`lib/catalog/tmdb-client.ts`) and mapper.
2. Implement genre map.
3. Build catalog API routes (search, show detail, person detail).
4. Build root layout with sidebar (filters panel) and top nav.
5. Build Collection Home page with status-grouped sections, media-type toggle.
6. Build Show Tile component with poster, title, badges.
7. Build Filter sidebar (All Shows, tag filters, genre/decade/score filters).
8. Build empty states.
9. Build Find/Discover layout with mode switcher.
10. Build Search page with text input, results grid, collection badges.

**Deliverables:** Users can search for shows, see results, navigate to detail, and view their collection organized by status with working filters.

### Phase 3: Show Detail + Person Detail

**Goal:** Complete Show Detail page with all sections; Person Detail page.

**Tasks:**

1. Build Show Detail page with full section hierarchy:
   - Header media carousel
   - Core facts + community score
   - Status toolbar (sticky) with chips and removal confirmation
   - Rating bar with auto-save logic
   - Tag picker with auto-save logic
   - Overview
   - Genres + languages
   - Traditional recommendations strand
   - Streaming providers
   - Cast & Crew strands
   - Seasons (TV)
   - Budget/Revenue (movies)
2. Build Person Detail page with bio, analytics charts, filmography.
3. Implement removal confirmation dialog with "stop asking" option.
4. Write integration tests for show save/remove flows.

**Deliverables:** Full show detail experience with all My Data controls; person profiles with filmography.

### Phase 4: AI Surfaces

**Goal:** All AI-powered features: Scoop, Ask, Concepts, Explore Similar, Alchemy.

**Tasks:**

1. Implement AI client (`lib/ai/client.ts`) with streaming support.
2. Write all prompt templates following voice/personality spec.
3. Build Scoop section: toggle, streaming display, 4-hour freshness check, persistence rules.
4. Build `/api/ai/scoop` route with SSE streaming.
5. Build Ask chat interface: message bubbles, streaming responses, mentioned-shows strip, starter prompts.
6. Build `/api/ai/ask` route with structured output (commentary + showList).
7. Implement Ask response parser and TMDB resolution for mentioned shows.
8. Implement conversation summarization after ~10 messages.
9. Build "Ask About This Show" flow (seeded context from Detail).
10. Build Concept chips component (shared by Explore Similar and Alchemy).
11. Build `/api/ai/concepts` route (single-show and multi-show modes).
12. Build Explore Similar section on Detail page (Get Concepts → select → Explore Shows).
13. Build `/api/ai/recommend` route with TMDB resolution.
14. Build Alchemy page with full multi-step flow (show picker → conceptualize → select concepts → alchemize → results → chain).
15. Implement Alchemy backtracking (changing shows clears downstream state).

**Deliverables:** All AI surfaces functional with correct voice, structured outputs, catalog resolution, and streaming.

### Phase 5: Settings, Export, Polish

**Goal:** Settings page, data export, UI polish, edge cases, test coverage.

**Tasks:**

1. Build Settings page with all sections (font size, search on launch, username, API keys, model selection).
2. Implement Export My Data (ZIP with JSON, ISO-8601 dates).
3. Implement font size setting (CSS variable propagation).
4. Implement "Search on Launch" redirect behavior.
5. Polish empty states, loading skeletons, error handling.
6. Ensure graceful fallbacks for missing media (no trailer, no backdrop, no poster).
7. Handle TV vs Movie conditional rendering throughout.
8. Verify all auto-save triggers and default behaviors match PRD.
9. Verify merge rules on catalog refresh.
10. Write E2E tests for key user journeys.
11. Verify namespace isolation (two builds don't interfere).
12. Verify dev identity switching works.
13. Final accessibility pass (keyboard nav, screen reader basics).

**Deliverables:** Complete, polished application matching all PRD requirements.

---

## 11. Data Flow Diagrams

### Save Show Flow

```
User Action (set status / rate / add tag)
    │
    ▼
Apply auto-save defaults (lib/shows/defaults.ts)
    │
    ▼
Check if show exists in Supabase
    │
    ├─ No  → INSERT with defaults + creation_date = NOW()
    │
    └─ Yes → MERGE using selectFirstNonEmpty (catalog fields)
             + timestamp comparison (user fields)
             + SET details_update_date = NOW()
             + PRESERVE creation_date
    │
    ▼
Return updated show to client
```

### AI Recommendation Resolution Flow

```
AI returns { title, externalId, mediaType, reason }
    │
    ▼
Lookup TMDB by externalId (if provided)
    │
    ├─ Found + title matches (case-insensitive) → Real Show object
    │       │
    │       ▼
    │   Check user collection for this show
    │       │
    │       ├─ In collection → Attach user overlay (status/tags/rating)
    │       └─ Not in collection → Clean catalog show
    │       │
    │       ▼
    │   Display as interactive tile with AI "reason" as transient text
    │
    └─ Not found → Display title as non-interactive text
                    OR hand off to Search
```

### Scoop Lifecycle

```
User taps "Give me the scoop!" / "Show the scoop"
    │
    ▼
Check ai_scoop_update_date
    │
    ├─ Exists + < 4 hours old → Display cached scoop
    │
    └─ Null OR > 4 hours old
        │
        ▼
    Call /api/ai/scoop (SSE streaming)
        │
        ▼
    Stream text progressively to UI
        │
        ▼
    Is show in collection?
        │
        ├─ Yes → Persist ai_scoop + ai_scoop_update_date
        └─ No  → Display only (ephemeral)
```

---

## 12. Testing Strategy

### Unit Tests

| Module | Key test cases |
|---|---|
| `merge.ts` | Non-empty never overwritten by empty; timestamp wins for user fields; creation_date preserved |
| `defaults.ts` | Rate unsaved → Done; tag unsaved → Later+Interested; explicit status honored; Interested/Excited → Later+interest |
| `ask-parser.ts` | Valid showList parsed; malformed input falls back gracefully; empty showList handled |
| `filter-logic.ts` | All Shows; tag filter; genre filter; media-type toggle stacks on top of filter; No Tags filter |
| `mapper.ts` | TMDB movie response maps correctly; TV response maps correctly; missing fields handled; logo selection |

### Integration Tests

| Test | Validates |
|---|---|
| Shows API | CRUD operations, namespace isolation, user_id scoping, merge on re-save |
| AI API | Scoop streaming, Ask structured output, concepts bullet format, recs with valid IDs |
| Catalog API | TMDB search returns mapped shows, detail returns full show + transient fields |

### E2E Tests

| Test | User journey |
|---|---|
| Collection Home | Shows grouped by status; filter changes update view; media-type toggle works |
| Search → Save | Search → select result → set status → appears in collection |
| Ask Chat | Send message → get streaming response → mentioned shows strip renders → click show → detail |
| Alchemy Flow | Pick shows → conceptualize → select concepts → alchemize → results appear → chain works |
| Removal | Reselect status → confirm → show removed from collection |

### Test Data Reset

`npm run test:reset` script:
1. Reads `NAMESPACE_ID` from env.
2. Deletes all rows in `shows`, `cloud_settings`, `app_metadata` where `namespace_id` matches.
3. Optionally re-seeds with test fixtures.

---

## 13. Cross-Cutting Concerns

### Error Handling

- **TMDB failures:** show graceful error state on search/detail; don't block page render for non-critical sections.
- **AI failures:** show "Couldn't generate" message with retry button; never crash the page.
- **Supabase failures:** toast notification; retry for transient errors.
- **Structured output parse failures:** retry once with stricter formatting; fall back to unstructured display.

### Performance

- TMDB responses cached in Next.js data cache (short TTL, e.g. 5 minutes) to reduce API calls for popular shows.
- Collection Home uses server components for initial render; client-side filter switching via URL params.
- AI streaming prevents blank-screen waiting.
- Images: use `next/image` with TMDB image CDN for automatic optimization.

### Security

- AI API keys and TMDB keys never in client bundles (no `NEXT_PUBLIC_` prefix).
- Supabase anon key is the only key exposed to browser; RLS enforces data isolation.
- Dev identity injection gated on `NODE_ENV=development`.
- User-entered API keys stored in `cloud_settings` (server-side); never committed to repo.

### Data Continuity

- `app_metadata.data_model_version` tracks schema version.
- Future migrations must include forward-migration logic that preserves all existing shows and My Data.
- Migration scripts are idempotent and ordered.

---

## 14. Open Questions & Decisions Deferred

These items from the PRD's "Open Questions" section are noted but **not implemented** in this plan unless a future decision is made:

1. **Next as first-class status** — data model includes `next` in `MyStatusType` but UI does not surface it.
2. **Named custom lists** — tags serve this purpose for now.
3. **AI Scoop on unsaved show implicitly saves** — current plan: scoop is ephemeral if show not in collection.
4. **Clearing My Rating: Unrated vs nil** — current plan: nil (no explicit unrated state).
5. **Import/Restore** — not in scope for initial build; export format designed to support future import.
6. **Saving/sharing Alchemy sessions** — sessions are ephemeral.
7. **myStatus filters in sidebar** — data model supports it; can be added as a sidebar filter type.
