# Implementation Plan — Personal TV & Movie Companion

> Generated from `docs/prd/`. This plan covers architecture, data model, feature breakdown, AI integration, and a phased implementation roadmap. It is technology-aware per `infra_rider_prd.md` (Next.js + Supabase) but stays focused on product behavior over vendor-specific details.

---

## 1. Executive Summary

Build a web application that lets users collect, organize, rate, and discover TV shows and movies. The product has three pillars:

1. **Personal Library** — A status-driven collection (Active, Later, Wait, Done, Quit) with user tags, ratings, and notes.
2. **Catalog + Detail** — Rich show/person pages backed by an external catalog (TMDB or similar), with streaming availability, cast/crew, trailers, and recommendations.
3. **AI-Powered Discovery** — Conversational "Ask," concept-blending "Alchemy," and per-show "Explore Similar," all grounded in the user's library and taste profile.

The build target is **Next.js (latest stable)** with **Supabase** as the persistence layer, and must support isolated benchmark runs via `namespace_id` + `user_id` scoping.

---

## 2. Guiding Architecture

### 2.1 Tech Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Runtime / UI | Next.js (App Router) | Required by benchmark baseline; gives SSR, server actions, and API routes. |
| Language | TypeScript | Type safety across data mapping, AI contracts, and UI. |
| Persistence | Supabase (Postgres) | Required by benchmark baseline; handles relational user data, JSON blobs, and optional sync. |
| Auth (dev/benchmark) | Dev-only identity injection (`X-User-Id` header or server env default) | Satisfies infra rider; swappable for real OAuth later without schema changes. |
| External Catalog | TMDB (or equivalent) | Mature, poster/backdrop/cast/crew/providers support; keys from env. |
| AI Provider | OpenAI / Anthropic / etc. via server-side calls | API key from env or user settings; never commit keys. |
| Styling | Tailwind CSS + CSS variables / design tokens | Aligns with "no inline styles" guideline; theme tokens for spacing, colors, type. |
| State | React hooks + server actions + SWR/React Query | Server is source of truth; client cache is disposable. |
| Testing | Vitest + React Testing Library + Playwright | Unit tests for logic; E2E for critical journeys. |

### 2.2 Fractal Directory Structure

Follow the repo's `INSTRUCTIONS.md` fractal architecture: pages contain features, features contain sub-features. No `index.tsx`; main file matches directory name.

```
my-app/
├── .env.example
├── .gitignore
├── package.json
├── supabase/
│   ├── migrations/
│   │   ├── 0001_initial_schema.sql
│   │   └── 0002_add_ai_scoop.sql
│   └── seed.sql
├── src/
│   ├── config/                  # Env, constants, feature flags
│   │   ├── env.ts
│   │   ├── constants.ts
│   │   └── filters.ts
│   ├── theme/                   # Tokens, global styles
│   │   ├── tokens.css
│   │   └── fonts.ts
│   ├── components/              # Shared UI primitives
│   │   ├── ShowTile/
│   │   │   └── ShowTile.tsx
│   │   ├── StatusChip/
│   │   │   └── StatusChip.tsx
│   │   ├── RatingSlider/
│   │   │   └── RatingSlider.tsx
│   │   ├── ConceptChip/
│   │   │   └── ConceptChip.tsx
│   │   ├── Strand/
│   │   │   └── Strand.tsx
│   │   └── PageShell/
│   │       └── PageShell.tsx
│   ├── hooks/                   # Global/shared hooks
│   │   ├── useUser.ts
│   │   ├── useNamespace.ts
│   │   └── useDebounce.ts
│   ├── utils/                   # Global pure functions
│   │   ├── dates.ts
│   │   ├── mergeShows.ts
│   │   └── catalogMappers.ts
│   ├── lib/                     # External clients (server-only where secrets)
│   │   ├── supabase/
│   │   │   ├── client.ts        # Anon key client
│   │   │   └── server.ts        # Service role / server client
│   │   ├── catalog/
│   │   │   └── tmdbClient.ts
│   │   └── ai/
│   │       ├── aiClient.ts
│   │       ├── prompts/
│   │       │   ├── ask.ts
│   │       │   ├── scoop.ts
│   │       │   ├── concepts.ts
│   │       │   └── conceptRecs.ts
│   │       └── parsers.ts
│   └── pages/
│       ├── Home/
│       │   ├── Home.tsx
│       │   ├── HomePage.tsx     # Next.js page wrapper
│       │   ├── layout.tsx
│       │   └── features/
│       │       ├── CollectionList/
│       │       │   ├── CollectionList.tsx
│       │       │   ├── hooks/
│       │       │   │   └── useCollectionList.ts
│       │       │   └── features/
│       │       │       └── StatusSection/
│       │       │           ├── StatusSection.tsx
│       │       │           └── hooks/
│       │       │               └── useStatusSection.ts
│       │       ├── FilterSidebar/
│       │       │   ├── FilterSidebar.tsx
│       │       │   └── hooks/
│       │       │       └── useFilters.ts
│       │       └── MediaTypeToggle/
│       │           ├── MediaTypeToggle.tsx
│       │           └── constants.ts
│       ├── Find/
│       │   ├── Find.tsx
│       │   ├── FindPage.tsx
│       │   └── features/
│       │       ├── ModeSwitcher/
│       │       │   └── ModeSwitcher.tsx
│       │       ├── Search/
│       │       │   ├── Search.tsx
│       │       │   ├── hooks/
│       │       │   │   └── useCatalogSearch.ts
│       │       │   └── features/
│       │       │       └── SearchResultsGrid/
│       │       │           └── SearchResultsGrid.tsx
│       │       ├── Ask/
│       │       │   ├── Ask.tsx
│       │       │   ├── hooks/
│       │       │   │   ├── useAskSession.ts
│       │       │   │   └── useMentionedShows.ts
│       │       │   └── features/
│       │       │       ├── ChatTranscript/
│       │       │       │   └── ChatTranscript.tsx
│       │       │       ├── MentionedShowsStrip/
│       │       │       │   └── MentionedShowsStrip.tsx
│       │       │       └── StarterPrompts/
│       │       │           └── StarterPrompts.tsx
│       │       └── Alchemy/
│       │           ├── Alchemy.tsx
│       │           ├── hooks/
│       │           │   ├── useAlchemySession.ts
│       │           │   └── useConceptSelection.ts
│       │           └── features/
│       │               ├── InputPicker/
│       │               │   └── InputPicker.tsx
│       │               ├── ConceptCatalysts/
│       │               │   └── ConceptCatalysts.tsx
│       │               └── AlchemyResults/
│       │                   └── AlchemyResults.tsx
│       ├── ShowDetail/
│       │   ├── ShowDetail.tsx
│       │   ├── ShowDetailPage.tsx
│       │   └── features/
│       │       ├── HeaderMedia/
│       │       │   └── HeaderMedia.tsx
│       │       ├── CoreFacts/
│       │       │   └── CoreFacts.tsx
│       │       ├── MyRelationshipToolbar/
│       │       │   ├── MyRelationshipToolbar.tsx
│       │       │   └── hooks/
│       │       │       └── useMyRelationship.ts
│       │       ├── OverviewAndScoop/
│       │       │   ├── OverviewAndScoop.tsx
│       │       │   └── hooks/
│       │       │       └── useScoop.ts
│       │       ├── AskAboutShow/
│       │       │   └── AskAboutShow.tsx
│       │       ├── RecommendationsStrand/
│       │       │   └── RecommendationsStrand.tsx
│       │       ├── ExploreSimilar/
│       │       │   ├── ExploreSimilar.tsx
│       │       │   └── hooks/
│       │       │       └── useExploreSimilar.ts
│       │       ├── StreamingProviders/
│       │       │   └── StreamingProviders.tsx
│       │       ├── CastCrewStrand/
│       │       │   └── CastCrewStrand.tsx
│       │       ├── Seasons/
│       │       │   └── Seasons.tsx
│       │       └── BudgetRevenue/
│       │           └── BudgetRevenue.tsx
│       ├── PersonDetail/
│       │   ├── PersonDetail.tsx
│       │   ├── PersonDetailPage.tsx
│       │   └── features/
│       │       ├── PersonHeader/
│       │       │   └── PersonHeader.tsx
│       │       ├── PersonAnalytics/
│       │       │   └── PersonAnalytics.tsx
│       │       └── Filmography/
│       │           └── Filmography.tsx
│       └── Settings/
│           ├── Settings.tsx
│           ├── SettingsPage.tsx
│           └── features/
│               ├── AppearanceSettings/
│               │   └── AppearanceSettings.tsx
│               ├── AISettings/
│               │   └── AISettings.tsx
│               ├── CatalogSettings/
│               │   └── CatalogSettings.tsx
│               └── DataManagement/
│                   ├── DataManagement.tsx
│                   └── hooks/
│                       └── useDataExport.ts
```

### 2.3 Key Architectural Decisions

1. **Server is source of truth.** All writes go through Next.js server actions or API routes to Supabase. Client cache (SWR/React Query) is disposable.
2. **Namespace + user scoping.** Every persisted record includes `(namespace_id, user_id)`. Dev identity injection provides these without OAuth.
3. **External catalog is read-only cache.** TMDB data is mapped into the app's `Show` shape on fetch; only public metadata is refreshed, never user overlay.
4. **AI calls are server-only.** API keys live only in server env / user encrypted settings; parsing and fallback logic are centralized.
5. **Humble components.** TSX files contain markup and binding; logic lives in adjacent `useFeatureLogic` hooks.
6. **Feature co-location.** Hooks/utils that are only used by one feature live inside that feature's directory.

---

## 3. Data Model

### 3.1 Supabase Tables

```sql
-- Run / build isolation primitive (not a user concept)
CREATE TABLE namespaces (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  slug TEXT UNIQUE NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Scoped users within a namespace. Dev mode seeds one default user per namespace.
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  namespace_id UUID NOT NULL REFERENCES namespaces(id) ON DELETE CASCADE,
  external_id TEXT, -- opaque stable string for future OAuth migration
  username TEXT,
  created_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE (namespace_id, external_id)
);

-- Saved shows with catalog metadata + user overlay + AI scoop
CREATE TABLE shows (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  namespace_id UUID NOT NULL REFERENCES namespaces(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

  -- Identity
  external_catalog_id TEXT NOT NULL,
  media_type TEXT NOT NULL CHECK (media_type IN ('movie','tv')),
  title TEXT NOT NULL,

  -- Catalog metadata (refreshed from TMDB)
  overview TEXT,
  tagline TEXT,
  genres TEXT[] DEFAULT '{}',
  original_language TEXT,
  spoken_languages TEXT[] DEFAULT '{}',
  languages TEXT[] DEFAULT '{}',
  poster_url TEXT,
  backdrop_url TEXT,
  logo_url TEXT,
  vote_average REAL,
  vote_count INT,
  popularity REAL,
  release_date DATE,
  first_air_date DATE,
  last_air_date DATE,
  runtime INT,
  budget BIGINT,
  revenue BIGINT,
  series_status TEXT,
  number_of_episodes INT,
  number_of_seasons INT,
  episode_run_time INT[],
  provider_data JSONB DEFAULT '{}',

  -- User overlay ("My Data")
  my_status TEXT CHECK (my_status IN ('active','later','wait','done','quit')),
  my_status_updated_at TIMESTAMPTZ,
  my_interest TEXT CHECK (my_interest IN ('interested','excited')),
  my_interest_updated_at TIMESTAMPTZ,
  my_tags TEXT[] DEFAULT '{}',
  my_tags_updated_at TIMESTAMPTZ,
  my_score REAL,
  my_score_updated_at TIMESTAMPTZ,

  -- AI data
  ai_scoop TEXT,
  ai_scoop_updated_at TIMESTAMPTZ,

  -- Management
  details_updated_at TIMESTAMPTZ DEFAULT now(),
  created_at TIMESTAMPTZ DEFAULT now(),

  UNIQUE (namespace_id, user_id, external_catalog_id)
);

-- App-wide settings synced per user
CREATE TABLE user_settings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  namespace_id UUID NOT NULL REFERENCES namespaces(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  username TEXT,
  font_size TEXT DEFAULT 'M' CHECK (font_size IN ('XS','S','M','L','XL','XXL')),
  search_on_launch BOOLEAN DEFAULT FALSE,
  ai_model TEXT,
  ai_api_key_encrypted TEXT,
  catalog_api_key_encrypted TEXT,
  version BIGINT DEFAULT 0,
  updated_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE (namespace_id, user_id)
);

-- RLS policies: users can only see/modify rows in their namespace + user_id
ALTER TABLE shows ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_settings ENABLE ROW LEVEL SECURITY;
```

### 3.2 TypeScript Shapes

```ts
// src/types/show.ts
export type MediaType = 'movie' | 'tv';
export type MyStatus = 'active' | 'later' | 'wait' | 'done' | 'quit';
export type MyInterest = 'interested' | 'excited';

export interface Show {
  id: string;
  externalCatalogId: string;
  mediaType: MediaType;
  title: string;

  // Catalog metadata
  overview?: string;
  tagline?: string;
  genres: string[];
  originalLanguage?: string;
  spokenLanguages: string[];
  languages: string[];
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
  seriesStatus?: string;
  numberOfEpisodes?: number;
  numberOfSeasons?: number;
  episodeRunTime: number[];
  providerData: ProviderData;

  // My Data
  myStatus?: MyStatus;
  myStatusUpdatedAt?: string;
  myInterest?: MyInterest;
  myInterestUpdatedAt?: string;
  myTags: string[];
  myTagsUpdatedAt?: string;
  myScore?: number;
  myScoreUpdatedAt?: string;

  // AI
  aiScoop?: string;
  aiScoopUpdatedAt?: string;

  // Management
  detailsUpdatedAt: string;
  createdAt: string;
}

export interface ProviderData {
  countries?: Record<string, { flatrate?: number[]; rent?: number[]; buy?: number[] }>;
}

export interface UserSettings {
  username: string;
  fontSize: 'XS' | 'S' | 'M' | 'L' | 'XL' | 'XXL';
  searchOnLaunch: boolean;
  aiModel?: string;
  aiApiKey?: string;
  catalogApiKey?: string;
  version: number;
}
```

### 3.3 Merge & Persistence Rules

1. **Collection membership:** A show is "in collection" when `my_status` is non-null.
2. **Auto-save triggers:**
   - Setting any status → save with that status.
   - Selecting Interested/Excited → set `my_status='later'`, `my_interest` accordingly.
   - Rating an unsaved show → save as `my_status='done'`, `my_score` set.
   - Adding first tag to unsaved show → save as `my_status='later'`, `my_interest='interested'`.
3. **Defaults:** New save without explicit status defaults to `later` + `interested`.
4. **Removal:** Clearing status shows confirmation; on confirm, delete the row (or nullify all My Data per product behavior). Use deletion to honor "removes from collection."
5. **Catalog refresh merge:**
   - Non-empty catalog fields win over empty stored fields (`selectFirstNonEmpty`).
   - My Data fields resolve by `updated_at` timestamp (newer wins).
   - Update `detailsUpdatedAt` after merge.
6. **AI Scoop:** Persisted only when show is in collection; 4-hour freshness; regenerate on demand when stale.

---

## 4. Feature Breakdown

### 4.1 Collection Home

**Purpose:** Display the user's library organized by relationship/status.

**Components:**
- `HomePage` / `Home` layout: sidebar + main content.
- `FilterSidebar`: All Shows, per-tag filters, "No tags," genre/decade/community-score filters.
- `MediaTypeToggle`: All / Movies / TV.
- `CollectionList`: groups shows into sections.
- `StatusSection`: Active (large tiles), Excited, Interested, Other (collapsed Wait/Quit/Done/unclassified Later).
- `ShowTile`: poster, title, in-collection indicator, user rating indicator.

**Logic:**
- `useCollectionList`: fetch saved shows for `(namespace_id, user_id)`, apply selected filter + media type, group by derived status.
- `useFilters`: derive available tag filters from user's saved tags.

**Empty states:**
- No collection: CTA to Search / Ask.
- Filter yields none: "No results found."

### 4.2 Find / Discover Hub

**Purpose:** Unified entry point for Search, Ask, and Alchemy.

**Components:**
- `FindPage` / `Find` with `ModeSwitcher`.

**Modes:**
1. **Search**
   - Text input debounced.
   - `useCatalogSearch`: call TMDB search; map results to `Show` shape; mark items already in collection.
   - `SearchResultsGrid`: poster grid.
2. **Ask**
   - Chat UI with user/assistant turns.
   - `useAskSession`: maintain React state of turns; call server action for AI response; summarize after ~10 turns.
   - `MentionedShowsStrip`: parse `showList` from structured response; resolve to catalog shows.
   - `StarterPrompts`: 6 random prompts from curated list, refreshable.
3. **Alchemy**
   - `useAlchemySession`: track inputs → concepts → results.
   - `InputPicker`: select 2+ starting shows (library + catalog search).
   - `ConceptCatalysts`: fetch AI concepts; selectable chips; max 8.
   - `AlchemyResults`: 6 AI recommendations; "More Alchemy!" chains results as new inputs.

### 4.3 Show Detail

**Purpose:** Single source of truth for a show.

**Section order (preserve existing narrative hierarchy):**
1. `HeaderMedia` — backdrops/posters/logos/trailers; fallback gracefully.
2. `CoreFacts` — year/runtime, community score.
3. `MyRelationshipToolbar` — status chips (Active, Interested, Excited, Wait, Done, Quit), rating slider, tags.
4. `OverviewAndScoop` — overview + "Give me the scoop!" toggle; streaming generation.
5. `AskAboutShow` — CTA to Ask seeded with this show.
6. `GenresLanguages` — genres + languages.
7. `RecommendationsStrand` — similar/recommended shows.
8. `ExploreSimilar` — Get Concepts → select → Explore Shows → 5 recs.
9. `StreamingProviders` — "Stream It" section.
10. `CastCrewStrand` — horizontal strands → Person Detail.
11. `Seasons` — TV only.
12. `BudgetRevenue` — movies only.

**Key logic:**
- `useMyRelationship`: handle status toggle, rating, tag add/remove; enforce auto-save/default rules; removal confirmation.
- `useScoop`: check freshness (4h), stream generation, persist only if in collection.
- `useExploreSimilar`: fetch concepts for single show, manage selection, fetch 5 recs.

### 4.4 Person Detail

**Purpose:** Explore cast/crew talent.

**Components:**
- `PersonHeader`: image gallery, name, bio.
- `PersonAnalytics`: charts for average project ratings, top genres, projects-by-year.
- `Filmography`: credits grouped by year; tapping credit opens Show Detail.

**Data:** Fetched transiently from TMDB; not persisted in `shows` table.

### 4.5 Settings & Data Management

**Components:**
- `AppearanceSettings`: font size, search-on-launch toggle.
- `AISettings`: AI provider key (server-encrypted), model selection.
- `CatalogSettings`: catalog provider key.
- `DataManagement`: export My Data as `.zip` containing ISO-8601 JSON backup.

**Notes:**
- Keys are optional; benchmark mode reads from env if not provided by user.
- Never commit keys to repo.

---

## 5. Backend & Server Layer

### 5.1 Server Actions / API Routes

| Endpoint / Action | Purpose |
|-------------------|---------|
| `getCurrentUser()` | Resolve `(namespace_id, user_id)` from dev header/env; ensure user row exists. |
| `searchCatalog(query, mediaType?)` | Proxy TMDB search; map to `Show` shapes. |
| `getShowDetails(externalId, mediaType)` | Fetch TMDB details + credits + videos + providers + recommendations; merge with saved show. |
| `getPersonDetails(externalId)` | Fetch TMDB person + credits; return transient shape. |
| `saveShow(show)` | Upsert show with My Data; apply auto-save defaults. |
| `updateMyStatus(...)` | Set/clear status; handle removal confirmation flow. |
| `updateMyInterest(...)` | Set interest (only valid when status is Later). |
| `updateMyTags(...)` | Add/remove tags; auto-save if first tag on unsaved show. |
| `updateMyScore(...)` | Set/clear rating; auto-save as Done if unsaved. |
| `getCollection(filters)` | Return saved shows for filter + media type. |
| `askChat(turns, library)` | Stream AI chat response; parse structured mentions. |
| `getConcepts(showIds, mediaTypes)` | Return 8 evocative concepts for single or multi-show. |
| `getConceptRecommendations(concepts, context)` | Return 5 (Explore) or 6 (Alchemy) recs mapped to catalog IDs. |
| `generateScoop(show)` | Return personality-driven review; persist if in collection. |
| `exportMyData()` | Zip JSON backup of all saved shows + settings. |
| `resetNamespaceData()` | Dev/test: delete all data for current namespace. |

### 5.2 Identity Injection (Dev / Benchmark)

- Read `NAMESPACE_ID` and `USER_ID` from request headers (`X-Namespace-Id`, `X-User-Id`) or env fallback.
- If missing, create deterministic defaults (e.g., `default` namespace + `default` user).
- Gate this behind `process.env.NODE_ENV !== 'production'` or an explicit `ALLOW_DEV_AUTH` flag.
- All Supabase RLS policies enforce `(namespace_id, user_id)` so dev injection cannot leak across runs.

### 5.3 Catalog Mapping

- Decode TMDB payload into app `Show` shape.
- Map IDs: `external_catalog_id = tmdbId`.
- Map images to full URLs using configured base URL.
- Store provider IDs only; resolve provider metadata client-side or from a static map.
- Mark transient fields (`cast`, `crew`, `seasons`, `videos`, `recommendations`) as not persisted.

---

## 6. AI Integration

### 6.1 Prompt Architecture

Centralize prompts in `src/lib/ai/prompts/`. Each prompt is a function that receives typed context and returns a string.

| Surface | File | Key Requirements |
|---------|------|------------------|
| Ask | `ask.ts` | Friend mode, taste-aware, bulleted recs, spoiler-safe, stay in TV/movies. |
| Ask with mentions | `ask.ts` + parser | Structured output: `commentary` + `showList` (`Title::externalId::mediaType;;...`). |
| Scoop | `scoop.ts` | Mini blog-post: personal take, stack-up, centerpiece, fit/warnings, verdict; 150–350 words. |
| Concepts | `concepts.ts` | Bullet list, 1–3 words, shared across all inputs for Alchemy, no spoilers. |
| Concept recs | `conceptRecs.ts` | 5 or 6 recs, reasons name concepts, bias recent but allow classics, real IDs. |

### 6.2 Parsing & Fallbacks

- `src/lib/ai/parsers.ts`: dedicated parsers for each structured output.
- On parse failure: retry once with stricter formatting; fallback to unstructured commentary + Search handoff.
- Validate that recommended IDs resolve to real catalog items; unresolved titles are shown non-interactively.

### 6.3 Context Inclusion

- For Ask / Alchemy / Explore Similar: include user's saved shows with status, tags, ratings as context.
- Summarize older chat turns to control token depth while preserving persona.
- Never include provider API keys or user keys in prompts.

### 6.4 Streaming

- Scoop and Ask should stream progressively to avoid blank states.
- Use Vercel AI SDK or native stream handling in server actions.

---

## 7. UI / UX Plan

### 7.1 Design Tokens

Create `src/theme/tokens.css`:
- Colors: background, surface, primary, text, muted, rating, status colors.
- Spacing scale.
- Typography scale.
- Radius, shadows.
- Breakpoints.

### 7.2 Shared Primitives

- `ShowTile`: consistent poster aspect ratio, badges, hover state.
- `StatusChip`: selected/unselected states; reselect triggers removal.
- `RatingSlider`: 0–10 or 0–5 with "unrated" state.
- `ConceptChip`: selectable, max-selection disabled state.
- `Strand`: horizontal scrollable row of tiles with section title.
- `PageShell`: nav, main area, responsive sidebar.

### 7.3 Responsive Layout

- Sidebar collapses to drawer on small screens.
- Home uses grid/list layouts that adapt to viewport.
- Detail page stacks vertically on mobile; media header full-width.

---

## 8. Implementation Phases

### Phase 1 — Foundation (Week 1)

1. Initialize Next.js project with TypeScript, Tailwind, Supabase client, Vitest, Playwright.
2. Create `.env.example`, `.gitignore`, and dev scripts (`dev`, `test`, `test:reset`).
3. Set up Supabase migrations: `namespaces`, `users`, `shows`, `user_settings`.
4. Implement dev identity injection middleware + default user seeding.
5. Create shared types, theme tokens, and base primitives (`ShowTile`, `PageShell`).
6. Build catalog client + mappers for TMDB.
7. Implement server actions: `searchCatalog`, `getShowDetails`, `saveShow`, `getCollection`.

**Milestone:** Can run app, search catalog, view detail, save a show, see it on Home.

### Phase 2 — Library & Detail (Week 2)

1. Build `Home` with filter sidebar, media type toggle, status grouping.
2. Build `ShowDetail` sections: header media, core facts, relationship toolbar, overview.
3. Implement full My Data flow: status, interest, tags, rating with auto-save rules.
4. Add removal confirmation + "don't ask again" preference.
5. Add streaming availability, cast/crew, seasons, budget/revenue sections.
6. Build `PersonDetail` with analytics and filmography.

**Milestone:** Collection management feels complete; detail page is rich and functional.

### Phase 3 — AI Discovery (Week 3)

1. Implement AI client and prompt library.
2. Build `Ask` mode with chat UI, starter prompts, mentioned shows strip.
3. Implement conversation summarization after ~10 turns.
4. Build `Alchemy` flow: input picker → concepts → results → chaining.
5. Build `ExploreSimilar` on Show Detail: concepts → 5 recs.
6. Implement `Scoop` generation with freshness check and streaming.

**Milestone:** All three discovery modes functional and resolving to real shows.

### Phase 4 — Settings, Export & Polish (Week 4)

1. Build `Settings` page: appearance, AI, catalog, data export.
2. Implement `.zip` export with ISO-8601 JSON.
3. Add data migration/versioning safeguard for future schema changes.
4. Add unit tests for merge logic, status rules, AI parsers.
5. Add Playwright tests for golden journeys: build collection, Ask, Alchemy, export.
6. Performance pass: debounce search, image optimization, lazy-load detail sections.
7. Accessibility pass: focus management, keyboard navigation, screen reader labels.

**Milestone:** Production-ready benchmark build; all tests green.

---

## 9. Testing Strategy

### 9.1 Unit Tests

- `mergeShows.test.ts`: catalog merge rules, timestamp resolution.
- `myRelationship.test.ts`: auto-save defaults, status → interest interactions, removal.
- `catalogMappers.test.ts`: TMDB JSON → Show shape for movie and TV.
- `aiParsers.test.ts`: mention list parser, concept parser, rec parser fallbacks.

### 9.2 Integration / E2E Tests

- Build collection: Search → Detail → set Interested → tag → rate → see on Home.
- Ask discovery: Ask a question → see mentioned shows → open one → save.
- Alchemy: pick inputs → conceptualize → select concepts → alchemize → chain.
- Explore Similar: Detail → Get Concepts → select → Explore Shows → save.
- Export data: Settings → Export → verify zip contains valid JSON.
- Namespace isolation: two namespaces do not see each other's data.

### 9.3 Quality Bar Validation

- Manual golden-set review of AI outputs against `discovery_quality_bar.md`:
  - Voice adherence
  - Taste alignment
  - Surprise without betrayal
  - Specificity
  - Real-show integrity (must be 2/2)

---

## 10. Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| AI provider rate limits / failures | Discovery features break | Implement robust fallbacks; cache concepts; allow user-provided keys. |
| Catalog ID mismatches in AI recs | Recs don't map to real shows | Parse IDs strictly; unresolved titles shown non-interactively or handed to Search. |
| Namespace/user scoping bugs | Data leaks between benchmark runs | RLS policies + server-side enforcement; isolation E2E tests. |
| Schema changes break existing libraries | User data loss | Versioned migrations; merge-forward logic; export/backup first. |
| Streaming AI complexity | Blank states, broken UX | Use Vercel AI SDK or proven streaming utilities; degrade to non-streaming. |
| Rich detail page becomes overwhelming | Poor UX | Preserve narrative hierarchy; cluster primary actions early; lazy-load tail sections. |

---

## 11. Open Questions to Resolve During Build

1. Should **Next** be surfaced as a first-class UI status? (PRD leaves open.)
2. Should generating an AI Scoop on an unsaved show implicitly save it? (PRD leaves open; current plan: no, persist only if already saved.)
3. Should clearing a rating store an explicit "Unrated" state vs `null`? (Plan: use `null` / absent score.)
4. Import/Restore from export zip is desired but out of scope for initial build; leave hook point.
5. Exact AI model and token budget will be tuned during Phase 3 quality bar validation.

---

## 12. Deliverables Checklist

- [ ] Next.js app bootstrapped with TypeScript + Tailwind.
- [ ] `.env.example` and `.gitignore` for secrets.
- [ ] Supabase migrations for `namespaces`, `users`, `shows`, `user_settings`.
- [ ] Dev identity injection + namespace isolation.
- [ ] Catalog search + detail mapping.
- [ ] Collection Home with filters and status grouping.
- [ ] Show Detail with My Data controls and all sections.
- [ ] Person Detail.
- [ ] Ask, Alchemy, Explore Similar, and Scoop AI features.
- [ ] Settings + Export My Data.
- [ ] Unit + E2E tests.
- [ ] `npm run dev`, `npm test`, `npm run test:reset` scripts.

---

*End of plan.*
