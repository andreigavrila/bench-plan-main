# Implementation Plan: Personal TV/Movie Companion App

## Executive Summary

This plan outlines the implementation of a personal TV and movie companion application that enables users to collect, organize, rate, and discover entertainment through both traditional browsing and AI-powered discovery mechanisms. The app centers on making user taste visible and actionable through a personal library with rich metadata overlays (status, interest, tags, ratings, AI-generated insights) and multiple discovery paths (search, conversational AI, concept-based "Alchemy" blending, and per-show exploration).

The implementation follows a benchmark-friendly architecture using Next.js for the application runtime and Supabase for persistence, with strict namespace isolation for build/run separation and user_id scoping for all persisted data.

---

## 1. Architecture Overview

### 1.1 Technology Stack

**Frontend + Server Boundary:**
- Next.js (latest stable) — React framework providing SSR/SSG capabilities, API routes for server-side operations, and client-side interactivity
- TypeScript — Type safety across the entire codebase
- Tailwind CSS or equivalent — Utility-first styling system aligned with theme tokens

**Persistence Layer:**
- Supabase — Hosted PostgreSQL database with official client libraries
- Row Level Security (RLS) — Data isolation by namespace_id and user_id
- Database migrations — Repeatable schema evolution via migration files

**AI Integration:**
- Pluggable AI provider interface — Abstract provider selection behind configuration
- Environment-injected API keys — No hardcoded secrets; keys provided via .env
- Structured output parsing — Deterministic parsing of AI responses for show mentions and recommendations

**External Catalog:**
- Pluggable catalog provider interface — Abstract catalog source (e.g., TMDB) behind configuration
- Provider ID mapping — Store provider IDs for streaming availability; resolve to full provider metadata as needed

### 1.2 Fractal Feature Architecture

Following the INSTRUCTIONS.md guidelines, the app uses a fractal architecture where pages contain features, and features contain sub-features, each self-contained with their own hooks, utils, and child components.

```
src/
├── config/                    # Global constants, env vars, type definitions
│   ├── env.ts                 # Environment variable validation and access
│   ├── constants.ts           # App-wide constants (statuses, interests, etc.)
│   └── types.ts               # Shared TypeScript interfaces
├── theme/                     # Design tokens and styling system
│   ├── colors.ts              # Color palette
│   ├── spacing.ts             # Spacing scale
│   ├── typography.ts          # Font sizes, weights, line heights
│   └── index.ts               # Theme composition
├── components/                # Shared UI primitives (buttons, cards, modals, etc.)
│   ├── Button/
│   │   └── Button.tsx
│   ├── Card/
│   │   └── Card.tsx
│   ├── Modal/
│   │   └── Modal.tsx
│   ├── Chip/
│   │   └── Chip.tsx
│   ├── RatingSlider/
│   │   └── RatingSlider.tsx
│   └── ...
├── hooks/                     # Global hooks (auth, api, settings)
│   ├── useAuth.ts             # Identity injection / auth context
│   ├── useApi.ts              # API client wrapper
│   └── useSettings.ts         # Cloud/local settings management
├── utils/                     # Global pure functions
│   ├── dateUtils.ts           # Date formatting and parsing
│   ├── mergeUtils.ts          # Show merge logic (catalog refresh)
│   ├── aiParser.ts            # Structured AI output parsing
│   └── exportUtils.ts         # Data export (JSON → zip)
├── lib/                       # Business logic layer (non-UI)
│   ├── supabase/              # Supabase client and query builders
│   │   ├── client.ts          # Supabase client initialization
│   │   ├── shows.ts           # Show CRUD operations
│   │   ├── settings.ts        # Settings CRUD
│   │   └── rls.ts             # RLS policy helpers
│   ├── catalog/               # External catalog integration
│   │   ├── types.ts           # Catalog response types
│   │   ├── mapper.ts          # Catalog → Show mapping
│   │   └── providers/         # Catalog provider implementations
│   ├── ai/                    # AI service integration
│   │   ├── types.ts           # AI request/response types
│   │   ├── prompts.ts         # Prompt templates (surface-specific)
│   │   ├── client.ts          # AI provider client
│   │   └── services/          # Surface-specific AI services
│   │       ├── scoopService.ts
│   │       ├── askService.ts
│   │       ├── conceptService.ts
│   │       └── recommendationService.ts
│   └── export/                # Data export functionality
│       ├── exporter.ts        # JSON serialization
│       └── zipBuilder.ts      # Zip file creation
└── pages/                     # Top-level routes
    ├── Home/                  # Collection home page
    │   ├── Home.tsx
    │   └── features/
    │       ├── FilterSidebar/
    │       │   ├── FilterSidebar.tsx
    │       │   ├── hooks/
    │       │   │   └── useFilters.ts
    │       │   └── features/
    │       │       ├── TagFilters/
    │       │       ├── GenreFilters/
    │       │       ├── DecadeFilters/
    │       │       └── ScoreFilters/
    │       ├── ShowGrid/
    │       │   ├── ShowGrid.tsx
    │       │   └── features/
    │       │       ├── StatusSection/
    │       │       └── ShowTile/
    │       └── MediaTypeToggle/
    │           └── MediaTypeToggle.tsx
    ├── Detail/                # Show detail page
    │   ├── Detail.tsx
    │   └── features/
    │       ├── HeaderMedia/
    │       │   ├── HeaderMedia.tsx
    │       │   └── hooks/
    │       │       └── useMediaCarousel.ts
    │       ├── CoreFacts/
    │       │   └── CoreFacts.tsx
    │       ├── MyRelationshipControls/
    │       │   ├── MyRelationshipControls.tsx
    │       │   ├── hooks/
    │       │   │   └── useMyData.ts
    │       │   └── features/
    │       │       ├── StatusChips/
    │       │       ├── RatingBar/
    │       │       └── TagPicker/
    │       ├── OverviewAndScoop/
    │       │   ├── OverviewAndScoop.tsx
    │       │   └── hooks/
    │       │       └── useScoop.ts
    │       ├── Recommendations/
    │       │   └── Recommendations.tsx
    │       ├── ExploreSimilar/
    │       │   ├── ExploreSimilar.tsx
    │       │   ├── hooks/
    │       │   │   └── useConcepts.ts
    │       │   └── features/
    │       │       ├── ConceptSelector/
    │       │       └── ConceptRecs/
    │       ├── StreamingProviders/
    │       │   └── StreamingProviders.tsx
    │       ├── CastAndCrew/
    │       │   ├── CastAndCrew.tsx
    │       │   └── features/
    │       │       ├── PersonCard/
    │       │       └── CreditList/
    │       ├── SeasonsList/
    │       │   └── SeasonsList.tsx
    │       └── BudgetRevenue/
    │           └── BudgetRevenue.tsx
    ├── Find/                  # Discovery hub
    │   ├── Find.tsx
    │   └── features/
    │       ├── ModeSwitcher/
    │       │   └── ModeSwitcher.tsx
    │       ├── Search/
    │       │   ├── Search.tsx
    │       │   └── hooks/
    │       │       └── useSearch.ts
    │       ├── Ask/
    │       │   ├── Ask.tsx
    │       │   ├── hooks/
    │       │   │   └── useAskChat.ts
    │       │   └── features/
    │       │       ├── ChatMessages/
    │       │       ├── MentionedShows/
    │       │       └── StarterPrompts/
    │       └── Alchemy/
    │           ├── Alchemy.tsx
    │           ├── hooks/
    │           │   └── useAlchemy.ts
    │           └── features/
    │               ├── InputShowSelector/
    │               ├── ConceptCatalysts/
    │               └── AlchemyResults/
    ├── Person/                # Person detail page
    │   ├── Person.tsx
    │   └── features/
    │       ├── PersonHeader/
    │       ├── AnalyticsCharts/
    │       ├── Filmography/
    │       └── ImageGallery/
    └── Settings/              # Settings page
        ├── Settings.tsx
        └── features/
            ├── AppSettings/
            ├── AISettings/
            ├── IntegrationSettings/
            └── DataExport/
```

### 1.3 Data Flow Principles

1. **Backend is source of truth** — All user-owned data persists in Supabase; client cache is disposable
2. **Namespace isolation** — Every query includes namespace_id scope via RLS policies
3. **User scoping** — Every user-owned record includes user_id; queries filter by (namespace_id, user_id)
4. **Optimistic UI** — Local state updates immediately; background sync to server
5. **Merge-on-refresh** — Catalog data merges with stored shows using timestamp-based conflict resolution

---

## 2. Database Schema & Persistence

### 2.1 Tables

#### `namespaces`
Tracks build/run isolation boundaries.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Namespace identifier |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT now() | Creation timestamp |
| label | TEXT | NULL | Optional human-readable label |

#### `users`
User identities within namespaces. Supports future multi-user and OAuth migration.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | User identifier |
| namespace_id | UUID | FK → namespaces.id, NOT NULL | Owning namespace |
| external_auth_id | TEXT | NULL, UNIQUE | Future OAuth provider ID |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT now() | Creation timestamp |

**Index:** `(namespace_id, id)` for efficient scoped queries

#### `shows`
Core entity: catalog items with user overlays.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | TEXT | PK, NOT NULL | Stable show identifier (from catalog) |
| namespace_id | UUID | FK → namespaces.id, NOT NULL | Owning namespace |
| user_id | UUID | FK → users.id, NOT NULL | Owning user |
| title | TEXT | NOT NULL | Display title |
| show_type | TEXT | NOT NULL | 'movie' \| 'tv' \| 'person' \| 'unknown' |
| external_ids | JSONB | NULL | External catalog identifiers |
| overview | TEXT | NULL | Plot summary |
| genres | TEXT[] | NOT NULL, DEFAULT '{}' | Genre names |
| tagline | TEXT | NULL | Marketing tagline |
| homepage | TEXT | NULL | Official website URL |
| original_language | TEXT | NULL | ISO 639-1 code |
| spoken_languages | TEXT[] | NOT NULL, DEFAULT '{}' | ISO 639-1 codes |
| languages | TEXT[] | NOT NULL, DEFAULT '{}' | Catalog language codes |
| poster_url | TEXT | NULL | Full poster image URL |
| backdrop_url | TEXT | NULL | Full backdrop image URL |
| logo_url | TEXT | NULL | Full logo image URL |
| network_logos | TEXT[] | NOT NULL, DEFAULT '{}' | Reserved |
| vote_average | DOUBLE PRECISION | NULL | Community score |
| popularity | DOUBLE PRECISION | NULL | Popularity metric |
| vote_count | INTEGER | NULL | Number of votes |
| last_air_date | DATE | NULL | TV: last episode air date |
| first_air_date | DATE | NULL | TV: first episode air date |
| release_date | DATE | NULL | Movie: release date |
| runtime | INTEGER | NULL | Movie: runtime in minutes |
| budget | BIGINT | NULL | Movie: production budget |
| revenue | BIGINT | NULL | Movie: box office revenue |
| series_status | TEXT | NULL | TV: series status |
| number_of_episodes | INTEGER | NULL | TV: total episodes |
| number_of_seasons | INTEGER | NULL | TV: total seasons |
| episode_run_time | INTEGER[] | NOT NULL, DEFAULT '{}' | TV: episode runtimes |
| last_episode_run_time | INTEGER | NULL | Reserved |
| my_tags | TEXT[] | NOT NULL, DEFAULT '{}' | User tags |
| my_tags_update_date | TIMESTAMPTZ | NULL | Tags last modified |
| my_score | DOUBLE PRECISION | NULL | User rating (0-10 scale) |
| my_score_update_date | TIMESTAMPTZ | NULL | Rating last modified |
| my_status | TEXT | NULL | 'active' \| 'next' \| 'later' \| 'done' \| 'quit' \| 'wait' |
| my_status_update_date | TIMESTAMPTZ | NULL | Status last modified |
| my_interest | TEXT | NULL | 'excited' \| 'interested' |
| my_interest_update_date | TIMESTAMPTZ | NULL | Interest last modified |
| ai_scoop | TEXT | NULL | AI-generated personality description |
| ai_scoop_update_date | TIMESTAMPTZ | NULL | Scoop last generated |
| details_update_date | TIMESTAMPTZ | NULL | Last catalog merge |
| creation_date | TIMESTAMPTZ | NULL | First save timestamp |
| is_test | BOOLEAN | NOT NULL, DEFAULT false | Test data flag |
| provider_data | JSONB | NULL | Streaming provider IDs by region |

**Indexes:**
- `(namespace_id, user_id, my_status)` — Filter by status
- `(namespace_id, user_id, my_tags)` — GIN index for tag filtering
- `(namespace_id, user_id, genres)` — GIN index for genre filtering
- `(namespace_id, user_id, vote_average)` — Score range filtering
- `(namespace_id, user_id, my_status_update_date DESC)` — Recently updated sorting

**RLS Policies:**
- SELECT: `namespace_id = current_setting('app.current_namespace')::uuid AND user_id = current_setting('app.current_user_id')::uuid`
- INSERT/UPDATE/DELETE: Same as SELECT

#### `cloud_settings`
Synced app-wide settings.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | TEXT | PK, NOT NULL, DEFAULT 'globalSettings' | Settings singleton key |
| namespace_id | UUID | FK → namespaces.id, NOT NULL | Owning namespace |
| user_id | UUID | FK → users.id, NOT NULL | Owning user |
| user_name | TEXT | NOT NULL | Random display name |
| version | BIGINT | NOT NULL | Epoch seconds for conflict resolution |
| catalog_api_key | TEXT | NULL | External catalog API key |
| ai_api_key | TEXT | NULL | AI provider API key |
| ai_model | TEXT | NOT NULL | AI model identifier |

**RLS:** Same as shows table

#### `app_metadata`
Tracks data model version for migrations.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | TEXT | PK, NOT NULL, DEFAULT 'metadata' | Singleton key |
| namespace_id | UUID | FK → namespaces.id, NOT NULL | Owning namespace |
| data_model_version | INTEGER | NOT NULL, DEFAULT 3 | Schema version |

**RLS:** Same as shows table

#### `local_settings` (client-side only, not in Supabase)
Stored in localStorage/cookies for non-synced preferences.

Keys:
- `autoSearch` (boolean) — Open search on launch
- `fontSize` (string) — 'XS' \| 'S' \| 'M' \| 'L' \| 'XL' \| 'XXL'

#### `ui_state` (client-side only, not in Supabase)
Stored in localStorage for UI preferences.

Keys:
- `hideStatusRemovalConfirmation` (boolean)
- `statusRemovalCountKey` (number)
- `lastSelectedFilter` (JSON-encoded FilterConfiguration)

### 2.2 Migrations

Migration files define schema evolution:

1. `001_create_namespaces.sql` — Create namespaces table
2. `002_create_users.sql` — Create users table with namespace FK
3. `003_create_shows.sql` — Create shows table with indexes and RLS policies
4. `004_create_cloud_settings.sql` — Create cloud_settings table
5. `005_create_app_metadata.sql` — Create app_metadata table
6. `006_enable_rls.sql` — Enable Row Level Security and create policies

Each migration is idempotent and can be applied to a fresh or existing database.

### 2.3 Seed Data (Optional)

For development/testing, seed scripts create:
- A default namespace
- A default user within that namespace
- Sample shows with various statuses, tags, and ratings

Seed data respects namespace isolation and can be cleared independently per namespace.

---

## 3. Identity & Isolation Model

### 3.1 Namespace Management

**Initialization:**
- On app startup, read `NAMESPACE_ID` from environment variables
- If not set, generate a random UUID and persist in session/localStorage for the dev session
- Set PostgreSQL session variable: `SET app.current_namespace = '<namespace_id>'`

**Enforcement:**
- All Supabase queries automatically include namespace_id via RLS policies
- API routes validate namespace_id matches session before forwarding to database
- Destructive test operations are scoped to the current namespace

### 3.2 User Identity (Benchmark Mode)

**Dev Identity Injection:**
- Read `USER_ID` from environment variables OR select from a dev-only user picker UI
- If not set, create/use a default user within the current namespace
- Set PostgreSQL session variable: `SET app.current_user_id = '<user_id>'`

**Production Migration Path:**
- Replace dev identity injection with OAuth flow (e.g., Google OAuth via Supabase Auth)
- Map OAuth user ID to internal user_id
- Schema remains unchanged; only auth wiring changes

**API Route Protection:**
```typescript
// Example middleware for API routes
export function withAuth(handler: NextApiHandler) {
  return async (req: NextApiRequest, res: NextApiResponse) => {
    const userId = process.env.NODE_ENV === 'development' 
      ? req.headers['x-user-id'] || getDefaultUserId()
      : await getAuthenticatedUserId(req);
    
    if (!userId) {
      return res.status(401).json({ error: 'Unauthorized' });
    }
    
    // Set session context for RLS
    await supabase.rpc('set_current_user', { user_id: userId });
    
    return handler(req, res);
  };
}
```

### 3.3 Multi-User Considerations

While the benchmark may run as single-user, the system is designed for multi-user:
- Each user has isolated data within a namespace
- Cloud settings are per-user (not shared across users in same namespace)
- Future: namespaces could represent organizations/families with multiple users

---

## 4. Core Features Implementation

### 4.1 Collection Home (`pages/Home/`)

**Purpose:** Display the user's library organized by status with filtering capabilities.

**Implementation Details:**

1. **Data Fetching:**
   - Query shows filtered by selected filter(s) and media type toggle
   - Group results by status on the client side
   - Sort within groups by `my_status_update_date DESC`

2. **Status Sections:**
   - **Active:** Prominent display with larger tiles
   - **Excited:** Later + Excited shows
   - **Interested:** Later + Interested shows
   - **Other:** Collapsible group containing Wait, Quit, Done, and Later without interest

3. **Filter Sidebar:**
   - Quick filter: "All Shows"
   - Tag filters: Dynamically generated from user's tag library
   - Genre filters: Extracted from saved shows' genres
   - Decade filters: Derived from release/air dates
   - Community score ranges: Predefined buckets (0-3, 3-5, 5-7, 7-8, 8-10)
   - Media type toggle: All / Movies / TV (applies on top of any filter)

4. **Empty States:**
   - No collection: CTA to Search or Ask
   - Filter yields no results: "No results found" message

5. **Show Tiles:**
   - Display poster, title
   - Badges: In-collection indicator, user rating indicator
   - Click opens Detail page

**Key Hooks:**
- `useHomeData(filter, mediaType)` — Fetches and groups shows
- `useFilters()` — Manages available filters and selection state

**Performance:**
- Paginate or virtualize large grids
- Cache filter options (tags, genres) to avoid recalculation

### 4.2 Show Detail Page (`pages/Detail/`)

**Purpose:** Single source of truth for a show with public facts, user relationship controls, and discovery launchpad.

**Implementation Details:**

1. **Header Media Carousel:**
   - Display trailers (if available), backdrops, posters, logos
   - Auto-advance carousel with manual controls
   - Graceful fallback to poster-only if no other media

2. **Core Facts:**
   - Year, runtime (movies) or seasons/episodes (TV)
   - Community score bar (visual representation of vote_average)

3. **My Relationship Controls (Toolbar):**
   - **Status Chips:** Active, Interested, Excited, Done, Quit, Wait
     - Clicking sets status + auto-saves
     - Reselecting active status triggers removal confirmation
     - Interested/Excited set `my_status=later` + `my_interest=interested/excited`
   - **Rating Bar:** 0-10 slider
     - Rating an unsaved show auto-saves with `my_status=done`
   - **Tag Picker:** Free-form tag input with autocomplete from existing tags
     - Adding a tag to unsaved show auto-saves with `my_status=later`, `my_interest=interested`

4. **Overview + Scoop:**
   - Overview text from catalog
   - Scoop toggle button:
     - No scoop: "Give me the scoop!"
     - Cached scoop (< 4 hours): "Show the scoop"
     - Expired scoop: Regenerate on demand
   - Scoop streams progressively (typewriter effect or chunk-by-chunk)
   - Scoop only persists if show is in collection

5. **Ask About This Show:**
   - Button launches Ask mode with show context seeded
   - Opens Find → Ask with pre-filled context

6. **Traditional Recommendations:**
   - Horizontal strand of similar/recommended shows from catalog
   - Clicking opens Detail for that show

7. **Explore Similar (Concept Discovery):**
   - **Get Concepts** button triggers AI concept extraction
   - Concepts displayed as selectable chips (1-3 words each)
   - User selects 1+ concepts (up to 8)
   - **Explore Shows** button fetches AI recommendations based on selected concepts
   - Results displayed as horizontal strand with reasons

8. **Streaming Availability:**
   - Display provider logos for flatrate/rent/buy options in user's region
   - Resolve provider IDs to metadata (name, logo URL)

9. **Cast & Crew:**
   - Horizontal strands for cast and crew
   - Person cards with image, name, character/job
   - Click opens Person Detail

10. **Seasons (TV Only):**
    - List of seasons with episode counts
    - Expandable to show episode details

11. **Budget vs Revenue (Movies):**
    - Visual comparison when data available

**Key Hooks:**
- `useShowDetail(showId)` — Fetches show data from backend
- `useMyData(showId)` — Manages user overlay (status, rating, tags, scoop)
- `useScoop(showId)` — Handles scoop generation, caching, and freshness
- `useConcepts(showId)` — Manages concept extraction and selection
- `useRecommendations(showId)` — Fetches traditional recommendations

**Auto-Save Logic:**
```typescript
function handleSaveTrigger(show: Show, action: SaveAction) {
  if (show.myStatus) {
    // Already saved, just update the relevant field
    updateShow(show.id, action.payload);
  } else {
    // Not saved yet — apply default status rules
    const defaults = getSaveDefaults(action);
    createShow({
      ...show,
      myStatus: defaults.status,
      myInterest: defaults.interest,
      ...action.payload
    });
  }
}

function getSaveDefaults(action: SaveAction): { status: MyStatusType; interest?: MyInterestType } {
  switch (action.type) {
    case 'SET_RATING':
      return { status: 'done' }; // Rating implies watched
    case 'ADD_TAG':
      return { status: 'later', interest: 'interested' };
    case 'SET_INTEREST':
      return { status: 'later', interest: action.interest };
    default:
      return { status: 'later', interest: 'interested' };
  }
}
```

**Removal Confirmation:**
```typescript
function handleRemoveStatus(showId: string) {
  const hideConfirm = localStorage.getItem('hideStatusRemovalConfirmation');
  const count = parseInt(localStorage.getItem('statusRemovalCountKey') || '0');
  
  if (hideConfirm === 'true') {
    deleteShow(showId);
    return;
  }
  
  showModal({
    title: 'Remove from collection?',
    body: 'This will clear all your data for this show (status, tags, rating, scoop).',
    actions: [
      { label: 'Cancel', onClick: () => closeModal() },
      { 
        label: 'Remove', 
        onClick: () => {
          deleteShow(showId);
          localStorage.setItem('statusRemovalCountKey', (count + 1).toString());
          if (count >= 3) {
            localStorage.setItem('hideStatusRemovalConfirmation', 'true');
          }
          closeModal();
        }
      }
    ]
  });
}
```

### 4.3 Search (`pages/Find/features/Search/`)

**Purpose:** Find shows in the global catalog by title/keywords.

**Implementation Details:**

1. **Search Input:**
   - Debounced text input (300ms delay)
   - Clear button to reset
   - Auto-focus on mount if "Search on Launch" setting enabled

2. **Results Grid:**
   - Poster grid layout
   - In-collection items marked with badge
   - Infinite scroll or pagination for large result sets

3. **Catalog Integration:**
   - Query external catalog API with search term
   - Map catalog results to Show objects (without user overlay)
   - Merge with local shows to display in-collection indicators

4. **Result Selection:**
   - Click opens Detail page
   - Detail page loads full show data including transient fields (cast, crew, etc.)

**Key Hook:**
- `useSearch(query, page)` — Debounced search with pagination

**Auto-Open on Launch:**
```typescript
// In Find page or app entry point
useEffect(() => {
  const autoSearch = localStorage.getItem('autoSearch');
  if (autoSearch === 'true' && !initialQuery) {
    setSearchMode('search');
    focusSearchInput();
  }
}, []);
```

### 4.4 Ask (AI Chat) (`pages/Find/features/Ask/`)

**Purpose:** Conversational discovery grounded in user taste.

**Implementation Details:**

1. **Chat Interface:**
   - Message list with user/assistant turns
   - Input field at bottom
   - Scroll-to-bottom on new messages

2. **Welcome View:**
   - 6 random starter prompts from curated list of 80
   - Refresh button to get new prompts
   - Clicking a prompt sends it as first message

3. **Conversation Context:**
   - Maintain message history in component state
   - After ~10 messages, summarize older turns (AI-powered summarization)
   - Include user library context in system prompt (saved shows with My Data)

4. **Mentioned Shows:**
   - Parse AI responses for structured show mentions
   - Format: `Title::externalId::mediaType;;Title2::externalId::mediaType;;...`
   - Display mentioned shows in horizontal strip below chat
   - Click opens Detail or hands off to Search if mapping fails

5. **Ask About a Show:**
   - Launched from Detail page
   - Seed conversation with show context (title, overview, user's My Data for that show)
   - Prefill behavior: Switch to Ask mode with show info in system prompt

6. **Tone & Personality:**
   - Warm, opinionated, spoiler-safe
   - Direct answers within first 3-5 lines
   - Bulleted lists for multi-recs
   - Honest about mixed reception

**Structured Output Parsing:**
```typescript
interface AskResponse {
  commentary: string;
  showList: Array<{
    title: string;
    externalId: string;
    mediaType: 'movie' | 'tv';
  }>;
}

function parseAskResponse(rawText: string): AskResponse {
  // Split on delimiter between commentary and show list
  const parts = rawText.split('||SHOWS||');
  const commentary = parts[0].trim();
  
  if (!parts[1]) {
    return { commentary, showList: [] };
  }
  
  const showList = parts[1]
    .split(';;')
    .filter(Boolean)
    .map(entry => {
      const [title, externalId, mediaType] = entry.split('::');
      return { title, externalId, mediaType: mediaType as 'movie' | 'tv' };
    });
  
  return { commentary, showList };
}
```

**Conversation Summarization:**
```typescript
async function summarizeOldTurns(messages: Message[]): Promise<string> {
  const oldMessages = messages.slice(0, -10);
  const prompt = `Summarize this conversation in 1-2 sentences, preserving the friendly tone:
  
  ${oldMessages.map(m => `${m.role}: ${m.content}`).join('\n')}
  
  Summary:`;
  
  const response = await aiClient.complete(prompt);
  return response.text;
}
```

**Key Hooks:**
- `useAskChat(namespaceId, userId)` — Manages chat state, message history, and AI calls
- `useStarterPrompts()` — Provides randomized starter prompts

### 4.5 Alchemy (`pages/Find/features/Alchemy/`)

**Purpose:** Structured discovery by blending multiple shows into concept catalysts.

**Implementation Details:**

1. **Step 1: Select Input Shows:**
   - Show selector allowing 2+ shows
   - Can pick from library or search global catalog
   - Minimum 2 shows required to proceed

2. **Step 2: Conceptualize:**
   - **Conceptualize Shows** button triggers AI concept extraction
   - AI analyzes all input shows and extracts shared concepts
   - Concepts displayed as selectable chips (larger pool than single-show)

3. **Step 3: Select Concepts:**
   - User selects up to 8 concepts
   - Selection/unselection clears downstream results
   - Visual feedback for selected state

4. **Step 4: Alchemize:**
   - **ALCHEMIZE!** button fetches recommendations
   - AI returns 6 recommended shows with reasons
   - Reasons explicitly reference selected concepts
   - Results displayed with poster, title, reason text

5. **Step 5: Chain Another Round:**
   - **More Alchemy!** button allows chaining
   - Previous results become available as new inputs
   - State resets for new round while preserving history

6. **Backtracking:**
   - Changing input shows clears concepts and results
   - Changing concept selection clears results
   - Clear visual indication of step progression

**State Machine:**
```typescript
type AlchemyStep = 'select-shows' | 'conceptualize' | 'select-concepts' | 'alchemize' | 'results';

interface AlchemyState {
  step: AlchemyStep;
  inputShows: Show[];
  concepts: string[];
  selectedConcepts: string[];
  results: Recommendation[];
  history: AlchemyRound[];
}
```

**Key Hook:**
- `useAlchemy()` — Manages alchemy state machine and AI calls

### 4.6 Person Detail (`pages/Person/`)

**Purpose:** Explore talent (cast/crew) behind shows.

**Implementation Details:**

1. **Person Header:**
   - Name, profile image
   - Bio text

2. **Image Gallery:**
   - Grid of person images from catalog

3. **Analytics Charts:**
   - Average project ratings over time
   - Top genres distribution
   - Projects by year histogram

4. **Filmography:**
   - Credits grouped by year (descending)
   - Each credit: show poster, title, role (character for cast, job for crew)
   - Click opens Show Detail

**Data Fetching:**
- Fetch person data from catalog API (not persisted locally)
- Transient data: no local storage except cache

**Key Hook:**
- `usePerson(personId)` — Fetches person data and filmography

### 4.7 Settings (`pages/Settings/`)

**Purpose:** Configure app settings, AI preferences, integrations, and data export.

**Implementation Details:**

1. **App Settings:**
   - Font size selector (XS, S, M, L, XL, XXL)
   - Search on launch toggle
   - Stored in localStorage (not synced)

2. **User Settings:**
   - Username display/edit (synced via cloud_settings)

3. **AI Settings:**
   - AI provider API key input (stored in cloud_settings)
   - AI model selector dropdown (stored in cloud_settings)
   - Warning: Keys synced across devices if enabled

4. **Integration Settings:**
   - Content catalog provider API key input (stored in cloud_settings)

5. **Data Export:**
   - **Export My Data** button generates ZIP file
   - ZIP contains JSON backup of all saved shows and My Data
   - Dates encoded as ISO-8601 strings
   - File naming: `export-{timestamp}.zip`

**Export Implementation:**
```typescript
async function exportUserData(userId: string, namespaceId: string): Promise<Blob> {
  const shows = await fetchUserShows(userId, namespaceId);
  const settings = await fetchCloudSettings(userId, namespaceId);
  
  const snapshot: StorageSnapshot = {
    shows: shows.map(show => ({
      ...show,
      // Ensure dates are ISO-8601 strings
      myTagsUpdateDate: show.myTagsUpdateDate?.toISOString(),
      myScoreUpdateDate: show.myScoreUpdateDate?.toISOString(),
      myStatusUpdateDate: show.myStatusUpdateDate?.toISOString(),
      myInterestUpdateDate: show.myInterestUpdateDate?.toISOString(),
      aiScoopUpdateDate: show.aiScoopUpdateDate?.toISOString(),
      detailsUpdateDate: show.detailsUpdateDate?.toISOString(),
      creationDate: show.creationDate?.toISOString(),
    })),
    cloudSettings: settings,
    appMetadata: { dataModelVersion: 3 },
  };
  
  const jsonStr = JSON.stringify(snapshot, null, 2);
  const zip = new JSZip();
  zip.file('export.json', jsonStr);
  
  return await zip.generateAsync({ type: 'blob' });
}
```

**Import/Restore (Not Implemented):**
- UI placeholder for future import feature
- Would parse ZIP, validate schema, and merge into existing data

---

## 5. AI Integration Layer

### 5.1 Provider Abstraction

**Interface:**
```typescript
interface AIProvider {
  complete(prompt: string, options?: CompleteOptions): Promise<CompletionResponse>;
  streamComplete(prompt: string, options?: CompleteOptions): AsyncIterable<string>;
}

interface CompleteOptions {
  temperature?: number;
  maxTokens?: number;
  stopSequences?: string[];
  format?: 'text' | 'json';
}

interface CompletionResponse {
  text: string;
  usage?: { promptTokens: number; completionTokens: number };
}
```

**Implementations:**
- `OpenAIProvider` — OpenAI API (GPT models)
- `AnthropicProvider` — Anthropic API (Claude models)
- `MockProvider` — For testing without API calls

**Selection:**
- Read `AI_MODEL` from environment or cloud_settings
- Instantiate appropriate provider based on model prefix

### 5.2 Prompt Templates

All prompts maintain consistent persona: fun, chatty, opinionated, spoiler-safe TV/movie nerd friend.

#### Scoop Prompt
```
You are a fun, chatty TV/movie nerd friend giving a spoiler-safe taste review.

Show: {title} ({year})
Type: {mediaType}
Overview: {overview}
Genres: {genres}
Community Score: {voteAverage}/10

User's relationship:
- Status: {myStatus}
- Rating: {myScore}/10
- Tags: {myTags}

Write a mini blog-post review with these sections:
1. Your personal take (make a stand)
2. Honest stack-up vs reviews (acknowledge mixed reception if relevant)
3. THE SCOOP (emotional centerpiece paragraph)
4. Practical fit / warnings (who it's for, who might not like it)
5. "Worth it?" gut check

Keep it warm, playful, specific, and spoiler-safe. ~150-350 words total.
```

#### Ask Prompt (System)
```
You are a fun, opinionated TV/movie nerd friend helping someone discover what to watch next.

Rules:
- Stay within TV/movies only
- Be spoiler-safe unless asked otherwise
- Pick favorites confidently
- Be honest about mixed reception
- Use specific vibe/structure/craft reasoning, not generic genre talk
- Keep responses concise (1-3 paragraphs + bulleted list for recs)
- Mirror the user's energy

User's Library (taste context):
{librarySummary}

Respond like you're chatting at a water cooler — friendly, direct, and excited to share.
```

#### Ask with Mentions Prompt Extension
```
When recommending shows, include them in a structured format after your commentary:

||SHOWS||
Title::externalId::mediaType;;Title2::externalId2::mediaType;;...

Example:
Here are some great picks for you!

||SHOWS||
Severance::12345::tv;;The Bear::67890::tv;;Past Lives::11111::movie
```

#### Concept Extraction Prompt (Single Show)
```
Extract 8 core "concept ingredients" that capture the feeling of this show.

Show: {title}
Overview: {overview}
Genres: {genres}

Concepts should be:
- 1-3 words each
- Evocative and specific (not generic like "good characters")
- Cover different axes: structure, vibe, emotion, craft, relationships
- No plot details or spoilers
- Ordered by strength (best "aha" concepts first)

Output as a bullet list only. No explanations.

Examples of great concepts:
- hopeful absurdity
- case-a-week
- quirky makeshift family
- slow-burn dread
- elegant puzzle-box
```

#### Concept Extraction Prompt (Multi-Show / Alchemy)
```
Extract shared concept ingredients across ALL these shows.

Shows:
{showsList}

Concepts must represent commonality across ALL input shows, not just one or two.

Requirements:
- Generate 12-16 concepts (user will select up to 8)
- Each concept 1-3 words
- Evocative, specific, spoiler-free
- Cover different axes: structure, vibe, emotion, craft, relationships
- Ordered by how strongly they connect all shows

Output as a bullet list only. No explanations.
```

#### Concept-Based Recommendations Prompt (Explore Similar)
```
Recommend 5 real shows matching these selected concepts.

Source Show: {sourceTitle}
Selected Concepts: {selectedConcepts}

Requirements:
- Each recommendation must be a REAL show with valid external ID
- Include a concise reason (1-3 sentences) naming which concepts align
- Bias toward recent shows but allow classics/hidden gems
- Stay spoiler-safe
- Be excited and specific in reasoning

Output format:
Title::externalId::mediaType::Reason text;;Title2::externalId2::mediaType::Reason text2;;...
```

#### Concept-Based Recommendations Prompt (Alchemy)
```
Recommend 6 real shows matching these blended concepts.

Input Shows: {inputShowsTitles}
Selected Concepts: {selectedConcepts}

Requirements:
- Each recommendation must be a REAL show with valid external ID
- Include a concise reason (1-3 sentences) naming which concepts align
- Surprise without betrayal: 1-2 unexpected but defensible picks
- Bias toward recent shows but allow classics
- Stay spoiler-safe
- Be thrilled to share — excited, happy tone

Output format:
Title::externalId::mediaType::Reason text;;Title2::externalId2::mediaType::Reason text2;;...
```

### 5.3 Context Assembly

**Library Context for AI:**
```typescript
function buildLibraryContext(shows: Show[]): string {
  const savedShows = shows.filter(s => s.myStatus);
  
  if (savedShows.length === 0) {
    return 'User has no saved shows yet.';
  }
  
  const lines = savedShows.map(show => {
    const parts = [`${show.title} (${show.showType})`];
    if (show.myStatus) parts.push(`Status: ${show.myStatus}`);
    if (show.myInterest) parts.push(`Interest: ${show.myInterest}`);
    if (show.myScore) parts.push(`Rating: ${show.myScore}/10`);
    if (show.myTags.length > 0) parts.push(`Tags: ${show.myTags.join(', ')}`);
    return '- ' + parts.join(' | ');
  });
  
  return `User's library (${savedShows.length} shows):\n${lines.join('\n')}`;
}
```

**Show Context for "Ask About This Show":**
```typescript
function buildShowContext(show: Show): string {
  return `Current show: ${show.title} (${show.showType}, ${show.releaseDate || show.firstAirDate})
Overview: ${show.overview}
Genres: ${show.genres.join(', ')}
Community Score: ${show.voteAverage}/10
User's Status: ${show.myStatus || 'not saved'}
User's Rating: ${show.myScore ? show.myScore + '/10' : 'not rated'}
User's Tags: ${show.myTags.join(', ') || 'none'}`;
}
```

### 5.4 Error Handling & Fallbacks

1. **AI API Failure:**
   - Retry once with exponential backoff
   - Fall back to cached data if available
   - Show user-friendly error message

2. **Structured Output Parse Failure:**
   - Retry once with stricter formatting instructions
   - Fall back to unstructured commentary + Search handoff for show resolution

3. **Show Resolution Failure:**
   - If AI-recommended show cannot be resolved in catalog, display as non-interactive text
   - Provide "Search for this" link to open Search with title pre-filled

4. **Rate Limiting:**
   - Implement client-side rate limiting for AI calls
   - Queue requests if limit exceeded
   - Show loading states during wait

---

## 6. External Catalog Integration

### 6.1 Provider Abstraction

**Interface:**
```typescript
interface CatalogProvider {
  search(query: string, page?: number): Promise<CatalogSearchResult[]>;
  getShow(id: string): Promise<CatalogShow>;
  getPerson(id: string): Promise<CatalogPerson>;
  getRecommendations(showId: string): Promise<CatalogShow[]>;
  getSimilar(showId: string): Promise<CatalogShow[]>;
  getProviders(showId: string, countryCode: string): Promise<ProviderData>;
}
```

**Implementation (TMDB Example):**
- Map TMDB API responses to internal Show types
- Handle pagination for search results
- Cache responses to reduce API calls

### 6.2 Catalog → Show Mapping

**Mapping Rules:**
```typescript
function mapCatalogToShow(catalogItem: CatalogShow): Partial<Show> {
  return {
    id: catalogItem.id.toString(),
    title: catalogItem.title || catalogItem.name,
    showType: catalogItem.media_type === 'movie' ? 'movie' : 'tv',
    externalIds: { tmdb: catalogItem.id.toString() },
    overview: catalogItem.overview,
    genres: catalogItem.genres.map(g => g.name),
    tagline: catalogItem.tagline,
    posterUrl: catalogItem.poster_path ? `https://image.tmdb.org/t/p/w500${catalogItem.poster_path}` : null,
    backdropUrl: catalogItem.backdrop_path ? `https://image.tmdb.org/t/p/original${catalogItem.backdrop_path}` : null,
    voteAverage: catalogItem.vote_average,
    voteCount: catalogItem.vote_count,
    popularity: catalogItem.popularity,
    releaseDate: catalogItem.release_date,
    firstAirDate: catalogItem.first_air_date,
    runtime: catalogItem.runtime,
    // ... additional fields
  };
}
```

### 6.3 Merge Strategy

When refreshing catalog data for an existing stored show:

```typescript
function mergeCatalogIntoStored(stored: Show, catalog: Partial<Show>): Show {
  const merged = { ...stored };
  
  // Non-my fields: selectFirstNonEmpty (never overwrite with empty/null)
  const nonMyFields = ['title', 'overview', 'tagline', 'posterUrl', 'backdropUrl', /* ... */];
  for (const field of nonMyFields) {
    if (catalog[field] && !isEmpty(catalog[field])) {
      merged[field] = catalog[field];
    }
  }
  
  // My fields: resolve by timestamp (newer wins)
  const myFields = [
    { field: 'myTags', dateField: 'myTagsUpdateDate' },
    { field: 'myScore', dateField: 'myScoreUpdateDate' },
    { field: 'myStatus', dateField: 'myStatusUpdateDate' },
    { field: 'myInterest', dateField: 'myInterestUpdateDate' },
  ];
  
  for (const { field, dateField } of myFields) {
    const storedDate = stored[dateField];
    const catalogDate = catalog[dateField];
    
    if (!storedDate && catalogDate) {
      merged[field] = catalog[field];
      merged[dateField] = catalogDate;
    } else if (storedDate && catalogDate && catalogDate > storedDate) {
      merged[field] = catalog[field];
      merged[dateField] = catalogDate;
    }
    // Otherwise keep stored value
  }
  
  // Update management fields
  merged.detailsUpdateDate = new Date().toISOString();
  // creationDate is NOT changed
  
  return merged;
}
```

### 6.4 Provider Data (Streaming Availability)

- Store only provider IDs by region in `provider_data` JSONB column
- Fetch provider metadata (name, logo) on-demand or from cached provider directory
- Display providers relevant to user's detected region

---

## 7. Data Export & Backup

### 7.1 Export Flow

1. User clicks "Export My Data" in Settings
2. System fetches all shows and settings for current user/namespace
3. Serialize to JSON with ISO-8601 dates
4. Wrap in ZIP file with single `export.json` file
5. Trigger browser download

### 7.2 Export Schema

```typescript
interface StorageSnapshot {
  shows: Show[];
  cloudSettings?: CloudSettings;
  appMetadata?: AppMetadata;
  localSettings?: LocalSettings;
  uiState?: UserDefaultsUIState;
}
```

### 7.3 Import/Restore (Future)

Not implemented in this phase. Future implementation would:
1. Accept ZIP file upload
2. Validate JSON schema and data model version
3. Offer merge strategies: replace all, merge with existing, selective import
4. Apply timestamps for conflict resolution

---

## 8. Testing Strategy

### 8.1 Unit Tests

**Critical Logic:**
- Show merge logic (`lib/catalog/mapper.test.ts`)
- Auto-save defaults (`pages/Detail/features/MyRelationshipControls/hooks/useMyData.test.ts`)
- AI output parsing (`utils/aiParser.test.ts`)
- Filter logic (`pages/Home/features/FilterSidebar/hooks/useFilters.test.ts`)
- Export serialization (`utils/exportUtils.test.ts`)

**Test Framework:** Jest or Vitest with React Testing Library

### 8.2 Integration Tests

**API Routes:**
- Show CRUD operations with namespace isolation
- Settings read/write
- Authentication middleware

**Database:**
- RLS policy enforcement
- Migration idempotency
- Index performance

### 8.3 Visual/Component Tests

**Tools:** Storybook + Chromatic or Playwright screenshots

**Key Components:**
- Show tile rendering with badges
- Status chip interactions
- Rating slider behavior
- Chat message rendering
- Concept chip selection
- Filter sidebar states

### 8.4 Destructive Testing

**Namespace Isolation Test:**
```typescript
test('destructive operations are scoped to namespace', async () => {
  const namespace1 = createNamespace();
  const namespace2 = createNamespace();
  const user1 = createUser(namespace1);
  const user2 = createUser(namespace2);
  
  // Add shows to both namespaces
  await addShow(namespace1, user1, { id: 'show1', title: 'Test Show' });
  await addShow(namespace2, user2, { id: 'show1', title: 'Test Show' });
  
  // Delete from namespace1
  await deleteShow(namespace1, user1, 'show1');
  
  // Verify namespace2 still has the show
  const ns2Shows = await getShows(namespace2, user2);
  expect(ns2Shows).toHaveLength(1);
});
```

**Test Reset Script:**
```bash
# npm run test:reset
# Deletes all data in current namespace, recreates seed data
```

### 8.5 AI Quality Tests

**Golden Set Validation:**
- Pre-defined scenarios with expected quality dimensions
- Score voice adherence, taste alignment, specificity, real-show integrity
- Passing threshold: Voice ≥1, Taste ≥1, Real-show integrity =2, Total ≥7/10

**Regression Detection:**
- Compare AI outputs across prompt/model changes
- Flag significant deviations in tone or structure

---

## 9. Environment Configuration

### 9.1 Required Environment Variables

**.env.example:**
```bash
# Supabase Configuration
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key  # Server-only

# Namespace & Identity (Benchmark Mode)
NAMESPACE_ID=your-namespace-uuid
USER_ID=your-user-uuid

# AI Provider
AI_API_KEY=your-ai-api-key
AI_MODEL=gpt-4o-mini  # or claude-3-haiku, etc.

# External Catalog
CATALOG_API_KEY=your-tmdb-api-key
CATALOG_PROVIDER=tmdb

# Optional: Region for streaming providers
USER_REGION=US
```

### 9.2 Scripts

**package.json:**
```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "test": "vitest",
    "test:reset": "tsx scripts/reset-test-data.ts",
    "db:migrate": "supabase db push",
    "db:seed": "tsx scripts/seed-database.ts",
    "lint": "eslint src/",
    "typecheck": "tsc --noEmit"
  }
}
```

### 9.3 Git Ignore

**.gitignore:**
```
.env
.env.local
.env.*.local
node_modules/
.next/
dist/
*.log
.DS_Store
```

---

## 10. Development Phases

### Phase 1: Foundation (Week 1-2)

**Goals:**
- Set up Next.js project with TypeScript
- Configure Supabase client and database
- Create database schema with migrations
- Implement namespace/user isolation
- Set up environment configuration
- Create base theme and component library

**Deliverables:**
- Working database with RLS policies
- Basic app shell with routing
- Theme system and core components (Button, Card, Modal, Chip, etc.)
- Auth/identity injection middleware

### Phase 2: Core Data Layer (Week 3-4)

**Goals:**
- Implement Show CRUD operations
- Build catalog provider integration (TMDB)
- Implement catalog → Show mapping and merge logic
- Create cloud_settings and app_metadata management
- Build data export functionality

**Deliverables:**
- Functional data layer with Supabase
- Catalog search and show detail fetching
- Working export to ZIP
- Unit tests for merge logic and mapping

### Phase 3: Collection Home & Filters (Week 5-6)

**Goals:**
- Build Collection Home page with status grouping
- Implement filter sidebar (tags, genres, decades, scores)
- Create show tile component with badges
- Implement media type toggle
- Add empty states

**Deliverables:**
- Fully functional Home page
- Dynamic filter generation
- Responsive grid layout
- Integration tests for filtering

### Phase 4: Show Detail & My Data (Week 7-8)

**Goals:**
- Build Show Detail page with all sections
- Implement My Relationship Controls (status, rating, tags)
- Auto-save logic with default rules
- Removal confirmation flow
- Header media carousel
- Traditional recommendations strand
- Cast & crew display
- Seasons list (TV)
- Budget/revenue display (movies)

**Deliverables:**
- Complete Detail page
- Working status/rating/tag interactions
- Auto-save with correct defaults
- Visual tests for Detail page layouts

### Phase 5: AI Integration - Scoop & Concepts (Week 9-10)

**Goals:**
- Implement AI provider abstraction
- Build Scoop generation with streaming
- Implement concept extraction (single-show)
- Build Explore Similar flow (concepts → recs)
- Implement AI caching and freshness logic

**Deliverables:**
- Working Scoop generation
- Concept extraction and selection UI
- Explore Similar recommendations
- AI quality validation against golden set

### Phase 6: AI Integration - Ask & Alchemy (Week 11-12)

**Goals:**
- Build Ask chat interface
- Implement conversation context management
- Parse structured show mentions
- Build Alchemy flow (multi-show concepts → recs)
- Implement conversation summarization
- Starter prompts system

**Deliverables:**
- Functional Ask chat with mentions
- Complete Alchemy flow with chaining
- Conversation summarization
- "Ask About This Show" handoff from Detail

### Phase 7: Search & Person Detail (Week 13)

**Goals:**
- Implement catalog search with debouncing
- Build Person Detail page
- Analytics charts for person filmography
- Image gallery
- Auto-open search on launch setting

**Deliverables:**
- Working search with infinite scroll
- Person Detail with filmography
- Chart components for analytics

### Phase 8: Settings & Polish (Week 14)

**Goals:**
- Build Settings page with all sections
- Font size and search-on-launch settings
- AI and catalog API key management
- Final data export testing
- Cross-browser testing
- Performance optimization
- Accessibility audit

**Deliverables:**
- Complete Settings page
- Working API key configuration
- Optimized bundle size
- Accessibility compliance

### Phase 9: Testing & Documentation (Week 15)

**Goals:**
- Comprehensive unit test coverage
- Integration tests for API routes
- Visual regression tests
- Destructive testing validation
- Write developer documentation
- Create deployment guide

**Deliverables:**
- Test suite with >80% coverage
- Passing CI pipeline
- Developer README
- Deployment instructions

---

## 11. Risk Mitigation

### 11.1 Technical Risks

**Risk: AI output inconsistency**
- Mitigation: Strict prompt engineering, structured output formats, retry logic, fallback to Search

**Risk: Catalog API rate limits**
- Mitigation: Client-side caching, request queuing, graceful degradation

**Risk: Supabase RLS complexity**
- Mitigation: Thorough testing of policies, session variable management, clear documentation

**Risk: Bundle size bloat**
- Mitigation: Code splitting, lazy loading, tree shaking, regular bundle analysis

### 11.2 Product Risks

**Risk: AI recommendations don't map to real shows**
- Mitigation: Strict output format requiring external IDs, fallback to Search handoff, user feedback mechanism

**Risk: Auto-save defaults feel surprising**
- Mitigation: Clear UI feedback on save, undo capability, user testing of flows

**Risk: Concept quality varies**
- Mitigation: Golden set validation, prompt iteration, quality scoring rubric

### 11.3 Benchmark Risks

**Risk: Namespace collisions in cloud builds**
- Mitigation: UUID generation for namespaces, strict RLS enforcement, isolation tests

**Risk: Dev identity injection leaks to production**
- Mitigation: Environment-gated auth middleware, clear separation of dev/prod modes

---

## 12. Success Criteria

A build is compliant with this plan if:

1. **Infrastructure Compliance:**
   - Provides `.env.example` with all required variables
   - Runs with `npm run dev` without code edits
   - Supports `npm test` and `npm run test:reset`
   - Includes database migrations for repeatable schema setup

2. **Isolation Compliance:**
   - Operates within a single stable namespace_id
   - Associates all user-owned records with user_id
   - Prevents cross-namespace data access via RLS
   - Supports destructive test resets without global teardown

3. **Product Completeness:**
   - Collection Home with status grouping and filters
   - Show Detail with all specified sections
   - Search, Ask, and Alchemy discovery modes
   - Person Detail with filmography and analytics
   - Settings with export functionality
   - Auto-save with correct default behaviors
   - AI outputs maintain consistent persona and quality

4. **Data Integrity:**
   - Backend is source of truth (clearing client storage doesn't lose data)
   - Merge logic preserves user edits across catalog refreshes
   - Timestamps tracked for all user fields
   - Export produces valid JSON backup with ISO-8601 dates

5. **Quality Standards:**
   - Lint-clean codebase
   - Unit tests for critical logic
   - Visual tests for key components
   - AI quality meets golden set thresholds

---

## 13. Open Questions & Future Extensions

### Addressed in This Plan
- Namespace and user isolation model ✓
- Auto-save default rules ✓
- AI structured output format ✓
- Catalog merge strategy ✓
- Data export format ✓

### Deferred to Future Iterations
1. **Next status as first-class UI element** — Currently hidden/inactive in data model
2. **Named custom lists beyond tags** — Tags serve as lightweight lists for now
3. **AI Scoop implicit save** — Currently Scoop only persists if show already saved
4. **Explicit Unrated state** — Currently nil means unrated
5. **Import/Restore from export** — Export implemented; import deferred
6. **Alchemy session saving/sharing** — Sessions are ephemeral
7. **Explicit myStatus filters in sidebar** — Model supports it; UI deferred
8. **OAuth integration** — Dev identity injection for benchmark; OAuth migration path defined

### Monitoring & Analytics (Future)
- Track weekly active additions to collection
- Monitor AI → collection conversion rates
- Measure Alchemy session completion and chaining
- Analyze retention driven by discovery features

---

## Appendix A: Key Type Definitions

```typescript
// Core Types
type ShowType = 'movie' | 'tv' | 'person' | 'unknown';
type MyStatusType = 'active' | 'next' | 'later' | 'done' | 'quit' | 'wait';
type MyInterestType = 'excited' | 'interested';
type FilterType = 'all' | 'genre' | 'myStatus' | 'communityScore' | 'decade' | 'myTag';

interface Show {
  id: string;
  title: string;
  showType: ShowType;
  externalIds?: Record<string, string>;
  overview?: string;
  genres: string[];
  tagline?: string;
  posterUrl?: string;
  backdropUrl?: string;
  logoUrl?: string;
  voteAverage?: number;
  voteCount?: number;
  popularity?: number;
  releaseDate?: string;
  firstAirDate?: string;
  lastAirDate?: string;
  runtime?: number;
  budget?: number;
  revenue?: number;
  numberOfSeasons?: number;
  numberOfEpisodes?: number;
  seriesStatus?: string;
  
  // User overlay
  myTags: string[];
  myTagsUpdateDate?: string;
  myScore?: number;
  myScoreUpdateDate?: string;
  myStatus?: MyStatusType;
  myStatusUpdateDate?: string;
  myInterest?: MyInterestType;
  myInterestUpdateDate?: string;
  aiScoop?: string;
  aiScoopUpdateDate?: string;
  
  // Management
  detailsUpdateDate?: string;
  creationDate?: string;
  isTest: boolean;
  
  // Providers
  providerData?: ProviderData;
}

interface FilterConfiguration {
  type: FilterType;
  label: string;
  value: string;
}

interface StorageSnapshot {
  shows: Show[];
  cloudSettings?: CloudSettings;
  appMetadata?: AppMetadata;
  localSettings?: LocalSettings;
  uiState?: UserDefaultsUIState;
}
```

## Appendix B: AI Prompt Evolution Guidelines

When iterating on prompts:

1. **Preserve persona pillars:** Joy-forward, opinionated honesty, vibe-first, specific, adaptive length
2. **Maintain surface-specific adaptations:** Scoop = mini blog post, Ask = chat dialogue, Concepts = ingredient bullets
3. **Never cross red lines:** No encyclopedic tone, no hedging walls, no generic filler, no non-TV/movie recommendations
4. **Test against golden set:** Validate voice, taste alignment, specificity, real-show integrity
5. **Document changes:** Track prompt versions and rationale for evolution

## Appendix C: Deployment Checklist

- [ ] Environment variables configured (.env populated from .env.example)
- [ ] Supabase project provisioned with migrations applied
- [ ] Namespace ID generated and set
- [ ] User ID configured (dev mode) or OAuth wired (production)
- [ ] AI provider API key set
- [ ] Catalog provider API key set
- [ ] RLS policies verified
- [ ] Build passes lint and typecheck
- [ ] Test suite passes
- [ ] Destructive test reset works
- [ ] Export functionality tested end-to-end
- [ ] AI outputs validated against quality bar
- [ ] Accessibility audit complete
- [ ] Performance budget met (bundle size, load times)

---

**Plan Version:** 1.0  
**Last Updated:** 2026-05-01  
**Author:** Kilo (qwen/qwen3.6-max-preview)
