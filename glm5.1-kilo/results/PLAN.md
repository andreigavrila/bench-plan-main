# Implementation Plan

**Date:** 2025-01-20
**Product:** Personal TV + Movie Companion
**Stack:** Next.js + TypeScript + Supabase

---

## Executive Summary

This plan outlines the implementation of a personal entertainment companion app that enables users to collect, organize, rate, and discover TV shows and movies. The app features AI-powered discovery (Ask, Alchemy, Explore Similar), a rich personal library with status/tag/rating systems, and concept-based taste profiling.

The implementation follows a **fractal architecture** (pages → features → sub-features), uses Next.js for the runtime, Supabase for persistence, and integrates with external APIs for catalog data and AI services. All user-owned data is scoped to `user_id`, and builds operate within isolated `namespace_id` boundaries for test safety.

---

## 1. Technology Stack & Architecture

### 1.1 Core Framework
- **Next.js** (latest stable) with App Router
- **TypeScript** for type safety
- **React Server Components** where appropriate for performance

### 1.2 Persistence Layer
- **Supabase** as database and backend-as-a-service
  - Postgres database for structured data
  - Row Level Security (RLS) for data isolation by `namespace_id` and `user_id`
  - Supabase client libraries for data access

### 1.3 Styling & UI
- **Tailwind CSS** for utility-first styling
- **Design token system** in `src/theme/` for colors, spacing, typography
- Component library of reusable primitives in `src/components/`

### 1.4 Data Fetching & State
- **React Query** (or similar) for server state caching and synchronization
- Custom hooks for feature-level logic (following humble components pattern)

### 1.5 External Services
- **Content catalog API** (e.g., TMDB) for show metadata, cast/crew, recommendations
- **AI provider** (OpenAI/Anthropic) for Scoop, Ask, Concepts, and recommendations

### 1.6 Development Tools
- ESLint and TypeScript strict mode for quality
- Unit tests using Jest or Vitest
- End-to-end tests using Playwright or Cypress

---

## 2. Data Layer Architecture

### 2.1 Database Schema (Supabase/PostgreSQL)

#### `shows` table
```sql
CREATE TABLE shows (
  id TEXT PRIMARY KEY,  -- External catalog ID (e.g., TMDB ID)
  namespace_id TEXT NOT NULL,  -- Build/run isolation
  title TEXT NOT NULL,
  show_type TEXT NOT NULL CHECK (show_type IN ('movie', 'tv', 'person', 'unknown')),
  -- Optional catalog metadata
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
  vote_average NUMERIC,
  vote_count INTEGER,
  popularity NUMERIC,
  last_air_date TIMESTAMPTZ,
  first_air_date TIMESTAMPTZ,
  release_date TIMESTAMPTZ,
  runtime INTEGER,
  budget BIGINT,
  revenue BIGINT,
  series_status TEXT,
  number_of_episodes INTEGER,
  number_of_seasons INTEGER,
  episode_run_time INTEGER[] DEFAULT '{}',
  last_episode_run_time INTEGER,
  -- User overlay fields
  my_tags TEXT[] DEFAULT '{}' NOT NULL,
  my_tags_update_date TIMESTAMPTZ,
  my_score NUMERIC,
  my_score_update_date TIMESTAMPTZ,
  my_status TEXT CHECK (my_status IN ('active', 'next', 'later', 'done', 'quit', 'wait')),
  my_status_update_date TIMESTAMPTZ,
  my_interest TEXT CHECK (my_interest IN ('excited', 'interested')),
  my_interest_update_date TIMESTAMPTZ,
  -- AI data
  ai_scoop TEXT,
  ai_scoop_update_date TIMESTAMPTZ,
  -- Metadata
  details_update_date TIMESTAMPTZ,
  creation_date TIMESTAMPTZ DEFAULT NOW(),
  is_test BOOLEAN DEFAULT FALSE NOT NULL,
  -- Provider data (JSONB)
  provider_data JSONB DEFAULT '{}',
  -- External IDs for resolution
  external_ids JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for common queries
CREATE INDEX idx_shows_namespace_user ON shows(namespace_id, my_status);
CREATE INDEX idx_shows_user_tags ON shows USING GIN(my_tags);
CREATE INDEX idx_shows_genre ON shows USING GIN(genres);
CREATE INDEX idx_shows_popularity ON shows(popularity DESC);
```

#### `cloud_settings` table
```sql
CREATE TABLE cloud_settings (
  id TEXT PRIMARY KEY DEFAULT 'globalSettings',
  namespace_id TEXT NOT NULL,
  user_id TEXT NOT NULL,
  user_name TEXT NOT NULL,
  version NUMERIC NOT NULL,
  catalog_api_key TEXT,
  ai_api_key TEXT,
  ai_model TEXT NOT NULL DEFAULT 'gpt-4o',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(namespace_id, user_id)
);
```

#### `app_metadata` table
```sql
CREATE TABLE app_metadata (
  id TEXT PRIMARY KEY DEFAULT 'appMetadata',
  namespace_id TEXT NOT NULL UNIQUE,
  data_model_version INTEGER DEFAULT 3 NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

### 2.2 Row Level Security (RLS) Policies

```sql
ALTER TABLE shows ENABLE ROW LEVEL SECURITY;
ALTER TABLE cloud_settings ENABLE ROW LEVEL SECURITY;
ALTER TABLE app_metadata ENABLE ROW LEVEL SECURITY;

-- Shows are scoped to namespace and user
CREATE POLICY "Users can see their namespace shows" ON shows
  FOR SELECT USING (namespace_id = current_setting('app.namespace_id', TRUE));

CREATE POLICY "Users can modify their namespace shows" ON shows
  FOR ALL USING (namespace_id = current_setting('app.namespace_id', TRUE));

-- Settings scoped to namespace+user
CREATE POLICY "Users can access their settings" ON cloud_settings
  FOR ALL USING (namespace_id = current_setting('app.namespace_id', TRUE));

-- Metadata scoped to namespace
CREATE POLICY "Read metadata by namespace" ON app_metadata
  FOR SELECT USING (namespace_id = current_setting('app.namespace_id', TRUE));
```

### 2.3 Merge Logic Layer

Implement a `ShowMergeService` that handles merge rules:
- **Non-my fields**: `selectFirstNonEmpty(newValue, oldValue)` - never overwrite with empty/nil
- **My fields**: resolve by timestamp - keep the most recent `*_update_date`
- **Catalog refresh**: only update catalog fields, preserve user data
- **Details update**: set `detailsUpdateDate = now()` after merge

### 2.4 Namespace & User Context

**Middleware layer** to inject isolation context:
```typescript
// Namespace isolation via environment variable or header
const namespace_id = process.env.NAMESPACE_ID || req.headers['x-namespace-id'];

// User identity (dev mode via header, prod via auth)
const user_id = process.env.DEV_USER_ID ||
                req.headers['x-user-id'] ||
                session.user.id;

// Set in Supabase session
await supabase.rpc('set_config', { name: 'app.namespace_id', value: namespace_id });
```

---

## 3. TypeScript Type System

### 3.1 Core Types

```typescript
// src/types/show.ts
export type ShowType = 'movie' | 'tv' | 'person' | 'unknown';
export type MyStatusType = 'active' | 'next' | 'later' | 'done' | 'quit' | 'wait';
export type MyInterestType = 'excited' | 'interested';

export interface Show {
  id: string;
  title: string;
  showType: ShowType;
  externalIds?: Record<string, string> | null;

  // Catalog metadata
  overview?: string | null;
  genres: string[];
  tagline?: string | null;

  homepage?: string | null;
  originalLanguage?: string | null;
  spokenLanguages: string[];
  languages: string[];

  posterUrlString?: string | null;
  backdropUrlString?: string | null;
  logoUrlString?: string | null;
  networkLogos: string[];

  voteAverage?: number | null;
  voteCount?: number | null;
  popularity?: number | null;

  lastAirDate?: string | null;
  firstAirDate?: string | null;
  releaseDate?: string | null;

  runtime?: number | null;
  budget?: number | null;
  revenue?: number | null;

  seriesStatus?: string | null;
  numberOfEpisodes?: number | null;
  numberOfSeasons?: number | null;
  episodeRunTime: number[];
  lastEpisodeRunTime?: number | null;

  // User overlay
  myTags: string[];
  myTagsUpdateDate?: string | null;
  myScore?: number | null;
  myScoreUpdateDate?: string | null;
  myStatus?: MyStatusType | null;
  myStatusUpdateDate?: string | null;
  myInterest?: MyInterestType | null;
  myInterestUpdateDate?: string | null;

  // AI data
  aiScoop?: string | null;
  aiScoopUpdateDate?: string | null;

  // Metadata
  detailsUpdateDate?: string | null;
  creationDate?: string | null;
  isTest: boolean;

  // Provider data (opaque blob)
  provider?: Record<string, unknown> | null;
}

export type FilterType =
  | 'all'
  | 'genre'
  | 'myStatus'
  | 'communityScore'
  | 'decade'
  | 'myTag';

export interface FilterConfiguration {
  type: FilterType;
  label: string;
  value: string;
}
```

---

## 4. Directory Structure (Fractal Architecture)

```
src/
├── config/
│   ├── constants.ts          # App-wide constants
│   ├── env.ts               # Environment variable management
│   └── ai-prompts.ts        # AI prompt templates
├── theme/
│   ├── colors.ts            # Design tokens
│   ├── spacing.ts
│   ├── typography.ts
│   └── index.ts             # Theme provider
├── components/
│   ├── ui/                  # Primitives (Button, Card, Badge, etc.)
│   ├── show-tile/           # Show tile component
│   ├── poster-carousel/     # Media carousel for detail pages
│   └── rating-slider/      # Rating input component
├── hooks/
│   ├── use-namespace.ts    # Namespace context hook
│   ├── use-user.ts         # User identity hook
│   └── use-ai-provider.ts  # AI service hook
├── utils/
│   ├── date.ts             # Date formatting helpers
│   ├── merge.ts            # Show merge logic
│   ├── catalog.ts          # Catalog API client
│   └── export.ts           # Data export utilities
├── lib/
│   ├── supabase.ts         # Supabase client
│   ├── ai-service.ts       # AI integration
│   └── catalog-service.ts  # Catalog service
└── pages/
    ├── home/
    │   ├── Home.tsx
    │   └── features/
    │       ├── collection-grid/
    │       │   ├── CollectionGrid.tsx
    │       │   ├── hooks/
    │       │   │   └── useCollectionGrid.ts
    │       │   └── utils/
    │       │       └── groupByStatus.ts
    │       ├── filter-sidebar/
    │       │   ├── FilterSidebar.tsx
    │       │   └── utils/
    │       │       └── buildFilters.ts
    │       └── my-data-chips/
    │           ├── MyDataChips.tsx
    │           └── hooks/
    │               └── useStatusUpdate.ts
    ├── show-detail/
    │   ├── ShowDetail.tsx
    │   └── features/
    │       ├── header-media/
    │       │   ├── HeaderMedia.tsx
    │       │   └── hooks/
    │       │       └── useMediaAssets.ts
    │       ├── status-toolbar/
    │       │   ├── StatusToolbar.tsx
    │       │   ├── hooks/
    │       │   │   └── useStatusUpdate.ts
    │       │   └── utils/
    │       │       └── autoSave.ts
    │       ├── scoop-section/
    │       │   ├── ScoopSection.tsx
    │       │   ├── hooks/
    │       │   │   └── useScoop.ts
    │       │   └── utils/
    │       │       └── cacheCheck.ts
    │       ├── explore-similar/
    │       │   ├── ExploreSimilar.tsx
    │       │   ├── features/
    │       │   │   ├── concept-picker/
    │       │   │   │   ├── ConceptPicker.tsx
    │       │   │   │   └── hooks/
    │       │   │   │       └── useConcepts.ts
    │       │   │   └── show-recommendations/
    │       │   │       ├── ShowRecommendations.tsx
    │       │   │       └── hooks/
    │       │   │           └── useConceptRecs.ts
    │       │   └── hooks/
    │       │       └── useExploreSimilar.ts
    │       ├── traditional-recs/
    │       │   ├── TraditionalRecs.tsx
    │       │   └── hooks/
    │       │       └── useTraditionalRecs.ts
    │       ├── cast-crew/
    │       │   ├── CastCrew.tsx
    │       │   └── hooks/
    │       │       └── useCastCrew.ts
    │       ├── streaming-providers/
    │       │   ├── StreamingProviders.tsx
    │       │   └── hooks/
    │       │       └── useProviders.ts
    │       └── budget-revenue/    # Movies only
    │           ├── BudgetRevenue.tsx
    │           └── hooks/
    │               └── useBudgetRevenue.ts
    ├── find/
    │   ├── Find.tsx
    │   └── features/
    │       ├── mode-switcher/
    │       │   ├── ModeSwitcher.tsx
    │       │   └── hooks/
    │       │       └── useModeNavigation.ts
    │       ├── search/
    │       │   ├── Search.tsx
    │       │   ├── hooks/
    │       │   │   └── useCatalogSearch.ts
    │       │   └── features/
    │       │       └── search-results/
    │       │           ├── SearchResults.tsx
    │       │           └── utils/
    │       │               └── mergeWithCollection.ts
    │       ├── ask/
    │       │   ├── Ask.tsx
    │       │   ├── features/
    │       │   │   ├── chat-interface/
    │       │   │   │   ├── ChatInterface.tsx
    │       │   │   │   ├── hooks/
    │       │   │   │   │   ├── useAskChat.ts
    │       │   │   │   │   └── useContextSummary.ts
    │       │   │   │   └── utils/
    │       │   │   │       ├── parseMentions.ts
    │       │   │   │       └── showListParser.ts
    │       │   │   ├── mentioned-shows/
    │       │   │   │   ├── MentionedShows.tsx
    │       │   │   │   └── hooks/
    │       │   │   │       └── useResolveMentions.ts
    │       │   │   └── starter-prompts/
    │       │   │       ├── StarterPrompts.tsx
    │       │   │       └── hooks/
    │       │   │           └── useRandomPrompts.ts
    │       │   └── hooks/
    │       │       └── useAskSession.ts
    │       └── alchemy/
    │           ├── Alchemy.tsx
    │           ├── features/
    │           │   ├── show-selector/
    │           │   │   ├── ShowSelector.tsx
    │           │   │   ├── hooks/
    │           │   │   │   └── useShowSelection.ts
    │           │   │   └── utils/
    │           │   │       └── mergeCatalogAndLibrary.ts
    │           │   ├── concept-extraction/
    │           │   │   ├── ConceptExtraction.tsx
    │           │   │   ├── hooks/
    │           │   │   │   └── useConceptExtraction.ts
    │           │   │   └── utils/
    │           │   │       └── filterSharedConcepts.ts
    │           │   ├── concept-picker/
    │           │   │   ├── ConceptPicker.tsx
    │           │   │   └── hooks/
    │           │   │       └── useConceptSelection.ts
    │           │   └── alchemy-results/
    │           │       ├── AlchemyResults.tsx
    │           │       ├── hooks/
    │           │       │   └── useAlchemyResults.ts
    │           │       └── utils/
    │           │           └── resolveRecShows.ts
    │           └── hooks/
    │               ├── useAlchemyFlow.ts
    │               └── useChaining.ts
    ├── person-detail/
    │   ├── PersonDetail.tsx
    │   └── features/
    │       ├── profile-header/
    │       │   ├── ProfileHeader.tsx
    │       │   └── hooks/
    │       │       └── usePersonData.ts
    │       ├── analytics-charts/
    │       │   ├── AnalyticsCharts.tsx
    │       │   ├── hooks/
    │       │   │   └── usePersonAnalytics.ts
    │       │   └── features/
    │       │       ├── ratings-chart/
    │       │       ├── genres-chart/
    │       │       └── projects-by-year/
    │       └── filmography/
    │           ├── Filmography.tsx
    │           ├── hooks/
    │           │   └── useFilmography.ts
    │           └── utils/
    │               └── groupByYear.ts
    └── settings/
        ├── Settings.tsx
        └── features/
            ├── app-settings/
            │   ├── AppSettings.tsx
            │   ├── hooks/
            │   │   └── useAppSettings.ts
            │   └── utils/
            │       └── fontSizeOptions.ts
            ├── ai-settings/
            │   ├── AISettings.tsx
            │   ├── hooks/
            │   │   └── useAISettings.ts
            │   └── utils/
            │       └── modelOptions.ts
            ├── export-import/
            │   ├── ExportImport.tsx
            │   ├── hooks/
            │   │   └── useExport.ts
            │   └── utils/
            │       ├── prepareExport.ts
            │       └── createZip.ts
            └── about/
                └── About.tsx
```

---

## 5. Core Services

### 5.1 AI Service (`lib/ai-service.ts`)

```typescript
interface AIService {
  // Scoop generation
  generateScoop(show: Show, userLibrary?: Show[]): Promise<string>;

  // Ask chat
  chat(
    messages: Message[],
    userLibrary: Show[],
    showContext?: Show
  ): Promise<{
    commentary: string;
    showList: string; // "Title::id::type;;Title2::id::type;;..."
  }>;

  // Concept generation
  extractConcepts(shows: Show[]): Promise<string[]>; // Single show
  extractSharedConcepts(shows: Show[]): Promise<string[]>; // Multi-show (Alchemy)

  // Recommendations
  getConceptRecs(
    concepts: string[],
    userLibrary: Show[],
    contextShow?: Show
  ): Promise<Array<{ show: Show; reason: string }>>;

  // Context summary
  summarizeConversation(messages: Message[]): Promise<string>;
}
```

**Prompt Templates** stored in `src/config/ai-prompts.ts`:
- Scoop prompt: structured output with personal take, stack-up, scoop paragraph, fit/warnings, verdict
- Ask persona: water cooler gossip + critic brain + hype friend
- Concept extraction: 1-3 word evocative ingredients, spoiler-free
- concept rec prompt: excited, detailed reasons naming the concept match

### 5.2 Catalog Service (`lib/catalog-service.ts`)

```typescript
interface CatalogService {
  search(query: string, page?: number): Promise<Show[]>;
  getShowDetails(id: string): Promise<Show>;
  getCastCrew(id: string): Promise<{ cast: Person[]; crew: Person[] }>;
  getSeasons(id: string): Promise<Season[]>;
  getVideos(id: string): Promise<Video[]>;
  getRecommendations(id: string): Promise<Show[]>;
  getSimilar(id: string): Promise<Show[]>;
  getPerson(id: string): Promise<Person>;
  getPersonCredits(id: string): Promise<Credit[]>;
  resolveShow(externalId: string, title: string): Promise<Show | null>;
}
```

**Note:** Resolve show uses title case-insensitive match on externalId lookup; if not found, return null for non-interactive display.

### 5.3 Data Service (`lib/data-service.ts`)

Handles all Supabase operations with namespace/user context:

```typescript
interface DataService {
  // Shows
  getShows(namespace_id: string, user_id: string, filter?: FilterConfiguration): Promise<Show[]>;
  getShow(id: string, namespace_id: string, user_id: string): Promise<Show | null>;
  upsertShow(show: Show, namespace_id: string, user_id: string): Promise<void>;
  deleteShow(id: string, namespace_id: string, user_id: string): Promise<void>;

  // Settings
  getCloudSettings(namespace_id: string, user_id: string): Promise<CloudSettings | null>;
  updateCloudSettings(settings: Partial<CloudSettings>): Promise<void>;

  // Metadata
  getDataModelVersion(namespace_id: string): Promise<number>;

  // Bulk operations
  exportUserData(namespace_id: string, user_id: string): Promise<StorageSnapshot>;
  importUserData(snapshot: StorageSnapshot, namespace_id: string, user_id: string): Promise<void>;
}
```

### 5.4 Show Merge Service (`lib/merge-service.ts`)

```typescript
interface MergeService {
  mergeCatalogIntoStored(catalogShow: Show, storedShow: Show): Show;
}
```

Implementation of merge rules:
- Non-my fields: `selectFirstNonEmpty(newValue, oldValue)`
- My fields: compare `*_update_date` timestamps, keep newer
- Set `detailsUpdateDate = now()`

---

## 6. Feature Implementation Plans

### 6.1 Collection Home (`pages/home/`)

**Purpose:** Display user's library organized by status.

**Key Behaviors:**
- Group shows by status: Active (prominent), Excited, Interested, Other (Wait/Quit/Done/uncategorized Later)
- Apply filter from sidebar (all shows, tag filters, data filters)
- Media type toggle (All/Movies/TV)
- Show tiles with poster, title, and My Data badges

**Implementation Steps:**
1. Create `CollectionGrid` component with status grouping logic
2. Implement `FilterSidebar` that builds available filters from collection
   - Tag filters: one per tag + "No tags" if applicable
   - Data filters: genre, decade, community score ranges
3. Create `MyDataChips` for quick status/interest updates
4. Implement `useCollectionGrid` hook that:
   - Fetches shows from `data-service`
   - Applies filter configuration
   - Groups by status
   - Handles media type toggle

**Data Query:**
```sql
SELECT * FROM shows
WHERE namespace_id = $1
  AND my_status IS NOT NULL  -- In collection
ORDER BY my_status_update_date DESC;
```

### 6.2 Search (`pages/find/features/search/`)

**Purpose:** Find shows in global catalog.

**Key Behaviors:**
- Text search by title/keywords
- Results in poster grid
- In-collection items marked (via `myStatus` badge)
- Open Detail on selection

**Implementation Steps:**
1. Create `Search` page with search input and results grid
2. Implement `useCatalogSearch` hook that:
   - Debounces search input
   - Calls `catalogService.search()`
   - Merges results with user collection to mark saved items
   - Paginates results (load more on scroll)

**Data Flow:**
```
User input → useCatalogSearch → CatalogService.search()
  → Merge with local collection → Display in SearchResults
```

### 6.3 Ask (`pages/find/features/ask/`)

**Purpose:** Conversational discovery grounded in taste.

**Key Behaviors:**
- Chat UI with user/assistant turns
- Friendly, opinionated, spoiler-safe tone
- AI mentions shows inline → appear in "mentioned shows" strip
- Tapping mentioned show opens Detail (or hands off to Search if mapping fails)
- Welcome view with 6 random starter prompts (refreshable)
- Conversation context retained, older turns summarized after ~10 messages
- Two variants:
  - General Ask from Find
  - Ask About a Show from Detail (seeds conversation with show context)

**Implementation Steps:**
1. Create `ChatInterface` component with:
   - Message list (user/assistant)
   - Input field with send button
   - Loading states
2. Implement `useAskChat` hook that:
   - Manages message list
   - Calls `aiService.chat()` with context
   - Parses response for `commentary` and `showList`
   - Summarizes old turns after threshold
3. Implement `parseMentions` utility:
   - Parse `showList` string format: `"Title::externalId::mediaType;;..."`
   - Resolve each show via `catalogService.resolveShow()`
   - Return list of show objects or null for unresolvable
4. Create `MentionedShows` horizontal strip showing resolved shows
5. Implement `useRandomPrompts` for welcome view (80 starter prompts in config)

**Data Context Sent to AI:**
```
{
  messages: Message[] (chat history, summarized),
  userLibrary: Show[] (all saved shows with My Data),
  showContext?: Show (seed for 'Ask about this')
}
```

**Prompt Template (Ask persona):**
```
You are a fun, chatty TV/movie nerd friend. You love entertainment deeply and show it,
have sharp taste and aren't afraid to make a call, are generous with context and insider
info, stay spoiler-safe unless invited otherwise, and keep things light even when critical.

Rules:
- Stay within TV/movies
- Be spoiler-safe by default
- Be opinionated and honest (say if reception is mixed)
- Use specific, vibe/structure/craft-based reasoning
- Mention shows inline so we can make them selectable

Output format (JSON only):
{
  "commentary": "...",  // Your response text
  "showList": "Title::externalId::mediaType;;Title2::externalId::mediaType;;..."
}

External ID: Use the TMDB ID if available.
Media Type: "movie" or "tv"
```

### 6.4 Alchemy (`pages/find/features/alchemy/`)

**Purpose:** Structured blending discovery.

**Flow:**
1. User selects 2+ starting shows (from library + global catalog)
2. Tap "Conceptualize Shows" → AI extracts shared concept catalysts
3. User selects 1–8 concepts
4. Tap "ALCHEMIZE!" → AI returns 6 recommendations with reasons
5. Optionally chain another round using results as inputs

**Implementation Steps:**
1. Create `ShowSelector` component:
   - Searchable list of shows (library + catalog)
   - Multi-select with removal
   - Minimum 2, no maximum
2. Implement `useShowSelection` hook:
   - Fetches user library
   - Integrates catalog search for additional shows
   - Tracks selected show IDs
3. Create `ConceptExtraction` component:
   - Step-by-step progress indicator
   - "Conceptualize Shows" button
   - Loading state
   - Display generated concepts as selectable chips (max 8 selection)
4. Implement `useConceptExtraction` hook:
   - Calls `aiService.extractSharedConcepts(selectedShows)`
   - Validates concepts (1-3 words, evocative, no generic)
   - Tracks selected concepts
5. Create `AlchemyResults` component:
   - 6 show tiles with AI reasoning
   - "More Alchemy!" button to chain
6. Implement `useAlchemyResults` hook:
   - Calls `aiService.getConceptRecs(concepts, userLibrary)`
   - Resolves recommendations to real show objects via `catalogService.resolveShow()`
   - Handles chaining (use results as new inputs)

**AI Context:**
```
{
  shows: Show[] (selected input shows),
  userLibrary: Show[] (saved shows with My Data)
}
```

**Concept Extraction Prompt:**
```
Extract 8-12 short, evocative concept "ingredients" that capture the SHARED feeling
across these shows.

Rules:
- Each concept: 1-3 words maximum
- Focus on: vibe, structure, emotional temperature, style, craft
- AVOID: plot details, spoilers, generic placeholders like "good characters"
- Output ONLY bullet list

Examples of good: "hopeful absurdity", "case-a-week", "quirky makeshift family", "light in dark moments"
Examples of bad: "good writing", "great characters", "funny", "action"
```

**Recommendation Prompt:**
```
Given these concepts, recommend 6 shows from the catalog (including recent releases,
classics, and hidden gems).

For each recommendation:
1. Title + external ID (TMDB) + media type (movie/tv)
2. A 1-3 sentence reason that explicitly names which concept(s) it matches and how

Requirements:
- Output excited, detailed reasoning
- Specific about the concept match
- Use format: {"shows": [{"title": "...", "externalId": "...", "mediaType": "...", "reason": "..."}, ...]}

Context: User's library and tastes are provided for grounding.
```

### 6.5 Show Detail (`pages/show-detail/`)

**Purpose:** Single source of truth for a show with My Data + discovery.

**Narrative Order (preserved):**
1. Header media carousel (backdrops/posters/logos/trailers)
2. Core facts row (year/length) + community score
3. My Tags display
4. Overview text + Scoop toggle/stream
5. "Ask about this show" CTA
6. Genres + languages
7. Traditional recommendations strand
8. Explore Similar (concepts → recs)
9. Streaming availability ("Stream It")
10. Cast & Crew
11. Seasons (TV only)
12. Budget/Revenue (movies when available)

**Implementation Steps:**

#### 5.1 Header Media
- Create `HeaderMedia` component with carousel
- Load poster, backdrop, logo, and videos (if available)
- Graceful fallback: if no video, show image carousel
- Use `useMediaAssets` hook to fetch assets

#### 5.2 Core Facts + Community Score
- Display row with year, runtime or seasons/episodes
- Community score bar (star rating or similar)

#### 5.3 My Relationship Controls (Status Toolbar)
- Create `StatusToolbar` component:
  - Status chips: Active / Interested / Excited / Done / Quit / Wait
  - Interested/Excited map to `Later + Interest`
  - Rating slider for `myScore` (0-10 or similar)
- Implement `useStatusUpdate` hook:
  - Setting status saves show (auto-save if not saved)
  - Clearing status (reselecting active) triggers confirmation
  - Rating unsaved show auto-saves as `Done`
- `autoSave` utility handles default values:
  - Default status: `Later`
  - Default interest: `Interested`
  - Exception: rating defaults to `Done`

#### 5.4 Overview + Scoop
- Display overview text
- Create `ScoopSection` component:
  - Toggle button: "Give me the scoop!" → "Show the scoop"
  - Streams in progressively (user sees "Generating...")
  - Cache freshness: regenerate after ~4 hours on demand
- Implement `useScoop` hook:
  - Checks `aiScoopUpdateDate` for freshness
  - Calls `aiService.generateScoop(show, userLibrary)` if needed
  - Persists `aiScoop` only if show is in collection

**Scoop Prompt Structure:**
```
You're writing a "mini blog post of taste" for this TV show or movie.

Tone: Gossipy, vivid, and useful—like a trusted friend's review.

Structure your response as:
1. First paragraph: Your personal take—take a stand.
2. Paragraph 2: Honest stack-up vs community reviews (don't gush if it's mixed).
3. Paragraph 3 (The Scoop): Emotional centerpiece—what you really think.
4. Paragraph 4: Practical fit + warnings (who this is for, who might hate it).
5. Final line: "Worth it?" gut check.

Rules:
- Spoiler-safe unless spoiler explicitly requested
- Use specific texture (pacing, writing intelligence, music/cinematography)
- Opinionated honesty—acknowledge mixed reception when relevant
- Length: ~150-350 words total

Context: User's library and tastes are provided for guidance.
```

#### 5.5 Ask About This Show
- CTA button that:
  - Navigates to Ask page
  - Seeds conversation with this show's context

#### 5.6 Traditional Recommendations
- Create `TraditionalRecs` component:
  - Horizontal strand of similar/recommended shows
  - Uses `catalogService.getRecommendations()` or similar
  - Mark in-collection items

#### 5.7 Explore Similar (Concept Discovery)
- Create `ExploreSimilar` component:
  - "Get Concepts" button
  - `ConceptPicker` (shared with Alchemy) for selecting concepts
  - "Explore Shows" button
  - `ShowRecommendations` component with 5 recs
- Implement `useExploreSimilar` hook:
  - Extracts concepts via `aiService.extractConcepts([show])`
  - Gets recommendations via `aiService.getConceptRecs(concepts, userLibrary, contextShow)`
  - Resolves to real shows and display

**Concept Extraction (Single Show):**
Same multi-show prompt but applied to one show, returning 8-12 concepts.

#### 5.8 Streaming Availability
- Create `StreamingProviders` component:
  - Display streaming services by region
  - Use `providerData` from show object
  - Map provider IDs to names/app links

#### 5.9 Cast & Crew
- Create `CastCrew` component:
  - Horizontal strands for cast and crew
  - Each person card with image, name, role
  - Tap opens Person Detail
- Use `useCastCrew` hook to fetch from catalog

#### 5.10 Seasons (TV only)
- Display season list if `showType === 'tv'`
- Show episode counts, air dates
- Tap to open season detail (optional, can link to external)

#### 5.11 Budget/Revenue (Movies only)
- Display if data available
- Simple comparison view

### 6.6 Person Detail (`pages/person-detail/`)

**Purpose:** Explore talent behind shows.

**Implementation Steps:**
1. Create `ProfileHeader` component:
   - Image gallery, name, bio
   - Use `usePersonData` hook
2. Create `AnalyticsCharts` component:
   - Average project ratings (line/bar chart)
   - Top genres (pie/bar chart)
   - Projects-by-year (timeline)
   - Sub-features for each chart
3. Create `Filmography` component:
   - Credits grouped by year
   - Each credit as clickable show tile
   - Use `useFilmography` hook with `groupByYear` utility

**Data Flow:**
```
Person ID → PersonService.getPerson() → Header
Person ID → PersonService.getCredits() → Filmography, Analytics
```

### 6.7 Settings (`pages/settings/`)

**Purpose:** User preferences, AI configuration, data export/import.

**Sections:**

#### 7.1 App Settings
- Font size selector (XS/S/M/L/XL/XXL)
- "Search on launch" toggle
- Implement `useAppSettings` hook

#### 7.2 AI Settings
- AI provider API key (synced if enabled)
- AI model selector (dropdown)
- NEVER commit API keys to repo
- Implement `useAISettings` hook

#### 7.3 Export/Import
- "Export My Data" button:
  - Generates `.zip` with JSON backup
  - Includes all saved shows and My Data
  - ISO-8601 date encoding
  - Use `useExport` hook
  - `prepareExport` utility formats data as `StorageSnapshot`
  - `createZip` utility creates downloadable zip
- Import/Restore:
  - Desired but not currently implemented (open question)

#### 7.4 About
- App info, version, links

---

## 7. Cross-Cutting Features

### 7.1 Auto-Save Behaviors

**Triggers for save:**
- Setting any Status
- Choosing Interest chip (Interested/Excited)
- Rating an unsaved show
- Adding at least one tag to an unsaved show

**Default values:**
- Status: `Later` (unless first save via rating → `Done`)
- Interest: `Interested`

**Implementation:**
Centralize in `pages/show-detail/features/status-toolbar/utils/autoSave.ts`:
```typescript
export async function autoSave(
  show: Show,
  field: 'status' | 'interest' | 'score' | 'tags',
  value: unknown,
  namespace_id: string,
  user_id: string
): Promise<Show> {
  const update: Partial<Show> = {};

  if (field === 'status') {
    update.myStatus = value;
    update.myStatusUpdateDate = new Date().toISOString();
    // If clearing status, remove show (with confirmation elsewhere)
  }

  if (field === 'interest') {
    update.myInterest = value;
    update.myInterestUpdateDate = new Date().toISOString();
    // Ensure show is in collection
    if (!show.myStatus) {
      update.myStatus = 'later';
      update.myStatusUpdateDate = new Date().toISOString();
    }
  }

  if (field === 'score') {
    update.myScore = value;
    update.myScoreUpdateDate = new Date().toISOString();
    // Rating unsaved show auto-saves as Done
    if (!show.myStatus) {
      update.myStatus = 'done';
      update.myStatusUpdateDate = new Date().toISOString();
    }
  }

  if (field === 'tags') {
    update.myTags = value as string[];
    update.myTagsUpdateDate = new Date().toISOString();
    // Adding tag to unsaved show auto-saves as Later + Interested
    if (!show.myStatus && (value as string[]).length > 0) {
      update.myStatus = 'later';
      update.myStatusUpdateDate = new Date().toISOString();
      update.myInterest = 'interested';
      update.myInterestUpdateDate = new Date().toISOString();
    }
  }

  const merged = mergeService.mergeCatalogIntoStored({ ...show, ...update }, show);
  await dataService.upsertShow(merged, namespace_id, user_id);
  return merged;
}
```

### 7.2 Filter System

**Types:**
- All Shows (default)
- Tag filters: one per tag, plus "No tags"
- Genre filters
- Decade filters
- Community score ranges
- Media type toggle (All/Movies/TV)

**Implementation:**
`pages/home/features/filter-sidebar/utils/buildFilters.ts`:
```typescript
export function buildFilters(shows: Show[]): FilterConfig[] {
  const configs: FilterConfig[] = [{ type: 'all', label: 'All Shows', value: '' }];

  // Tags
  const allTags = new Set<string>();
  for (const show of shows) {
    for (const tag of show.myTags) allTags.add(tag);
  }
  for (const tag of allTags) {
    configs.push({ type: 'myTag', label: tag, value: tag });
  }
  if (shows.some(s => s.myTags.length === 0 && s.myStatus)) {
    configs.push({ type: 'myTag', label: 'No tags', value: '' });
  }

  // Genres
  const allGenres = new Set<string>();
  for (const show of shows) {
    for (const genre of show.genres) allGenres.add(genre);
  }
  for (const genre of allGenres) {
    configs.push({ type: 'genre', label: genre, value: genre });
  }

  // Decades
  const decades = new Set<string>();
  for (const show of shows) {
    const year = show.releaseDate || show.firstAirDate;
    if (year) {
      const d = year.substring(0, 3) + '0s';
      decades.add(d);
    }
  }
  for (const decade of decades) {
    configs.push({ type: 'decade', label: decade, value: decade });
  }

  // Community score ranges
  configs.push(
    { type: 'communityScore', label: '8+ Stars', value: '8' },
    { type: 'communityScore', label: '7+ Stars', value: '7' },
    { type: 'communityScore', label: '6+ Stars', value: '6' }
  );

  return configs;
}
```

**Apply filter in `useCollectionGrid`:**
```typescript
function applyFilter(shows: Show[], filter: FilterConfig, mediaType?: 'all' | 'movie' | 'tv'): Show[] {
  return shows.filter(show => {
    // Media type
    if (mediaType === 'movie' && show.showType !== 'movie') return false;
    if (mediaType === 'tv' && show.showType !== 'tv') return false;

    // Filter type
    switch (filter.type) {
      case 'all':
        return true;
      case 'myTag':
        if (filter.value === '') return show.myTags.length === 0;
        return show.myTags.includes(filter.value);
      case 'genre':
        return show.genres.includes(filter.value);
      case 'decade':
        const year = show.releaseDate || show.firstAirDate;
        if (!year) return false;
        return year.startsWith(filter.value);
      case 'communityScore':
        return show.voteAverage !== undefined && show.voteAverage >= parseInt(filter.value);
      case 'myStatus':
        return show.myStatus === filter.value;
      default:
        return true;
    }
  });
}
```

### 7.3 Recommendation Resolution

**Critical:** All AI recommendations must map to real show objects for interactivity.

**Implementation (`pages/find/features/alchemy/features/alchemy-results/utils/resolveRecShows.ts`):**
```typescript
export async function resolveRecommendations(
  aiRecs: Array<{ title: string; externalId: string; mediaType: string; reason: string }>,
  catalogService: CatalogService
): Promise<Array<{ show: Show | null; reason: string }>> {
  const resolved = await Promise.all(
    aiRecs.map(async (rec) => {
      const show = await catalogService.resolveShow(rec.externalId, rec.title);
      return { show, reason: rec.reason };
    })
  );

  // Filter out unresolvable shows (or show as non-interactive)
  return resolved.filter(r => r.show !== null);
}
```

### 7.4 Export/Backup Data Format

**Storage Snapshot:**
```typescript
export interface StorageSnapshot {
  shows: Show[];
  cloudSettings?: CloudSettings | null;
  appMetadata?: AppMetadata | null;
  localSettings?: {
    autoSearch: boolean;
    fontSize: 'XS' | 'S' | 'M' | 'L' | 'XL' | 'XXL';
  } | null;
  uiState?: {
    hideStatusRemovalConfirmation?: boolean;
    statusRemovalCountKey?: number;
    lastSelectedFilter?: FilterConfiguration | null;
  } | null;
}
```

**Export Flow:**
```
"useExport" hook → dataService.exportUserData() → prepareExport() → createZip() → Download
```

Dates encoded as ISO-8601 strings.

### 7.5 Namespace & User ID Injection (Dev Mode)

**Middleware or API route:**
```typescript
// src/middleware.ts or app/api/validate-identity/route.ts

export async function validateIdentity(req: NextRequest) {
  const namespace = req.headers.get('x-namespace-id') || process.env.NAMESPACE_ID;
  const user = req.headers.get('x-user-id') || process.env.DEV_USER_ID;

  if (!namespace || !user) {
    throw new Error('Namespace and user identity required');
  }

  // Set in Supabase session via RPC
  await supabase.rpc('set_config', {
    name: 'app.namespace_id',
    value: namespace
  });

  return { namespace_id: namespace, user_id: user };
}
```

---

## 8. Environment Configuration

### 8.1 Required Environment Variables

`.env.example`:

```env
# Supabase (required)
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# Catalog API (e.g., TMDB)
NEXT_PUBLIC_CATALOG_API_URL=https://api.themoviedb.org/3
NEXT_PUBLIC_CATALOG_API_KEY=your_tmdb_key

# AI Provider (OpenAI, Anthropic, etc.)
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
NEXT_PUBLIC_AI_MODEL=gpt-4o

# Identity Injection (dev mode)
NAMESPACE_ID=benchmark-run-001
DEV_USER_ID=default-user

# App
NEXT_PUBLIC_APP_NAME=Entertainment Companion
NODE_ENV=development
```

**Security Rules:**
- `.env*` (except `.env.example`) in `.gitignore`
- Browser/client code uses `NEXT_PUBLIC_*` anon/public keys only
- Service role keys server-only

---

## 9. Testing Strategy

### 9.1 Unit Tests

**Test files adjacent to source files** (e.g., `utils.ts` → `utils.test.ts`):

- **Merge logic** (`lib/merge-service.test.ts`): Test merge rules for all field types
- **Filter logic** (`pages/home/features/filter-sidebar/utils/buildFilters.test.ts`): Test filter building and application
- **Parse mentions** (`pages/find/features/ask/features/chat-interface/utils/parseMentions.test.ts`): Test show list parsing
- **Show list parser** (`pages/find/features/ask/features/chat-interface/utils/showListParser.test.ts`): Test structured output parsing
- **Auto-save defaults** (`pages/show-detail/features/status-toolbar/utils/autoSave.test.ts`): Test default status/interest logic

**Framework:** Jest or Vitest

### 9.2 Integration Tests

- **Data layer** (`lib/data-service.test.ts`): Test CRUD operations with isolation
- **AI service** (`lib/ai-service.test.ts`): Mock AI responses, test prompt formatting
- **Catalog service** (`lib/catalog-service.test.ts`): Mock external API, test show resolution

### 9.3 End-to-End Tests

**Key User Journeys:** (from PRD)

1. Build collection
2. Rate-to-save
3. Tag-to-save
4. Maintain collection
5. Tag-driven organization
6. Ask discovery
7. Explore Similar
8. Alchemy
9. Talent deep-dive
10. Backup

**Framework:** Playwright or Cypress

**Setup:** Use namespace isolation to run tests without data collisions.

### 9.4 Test Data Management

**Reset script:** `npm run test:reset`

```sql
-- Reset namespace data (safe, no global teardown)
DELETE FROM shows WHERE namespace_id = $1;
DELETE FROM cloud_settings WHERE namespace_id = $1;
DELETE FROM app_metadata WHERE namespace_id = $1;
```

---

## 10. Migrations & Data Evolution

### 10.1 Migration Artifacts

Store migrations in `supabase/migrations/`:

```
supabase/migrations/
├── 001_initial_schema.sql
├── 002_add_indexes.sql
└── 003_data_model_v3_upgrade.sql
```

### 10.2 Data Model Versioning

Track `dataModelVersion` in `app_metadata` table. On startup, check version and run migrations if needed.

### 10.3 Data Continuity Rule

**Product Requirement:** Preserve user libraries across updates.

**Implementation:**
- Use column defaults and NOT NULL carefully
- Use explicit migration scripts for breaking changes
- Merge old data into new schema
- Never drop columns with user data

---

## 11. Development Scripts

**`package.json` scripts:**

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "typecheck": "tsc --noEmit",
    "test": "vitest",
    "test:reset": "node scripts/reset-test-data.js",
    "migrate": "supabase db push",
    "export": "node scripts/export-data.js"
  }
}
```

---

## 12. Open Questions & Decisions (from PRD)

1. **Should "Next" become a first-class status in UI?**
   - Currently present in data model but not surfaced
   - Decision: Keep as internal status, not primary chip

2. **Should users create named custom lists beyond tags?**
   - Current: Tags are free-form, no named lists
   - Decision: Deferred (optional extension)

3. **Should generating AI Scoop on an unsaved show implicitly save it?**
   - Current: Scoop persists only if show is in collection
   - Decision: No change (keep current behavior)

4. **Should clearing My Rating store an explicit "Unrated" state vs nil?**
   - Decision: Use nil (null) to represent unrated

5. **Add Import/Restore from export zip:**
   - Current: Export only
   - Decision: Implement in Phase 2

6. **Support saving/sharing Alchemy sessions as reusable "blends":**
   - Decision: Deferred (optional extension)

7. **Add explicit myStatus filters in sidebar:**
   - Model supports it, UI doesn't expose all
   - Decision: Keep current filter system, could add later

---

## 13. Implementation Phases

### Phase 1: Foundation (Weeks 1-2)

**Goal:** Basic data layer + core navigation + collection home

- Set up Next.js project with TypeScript
- Configure Supabase client and RLS policies
- Implement database schema and migrations
- Create `DataService` with CRUD operations
- Implement `MergeService` for merge logic
- Create `CatalogService` for external catalog
- Build Home page with Collection Grid
- Implement Status/Interest/Tag update flows
- Build Filter sidebar with basic filters

**Deliverables:**
- Working database with namespace/user isolation
- Home page showing collection grouped by status
- Ability to save/update shows and tags
- Filter system (all, tags, genres, decades)

### Phase 2: Discovery Core (Weeks 3-4)

**Goal:** Search + Show Detail + AI Scoop

- Implement Search page with catalog integration
- Build Show Detail page with Core Facts, Overview, Status Toolbar
- Implement `AIService` with Scoop generation
- Add Scoop section to Detail page with caching
- Create Cast & Crew sections
- Add Streaming Providers
- Implement Traditional Recommendations

**Deliverables:**
- Search for shows in global catalog
- Complete Show Detail page (except Explore Similar)
- AI Scoop with freshness caching
- Cast/Crew and streaming sections

### Phase 3: AI Discovery (Weeks 5-6)

**Goal:** Ask + Concepts + Explore Similar

- Implement Ask page with chat UI
- Build `ChatInterface` with message history
- Implement mention parsing and "mentioned shows" strip
- Add starter prompts
- Build concept extraction (single-show)
- Implement Explore Similar (concepts → recs)
- Add concept picker component

**Deliverables:**
- Working Ask chat with taste-aware responses
- Mentioned shows linking to Detail/Search
- Explore Similar with concept extraction and recommendations

### Phase 4: Alchemy (Weeks 7-8)

**Goal**: Multi-show concept blending

- Implement Show Selector (library + catalog)
- Build Concept Extraction for multi-show (shared concepts)
- Create concept picker (max 8)
- Implement Alchemy Results with 6 recs
- Add "More Alchemy!" chaining

**Deliverables:**
- Complete Alchemy flow from show selection to recs
- Shared concept generation across multiple shows
- Concept-based recommendation pipeline
- Chaining capability

### Phase 5: Person Detail + Polish (Weeks 9-10)

**Goal:** Person profiles + export/import + settings

- Build Person Detail page
- Implement Profile Header with image gallery
- Add Analytics Charts (ratings, genres, projects-by-year)
- Create Filmography section
- Implement Settings pages (app, AI)
- Add Export/Backup functionality
- Add Import/Restore (if time)
- Polish UI and error states

**Deliverables:**
- Working Person Detail page
- Analytics and filmography sections
- Complete Settings interface
- Data export/backup
- Refined UI/UX

### Phase 6: Testing & Launch (Weeks 11-12)

**Goal:** Quality assurance + deployment prep

- Write unit tests for critical logic (merge, filters, parsing)
- Add integration tests for data layer
- Implement E2E tests for key user journeys
- Fix bugs and edge cases
- Performance optimization
- Prepare deployment configuration
- Documentation (setup, deployment, env vars)

**Deliverables:**
- Test coverage for core functionality
- Stable production build
- Deployment guide
- Completed benchmark submission

---

## 14. Success Criteria

Build is successful if:

✅ User can add shows to collection via Search/Ask/Alchemy/Detail
✅ User's My Data (status, tags, rating) displays on all show tiles
✅ AI surfaces (Scoop, Ask, Alchemy, Explore Similar) feel consistent and on-brand
✅ All AI recommendations map to real, selectable shows
✅ Namespace isolation prevents data collisions between test runs
✅ All user-owned records are scoped to `user_id`
✅ Destructive tests can run without global database teardown
✅ Data export produces complete backup with ISO-8601 dates
✅ Settings sync across devices (if enabled)
✅ Migrations preserve user data across versions
✅ Code passes lint and typecheck
✅ Critical logic has unit tests

---

## 15. Deviation Notes

This plan follows the PRD specifications with intentional decisions:

1. **No Next status in UI**: Kept as internal status only
2. **Export only, Import deferred**: Implement Import in Phase 2 extension
3. **Custom lists via tags only**: No named lists extension
4. **AI Scoop persistence**: Only for shows in collection (current behavior unchanged)
5. **Unrated as null**: Stored as `null` instead of explicit `"unrated"`

All other requirements from PRD and supporting docs are preserved.

---

**End of Implementation Plan**
