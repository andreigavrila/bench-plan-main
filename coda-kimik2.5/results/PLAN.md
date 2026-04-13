# Implementation Plan: TV + Movie Companion App

## 1. Overview

This document outlines the implementation strategy for a personal TV and movie companion application. The app enables users to collect, organize, rate, and discover entertainment through an AI-powered, taste-aware interface.

### Core Value Proposition
- **Personal Library**: A living map of what users watch and want to watch
- **Taste-Aware Discovery**: AI-powered recommendations grounded in the user's collection
- **Seamless Organization**: Statuses, interest levels, and free-form tags

---

## 2. Architecture

### 2.1 Tech Stack
| Layer | Technology |
|-------|------------|
| Frontend | Next.js (latest stable) with App Router |
| Backend | Next.js API Routes |
| Database | Supabase (PostgreSQL) |
| AI Integration | OpenAI/Anthropic API (configurable) |
| External Catalog | TMDB or similar (configurable) |
| Styling | CSS Modules or Tailwind CSS |
| State Management | React Context + Server Actions |

### 2.2 Project Structure
```
app/
├── page.tsx                    # Collection Home
├── layout.tsx                  # Root layout with nav
├── globals.css
├── (routes)/
│   ├── show/[id]/page.tsx      # Show Detail
│   ├── person/[id]/page.tsx    # Person Detail
│   ├── find/page.tsx           # Find/Discover hub
│   └── settings/page.tsx       # Settings & Export
├── api/
│   ├── shows/route.ts          # CRUD for shows
│   ├── ask/route.ts            # AI chat endpoint
│   ├── concepts/route.ts       # Concept generation
│   ├── recommendations/route.ts # Recommendations
│   └── import-export/route.ts  # Backup/restore
├── components/
│   ├── collection/             # Home view components
│   ├── show/                   # Detail page components
│   ├── discovery/              # Ask, Alchemy, Search
│   ├── ui/                     # Shared UI primitives
│   └── person/                 # Person detail components
├── hooks/                      # Custom React hooks
├── lib/
│   ├── supabase/               # Supabase client & types
│   ├── ai/                     # AI prompt builders
│   ├── catalog/                # External catalog client
│   └── utils/                  # Helper functions
└── types/
    └── index.ts                # Shared TypeScript types

supabase/
├── migrations/                 # Database migrations
└── seed.sql                    # Seed data (optional)

scripts/
├── reset-test-data.js          # Reset namespace data
└── setup-dev.js                # Dev environment setup
```

### 2.3 Namespace & Identity Model

**Namespace Isolation (`namespace_id`)**
- Inject via `X-Namespace-Id` header in dev/test
- All persisted data partitioned by namespace
- Destructive tests scoped to namespace only

**User Identity (`user_id`)**
- Dev mode: injected via `X-User-Id` header or dev selector
- All user-owned records include `user_id` column
- Multiple users can exist within a namespace
- Composite partition: `(namespace_id, user_id)`

---

## 3. Database Schema

### 3.1 Core Tables

```sql
-- Shows in user collection
CREATE TABLE shows (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  namespace_id TEXT NOT NULL,
  user_id TEXT NOT NULL,
  
  -- Identity
  tmdb_id INTEGER,
  imdb_id TEXT,
  title TEXT NOT NULL,
  show_type TEXT NOT NULL CHECK (show_type IN ('movie', 'tv')),
  
  -- Public catalog data (cached)
  overview TEXT,
  tagline TEXT,
  genres TEXT[] DEFAULT '{}',
  original_language TEXT,
  spoken_languages TEXT[] DEFAULT '{}',
  poster_path TEXT,
  backdrop_path TEXT,
  logo_path TEXT,
  vote_average DECIMAL(3,1),
  vote_count INTEGER,
  popularity DECIMAL(10,3),
  first_air_date DATE,
  last_air_date DATE,
  release_date DATE,
  
  -- Movie-specific
  runtime INTEGER,
  budget BIGINT,
  revenue BIGINT,
  
  -- TV-specific
  number_of_seasons INTEGER,
  number_of_episodes INTEGER,
  series_status TEXT,
  episode_run_time INTEGER[],
  
  -- Streaming providers (JSON for flexibility)
  provider_data JSONB,
  
  -- User data ("My Data")
  my_status TEXT CHECK (my_status IN ('active', 'next', 'later', 'done', 'quit', 'wait')),
  my_status_updated_at TIMESTAMPTZ,
  my_interest TEXT CHECK (my_interest IN ('excited', 'interested')),
  my_interest_updated_at TIMESTAMPTZ,
  my_tags TEXT[] DEFAULT '{}',
  my_tags_updated_at TIMESTAMPTZ,
  my_score DECIMAL(3,1) CHECK (my_score >= 0 AND my_score <= 10),
  my_score_updated_at TIMESTAMPTZ,
  
  -- AI data
  ai_scoop TEXT,
  ai_scoop_updated_at TIMESTAMPTZ,
  
  -- Metadata
  catalog_updated_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  
  UNIQUE(namespace_id, user_id, tmdb_id),
  INDEX shows_namespace_user_idx ON shows(namespace_id, user_id),
  INDEX shows_status_idx ON shows(namespace_id, user_id, my_status),
  INDEX shows_tags_idx USING GIN(my_tags)
);

-- Cast/Crew (denormalized for performance, refreshed from catalog)
CREATE TABLE credits (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  show_id UUID REFERENCES shows(id) ON DELETE CASCADE,
  person_tmdb_id INTEGER NOT NULL,
  name TEXT NOT NULL,
  character TEXT,
  job TEXT,
  department TEXT,
  profile_path TEXT,
  order_index INTEGER,
  UNIQUE(show_id, person_tmdb_id, job, character)
);

-- Sessions for AI chat (ephemeral, but stored for context)
CREATE TABLE chat_sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  namespace_id TEXT NOT NULL,
  user_id TEXT NOT NULL,
  session_type TEXT NOT NULL CHECK (session_type IN ('ask', 'alchemy')),
  context_show_id UUID REFERENCES shows(id),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  last_activity_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE chat_messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id UUID REFERENCES chat_sessions(id) ON DELETE CASCADE,
  role TEXT NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
  content TEXT NOT NULL,
  mentioned_shows JSONB, -- Array of {tmdb_id, title, media_type}
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- User settings (synced)
CREATE TABLE user_settings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  namespace_id TEXT NOT NULL,
  user_id TEXT NOT NULL UNIQUE,
  username TEXT,
  ai_model TEXT DEFAULT 'gpt-4o-mini',
  font_size TEXT DEFAULT 'M' CHECK (font_size IN ('XS', 'S', 'M', 'L', 'XL', 'XXL')),
  search_on_launch BOOLEAN DEFAULT FALSE,
  hide_status_removal_confirmation BOOLEAN DEFAULT FALSE,
  version INTEGER DEFAULT 1, -- For conflict resolution
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(namespace_id, user_id)
);

-- App metadata for migrations
CREATE TABLE app_metadata (
  id INTEGER PRIMARY KEY DEFAULT 1 CHECK (id = 1),
  data_model_version INTEGER DEFAULT 1,
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

### 3.2 Row Level Security (RLS) Policies

```sql
-- Enable RLS on all tables
ALTER TABLE shows ENABLE ROW LEVEL SECURITY;
ALTER TABLE credits ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_settings ENABLE ROW LEVEL SECURITY;

-- Shows: users can only access their namespace + user data
CREATE POLICY shows_isolation ON shows
  FOR ALL USING (namespace_id = current_setting('app.namespace_id', TRUE));

-- Similar policies for other tables...
```

---

## 4. Feature Implementation

### 4.1 Collection Home

**Purpose**: Display user's library organized by relationship/status.

**Implementation Steps**:
1. **Data Fetching**
   - Server Action: `getCollection(namespace_id, user_id, filter?)`
   - Query shows table with grouping by `my_status`

2. **Grouping Logic**
   ```typescript
   const groups = {
     active: shows.filter(s => s.my_status === 'active'),
     excited: shows.filter(s => s.my_status === 'later' && s.my_interest === 'excited'),
     interested: shows.filter(s => s.my_status === 'later' && s.my_interest === 'interested'),
     other: shows.filter(s => ['wait', 'quit', 'done'].includes(s.my_status))
   };
   ```

3. **Filters Sidebar**
   - "All Shows" (default)
   - Tags: dynamically generate from `my_tags` array
   - Data filters: genre, decade, community score ranges
   - Media type toggle: All / Movies / TV

4. **Empty States**
   - No collection: CTA to Search/Ask with illustration
   - Filter yields none: "No results found" with clear filter option

### 4.2 Search (Find → Search)

**Purpose**: Find shows in the global catalog.

**Implementation Steps**:
1. **Catalog Integration**
   - Create `lib/catalog/tmdb.ts` client
   - Implement `searchCatalog(query: string, page?: number)`
   - Map TMDB response to internal Show type

2. **Search UI**
   - Debounced input (300ms)
   - Grid of poster tiles
   - Infinite scroll or pagination
   - Loading skeletons

3. **Collection Integration**
   - Mark in-collection items with badge
   - Quick-add buttons on hover (Interested/Excited/Active)

### 4.3 Show Detail Page

**Purpose**: Single source of truth for a show with My Data + discovery.

**Implementation Steps**:
1. **Data Loading**
   - Check if show exists in user's collection
   - Fetch full catalog details from TMDB if needed
   - Merge stored data with fresh catalog data

2. **Header Section**
   - Backdrop/poster carousel with lazy loading
   - Logo display (if available)
   - Trailer embed (if available)

3. **My Data Controls**
   - Status chips: Active, Interested, Excited, Done, Quit, Wait
   - Interest toggle (visible only when Later selected)
   - Rating slider (0-10, marks at integers)
   - Tag input with autocomplete from existing tags
   - Auto-save logic:
     - Rating unsaved show → save as `Done`
     - Tag on unsaved show → save as `Later + Interested`
     - Any status → save with defaults

4. **AI Scoop Section**
   - Toggle: "Give me the scoop!" / "Show the scoop"
   - Progressive streaming display
   - Regenerate after 4 hours
   - Persist only if show in collection

5. **Explore Similar**
   - "Get Concepts" button → fetch AI concepts
   - Display concepts as selectable chips
   - "Explore Shows" → get recommendations
   - Show 5 AI recommendations with reasons

6. **Additional Sections**
   - Overview, Genres, Languages
   - Traditional recommendations strand
   - Streaming availability (providers)
   - Cast & Crew (horizontal scroll)
   - Seasons accordion (TV only)
   - Budget/Revenue (movies)

### 4.4 Ask (AI Chat)

**Purpose**: Conversational discovery grounded in taste.

**Implementation Steps**:
1. **Session Management**
   - Create `chat_sessions` entry on first message
   - Maintain message history in `chat_messages`
   - Cleanup old sessions (optional)

2. **AI Integration**
   - Build prompt with:
     - User's library (titles, statuses, ratings, tags)
     - Recent conversation turns
     - System persona instructions
   - Handle structured output for mentioned shows

3. **UI Components**
   - Message bubbles (user/assistant)
   - "Mentioned shows" horizontal strip
   - Welcome view with 6 random starter prompts
   - Refresh prompts button

4. **Context Management**
   - Summarize older turns after ~10 messages
   - Preserve conversation feel while controlling tokens

5. **Ask About Show**
   - Launch from Detail page with pre-filled context
   - Seed conversation with show details

### 4.5 Alchemy (Find → Alchemy)

**Purpose**: Structured discovery by blending multiple shows.

**Implementation Steps**:
1. **Input Selection**
   - Dual search: user's collection + catalog
   - Minimum 2 shows, no maximum
   - Display as removable chips

2. **Concept Generation**
   - AI prompt with all selected shows
   - Return 8 shared concepts (1-3 words each)
   - Display as selectable chips

3. **Recommendation Flow**
   - User selects 1-8 concepts
   - "Alchemize!" button → fetch 6 recommendations
   - Each rec includes reason tied to selected concepts
   - "More Alchemy!" to chain with results as inputs

4. **State Management**
   - Clear concepts when inputs change
   - Clear results when concepts change
   - Allow backtracking

### 4.6 Person Detail Page

**Purpose**: Explore talent behind shows.

**Implementation Steps**:
1. **Data Fetching**
   - Fetch from TMDB: person details, images, credits
   - Group filmography by year
   - Calculate analytics: avg ratings, top genres, projects by year

2. **UI Layout**
   - Image gallery with lightbox
   - Name, bio, known for
   - Analytics charts (simple bar/line charts)
   - Filmography list with year grouping
   - Click credit → navigate to Show Detail

### 4.7 Settings & Data Management

**Purpose**: App configuration and data portability.

**Implementation Steps**:
1. **Settings Form**
   - Username input
   - Font size selector (XS-XXL)
   - Search on launch toggle
   - AI model selection
   - API key inputs (backend-encrypted)

2. **Export/Backup**
   - "Export My Data" button
   - Generate JSON with all shows, settings
   - Package as ZIP download
   - ISO-8601 date encoding

3. **Import/Restore** (Future)
   - File upload for ZIP
   - Validate and merge data
   - Conflict resolution by timestamp

---

## 5. AI Implementation

### 5.1 Prompt Architecture

**Base System Prompt** (included in all AI calls):
```
You are a fun, chatty TV/movie nerd friend. You:
- Love entertainment deeply and show it
- Have sharp taste and aren't afraid to make a call
- Are generous with context and insider info
- Stay spoiler-safe unless explicitly invited
- Keep things light even when being critical

Tone: 70% friend / 30% critic, 60% hype / 40% measured
```

### 5.2 Surface-Specific Prompts

**Scoop Generation**:
- Input: Show details + user library context
- Output structure:
  1. Personal take (make a stand)
  2. Honest stack-up vs reviews
  3. The Scoop paragraph (emotional centerpiece)
  4. Practical fit/warnings
  5. "Worth it?" verdict
- Length: 150-350 words

**Concept Generation**:
- Single show: return 8 concepts
- Multi-show (Alchemy): return shared concepts only
- Format: Bullet list, 1-3 words each
- Constraints: No plot details, no generics ("good characters")

**Recommendations**:
- Input: Selected concepts + user library
- Output: 5-6 shows with reasons
- Each reason must reference specific concepts
- Include external ID for catalog resolution

**Chat (Ask)**:
- Include user library in context
- Mentioned shows format: `Title::externalId::mediaType;;...`
- Parse and store separately for UI display

### 5.3 AI Client Implementation

```typescript
// lib/ai/client.ts
export async function generateScoop(show: Show, library: Show[]): Promise<string>;
export async function generateConcepts(shows: Show[]): Promise<string[]>;
export async function generateRecommendations(
  concepts: string[], 
  library: Show[],
  count: number
): Promise<Recommendation[]>;
export async function chatAsk(
  messages: Message[], 
  library: Show[],
  contextShow?: Show
): Promise<{content: string, mentionedShows: MentionedShow[]}>;
```

---

## 6. External Catalog Integration

### 6.1 TMDB Client

```typescript
// lib/catalog/tmdb.ts
const TMDB_BASE_URL = 'https://api.themoviedb.org/3';

export async function searchShows(query: string, page?: number): Promise<SearchResult>;
export async function getShowDetails(tmdbId: number, type: 'movie' | 'tv'): Promise<ShowDetails>;
export async function getPersonDetails(tmdbId: number): Promise<PersonDetails>;
export async function getRecommendations(tmdbId: number, type: 'movie' | 'tv'): Promise<Show[]>;
export async function getSimilar(tmdbId: number, type: 'movie' | 'tv'): Promise<Show[]>;
export async function getCredits(tmdbId: number, type: 'movie' | 'tv'): Promise<Credits>;
export async function getProviders(tmdbId: number, type: 'movie' | 'tv'): Promise<ProviderData>;
```

### 6.2 Data Mapping

| TMDB Field | Internal Field |
|------------|----------------|
| id | tmdb_id |
| title / name | title |
| media_type | show_type |
| overview | overview |
| genre_ids → names | genres |
| poster_path | poster_path |
| backdrop_path | backdrop_path |
| vote_average | vote_average |
| release_date / first_air_date | release_date / first_air_date |
| runtime / episode_run_time | runtime / episode_run_time |
| number_of_seasons | number_of_seasons |
| watch/providers | provider_data |

### 6.3 Image URL Construction

```typescript
const IMAGE_BASE_URL = 'https://image.tmdb.org/t/p';
const POSTER_SIZE = 'w342';
const BACKDROP_SIZE = 'w780';
const LOGO_SIZE = 'w185';

function getImageUrl(path: string | null, size: string): string | null {
  return path ? `${IMAGE_BASE_URL}/${size}${path}` : null;
}
```

---

## 7. Data Behaviors & Business Logic

### 7.1 Collection Membership

A show is "in collection" when `my_status` is non-null.

### 7.2 Saving Triggers

| Action | Effect |
|--------|--------|
| Set any status | Save with status |
| Select Interested/Excited chip | Save as Later + Interest |
| Rate unsaved show | Save as Done |
| Add tag to unsaved show | Save as Later + Interested |

### 7.3 Default Values

On first save without explicit status:
- `my_status = 'later'`
- `my_interest = 'interested'`

Exception: Rating an unsaved show defaults to `my_status = 'done'`.

### 7.4 Removal

Trigger: User clears status (reselects active status and confirms).

Effects:
- Delete show record (or nullify all My Data)
- Clear status, interest, tags, rating, AI scoop
- Show confirmation (with "don't ask again" option)

### 7.5 Merge Policy

When external catalog data is merged into stored show:

**Catalog fields**: Use `selectFirstNonEmpty(newValue, oldValue)`
- Never overwrite non-empty with empty
- Never overwrite non-null with null

**User fields**: Resolve by timestamp
- Keep newer based on `*_updated_at` fields
- Preserves user edits across syncs

### 7.6 Timestamps

All user data fields track modification time:
- `my_status_updated_at`
- `my_interest_updated_at`
- `my_tags_updated_at`
- `my_score_updated_at`
- `ai_scoop_updated_at`

Uses:
- Sorting recently updated
- Conflict resolution
- AI cache freshness (4 hours for scoop)

---

## 8. UI/UX Specifications

### 8.1 Design Principles

1. **User's version takes precedence** everywhere
2. **Discovery must be actionable**: every recommendation is a real show
3. **Taste-aware AI**: use library + My Data + context
4. **Spoiler-safe by default**
5. **Implicit behaviors feel natural**
6. **Your data is yours**: export/backup first-class

### 8.2 Show Tile Requirements

- Poster image (lazy loaded)
- Title overlay
- Collection indicator (small badge when `my_status` exists)
- User rating indicator (when `my_score` exists)
- Hover: quick actions (Interested/Excited/Active)

### 8.3 Color & Typography

- Primary action: accent color for status chips, CTAs
- Status colors: Active (green), Excited (orange), Interested (blue)
- Typography: System font stack, configurable sizes (XS-XXL)
- Dark mode support (optional but recommended)

### 8.4 Animations

- Page transitions: simple fade
- Tile hover: subtle scale (1.02)
- Loading: skeleton placeholders
- Scoop streaming: typewriter/word-by-word reveal

---

## 9. Development Workflow

### 9.1 Environment Setup

Create `.env.example`:
```env
# Database
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# External APIs
TMDB_API_KEY=your-tmdb-key
OPENAI_API_KEY=your-openai-key

# App
APP_NAMESPACE=default
DEFAULT_USER_ID=dev-user
```

### 9.2 Scripts

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "test": "jest",
    "test:reset": "node scripts/reset-test-data.js",
    "db:migrate": "supabase migration up",
    "db:reset": "supabase db reset"
  }
}
```

### 9.3 Testing Strategy

1. **Unit Tests**: Utility functions, data mapping
2. **Integration Tests**: API routes with test namespace
3. **E2E Tests**: Critical user journeys with Playwright

### 9.4 Dev Identity Injection

```typescript
// middleware.ts or API helper
function getDevContext(request: NextRequest): { namespaceId: string, userId: string } {
  const namespaceId = request.headers.get('X-Namespace-Id') || process.env.APP_NAMESPACE || 'default';
  const userId = request.headers.get('X-User-Id') || process.env.DEFAULT_USER_ID || 'dev-user';
  return { namespaceId, userId };
}
```

---

## 10. Deployment & Operations

### 10.1 Build Configuration

- Environment variables validated at build time
- No secrets committed to repo
- Service role key server-only

### 10.2 Database Migrations

1. Create migration: `supabase migration new description`
2. Edit `supabase/migrations/YYYYMMDDHHMMSS_description.sql`
3. Apply: `supabase migration up`

### 10.3 Monitoring

- Error tracking: Sentry or similar
- AI usage: Monitor token consumption
- Performance: Core Web Vitals

---

## 11. Implementation Phases

### Phase 1: Foundation (Week 1)
- [ ] Project setup (Next.js, Supabase, Tailwind)
- [ ] Database schema + migrations
- [ ] TMDB client + basic search
- [ ] Show Detail page (no AI)

### Phase 2: Collection Core (Week 2)
- [ ] Collection Home with status groups
- [ ] My Data controls (status, interest, tags, rating)
- [ ] Save/remove business logic
- [ ] Filters sidebar

### Phase 3: AI Discovery (Week 3)
- [ ] AI client integration
- [ ] Scoop generation
- [ ] Concept generation
- [ ] Ask chat interface

### Phase 4: Alchemy & Polish (Week 4)
- [ ] Alchemy multi-show flow
- [ ] Explore Similar
- [ ] Person Detail
- [ ] Settings + Export
- [ ] Testing + Bug fixes

---

## 12. Open Questions Resolution

| Question | Decision |
|----------|----------|
| Should "Next" become first-class status? | Not for MVP; keep hidden |
| Custom named lists beyond tags? | Not for MVP; tags suffice |
| Scoop on unsaved show → save? | No, ephemeral only |
| Clear rating = explicit "Unrated"? | No, store as null |
| Import/Restore from export? | Future enhancement |
| Save Alchemy sessions? | Future enhancement |
| myStatus filters in sidebar? | Yes, implement |

---

## 13. Success Criteria

- User can build and maintain a collection
- Status/interest/tag updates persist correctly
- AI recommendations are taste-aware and actionable
- Data exports successfully
- No data collisions between namespace runs
- All user data scoped to user_id
- Dev identity injection works without full OAuth
