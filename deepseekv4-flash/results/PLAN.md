# Implementation Plan: Personal TV + Movie Companion

## Tech Stack
- **Runtime:** Next.js (latest stable) with App Router (server actions + API routes)
- **Database:** Supabase (PostgreSQL) accessed via `@supabase/supabase-js`
- **AI:** OpenAI-compatible API (provider/model configurable in settings)
- **Catalog:** TMDB (or equivalent external catalog API)

## Phase 1: Project Scaffolding & Infrastructure

### 1.1 Initialize Next.js + Supabase
- `npx create-next-app@latest` with TypeScript, App Router, Tailwind
- Install `@supabase/supabase-js`, `@supabase/ssr`
- Create `.env.example` with keys: `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `NEXT_PUBLIC_CATALOG_API_KEY`, `AI_API_KEY`, `AI_MODEL`, `NAMESPACE_ID`
- `.gitignore` excludes `.env*` (except `.env.example`)

### 1.2 Database Schema (Supabase Migrations)
- `shows` table: all fields from `storage-schema.ts` (Show interface), plus `namespace_id TEXT` and `user_id TEXT`
- `cloud_settings` table: `id TEXT`, `user_id TEXT`, `namespace_id TEXT`, `user_name TEXT`, `version DOUBLE`, `catalog_api_key TEXT`, `ai_api_key TEXT`, `ai_model TEXT`
- `app_metadata` table: `namespace_id TEXT`, `data_model_version INT`
- Row-Level Security (RLS) policies scoped to `(namespace_id, user_id)`
- Composite primary keys on `(namespace_id, user_id, id)` for shows
- Migration files in `supabase/migrations/`

### 1.3 Identity & Namespace Isolation
- Server middleware reads `x-namespace-id` header (or falls back to `process.env.NAMESPACE_ID`)
- Server middleware reads `x-user-id` header in dev/benchmark mode
- All queries include `WHERE namespace_id = ... AND user_id = ...`
- `getServerClient()` and `getRouteHandlerClient()` factory functions inject both IDs

### 1.4 Dev Experience Scripts
- `npm run dev` — starts Next.js dev server
- `npm test` — runs tests
- `npm run test:reset` — deletes all data for current namespace via Supabase service role
- `package.json` scripts point to these

## Phase 2: Core Data Layer

### 2.1 Show Service
- CRUD operations: `getShow(id)`, `saveShow(show)`, `removeShow(id)`, `listShows(filters)`
- Merge logic: catalog merge uses `selectFirstNonEmpty`; user field merge uses timestamp comparison
- Default values on save: status=Later, interest=Interested (except rating-save → Done)
- `removeShow` clears all `my*` fields; confirmation required

### 2.2 Filter Engine
- `listShows` supports filters: mediaType, myStatus, myTags (array overlap), genre, decade, communityScore range
- Returns shows ordered by `myStatusUpdateDate` desc (recently updated first)

### 2.3 Sync & Migration
- `CloudSettings` service: read/write with timestamp-based conflict resolution
- `AppMetadata` tracks `dataModelVersion`; migration logic checks version on startup

### 2.4 Export Service
- `/api/export` server action: queries all user shows + settings, builds JSON, returns as `.zip`
- ISO-8601 date encoding

## Phase 3: Catalog Integration

### 3.1 External Catalog Client
- Abstract `CatalogProvider` interface (implemented for TMDB initially)
- Methods: `search(query)`, `getShowDetails(id, type)`, `getRecommendations(id)`, `getSimilar(id)`, `getCredits(id)`, `getSeasons(id)`, `getProviders(id, region)`, `getPerson(id)`, `getPersonCredits(id)`
- Rate limiting and error handling

### 3.2 Show-to-Catalog Mapping
- `decodeCatalogShow(raw)` → maps external payload to `Show` fields per `storage-schema.md`
- Title resolution: `title` for movies, `name` for TV; fallback to `.unknown`
- Genre ID → name mapping
- Image URL construction
- Provider data: store IDs only by region

### 3.3 Transient Fetches
- Cast, crew, seasons, videos, recommendations, similar, images — fetched on demand, not persisted
- Server actions for each: `getShowCredits`, `getShowSeasons`, etc.

## Phase 4: UI — Collection Home

### 4.1 Layout & Navigation
- Sidebar/nav panel: "All Shows", tag filters, data filters (genre, decade, community score)
- Media-type toggle: All / Movies / TV (persisted as URL param)
- Main content area: filtered library

### 4.2 Library Grid
- Shows grouped by status sections: Active (prominent), Excited, Interested, Other (Wait/Quit/Done/unclassified)
- Tiles: poster, title, in-collection badge, rating badge
- Empty states: "No shows yet — Search or Ask" / "No results found"

### 4.3 Filter Sidebar
- Tag filters: auto-generated from user's tag library; one per tag + "No tags"
- Data filters: genre (multi-select), decade range, community score range
- Active filter indication

## Phase 5: UI — Show Detail Page

### 5.1 Page Structure (server component + client islands)
1. Header carousel: backdrops/posters/logos + trailer embed
2. Core facts row: year, runtime/seasons, community score
3. My Tags chips (with tag picker)
4. Overview text + Scoop toggle (client streaming)
5. "Ask about this show" button
6. Genres + languages
7. Recommendations strand (catalog-based)
8. Explore Similar: Get Concepts → select → Explore Shows
9. Streaming providers
10. Cast & Crew horizontal strands → Person Detail
11. Seasons (TV only)
12. Budget/Revenue (movies)

### 5.2 My Relationship Controls (Toolbar)
- Status chips: Active, Interested, Excited, Wait, Done, Quit
  - Interested/Excited set status=Later + interest level
  - Reselecting active status shows removal confirmation
- Rating slider: unsaved + rate → auto-save as Done
- Tag picker: unsaved + add tag → auto-save as Later + Interested

### 5.3 AI Scoop
- Toggle button: "Give me the scoop!" / "Show the scoop"
- Progressive streaming via server-sent events or streaming server action
- 4-hour cache freshness; regenerate on demand
- Only persists if show is in collection

### 5.4 Explore Similar
- "Get Concepts" button → calls AI concept generation
- Concepts rendered as selectable chips (1–3 words, evocative)
- User selects 1+ concepts → "Explore Shows" → AI returns 5 recs with concept-grounded reasons

## Phase 6: UI — Find/Discover Hub

### 6.1 Mode Switcher
- Three tabs: Search | Ask | Alchemy

### 6.2 Search
- Text input → debounced catalog search → poster grid results
- In-collection items marked with badge
- Select → navigate to Show Detail
- Optional auto-open on launch (settings toggle)

### 6.3 Ask (AI Chat)
- Chat UI: message bubbles, user input, loading states
- Welcome view: 6 random starter prompts (from 80-prompt pool), refreshable
- AI responds with commentary + structured `showList` (pipe-delimited format)
- "Mentioned shows" horizontal strip below chat, parsed from AI response
- Tap mentioned show → open Detail (or Search fallback)
- Context retention: last ~10 turns; older turns summarized into 1–2 sentences
- Reset/clear session button

### 6.4 Alchemy
- Step 1: Search/select 2+ starting shows (library + global catalog)
- Step 2: "Conceptualize Shows" → AI generates shared concepts
- Step 3: Select 1–8 concept catalysts from chip list
- Step 4: "ALCHEMIZE!" → AI returns 6 recs with concept-grounded reasons
- Step 5: "More Alchemy!" chains using recs as new inputs
- Backtracking: changing shows clears concepts/results

## Phase 7: UI — Person Detail

### 7.1 Person Profile
- Image gallery, name, bio
- Filmography grouped by year
- Analytics charts: avg rating per year, top genres, projects-by-year bar chart
- Each credit tappable → opens Show Detail

## Phase 8: UI — Settings & Your Data

### 8.1 Settings Page
- Font size selector (XS–XXL)
- Search on launch toggle
- Username input
- AI provider API key (stored server-side, never committed)
- AI model selector
- Catalog API key

### 8.2 Your Data Section
- "Export My Data" button → triggers `/api/export`, downloads zip
- "Import / Restore" placeholder (future)

## Phase 9: AI Integration

### 9.1 AI Service Layer
- `AIService` class with methods: `ask(prompt, context)`, `generateScoop(show)`, `generateConcepts(shows[])`, `generateRecommendations(concepts[], count)`
- Configurable provider/base URL via settings/env
- Structured output parsing for `showList` format (`Title::id::type;;`)
- Retry logic for parse failures (once with stricter instructions, then fallback)

### 9.2 Prompt Management
- Base personality prompt: "fun, chatty TV/movie nerd friend" with voice pillars
- Surface-specific prompt templates: Ask, Scoop, Concepts, ConceptRecs
- 80 starter prompts for Ask welcome view (stored as static JSON)
- Conversation summarization prompt (preserves persona tone)

### 9.3 AI Recommendation to Real Show Resolution
- Parse `externalId` from structured output
- Look up in catalog via external catalog provider
- Fallback: title-based search if ID missing
- Non-resolvable: display as non-interactive text + Search handoff

## Phase 10: Testing Strategy

### 10.1 Unit Tests
- Data layer: merge logic, default values, removal semantics, filter engine
- Schema mapping: catalog payload → Show conversion
- AI response parsing: `showList` format, retry logic

### 10.2 Integration Tests
- API routes: CRUD shows, export, auth middleware
- Supabase queries with test namespace isolation

### 10.3 E2E Tests
- Key user journeys (build collection, rate-to-save, tag-to-save, Ask discovery, Alchemy, etc.)
- Runs against test namespace; `npm run test:reset` wipes namespace data

## Phase 11: Cross-Cutting Concerns

### 11.1 Data Continuity
- `AppMetadata.dataModelVersion` checked on app load
- Migration functions mapped to version increments
- Forward-only migrations; no destructive changes without version bump

### 11.2 Error Handling
- Global error boundary for UI crashes
- API route error wrapping (never leak internal state)
- AI fallback: retry → Search handoff for unresolvable recs

### 11.3 Security
- RLS policies scoped to `(namespace_id, user_id)`
- Server-only service role key (never exposed to client)
- API keys never committed; stored server-side only
- Dev auth header (`x-user-id`) gated behind `NODE_ENV !== 'production'`

## Implementation Order

1. **Phase 1** (scaffolding, DB, identity) — foundation, must be first
2. **Phase 2** (data layer, services) — enables all features
3. **Phase 3** (catalog integration) — enables content
4. **Phase 4** (Collection Home UI) — first visible feature
5. **Phase 5** (Show Detail) — core interaction hub
6. **Phase 6** (Find/Discover: Search, Ask, Alchemy) — discovery features
7. **Phase 7** (Person Detail) — talent exploration
8. **Phase 8** (Settings, Export) — user control
9. **Phase 9** (AI service layer) — powers Phases 5–6 AI surfaces; can overlap
10. **Phase 10** (Tests) — ongoing, but explicit test pass required before ship