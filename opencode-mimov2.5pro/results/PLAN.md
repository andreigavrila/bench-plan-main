# Implementation Plan — TV/Movie Companion App

## 1. Architecture Overview

### Tech Stack
- **Framework:** Next.js 14+ (App Router)
- **Persistence:** Supabase (PostgreSQL + Realtime)
- **Styling:** Tailwind CSS + shadcn/ui
- **AI Integration:** Vercel AI SDK (provider-agnostic)
- **State Management:** React Query (TanStack Query) for server state, Zustand for client state
- **Testing:** Vitest + React Testing Library + Playwright (E2E)

### Architecture Pattern
Fractal architecture with self-contained features:
```
src/
├── config/          # Environment, constants, feature flags
├── theme/           # Design tokens, typography, colors
├── components/      # Shared UI primitives
├── hooks/           # Global hooks (useUser, useNamespace, useSupabase)
├── utils/           # Pure functions (dates, formatting, merge logic)
├── lib/             # Supabase client, AI SDK setup
├── types/           # Shared TypeScript types
└── pages/
    ├── Home/        # Collection view
    ├── Detail/      # Show detail page
    ├── Find/        # Discovery hub (Search, Ask, Alchemy)
    ├── Person/      # Cast/crew profiles
    └── Settings/    # App configuration
```

---

## 2. Database Schema (Supabase)

### Tables

#### `shows`
Primary table for user-owned show records with embedded user data.

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | uuid | PK, default gen_random_uuid() | Internal ID |
| `user_id` | uuid | NOT NULL, FK → auth.users | Ownership |
| `namespace_id` | text | NOT NULL | Build isolation |
| `external_id` | text | NOT NULL | Catalog provider ID |
| `title` | text | NOT NULL | |
| `show_type` | text | NOT NULL | movie, tv, person, unknown |
| `overview` | text | | |
| `genres` | text[] | DEFAULT '{}' | |
| `tagline` | text | | |
| `poster_url` | text | | |
| `backdrop_url` | text | | |
| `logo_url` | text | | |
| `vote_average` | float | | |
| `vote_count` | int | | |
| `popularity` | float | | |
| `release_date` | date | | |
| `first_air_date` | date | | |
| `last_air_date` | date | | |
| `runtime` | int | | Minutes (movies) |
| `budget` | bigint | | |
| `revenue` | bigint | | |
| `number_of_seasons` | int | | |
| `number_of_episodes` | int | | |
| `series_status` | text | | |
| `original_language` | text | | |
| `spoken_languages` | text[] | DEFAULT '{}' | |
| `my_status` | text | | active, later, done, quit, wait |
| `my_interest` | text | | excited, interested |
| `my_score` | float | | 0-10 |
| `my_tags` | text[] | DEFAULT '{}' | |
| `ai_scoop` | text | | |
| `ai_scoop_updated_at` | timestamptz | | |
| `my_status_updated_at` | timestamptz | | |
| `my_interest_updated_at` | timestamptz | | |
| `my_score_updated_at` | timestamptz | | |
| `my_tags_updated_at` | timestamptz | | |
| `details_updated_at` | timestamptz | | Last catalog refresh |
| `created_at` | timestamptz | DEFAULT now() | |
| `updated_at` | timestamptz | DEFAULT now() | |
| `is_test` | boolean | DEFAULT false | |

**Composite unique constraint:** `(user_id, namespace_id, external_id)`

#### `provider_data`
Streaming availability per region.

| Column | Type | Notes |
|--------|------|-------|
| `id` | uuid | PK |
| `show_id` | uuid | FK → shows |
| `country_code` | text | ISO 3166-1 |
| `provider_type` | text | flatrate, rent, buy |
| `provider_ids` | int[] | Catalog provider IDs |

#### `cloud_settings`
Synced user preferences.

| Column | Type | Notes |
|--------|------|-------|
| `user_id` | uuid | PK |
| `namespace_id` | text | PK |
| `user_name` | text | Random on first launch |
| `catalog_api_key` | text | Encrypted at rest |
| `ai_api_key` | text | Encrypted at rest |
| `ai_model` | text | Default model key |
| `version` | bigint | Epoch seconds for conflict resolution |
| `updated_at` | timestamptz | |

#### `app_metadata`
Tracks schema version for migrations.

| Column | Type | Notes |
|--------|------|-------|
| `namespace_id` | text | PK |
| `data_model_version` | int | Default 3 |

### Indexes
```sql
CREATE INDEX idx_shows_user_namespace ON shows(user_id, namespace_id);
CREATE INDEX idx_shows_status ON shows(my_status) WHERE my_status IS NOT NULL;
CREATE INDEX idx_shows_tags ON shows USING GIN(my_tags);
CREATE INDEX idx_provider_data_show ON provider_data(show_id);
```

### Row Level Security (RLS)
```sql
ALTER TABLE shows ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users see own shows" ON shows
  FOR ALL USING (auth.uid() = user_id);
```

---

## 3. Feature Breakdown

### 3.1 Authentication & Identity

**Benchmark Mode (Default)**
- Inject `user_id` via `X-User-Id` header (server routes only)
- Default user auto-created per namespace
- No OAuth UI required

**Production Path (Future)**
- Supabase Auth with Google OAuth
- Same `user_id` field, just sourced differently

**Implementation:**
- `src/hooks/useUser.ts` — Returns current user ID
- `src/lib/auth.ts` — Dev identity injection middleware
- `src/config/env.ts` — `BENCHMARK_USER_ID` env var

### 3.2 Namespace Isolation

Every query is scoped to `(user_id, namespace_id)`.

**Implementation:**
- `NAMESPACE_ID` environment variable (set per build/run)
- All Supabase queries include `.eq('namespace_id', namespaceId)`
- `src/lib/supabase.ts` — Client with namespace context

### 3.3 Collection Home

**Route:** `/`

**Features:**
- Status-grouped sections: Active → Excited → Interested → Other
- Media-type toggle (All / Movies / TV)
- Filter sidebar (All Shows, tags, genres, decades, scores)
- Empty states with Search/Ask prompts

**Components:**
```
pages/Home/
├── Home.tsx
├── features/
│   ├── CollectionGrid/
│   │   ├── CollectionGrid.tsx
│   │   ├── hooks/useCollectionQuery.ts
│   │   └── features/
│   │       ├── StatusSection/
│   │       │   ├── StatusSection.tsx
│   │       │   └── StatusSection.constants.ts
│   │       └── ShowTile/
│   │           ├── ShowTile.tsx
│   │           ├── hooks/useShowTile.ts
│   │           └── ShowTile.module.css
│   ├── FilterSidebar/
│   │   ├── FilterSidebar.tsx
│   │   ├── hooks/useFilters.ts
│   │   └── features/
│   │       ├── TagFilter/
│   │       └── GenreFilter/
│   └── MediaTypeToggle/
│       └── MediaTypeToggle.tsx
```

### 3.4 Search

**Route:** `/find` (Search tab)

**Features:**
- Text search via catalog API (TMDB or configured provider)
- Poster grid results
- In-collection badges
- "Search on Launch" setting

**Components:**
```
pages/Find/
├── Find.tsx
├── features/
│   ├── SearchView/
│   │   ├── SearchView.tsx
│   │   ├── hooks/useSearch.ts
│   │   └── features/
│   │       ├── SearchBar/
│   │       └── SearchResults/
│   ├── AskView/
│   │   └── (see 3.5)
│   └── AlchemyView/
│       └── (see 3.6)
```

### 3.5 Ask (AI Chat)

**Route:** `/find` (Ask tab)

**Features:**
- Chat UI with streaming responses
- "Mentioned shows" strip (structured output parsing)
- Welcome view with 6 random starter prompts
- Session-only history (summarized after ~10 messages)
- "Ask about this show" variant (seeded context from Detail)

**AI Contract:**
- Input: user message + library context + recent turns
- Output: `{ commentary: string, showList: "Title::id::type;;..." }`
- Persona: fun, chatty, opinionated, spoiler-safe

**Components:**
```
pages/Find/features/AskView/
├── AskView.tsx
├── hooks/
│   ├── useAskChat.ts
│   └── useShowMentions.ts
├── utils/
│   └── parseShowMentions.ts
└── features/
    ├── ChatBubble/
    ├── MentionedShows/
    └── StarterPrompts/
```

### 3.6 Alchemy (Concept Blending)

**Route:** `/find` (Alchemy tab)

**Flow:**
1. Select 2+ shows (library + catalog search)
2. "Conceptualize Shows" → AI extracts shared concepts
3. Select 1-8 concept chips
4. "ALCHEMIZE!" → 6 recommendations with reasons
5. Optional "More Alchemy!" chaining

**AI Contract:**
- Concept extraction: `{ concepts: string[] }` (1-3 words each, shared across inputs)
- Recommendations: `{ shows: [{ title, externalId, reason }] }` (6 per round)

**Components:**
```
pages/Find/features/AlchemyView/
├── AlchemyView.tsx
├── hooks/
│   ├── useAlchemy.ts
│   ├── useConceptExtraction.ts
│   └── useAlchemyRecommendations.ts
├── utils/
│   └── resolveExternalShow.ts
└── features/
    ├── ShowSelector/
    ├── ConceptChips/
    └── RecommendationGrid/
```

### 3.7 Show Detail

**Route:** `/show/[id]`

**Sections (top to bottom):**
1. Header media carousel (backdrops/posters/logos/trailers)
2. Core facts (year, runtime/seasons) + community score
3. My Tags + tag picker
4. Overview + AI Scoop toggle/stream
5. "Ask about this show" CTA
6. Genres + languages
7. Recommendations strand (similar shows)
8. Explore Similar (concepts → recs)
9. Streaming providers
10. Cast & Crew strands → Person Detail
11. Seasons (TV only)
12. Budget/Revenue (movies)

**Status/Interest Controls:**
- Toolbar chips: Active, Interested, Excited, Later, Wait, Done, Quit
- Reselecting active status → removal confirmation
- Auto-save rules:
  - Rating unsaved show → Done
  - Adding tag unsaved → Later + Interested

**AI Scoop:**
- Toggle: "Give me the scoop!" / "Show the scoop"
- Streams progressively
- 4-hour freshness cache
- Persists only if show in collection

**Components:**
```
pages/Detail/
├── Detail.tsx
├── hooks/
│   ├── useShowDetail.ts
│   ├── useShowMutations.ts
│   └── useAIScoop.ts
├── utils/
│   └── mergeShowData.ts
└── features/
    ├── HeaderMedia/
    │   └── HeaderMedia.tsx
    ├── StatusToolbar/
    │   ├── StatusToolbar.tsx
    │   └── hooks/useStatusActions.ts
    ├── RatingBar/
    ├── TagPicker/
    ├── OverviewSection/
    ├── ScoopSection/
    │   ├── ScoopSection.tsx
    │   └── hooks/useScoopStream.ts
    ├── ExploreSimilar/
    │   ├── ExploreSimilar.tsx
    │   └── hooks/useExploreSimilar.ts
    ├── Recommendations/
    ├── Providers/
    ├── CastCrew/
    ├── Seasons/
    └── BudgetRevenue/
```

### 3.8 Person Detail

**Route:** `/person/[id]`

**Features:**
- Image gallery
- Bio
- Analytics charts (avg ratings, top genres, projects-by-year)
- Filmography grouped by year
- Tap credit → Show Detail

**Components:**
```
pages/Person/
├── Person.tsx
├── hooks/usePerson.ts
└── features/
    ├── PersonGallery/
    ├── PersonAnalytics/
    │   └── features/
    │       ├── RatingsChart/
    │       ├── GenresChart/
    │       └── ProjectsByYear/
    └── Filmography/
```

### 3.9 Settings

**Route:** `/settings`

**Sections:**
- App: Font size, Search on Launch
- User: Username
- AI: API key, model selection
- Integrations: Catalog API key
- Data: Export My Data (.zip backup)

**Components:**
```
pages/Settings/
├── Settings.tsx
├── hooks/useSettings.ts
└── features/
    ├── AppSettings/
    ├── UserSettings/
    ├── AISettings/
    ├── Integrations/
    └── DataExport/
        ├── DataExport.tsx
        └── utils/exportToZip.ts
```

---

## 4. API Routes (Next.js Server Actions / Route Handlers)

### Shows
- `GET /api/shows` — List collection (filtered, paginated)
- `GET /api/shows/[id]` — Get show with transient data
- `POST /api/shows` — Save show to collection
- `PATCH /api/shows/[id]` — Update user data (status, tags, rating)
- `DELETE /api/shows/[id]` — Remove from collection
- `GET /api/shows/search?q=` — Search external catalog

### AI Surfaces
- `POST /api/ai/ask` — Chat (streaming)
- `POST /api/ai/scoop` — Generate Scoop (streaming)
- `POST /api/ai/concepts` — Extract concepts (single or multi-show)
- `POST /api/ai/explore-similar` — Concept-based recommendations
- `POST /api/ai/alchemy` — Alchemy recommendations

### Person
- `GET /api/person/[id]` — Person detail + filmography

### Settings
- `GET /api/settings` — Get cloud settings
- `PATCH /api/settings` — Update settings
- `POST /api/export` — Generate export .zip

### Test Support
- `POST /api/test/reset` — Delete all data for namespace (destructive)

---

## 5. AI Integration Architecture

### Provider Abstraction
```typescript
// src/lib/ai/provider.ts
interface AIProvider {
  chat(messages: Message[], context: AIContext): AsyncStream<Response>;
  extractConcepts(shows: Show[]): Promise<string[]>;
  generateScoop(show: Show): AsyncStream<string>;
  recommend(concepts: string[], context: AIContext): Promise<Recommendation[]>;
}
```

### Context Assembly
For each AI call, assemble:
1. User's library (shows + My Data)
2. Current show context (if applicable)
3. Selected concepts (if applicable)
4. Recent conversation turns (if chat)
5. Namespace/user metadata

### Prompt Templates
- `src/lib/ai/prompts/ask.ts` — Ask chat system prompt
- `src/lib/ai/prompts/scoop.ts` — Scoop generation prompt
- `src/lib/ai/prompts/concepts.ts` — Concept extraction prompt
- `src/lib/ai/prompts/recommend.ts` — Recommendation prompt
- `src/lib/ai/prompts/starters.ts` — 80 conversation starters

### Response Parsing
- `src/lib/ai/parsers/parseShowList.ts` — `Title::id::type;;...` format
- `src/lib/ai/parsers/parseConcepts.ts` — Bullet list extraction
- `src/lib/ai/parsers/parseRecommendations.ts` — Structured rec output

---

## 6. Data Flow & State Management

### Server State (React Query)
- Collection queries with namespace scoping
- Optimistic updates for status/tag/rating changes
- Cache invalidation on mutations
- Prefetch on hover for Show Detail

### Client State (Zustand)
- UI state: selected filter, media type toggle
- Session state: Ask chat history, Alchemy selections
- Local settings: font size, auto-search

### Merge Logic
When catalog data refreshes:
- Non-user fields: `selectFirstNonEmpty(new, old)`
- User fields: timestamp-based (newer wins)
- Always preserve user edits

---

## 7. Implementation Phases

### Phase 1: Foundation (Week 1)
- [ ] Next.js project setup with App Router
- [ ] Supabase client configuration
- [ ] Database schema + migrations
- [ ] RLS policies + namespace isolation
- [ ] Auth middleware (benchmark mode)
- [ ] Shared types from schema
- [ ] Theme + design tokens

### Phase 2: Core Collection (Week 2)
- [ ] Show Detail page (all sections)
- [ ] Status/Interest controls with auto-save
- [ ] Tag system
- [ ] Rating system
- [ ] Collection Home with status grouping
- [ ] Filter sidebar
- [ ] Media type toggle

### Phase 3: Discovery (Week 3)
- [ ] Search (catalog API integration)
- [ ] Ask chat with streaming
- [ ] Mentioned shows parsing
- [ ] Starter prompts
- [ ] AI Scoop generation + streaming
- [ ] Explore Similar (concepts → recs)

### Phase 4: Advanced Discovery (Week 4)
- [ ] Alchemy full flow
- [ ] Concept extraction (single + multi-show)
- [ ] Recommendation resolution to real shows
- [ ] Chaining support

### Phase 5: Polish & Infrastructure (Week 5)
- [ ] Person Detail page
- [ ] Settings page
- [ ] Data export
- [ ] Streaming providers display
- [ ] Seasons display
- [ ] Budget/Revenue display

### Phase 6: Quality & Testing (Week 6)
- [ ] Unit tests for critical logic
- [ ] Component tests for key features
- [ ] E2E tests for user journeys
- [ ] AI quality validation against golden set
- [ ] Performance optimization

---

## 8. Environment Configuration

### Required Variables
```env
# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...
SUPABASE_SERVICE_ROLE_KEY=eyJ...  # Server only

# Namespace & Identity
NAMESPACE_ID=benchmark-run-001
BENCHMARK_USER_ID=dev-user-001  # Benchmark mode only

# AI Provider
AI_PROVIDER=openai  # or anthropic, etc.
AI_API_KEY=sk-...

# Catalog Provider
CATALOG_API_KEY=...  # TMDB or equivalent
```

### Scripts
```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "test": "vitest",
    "test:e2e": "playwright test",
    "test:reset": "tsx scripts/reset-namespace.ts",
    "db:migrate": "supabase db push",
    "db:seed": "tsx scripts/seed.ts"
  }
}
```

---

## 9. Key Business Rules Implementation

### Auto-Save Triggers
```typescript
// src/hooks/useShowMutations.ts
function useShowMutations(show: Show | null) {
  const saveShow = useMutation({
    mutationFn: async (data: Partial<Show>) => {
      if (!show) {
        // New save: default to Later + Interested
        return createShow({
          ...data,
          myStatus: 'later',
          myInterest: 'interested',
          myStatusUpdatedAt: new Date(),
          myInterestUpdatedAt: new Date(),
        });
      }
      return updateShow(show.id, data);
    },
  });

  const rateShow = (score: number) => {
    if (!show) {
      // Rating unsaved → Done
      saveShow.mutate({
        myScore: score,
        myStatus: 'done',
        myScoreUpdatedAt: new Date(),
      });
    } else {
      saveShow.mutate({
        myScore: score,
        myScoreUpdatedAt: new Date(),
      });
    }
  };

  const addTag = (tag: string) => {
    if (!show) {
      // Tag unsaved → Later + Interested
      saveShow.mutate({
        myTags: [tag],
        myStatus: 'later',
        myInterest: 'interested',
        myTagsUpdatedAt: new Date(),
      });
    } else {
      saveShow.mutate({
        myTags: [...show.myTags, tag],
        myTagsUpdatedAt: new Date(),
      });
    }
  };

  return { saveShow, rateShow, addTag };
}
```

### Status Removal Flow
```typescript
// src/features/StatusToolbar/hooks/useStatusActions.ts
function useStatusActions(show: Show) {
  const removeShow = useMutation({
    mutationFn: async () => {
      // Clear all My Data
      await deleteShow(show.id);
      // Redirect to home or close detail
    },
  });

  const handleStatusSelect = (status: MyStatusType) => {
    if (status === show.myStatus) {
      // Reselecting → removal confirmation
      if (shouldShowConfirmation()) {
        showRemovalConfirmation({
          onConfirm: () => removeShow.mutate(),
          onDontAskAgain: () => setHideConfirmation(true),
        });
      } else {
        removeShow.mutate();
      }
    } else {
      // New status
      updateShow(show.id, {
        myStatus: status,
        myStatusUpdatedAt: new Date(),
        // Clear interest if not Later
        myInterest: status === 'later' ? show.myInterest : null,
      });
    }
  };

  return { handleStatusSelect };
}
```

### AI Scoop Freshness
```typescript
// src/hooks/useAIScoop.ts
function useAIScoop(show: Show) {
  const SCOOP_MAX_AGE = 4 * 60 * 60 * 1000; // 4 hours

  const isScoopFresh = show.aiScoopUpdatedAt
    ? Date.now() - new Date(show.aiScoopUpdatedAt).getTime() < SCOOP_MAX_AGE
    : false;

  const shouldShowCached = show.aiScoop && isScoopFresh;

  const generateScoop = useMutation({
    mutationFn: async () => {
      const stream = await fetch('/api/ai/scoop', {
        method: 'POST',
        body: JSON.stringify({ showId: show.id }),
      });
      return stream;
    },
    onSuccess: async (stream) => {
      // Stream to UI
      // On complete, persist if show in collection
      if (show.myStatus) {
        await updateShow(show.id, {
          aiScoop: accumulatedText,
          aiScoopUpdatedAt: new Date(),
        });
      }
    },
  });

  return { shouldShowCached, generateScoop };
}
```

---

## 10. Testing Strategy

### Unit Tests
- Merge logic (`mergeShowData`)
- Status/interest auto-save rules
- Concept validation (1-3 words, no generic)
- Show mention parsing
- Filter logic

### Component Tests
- ShowTile with various states
- StatusToolbar interactions
- TagPicker add/remove
- RatingBar with auto-save

### E2E Tests (Playwright)
1. Build collection: Search → save → verify in Home
2. Rate-to-save: Search → rate → verify Done status
3. Tag-to-save: Search → tag → verify Later + Interested
4. Ask discovery: chat → select recommendation → save
5. Alchemy: pick shows → concepts → recommendations → save
6. Explore Similar: Detail → concepts → recs → save
7. Export: Settings → export → verify .zip contents

### AI Quality Tests
- Scoop: sections present, spoiler-safe, honest about mixed reviews
- Ask: direct answers, bulleted lists, confident picks
- Concepts: 8 generated, 1-3 words, no generic
- Recommendations: real shows, reasons cite concepts

---

## 11. Deployment & DevOps

### Local Development
```bash
# 1. Copy env
cp .env.example .env.local

# 2. Start Supabase (optional, can use hosted)
npx supabase start

# 3. Run migrations
npm run db:migrate

# 4. Start dev server
npm run dev
```

### Cloud Agent (Benchmark)
- Connect to hosted Supabase
- Set `NAMESPACE_ID` per run
- Run tests with namespace isolation
- Reset via `npm run test:reset`

### Production (Future)
- Vercel deployment
- Supabase hosted
- Real OAuth via Supabase Auth
- Environment-based feature flags

---

## 12. Migration Path

### Current → Production
1. Replace `BENCHMARK_USER_ID` injection with Supabase Auth
2. Add OAuth UI (Google)
3. Update RLS to use `auth.uid()`
4. No schema changes required

### Schema Evolution
- `app_metadata.data_model_version` tracks current version
- Migrations run on startup
- User data preserved across versions (merge rules apply)

---

## 13. Risk Mitigation

| Risk | Mitigation |
|------|------------|
| AI hallucinated shows | Resolve to real catalog items; fallback to Search |
| Structured output parsing fails | Retry once with stricter format; fallback to unstructured |
| Namespace collision | Enforce `(user_id, namespace_id)` partitioning |
| Data loss on update | Timestamp-based merge; never delete without confirmation |
| AI costs | Cache Scoop 4h; session-only for Ask/Alchemy |
| Catalog API limits | Cache resolved shows; batch lookups |

---

## 14. Success Criteria Checklist

- [ ] `.env.example` provided, configurable without code edits
- [ ] Namespace isolation prevents data collisions
- [ ] All user records scoped to `user_id`
- [ ] Destructive testing without global teardown
- [ ] OAuth migration path (no schema redesign)
- [ ] Status system: Active, Later, Wait, Done, Quit
- [ ] Interest levels: Interested, Excited (for Later)
- [ ] Tags: free-form, filterable
- [ ] Search: text search, poster grid, collection badges
- [ ] Ask: streaming chat, mentioned shows, starters
- [ ] Alchemy: 2+ shows → concepts → 6 recommendations
- [ ] Explore Similar: concepts → 5 recommendations
- [ ] AI Scoop: spoiler-safe, 4h cache, persists if saved
- [ ] Person Detail: gallery, bio, analytics, filmography
- [ ] Settings: font size, search on launch, API keys, export
- [ ] Export: .zip with JSON backup, ISO-8601 dates
