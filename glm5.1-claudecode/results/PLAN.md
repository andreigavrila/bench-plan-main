# Implementation Plan — Personal TV & Movie Companion

## 1. Executive Summary

A personal entertainment companion app for collecting, organizing, rating, and discovering TV shows and movies. Users build their own version of each show (status, interest, tags, rating, AI scoop), and the app uses that taste profile to power discovery through search, conversational AI ("Ask"), concept-blending ("Alchemy"), and per-show "Explore Similar."

**Stack:** Next.js (latest stable), Supabase (persistence), external catalog API (e.g. TMDB), AI provider (LLM API).

---

## 2. Architecture Overview

### 2.1 Technology Decisions

| Layer | Choice | Rationale |
|---|---|---|
| Framework | Next.js (App Router) | Required by infra rider; server components + API routes |
| Database | Supabase (PostgreSQL) | Required by infra rider; provides auth, RLS, real-time |
| State Management | React Context + SWR/React Query | Client cache with server as truth; SWR for revalidation |
| Styling | Tailwind CSS + design tokens in `src/theme/` | Fast iteration, token-based per INSTRUCTIONS.md |
| AI Integration | Server-side LLM API routes | Keep API keys server-only; stream responses to client |
| External Catalog | TMDB API (or similar) via server routes | Catalog data fetched server-side, keys server-only |
| Testing | Jest + React Testing Library + Playwright (visual) | Unit + visual tests per INSTRUCTIONS.md |

### 2.2 Fractal Architecture

Following the INSTRUCTIONS.md pattern: Pages contain Features, Features contain Sub-Features — each self-contained.

```
src/
├── config/                  # Global constants & env vars
│   ├── env.ts               # NEXT_PUBLIC_* and server-only vars
│   └── constants.ts         # Status types, interest levels, limits
├── theme/                   # Design tokens & styling
│   └── tokens.ts            # Colors, spacing, typography scales
├── components/              # Shared UI primitives
│   ├── PosterTile/
│   ├── StatusChips/
│   ├── RatingBar/
│   ├── TagPicker/
│   ├── MediaCarousel/
│   ├── SectionStrand/
│   └── LoadingState/
├── hooks/                   # Global hooks
│   ├── useNamespace.ts
│   ├── useUser.ts
│   └── useSettings.ts
├── utils/                   # Global pure functions
│   ├── catalogMapper.ts     # External catalog → Show mapping
│   ├── mergeRules.ts        # Show merge/overwrite policy
│   ├── exportBackup.ts      # ZIP export logic
│   └── dateUtils.ts
├── lib/                     # External service clients
│   ├── supabase/
│   │   ├── client.ts        # Browser Supabase client
│   │   ├── server.ts        # Server Supabase client
│   │   └── queries/         # Typed database queries
│   ├── catalog/             # External catalog API client
│   └── ai/                  # AI provider client + prompt templates
├── types/                   # Shared TypeScript types
│   └── show.ts              # Show, MyStatusType, MyInterestType, etc.
└── pages/ (or app/ routes)
    ├── Home/
    │   ├── Home.tsx
    │   └── features/
    │       ├── FilterPanel/
    │       ├── StatusSections/
    │       └── MediaTypeToggle/
    ├── Find/
    │   ├── Find.tsx
    │   └── features/
    │       ├── Search/
    │       ├── Ask/
    │       │   ├── Ask.tsx
    │       │   └── features/
    │       │       ├── ChatMessages/
    │       │       ├── MentionedShows/
    │       │       └── StarterPrompts/
    │       └── Alchemy/
    │           ├── Alchemy.tsx
    │           └── features/
    │               ├── ShowSelector/
    │               ├── ConceptChips/
    │               └── RecommendationResults/
    ├── Detail/
    │   ├── Detail.tsx
    │   └── features/
    │       ├── HeaderMedia/
    │       ├── CoreFacts/
    │       ├── StatusControls/
    │       ├── RatingControl/
    │       ├── TagManager/
    │       ├── OverviewAndScoop/
    │       ├── ExploreSimilar/
    │       ├── Recommendations/
    │       ├── StreamingProviders/
    │       ├── CastCrew/
    │       ├── Seasons/
    │       └── BudgetRevenue/
    ├── Person/
    │   ├── Person.tsx
    │   └── features/
    │       ├── PersonGallery/
    │       ├── Filmography/
    │       └── AnalyticsCharts/
    └── Settings/
        ├── Settings.tsx
        └── features/
            ├── UserSettings/
            ├── AISettings/
            └── DataExport/
```

### 2.3 Server/Client Boundary

- **Server Components:** Layout shells, initial data loading, SEO metadata
- **Client Components:** Interactive features (status chips, rating bars, chat, filters)
- **API Routes (App Router `route.ts`):** All external API calls (catalog, AI), data mutations to Supabase
- **Server Actions:** Form submissions for settings, status changes, etc.

---

## 3. Data Model & Supabase Schema

### 3.1 Database Tables

```sql
-- Namespace isolation
CREATE TABLE namespaces (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Users within a namespace
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  namespace_id UUID NOT NULL REFERENCES namespaces(id) ON DELETE CASCADE,
  display_name TEXT NOT NULL DEFAULT 'User',
  created_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE(namespace_id, id)
);

-- Shows (collection + catalog data)
CREATE TABLE shows (
  id TEXT PRIMARY KEY,               -- external catalog ID (e.g. "tmdb-12345")
  namespace_id UUID NOT NULL REFERENCES namespaces(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  show_type TEXT NOT NULL DEFAULT 'unknown',  -- movie | tv | person | unknown
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
  -- User data ("My Data")
  my_tags TEXT[] DEFAULT '{}',
  my_tags_update_date TIMESTAMPTZ,
  my_score FLOAT,
  my_score_update_date TIMESTAMPTZ,
  my_status TEXT,                     -- active | next | later | done | quit | wait
  my_status_update_date TIMESTAMPTZ,
  my_interest TEXT,                   -- excited | interested
  my_interest_update_date TIMESTAMPTZ,
  -- AI data
  ai_scoop TEXT,
  ai_scoop_update_date TIMESTAMPTZ,
  -- Metadata
  details_update_date TIMESTAMPTZ,
  creation_date TIMESTAMPTZ DEFAULT now(),
  is_test BOOLEAN DEFAULT false,
  provider_data JSONB,
  UNIQUE(namespace_id, user_id, id)
);

-- Cloud settings (synced preferences)
CREATE TABLE cloud_settings (
  id TEXT PRIMARY KEY DEFAULT 'globalSettings',
  namespace_id UUID NOT NULL REFERENCES namespaces(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  user_name TEXT NOT NULL DEFAULT 'User',
  version FLOAT NOT NULL DEFAULT 0,
  catalog_api_key TEXT,
  ai_api_key TEXT,
  ai_model TEXT NOT NULL DEFAULT 'default',
  updated_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE(namespace_id, user_id)
);

-- App metadata (migration tracking)
CREATE TABLE app_metadata (
  id TEXT PRIMARY KEY DEFAULT 'singleton',
  namespace_id UUID NOT NULL REFERENCES namespaces(id) ON DELETE CASCADE,
  data_model_version INT NOT NULL DEFAULT 4,
  UNIQUE(namespace_id)
);

-- Row-Level Security
ALTER TABLE shows ENABLE ROW LEVEL SECURITY;
ALTER TABLE cloud_settings ENABLE ROW LEVEL SECURITY;
ALTER TABLE app_metadata ENABLE ROW LEVEL SECURITY;

CREATE POLICY "shows_ns_user" ON shows
  USING (namespace_id = current_setting('app.namespace_id')::uuid
    AND user_id = current_setting('app.user_id')::uuid);

CREATE POLICY "settings_ns_user" ON cloud_settings
  USING (namespace_id = current_setting('app.namespace_id')::uuid
    AND user_id = current_setting('app.user_id')::uuid);
```

### 3.2 Local Settings (Client-Side)

Stored in localStorage (or Supabase `local_settings` table if cross-device sync needed):
- `autoSearch: boolean` — open Search on launch
- `fontSize: "XS" | "S" | "M" | "L" | "XL" | "XXL"`
- `hideStatusRemovalConfirmation: boolean`
- `statusRemovalCount: number`
- `lastSelectedFilter: FilterConfiguration | null`

### 3.3 Transient Data (Not Persisted)

These are fetched per-session and never stored:
- Cast & crew credits
- Season/episode details
- Full image galleries
- Video/trailer data
- Traditional recommendations & similar shows
- AI chat history (Ask sessions)
- Alchemy session state
- AI-generated descriptions

---

## 4. Core Features — Implementation Breakdown

### 4.1 Collection Home

**Route:** `/` (root)

**Features:**
- **FilterPanel** — sidebar with filter chips: All Shows, tag filters, genre/decade/score filters, media-type toggle (All/Movies/TV)
- **StatusSections** — groups shows into sections:
  1. Active (prominent, larger tiles)
  2. Excited (Later + Excited)
  3. Interested (Later + Interested)
  4. Other (collapsed: Wait, Quit, Done, unclassified Later)
- **Show tiles** display: poster, title, in-collection badge, user rating badge

**Data flow:**
- Query `shows` table filtered by `(namespace_id, user_id)` where `my_status IS NOT NULL`
- Apply active filter configuration
- Sort by `my_status_update_date` DESC within each section

**Empty states:**
- No collection → prompt to Search/Ask
- Filter yields nothing → "No results found"

### 4.2 Find/Discover Hub

**Route:** `/find`

**Features:**
- Mode switcher tabs: Search | Ask | Alchemy
- Each mode is a self-contained feature

#### 4.2.1 Search

**Features:**
- Text input, live query against external catalog API
- Poster grid results, in-collection items marked
- Selecting a show navigates to `/detail/[id]`
- Optional "Search on Launch" auto-opens Search on app launch

**Data flow:**
- API route: `GET /api/catalog/search?q={query}`
- Server calls external catalog, maps results to Show type
- For each result, check if user has saved version → overlay My Data

#### 4.2.2 Ask (Chat)

**Features:**
- **StarterPrompts** — 6 random prompts from a curated list of 80; refreshable
- **ChatMessages** — conversation turns, user + assistant
- **MentionedShows** — horizontal strip of shows mentioned by AI
- "Ask about a show" variant seeds conversation with show context

**Data flow:**
- API route: `POST /api/ai/ask`
- Request: conversation history (recent turns + summary of older), user library context, optional show context
- Response: `{ commentary: string, showList: string }` where showList format is `Title::externalId::mediaType;;...`
- Client parses showList into MentionedShows strip
- Each mentioned show resolves via catalog lookup; failures become non-interactive text

**Conversation management:**
- Keep last ~10 turns as-is
- Summarize older turns into 1-2 sentences (same persona tone)
- Session-scoped only; clearing on navigation

#### 4.2.3 Alchemy

**Features:**
- **ShowSelector** — pick 2+ shows from library + global catalog search
- **ConceptChips** — after "Conceptualize Shows", display AI-generated concept chips; user selects 1-8
- **RecommendationResults** — after "ALCHEMIZE!", show 6 recommended shows with reasons
- "More Alchemy!" chains another round using results as new inputs

**Data flow:**
- API route: `POST /api/ai/concepts` — input: shows → output: concept list
- API route: `POST /api/ai/recommendations` — input: selected concepts + shows → output: 6 recs with reasons
- Each rec must map to real catalog item (title + external ID + media type)
- Unresolvable titles shown non-interactive or handed to Search

### 4.3 Show Detail Page

**Route:** `/detail/[id]`

**Sections (in order):**
1. **HeaderMedia** — backdrop/poster/logo carousel + trailers when available
2. **CoreFacts** — year, runtime/seasons, community score bar
3. **StatusControls** — status chips in toolbar (Active/Interested/Excited/Done/Quit/Wait)
4. **RatingControl** — rating bar; rating unsaved show auto-saves as Done
5. **TagManager** — tag display + picker; tagging unsaved show auto-saves as Later+Interested
6. **OverviewAndScoop** — overview text + "The Scoop" toggle/stream
7. **AskAboutShow** — CTA button → navigates to Ask with show context seeded
8. **Genres & Languages** — chips
9. **Recommendations** — traditional "similar/recommended" strand
10. **ExploreSimilar** — "Get Concepts" → select concepts → "Explore Shows" (5 AI recs)
11. **StreamingProviders** — "Stream It" section with provider logos
12. **CastCrew** — horizontal strands → links to Person Detail
13. **Seasons** (TV only)
14. **BudgetRevenue** (movies where available)

**Auto-save behaviors:**
- Setting any status → save show
- Rating unsaved show → save as Done
- Tagging unsaved show → save as Later + Interested
- Reselecting active status → confirmation dialog → remove show + clear all My Data

**Scoop behavior:**
- Toggle: "Give me the scoop!" → "Show the scoop" → "The Scoop" (expanded)
- Streams progressively via SSE/streaming endpoint
- Freshness: regenerates after 4 hours on demand
- Only persists to DB if show is in collection

### 4.4 Person Detail Page

**Route:** `/person/[id]`

**Features:**
- **PersonGallery** — image gallery + name + bio
- **Filmography** — credits grouped by year
- **AnalyticsCharts** — average project ratings, top genres, projects-by-year
- Each credit links to Show Detail

### 4.5 Settings Page

**Route:** `/settings`

**Sections:**
- **App settings:** Font size, Search on Launch
- **User:** Username (synced)
- **AI settings:** Provider key (env var or user-entered, never committed), model selection (synced)
- **Integrations:** Catalog API key (synced)
- **Your Data:** "Export My Data" → produces `.zip` with JSON backup (ISO-8601 dates)

---

## 5. Cross-Cutting Concerns

### 5.1 Identity & Isolation

**Namespace isolation:**
- Every Supabase query includes `namespace_id` filter
- Server middleware extracts namespace from config/env
- RLS policies enforce namespace + user_id partition

**User identity (dev mode):**
- `X-User-Id` header accepted by API routes in development
- Server middleware injects user_id into request context
- Dev-only "login as user" selector available
- Production: replace with real OAuth (Google) without schema changes

**Environment variables:**
```
# .env.example
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=       # Server-only
NAMESPACE_ID=                    # Build isolation
DEFAULT_USER_ID=                 # Dev identity injection
AI_API_KEY=                      # AI provider key (server-only)
CATALOG_API_KEY=                 # External catalog key (server-only)
```

### 5.2 Catalog Integration

**External catalog API (TMDB assumed as reference):**
- Server-side API routes proxy all catalog requests
- Map TMDB responses to internal Show type using `catalogMapper.ts`
- Merge rules when updating existing saved shows:
  - Non-My fields: `selectFirstNonEmpty(new, old)` — never overwrite non-empty with empty
  - My fields: resolve by update timestamp (newer wins)
  - `detailsUpdateDate` = now after merge
  - `creationDate` set only on first creation

**Transient fetches (not persisted):**
- Credits (cast/crew) — fetched per Detail page visit
- Seasons/episodes — fetched per Detail page visit
- Images/videos — fetched per Detail page visit
- Recommendations/similar — fetched per Detail page visit

### 5.3 AI Integration

**AI surfaces and their contracts:**

| Surface | Input | Output | Persistence |
|---|---|---|---|
| Ask (chat) | Library, conversation history, optional show context | `{ commentary, showList }` | Session only |
| Scoop | Show details | Structured "mini blog post" text | Cached 4h if in collection |
| Concepts (single) | 1 show | 1-3 word evocative bullet list | Session only |
| Concepts (multi/Alchemy) | 2+ shows | Shared concept bullet list | Session only |
| Concept Recs | Selected concepts + shows | 5-6 shows with reasons | Session only |

**Server-side AI routes:**
- All AI API keys stored server-only
- Streaming responses via ReadableStream/SSE for Scoop and Ask
- Structured output parsing with retry-on-failure fallback
- Guardrails: stay in TV/movie domain, spoiler-safe, taste-aware

**AI persona consistency:**
- Fun, chatty TV/movie nerd friend
- 70% friend / 30% critic tone balance
- Joy-forward, opinionated, specific (not generic)
- Mirror show's emotional color; spoiler-safe by default

### 5.4 Data Behaviors & Business Rules

**Saving triggers:**
- Setting status → save
- Choosing interest chip → save (Later + Interested/Excited)
- Rating unsaved show → save as Done
- Tagging unsaved show → save as Later + Interested

**Default values:**
- No explicit status → Later + Interested
- Rating first → Done (implies watched)

**Removal:**
- Clear status (reselect + confirm) → remove show, clear all My Data
- Warning confirmation with "don't ask again" option after repeated removals

**Re-adding:**
- Preserve latest My Data, refresh public metadata
- Merge by newest timestamp per field

### 5.5 Export/Backup

"Export My Data" produces a `.zip` containing:
- JSON file with all saved shows and My Data
- ISO-8601 date encoding
- Re-import is a future feature (noted in open questions)

---

## 6. API Routes

| Route | Method | Purpose |
|---|---|---|
| `/api/catalog/search` | GET | Search external catalog by query |
| `/api/catalog/show/[id]` | GET | Fetch show details + credits/seasons/images |
| `/api/catalog/person/[id]` | GET | Fetch person details + filmography |
| `/api/shows` | GET | List user's collection (filtered) |
| `/api/shows/[id]` | GET/PUT/DELETE | CRUD on saved show |
| `/api/shows/[id]/status` | PUT | Update My Status |
| `/api/shows/[id]/rate` | PUT | Update My Rating |
| `/api/shows/[id]/tags` | PUT | Update My Tags |
| `/api/ai/ask` | POST | Ask chat (streaming) |
| `/api/ai/scoop/[id]` | POST | Generate AI Scoop (streaming) |
| `/api/ai/concepts` | POST | Generate concepts |
| `/api/ai/recommendations` | POST | Generate concept-based recs |
| `/api/settings` | GET/PUT | Cloud settings |
| `/api/export` | GET | Export user data as zip |

---

## 7. Implementation Phases

### Phase 1: Foundation (Infrastructure & Skeleton)

**Goal:** Runnable app with auth, database, and empty page shells.

1. Initialize Next.js project with TypeScript, Tailwind, App Router
2. Set up Supabase project, run migrations for all tables
3. Create `.env.example`, `.gitignore`
4. Implement namespace + user identity middleware (dev identity injection via header/config)
5. Set up `src/config/`, `src/theme/`, `src/types/`
6. Create shared UI primitives: PosterTile, StatusChips, RatingBar, TagPicker, MediaCarousel, SectionStrand, LoadingState
7. Create page shells: Home, Find, Detail, Person, Settings
8. Set up Supabase client files (browser + server)
9. Add `npm run dev`, `npm test`, `npm run test:reset` scripts
10. Seed script for test data within namespace

### Phase 2: Core Data & Collection

**Goal:** Users can save, organize, and browse their collection.

1. Implement catalog API client and mapper (`src/lib/catalog/`)
2. Implement Search feature (Find → Search) with external catalog integration
3. Implement Show Detail page — basic layout with core facts, overview
4. Implement StatusControls (status chips + auto-save logic)
5. Implement RatingControl (rating bar + auto-save-as-Done logic)
6. Implement TagManager (tag picker + auto-save-as-Later logic)
7. Implement Collection Home — status sections, filter panel, media-type toggle
8. Implement merge rules for catalog refresh into saved shows
9. Implement removal flow (confirmation + clear My Data)

### Phase 3: AI Features

**Goal:** All AI surfaces functional with consistent persona.

1. Set up AI client (`src/lib/ai/`) with streaming support
2. Implement AI Scoop (Detail page) — streaming generation, 4h cache, persistence rules
3. Implement Ask (Find → Ask) — chat UI, conversation management, summarization, mentioned shows parsing
4. Implement StarterPrompts for Ask (curated list, random selection, refresh)
5. Implement Concepts generation (single-show for Explore Similar)
6. Implement Explore Similar flow (Detail → Get Concepts → select → Explore Shows → 5 recs)
7. Implement Alchemy (Find → Alchemy) — show selector, concept generation, recommendations, chaining
8. Implement "Ask about this show" handoff from Detail to Ask
9. Add AI settings (API key config, model selection) in Settings

### Phase 4: Polish & Remaining Features

**Goal:** Complete feature set and quality bar.

1. Implement Person Detail page (gallery, filmography, analytics charts)
2. Implement Cast & Crew section in Detail (horizontal strands linking to Person)
3. Implement Streaming Providers section ("Stream It")
4. Implement Seasons section (TV shows)
5. Implement Budget/Revenue section (movies)
6. Implement Header Media carousel (backdrops/posters/logos/trailers)
7. Implement traditional recommendations strand
8. Implement Settings page fully (font size, search-on-launch, username, export)
9. Implement Export My Data (zip + JSON)
10. Implement cloud settings sync

### Phase 5: Quality & Testing

**Goal:** Robust, testable, benchmark-ready.

1. Unit tests for merge rules, auto-save triggers, filter logic, export logic
2. Unit tests for AI response parsing (showList format, concept format)
3. Integration tests for CRUD flows (save, update, remove, re-add)
4. Integration tests for namespace isolation (data collision prevention)
5. Visual tests for key pages (Home, Detail, Ask, Alchemy)
6. Test reset script (namespace-scoped destructive testing)
7. Error handling: network failures, AI parsing failures, catalog API errors
8. Loading states and empty states for all features
9. Responsive layout verification

---

## 8. Testing Strategy

### Unit Tests
- `mergeRules.ts` — all merge/overwrite scenarios (empty vs non-empty, timestamp resolution)
- `catalogMapper.ts` — external catalog → Show mapping, type inference rules
- Auto-save trigger logic — verify correct defaults per trigger type
- AI response parsing — showList format, concept format, retry logic
- Filter logic — status sections, tag filters, genre/decade/score ranges
- Export backup — JSON structure, ISO-8601 dates

### Integration Tests
- Full CRUD lifecycle: save → update → refresh catalog → merge → remove → re-add
- Namespace isolation: two namespaces cannot read/write each other's data
- User isolation within namespace
- AI surface contracts: Ask returns valid showList, Scoop streams, Concepts are 1-3 words
- Destructive test reset: seed data → run tests → reset → verify clean state

### Visual Tests
- Home page with populated collection (all status sections)
- Detail page (saved vs unsaved show states)
- Ask chat interface
- Alchemy flow (each step)
- Empty states

---

## 9. Key Technical Decisions & Rationale

| Decision | Rationale |
|---|---|
| Store user data (My Data) alongside catalog data in one `shows` table | Simpler queries; user data is the primary access pattern; merge rules handle conflicts |
| Transient data not persisted | Cast/credits/seasons/images change frequently; re-fetching ensures freshness; reduces storage |
| AI API keys server-only | Security requirement from infra rider; client never sees elevated keys |
| Streaming for Scoop and Ask | UX requirement: "user sees Generating... not a blank wait"; progressive rendering |
| Namespace + user_id composite partition | Required by infra rider for build isolation and multi-user readiness |
| Dev identity injection via header | Fastest benchmark iteration; no OAuth flow needed; documented for production swap |
| SWR/React Query for client cache | Server is truth; cache is disposable; automatic revalidation aligns with "cache is disposable" rule |

---

## 10. File Structure — Key Modules

```
src/
├── config/
│   ├── env.ts                          # Environment variable access
│   └── constants.ts                    # Status types, interest levels, limits
├── theme/
│   └── tokens.ts                       # Design tokens (colors, spacing, fonts)
├── types/
│   └── show.ts                         # Show, MyStatusType, MyInterestType, FilterType, etc.
├── lib/
│   ├── supabase/
│   │   ├── client.ts                   # Browser client
│   │   ├── server.ts                   # Server client with namespace/user context
│   │   └── queries/
│   │       ├── shows.ts                # Show CRUD + filters
│   │       ├── settings.ts             # Cloud settings CRUD
│   │       └── metadata.ts             # App metadata
│   ├── catalog/
│   │   ├── client.ts                   # External catalog HTTP client
│   │   └── mapper.ts                   # Catalog response → Show type
│   └── ai/
│       ├── client.ts                   # LLM API client with streaming
│       ├── prompts/
│       │   ├── scoop.ts                # Scoop prompt template
│       │   ├── ask.ts                  # Ask prompt template
│       │   ├── concepts.ts             # Concept generation prompt
│       │   └── recommendations.ts      # Concept-based rec prompt
│       └── parsers/
│           ├── showListParser.ts       # Parse "Title::id::type;;" format
│           └── conceptParser.ts        # Parse concept bullet list
├── utils/
│   ├── mergeRules.ts                   # Show merge/overwrite policy
│   ├── autoSaveRules.ts               # Saving trigger logic + defaults
│   ├── exportBackup.ts                # ZIP export logic
│   └── dateUtils.ts                   # Date formatting, freshness checks
├── components/                         # Shared UI primitives (see §2.2)
├── hooks/
│   ├── useNamespace.ts                 # Current namespace context
│   ├── useUser.ts                      # Current user context (dev injection)
│   └── useSettings.ts                  # Cloud + local settings
└── app/                                # Next.js App Router
    ├── layout.tsx                      # Root layout with providers
    ├── page.tsx                        # Home (Collection)
    ├── find/
    │   └── page.tsx                    # Find hub
    ├── detail/
    │   └── [id]/
    │       └── page.tsx                # Show Detail
    ├── person/
    │   └── [id]/
    │       └── page.tsx                # Person Detail
    ├── settings/
    │   └── page.tsx                    # Settings
    └── api/
        ├── catalog/
        │   ├── search/route.ts
        │   ├── show/[id]/route.ts
        │   └── person/[id]/route.ts
        ├── shows/
        │   ├── route.ts               # List + Create
        │   └── [id]/
        │       ├── route.ts           # Get + Update + Delete
        │       ├── status/route.ts
        │       ├── rate/route.ts
        │       └── tags/route.ts
        ├── ai/
        │   ├── ask/route.ts
        │   ├── scoop/[id]/route.ts
        │   ├── concepts/route.ts
        │   └── recommendations/route.ts
        ├── settings/route.ts
        └── export/route.ts
```

---

## 11. Acceptance Criteria

The implementation is complete when:

1. **Infrastructure:** App runs via `npm run dev`, configurable via `.env`, tests via `npm test`, namespace-scoped reset via `npm run test:reset`
2. **Collection:** Users can search catalog, save shows (with correct auto-save triggers and defaults), organize by status/interest/tags/rating, and browse via filters
3. **AI Discovery:** Ask chat works with streaming, mentioned shows render, Scoop generates and caches, Alchemy full flow works, Explore Similar works from Detail
4. **Data Integrity:** Merge rules correct, re-add preserves My Data, removal clears all user data, timestamps track all modifications
5. **Isolation:** Namespace isolation verified, user_id on all records, destructive tests scoped to namespace
6. **Export:** "Export My Data" produces valid zip with JSON
7. **Auth-ready:** Dev identity injection works and is documented; schema supports future OAuth without redesign
8. **Persona:** AI voice is consistent across all surfaces — warm, opinionated, specific, spoiler-safe
