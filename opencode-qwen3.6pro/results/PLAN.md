# Implementation Plan

## Overview

This plan outlines the implementation of a personal TV + movie companion application built with **Next.js** (latest stable) and **Supabase** as the persistence layer. The app enables users to build a personal collection of shows, organize them with statuses/interest/tags/ratings, and discover new content through AI-powered surfaces (Ask, Alchemy, Explore Similar) and traditional search.

---

## 1. Architecture

### 1.1 Tech Stack
- **Framework**: Next.js (App Router, latest stable)
- **Database**: Supabase (PostgreSQL)
- **ORM/Client**: Supabase JS client (official libraries)
- **AI Provider**: Configurable via API key (user-provided)
- **Catalog Provider**: External media catalog API (e.g., TMDB)
- **Styling**: Tailwind CSS or equivalent
- **Testing**: Vitest/Jest + Playwright (or equivalent)

### 1.2 Project Structure
```
/
├── app/                          # Next.js App Router
│   ├── (main)/                   # Main layout group
│   │   ├── page.tsx              # Home/Collection
│   │   ├── show/[id]/            # Show Detail
│   │   ├── person/[id]/          # Person Detail
│   │   ├── find/                 # Find/Discover hub
│   │   │   ├── page.tsx          # Mode switcher (Search/Ask/Alchemy)
│   │   │   ├── search/           # Search mode
│   │   │   ├── ask/              # Ask (AI chat) mode
│   │   │   └── alchemy/          # Alchemy mode
│   │   └── settings/             # Settings page
│   ├── api/                      # Server routes
│   │   ├── shows/                # Show CRUD + catalog sync
│   │   ├── ai/                   # AI endpoints (scoop, ask, alchemy, concepts)
│   │   ├── catalog/              # External catalog proxy
│   │   └── export/               # Data export
│   ├── layout.tsx                # Root layout
│   └── globals.css
├── components/                   # UI components
│   ├── show/                     # Show tiles, detail sections
│   ├── discovery/                # Ask, Alchemy, Explore Similar
│   ├── person/                   # Person detail components
│   ├── filters/                  # Sidebar filters
│   └── settings/                 # Settings form components
├── lib/                          # Core utilities
│   ├── supabase/                 # Supabase client + server clients
│   ├── catalog/                  # External catalog integration
│   ├── ai/                       # AI provider abstraction + prompts
│   ├── auth/                     # Dev identity injection
│   └── utils/                    # Helpers (date formatting, etc.)
├── db/                           # Database artifacts
│   ├── migrations/               # SQL migrations
│   └── seed/                     # Optional seed data
├── tests/                        # Test suites
├── .env.example
├── next.config.ts
└── package.json
```

---

## 2. Database Schema

### 2.1 Core Tables

#### `shows`
Stores both catalog metadata and user overlay ("My Data"). Each row is scoped to `(namespace_id, user_id)`.

| Column | Type | Notes |
|--------|------|-------|
| `id` | UUID | Primary key |
| `namespace_id` | TEXT | Build/run isolation |
| `user_id` | TEXT | User identity (opaque stable string) |
| `catalog_id` | TEXT | External catalog ID (e.g., TMDB ID) |
| `show_type` | TEXT | `movie` \| `tv` \| `person` \| `unknown` |
| `title` | TEXT | Display title |
| `external_ids` | JSONB | External identifiers |
| `overview` | TEXT | |
| `genres` | TEXT[] | Genre names |
| `tagline` | TEXT | |
| `homepage` | TEXT | |
| `original_language` | TEXT | |
| `spoken_languages` | TEXT[] | ISO 639-1 codes |
| `languages` | TEXT[] | |
| `poster_url` | TEXT | |
| `backdrop_url` | TEXT | |
| `logo_url` | TEXT | |
| `network_logos` | TEXT[] | |
| `vote_average` | DOUBLE | |
| `popularity` | DOUBLE | |
| `vote_count` | INTEGER | |
| `last_air_date` | TIMESTAMPTZ | |
| `first_air_date` | TIMESTAMPTZ | |
| `release_date` | TIMESTAMPTZ | |
| `runtime` | INTEGER | Movies |
| `budget` | INTEGER | Movies |
| `revenue` | INTEGER | Movies |
| `series_status` | TEXT | TV |
| `num_episodes` | INTEGER | TV |
| `num_seasons` | INTEGER | TV |
| `episode_run_time` | INTEGER[] | TV |
| `provider_data` | JSONB | Streaming provider IDs by region |
| `my_status` | TEXT | `active` \| `next` \| `later` \| `done` \| `quit` \| `wait` |
| `my_status_update_date` | TIMESTAMPTZ | |
| `my_interest` | TEXT | `excited` \| `interested` |
| `my_interest_update_date` | TIMESTAMPTZ | |
| `my_tags` | TEXT[] | |
| `my_tags_update_date` | TIMESTAMPTZ | |
| `my_score` | DOUBLE | |
| `my_score_update_date` | TIMESTAMPTZ | |
| `ai_scoop` | TEXT | |
| `ai_scoop_update_date` | TIMESTAMPTZ | |
| `details_update_date` | TIMESTAMPTZ | Catalog refresh timestamp |
| `creation_date` | TIMESTAMPTZ | |
| `is_test` | BOOLEAN | For destructive testing |

**Indexes**: `(namespace_id, user_id)`, `(namespace_id, user_id, my_status)`, `(namespace_id, user_id, catalog_id)`, `(namespace_id, user_id, my_tags)` (GIN)

#### `cloud_settings`
App-wide settings synced across devices.

| Column | Type | Notes |
|--------|------|-------|
| `id` | TEXT | Primary key (default `"globalSettings"`) |
| `namespace_id` | TEXT | |
| `user_id` | TEXT | |
| `user_name` | TEXT | Random name on first launch |
| `catalog_api_key` | TEXT | |
| `ai_api_key` | TEXT | |
| `ai_model` | TEXT | |
| `version` | DOUBLE | Epoch seconds for conflict resolution |

#### `app_metadata`
Tracks data model version for migrations.

| Column | Type | Notes |
|--------|------|-------|
| `namespace_id` | TEXT | |
| `data_model_version` | INTEGER | Default: 3 |

#### `local_settings`
Client-side preferences (stored in localStorage or server-side if sync desired).

| Key | Type | Default |
|-----|------|---------|
| `auto_search` | BOOLEAN | false |
| `font_size` | TEXT | `"M"` (one of XS/S/M/L/XL/XXL) |

#### `ui_state`
UI preferences.

| Key | Type | Notes |
|-----|------|-------|
| `hide_status_removal_confirmation` | BOOLEAN | Suppress confirmation after repeated dismissals |
| `status_removal_count_key` | INTEGER | Count of confirmations shown |
| `last_selected_filter` | JSONB | `{ type, label, value }` |

### 2.2 RLS Policies (Row Level Security)
- All tables scoped by `(namespace_id, user_id)`
- Supabase anon key used for client queries; service role key for server-only operations
- Policies ensure users can only read/write their own data within their namespace

---

## 3. Identity & Isolation

### 3.1 Namespace Isolation
- `namespace_id` injected via environment variable (`NAMESPACE_ID`)
- All database queries include `WHERE namespace_id = $1`
- Destructive test operations scoped to namespace only

### 3.2 User Identity
- `user_id` injected via dev-only mechanism:
  - `X-User-Id` header accepted by server routes in development/test
  - Dev-only "login as user" selector in UI (gated behind `NODE_ENV !== 'production'`)
  - Default fallback user for benchmark mode
- `user_id` treated as opaque stable string (UUID preferred)
- Schema designed for future OAuth migration without redesign

### 3.3 Effective Partition
All queries use `(namespace_id, user_id)` as the partition key.

---

## 4. External Catalog Integration

### 4.1 Catalog Service (`lib/catalog/`)
- Abstraction layer over external catalog API (e.g., TMDB)
- Supports: search by title/keywords, fetch show details, fetch person details, fetch credits, fetch streaming providers, fetch similar/recommended shows
- Maps catalog responses to internal `Show` format
- Handles image URL construction, genre name resolution, date parsing

### 4.2 Catalog → Show Mapping
- External catalog `id` → `catalog_id`
- Title → `title` (prefer movie title or TV series name)
- Media type → `show_type`
- Genres → `genres` (names, not IDs)
- Images → `poster_url`, `backdrop_url`, `logo_url`
- Ratings → `vote_average`, `vote_count`, `popularity`
- Dates → parsed to ISO-8601
- Provider data → `provider_data` (IDs only, by region)

### 4.3 Merge Policy
When catalog data is merged into existing stored show:
- **Non-my fields**: `selectFirstNonEmpty(newValue, oldValue)` — never overwrite non-empty with empty, never overwrite non-nil with nil
- **My fields**: resolve by timestamp — keep newer update date; if only one side has date, keep that side
- `details_update_date` set to "now" after merge
- `creation_date` set only on first creation

---

## 5. Core Features Implementation

### 5.1 Collection Home (`app/(main)/page.tsx`)

**Purpose**: Display user's library organized by status.

**Implementation**:
- Fetch shows filtered by `(namespace_id, user_id)` and active filter
- Group by status sections:
  1. **Active** (prominent, larger tiles)
  2. **Excited** (Later + Excited)
  3. **Interested** (Later + Interested)
  4. **Other** (collapsed: Wait, Quit, Done, unclassified Later)
- Media type toggle: All / Movies / TV
- Tiles show: poster, title, My Data badges (status indicator, rating badge)
- Empty states: "No shows yet — try Search or Ask" / "No results found"

**Server Component**: Fetch data server-side, pass to client components for interactivity

### 5.2 Filters (Sidebar)

**Implementation**:
- Quick/default: "All Shows"
- Tag filters: one per unique tag in user's collection, plus "No tags" if applicable
- Data filters: genre, decade, community score ranges
- Media type toggle: All / Movies / TV
- Filter state persisted in `ui_state.last_selected_filter`

### 5.3 Search (`app/(main)/find/search`)

**Implementation**:
- Text input → catalog API search
- Results in poster grid
- In-collection items marked with badge
- Selecting show → navigate to Show Detail
- Optional "Search on Launch" via `local_settings.auto_search`
- Live queries (no complex pre-loading/caching required)

### 5.4 Ask (AI Chat) (`app/(main)/find/ask`)

**Implementation**:
- Chat UI with user/assistant turns
- Welcome view with 6 random starter prompts (refreshable)
- Session context maintained; older turns summarized after ~10 messages
- AI may mention shows inline → rendered as "mentioned shows" horizontal strip
- Tapping mentioned show → Show Detail (or Search handoff if mapping fails)
- Structured output: `{ commentary, showList }` where `showList` format: `Title::externalId::mediaType;;...`
- "Ask About a Show" variant: launched from Show Detail, seeds conversation with show context

**Server Route**: `POST /api/ai/ask` — handles chat completion with context

### 5.5 Alchemy (`app/(main)/find/alchemy`)

**Flow**:
1. User selects 2+ starting shows (from library + global catalog)
2. Tap "Conceptualize Shows" → AI extracts shared concepts
3. User selects 1–8 concepts
4. Tap "ALCHEMIZE!" → AI returns 6 recommendations with reasons
5. Optional: "More Alchemy!" to chain using results as new inputs

**Implementation**:
- Multi-step UI with clear step indicators
- Backtracking allowed (changing shows clears concepts/results)
- Concepts: bullet list, 1–3 words, evocative, no explanation
- Recommendations: real catalog items with external IDs + reason text
- Session-only state (not persisted)

**Server Routes**:
- `POST /api/ai/concepts` — concept extraction (single or multi-show)
- `POST /api/ai/recommendations` — concept-based recommendations

### 5.6 Show Detail (`app/(main)/show/[id]`)

**Sections** (in order):
1. **Header media**: backdrops/posters/logos/carousel (trailers if available)
2. **Core facts**: year, runtime/seasons, genres, languages
3. **Community score + My Rating**: rating slider; rating unsaved show → auto-save as Done
4. **My Status + Interest**: status chips; setting status saves; reselecting → removal confirmation
5. **My Tags**: tag display + picker; adding tag to unsaved show → auto-save as Later + Interested
6. **Overview**
7. **AI Scoop**: "Give me the scoop!" toggle; streams progressively; 4-hour cache; persists only if in collection
8. **Traditional recommendations**: similar/recommended shows strand
9. **Explore Similar**: Get Concepts → select concepts → Explore Shows (AI recs)
10. **Streaming availability**
11. **Cast & Crew**: horizontal strands → Person Detail
12. **Seasons** (TV only)
13. **Budget vs Revenue** (movies when available)

**Saving Triggers**:
- Setting any status → save to collection
- Choosing interest chip → save
- Rating unsaved show → save as Done
- Adding tag to unsaved show → save as Later + Interested

**Removing from Collection**:
- User clears status → confirmation warning → remove show + all My Data
- Option to "stop asking" after repeated removals → set `hide_status_removal_confirmation`

### 5.7 Person Detail (`app/(main)/person/[id]`)

**Implementation**:
- Image gallery, name, bio
- Analytics charts: average project ratings, top genres, projects-by-year
- Filmography grouped by year
- Selecting credit → navigate to Show Detail

### 5.8 Settings (`app/(main)/settings`)

**Sections**:
- **App settings**: font size (XS–XXL), search on launch toggle
- **User**: username display
- **AI**: provider API key, model selection
- **Integrations**: catalog API key
- **Your data**:
  - Export My Data → `.zip` with JSON backup (ISO-8601 dates)
  - Import/Restore: noted as not yet implemented

---

## 6. AI System

### 6.1 AI Provider Abstraction (`lib/ai/`)
- Interface for AI provider (OpenAI-compatible or similar)
- Configurable via `AI_API_KEY` and `AI_MODEL` env vars
- Supports streaming responses for Scoop
- Handles structured output parsing (concepts, recommendations with show lists)

### 6.2 AI Personality
Consistent persona across all surfaces: "fun, chatty TV/movie nerd friend"
- Joy-forward, warm, opinionated but honest
- Vibe-first, spoiler-safe by default
- Specific, not generic
- Short by default, lush when earned (Scoop)

### 6.3 AI Surfaces

| Surface | Purpose | Output | Count |
|---------|---------|--------|-------|
| Scoop | Taste review on Detail | Structured mini blog post | ~150-350 words |
| Ask | Conversational discovery | Chat response + optional show list | 1-3 paragraphs + list |
| Concepts | Extract show ingredients | Bullet list | 8 concepts (default) |
| Recommendations | Concept-based recs | Shows + reasons | 5 (Explore) / 6 (Alchemy) |

### 6.4 AI Data Persistence

| AI Data | Persisted? | Freshness | Notes |
|---------|-----------|-----------|-------|
| AI Scoop | Yes (if in collection) | 4 hours | Regenerates on demand after expiry |
| Alchemy results | No | Session only | Cleared when leaving |
| Ask chat history | No | Session only | Cleared when resetting |
| Mentioned shows | No | Session only | Derived from current context |

### 6.5 Conversation Summarization
- After ~10 messages, older turns summarized to 1-2 sentences
- Summary preserves persona/tone (no sterile "system summary" voice)

### 6.6 Guardrails
- Recommendations must resolve to real catalog items via external ID
- If resolution fails: show as non-interactive or hand off to Search
- If structured output parsing fails: retry once, then fall back to unstructured + Search

---

## 7. Data Behaviors & Business Rules

### 7.1 Collection Membership
- Show is "in collection" when it has a non-nil `my_status`

### 7.2 Default Values When Saving
- Default status: `Later`
- Default interest: `Interested`
- Exception: first save via rating → status defaults to `Done`

### 7.3 Re-adding Same Show
- Preserve latest status, interest, tags, rating, AI Scoop
- Refresh public metadata
- Merge conflicts: most recent update timestamp per field wins

### 7.4 Tile Indicators
- In-collection badge when `my_status` exists
- User rating badge when `my_score` exists

### 7.5 Data Sync & Integrity
- Optional cross-device sync via Supabase
- Conflicts resolved per field using most recent edit timestamp
- Duplicates detected and merged transparently

### 7.6 Data Continuity Across Versions
- `data_model_version` in `app_metadata` tracks schema version
- Migrations preserve all user data across updates
- Users never lose collection, ratings, tags, statuses, interest levels, or AI Scoop due to update

---

## 8. Environment & Configuration

### 8.1 `.env.example`
```env
# Supabase
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=

# Namespace & User (benchmark/dev mode)
NAMESPACE_ID=
DEFAULT_USER_ID=

# AI Provider
AI_API_KEY=
AI_MODEL=

# External Catalog
CATALOG_API_KEY=
CATALOG_BASE_URL=

# Node
NODE_ENV=development
```

### 8.2 `.gitignore`
Excludes `.env*` (except `.env.example`), `node_modules/`, `.next/`, etc.

### 8.3 Scripts
- `npm run dev` — Start development server
- `npm test` — Run test suite
- `npm run test:reset` — Reset test data for current namespace

---

## 9. Database Migrations

### 9.1 Migration Strategy
- SQL migration files in `db/migrations/`
- Numbered sequentially (e.g., `001_create_shows.sql`)
- Each migration is idempotent where possible
- `data_model_version` incremented with each schema change

### 9.2 Initial Migrations
1. `001_create_shows` — Create `shows` table with all fields + indexes
2. `002_create_cloud_settings` — Create `cloud_settings` table
3. `003_create_app_metadata` — Create `app_metadata` table
4. `004_rls_policies` — Set up Row Level Security policies
5. `005_indexes` — Add performance indexes

---

## 10. Testing Strategy

### 10.1 Unit Tests
- Catalog mapping logic
- Merge policy implementation
- AI output parsing (concepts, recommendations, show list format)
- Status/interest/tag saving triggers
- Default value logic

### 10.2 Integration Tests
- Show CRUD operations with namespace isolation
- AI endpoint responses (mocked AI provider)
- Catalog API integration (mocked)
- Data export functionality

### 10.3 E2E Tests
- Collection home: add show, change status, verify grouping
- Search: query results, navigate to detail
- Ask: send message, receive response, tap mentioned show
- Alchemy: full flow (select shows → concepts → recommendations)
- Settings: export data, verify zip contents
- Namespace isolation: two namespaces don't see each other's data

### 10.4 Destructive Testing
- Test data created within namespace only
- `npm run test:reset` clears test data for current namespace
- No global database teardown required

---

## 11. Discovery Quality Bar

### 11.1 Quality Dimensions
- **Voice Adherence**: warm, playful, opinionated, spoiler-safe
- **Taste Alignment**: grounded in concepts/library, specific reasons
- **Surprise Without Betrayal**: 1-2 pleasantly unexpected but defensible recs
- **Specificity of Reasoning**: concrete "because" tied to concepts
- **Real-Show Integrity**: every rec maps to real catalog item (non-negotiable)

### 11.2 Scoring Rubric
Score each dimension 0-2:
- 0 = fail, 1 = acceptable, 2 = great
- Passing: Voice ≥1, Taste alignment ≥1, Real-show integrity =2, Total ≥7/10

---

## 12. Implementation Phases

### Phase 1: Foundation (Week 1-2)
- Project setup with Next.js + Supabase
- Database schema + migrations
- Environment configuration + `.env.example`
- Dev identity injection (`X-User-Id` header, default user)
- Catalog integration layer
- Basic Show model + CRUD API

### Phase 2: Collection & Detail (Week 2-3)
- Collection Home with status grouping
- Filters sidebar (tags, genre, decade, score)
- Show Detail page (all sections except AI)
- Status/Interest/Tag/Rating saving triggers
- Merge policy implementation
- Tile indicators

### Phase 3: Discovery (Week 3-4)
- Search with catalog integration
- Find/Discover hub with mode switcher
- Person Detail page
- Traditional recommendations strand

### Phase 4: AI Surfaces (Week 4-5)
- AI provider abstraction
- Scoop generation + streaming + 4-hour cache
- Ask chat UI + session context + summarization
- Mentioned shows parsing + strip
- Concept extraction (single + multi-show)
- Explore Similar flow
- Alchemy full flow

### Phase 5: Settings & Export (Week 5)
- Settings page (app, user, AI, integrations)
- Export My Data (JSON → zip)
- Local settings (font size, auto search)
- UI state persistence

### Phase 6: Polish & Testing (Week 5-6)
- Empty states
- Loading states + error handling
- Namespace isolation verification
- Destructive test reset script
- Unit + integration + E2E tests
- Discovery quality validation

---

## 13. Open Questions / Deferred

- **Next status**: Present in data model but not surfaced as first-class UI. Keep hidden for now.
- **Named custom lists**: Beyond tags — defer to future iteration.
- **AI Scoop on unsaved show**: Currently ephemeral; does not implicitly save.
- **Unrated state vs nil**: Keep as nil for now.
- **Import/Restore**: Mentioned in Settings but not implemented — defer.
- **Save/share Alchemy sessions**: Defer.
- **myStatus filters in sidebar**: Model supports it; UI can be added later.

---

## 14. Key Design Decisions

1. **Backend is source of truth**: Clients cache for performance but correctness doesn't depend on local persistence
2. **User's version takes precedence**: My Data always wins over refreshed public data
3. **Taste-aware AI**: All AI surfaces use library + My Data + session context
4. **Namespace isolation**: `(namespace_id, user_id)` partition for all data
5. **Migration-friendly auth**: Dev identity injection designed for easy OAuth swap later
6. **Session-only AI state**: Alchemy results, chat history, mentioned shows are ephemeral
7. **Structured AI output**: Recommendations include external IDs for catalog resolution
8. **Progressive streaming**: Scoop streams progressively to avoid blank wait states
