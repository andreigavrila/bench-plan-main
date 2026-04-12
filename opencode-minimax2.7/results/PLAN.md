# Implementation Plan

## 1. Project Foundation

### 1.1 Tech Stack
- **Runtime**: Next.js (latest stable) with App Router
- **Persistence**: Supabase (PostgreSQL + client libraries)
- **Styling**: CSS Modules or Tailwind (implementation choice)
- **State**: React Context or Zustand for client state
- **AI**: External AI provider (API key configurable via env)

### 1.2 Required Deliverables
- `.env.example` with all required variables (no secrets committed)
- `.gitignore` excluding `.env*` files
- `npm run dev` — start application
- `npm test` — run tests
- `npm run test:reset` — reset test data for namespace
- Database migrations for repeatable schema setup

### 1.3 Infrastructure Isolation
- **Namespace isolation**: All data scoped by `namespace_id` to prevent collisions between runs
- **User identity**: All user-owned records include `user_id` (opaque string/UUID)
- **Dev identity injection**: `X-User-Id` header or equivalent for development
- **Design for OAuth migration**: Auth mechanism swappable without schema redesign

---

## 2. Data Model

### 2.1 Core Entities

**Show**
- Identity: `id`, `title`, `showType` (movie/tv/person/unknown), `externalIds`
- Catalog: `overview`, `genres`, `tagline`, `homepage`, `languages`, `spokenLanguages`
- Images: `posterUrlString`, `backdropUrlString`, `logoUrlString`
- Ratings: `voteAverage`, `voteCount`, `popularity`
- Dates: `releaseDate`, `firstAirDate`, `lastAirDate`
- Movie: `runtime`, `budget`, `revenue`
- TV: `seriesStatus`, `numberOfEpisodes`, `numberOfSeasons`, `episodeRunTime`
- User data: `myTags`, `myTagsUpdateDate`, `myScore`, `myScoreUpdateDate`, `myStatus`, `myStatusUpdateDate`, `myInterest`, `myInterestUpdateDate`
- AI: `aiScoop`, `aiScoopUpdateDate`
- Meta: `detailsUpdateDate`, `creationDate`, `isTest`, `namespaceId`, `userId`

**Status Enum**: `active`, `later`, `wait`, `done`, `quit`

**Interest Enum**: `interested`, `excited` (only when status is `later`)

**CloudSettings**
- `id` (default "globalSettings"), `userName`, `version`, `catalogApiKey`, `aiApiKey`, `aiModel`, `namespaceId`, `userId`

**AppMetadata**
- `dataModelVersion` (default 3)

### 2.2 Merge Rules
- Non-my fields: `selectFirstNonEmpty(new, old)` — never overwrite non-empty with empty
- My fields: resolve by timestamp (newer wins)
- `detailsUpdateDate` updated on merge; `creationDate` preserved on first create

### 2.3 External Catalog Mapping
- Map external catalog payload to Show entity
- Match by external ID when available; fallback to title match (case-insensitive)
- Transient (not stored): cast, crew, seasons, images, videos, recommendations, similar

---

## 3. Application Structure

### 3.1 Navigation Layout
```
- Filters/Navigation Panel (sidebar)
  - All Shows
  - Tag filters (one per user tag)
  - Data filters (genre, decade, score range)
  - Media type toggle (All/Movies/TV)
- Main Content Area
  - Home (filtered collection)
  - Show Detail
  - Find/Discover (Search, Ask, Alchemy)
  - Person Detail
  - Settings
```

### 3.2 Page Specifications

**Collection Home**
- Grouped by status: Active (large tiles), Excited, Interested, Other (Wait/Quit/Done/unclassified Later)
- Media type toggle at top
- Show tiles: poster, title, status badges, user rating badge
- Empty state: prompt to Search/Ask

**Show Detail Page**
1. Header media carousel (backdrops/posters/logos/trailers)
2. Core facts row (year/length) + community score
3. My Status + Interest chips (toolbar)
4. My Rating bar
5. My Tags display + picker
6. Overview text + Scoop toggle
7. "Ask about this show" CTA
8. Genres + languages
9. Traditional recommendations strand
10. Explore Similar (Get Concepts → select → Explore Shows)
11. Streaming availability
12. Cast & Crew horizontal strands → Person Detail
13. Seasons (TV only)
14. Budget/Revenue (movies)

**Find/Discover Hub**
- Mode switcher: Search | Ask | Alchemy
- Search: text input → poster grid results
- Ask: chat UI with mentioned shows strip, 80 starter prompts
- Alchemy: show selection → Conceptualize → select concepts → Alchemize → results

**Person Detail Page**
- Image gallery, name, bio
- Analytics charts (ratings, genres, projects-by-year)
- Filmography grouped by year
- Credits → Show Detail

**Settings**
- Font size selector
- Search on launch toggle
- Username (synced)
- AI API key + model selection (synced)
- Catalog API key (synced)
- Export My Data button (generates .zip with JSON backup)

---

## 4. Feature Implementation Details

### 4.1 Collection Management

**Saving Triggers**
- Setting any status
- Choosing interest chip (Interested/Excited)
- Rating an unsaved show → defaults to Done
- Adding tag to unsaved show → defaults to Later + Interested

**Default Values on Save**
- No explicit status: `Later` + `Interested`
- Exception: rating defaults to `Done`

**Removal**
- User clears status (reselects active status, confirms)
- Clears all My Data
- Shows warning confirmation (suppressible after repeated removals)

### 4.2 Status System

**Core Statuses**
- `active`: currently watching
- `later`: saved for later (with interest level)
- `wait`: paused/waiting for right moment
- `done`: completed
- `quit`: abandoned

**Interest Levels** (only when `later`)
- `interested`: mild/normal priority
- `excited`: high priority/"next up"

**UI Display**
- "Interested" and "Excited" chips surface as primary options
- Selecting either sets `myStatus = later` + appropriate `myInterest`

### 4.3 Discovery Features

**Search**
- Live text search against external catalog
- Poster grid results
- In-collection items marked
- Opens Show Detail on selection

**Ask (AI Chat)**
- Conversational discovery
- 80 starter prompts (refreshable)
- Inline show mentions → horizontal "mentioned shows" strip
- Tapping mentioned show opens Detail
- Session context retained; older turns summarized after ~10 messages
- Structured output: `{ commentary: string, showList: "Title::externalId::mediaType;;..." }`
- "Ask about this show" variant: seeds conversation with show context

**Alchemy**
1. Select 2+ shows (library + catalog)
2. Tap "Conceptualize Shows" → AI extracts shared concepts (max 8 selectable)
3. Select 1-8 concept catalysts
4. Tap "ALCHEMIZE!" → 6 recommendations with reasons
5. Optional: "More Alchemy!" chains results as new inputs
6. Backtracking: changing shows clears concepts/results

**Explore Similar (Per-Show)**
1. From Show Detail: tap "Get Concepts"
2. Select 1+ concept chips
3. Tap "Explore Shows" → 5 AI recommendations
4. Recommendations map to real catalog items

### 4.4 AI Features

**AI Scoop**
- On-demand generation from Show Detail
- Cached for 4 hours freshness
- Only persists if show is in collection
- Progressive streaming if UI supports
- Structure: personal take → honest stack-up → "Scoop" centerpiece → fit/warnings → verdict

**AI Voice Personality**
- Fun, chatty TV/movie nerd friend
- 70% friend / 30% critic
- 60% hype / 40% measured
- Spoiler-safe by default
- Specific, vibe-first reasoning
- Short by default; lush when earned

**Concept Generation**
- 1-3 word evocative bullets
- No plot details or spoilers
- Specific over generic
- Covers: structure, tone, emotion, relationships, craft
- Ordered by strength/aha factor

**Concept-Based Recommendations**
- 5 recs (Explore Similar) / 6 recs (Alchemy)
- Reasons cite specific concepts
- Bias toward recent but allow classics

### 4.5 Data Persistence Rules

| Data | Persisted? | Freshness |
|------|------------|-----------|
| AI Scoop | Yes (if in collection) | 4 hours |
| Alchemy results | No | Session only |
| Ask chat history | No | Session only |
| Mentioned shows strip | No | Session only |

---

## 5. API Design

### 5.1 External Catalog Integration
- Configurable provider (e.g., TMDB-style API)
- API key stored in CloudSettings
- Endpoints needed:
  - Search by title
  - Get show details by ID
  - Get show credits (cast/crew)
  - Get person details
  - Get streaming providers

### 5.2 AI Integration
- Configurable AI provider and model
- API key stored in CloudSettings
- Surfaces: Scoop, Ask, Ask (with mentions), Concepts, Concept-Based Recs

### 5.3 Supabase Backend
- Auth (dev identity injection)
- CRUD for Shows
- CRUD for CloudSettings
- CRUD for AppMetadata
- All tables include `namespace_id` and `user_id` for isolation

---

## 6. Key User Journeys

1. **Build collection**: Find → Search → open show → set Interested/Excited/Active → tag/rate
2. **Rate-to-save**: Search → open show → adjust rating → auto-saved as Done
3. **Tag-to-save**: Search → open show → add tag → auto-saved as Later + Interested
4. **Maintain collection**: Home → browse by status → update My Data from Detail
5. **Tag-driven organization**: Add tags → sidebar gains tag filters → select filter
6. **Ask discovery**: Find → Ask → ask for vibe → select recommendation → save
7. **Explore Similar**: Detail → Get Concepts → select → Explore Shows → save
8. **Alchemy**: Find → Alchemy → pick favorites → Conceptualize → select catalysts → Alchemize → chain
9. **Talent deep-dive**: Detail → select person → Person Detail → select credit → new Detail
10. **Backup**: Settings → Export My Data → save .zip

---

## 7. Cross-Cutting Concerns

1. **User data wins**: My Data always displays over refreshed public data
2. **Discovery actionable**: All recommendations map to real catalog shows
3. **Spoiler-safe**: AI outputs spoiler-safe by default
4. **Implicit feels natural**: Auto-save and defaults do not surprise
5. **Export first-class**: Settings includes working Export My Data
6. **Namespace isolation**: All queries scoped by namespace_id
7. **User identity**: All user-owned records have user_id
8. **Backend as source of truth**: Correctness not dependent on local persistence

---

## 8. Phases

### Phase 1: Foundation
- Next.js project setup with App Router
- Supabase schema and migrations
- Environment variables and configuration
- Namespace and user identity infrastructure
- Basic auth injection for dev/test

### Phase 2: Core Collection
- Show entity and catalog mapping
- Collection Home page with status grouping
- Show Detail page (header, facts, overview, recommendations)
- Status/Interest system with save triggers
- Tags and ratings

### Phase 3: Discovery
- Search with external catalog integration
- Ask (AI chat) with mentioned shows
- Alchemy flow (select → conceptualize → select → alchemize)
- Explore Similar (get concepts → explore shows)

### Phase 4: AI Features
- AI Scoop generation and caching
- AI voice consistency across surfaces
- Concept extraction quality

### Phase 5: Supporting Features
- Person Detail page
- Settings (font size, search on launch)
- Export My Data

### Phase 6: Polish
- Filters (tag, genre, decade, score)
- Empty states
- Error handling
- Data sync (future-ready)

---

## 9. Open Questions (from PRD)

- Should "Next" become first-class UI status?
- Should users create named custom lists beyond tags?
- Should generating AI Scoop on unsaved show implicitly save it?
- Should clearing My Rating store "Unrated" vs nil?
- Add Import/Restore from export zip?
- Support saving/sharing Alchemy sessions?
- Add explicit myStatus filters in sidebar?

---

## 10. Out of Scope

- Detailed caching/offline strategy beyond freshness rules
- Low-level data schema migration details
- Vendor-specific API specs
- UI animation prescriptions
- Social/community features
- Real OAuth (dev identity injection acceptable for benchmark)
