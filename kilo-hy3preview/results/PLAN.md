# Implementation Plan: Personal TV/Movie Companion App

## Overview

This plan outlines the implementation of a personal TV/movie companion application for collecting, organizing, rating, and discovering entertainment. The app enables users to build their version of each show (status, interest, tags, rating, notes/AI scoop) and uses that taste profile to power multiple discovery paths.

**Tech Stack (per Infra Rider):**
- Next.js (latest stable) - UI + server runtime
- Supabase - persistence layer
- Namespace isolation for build/test runs
- `user_id` scoped records

---

## 1. Data Model & Schema Design

### 1.1 Core Entities (from storage-schema)

**Show Entity:**
```
- id: string (primary key)
- title: string
- showType: "movie" | "tv" | "person" | "unknown"
- externalIds: Record<string, string> (optional)
- overview, tagline, homepage
- genres: string[]
- spokenLanguages, languages: string[]
- posterUrlString, backdropUrlString, logoUrlString
- voteAverage, voteCount, popularity
- releaseDate / firstAirDate / lastAirDate (ISO-8601)
- Movie: runtime, budget, revenue
- TV: seriesStatus, numberOfEpisodes, numberOfSeasons, episodeRunTime
- User Data:
  - myTags: string[], myTagsUpdateDate
  - myScore, myScoreUpdateDate
  - myStatus: "active" | "next" | "later" | "done" | "quit" | "wait"
  - myInterest: "excited" | "interested"
  - aiScoop, aiScoopUpdateDate
- Metadata: detailsUpdateDate, creationDate, isTest
- providerData: ProviderData (by country/region)
```

**CloudSettings Entity:**
```
- id: string (default "globalSettings")
- userName: string
- version: number (epoch seconds)
- catalogApiKey, aiApiKey (optional, synced)
- aiModel: string
```

**AppMetadata Entity:**
```
- dataModelVersion: number (default 3)
```

### 1.2 Supabase Schema (SQL Migrations)

```sql
-- Namespaces table for build isolation
CREATE TABLE namespaces (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  namespace_id TEXT UNIQUE NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Users table (opaque user_id, not provider-specific)
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id TEXT NOT NULL,
  namespace_id TEXT NOT NULL REFERENCES namespaces(namespace_id),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(user_id, namespace_id)
);

-- Shows table with user overlay
CREATE TABLE shows (
  id TEXT NOT NULL,
  user_id TEXT NOT NULL,
  namespace_id TEXT NOT NULL,
  title TEXT NOT NULL,
  show_type TEXT NOT NULL CHECK (show_type IN ('movie', 'tv', 'person', 'unknown')),
  external_ids JSONB,
  overview TEXT,
  genres TEXT[],
  tagline TEXT,
  homepage TEXT,
  original_language TEXT,
  spoken_languages TEXT[],
  languages TEXT[],
  poster_url TEXT,
  backdrop_url TEXT,
  logo_url TEXT,
  vote_average NUMERIC,
  vote_count INTEGER,
  popularity NUMERIC,
  release_date DATE,
  first_air_date DATE,
  last_air_date DATE,
  runtime INTEGER,
  budget BIGINT,
  revenue BIGINT,
  series_status TEXT,
  number_of_episodes INTEGER,
  number_of_seasons INTEGER,
  episode_run_time INTEGER[],
  my_tags TEXT[],
  my_tags_updated_at TIMESTAMP WITH TIME ZONE,
  my_score NUMERIC,
  my_score_updated_at TIMESTAMP WITH TIME ZONE,
  my_status TEXT CHECK (my_status IN ('active', 'next', 'later', 'done', 'quit', 'wait')),
  my_status_updated_at TIMESTAMP WITH TIME ZONE,
  my_interest TEXT CHECK (my_interest IN ('excited', 'interested')),
  my_interest_updated_at TIMESTAMP WITH TIME ZONE,
  ai_scoop TEXT,
  ai_scoop_updated_at TIMESTAMP WITH TIME ZONE,
  details_updated_at TIMESTAMP WITH TIME ZONE,
  creation_date TIMESTAMP WITH TIME ZONE,
  is_test BOOLEAN DEFAULT FALSE,
  provider_data JSONB,
  PRIMARY KEY (id, user_id, namespace_id),
  FOREIGN KEY (user_id, namespace_id) REFERENCES users(user_id, namespace_id)
);

-- Cloud settings (synced across devices)
CREATE TABLE cloud_settings (
  id TEXT DEFAULT 'globalSettings',
  user_id TEXT NOT NULL,
  namespace_id TEXT NOT NULL,
  user_name TEXT,
  version NUMERIC,
  catalog_api_key TEXT,
  ai_api_key TEXT,
  ai_model TEXT,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  PRIMARY KEY (id, user_id, namespace_id),
  FOREIGN KEY (user_id, namespace_id) REFERENCES users(user_id, namespace_id)
);

-- App metadata for migrations
CREATE TABLE app_metadata (
  id TEXT DEFAULT 'app',
  namespace_id TEXT NOT NULL,
  data_model_version INTEGER DEFAULT 3,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  PRIMARY KEY (id, namespace_id)
);

-- Indexes for performance
CREATE INDEX idx_shows_user_namespace ON shows(user_id, namespace_id);
CREATE INDEX idx_shows_my_status ON shows(my_status) WHERE my_status IS NOT NULL;
CREATE INDEX idx_shows_creation_date ON shows(creation_date DESC);
```

### 1.3 Merge Rules (Critical)

When external catalog data merges into existing stored show:
- **Non-my fields:** `selectFirstNonEmpty(newValue, oldValue)` - never overwrite non-empty with empty
- **My fields:** resolve by `my*UpdateDate` timestamp - newer wins
- `detailsUpdateDate` set to "now" after merge
- `creationDate` set only on first creation

---

## 2. Infrastructure Setup

### 2.1 Environment Configuration

**.env.example:**
```env
# Supabase
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# Namespace (build isolation)
NAMESPACE_ID=default

# Default User (benchmark mode)
DEFAULT_USER_ID=default_user

# Catalog API (e.g., TMDB)
CATALOG_API_KEY=your_tmdb_key
CATALOG_API_BASE_URL=https://api.themoviedb.org/3

# AI Provider (e.g., OpenAI)
AI_API_KEY=your_openai_key
AI_MODEL=gpt-4

# App Settings
NEXT_PUBLIC_SEARCH_ON_LAUNCH=false
```

### 2.2 Namespace Isolation Middleware

Create middleware that:
1. Reads `NAMESPACE_ID` from env
2. Injects `namespace_id` into all DB queries
3. Ensures all writes include `(namespace_id, user_id)` partition

### 2.3 Dev Identity Injection

For benchmark mode, implement:
- `X-User-Id` header acceptance in server routes
- Default user creation for namespace on first access
- No OAuth required (gated for production)

---

## 3. Feature Implementation Phases

### Phase 1: Foundation (Core Infrastructure + Data Layer)

1. **Project setup**
   - Initialize Next.js app
   - Configure Supabase client
   - Set up environment variables
   - Create `.env.example` and `.gitignore`

2. **Database migrations**
   - Run schema creation SQL
   - Set up migration framework (e.g., `supabase/migrations/`)

3. **Data access layer**
   - Create Show CRUD operations
   - Implement merge logic (catalog refresh)
   - Build user/scoping helpers

4. **Catalog API integration**
   - TMDB API client
   - Show search by title
   - Show details fetch
   - Map external payload → `Show` schema
   - Handle images, videos, credits (transient)

### Phase 2: Collection Home & Show Detail

1. **Collection Home page**
   - Display shows grouped by status:
     - Active (prominent/larger tiles)
     - Excited (Later + Excited)
     - Interested (Later + Interested)
     - Other (Wait, Quit, Done, collapsed)
   - Media-type toggle: All / Movies / TV
   - Tile display: poster, title, My Data badges
   - Empty states

2. **Show Detail page**
   - Header media carousel (backdrops/posters/logos/videos)
   - Core facts row (year, runtime/seasons, genres)
   - Community score + My Rating slider
   - Status/Interest chips in toolbar
   - My Tags display + picker
   - Overview section
   - Streaming availability (ProviderData)
   - Cast & Crew horizontal strands
   - TV: Seasons section
   - Movies: Budget/Revenue

3. **Auto-save triggers**
   - Setting status → save with defaults
   - Rating unsaved show → auto-save as `Done`
   - Adding tag to unsaved → auto-save as `Later + Interested`

### Phase 3: Filters & Navigation

1. **Sidebar/Filter panel**
   - Quick/default: All Shows
   - Tag filters: one per tag + "No tags"
   - Data filters: genre, decade, community score ranges
   - Media-type toggle applies on top of any filter

2. **Navigation structure**
   - Home (filtered library)
   - Find/Discover hub
   - Settings
   - Person Detail (from cast/crew links)

### Phase 4: Search

1. **Search functionality**
   - Text search by title/keywords
   - Results in poster grid
   - In-collection items marked
   - Auto-open if "Search on Launch" enabled

2. **Search → Detail flow**
   - Select show opens Detail
   - Back to search preserves state

### Phase 5: AI Features

#### 5.1 AI Scoop ("The Scoop")

1. **Scoop generation**
   - Button: "Give me the scoop!" / "Show the scoop"
   - Progressive streaming display
   - Cache for 4 hours (check `aiScoopUpdateDate`)
   - Persist only if show in collection
   - Structure: personal take, honest stack-up, Scoop centerpiece, fit/warnings, verdict

2. **Voice implementation**
   - Warm, playful, opinionated tone
   - Spoiler-safe by default
   - ~150-350 words total

#### 5.2 Ask (AI Chat Discovery)

1. **Chat UI**
   - User/assistant turns
   - Mentioned shows strip (horizontal, selectable)
   - Welcome view with 6 starter prompts (refreshable)
   - Context retention + summarization after ~10 messages

2. **Structured output**
   - `commentary`: user-facing response
   - `showList`: `Title::externalId::mediaType;;...` format

3. **Ask About a Show**
   - Launch from Detail page
   - Seed conversation with show context

4. **Voice:** friendly, opinionated, spoiler-safe, confident picks

#### 5.3 Concept System

1. **Get Concepts**
   - Single-show: extract concepts for that show
   - Multi-show (Alchemy): shared concepts across all inputs
   - Output: bullet list, 1-3 words, evocative, no explanation
   - Default: 8 concepts

2. **Concept quality rules**
   - Specific over generic ("hopeful absurdity" not "good characters")
   - Cover different axes (structure, vibe, emotion, craft)
   - Order by strength

#### 5.4 Explore Similar (Per-Show Concepts)

1. **Flow**
   - Detail → Get Concepts → select concepts → Explore Shows
   - Returns 5 recommendations with reasons
   - Reasons name which concepts match

#### 5.5 Alchemy (Concept Blending)

1. **Flow**
   - Select 2+ starting shows
   - Conceptualize Shows → select concepts (max 8)
   - Alchemize! → 6 recommendations
   - More Alchemy! to chain (use results as new inputs)

2. **UX**
   - Step clarity (cards/sections)
   - Backtracking allowed

### Phase 6: Person Detail

1. **Person profile**
   - Image gallery, bio
   - Analytics: average ratings, top genres, projects-by-year
   - Filmography grouped by year
   - Tap credit → opens Show Detail

### Phase 7: Settings & Data Management

1. **Settings page**
   - Font size / readability
   - Search on launch toggle
   - Username
   - AI provider API key + model selection
   - Content catalog API key

2. **Export/Backup**
   - "Export My Data" → `.zip` with JSON backup
   - Dates encoded ISO-8601
   - All saved shows + My Data

---

## 4. AI Integration Details

### 4.1 Prompt Design (Behavioral Contracts)

**Shared Rules (All Surfaces):**
- Stay within TV/movies domain
- Spoiler-safe by default
- Opinionated and honest
- Specific, vibe/structure/craft-based reasoning

**Surface-Specific Prompts:**

1. **Scoop Prompt:**
   - Mini blog-post structure
   - Personal take + honest stack-up + Scoop centerpiece + fit + verdict
   - ~150-350 words

2. **Ask Prompt:**
   - Conversational, like a friend
   - Structured output: `{ commentary, showList }`
   - 1-3 paragraphs, bulleted lists for multi-recs

3. **Concepts Prompt:**
   - Bullet list only, 1-3 words each
   - Evocative, no plot/explanation
   - Shared across inputs for multi-show

4. **Concept Recs Prompt:**
   - 5-6 recommendations with reasons
   - Reasons name matching concepts
   - Bias recent but allow classics

### 4.2 Context Injection

Include in AI context:
- User's library (saved shows + My Data)
- Current show context (for Scoop/Ask About Show)
- Selected concepts (for Explore Similar/Alchemy)
- Recent conversation turns (summarized if old)

### 4.3 Real-Show Resolution

When AI returns recommendations:
1. Extract title + external ID + media type
2. Lookup catalog by external ID
3. Accept first result with case-insensitive title match
4. If not found: show non-interactive or hand off to Search

---

## 5. Key Business Rules Implementation

### 5.1 Collection Membership
- Show "in collection" when `myStatus` is set (non-nil)

### 5.2 Saving Triggers
- Setting any status
- Choosing Interested/Excited chip
- Rating unsaved show
- Adding tag to unsaved show

### 5.3 Default Values on Save
- Default: `myStatus = "later"`, `myInterest = "interested"`
- Exception: first save via rating → `myStatus = "done"`

### 5.4 Remove from Collection
- Clear status (with confirmation)
- Remove show from storage
- Clear all My Data
- Warning confirmation (optional "don't ask again")

### 5.5 Re-add Same Show
- Preserve latest status, interest, tags, rating, scoop
- Refresh public metadata
- Merge by most recent timestamp per field

### 5.6 Tile Indicators
- In-collection indicator when `myStatus` exists
- User rating indicator when `myScore` exists

---

## 6. Cross-Cutting Concerns

### 6.1 User's Version Precedence
- Everywhere a show appears, display user-overlaid version
- User edits always win over refreshed public data

### 6.2 Data Sync & Integrity
- Library/settings consistent across devices (if sync enabled)
- Conflict resolution: newest timestamp wins per field
- Duplicate detection and merge

### 6.3 Data Continuity Across Versions
- Preserve user libraries across updates
- Automatic migration to new data model
- No user intervention required

### 6.4 Spoiler Safety
- AI outputs spoiler-safe by default
- User must explicitly request spoilers

---

## 7. Testing Strategy

### 7.1 Unit Tests
- Data merge logic
- Auto-save trigger rules
- Concept generation quality
- Show resolution from AI output

### 7.2 Integration Tests
- Search → Detail → Save flow
- Ask conversation with mentions
- Alchemy full flow (select shows → concepts → recs)
- Explore Similar flow

### 7.3 Namespace Isolation Tests
- Verify data doesn't leak between namespaces
- Destructive test reset scoped to namespace
- `npm run test:reset` clears test data

### 7.4 AI Quality Tests (from discovery_quality_bar.md)
- Voice adherence (warm, playful, opinionated)
- Taste alignment (grounded in library/concepts)
- Surprise without betrayal (1-2 unexpected but defensible)
- Specificity of reasoning (concrete "because")
- Real-show integrity (valid external IDs, non-negotiable)

---

## 8. Scripts & Commands

**Required one-command experiences:**
```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "test": "jest",
    "test:reset": "node scripts/reset-test-data.js",
    "migrate": "supabase db push"
  }
}
```

**Test reset script (`scripts/reset-test-data.js`):**
- Connect to Supabase
- Delete all data scoped to `namespace_id`
- Preserve schema (no global teardown)

---

## 9. File Structure

```
src/
├── app/
│   ├── (home)/
│   │   └── page.tsx           # Collection Home
│   ├── detail/
│   │   └── [id]/
│   │       └── page.tsx       # Show Detail
│   ├── find/
│   │   ├── page.tsx           # Find/Discover hub
│   │   ├── search/
│   │   │   └── page.tsx      # Search
│   │   ├── ask/
│   │   │   └── page.tsx      # Ask chat
│   │   └── alchemy/
│   │       └── page.tsx      # Alchemy
│   ├── person/
│   │   └── [id]/
│   │       └── page.tsx      # Person Detail
│   ├── settings/
│   │   └── page.tsx          # Settings
│   └── layout.tsx            # Root layout with nav
├── components/
│   ├── home/
│   │   ├── ShowTile.tsx
│   │   ├── StatusGroup.tsx
│   │   └── MediaTypeToggle.tsx
│   ├── detail/
│   │   ├── HeaderCarousel.tsx
│   │   ├── CoreFacts.tsx
│   │   ├── MyRating.tsx
│   │   ├── StatusChips.tsx
│   │   ├── TagPicker.tsx
│   │   ├── Overview.tsx
│   │   ├── Scoop.tsx
│   │   ├── CastCrew.tsx
│   │   ├── Seasons.tsx
│   │   └── StreamingProviders.tsx
│   ├── search/
│   │   └── SearchGrid.tsx
│   ├── ask/
│   │   ├── ChatUI.tsx
│   │   ├── MentionedShows.tsx
│   │   └── StarterPrompts.tsx
│   ├── alchemy/
│   │   ├── ShowSelector.tsx
│   │   ├── ConceptSelector.tsx
│   │   └── Recommendations.tsx
│   ├── filters/
│   │   └── FilterPanel.tsx
│   └── ui/                   # Shared UI components
├── lib/
│   ├── supabase/
│   │   ├── client.ts
│   │   ├── server.ts
│   │   └── schema.sql
│   ├── catalog/
│   │   ├── tmdb-client.ts
│   │   └── show-mapper.ts
│   ├── ai/
│   │   ├── openai-client.ts
│   │   ├── prompts/
│   │   │   ├── scoop.ts
│   │   │   ├── ask.ts
│   │   │   ├── concepts.ts
│   │   │   └── recommendations.ts
│   │   └── types.ts
│   ├── data/
│   │   ├── shows.ts          # CRUD + merge logic
│   │   ├── users.ts
│   │   └── settings.ts
│   └── utils/
│       ├── merge.ts          # Merge rules
│       └── dates.ts
├── types/
│   ├── show.ts
│   ├── user.ts
│   └── ai.ts
└── middleware.ts              # Namespace + user injection
```

---

## 10. Implementation Order & Dependencies

1. **Phase 1** (Foundation) - no dependencies
2. **Phase 2** (Collection + Detail) - depends on Phase 1
3. **Phase 3** (Filters + Nav) - depends on Phase 2
4. **Phase 4** (Search) - depends on Phase 2
5. **Phase 5** (AI Features) - depends on Phases 2, 3, 4
   - 5.1 Scoop - depends on Detail page
   - 5.2 Ask - depends on Search + Scoop prompts
   - 5.3 Concepts - depends on Ask prompts
   - 5.4 Explore Similar - depends on Concepts
   - 5.5 Alchemy - depends on Concepts + Explore Similar
6. **Phase 6** (Person Detail) - depends on Phase 2
7. **Phase 7** (Settings) - independent, can parallel

---

## 11. Critical Reminders

1. **Do NOT implement OAuth yet** - use dev identity injection
2. **Namespace isolation is mandatory** - all queries scoped to `(namespace_id, user_id)`
3. **User's version takes precedence** - overlay public data with My Data everywhere
4. **AI must be taste-aware** - include library context in prompts
5. **Real-show integrity is non-negotiable** - every AI rec must map to catalog item
6. **Spoiler-safe by default** - AI prompts must enforce this
7. **Backend is source of truth** - client cache is disposable
8. **No offline-first requirement** - normal network failure handling is sufficient

---

## 12. Success Criteria (from Infra Rider)

Build is compliant if:
- ✅ Provides `.env.example` and runs without code edits
- ✅ Runs repeatedly without data collisions (namespace isolation)
- ✅ Associates all user-owned records with `user_id`
- ✅ Supports destructive test runs without global teardown
- ✅ Can adopt real OAuth later without schema redesign
