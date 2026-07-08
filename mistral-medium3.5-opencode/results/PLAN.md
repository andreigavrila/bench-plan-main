# Implementation Plan: Personal TV + Movie Companion App

## Executive Summary

Build a personal TV and movie companion application for collecting, organizing, rating, and discovering entertainment. The app enables users to build their personalized version of each show (status, interest, tags, rating, AI-generated scoop) and uses that taste profile to power multiple discovery paths: traditional search/browse, conversational AI (Ask), Alchemy blending based on shared concepts, and per-show Explore Similar via AI concepts.

**Core Value Proposition:** Make a user's taste visible and actionable through a clean personal library and smart, personalized discovery grounded in that library.

---

## 1. Architecture Overview

### 1.1 Technology Stack (Benchmark Baseline)
- **Framework:** Next.js (latest stable) for UI + server boundary
- **Persistence:** Supabase as the persistence layer, accessed via official client libraries
- **Authentication:** Development identity injection mechanism (X-User-Id header or dev-only selector)
- **AI Provider:** Configurable via environment variables (API key + model selection)
- **Catalog Provider:** External content catalog API (configurable via environment variables)

### 1.2 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client (Next.js)                            │
├─────────────────────────────────────────────────────────────────┤
│  UI Layers:                                                      │
│  - Pages: Home, Find/Discover, Detail, Person, Settings            │
│  - Components: Filters, Tiles, Status Chips, Rating, Tags, etc.    │
│  - State: Local cache for performance (disposable)               │
│  - AI Integration: Chat, Concepts, Recommendations                │
└─────────────────────────────┬───────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Server Layer (Next.js API)                    │
├─────────────────────────────────────────────────────────────────┤
│  - REST/GraphQL endpoints for CRUD operations                       │
│  - AI service integration (prompt engineering, response parsing)  │
│  - Catalog service integration (external API calls)             │
│  - Authentication handling (dev injection + OAuth-ready)          │
│  - Namespace/user isolation logic                                 │
└─────────────────────────────┬───────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Supabase (Hosted or Local)                    │
├─────────────────────────────────────────────────────────────────┤
│  - tables: shows, cloud_settings, app_metadata                      │
│  - Row-level security for namespace + user_id isolation            │
│  - Real-time subscriptions (optional for future enhancements)    │
└─────────────────────────────────────────────────────────────────┘
```

### 1.3 Data Flow Diagram

```
User Actions → Client UI → Server API → Supabase
                    ↑          ↑
                    │          │
                    ▼          ▼
              Local Cache   AI Provider + Catalog Provider
```

---

## 2. Core Data Model

### 2.1 Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        SHOW                                        │
├─────────────────────────────────────────────────────────────────┤
│ PK: id                                                               │
│.UK: (namespace_id, user_id, id)                                     │
│                                                                      │
│  Identity:                                                           │
│  - id (String, required)                                             │
│  - title (String, required)                                         │
│  - showType (Enum: movie | tv | person | unknown)                   │
│  - externalIds (Map<string, string>)                                │
│                                                                      │
│  Catalog Metadata:                                                  │
│  - overview, tagline, homepage                                       │
│  - genres (String[]), languages (String[])                          │
│  - voteAverage, voteCount, popularity (Numbers)                     │
│  - releaseDate, firstAirDate, lastAirDate (ISO dates)              │
│  - runtime, budget, revenue (movie-specific)                        │
│  - seriesStatus, numberOfEpisodes, numberOfSeasons (TV-specific)    │
│  - posterUrlString, backdropUrlString, logoUrlString               │
│  - providerData (JSONB: country → {flatrate[], rent[], buy[]})      │
│                                                                      │
│  User Data (My Data):                                               │
│  - myStatus (Enum: active | next | later | done | quit | wait)      │
│  - myInterest (Enum: excited | interested) *only valid when later*│
│  - myTags (String[])                                                 │
│  - myScore (Number: 0-10 or null for unrated)                       │
│  - aiScoop (String) *persisted only if in collection*              │
│                                                                      │
│  Timestamps:                                                        │
│  - myStatusUpdateDate, myInterestUpdateDate, myTagsUpdateDate      │
│  - myScoreUpdateDate, aiScoopUpdateDate, detailsUpdateDate        │
│  - creationDate                                                     │
│                                                                      │
│  Management:                                                        │
│  - isTest (Boolean)                                                 │
│  - namespace_id (String, required) *partition key*                  │
│  - user_id (String, required) *user scopes all records*             │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     CLOUD_SETTINGS                                  │
├─────────────────────────────────────────────────────────────────┤
│ PK: (namespace_id, id)                                              │
│  - id (String, default: "globalSettings")                          │
│  - userName (String)                                                │
│  - version (Int: epoch seconds for conflict resolution)           │
│  - catalogApiKey (String), aiApiKey (String)                       │
│  - aiModel (String)                                                 │
│  - namespace_id (String, required)                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      APP_METADATA                                   │
├─────────────────────────────────────────────────────────────────┤
│ PK: (namespace_id, id)                                              │
│  - id (String, default: "metadata")                                │
│  - dataModelVersion (Int, default: 3)                              │
│  - namespace_id (String, required)                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    PERSON (derived from Show)                       │
├─────────────────────────────────────────────────────────────────┤
│ *Person profiles are NOT stored separately; they are virtual*       │
│ *entities derived from Show.cast/crew for UI display*              │
│  - id (from external catalog)                                      │
│  - name, bio, profileUrl                                           │
│  - filmography (derived from shows they appear in)                │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Storage Schema (Supabase Tables)

**Table: shows**
```sql
CREATE TABLE shows (
    id TEXT NOT NULL,
    namespace_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    title TEXT NOT NULL,
    showType TEXT NOT NULL CHECK (showType IN ('movie', 'tv', 'person', 'unknown')),
    externalIds JSONB,
    
    -- Catalog metadata
    overview TEXT,
    tagline TEXT,
    homepage TEXT,
    originalLanguage TEXT,
    spokenLanguages TEXT[],
    languages TEXT[],
    posterUrlString TEXT,
    backdropUrlString TEXT,
    logoUrlString TEXT,
    networkLogos TEXT[],
    voteAverage DOUBLE PRECISION,
    voteCount BIGINT,
    popularity DOUBLE PRECISION,
    lastAirDate TEXT,
    firstAirDate TEXT,
    releaseDate TEXT,
    runtime INTEGER,
    budget BIGINT,
    revenue BIGINT,
    seriesStatus TEXT,
    numberOfEpisodes INTEGER,
    numberOfSeasons INTEGER,
    episodeRunTime INTEGER[],
    lastEpisodeRunTime INTEGER,
    
    -- User data
    myTags TEXT[],
    myScore DOUBLE PRECISION,
    myStatus TEXT CHECK (myStatus IN ('active', 'next', 'later', 'done', 'quit', 'wait')),
    myInterest TEXT CHECK (myInterest IN ('excited', 'interested')),
    aiScoop TEXT,
    
    -- Timestamps
    myTagsUpdateDate TEXT,
    myScoreUpdateDate TEXT,
    myStatusUpdateDate TEXT,
    myInterestUpdateDate TEXT,
    aiScoopUpdateDate TEXT,
    detailsUpdateDate TEXT,
    creationDate TEXT NOT NULL,
    
    -- Management
    isTest BOOLEAN DEFAULT FALSE,
    
    -- Provider data
    providerData JSONB,
    
    PRIMARY KEY (namespace_id, user_id, id)
);

-- Indexes for common query patterns
CREATE INDEX idx_shows_namespace_user ON shows(namespace_id, user_id);
CREATE INDEX idx_shows_namespace_user_status ON shows(namespace_id, user_id, myStatus);
CREATE INDEX idx_shows_namespace_user_tags ON shows(namespace_id, user_id) WHERE myTags IS NOT NULL;
CREATE INDEX idx_shows_namespace_user_type ON shows(namespace_id, user_id, showType);
```

**Table: cloud_settings**
```sql
CREATE TABLE cloud_settings (
    id TEXT NOT NULL DEFAULT 'globalSettings',
    namespace_id TEXT NOT NULL,
    userName TEXT NOT NULL,
    version BIGINT NOT NULL,  -- epoch seconds
    catalogApiKey TEXT,
    aiApiKey TEXT,
    aiModel TEXT NOT NULL,
    PRIMARY KEY (namespace_id, id)
);
```

**Table: app_metadata**
```sql
CREATE TABLE app_metadata (
    id TEXT NOT NULL DEFAULT 'metadata',
    namespace_id TEXT NOT NULL,
    dataModelVersion INTEGER NOT NULL DEFAULT 3,
    PRIMARY KEY (namespace_id, id)
);
```

### 2.3 Data Merge Rules

When merging external catalog data into an existing stored show:

1. **Non-my fields**: Use `selectFirstNonEmpty(newValue, oldValue)`
   - Never overwrite non-empty stored string/array with empty string/empty array
   - Never overwrite non-nil stored value with nil

2. **My fields** (`myTags`, `myScore`, `myStatus`, `myInterest`): Resolve by timestamp
   - If both sides have update dates, keep the newer
   - If only one side has an update date, keep that side
   - Preserves user edits across sync merges and catalog refreshes

3. **Special fields**:
   - `detailsUpdateDate`: Set to "now" after merge
   - `creationDate`: Set only on first creation; catalog refreshes do NOT change it

### 2.4 Collection Membership Rules

A show is "in collection" when it has an assigned status (non-nil `myStatus`).

**Saving Triggers:**
- Setting any status
- Choosing an interest chip (Interested/Excited)
- Rating an unsaved show
- Adding at least one tag to an unsaved show

**Default Values When Saving:**
- Default status: `Later`
- Default interest: `Interest`
- Exception: First save via rating defaults status to `Done`

**Removing from Collection:**
- Trigger: User clears status (reselects active status and confirms removal)
- Effects: Remove show from storage, clear all My Data (status, interest, tags, rating, AI Scoop)
- Show warning confirmation (with option to stop asking after repeated removals)

**Re-adding Same Show:**
- Preserve latest status, interest, tags, rating, and AI Scoop
- Refresh public metadata as available
- Merge conflicts resolve by most recent update timestamp per field

---

## 3. Application Structure

### 3.1 Directory Structure

```
/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── (auth)/             # Auth-related routes (future)
│   │   ├── (main)/             # Main app routes
│   │   │   ├── layout.tsx      # Main layout with filters panel
│   │   │   ├── page.tsx        # Collection Home
│   │   │   ├── find/           # Find/Discover hub
│   │   │   │   ├── page.tsx    # Find selector (Search/Ask/Alchemy)
│   │   │   │   ├── search/     # Search mode
│   │   │   │   │   └── page.tsx
│   │   │   │   ├── ask/        # Ask mode
│   │   │   │   │   └── page.tsx
│   │   │   │   └── alchemy/    # Alchemy mode
│   │   │   │       └── page.tsx
│   │   │   ├── show/           # Show Detail
│   │   │   │   └── [id]/
│   │   │   │       └── page.tsx
│   │   │   ├── person/         # Person Detail
│   │   │   │   └── [id]/
│   │   │   │       └── page.tsx
│   │   │   └── settings/       # Settings
│   │   │       └── page.tsx
│   │   ├── api/                # API routes
│   │   │   ├── shows/          # Show CRUD
│   │   │   │   └── route.ts
│   │   │   ├── ai/             # AI services
│   │   │   │   ├── concepts/   # Concept generation
│   │   │   │   │   └── route.ts
│   │   │   │   ├── scoop/      # AI Scoop
│   │   │   │   │   └── route.ts
│   │   │   │   ├── ask/        # Ask chat
│   │   │   │   │   └── route.ts
│   │   │   │   └── recommend/  # Concept-based recommendations
│   │   │   │       └── route.ts
│   │   │   ├── catalog/        # Catalog integration
│   │   │   │   └── route.ts
│   │   │   ├── settings/      # Settings CRUD
│   │   │   │   └── route.ts
│   │   │   └── namespace/     # Namespace operations
│   │   │       └── route.ts
│   │   ├── layout.tsx          # Root layout
│   │   └── page.tsx            # Redirect to main or entry
│   │
│   ├── components/
│   │   ├── ui/                 # Reusable UI components
│   │   │   ├── Button.tsx
│   │   │   ├── Chip.tsx
│   │   │   ├── Modal.tsx
│   │   │   ├── Slider.tsx
│   │   │   └── ...
│   │   ├── layout/             # Layout components
│   │   │   ├── FiltersPanel.tsx
│   │   │   ├── TopBar.tsx
│   │   │   └── Sidebar.tsx
│   │   ├── shows/              # Show-related components
│   │   │   ├── ShowTile.tsx
│   │   │   ├── ShowCard.tsx
│   │   │   ├── StatusChips.tsx
│   │   │   ├── RatingSlider.tsx
│   │   │   └── TagPicker.tsx
│   │   ├── detail/             # Detail page components
│   │   │   ├── HeaderCarousel.tsx
│   │   │   ├── DetailSection.tsx
│   │   │   ├── ConceptsSection.tsx
│   │   │   └── ScoopSection.tsx
│   │   ├── ai/                 # AI feature components
│   │   │   ├── AskChat.tsx
│   │   │   ├── ConceptSelector.tsx
│   │   │   ├── AlchemyFlow.tsx
│   │   │   └── MentionedShowsStrip.tsx
│   │   └── common/             # Common utilities
│   │       ├── Loading.tsx
│   │       ├── EmptyState.tsx
│   │       └── ErrorBoundary.tsx
│   │
│   ├── lib/
│   │   ├── constants/          # App constants
│   │   │   ├── status.ts       # Status definitions
│   │   │   ├── interest.ts     # Interest definitions
│   │   │   └── filters.ts      # Filter definitions
│   │   ├── utils/              # Utility functions
│   │   │   ├── date.ts
│   │   │   ├── format.ts
│   │   │   └── storage.ts
│   │   ├── types/              # TypeScript type definitions
│   │   │   ├── show.ts
│   │   │   ├── user.ts
│   │   │   └── api.ts
│   │   ├── db/                 # Database layer
│   │   │   ├── supabase.ts     # Supabase client
│   │   │   ├── queries.ts      # Query functions
│   │   │   └── mutations.ts    # Mutation functions
│   │   ├── ai/                 # AI integration layer
│   │   │   ├── prompts/        # Prompt definitions
│   │   │   │   ├── scoop.ts
│   │   │   │   ├── ask.ts
│   │   │   │   ├── concepts.ts
│   │   │   │   └── recommend.ts
│   │   │   ├── parser.ts       # Response parsing
│   │   │   └── provider.ts     # AI provider integration
│   │   └── catalog/            # Catalog integration
│   │       ├── provider.ts     # Catalog provider
│   │       └── mapper.ts       # Data mapping
│   │
│   ├── hooks/                  # React hooks
│   │   ├── useShows.ts
│   │   ├── useFilters.ts
│   │   ├── useAI.ts
│   │   └── useSettings.ts
│   │
│   ├── styles/                 # CSS/design system
│   │   ├── globals.css
│   │   ├── variables.css
│   │   └── components.css
│   │
│   └── config/                 # Configuration
│       ├── app.ts              # App configuration
│       └── routes.ts           # Route definitions
│
├── public/                      # Static assets
│   └── images/
│
├── .env.example                 # Environment variable template
├── .gitignore
├── next.config.js
├── package.json
├── tsconfig.json
└── README.md
```

### 3.2 Component Hierarchy

```
App
├── AuthProvider (dev injection)
├── NamespaceProvider
├── SettingsProvider
├── SupabaseProvider
│
└── MainLayout
    ├── FiltersPanel
    │   ├── StatusFilters
    │   ├── TagFilters
    │   ├── GenreFilters
    │   ├── DecadeFilters
    │   └── ScoreFilters
    │
    └── MainContent
        ├── CollectionHome
        │   ├── StatusGroups
        │   │   ├── ActiveSection
        │   │   ├── ExcitedSection
        │   │   ├── InterestedSection
        │   │   └── OtherStatusSection
        │   └── ShowGrid
        │       └── ShowTile[]
        │
        ├── FindHub
        │   ├── ModeSwitcher
        │   ├── SearchView
        │   │   └── SearchResults
        │   │       └── ShowGrid
        │   ├── AskView
        │   │   ├── AskChat
        │   │   │   ├── MessageList
        │   │   │   └── MentionedShowsStrip
        │   │   └── StarterPrompts
        │   └── AlchemyView
        │       ├── ShowSelector
        │       ├── ConceptSelector
        │       └── RecommendationResults
        │
        ├── ShowDetail
        │   ├── HeaderCarousel
        │   ├── Toolbar
        │   │   ├── StatusChips
        │   │   ├── RatingSlider
        │   │   └── ActionButtons
        │   ├── CoreFactsRow
        │   ├── MyTagsSection
        │   ├── OverviewSection
        │   ├── ScoopSection
        │   ├── AskCTA
        │   ├── TraditionalRecommendations
        │   ├── ExploreSimilar
        │   │   ├── ConceptButtons
        │   │   └── SimilarResults
        │   ├── StreamingSection
        │   ├── CastCrewSection
        │   │   └── PersonTile[]
        │   ├── SeasonsSection (TV only)
        │   └── BudgetRevenueSection (Movie only)
        │
        ├── PersonDetail
        │   ├── ImageGallery
        │   ├── BioSection
        │   ├── AnalyticsCharts
        │   └── Filmography
        │       └── ShowTile[]
        │
        └── SettingsPage
            ├── UserSettings
            ├── AISettings
            ├── IntegrationSettings
            └── DataExport
```

---

## 4. Feature Implementation Breakdown

### 4.1 Collection Home (7.1)

**Purpose:** Display user's library organized by relationship/status.

**Components:**
- FiltersPanel (sidebar)
- StatusGroups (Active, Excited, Interested, Other)
- ShowGrid with ShowTile
- Media type toggle (All/Movies/TV)

**Behavior:**
- Group shows by status: Active (prominent), Excited (Later+Excited), Interested (Later+Interested), Other (Wait, Quit, Done, unclassified Later)
- Tiles display poster, title, and My Data badges (in-collection indicator, user rating)
- Empty state: "No shows in collection" → prompt to Search/Ask
- Filter yields none: "No results found"

**Data Flow:**
1. Load user shows from Supabase (filtered by namespace_id + user_id)
2. Group by status and apply active filters
3. Sort within groups (default: by update date descending)
4. Render grouped ShowGrid

**API Endpoints:**
- `GET /api/shows` - Get user's shows with filters

---

### 4.2 Search (7.3)

**Purpose:** Find shows in the global catalog.

**Components:**
- SearchInput
- SearchResults (ShowGrid)
- ShowTile with in-collection badge

**Behavior:**
- Text search by title/keywords against external catalog
- Results in poster grid
- In-collection items marked with badge
- Selecting a show opens Detail
- Auto-open on launch if user enabled "Search on Launch"

**Data Flow:**
1. User types query
2. Call catalog API with query
3. Map results to Show objects
4. Check which results are in user's collection
5. Display results with in-collection indicators

**API Endpoints:**
- External catalog search endpoint
- `GET /api/catalog/search?query={query}` - Proxy to catalog

---

### 4.3 Ask (7.4)

**Purpose:** Conversational discovery via chat.

**Components:**
- AskChat (MessageList + Input)
- MentionedShowsStrip
- StarterPrompts (6 random, refreshable)

**Behavior:**
- Chat UI with user/assistant turns
- Friendly, opinionated, spoiler-safe tone
- AI mentions shows inline → appear in horizontal strip
- Tapping mentioned show opens Detail or hands off to Search if mapping fails
- Conversation context retained; older turns summarized after ~10 messages
- Welcome view shows starter prompts

**Modes:**
- **General Ask**: Started from Find
- **Ask About a Show**: Launched from Show Detail button. Seed conversation with show context.

**Data Flow:**
1. User sends message
2. Build context: conversation history (summarized) + user library + show context (if applicable)
3. Call AI provider with Ask prompt
4. Parse response for: commentary + showList (structured format)
5. Map showList to real Show objects
6. Display commentary + MentionedShowsStrip

**API Endpoints:**
- `POST /api/ai/ask` - Process chat message, return commentary + structured show list

**Structured Output Format:**
```
commentary: string (user-facing response)
showList: "Title::externalId::mediaType;;Title2::externalId::mediaType;;..."
```

---

### 4.4 Alchemy (7.5)

**Purpose:** Structured blending discovery.

**Flow:**
1. Select 2+ starting shows (from library or global catalog)
2. Tap "Conceptualize Shows"
3. AI extracts shared concept catalysts (themes, vibes, ingredients)
4. User selects 1-8 concepts
5. Tap "ALCHEMIZE!"
6. AI returns 6 recommended shows grounded to real catalog items with reasons
7. User can chain another round using results as new inputs with "More Alchemy!"

**Components:**
- ShowSelector (multi-select, 2+ required)
- ConceptualizeButton
- ConceptSelector (select up to 8)
- AlchemizeButton
- RecommendationResults (6 items with reasons)
- ChainButton ("More Alchemy!")

**UX Rules:**
- Step clarity with cards/sections
- Backtracking allowed (changing shows clears concepts/results)
- UI hints: "pick the ingredients you want more of"
- Empty state: nudge to select at least one concept

**Data Flow:**
1. User selects shows
2. Call AI with selected shows → get concepts
3. User selects concepts
4. Call AI with selected shows + concepts → get recommendations
5. Map recommendations to real catalog items
6. Display with reasons tied to selected concepts

**API Endpoints:**
- `POST /api/ai/concepts` - Generate concepts from shows
- `POST /api/ai/recommend` - Get recommendations from shows + concepts

---

### 4.5 Show Detail Page (7.6)

**Purpose:** Single source of truth for a show with My Data + discovery.

**Sections (in order):**
1. Header media carousel (backdrops/posters/logos, trailers when available)
2. Core facts row (year/length) + community score
3. My Tags (tag chips)
4. Overview + Scoop toggle/stream
5. "Ask about this show" CTA
6. Genres + languages
7. Traditional recommendations strand
8. Explore Similar (concepts → recs)
9. Streaming availability ("Stream It")
10. Cast & Crew (horizontal) → Person Detail
11. Seasons (TV only)
12. Budget vs Revenue (movies where available)

**Toolbar Controls (always visible):**
- Status chips: Interested, Excited, Active, Wait, Done, Quit
- Rating slider
- Tags picker

**Behavior:**
- Rating an unsaved show auto-saves as Done
- Adding a tag to unsaved show auto-saves as Later + Interested
- Setting status saves; reselecting status triggers removal confirmation
- Scoop toggle: "Give me the scoop!" / "Show the scoop" / "The Scoop"
- Scoop streams progressively ("Generating..." not blank wait)
- Scoop freshness: regenerate after ~4 hours on demand
- Scoop persists only if show is in collection

**Explore Similar Flow:**
1. Tap "Get Concepts"
2. Select 1+ concepts
3. Tap "Explore Shows"
4. Display 5 AI recommendations with reasons

**API Endpoints:**
- `GET /api/shows/{id}` - Get show (merge with catalog if needed)
- `PUT /api/shows/{id}` - Update show (My Data)
- `DELETE /api/shows/{id}` - Remove from collection
- `POST /api/ai/scoop/{id}` - Generate AI Scoop
- `POST /api/ai/concepts/{id}` - Get concepts for single show
- `POST /api/ai/recommend/{id}` - Explore Similar recommendations

---

### 4.6 Person Detail Page (7.7)

**Purpose:** Explore talent behind shows.

**Components:**
- ImageGallery
- Name + Bio
- AnalyticsCharts (average project ratings, top genres, projects-by-year)
- Filmography (grouped by year)

**Behavior:**
- Selecting a credit opens Show Detail
- Filmography sorted by year descending
- Analytics computed from user's collection data

**Data Flow:**
1. Load person from catalog (via show's cast/crew)
2. Fetch person's filmography from catalog
3. Compute analytics from user's collection
4. Map filmography items to Show objects (check if in collection)

**API Endpoints:**
- `GET /api/catalog/person/{id}` - Get person details
- `GET /api/catalog/person/{id}/credits` - Get person's credits

---

### 4.7 Settings & Your Data (7.8)

**App Settings:**
- Font size / readability (XS, S, M, L, XL, XXL)
- Search on launch (boolean)

**User:**
- Username (synced across devices if enabled)

**AI:**
- AI provider API key (benchmark: env vars; optional storage, never committed)
- AI model selection (synced if enabled)

**Integrations:**
- Content catalog provider API key (synced if enabled)

**Your Data:**
- Export My Data: Produces .zip with JSON backup of all saved shows and My Data
  - Dates encoded ISO-8601
  - Includes: shows, cloud_settings (without API keys), app_metadata
- Import / Restore: Desired but not required for initial implementation

**API Endpoints:**
- `GET /api/settings` - Get user settings
- `PUT /api/settings` - Update settings
- `GET /api/export` - Export user data as JSON
- `POST /api/namespace/reset` - Reset namespace data (destructive testing)

---

### 4.8 AI Features Implementation

#### 4.8.1 AI Scoop (The Scoop)

**Purpose:** Personality-driven, spoiler-safe taste review.

**Contract:**
- Structured as mini blog-post of taste
- Includes: personal take, honest stack-up vs reviews, Scoop centerpiece, fit/warnings, verdict
- ~150-350 words total, Scoop paragraph gets most real estate
- Spoiler-safe by default
-Generates on demand from Show Detail
- Cached for ~4 hours
- Persists only if show is in collection

**Prompt Requirements:**
- Warm, playful, opinionated tone
- Honest about mixed reception
- Vibe-first, structure/craft focused
- Never generic

**API Endpoint:**
- `POST /api/ai/scoop` - Input: show details + user context, Output: Scoop text

#### 4.8.2 Ask Chat

**Contract:**
- Responds like friend in dialogue
- Willing to pick favorites
- Adapts depth to user's question
- Uses simple formatting and bulleted lists for multi-recs
- Direct answer within first 3-5 lines
- Confident picks

**Structured Output:**
```typescript
{
  commentary: string;
  showList: string; // "Title::externalId::mediaType;;..."
}
```

**Summarization:**
- After ~10 messages, summarize older turns to 1-2 sentences
- Summaries preserve persona/tone (no sterile system voice)

#### 4.8.3 Concepts Generation

**Contract:**
- Returns bullet list only
- Each concept: 1-3 words, evocative, spoiler-free
- Avoids generic concepts ("good characters", "great story")
- For multi-show: concepts represent shared commonality across all inputs
- Diversity: cover different axes (structure, vibe, emotion, craft)
- Order by strength (best "aha" concepts first)

**Quality Heuristic:**
- Shared and core (for multi-show)
- Evocative and specific (ingredient-like)
- Useful to steer recommendations
- Varied across axes

**Counts:**
- Default: 8 concepts generated
- Selection cap: 8 concepts (UI)
- Explore Similar: 5 recommendations
- Alchemy: 6 recommendations

**API Endpoint:**
- `POST /api/ai/concepts` - Input: show IDs, Output: concept list

#### 4.8.4 Concept-Based Recommendations

**Contract:**
- Returns list of recommended shows with concise reasons
- Reasons explicitly reflect selected concepts
- Recommendations must resolve to real catalog items
- Bias toward recent but allow classics/hidden gems

**Mapping Strategy:**
1. AI outputs: title + external ID + media type
2. Look up by external ID in catalog
3. Accept first result with case-insensitive title match
4. If found: becomes selectable Show with AI reason as transient text
5. If not found: show non-interactive or hand off to Search

---

## 5. Cross-Cutting Concerns

### 5.1 Identity & Isolation (infra_rider_prd.md)

**Namespace Model:**
- Each build operates in a single stable `namespace_id`
- Namespace is a build isolation primitive, not user concept
- Two different namespaces MUST NOT read/write each other's data
- Destructive testing scoped to namespace

**User Identity:**
- All user-owned records associated with `user_id` (opaque stable string/UUID)
- System behaves as if multiple users could exist (even if UI doesn't expose it)
- Within namespace, partition is: `(namespace_id, user_id)`

**Development Identity Injection:**
- Accept `X-User-Id` header in dev/test
- Or local dev-only "login as user" selector
- Or fixed "default user" for namespace
- Must be documented and gated for production

**Migration to OAuth:**
- Replacing dev mechanism with OAuth must require only config + auth wiring
- NOT a schema redesign

### 5.2 Data Persistence Rules

**Source of Truth:** Server-side (Supabase)
- Clients may cache for performance
- Clearing client storage must NOT lose user data

**Cache Disposable:**
- Safe to clear local storage
- Safe to reinstall app
- User data preserved in backend

**Destructive Testing:**
- Create test data inside namespace
- Delete/reset test data inside namespace
- MUST NOT require global database teardown

### 5.3 Environment Configuration

**.env.example:**
```
# Supabase
NEXT_PUBLIC_SUPABASE_URL=your-supabase-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-key

# Namespace (for benchmark runs)
NAMESPACE_ID=dev-default

# AI Provider
AI_PROVIDER=openai
AI_API_KEY=your-ai-key
AI_MODEL=gpt-4

# Catalog Provider
CATALOG_PROVIDER=tmdb
CATALOG_API_KEY=your-catalog-key

# Optional: Default user for dev
DEFAULT_USER_ID.dev=dev-user-1
```

**Credential Rules:**
- Secrets NEVER committed
- Browser code uses anon/public key only
- Service role key server-only

### 5.4 Data Sync & Integrity

**Cross-device Sync (when enabled):**
- Library and settings consistent across devices
- Conflicts resolve per field using most recent edit timestamp
- Duplicate items detected and merged transparently

**Data Continuity:**
- Preserve user libraries across updates
- Automatic migration when data model changes
- Users never lose collection, ratings, tags, statuses, interest, AI Scoop
- `dataModelVersion` in app_metadata tracks current schema version

---

## 6. Technical Implementation Details

### 6.1 Supabase Setup

**Initial Schema Migration:**
```bash
# Apply initial schema
npx supabase db push --db-url $DATABASE_URL

# Or use migrations
npx supabase migration new init_schema
# Then apply
npx supabase migration up --db-url $DATABASE_URL
```

**Row-Level Security (RLS):**
```sql
-- Enable RLS on all tables
ALTER TABLE shows ENABLE ROW LEVEL SECURITY;
ALTER TABLE cloud_settings ENABLE ROW LEVEL SECURITY;
ALTER TABLE app_metadata ENABLE ROW LEVEL SECURITY;

-- Policies using namespace + user_id
CREATE POLICY "Users can access their own shows"
ON shows
FOR ALL
USING (
    auth.uid() = user_id AND
    (
        -- In benchmark mode, also check namespace
        EXISTS (
            SELECT 1 FROM app_metadata am
            WHERE am.namespace_id = shows.namespace_id
            AND am.id = 'metadata'
        )
    )
);
```

### 6.2 API Layer Design

**General Pattern:**
- All API routes in `/app/api/`
- Use Next.js Route Handlers
- Request validation with Zod
- Error handling with consistent format

**Response Format:**
```typescript
{
  data?: any;
  error?: {
    code: string;
    message: string;
    details?: any;
  };
}
```

**Middleware:**
- Namespace injection from headers/config
- User ID injection from auth (dev header or OAuth)
- Rate limiting (optional for production)

### 6.3 AI Provider Integration

**Provider Interface:**
```typescript
interface AIProvider {
  generate unrestricted(content: string, options?: GenerateOptions): Promise<string>;
  generateStructured<T>(content: string, schema: z.ZodSchema<T>, options?: GenerateOptions): Promise<T>;
}
```

**Prompt Management:**
- Prompts in `/lib/ai/prompts/`
- Template literals with variable interpolation
- Version control for prompt evolution

**Response Parsing:**
- Structured outputs use schema validation
- Retry with stricter formatting on parse failure
- Graceful fallback to unstructured + Search handoff

### 6.4 Catalog Integration

**Provider Interface:**
```typescript
interface CatalogProvider {
  search(query: string, options?: SearchOptions): Promise<Show[]>;
  getDetails(id: string, type: ShowType): Promise<Show>;
  getCredits(id: string, type: ShowType): Promise<{ cast: Person[]; crew: Person[] }>;
  getRecommendations(id: string, type: ShowType): Promise<Show[]>;
  getSimilar(id: string, type: ShowType): Promise<Show[]>;
  getProviders(id: string, type: ShowType): Promise<ProviderData>;
}
```

**Caching:**
- Catalog responses cached for performance
- TTL: ~1 hour for show details, ~24 hours for search
- Cache key: `catalog:{type}:{id}` or `catalog:search:{query}`

### 6.5 State Management (Client)

**Approach:** React Context + useReducer for complex state

**Main State:**
- Collection (shows)
- Filters (current active filters)
- AI sessions (Ask chat history, Alchemy state)
- UI preferences

**Optimistic Updates:**
- Status/tag/rating changes applied optimistically
- Revert on error with toast notification

**Data Fetching:**
- SWR or React Query for server state
- useEffect for initial loads
- useTransition for pending states

---

## 7. Data Flow Scenarios

### 7.1 Build Collection Journey
```
User → Find → Search → [type query] → [select show] → Show Detail
→ [set Interested] → Auto-save (status=Later, interest=Interested)
→ Collection Home (show appears in Interested group)
```

**Data Changes:**
- Show created with: id, title, showType, myStatus=Later, myInterest=Interested
- myStatusUpdateDate = now, myInterestUpdateDate = now, creationDate = now

### 7.2 Rate-to-Save Journey
```
User → Search → [select show] → Show Detail → [rate 8/10]
→ Auto-save (status=Done) → Collection Home (show in Done group)
```

**Data Changes:**
- Show created with: myStatus=Done, myScore=8
- myStatusUpdateDate = now, myScoreUpdateDate = now

### 7.3 Tag-to-Save Journey
```
User → Search → [select show] → Show Detail → [add tag "sci-fi"]
→ Auto-save (status=Later, interest=Interested) → Collection Home
```

### 7.4 Ask Discovery Journey
```
User → Find → Ask → [type "sci-fi with strong female leads"]
→ AI returns commentary + showList
→ Map showList to Show objects
→ Display mentioned shows strip
→ User selects a show → Show Detail
→ [User saves] → Collection Home
```

### 7.5 Alchemy Journey
```
User → Find → Alchemy
→ [select 3 shows from collection]
→ [Conceptualize] → AI returns 8 shared concepts
→ [select 4 concepts]
→ [ALCHEMIZE!] → AI returns 6 recommendations
→ [select "More Alchemy!"] → Use results as new inputs
→ Chain continues...
```

### 7.6 Explore Similar Journey
```
User → Collection Home → [select show] → Show Detail
→ [Get Concepts] → AI returns 8 concepts
→ [select 3 concepts] → [Explore Shows]
→ AI returns 5 recommendations with concept-matched reasons
→ [Select recommendation] → Show Detail (new show)
```

---

## 8. Error Handling & Edge Cases

### 8.1 Error Categories

**Network Errors:**
- Show toast: "Connection lost. Please check your internet."
- Retry automatically for transient errors
- Provide offline mode indication

**Catalog Errors:**
- Show not found: "Show not found in catalog"
- Rate limit: "Too many requests. Please wait and try again."
- Invalid API key: "Catalog service unavailable"

**AI Errors:**
- Provider error: "AI service unavailable"
- Rate limit: "Too many AI requests. Please wait."
- Invalid response: "AI response incomplete. Please try again."

**Database Errors:**
- Constraint violation: "Operation failed. Please try again."
- Unique violation: "Show already exists"
- Permission denied: "Access denied"

### 8.2 Edge Cases

**Show Already Saved:**
- Opening a show already in collection → display with My Data overlay
- No duplicate creation; merge public metadata

**Conflict Resolution:**
- Field-level: newer timestamp wins
- User edits always preserved over catalog refresh

**Empty States:**
- No collection: "Your collection is empty. Search for shows to add."
- No search results: "No shows found. Try different keywords."
- No concepts: "No concepts found. Try different shows."
- No recommendations: "No recommendations found. Try different concepts."

**Rate Limiting:**
- Implement token bucket for AI and catalog calls
- Queue requests when rate limited
- Show estimated wait time

**Invalid Data:**
- Validate all catalog responses
- Sanitize user inputs
- Graceful degradation for malformed data

---

## 9. Testing Strategy

### 9.1 Unit Tests
- Data model validation
- Merge rule logic
- Timestamp comparison
- Status transitions
- Filter application

### 9.2 Integration Tests
- API endpoint responses
- Database query correctness
- AI response parsing
- Catalog data mapping

### 9.3 End-to-End Tests
- User journeys (Build collection, Rate-to-save, etc.)
- Cross-device sync
- Data export/import
- Namespace isolation

### 9.4 Test Data Setup
```bash
# Create test namespace
npm run test:setup -- --namespace test-run-001

# Seed test data
npm run test:seed -- --namespace test-run-001 --user test-user-1

# Run tests
npm test

# Reset test namespace
npm run test:reset -- --namespace test-run-001
```

### 9.5 Test Coverage Targets
- Unit tests: 80%+ coverage
- Integration tests: Key paths covered
- E2E tests: All major user journeys

---

## 10. Performance Considerations

### 10.1 Client-Side
- Virtualized lists for large collections
- Image lazy loading with placeholder
- Debounced search input (300ms)
- Memoized component renders
- Code splitting for large routes

### 10.2 Server-Side
- Database indexes for common queries
- Query batching where possible
- Caching layer for catalog and AI responses
- Connection pooling for Supabase
- Request timeouts (5-10 seconds)

### 10.3 Data Loading
- Pagination for large datasets (20-50 items per page)
- Infinite scroll for collections
- Prefetch next pages
- Skeleton loading states

### 10.4 Bundle Size
- Monitor with `@next/bundle-analyzer`
- Target: <500KB main bundle
- Code splitting for AI and catalog heavy features
- Lazy load non-critical components

---

## 11. Security Considerations

### 11.1 Data Protection
- API keys never exposed to client (except anon Supabase key)
- Sensitive data encrypted at rest (Supabase default)
- HTTPS everywhere
- No sensitive data in URLs

### 11.2 Authentication
- Dev mode: X-User-Id header (documented, gated)
- Production: OAuth-ready (Google, etc.)
- Session management with secure cookies
- CSRF protection

### 11.3 Authorization
- Row-level security on Supabase
- Namespace isolation enforced at all layers
- User scope enforced on all operations
- Read-only for non-owned data

### 11.4 Input Validation
- All API inputs validated with Zod
- Sanitize user-generated content
- Prevent injection attacks
- Rate limiting on public endpoints

---

## 12. Deployment & CI/CD

### 12.1 Local Development
```bash
# Install dependencies
npm install

# Set up environment
cp .env.example .env
# Edit .env with local values

# Start Supabase locally (optional)
npx supabase start

# Run migrations
npx supabase db push

# Start app
npm run dev

# Run tests
npm test

# Reset test data
npm run test:reset
```

### 12.2 CI/CD Pipeline
```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        ports: ["5432:5432"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npm run test:setup
      - run: npm test
      - run: npm run lint
      - run: npm run typecheck
```

### 12.3 Production Deployment
- Vercel (Next.js optimized)
- Supabase hosted (or self-hosted)
- Environment variables via secrets management
- Zero-downtime deployments
- Health checks and monitoring

---

## 13. Development Roadmap

### Phase 1: Foundation (Week 1-2)
- Set up Next.js project
- Configure Supabase
- Implement basic types and utilities
- Create database schema and migrations
- Set up API layer structure
- Implement authentication (dev injection)

### Phase 2: Core Collection (Week 2-3)
- Implement Show model and storage
- Build Collection Home page
- Create ShowTile and ShowCard components
- Implement filters (status, tags, data)
- Add Show Detail page (basic)
- Implement CRUD operations for My Data

### Phase 3: Discovery Foundation (Week 3-4)
- Implement Search functionality
- Build catalog integration
- Create Find hub with mode switching
- Implement basic AI integration
- Add Scoop generation
- Build Ask chat (basic)

### Phase 4: Advanced Discovery (Week 4-5)
- Implement Concepts generation
- Build Explore Similar
- Implement Alchemy flow
- Add Concept-based recommendations
- Implement structured AI outputs
- Add MentionedShowsStrip

### Phase 5: Polish & Features (Week 5-6)
- Add Person Detail page
- Implement Settings page
- Add data export functionality
- Implement streaming availability
- Add traditional recommendations
- Polish UI and UX

### Phase 6: Testing & Hardening (Week 6-7)
- Write unit and integration tests
- Implement E2E tests
- Add error handling and edge cases
- Performance optimization
- Security review

### Phase 7: Production Ready (Week 7-8)
- OAuth integration
- CI/CD pipeline
- Monitoring and analytics
- Documentation
- Final testing

---

## 14. Open Questions & Decisions Log

### Open Questions (from PRD)
1. Should **Next** become a first-class status in UI?
   - Current: Hidden in data model, not surfaced
   - Decision: Defer to post-MVP; can be enabled via feature flag

2. Should users create **named custom lists** beyond tags?
   - Current: Tags only
   - Decision: Defer; tags provide similar functionality

3. Should generating **AI Scoop** on unsaved show implicitly save it?
   - Current: Scoop generated but not persisted unless show saved
   - Decision: No; explicit user action required to save

4. Should clearing My Rating store explicit **Unrated** state vs nil?
   - Current: nil = unrated
   - Decision: Use nil; simpler data model

5. Add **Import/Restore** from export zip?
   - Current: Export only
   - Decision: Desired but not required for initial implementation

6. Support saving/sharing **Alchemy sessions** as reusable blends?
   - Current: Session only
   - Decision: Nice-to-have; defer to post-MVP

7. Add explicit **myStatus filters** in sidebar?
   - Current: Implicit in grouping
   - Decision: Model supports it; can be added easily

### Decisions Made
1. **Framework:** Next.js with App Router (matches benchmark baseline)
2. **Database:** Supabase with RLS (matches benchmark baseline)
3. **AI Response Parsing:** Schema validation with Zod for structured outputs
4. **Error Handling:** Consistent error format across all APIs
5. **State Management:** React Context + SWR (no external library needed)
6. **Styling:** CSS Modules or Tailwind (decision: Tailwind for rapid development)
7. **Namespace Injection:** Via environment variable + dev header
8. **User Injection:** Via X-User-Id header in dev, OAuth in production

---

## 15. Success Criteria Checklist

### From infra_rider_prd.md
- [ ] Provides `.env.example` with all required variables
- [ ] Can run without code edits (configuration only)
- [ ] Can run repeatedly without data collisions (namespace isolation)
- [ ] Associates all user-owned records with `user_id`
- [ ] Supports destructive test runs without global teardown
- [ ] Can later adopt real OAuth without schema redesign

### From product_prd.md
- [ ] Users can build and maintain a meaningful personal collection
- [ ] Organization through statuses, interest levels, and tags is effortless
- [ ] High-quality, taste-aware discovery through AI and Alchemy
- [ ] User data consistent and durable everywhere a show appears
- [ ] User's version takes precedence over catalog data
- [ ] Discovery is actionable (all recommendations map to real shows)
- [ ] Taste-aware AI uses library + My Data + session context
- [ ] Spoiler-safe by default
- [ ] Implicit behaviors feel natural
- [ ] Data export/backup is first-class
- [ ] Identity is explicit with `user_id` scoping
- [ ] Builds are isolated with `namespace_id`
- [ ] Backend is source of truth

---

## 16. Delivery Checklist

### Code Deliverables
- [ ] Next.js application with all features implemented
- [ ] Supabase schema and migrations
- [ ] Environment configuration (.env.example, .gitignore)
- [ ] API documentation (optional but recommended)
- [ ] TypeScript types and interfaces
- [ ] Unit and integration tests
- [ ] E2E test suite

### Documentation
- [ ] README.md with setup and usage instructions
- [ ] DEVELOPMENT.md with local dev setup
- [ ] API.md with endpoint documentation (optional)
- [ ] ARCHITECTURE.md with high-level overview (optional)

### Development Experience
- [ ] One-command start (`npm run dev`)
- [ ] One-command test (`npm test`)
- [ ] One-command reset (`npm run test:reset`)
- [ ] Clear error messages
- [ ] Helpful console output

### Quality
- [ ] Typecheck passes (`npm run typecheck`)
- [ ] Lint passes (`npm run lint`)
- [ ] All tests pass
- [ ] No console warnings/errors
- [ ] Responsive design
- [ ] Accessibility (WCAG 2.1 AA minimum)

---

## 17. Files to Create

### Root
- `.env.example`
- `.gitignore`
- `package.json`
- `tsconfig.json`
- `next.config.js`
- `README.md`

### Source
- `src/app/layout.tsx`
- `src/app/page.tsx`
- `src/app/(main)/layout.tsx`
- `src/app/(main)/page.tsx` (Collection Home)
- `src/app/(main)/find/page.tsx`
- `src/app/(main)/find/search/page.tsx`
- `src/app/(main)/find/ask/page.tsx`
- `src/app/(main)/find/alchemy/page.tsx`
- `src/app/(main)/show/[id]/page.tsx`
- `src/app/(main)/person/[id]/page.tsx`
- `src/app/(main)/settings/page.tsx`
- `src/app/api/shows/route.ts`
- `src/app/api/shows/[id]/route.ts`
- `src/app/api/ai/ask/route.ts`
- `src/app/api/ai/scoop/route.ts`
- `src/app/api/ai/concepts/route.ts`
- `src/app/api/ai/recommend/route.ts`
- `src/app/api/catalog/search/route.ts`
- `src/app/api/catalog/details/route.ts`
- `src/app/api/settings/route.ts`
- `src/app/api/namespace/route.ts`
- `src/app/api/export/route.ts`

### Components
- `src/components/ui/*.tsx` (Button, Chip, Modal, Slider, etc.)
- `src/components/layout/*.tsx` (FiltersPanel, TopBar, Sidebar)
- `src/components/shows/*.tsx` (ShowTile, ShowCard, StatusChips, RatingSlider, TagPicker)
- `src/components/detail/*.tsx` (HeaderCarousel, DetailSection, ConceptsSection, ScoopSection)
- `src/components/ai/*.tsx` (AskChat, ConceptSelector, AlchemyFlow, MentionedShowsStrip)
- `src/components/common/*.tsx` (Loading, EmptyState, ErrorBoundary)

### Library
- `src/lib/constants/*.ts` (status, interest, filters)
- `src/lib/utils/*.ts` (date, format, storage)
- `src/lib/types/*.ts` (show, user, api)
- `src/lib/db/*.ts` (supabase client, queries, mutations)
- `src/lib/ai/*.ts` (prompts, parser, provider)
- `src/lib/catalog/*.ts` (provider, mapper)

### Hooks
- `src/hooks/*.ts` (useShows, useFilters, useAI, useSettings)

### Styles
- `src/styles/*.css` (globals, variables, components)

### Config
- `src/config/*.ts` (app, routes)

---

## 18. Summary

This plan provides a comprehensive blueprint for implementing the Personal TV + Movie Companion App as specified in the PRD and supporting documents. The implementation follows the benchmark baseline (Next.js + Supabase) with proper namespace/user isolation, development identity injection, and all product features including Collection Home, Search, Ask, Alchemy, Show Detail, Person Detail, Settings, and AI-powered discovery features.

Key design decisions:
- Backend as source of truth with client-side caching
- Namespace.user_id partition for all persisted data
- Structured AI outputs with schema validation
- Auto-save behavior with explicit user control for destructive actions
- Spoiler-safe by default across all AI surfaces
- One consistent AI persona across Scoop, Ask, Alchemy, and Explore Similar

The plan addresses all requirements from both product_prd.md and infra_rider_prd.md, including data model, merge rules, collection membership, status/interest systems, concept generation, AI contracts, and execution constraints.
