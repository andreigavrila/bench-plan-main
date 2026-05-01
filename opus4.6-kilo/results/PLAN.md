# Implementation Plan

## Overview

This plan covers the full implementation of a personal TV/movie companion app for collecting, organizing, rating, and discovering entertainment. Users build a personal library with statuses, tags, ratings, and AI-powered discovery (Ask chat, Alchemy blending, Explore Similar concepts). The stack is Next.js + Supabase with namespace/user isolation for benchmark repeatability.

---

## Phase 0: Project Scaffolding & Infrastructure

### 0.1 Repository Setup
- Initialize Next.js project (latest stable, App Router)
- Configure TypeScript, ESLint, Prettier
- Create `.env.example` with all required variables:
  - `NEXT_PUBLIC_SUPABASE_URL` — Supabase project URL
  - `NEXT_PUBLIC_SUPABASE_ANON_KEY` — Supabase anon/public key
  - `SUPABASE_SERVICE_ROLE_KEY` — server-only elevated key
  - `TMDB_API_KEY` — external catalog API key (server-only)
  - `AI_API_KEY` — AI provider API key (server-only default; user can override in settings)
  - `AI_MODEL` — default AI model identifier
  - `DEFAULT_NAMESPACE_ID` — build/run namespace identifier
  - `DEFAULT_USER_ID` — default dev user identity
- `.gitignore` excludes `.env*` (except `.env.example`), `node_modules`, `.next`

### 0.2 Supabase Schema & Migrations
- Create a `supabase/migrations/` directory with numbered SQL migration files
- Migration 001 — Core tables:

```sql
-- Namespaces table (build isolation)
CREATE TABLE namespaces (
  id TEXT PRIMARY KEY,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Shows table (the core entity)
CREATE TABLE shows (
  id TEXT NOT NULL,
  namespace_id TEXT NOT NULL REFERENCES namespaces(id),
  user_id TEXT NOT NULL,
  title TEXT NOT NULL,
  show_type TEXT NOT NULL CHECK (show_type IN ('movie', 'tv', 'person', 'unknown')),
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
  vote_average DOUBLE PRECISION,
  vote_count INTEGER,
  popularity DOUBLE PRECISION,
  last_air_date TIMESTAMPTZ,
  first_air_date TIMESTAMPTZ,
  release_date TIMESTAMPTZ,
  runtime INTEGER,
  budget INTEGER,
  revenue INTEGER,
  series_status TEXT,
  number_of_episodes INTEGER,
  number_of_seasons INTEGER,
  episode_run_time INTEGER[] DEFAULT '{}',
  my_tags TEXT[] DEFAULT '{}',
  my_tags_update_date TIMESTAMPTZ,
  my_score DOUBLE PRECISION,
  my_score_update_date TIMESTAMPTZ,
  my_status TEXT CHECK (my_status IN ('active', 'next', 'later', 'done', 'quit', 'wait')),
  my_status_update_date TIMESTAMPTZ,
  my_interest TEXT CHECK (my_interest IN ('excited', 'interested')),
  my_interest_update_date TIMESTAMPTZ,
  ai_scoop TEXT,
  ai_scoop_update_date TIMESTAMPTZ,
  details_update_date TIMESTAMPTZ,
  creation_date TIMESTAMPTZ DEFAULT now(),
  is_test BOOLEAN DEFAULT false,
  provider_data JSONB,
  PRIMARY KEY (id, namespace_id, user_id)
);

-- Row Level Security: scope all queries to namespace + user
ALTER TABLE shows ENABLE ROW LEVEL SECURITY;

-- Cloud settings (per namespace + user)
CREATE TABLE cloud_settings (
  id TEXT DEFAULT 'globalSettings',
  namespace_id TEXT NOT NULL REFERENCES namespaces(id),
  user_id TEXT NOT NULL,
  user_name TEXT NOT NULL,
  version DOUBLE PRECISION DEFAULT 0,
  catalog_api_key TEXT,
  ai_api_key TEXT,
  ai_model TEXT DEFAULT 'gpt-4o',
  PRIMARY KEY (id, namespace_id, user_id)
);

-- App metadata (per namespace)
CREATE TABLE app_metadata (
  namespace_id TEXT NOT NULL REFERENCES namespaces(id),
  data_model_version INTEGER DEFAULT 3,
  PRIMARY KEY (namespace_id)
);
```

- Migration 002 — RLS policies:
  - Policies on `shows` that filter by `namespace_id` and `user_id` matching request context
  - Policies on `cloud_settings` similarly scoped
- Migration 003 — Indexes:
  - `shows(namespace_id, user_id, my_status)` for collection home queries
  - `shows(namespace_id, user_id, my_tags)` using GIN for tag filtering
  - `shows(namespace_id, user_id, genres)` using GIN for genre filtering

### 0.3 Identity & Namespace Injection
- Create a middleware (`src/middleware.ts`) that:
  - In development/test mode: reads `X-Namespace-Id` and `X-User-Id` headers (or falls back to `DEFAULT_NAMESPACE_ID` / `DEFAULT_USER_ID` env vars)
  - Injects these into a request context accessible by all API routes and server components
  - In production mode: disables header-based injection; requires real auth
- Create a dev-only "Login as user" selector component in the UI header (gated behind `NODE_ENV === 'development'`)
- Ensure the namespace row exists in `namespaces` table on first request (upsert)
- Document the identity mechanism clearly in README

### 0.4 Supabase Client Setup
- `src/lib/supabase/server.ts` — server-side Supabase client using service role key, scoped to current namespace/user via RLS or query filters
- `src/lib/supabase/client.ts` — browser client using anon key
- All database queries include `namespace_id` and `user_id` in WHERE clauses (defense-in-depth alongside RLS)

### 0.5 NPM Scripts
- `npm run dev` — starts Next.js dev server
- `npm test` — runs test suite (Jest + React Testing Library)
- `npm run test:reset` — script that deletes all data for a given namespace (reads `DEFAULT_NAMESPACE_ID` from env)
- `npm run db:migrate` — applies Supabase migrations
- `npm run db:seed` — optional seed data for development

---

## Phase 1: Data Layer & API Routes

### 1.1 TypeScript Types & Validation
- `src/types/show.ts` — TypeScript interfaces mirroring the schema: `Show`, `ShowType`, `MyStatusType`, `MyInterestType`, `ProviderData`, `ProviderTypeIdLists`
- `src/types/settings.ts` — `CloudSettings`, `AppMetadata`, `LocalSettings`, `FilterConfiguration`, `UIState`
- Use Zod schemas for runtime validation of API inputs/outputs

### 1.2 Show Repository (Server-Side Data Access)
- `src/lib/repositories/show-repository.ts`
- Functions:
  - `getCollectionShows(namespaceId, userId, filter?)` — retrieve user's library with optional filtering by status, tags, genre, decade, community score, media type
  - `getShowById(namespaceId, userId, showId)` — single show with user overlay
  - `upsertShow(namespaceId, userId, show)` — create or merge a show using merge rules:
    - Non-my fields: `selectFirstNonEmpty(newValue, oldValue)` — never overwrite non-empty with empty
    - My fields: resolve by timestamp (newer wins)
    - Set `details_update_date` to now on merge
    - Set `creation_date` only on first creation
  - `updateMyData(namespaceId, userId, showId, fields)` — partial update of my_status, my_interest, my_tags, my_score, ai_scoop with corresponding update timestamps
  - `removeShow(namespaceId, userId, showId)` — delete from collection (clears all My Data)
  - `getShowsByTag(namespaceId, userId, tag)` — shows matching a specific tag
  - `getUserTags(namespaceId, userId)` — distinct tag list from all shows
  - `resetNamespaceData(namespaceId)` — destructive test reset scoped to namespace

### 1.3 Settings Repository
- `src/lib/repositories/settings-repository.ts`
- Functions:
  - `getCloudSettings(namespaceId, userId)` / `upsertCloudSettings(...)`
  - `getAppMetadata(namespaceId)` / `upsertAppMetadata(...)`
- Cloud settings conflict resolution: compare `version` (epoch seconds), newer wins

### 1.4 External Catalog Service (TMDB Integration)
- `src/lib/services/catalog-service.ts`
- Server-only (TMDB API key never exposed to client)
- Functions:
  - `searchShows(query, mediaType?)` — search by title/keywords; returns mapped `Show[]`
  - `getShowDetails(externalId, mediaType)` — full detail including credits, seasons, videos, recommendations, similar, images, providers
  - `getPersonDetails(personId)` — person bio, image gallery, credits
  - `getTrending(mediaType?, timeWindow?)` — trending shows (for empty states)
  - `getProviders(externalId, mediaType)` — streaming availability by region
- Internal mapper: `mapCatalogResponseToShow(apiResponse)` implementing field mapping rules:
  - Catalog id -> Show id
  - Title inference (movie title vs TV name)
  - ShowType inference from media_type field
  - Genre ID-to-name mapping
  - Date parsing with multiple format support
  - Image path to full URL construction
  - Best logo selection (prefer English, highest rated)
  - Provider data extraction by country

### 1.5 AI Service Layer
- `src/lib/services/ai-service.ts`
- Server-only (AI API key never exposed to client)
- Configurable provider/model (reads from cloud_settings, falls back to env vars)
- Functions:
  - `generateScoop(show, userLibraryContext?)` — returns structured Scoop text (~150-350 words)
  - `generateAskResponse(messages, userLibrary, mentionedShows?)` — conversational response + structured showList
  - `generateAskWithShowContext(show, messages, userLibrary)` — "Ask about this show" variant seeded with show context
  - `generateConcepts(shows[])` — returns bullet list of 1-3 word concepts (8 concepts for single-show, larger pool for multi-show)
  - `generateConceptRecommendations(concepts[], inputShows[], userLibrary, count)` — returns recommendations with reasons tied to concepts (5 for Explore Similar, 6 for Alchemy)
  - `summarizeConversation(messages)` — condense older turns into 1-2 sentences preserving persona tone
- Prompt construction:
  - Each function builds a system prompt + user message following the AI personality spec
  - Shared persona: fun, chatty TV/movie nerd friend — warm, opinionated, spoiler-safe, vibe-first
  - Stay within TV/movies domain
  - Tone sliders: 70% friend / 30% critic, 60% hype / 40% measured
- Structured output parsing:
  - Ask mentions: parse `Title::externalId::mediaType;;` format from showList field
  - Concepts: parse bullet list
  - Recommendations: parse structured array with title, externalId, mediaType, reason
  - Fallback: on parse failure, retry once with stricter formatting; then fall back to unstructured + search handoff
- Show resolution pipeline:
  - `src/lib/services/show-resolver.ts`
  - Takes AI output (title + externalId + mediaType) and resolves against TMDB
  - Lookup by externalId first; accept if title matches case-insensitively
  - If not found, fall back to search; accept first result with matching title
  - If still not found, mark as non-interactive (title-only display)

### 1.6 API Routes (Next.js Route Handlers)
All routes under `src/app/api/` — all inject namespace_id and user_id from middleware context.

**Collection routes:**
- `GET /api/collection` — list user's collection (query params: filter, mediaType, status)
- `GET /api/collection/tags` — distinct tag list
- `GET /api/collection/[showId]` — single show with user overlay
- `PUT /api/collection/[showId]` — upsert show (save/update)
- `PATCH /api/collection/[showId]/my-data` — partial update of My Data fields
- `DELETE /api/collection/[showId]` — remove from collection

**Catalog routes:**
- `GET /api/catalog/search` — search external catalog (query: q, mediaType)
- `GET /api/catalog/[showId]` — full show details from catalog (with user overlay if saved)
- `GET /api/catalog/[showId]/credits` — cast & crew
- `GET /api/catalog/[showId]/seasons` — TV seasons/episodes
- `GET /api/catalog/[showId]/providers` — streaming availability
- `GET /api/catalog/[showId]/recommendations` — traditional similar/recommended
- `GET /api/catalog/person/[personId]` — person details + credits
- `GET /api/catalog/trending` — trending shows

**AI routes:**
- `POST /api/ai/scoop` — generate AI Scoop for a show (body: showId, mediaType)
- `POST /api/ai/ask` — Ask chat turn (body: messages[], handoffShow?)
- `POST /api/ai/concepts` — generate concepts (body: showIds[])
- `POST /api/ai/recommendations` — concept-based recs (body: concepts[], showIds[], count)

**Settings routes:**
- `GET /api/settings` — get cloud settings
- `PUT /api/settings` — update cloud settings (with version conflict resolution)

**Admin/test routes:**
- `POST /api/admin/reset` — destructive namespace reset (dev/test only)

**Export route:**
- `GET /api/export` — generate and download ZIP of user data (JSON backup, ISO-8601 dates)

---

## Phase 2: Core UI Shell & Navigation

### 2.1 Layout & Routing Structure
- `src/app/layout.tsx` — root layout with providers (Supabase, theme, settings context)
- `src/app/(main)/layout.tsx` — main app layout with:
  - Sidebar/filter panel (left)
  - Main content area (right)
  - Top navigation bar with: app title, Find/Discover button, Settings button
  - Dev-only user selector (if NODE_ENV=development)
- Route structure:
  - `/(main)/` — Collection Home
  - `/(main)/show/[id]` — Show Detail
  - `/(main)/person/[id]` — Person Detail
  - `/(main)/find/` — Find/Discover hub (with sub-routes or tabs for Search, Ask, Alchemy)
  - `/(main)/settings` — Settings page

### 2.2 Sidebar / Filter Panel
- `src/components/sidebar/FilterPanel.tsx`
- Sections:
  - "All Shows" (default quick filter)
  - Tag filters: dynamically generated from user's tag library; includes "No tags" if tagless shows exist
  - Data filters: Genre, Decade, Community Score ranges
- Media-type toggle at top of content area: All / Movies / TV (applies on top of any filter)
- Persist last selected filter to local storage (`lastSelectedFilter` key)
- Fetch tag list via `GET /api/collection/tags`

### 2.3 Shared Components
- `src/components/show/ShowTile.tsx` — poster tile with title, in-collection badge, user rating badge
- `src/components/show/ShowGrid.tsx` — responsive grid of ShowTiles
- `src/components/show/ShowRow.tsx` — horizontal scrollable row of ShowTiles (for recommendations, mentioned shows)
- `src/components/show/StatusChips.tsx` — status selection chips (Active, Interested, Excited, Wait, Done, Quit) with correct mapping logic:
  - Interested -> status=Later, interest=Interested
  - Excited -> status=Later, interest=Excited
  - Reselect active status -> removal confirmation
- `src/components/show/RatingBar.tsx` — rating slider/input component
- `src/components/show/TagPicker.tsx` — tag display + add/remove interface
- `src/components/ui/` — base UI primitives (Button, Modal, Chip, Input, Spinner, etc.)

### 2.4 Client-Side State Management
- Use React Context + hooks for:
  - `SettingsContext` — cloud settings + local settings
  - `CollectionContext` — lightweight collection metadata (for badge display on tiles)
- Server state via React Query (TanStack Query) or SWR for:
  - Collection data with cache invalidation on mutations
  - Catalog search results
  - Show details
- Local storage for: `autoSearch`, `fontSize`, `hideStatusRemovalConfirmation`, `statusRemovalCountKey`, `lastSelectedFilter`

---

## Phase 3: Collection Home

### 3.1 Collection Home Page
- `src/app/(main)/page.tsx`
- Fetches user's collection via `GET /api/collection` with active filter + media type
- Groups shows into status sections rendered in order:
  1. **Active** — prominent/larger tiles
  2. **Excited** — Later + Excited interest
  3. **Interested** — Later + Interested interest
  4. **Other** (collapsed by default): Wait, Quit, Done, and Later items without interest
- Each section has a header label and horizontal/grid show tiles
- Media-type toggle: All / Movies / TV (re-fetches with filter param)

### 3.2 Saving Business Logic (Client-Side Hooks)
- `src/hooks/useShowActions.ts` — encapsulates all save/update/remove logic:
  - `saveWithStatus(show, status, interest?)` — sets status (and interest if Later)
  - `saveWithRating(show, score)` — auto-saves as Done if unsaved
  - `saveWithTag(show, tag)` — auto-saves as Later + Interested if unsaved
  - `removeShow(show)` — triggers confirmation modal, then DELETE
  - Default values: if saving without explicit status -> Later + Interested; if first save via rating -> Done
- `src/hooks/useRemovalConfirmation.ts` — manages the confirmation dialog:
  - Shows warning on removal
  - Tracks `statusRemovalCountKey` in local storage
  - Option to suppress future confirmations (`hideStatusRemovalConfirmation`)

### 3.3 Empty States
- No shows in collection: centered message with CTAs to Search or Ask
- Filter yields no results: "No results found" message

---

## Phase 4: Find/Discover Hub

### 4.1 Find Layout
- `src/app/(main)/find/page.tsx`
- Mode switcher component (tabs or segmented control): Search | Ask | Alchemy
- Each mode renders its own content panel below the switcher
- Default to Search mode; if `autoSearch` setting is true, auto-focus search input on app launch

### 4.2 Search Mode
- `src/app/(main)/find/search/` (or inline component)
- `src/components/find/SearchPanel.tsx`
- Text input for title/keyword search
- On submit: `GET /api/catalog/search?q=...&mediaType=...`
- Results in a poster grid (`ShowGrid`)
- In-collection items display collection badge
- Clicking a tile navigates to Show Detail `/(main)/show/[id]`

### 4.3 Ask Mode (AI Chat)
- `src/components/find/AskPanel.tsx`
- Chat UI: scrollable message list + input field
- Messages stored in component state (session-only, not persisted)
- On send: `POST /api/ai/ask` with message history
- Response parsed into:
  - `commentary` — rendered as assistant message bubble
  - `showList` — parsed into ShowRow ("Mentioned Shows" horizontal strip)
- Mentioned show tiles: tapping opens Show Detail; if resolution failed, hand off to Search
- Welcome state: 6 random starter prompt chips (from a curated set of ~80 prompts); refresh button
- Conversation summarization: after ~10 messages, older turns auto-summarized via `POST /api/ai/ask` with summarization flag
- Session reset: clear button resets chat state

### 4.4 Alchemy Mode
- `src/components/find/AlchemyPanel.tsx`
- Multi-step wizard UI with clear step indicators:

**Step 1: Select Starting Shows (2+)**
- Search input to find shows from catalog + collection
- Selected shows displayed as removable chips/cards
- Minimum 2 shows required to proceed

**Step 2: Conceptualize**
- Button: "Conceptualize Shows"
- Calls `POST /api/ai/concepts` with selected show IDs
- Displays returned concepts as selectable chips
- User selects 1-8 concepts

**Step 3: Alchemize**
- Button: "ALCHEMIZE!"
- Calls `POST /api/ai/recommendations` with concepts + show IDs, count=6
- Displays 6 recommendation cards with poster + title + reason text
- Each card is tappable -> Show Detail

**Step 4: Chain (optional)**
- Button: "More Alchemy!"
- Adds result shows to a new input set -> returns to Step 1 with pre-populated shows

**Backtracking rules:**
- Changing selected shows clears concepts and results
- Changing selected concepts clears results

---

## Phase 5: Show Detail Page

### 5.1 Show Detail Page Structure
- `src/app/(main)/show/[id]/page.tsx`
- Server component that fetches show details via `GET /api/catalog/[id]` (merges with user overlay)
- Section order (per detail_page_experience.md narrative hierarchy):

**1. Header Media Carousel**
- `src/components/detail/HeaderMedia.tsx`
- Backdrops, posters, logos; inline trailer playback when available
- Graceful fallback: poster/logo layout if no backdrops/trailers

**2. Core Facts + Community Score**
- `src/components/detail/CoreFacts.tsx`
- Year, runtime (movies) or seasons/episodes (TV), genres
- Community score bar (vote_average visualization)

**3. My Relationship Controls (Toolbar)**
- `src/components/detail/DetailToolbar.tsx`
- Status/Interest chips: Active, Interested, Excited, Wait, Done, Quit
  - Interested maps to status=Later, interest=Interested
  - Excited maps to status=Later, interest=Excited
  - Reselecting active status triggers removal confirmation
- My Rating bar:
  - Rating an unsaved show auto-saves as Done
- Tags section:
  - Adding a tag to unsaved show auto-saves as Later + Interested
  - Tag picker with existing tags + new tag input

**4. Overview + AI Scoop**
- `src/components/detail/OverviewScoop.tsx`
- Overview text displayed directly
- Scoop toggle button with dynamic copy:
  - No scoop generated: "Give me the scoop!"
  - Cached scoop (< 4 hours): "Show the scoop"
  - When open: section title "The Scoop"
- On generate: `POST /api/ai/scoop` with streaming response
- Show "Generating..." state during stream
- Freshness: regenerate after 4 hours on demand
- Persistence: only persist to DB if show is in collection

**5. Ask About This Show**
- `src/components/detail/AskAboutShow.tsx`
- CTA button "Ask about [show title]..."
- On tap: navigates to Find -> Ask mode with show context seeded into first message

**6. Genres + Languages**
- `src/components/detail/GenresLanguages.tsx`

**7. Traditional Recommendations Strand**
- `src/components/detail/RecommendationsStrand.tsx`
- Horizontal ShowRow of similar/recommended shows from catalog API
- Low-effort discovery (no AI)

**8. Explore Similar (Concept Discovery)**
- `src/components/detail/ExploreSimilar.tsx`
- Sub-flow within detail page:
  1. "Get Concepts" button -> `POST /api/ai/concepts` with this show
  2. Concepts displayed as selectable chips (1-8 selection cap)
  3. "Explore Shows" button -> `POST /api/ai/recommendations` with concepts, count=5
  4. Results: ShowRow with reason text
- Copy hint: "pick the ingredients you want more of"
- Empty state: only "Get Concepts" CTA visible

**9. Streaming Availability**
- `src/components/detail/StreamingProviders.tsx`
- "Stream It" section showing provider logos/links by category (flatrate, rent, buy)
- Data from provider_data field (provider IDs mapped to display info)

**10. Cast & Crew**
- `src/components/detail/CastCrew.tsx`
- Horizontal scrollable strands for cast and crew
- Each person card: photo + name + role
- Tapping navigates to Person Detail `/(main)/person/[id]`

**11. Seasons (TV only)**
- `src/components/detail/Seasons.tsx`
- Season list with episode counts; conditionally rendered for show_type=tv

**12. Budget vs Revenue (Movies)**
- `src/components/detail/BudgetRevenue.tsx`
- Conditionally rendered when budget/revenue data available

---

## Phase 6: Person Detail Page

### 6.1 Person Detail
- `src/app/(main)/person/[id]/page.tsx`
- Fetches via `GET /api/catalog/person/[id]`
- Sections:
  - **Image Gallery** — profile images
  - **Name + Bio** — biography text
  - **Analytics Charts** — lightweight visualizations:
    - Average project ratings (bar or line chart)
    - Top genres (bar chart or pie)
    - Projects by year (timeline chart)
  - **Filmography** — credits grouped by year, most recent first
    - Each credit is a tappable ShowTile -> navigates to Show Detail
- Use a lightweight chart library (e.g., Recharts or Chart.js)

---

## Phase 7: Settings & Data Management

### 7.1 Settings Page
- `src/app/(main)/settings/page.tsx`
- Sections:

**App Settings**
- Font size selector: XS, S, M, L, XL, XXL (stored in local storage, applied via CSS custom property)
- Search on launch toggle (stored in local storage as `autoSearch`)

**User**
- Username input (synced via cloud_settings)
- Generated randomly on first launch

**AI Configuration**
- AI provider API key input (stored in cloud_settings; server-side usage only; never committed)
- AI model selection dropdown (stored in cloud_settings)

**Integrations**
- Content catalog provider API key input (stored in cloud_settings)

**Your Data**
- "Export My Data" button:
  - Calls `GET /api/export`
  - Server generates a `.zip` containing:
    - `shows.json` — all saved shows with My Data, dates in ISO-8601
    - `settings.json` — cloud settings (excluding sensitive keys)
    - `metadata.json` — export metadata (export date, namespace, user_id, data model version)
  - Downloads via browser

**Dev Identity (dev mode only)**
- Namespace ID display/input
- User ID display/input

---

## Phase 8: AI Prompt Engineering

### 8.1 Shared System Prompt Base
- Define a reusable base prompt segment that establishes the persona:
  - Fun, chatty TV/movie nerd friend
  - Warm, opinionated, spoiler-safe, vibe-first
  - Conversational contractions, vivid adjectives, quick contrasts
  - Stay within TV/movies; redirect if asked to leave
  - Tone: 70% friend / 30% critic, 60% hype / 40% measured
- Store prompts in `src/lib/ai/prompts/` as template strings with interpolation points

### 8.2 Scoop Prompt
- System: base persona + Scoop-specific instructions
- Structure: personal take, honest stack-up, "The Scoop" centerpiece, fit/warnings, "Worth it?" verdict
- Length target: 150-350 words
- Input context: show metadata, user library summary (if available)
- Output: single text string

### 8.3 Ask Prompt
- System: base persona + Ask-specific instructions
  - Respond like friend in dialogue, not essay
  - Pick favorites confidently
  - Use simple formatting + bulleted lists for multi-recs
- User message includes: conversation history, user library summary
- Output: structured JSON with `commentary` (text) and `showList` (Title::externalId::mediaType;; format)
- Conversation summarization prompt: condense older turns preserving persona tone

### 8.4 Ask About Show Prompt
- Variant of Ask with show context seeded
- System prompt includes current show details as context
- Chameleon behavior: mirror the emotion of the show being discussed

### 8.5 Concepts Prompt
- System: base persona + concept extraction rules
- Instructions: 1-3 word evocative bullets, no plot, no generic concepts
- Single-show: extract 8 concepts covering different axes (structure/vibe/emotion/craft)
- Multi-show (Alchemy): extract shared commonality concepts, larger pool (~12-15)
- Output: bullet list only

### 8.6 Concept Recommendations Prompt
- System: base persona + recommendation rules
- Input: selected concepts, input shows, user library
- Instructions: recommend real shows with reasons citing specific concepts; recent bias but allow classics
- Explore Similar: 5 recommendations
- Alchemy: 6 recommendations
- Output: structured list with title, externalId, mediaType, reason per recommendation

### 8.7 Starter Prompts
- `src/lib/ai/starter-prompts.ts`
- Array of ~80 curated conversation starters for the Ask welcome state
- Categorized by mood/intent (e.g., "looking for comfort," "want something dark," "hidden gems")
- Random selection of 6 displayed on welcome; refresh picks new 6

---

## Phase 9: Cross-Cutting Concerns

### 9.1 Show Tile Indicators
- In-collection badge: small icon/dot on tile when `my_status` exists
- User rating badge: small score display when `my_score` exists
- Both rendered by `ShowTile` component using collection context

### 9.2 User Data Overlay (User's Version Takes Precedence)
- Everywhere a show appears (search results, recommendations, AI outputs, etc.), check if user has a saved version
- If saved: merge user overlay (status, interest, tags, rating, scoop) onto display
- Implemented via a shared hook: `src/hooks/useShowWithOverlay.ts`
  - Checks collection cache for matching show ID
  - Returns merged show object with user fields taking precedence

### 9.3 Auto-Save Rules (Centralized)
- All auto-save triggers handled in `useShowActions` hook:
  - Setting any status -> save with that status
  - Choosing Interested/Excited chip -> save as Later + interest level
  - Rating unsaved show -> save as Done
  - Adding tag to unsaved show -> save as Later + Interested
- Default save values: status=Later, interest=Interested (when not explicitly set)
- Exception: first save via rating defaults to Done

### 9.4 Data Merge on Re-Add / Catalog Refresh
- When a catalog show is fetched and a saved version exists:
  - Non-my fields: `selectFirstNonEmpty(new, old)` — preserve existing non-empty values
  - My fields: keep the one with the most recent update timestamp
  - Set `details_update_date` to now
  - Keep original `creation_date`
- Implemented in the show repository's upsert function

### 9.5 AI Data Lifecycle
- AI Scoop: persisted in DB only if show is in collection; 4-hour freshness cache
- Alchemy results/reasons: session-only (component state); cleared on leave
- Ask chat history: session-only (component state); cleared on reset/leave
- Mentioned shows strip: derived from current chat context (component state)

### 9.6 Spoiler Safety
- All AI prompts include "spoiler-safe by default" instruction
- No override mechanism unless user explicitly requests in chat

### 9.7 Streaming / Progressive Loading for AI
- AI Scoop uses streaming response (Server-Sent Events or fetch streaming)
- Show "Generating..." indicator during stream
- Ask chat also streams assistant responses for perceived responsiveness

### 9.8 Error Handling & Fallbacks
- AI structured output parsing failures: retry once with stricter formatting, then fall back to unstructured text + search handoff
- Catalog API failures: show error state with retry option
- Network failures: standard error handling (no offline mode required)
- Unresolvable AI recommendations: display as non-interactive title text or offer search link

---

## Phase 10: Testing Strategy

### 10.1 Unit Tests
- Repository functions: test CRUD operations, merge logic, timestamp resolution
- Catalog mapper: test field mapping, edge cases (missing fields, unknown types)
- AI service: test prompt construction, output parsing, fallback logic (mock AI responses)
- Show actions hook: test auto-save rules, default values, removal logic
- Filter logic: test tag/genre/decade/score/media-type filtering

### 10.2 Integration Tests
- API routes: test full request/response cycle with test Supabase instance
- Namespace isolation: verify two namespaces cannot read/write each other's data
- User isolation: verify two users within a namespace have independent collections
- Destructive reset: verify namespace reset clears only targeted namespace data
- Export: verify ZIP contents match expected schema

### 10.3 E2E Tests (Optional / Stretch)
- Key user journeys with Playwright or Cypress:
  - Search -> save show -> verify in collection
  - Rate unsaved show -> verify auto-saved as Done
  - Tag unsaved show -> verify auto-saved as Later + Interested
  - Remove show -> verify confirmation -> verify cleared
  - Ask flow -> verify mentioned shows render
  - Alchemy flow -> 3 shows -> concepts -> recommendations

### 10.4 Test Data Management
- `npm run test:reset` script:
  - Reads `DEFAULT_NAMESPACE_ID` from env
  - Calls `DELETE FROM shows WHERE namespace_id = $1`
  - Calls `DELETE FROM cloud_settings WHERE namespace_id = $1`
  - Calls `DELETE FROM app_metadata WHERE namespace_id = $1`
- All test data created with `is_test = true` for additional safety
- Tests use a dedicated test namespace (e.g., `test-namespace-{timestamp}`)

---

## Phase 11: Data Model Versioning & Migration

### 11.1 Migration Strategy
- `app_metadata.data_model_version` tracks current schema version (default 3 per spec)
- On app startup, server checks current version vs expected version
- If version mismatch: run forward migrations in sequence
- Migration scripts in `supabase/migrations/` with sequential numbering
- User data preservation: migrations MUST be non-destructive; existing shows, ratings, tags, statuses, interest levels, AI Scoop all carried forward
- No user intervention required on upgrade

---

## Phase 12: Polish & Production Readiness

### 12.1 Responsive Design
- Mobile-first responsive layout
- Sidebar collapses to hamburger menu on small screens
- Detail page sections stack vertically on mobile
- Touch-friendly chip/button sizes

### 12.2 Font Size System
- CSS custom property `--app-font-size` driven by settings
- XS through XXL mapped to specific rem values
- Applied globally via root layout

### 12.3 Loading States
- Skeleton loaders for collection home, search results, show detail
- Spinner for AI operations (Scoop, Ask, Concepts, Alchemy)
- Optimistic updates where appropriate (status changes, rating)

### 12.4 Accessibility
- Semantic HTML elements
- ARIA labels on interactive elements
- Keyboard navigation for core flows
- Color contrast compliance

---

## Implementation Order & Dependencies

The phases have the following dependency chain:

```
Phase 0 (Scaffolding)
  |
Phase 1 (Data Layer & API)
  |
  +-- Phase 2 (UI Shell) -- depends on API routes existing
  |     |
  |     +-- Phase 3 (Collection Home) -- depends on UI shell + collection API
  |     |
  |     +-- Phase 4 (Find/Discover) -- depends on UI shell + catalog API + AI API
  |     |
  |     +-- Phase 5 (Show Detail) -- depends on UI shell + catalog API + AI API + collection API
  |     |
  |     +-- Phase 6 (Person Detail) -- depends on UI shell + catalog API
  |     |
  |     +-- Phase 7 (Settings) -- depends on UI shell + settings API
  |
  +-- Phase 8 (AI Prompts) -- parallel with UI, needed before AI features go live
  |
Phase 9 (Cross-Cutting) -- woven throughout Phases 3-8
  |
Phase 10 (Testing) -- written alongside each phase
  |
Phase 11 (Migrations) -- after core schema is stable
  |
Phase 12 (Polish) -- final pass
```

### Recommended Build Sequence

1. **Phase 0** — scaffolding, env, Supabase schema, identity injection
2. **Phase 1.1-1.3** — types, show repository, settings repository
3. **Phase 1.4** — catalog service (TMDB integration)
4. **Phase 2** — UI shell, layout, navigation, shared components
5. **Phase 3** — Collection Home (first visible feature)
6. **Phase 4.2** — Search mode (enables finding shows)
7. **Phase 5** — Show Detail page (the core experience hub)
8. **Phase 1.5** — AI service layer
9. **Phase 8** — AI prompt engineering
10. **Phase 4.3** — Ask mode (AI chat)
11. **Phase 4.4** — Alchemy mode
12. **Phase 5 (Explore Similar section)** — concept discovery on detail page
13. **Phase 6** — Person Detail
14. **Phase 7** — Settings & Export
15. **Phase 9** — cross-cutting polish (overlays, indicators, auto-save audit)
16. **Phase 10** — testing suite
17. **Phase 11** — migration versioning
18. **Phase 12** — responsive design, loading states, accessibility

---

## File Structure Summary

```
/
├── .env.example
├── .gitignore
├── package.json
├── next.config.js
├── tsconfig.json
├── supabase/
│   └── migrations/
│       ├── 001_core_tables.sql
│       ├── 002_rls_policies.sql
│       └── 003_indexes.sql
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── api/
│   │   │   ├── collection/
│   │   │   │   ├── route.ts
│   │   │   │   ├── tags/route.ts
│   │   │   │   └── [showId]/
│   │   │   │       ├── route.ts
│   │   │   │       └── my-data/route.ts
│   │   │   ├── catalog/
│   │   │   │   ├── search/route.ts
│   │   │   │   ├── trending/route.ts
│   │   │   │   ├── person/[personId]/route.ts
│   │   │   │   └── [showId]/
│   │   │   │       ├── route.ts
│   │   │   │       ├── credits/route.ts
│   │   │   │       ├── seasons/route.ts
│   │   │   │       ├── providers/route.ts
│   │   │   │       └── recommendations/route.ts
│   │   │   ├── ai/
│   │   │   │   ├── scoop/route.ts
│   │   │   │   ├── ask/route.ts
│   │   │   │   ├── concepts/route.ts
│   │   │   │   └── recommendations/route.ts
│   │   │   ├── settings/route.ts
│   │   │   ├── export/route.ts
│   │   │   └── admin/reset/route.ts
│   │   └── (main)/
│   │       ├── layout.tsx
│   │       ├── page.tsx                    # Collection Home
│   │       ├── find/
│   │       │   └── page.tsx                # Find/Discover hub
│   │       ├── show/
│   │       │   └── [id]/page.tsx           # Show Detail
│   │       ├── person/
│   │       │   └── [id]/page.tsx           # Person Detail
│   │       └── settings/
│   │           └── page.tsx                # Settings
│   ├── components/
│   │   ├── ui/                             # Base primitives
│   │   ├── sidebar/
│   │   │   └── FilterPanel.tsx
│   │   ├── show/
│   │   │   ├── ShowTile.tsx
│   │   │   ├── ShowGrid.tsx
│   │   │   ├── ShowRow.tsx
│   │   │   ├── StatusChips.tsx
│   │   │   ├── RatingBar.tsx
│   │   │   └── TagPicker.tsx
│   │   ├── detail/
│   │   │   ├── HeaderMedia.tsx
│   │   │   ├── CoreFacts.tsx
│   │   │   ├── DetailToolbar.tsx
│   │   │   ├── OverviewScoop.tsx
│   │   │   ├── AskAboutShow.tsx
│   │   │   ├── GenresLanguages.tsx
│   │   │   ├── RecommendationsStrand.tsx
│   │   │   ├── ExploreSimilar.tsx
│   │   │   ├── StreamingProviders.tsx
│   │   │   ├── CastCrew.tsx
│   │   │   ├── Seasons.tsx
│   │   │   └── BudgetRevenue.tsx
│   │   ├── find/
│   │   │   ├── SearchPanel.tsx
│   │   │   ├── AskPanel.tsx
│   │   │   └── AlchemyPanel.tsx
│   │   └── person/
│   │       ├── PersonHeader.tsx
│   │       ├── PersonAnalytics.tsx
│   │       └── Filmography.tsx
│   ├── hooks/
│   │   ├── useShowActions.ts
│   │   ├── useShowWithOverlay.ts
│   │   ├── useRemovalConfirmation.ts
│   │   └── useLocalSettings.ts
│   ├── lib/
│   │   ├── supabase/
│   │   │   ├── server.ts
│   │   │   └── client.ts
│   │   ├── repositories/
│   │   │   ├── show-repository.ts
│   │   │   └── settings-repository.ts
│   │   ├── services/
│   │   │   ├── catalog-service.ts
│   │   │   ├── ai-service.ts
│   │   │   └── show-resolver.ts
│   │   └── ai/
│   │       ├── prompts/
│   │       │   ├── base-persona.ts
│   │       │   ├── scoop-prompt.ts
│   │       │   ├── ask-prompt.ts
│   │       │   ├── concepts-prompt.ts
│   │       │   └── recommendations-prompt.ts
│   │       └── starter-prompts.ts
│   ├── types/
│   │   ├── show.ts
│   │   └── settings.ts
│   ├── contexts/
│   │   ├── SettingsContext.tsx
│   │   └── CollectionContext.tsx
│   └── middleware.ts
├── scripts/
│   └── test-reset.ts
└── tests/
    ├── unit/
    ├── integration/
    └── e2e/
```

---

## Key Technical Decisions & Rationale

| Decision | Rationale |
|---|---|
| Next.js App Router | Required by infra rider; enables server components, route handlers, middleware, streaming |
| Supabase with RLS | Required by infra rider; RLS provides defense-in-depth for namespace/user isolation |
| Composite primary key `(id, namespace_id, user_id)` on shows | Ensures complete data isolation between builds and users without needing separate tables |
| Server-side TMDB calls | API key protection; client never sees catalog provider credentials |
| Server-side AI calls | API key protection; enables streaming responses via route handlers |
| TanStack Query for client state | Efficient cache management, automatic refetching, optimistic updates for mutations |
| Zod for validation | Runtime type safety at API boundaries; complements TypeScript compile-time checks |
| Separate repository layer | Clean separation; easy to swap Supabase for another provider later (per rider non-goals) |
| Streaming AI responses (SSE) | Prevents blank-stare UX during Scoop/Ask generation; matches spec requirement |
| Local storage for UI preferences | Font size, autoSearch, filter state are device-local; not worth syncing |
| Cloud settings for user/AI config | Username, API keys, AI model need cross-device sync capability |

---

## Risks & Mitigations

| Risk | Mitigation |
|---|---|
| AI hallucinating show titles | Show resolver validates against TMDB; unresolvable titles shown as non-interactive or handed to search |
| AI structured output parse failures | Retry with stricter formatting; fall back to unstructured text |
| TMDB rate limiting | Server-side caching of catalog responses; debounce search input |
| Large user libraries impacting performance | Paginate collection queries; index on status/tags/genres |
| Namespace data leakage | RLS policies + application-level WHERE clauses (defense-in-depth) |
| Schema changes breaking existing data | Migration system with version tracking; non-destructive forward migrations |
| AI Scoop cache staleness | 4-hour freshness window with on-demand regeneration |

---

## Open Questions (Deferred per PRD)

These items are noted in the PRD as open questions and are NOT included in this implementation plan:
- Whether "Next" becomes a first-class UI status (data model supports it)
- Named custom lists beyond tags
- Whether generating AI Scoop on unsaved show implicitly saves it
- Whether clearing My Rating stores explicit "Unrated" vs nil
- Import/Restore from export ZIP
- Saving/sharing Alchemy sessions
- Explicit myStatus filters in sidebar (data model supports it)
