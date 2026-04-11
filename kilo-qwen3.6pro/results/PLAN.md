# Implementation Plan: Personal TV + Movie Companion App

## Overview

A personal TV + movie companion for collecting, organizing, rating, and discovering entertainment. The app combines a personal library with taste-aware AI discovery through conversational AI ("Ask"), concept blending ("Alchemy"), and per-show concept-based recommendations ("Explore Similar").

---

## Architecture Summary

| Layer | Technology |
|---|---|
| Application runtime | Next.js (latest stable) — UI + server boundary |
| Persistence | Supabase (hosted or local) |
| AI | User-provided API key, configurable model |
| External catalog | Provider API key (e.g., TMDB) |
| Auth | Dev identity injection (benchmark mode); designed for future OAuth |

---

## 1. Project Setup & Infrastructure

### 1.1 Repository Structure

```
├── .env.example
├── .gitignore
├── package.json
├── next.config.ts
├── tsconfig.json
├── supabase/
│   ├── migrations/          # Repeatable schema evolution
│   └── seed.sql             # Optional seed data
├── src/
│   ├── config/              # Global constants, env vars
│   ├── theme/               # Design tokens & styling
│   ├── components/          # Shared UI primitives
│   ├── hooks/               # Global hooks
│   ├── utils/               # Global pure functions
│   ├── pages/               # Top-level routes (fractal architecture)
│   ├── server/              # Server-side API routes & AI orchestration
│   └── types/               # Shared TypeScript types
├── tests/
│   ├── unit/
│   └── integration/
└── scripts/
    ├── dev.sh
    ├── test.sh
    └── test-reset.sh
```

### 1.2 Environment Variables

`.env.example`:
```
# Supabase
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=    # Server-only

# External Catalog API
CATALOG_API_KEY=
CATALOG_API_BASE_URL=

# AI Provider
AI_API_KEY=
AI_MODEL=

# Identity (benchmark/dev mode)
DEFAULT_USER_ID=
NAMESPACE_ID=
```

### 1.3 Database Schema (Supabase/PostgreSQL)

#### Tables

**`shows`** — Catalog shows with user overlay
```sql
CREATE TABLE shows (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  namespace_id TEXT NOT NULL,
  user_id TEXT NOT NULL,
  external_catalog_id TEXT,
  title TEXT NOT NULL,
  show_type TEXT NOT NULL CHECK (show_type IN ('movie', 'tv', 'person', 'unknown')),
  overview TEXT,
  genres TEXT[] DEFAULT '{}',
  tagline TEXT,
  homepage TEXT,
  original_language TEXT,
  spoken_languages TEXT[] DEFAULT '{}',
  poster_url TEXT,
  backdrop_url TEXT,
  logo_url TEXT,
  vote_average DOUBLE PRECISION,
  vote_count INTEGER,
  popularity DOUBLE PRECISION,
  release_date DATE,
  first_air_date DATE,
  last_air_date DATE,
  runtime INTEGER,
  budget INTEGER,
  revenue INTEGER,
  series_status TEXT,
  number_of_episodes INTEGER,
  number_of_seasons INTEGER,
  episode_run_time INTEGER[] DEFAULT '{}',
  provider_data JSONB,
  -- User data ("My Data")
  my_status TEXT CHECK (my_status IN ('active', 'later', 'wait', 'done', 'quit', 'next')),
  my_status_update_date TIMESTAMPTZ,
  my_interest TEXT CHECK (my_interest IN ('interested', 'excited')),
  my_interest_update_date TIMESTAMPTZ,
  my_tags TEXT[] DEFAULT '{}',
  my_tags_update_date TIMESTAMPTZ,
  my_score DOUBLE PRECISION,
  my_score_update_date TIMESTAMPTZ,
  ai_scoop TEXT,
  ai_scoop_update_date TIMESTAMPTZ,
  -- Management
  details_update_date TIMESTAMPTZ,
  creation_date TIMESTAMPTZ DEFAULT NOW(),
  is_test BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

**`app_metadata`** — Data model version tracking
```sql
CREATE TABLE app_metadata (
  id TEXT PRIMARY KEY DEFAULT 'globalMetadata',
  namespace_id TEXT NOT NULL,
  data_model_version INTEGER DEFAULT 3,
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

**`cloud_settings`** — Synced app settings (optional)
```sql
CREATE TABLE cloud_settings (
  id TEXT PRIMARY KEY DEFAULT 'globalSettings',
  namespace_id TEXT NOT NULL,
  user_id TEXT NOT NULL,
  user_name TEXT,
  version DOUBLE PRECISION DEFAULT EXTRACT(EPOCH FROM NOW()),
  catalog_api_key TEXT,
  ai_api_key TEXT,
  ai_model TEXT,
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

**Indexes**:
- `(namespace_id, user_id)` on all tables
- `(namespace_id, user_id, my_status)` for collection queries
- `(namespace_id, user_id, my_tags)` for tag filtering
- `(external_catalog_id, show_type)` for catalog lookups

**Row Level Security (RLS)**: All tables scoped by `(namespace_id, user_id)`.

### 1.4 Scripts

- `npm run dev` — Start Next.js dev server
- `npm test` — Run test suite
- `npm run test:reset` — Reset test data for current namespace only (scoped deletes)

---

## 2. Shared Infrastructure Layer

### 2.1 Supabase Client

- `src/config/supabase.ts` — Client creation (browser uses anon key; server routes may use service role)
- `src/hooks/useSupabase.ts` — React hook for client access
- RLS policies enforce `(namespace_id, user_id)` partitioning

### 2.2 Identity Management

- Dev mode: `DEFAULT_USER_ID` from env, or dev-only selector UI
- `src/utils/identity.ts` — Resolve current `user_id` and `namespace_id`
- Server middleware: accept `X-User-Id` header in dev/test only
- All user-owned records scoped to `(namespace_id, user_id)`

### 2.3 External Catalog Integration

- `src/server/catalog/` — Server-side catalog API abstraction
- Provider-agnostic interface: `searchShows()`, `getShowDetails()`, `getPersonDetails()`, `resolveShowByExternalId()`
- Provider data stored as opaque `provider_data` JSONB blob
- Mapping strategy per `storage-schema.md` external catalog → Show mapping rules

### 2.4 AI Service Layer

- `src/server/ai/` — Provider-agnostic AI interface
- Supports streaming responses
- Surface-specific prompt builders:
  - `buildScoopPrompt()` — Show Detail Scoop
  - `buildAskPrompt()` — Conversational discovery
  - `buildConceptsPrompt()` — Single/multi-show concept extraction
  - `buildConceptRecsPrompt()` — Explore Similar / Alchemy recommendations
- Structured output parsing with retry + fallback (per `ai_prompting_context.md`)
- Conversation summarization for chat surfaces (~10 turns threshold)

---

## 3. Pages & Features (Fractal Architecture)

### 3.1 Collection Home Page (`src/pages/Home/`)

**Purpose:** Display user's library organized by status/relationship.

**Features:**
- `Home.tsx` — Page shell with filter sidebar + main content area
- `features/FilterSidebar/` — Navigation panel
  - All Shows (default)
  - Tag filters (one per tag + "No tags")
  - Data filters (genre, decade, community score ranges)
  - Media type toggle (All / Movies / TV)
  - `hooks/useFilterState.ts` — Filter state management
- `features/ShowLibrary/` — Main content grid
  - Status sections: Active (prominent), Excited, Interested, Other (Wait/Quit/Done)
  - `features/ShowTile/` — Individual show tile with poster, title, My Data badges
    - In-collection indicator badge
    - User rating indicator badge
  - `hooks/useLibraryQuery.ts` — Supabase query with filter + status grouping
  - Empty states: "No shows" → prompt Search/Ask; "No results" → filter empty
- `hooks/useCollectionHome.ts` — Orchestrates filter + library state

### 3.2 Find/Discover Hub Page (`src/pages/Find/`)

**Purpose:** Unified discovery entry point with mode switching.

**Features:**
- `Find.tsx` — Page shell with mode switcher
- `features/ModeSwitcher/` — Toggle between Search / Ask / Alchemy
- `features/SearchMode/` — Catalog search
  - Text search by title/keywords
  - Poster grid results
  - In-collection items marked
  - Selecting show → navigate to Detail
  - Auto-open on launch if "Search on Launch" enabled
  - `hooks/useCatalogSearch.ts` — Debounced live search
- `features/AskMode/` — AI chat discovery
  - `features/ChatInterface/` — Chat UI with user/assistant turns
  - `features/MentionedShowsStrip/` — Horizontal strip of AI-mentioned shows
  - `features/StarterPrompts/` — 6 random starter prompts (refreshable)
  - `hooks/useAskSession.ts` — Session management, context, summarization
  - `hooks/useMentionedShowsParser.ts` — Parse `Title::externalId::mediaType;;` format
  - Welcome view when no active session
  - "Ask About a Show" variant: seeded conversation with show context
- `features/AlchemyMode/` — Structured blending discovery
  - Step 1: `features/ShowSelector/` — Pick 2+ starting shows (library + catalog)
  - Step 2: `features/ConceptCatalysts/` — AI-generated concept chips (select 1-8)
  - Step 3: `features/AlchemyResults/` — 6 recommended shows with reasons
  - `features/AlchemyChain/` — "More Alchemy!" to chain rounds
  - `hooks/useAlchemySession.ts` — Multi-step state machine
  - Backtracking: changing shows clears concepts + results

### 3.3 Show Detail Page (`src/pages/ShowDetail/`)

**Purpose:** Single source of truth for a show with My Data + discovery.

**Section order (per `detail_page_experience.md`):**

1. `features/HeaderMedia/` — Backdrops/posters/logos carousel, trailers when available
2. `features/CoreFacts/` — Year, runtime/seasons, genres, languages, community score
3. `features/MyRating/` — Rating slider; rating unsaved show → auto-save as Done
4. `features/MyStatus/` — Status chips (Active/Interested/Excited/Done/Quit/Wait)
   - Interested/Excited → Later + Interest
   - Reselecting status → removal confirmation (with "stop asking" option)
   - Clearing status → remove from collection + clear all My Data
5. `features/MyTags/` — Tag display + picker; adding tag to unsaved → auto-save as Later + Interested
6. `features/Overview/` — Show overview text
7. `features/AIScoop/` — "The Scoop" toggle
   - States: "Give me the scoop!" → "Show the scoop" → open "The Scoop"
   - Streaming generation, 4-hour cache, persisted only if in collection
   - `hooks/useAIScoop.ts` — Generation, caching, streaming
8. `features/AskAboutShow/` — "Ask about this show" CTA → enters Ask mode with context
9. `features/TraditionalRecs/` — Similar/recommended shows strand
10. `features/ExploreSimilar/` — Concept-based discovery
    - "Get Concepts" → select concepts → "Explore Shows" → 5 AI recs
    - `hooks/useExploreSimilar.ts` — Concept fetch + selection + recommendation
11. `features/StreamingAvailability/` — "Stream It" providers
12. `features/CastCrew/` — Horizontal strands → Person Detail navigation
13. `features/Seasons/` — TV only
14. `features/BudgetRevenue/` — Movies when available

**Hooks:**
- `hooks/useShowDetail.ts` — Orchestrates show data loading, merge, My Data state
- `hooks/useShowSave.ts` — Implicit save logic (status, rating, tag triggers)
- `hooks/useShowRemoval.ts` — Removal confirmation + data clearing

### 3.4 Person Detail Page (`src/pages/PersonDetail/`)

**Purpose:** Explore talent behind shows.

**Features:**
- `PersonDetail.tsx` — Page shell
- `features/PersonHeader/` — Image gallery, name, bio
- `features/PersonAnalytics/` — Charts (avg project ratings, top genres, projects-by-year)
- `features/Filmography/` — Credits grouped by year
  - Selecting credit → navigate to Show Detail
- `hooks/usePersonDetail.ts` — Person data loading

### 3.5 Settings Page (`src/pages/Settings/`)

**Purpose:** App configuration and data management.

**Features:**
- `Settings.tsx` — Page shell
- `features/AppSettings/` — Font size (XS/S/M/L/XL/XXL), Search on Launch
- `features/UserSettings/` — Username display/edit
- `features/AISettings/` — AI provider API key, model selection
- `features/IntegrationSettings/` — Catalog API key
- `features/YourData/` — Export My Data (ZIP with JSON, ISO-8601 dates)
  - Import/Restore (noted as open question, not implemented)
- `hooks/useSettings.ts` — Settings state + persistence
- `hooks/useDataExport.ts` — Export logic (JSON → ZIP)

---

## 4. Data Behaviors & Business Rules

### 4.1 Saving Triggers

Any of these actions save a show to the collection:
- Setting any status
- Choosing an interest chip (Interested/Excited)
- Rating an unsaved show → defaults to `Done`
- Adding at least one tag to unsaved show → defaults to `Later + Interested`

### 4.2 Default Values

- Default status on save: `Later`
- Default interest on save: `Interested`
- Exception: First save via rating → `Done`

### 4.3 Removal

- Trigger: User clears status (reselects + confirms)
- Effects: Remove from storage, clear all My Data (status, interest, tags, rating, AI Scoop)
- Warning confirmation shown (with "stop asking" option after repeated removals)

### 4.4 Re-adding

- Preserve latest status, interest, tags, rating, AI Scoop
- Refresh public metadata
- Merge conflicts: most recent update timestamp per field wins

### 4.5 Display Rule

Whenever a show appears anywhere (lists, search, recommendations, AI outputs), if the user has a saved version, display the user-overlaid version (status/tags/rating/scoop). User edits always win over refreshed public data.

### 4.6 Merge Policy

Per `storage-schema.md`:
- Non-my fields: `selectFirstNonEmpty(newValue, oldValue)` — never overwrite non-empty with empty
- My fields: resolve by timestamp (newer wins)
- `detailsUpdateDate` set to now after merge
- `creationDate` set only on first creation

### 4.7 AI Data Persistence

| AI data | Persisted? | Freshness | Notes |
|---|---|---|---|
| AI Scoop | Yes (if in collection) | 4 hours | Regenerates after expiry on demand |
| Alchemy results/reasons | No | Session only | Cleared when leaving Alchemy |
| Ask chat history | No | Session only | Cleared when resetting/leaving Ask |
| Mentioned shows strip | No | Session only | Derived from current chat context |

### 4.8 AI Recommendations → Real Shows

- AI outputs: title + external ID + media type
- System looks up by external ID, accepts first case-insensitive title match
- If found: real selectable Show with transient "reason" text
- If not found: shown non-interactive or handed off to Search

---

## 5. AI Surface Contracts

### 5.1 Shared Rules

- Stay within TV/movies domain
- Spoiler-safe by default
- Opinionated and honest
- Specific, vibe/structure/craft-based reasoning
- Recommendations resolve to real catalog items

### 5.2 Scoop

- Structured: personal take, honest stack-up, Scoop centerpiece, fit/warnings, verdict
- Length: ~150-350 words
- Streaming progressive generation
- Voice: gossipy, vivid, useful

### 5.3 Ask

- Conversational, friend-like dialogue
- Willing to pick favorites
- Simple formatting, bulleted lists for multi-recs
- Length: 1-3 tight paragraphs + list
- Structured mentions: `Title::externalId::mediaType;;` format

### 5.4 Concepts

- Bullet list only
- 1-3 words, evocative, spoiler-free
- No generic concepts ("good characters", "great story")
- Multi-show: shared commonality across all inputs
- Diversity across axes (structure/vibe/emotion/craft)

### 5.5 Concept-Based Recommendations

- Explore Similar: 5 recs per round
- Alchemy: 6 recs per round
- Reasons explicitly reference selected concepts
- Length: 1-3 sentences per rec
- Real catalog items with valid external IDs

### 5.6 Conversation Summarization

- Older turns summarized into 1-2 sentences after ~10 messages
- Summaries preserve persona/tone (no sterile system voice)

### 5.7 Guardrails & Fallbacks

- Unresolvable recommendations: non-interactive or Search handoff
- Structured output parse failure: retry once with stricter instructions, then fallback to unstructured + Search

---

## 6. Cross-Cutting Concerns

### 6.1 Namespace Isolation

- All queries scoped by `(namespace_id, user_id)`
- Destructive test operations scoped to namespace only
- No global database teardown required for test resets

### 6.2 Data Continuity

- `data_model_version` in `app_metadata` tracks schema version
- Migration scripts in `supabase/migrations/`
- On upgrade: existing saved shows and My Data brought forward safely

### 6.3 Backend as Source of Truth

- Clients may cache for performance
- Correctness does not depend on local persistence
- Clearing client storage must not lose user data

### 6.4 Local Settings (client-side)

- `autoSearch` (Bool) — Search opens on launch
- `fontSize` (String) — XS/S/M/L/XL/XXL
- `hideStatusRemovalConfirmation` (Bool)
- `statusRemovalCountKey` (Int)
- `lastSelectedFilter` (JSON) — FilterConfiguration

---

## 7. Implementation Phases

### Phase 1: Foundation
- Project setup, Supabase schema, migrations
- Environment configuration, `.env.example`, `.gitignore`
- Supabase client, identity management, namespace isolation
- External catalog integration (provider-agnostic interface)
- Basic routing and page shells

### Phase 2: Collection & Show Detail
- Show Detail page (all sections per narrative hierarchy)
- My Status, My Interest, My Tags, My Rating with implicit save logic
- AI Scoop generation, caching, streaming
- Collection Home with filter sidebar and status-grouped library
- Show tiles with My Data badges
- Merge policy and display rule implementation

### Phase 3: Discovery Features
- Search mode (catalog search, poster grid, in-collection markers)
- Ask mode (chat UI, starter prompts, mentioned shows parsing, session management)
- Alchemy mode (show selector, concept catalysts, recommendations, chaining)
- Explore Similar (concepts → recommendations on Show Detail)
- AI service layer with all prompt builders and structured output parsing

### Phase 4: Person Detail & Settings
- Person Detail page (header, analytics, filmography)
- Settings page (app settings, user, AI, integrations, data export)
- Data export (ZIP with JSON, ISO-8601 dates)
- Local settings persistence

### Phase 5: Polish & Testing
- Empty states, loading states, error handling
- Unit tests for critical logic (save triggers, merge policy, AI parsing)
- Test reset script (namespace-scoped)
- Discovery quality validation (voice adherence, taste alignment, real-show integrity)
- Lint, typecheck, visual testing

---

## 8. Open Questions / Deferred

- **Next status**: Present in data model but not surfaced as first-class UI
- **Named custom lists**: Beyond tags (e.g., "Weekend Watchlist")
- **AI Scoop on unsaved show**: Should it implicitly save?
- **Explicit Unrated state**: vs nil for cleared rating
- **Import/Restore**: Settings mentions but not implemented
- **Save/share Alchemy sessions**: As reusable "blends"
- **myStatus filters in sidebar**: Model supports it, UI TBD

---

## 9. Key Risk Areas

1. **AI prompt quality**: The AI personality is central to the product experience. Prompt engineering must produce consistent voice across all surfaces (Scoop, Ask, Alchemy, Explore Similar).
2. **Show resolution**: AI recommendations must reliably map to real catalog items. The external ID + title matching fallback needs robust error handling.
3. **Merge conflicts**: Timestamp-based resolution for My Data fields requires careful implementation to avoid data loss during sync.
4. **Conversation summarization**: Must preserve persona tone while compressing context — not a sterile system summary.
5. **Namespace isolation**: All database operations must be correctly scoped to prevent cross-build data leakage in benchmark scenarios.
