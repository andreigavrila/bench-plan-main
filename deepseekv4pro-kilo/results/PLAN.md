# Implementation Plan — Personal TV & Movie Companion

## 1. Technology Foundation

### 1.1 Stack
| Layer | Technology |
|-------|-----------|
| Runtime | Next.js (latest stable) — App Router, server components + client components |
| Persistence | Supabase (hosted preferred; local optional) via `@supabase/supabase-js` |
| Styling | CSS Modules or Tailwind CSS (theme tokens from `src/theme/`) |
| AI | OpenAI-compatible chat/completions API; provider key configured via env |
| Testing | Vitest + React Testing Library; Playwright for E2E (optional) |

### 1.2 Environment Configuration
- `.env.example` — all required variables with comments:
  - `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY` (client-safe anon key)
  - `SUPABASE_SERVICE_ROLE_KEY` (server-only, never exposed to client)
  - `NAMESPACE_ID` — build isolation identifier
  - `USER_ID` — default dev user identity
  - `AI_PROVIDER_URL`, `AI_API_KEY`, `AI_MODEL` — AI provider configuration
  - `CATALOG_API_KEY` — external catalog provider (e.g., TMDB)
- `.gitignore` excludes `.env*` except `.env.example`
- All source code references config via `src/config/` constants, never raw env vars

### 1.3 One-Command DX
| Command | Purpose |
|---------|---------|
| `npm run dev` | Start Next.js dev server |
| `npm test` | Run unit/integration tests |
| `npm run test:reset` | Reset test data for the current namespace |

### 1.4 Database
- Migrations in `supabase/migrations/` — repeatable, ordered schema definitions
- Optional seed data in `supabase/seed/` for dev convenience
- Schema evolution tracked via `dataModelVersion` in `AppMetadata`

---

## 2. Identity & Isolation Architecture

### 2.1 Namespace Isolation (`namespace_id`)
- Every persisted record scoped to `namespace_id` (a stable string, injected via env or dev selector)
- Two namespaces cannot read/write each other's data
- Destructive testing (`npm run test:reset`) deletes only records within the current namespace
- Implemented via: appending `namespace_id` column to all user-data tables; RLS policies filter by it; or using Supabase row-level security on a namespace column

### 2.2 User Identity (`user_id`)
- All user-owned records (shows, settings) carry `user_id` (opaque stable string / UUID)
- In benchmark mode: dev identity injection — accept `X-User-Id` header in dev/test, or use fixed `USER_ID` env var
- Designed so migrating to real OAuth (Google) later requires only auth wiring changes, not schema redesign
- Within a namespace, multiple users may exist; effective partition is `(namespace_id, user_id)`

### 2.3 Data Ownership
- Server-side (Supabase) is the source of truth
- Client may cache for performance but clearing local storage must not lose data
- No offline-first requirement

---

## 3. Directory Structure (Fractal Architecture)

Following the guidelines in `INSTRUCTIONS.md`:

```
src/
├── config/                  # Global constants, env var accessors
│   ├── env.ts               # Typed env var access
│   └── constants.ts         # Limits, defaults, magic numbers
├── theme/                   # Design tokens
│   ├── tokens.css / tokens.ts
│   └── fonts.ts
├── components/              # Shared UI primitives (no page-level logic)
│   ├── ShowTile/
│   │   ├── ShowTile.tsx
│   │   └── hooks/
│   ├── StatusChips/
│   ├── RatingBar/
│   ├── TagPicker/
│   ├── ConceptChips/
│   ├── MediaTypeToggle/
│   ├── ModeSwitcher/
│   ├── SearchInput/
│   ├── ChatBubble/
│   ├── StreamingIndicator/
│   └── ...
├── hooks/                   # Global hooks
│   ├── useNamespace.ts      # Read current namespace_id
│   ├── useUserId.ts         # Read current user_id
│   └── useMediaQuery.ts
├── utils/                   # Global pure functions
│   ├── iso8601.ts           # Date formatting
│   ├── mergeShow.ts         # Show merge logic (catalog + user overlay)
│   ├── parseMentionedShows.ts
│   ├── catalog/             # External catalog adapter
│   │   ├── search.ts
│   │   ├── getShow.ts
│   │   ├── getPerson.ts
│   │   ├── decodeShow.ts    # External payload → internal Show shape
│   │   └── constants.ts     # Base URLs, image URL builders
│   └── supabase/            # DB client + query helpers
│       ├── client.ts        # Browser client (anon key)
│       ├── server.ts        # Server client (service role key)
│       ├── shows.ts         # CRUD for shows
│       ├── settings.ts      # CRUD for cloud settings
│       └── migrations.ts    # App metadata / version checks
├── ai/                      # AI prompt assembly & response parsing
│   ├── prompts/             # Prompt templates per surface
│   │   ├── scoops.ts
│   │   ├── ask.ts           # General chat + Ask About Show
│   │   ├── concepts.ts      # Single-show + multi-show concept generation
│   │   ├── recommendations.ts  # Explore Similar + Alchemy recs
│   │   └── summarize.ts     # Conversation summarization
│   ├── parsers/             # Structured output parsers
│   │   ├── parseMentionedShows.ts
│   │   ├── parseConcepts.ts
│   │   └── parseRecommendations.ts
│   ├── client.ts            # AI provider HTTP client
│   └── voice.ts             # Persona constants, tone sliders
└── pages/                   # Next.js App Router pages
    ├── layout.tsx            # Root layout (nav + main content area)
    ├── page.tsx              # Home / Collection
    ├── settings/
    │   └── page.tsx
    ├── detail/
    │   └── [id]/
    │       └── page.tsx
    ├── person/
    │   └── [id]/
    │       └── page.tsx
    └── find/
        ├── page.tsx          # Find hub (mode switcher)
        ├── features/
        │   ├── Search/
        │   │   ├── Search.tsx
        │   │   ├── hooks/
        │   │   └── features/
        │   │       └── SearchResults/
        │   ├── Ask/
        │   │   ├── Ask.tsx
        │   │   ├── hooks/
        │   │   │   ├── useAskChat.ts
        │   │   │   └── useAskContext.ts
        │   │   └── features/
        │   │       ├── ChatThread/
        │   │       ├── MentionedShows/
        │   │       └── StarterPrompts/
        │   └── Alchemy/
        │       ├── Alchemy.tsx
        │       ├── hooks/
        │       │   ├── useAlchemyFlow.ts
        │       │   └── useAlchemyState.ts
        │       └── features/
        │           ├── ShowSelector/
        │           ├── ConceptSelector/
        │           ├── AlchemyResults/
        │           └── ChainControls/
        └── (shared hooks)
            └── useModeSwitcher.ts
```

### Home / Collection page
```
src/pages/home/
├── page.tsx
└── features/
    ├── CollectionHome/
    │   ├── CollectionHome.tsx
    │   ├── hooks/
    │   │   ├── useCollection.ts      # Fetch + filter + sort
    │   │   └── useCollectionFilters.ts
    │   └── features/
    │       ├── StatusSections/
    │       │   ├── StatusSections.tsx
    │       │   ├── hooks/
    │       │   └── features/
    │       │       ├── ActiveSection/
    │       │       ├── ExcitedSection/
    │       │       ├── InterestedSection/
    │       │       └── OtherStatusesSection/
    │       ├── MediaTypeToggle/
    │       └── EmptyStates/
    └── FilterPanel/
        ├── FilterPanel.tsx
        ├── hooks/
        │   ├── useTagFilters.ts
        │   └── useDataFilters.ts
        └── features/
            ├── TagFilters/
            ├── GenreFilters/
            ├── DecadeFilters/
            └── CommunityScoreFilters/
```

### Show Detail page
```
src/pages/detail/[id]/
├── page.tsx
└── features/
    ├── DetailShell/
    │   ├── DetailShell.tsx
    │   ├── hooks/
    │   │   ├── useDetailShow.ts     # Fetch + merge show data
    │   │   ├── useSaveTriggers.ts   # Auto-save logic
    │   │   └── useRemovalConfirm.ts
    │   └── features/
    │       ├── HeaderCarousel/      # Backdrops, posters, logos, videos
    │       ├── CoreFacts/           # Year, runtime/seasons, community score
    │       ├── StatusControls/      # Status/interest chips in toolbar
    │       ├── RatingControls/      # Rating slider
    │       ├── TagControls/         # Tag display + picker
    │       ├── OverviewSection/     # Overview text
    │       ├── ScoopSection/        # AI Scoop generation + streaming
    │       ├── AskAboutShow/        # CTA → Ask with show context
    │       ├── GenresLanguages/
    │       ├── TraditionalRecs/     # Similar/recommended strand
    │       ├── ExploreSimilar/      # Get Concepts → select → Explore Shows
    │       │   ├── ExploreSimilar.tsx
    │       │   ├── hooks/
    │       │   │   ├── useConcepts.ts
    │       │   │   └── useExploreRecs.ts
    │       │   └── features/
    │       │       ├── ConceptChips/
    │       │       └── ExploreResults/
    │       ├── StreamingSection/    # Provider availability
    │       ├── CastCrewSection/     # Horizontal strands → Person Detail
    │       ├── SeasonsSection/      # TV only
    │       └── BudgetRevenueSection/ # Movies when available
```

### Person Detail page
```
src/pages/person/[id]/
├── page.tsx
└── features/
    └── PersonShell/
        ├── PersonShell.tsx
        ├── hooks/
        │   └── usePersonData.ts
        └── features/
            ├── ImageGallery/
            ├── BioSection/
            ├── AnalyticsCharts/    # Ratings, genres, projects-by-year
            └── Filmography/        # Grouped by year
```

---

## 4. Data Model

### 4.1 Supabase Tables

#### `shows`
Primary table. Columns map to the `Show` interface from `storage-schema.ts`.

| Column | Type | Notes |
|--------|------|-------|
| `id` | `text` | Primary key (catalog ID) |
| `namespace_id` | `text` | Build isolation |
| `user_id` | `text` | User identity |
| `title` | `text` | Not null |
| `show_type` | `text` | `'movie' | 'tv' | 'person' | 'unknown'` |
| `external_ids` | `jsonb` | `Record<string, string>` |
| `overview` | `text` | nullable |
| `genres` | `jsonb` | `string[]` |
| `tagline` | `text` | nullable |
| `homepage` | `text` | nullable |
| `original_language` | `text` | nullable |
| `spoken_languages` | `jsonb` | `string[]` |
| `languages` | `jsonb` | `string[]` |
| `poster_url` | `text` | nullable |
| `backdrop_url` | `text` | nullable |
| `logo_url` | `text` | nullable |
| `network_logos` | `jsonb` | `string[]` |
| `vote_average` | `float8` | nullable |
| `vote_count` | `int` | nullable |
| `popularity` | `float8` | nullable |
| `last_air_date` | `timestamptz` | nullable |
| `first_air_date` | `timestamptz` | nullable |
| `release_date` | `timestamptz` | nullable |
| `runtime` | `int` | nullable |
| `budget` | `int` | nullable |
| `revenue` | `int` | nullable |
| `series_status` | `text` | nullable |
| `number_of_episodes` | `int` | nullable |
| `number_of_seasons` | `int` | nullable |
| `episode_run_time` | `jsonb` | `int[]` |
| `my_tags` | `jsonb` | `string[]` |
| `my_tags_update_date` | `timestamptz` | nullable |
| `my_score` | `float8` | nullable |
| `my_score_update_date` | `timestamptz` | nullable |
| `my_status` | `text` | `'active' | 'next' | 'later' | 'done' | 'quit' | 'wait'` |
| `my_status_update_date` | `timestamptz` | nullable |
| `my_interest` | `text` | `'excited' | 'interested'` |
| `my_interest_update_date` | `timestamptz` | nullable |
| `ai_scoop` | `text` | nullable |
| `ai_scoop_update_date` | `timestamptz` | nullable |
| `details_update_date` | `timestamptz` | nullable |
| `creation_date` | `timestamptz` | nullable |
| `is_test` | `boolean` | default false |
| `provider_data` | `jsonb` | `ProviderData` shape |

**Composite primary key**: `(id, namespace_id, user_id)` or separate UUID pk with unique constraint on `(id, namespace_id, user_id)`.

**Row-Level Security (RLS)**: Policies ensure queries are scoped to `(namespace_id, user_id)`.

#### `cloud_settings`
| Column | Type | Notes |
|--------|------|-------|
| `id` | `text` | default `'globalSettings'` |
| `namespace_id` | `text` | |
| `user_id` | `text` | |
| `user_name` | `text` | |
| `version` | `float8` | epoch seconds for conflict resolution |
| `catalog_api_key` | `text` | nullable |
| `ai_api_key` | `text` | nullable |
| `ai_model` | `text` | |

#### `app_metadata`
| Column | Type | Notes |
|--------|------|-------|
| `key` | `text` | e.g. `'dataModelVersion'` |
| `namespace_id` | `text` | |
| `value` | `text` | |

### 4.2 Key Business Rules (Implementation Contracts)

#### Collection Membership
A show is "in collection" when `my_status IS NOT NULL`.

#### Auto-Save Triggers
| Action on unsaved show | Default Status | Default Interest |
|------------------------|---------------|-----------------|
| Set any status | The chosen status | `interested` (if Later) |
| Select Interested/Excited chip | `later` | `interested` / `excited` |
| Rate | `done` | — |
| Add tag | `later` | `interested` |

#### Removal
- Clearing status → confirmation prompt → delete row (or set all my* fields to null, delete row preferred for cleanliness)
- All My Data cleared: status, interest, tags, rating, AI Scoop
- Warning confirmation with "don't ask again" option (tracked via `hideStatusRemovalConfirmation`)

#### Merge Policy
- **Non-my fields** (catalog data): `selectFirstNonEmpty(new, old)` — never overwrite non-empty with empty
- **My fields**: resolve by timestamp — newer `_update_date` wins
- `detailsUpdateDate` set to now on merge
- `creationDate` set only on first creation

#### AI Data Persistence
| Data | Persisted | Freshness |
|------|-----------|-----------|
| AI Scoop | Yes (if in collection) | 4 hours |
| Alchemy results/reasons | No (session only) | — |
| Ask chat history | No (session only) | — |
| Mentioned shows | No (session only) | — |

---

## 5. AI Architecture

### 5.1 Provider Integration
- `src/ai/client.ts` — thin wrapper around AI provider API
- Supports streaming responses for Scoop and Ask
- Configurable model via `AI_MODEL` env var
- Prompt assembly in `src/ai/prompts/` — one file per surface

### 5.2 Shared AI Rules (All Surfaces)
- Domain-bounded: stay within TV/movies; redirect if asked outside
- Spoiler-safe by default; spoilers allowed only when user explicitly requests
- Opinionated and honest; acknowledge mixed reception
- Prefer vibe/structure/craft reasoning over generic genre summaries

### 5.3 Surface Implementations

#### 5.3.1 Ask (Chat) — `src/pages/find/features/Ask/`
- Chat UI with user/assistant turns
- Context includes: user library (saved shows + My Data), recent conversation turns
- After ~10 messages, summarize older turns (1–2 sentences, preserving persona)
- Mentioned shows extracted via structured output:
  - Response includes `commentary` (user-facing text) + `showList` (machine-readable)
  - `showList` format: `Title::externalId::mediaType;;Title2::externalId::mediaType`
  - Parser: `src/ai/parsers/parseMentionedShows.ts`
  - Failed parsing → retry once with stricter formatting → fallback to Search handoff
- Welcome view: 6 random starter prompts (refreshed on demand)
- **Ask About a Show**: launched from Detail → seeds Ask context with show data
- Persona: low-friction, fast, fun; 1–3 tight paragraphs + bulleted list for recs

#### 5.3.2 AI Scoop — `src/pages/detail/[id]/features/DetailShell/features/ScoopSection/`
- Generated on demand via "Give me the scoop!" toggle
- Structured as mini blog post: personal take → stack-up → Scoop paragraph (centerpiece) → fit/warnings → verdict
- Target length: ~150–350 words
- Streams progressively (no blank wait)
- 4-hour cache: check `aiScoopUpdateDate`, regenerate if expired
- Freshness check: if `aiScoopUpdateDate` < 4 hours ago, show cached; else fetch new
- Persisted only if show is in collection; ephemeral otherwise
- Persona: gossipy, vivid, useful

#### 5.3.3 Get Concepts (Single-Show) — `src/ai/prompts/concepts.ts`
- Input: show catalog data
- Output: bullet list of 1–3 word evocative concepts
- Rules: no plot/spoilers, no generic concepts ("good characters", "great story"), varied across axes (structure, vibe, emotion, craft), ordered by strength
- Default: 8 concepts

#### 5.3.4 Get Concepts (Multi-Show, Alchemy) — `src/ai/prompts/concepts.ts`
- Input: 2+ show catalog data objects
- Output: bullet list of concepts shared across all input shows
- Same quality rules as single-show; larger pool of options

#### 5.3.5 Concept-Based Recommendations (Explore Similar) — `src/ai/prompts/recommendations.ts`
- Input: selected concepts, current show, user library
- Output: 5 recommended shows with concise reasons
- Each reason must explicitly reference which concept(s) it aligns with
- Reasons: ~1–3 sentences, taste-aware, not synopses
- Results must resolve to real catalog items (external IDs required)
- Fallback: non-resolvable recs → non-interactive display + Search handoff

#### 5.3.6 Concept-Based Recommendations (Alchemy) — `src/ai/prompts/recommendations.ts`
- Input: selected concepts, input shows, user library
- Output: 6 recommended shows with concise reasons
- Same quality bar as Explore Similar

### 5.4 Voice & Persona
- Consistent persona across all AI surfaces: "fun, chatty TV/movie nerd friend"
- Tone: 70% friend / 30% critic; 60% hype / 40% measured; adaptive playful↔serious
- Search has no AI voice — straightforward catalog search only

---

## 6. Feature Implementation Order

### Phase 1: Foundation
1. **Scaffold Next.js + Supabase**
   - `npm create next-app` with App Router
   - Install `@supabase/supabase-js`, set up clients (`src/utils/supabase/`)
2. **Environment config** (`src/config/env.ts`, `.env.example`, `.gitignore`)
3. **Database migrations** — schema for `shows`, `cloud_settings`, `app_metadata`
4. **Namespace + User identity** plumbing (`src/hooks/useNamespace.ts`, `useUserId.ts`)
5. **Theme tokens** (`src/theme/`)
6. **External catalog adapter** (`src/utils/catalog/`) — search, getShow, getPerson, image URL builders

### Phase 2: Core Data Operations
7. **Show CRUD + merge logic** (`src/utils/supabase/shows.ts`, `mergeShow.ts`)
8. **Cloud settings CRUD** (`src/utils/supabase/settings.ts`)
9. **App metadata / data model versioning**

### Phase 3: Navigation & Layout
10. **Root layout** — nav with FilterPanel sidebar + main content area
11. **FilterPanel** — All Shows, tag filters, genre/decade/community score filters
12. **Global navigation** — Home, Find/Discover, Settings entry points

### Phase 4: Collection Home
13. **CollectionHome** — fetch filtered shows, group by status sections
14. **StatusSections** — Active (prominent), Excited, Interested, Other (collapsed: Wait, Quit, Done, unclassified Later)
15. **MediaTypeToggle** — All / Movies / TV
16. **Empty states** — no collection → prompt Search/Ask; no filter results → "No results found"

### Phase 5: Show Detail Page
17. **DetailShell** — fetch show (catalog + overlay), merge, display
18. **Header carousel** — backdrops, posters, logos, trailers
19. **Core facts** — year, runtime/seasons, community score
20. **Status controls** — status chips; reselect confirms removal
21. **Rating bar** — rating slider; auto-save unsaved as Done
22. **Tag controls** — tag display + picker; auto-save unsaved as Later+Interested
23. **Overview + Scoop** — overview text, Scoop section (generate/stream/cache)
24. **Show tile components** — poster + title + collection badge + rating badge (reusable across app)
25. **Traditional recommendations** — similar/recommended strand
26. **Explore Similar** — Get Concepts → select → Explore Shows
27. **Genres / Languages / Streaming / CastCrew / Seasons / BudgetRevenue** sections

### Phase 6: Find/Discover Hub
28. **Find hub page** — mode switcher (Search / Ask / Alchemy)
29. **Search** — text search → poster grid → Detail; in-collection indicators; Search on Launch setting
30. **Ask** — chat UI, context injection, mentioned shows strip, starter prompts
31. **Ask About Show** — seed context from Detail
32. **Alchemy** — show selection (2+ from library + catalog) → Conceptualize → select concepts (max 8) → Alchemize → results → chain

### Phase 7: Person Detail
33. **PersonShell** — image gallery, bio, analytics charts, filmography grouped by year
34. **Credit links** — tap credit → navigate to Show Detail

### Phase 8: Settings & Data Management
35. **Settings page** — font size, search on launch, username, AI provider/model config, catalog API key
36. **Export My Data** — produce `.zip` with JSON backup of all saved shows + My Data (ISO-8601 dates)
37. **Data continuity** — on app load, check `dataModelVersion`; if schema version changed, run migration to bring existing shows forward

### Phase 9: Testing & Polish
38. **Unit tests** — merge logic, parsing, business rules, auto-save triggers
39. **Integration tests** — CRUD operations, filter behavior
40. **Test reset** (`npm run test:reset`) — delete all records in current namespace
41. **RLS verification** — namespace/user isolation working correctly
42. **AI fallback handling** — parsing failures, unresolvable shows

---

## 7. API Route Design

### 7.1 Server Routes (Next.js API Routes / Server Actions)

| Route | Method | Purpose | Auth |
|-------|--------|---------|------|
| `/api/shows` | GET | List shows for user (optional filters) | `(namespace, user)` |
| `/api/shows/[id]` | GET | Get single show (merged catalog + user data) | `(namespace, user)` |
| `/api/shows/[id]` | PUT | Save/update show (My Data fields) | `(namespace, user)` |
| `/api/shows/[id]` | DELETE | Remove show from collection | `(namespace, user)` |
| `/api/shows/export` | GET | Export all saved shows as JSON | `(namespace, user)` |
| `/api/catalog/search` | GET | Proxy search to external catalog | `(namespace)` |
| `/api/catalog/shows/[id]` | GET | Proxy show fetch from external catalog | `(namespace)` |
| `/api/catalog/people/[id]` | GET | Proxy person fetch from external catalog | `(namespace)` |
| `/api/ai/ask` | POST | Ask chat (streaming) | `(namespace, user)` |
| `/api/ai/scoop` | POST | Generate Scoop for a show (streaming) | `(namespace, user)` |
| `/api/ai/concepts` | POST | Generate concepts (single or multi-show) | `(namespace, user)` |
| `/api/ai/recommendations` | POST | Generate concept-based recommendations | `(namespace, user)` |
| `/api/settings` | GET/PUT | Cloud settings | `(namespace, user)` |

### 7.2 Identity Injection (Benchmark Mode)
- Server routes read `X-User-Id` header in dev/test
- Server reads `NAMESPACE_ID` from env
- Production mode: header acceptance gated behind `NODE_ENV !== 'production'`
- All queries append `WHERE namespace_id = $1 AND user_id = $2`

### 7.3 AI Routes — Context Assembly
- All AI routes assemble context from the user's library (saved shows + My Data)
- Ask routes include recent conversation turns; auto-summarize after ~10 messages
- Scoop route includes full show catalog data
- Concepts route includes catalog data for 1+ shows
- Recommendations route includes selected concepts + user library

---

## 8. Schema Evolution & Data Continuity

### 8.1 Version Tracking
- `app_metadata` table stores `dataModelVersion`
- On app startup, compare stored version with current expected version
- If stored < current: run migration logic

### 8.2 Migration Strategy
- Sequential migrations: v1→v2, v2→v3, etc.
- Each migration: read all shows for the namespace/user, transform fields, write back
- Non-destructive: existing data is preserved, new fields get defaults, removed fields are handled gracefully
- Migration runs on server-side (route handler or startup script)

---

## 9. Export / Backup

### 9.1 Export Format
- All saved shows for `(namespace_id, user_id)` serialized as JSON
- Dates in ISO-8601 format
- Packaged in a `.zip` file
- Download initiated from Settings → "Export My Data"

### 9.2 Import (Future)
- Not required for current implementation
- Designed so JSON export format supports future import

---

## 10. Testing Strategy

### 10.1 Isolation
- All tests use a distinct `NAMESPACE_ID`
- `npm run test:reset` deletes all rows in all tables for that namespace
- Supabase RLS policies already scope queries to namespace; tests verify this

### 10.2 Test Categories
| Category | Tool | What |
|----------|------|------|
| Unit | Vitest | Merge logic, parsing, date formatting, business rule functions |
| Integration | Vitest + Supabase local | CRUD operations, filter queries, export |
| E2E (optional) | Playwright | Full user journeys |

### 10.3 Key Business Logic Tests
- Auto-save triggers (status, interest, rating, tag) and default values
- Removal flow (confirmation, data cleared)
- Merge policy (non-my: selectFirstNonEmpty; my: timestamp resolution)
- Timestamp updates on field changes
- Collection membership definition (`my_status IS NOT NULL`)
- Mentioned shows parsing (success, failure, retry, fallback)
- AI Scoop cache freshness (within 4h: cached; after 4h: regenerate)

---

## 11. Cross-Cutting Concerns

### 11.1 Secrets
- `.env*` files (except `.env.example`) in `.gitignore`
- Client code uses `NEXT_PUBLIC_SUPABASE_ANON_KEY` only
- Server code uses `SUPABASE_SERVICE_ROLE_KEY`, never exposed
- AI API keys: server-side only; optional setting for user-provided keys stored server-side

### 11.2 Performance
- Show tiles use Next.js `Image` component for optimized poster/backdrop loading
- AI responses stream via SSE for progressive rendering
- Client-side caching of catalog data (React Query / SWR)
- No offline-first requirement; cache is disposable

### 11.3 Accessibility
- Keyboard navigation for status chips, rating slider, concept selection
- Semantic HTML (proper headings, landmarks)
- Color contrast meets WCAG AA

---

## 12. Open Questions (PRD §10 — Deferred Decisions)

The following are noted as open per the PRD and are NOT part of the current implementation scope:
1. Should **Next** become a first-class status in UI?
2. Should users create **named custom lists** beyond tags?
3. Should generating **AI Scoop** on an unsaved show implicitly save it?
4. Should clearing My Rating store an explicit **Unrated** state vs nil?
5. Add **Import/Restore** from export zip
6. Support saving/sharing **Alchemy sessions** as reusable blends
7. Add explicit **myStatus filters** in sidebar

---

## 13. Out of Scope (PRD §11)

- Detailed caching/offline strategy beyond current freshness rules
- Low-level migration internals beyond version tracking + transform
- Vendor-specific API integration specs (provider-specific implementation)
- UI animation/micro-interaction prescriptions
- Full social or community features
