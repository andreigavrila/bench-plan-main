# Implementation Plan

## 1. Project Bootstrap

### 1.1 Initialize Next.js + Supabase Project
- Create Next.js (latest stable) project with TypeScript, App Router, Tailwind CSS
- Install dependencies: `@supabase/supabase-js`, `@supabase/ssr`, AI SDK (e.g. `openai` or `@anthropic-ai/sdk`)
- Create `.env.example` with all required variables:
  ```
  NEXT_PUBLIC_SUPABASE_URL=
  NEXT_PUBLIC_SUPABASE_ANON_KEY=
  SUPABASE_SERVICE_ROLE_KEY=       # server-only
  TMDB_API_KEY=                    # content catalog
  AI_API_KEY=                      # AI provider
  AI_MODEL=                        # AI model name
  NAMESPACE_ID=                    # build isolation
  DEFAULT_USER_ID=                 # dev identity
  ```
- `.gitignore` excludes `.env*` (except `.env.example`)

### 1.2 Scripts
- `npm run dev` — start app
- `npm test` — run tests
- `npm run test:reset` — reset test data for current namespace
- `npm run db:migrate` — run migrations

---

## 2. Database Schema & Migrations

### 2.1 Supabase Migrations

All tables include `namespace_id` column for build isolation and `user_id` for user scoping. Primary partition key is `(namespace_id, user_id)` on user-owned tables.

#### Table: `shows`
Maps directly to the `Show` interface from `storage-schema.ts`. Key columns:

| Column | Type | Notes |
|--------|------|-------|
| `id` | `text` PK | Catalog external ID |
| `namespace_id` | `text` NOT NULL | Build isolation |
| `user_id` | `text` NOT NULL | User scoping |
| `title` | `text` NOT NULL | |
| `show_type` | `text` NOT NULL | `movie`, `tv`, `person`, `unknown` |
| `external_ids` | `jsonb` | Optional external IDs |
| `overview` | `text` | |
| `genres` | `text[]` | Genre name strings |
| `tagline` | `text` | |
| `homepage` | `text` | |
| `original_language` | `text` | |
| `spoken_languages` | `text[]` | |
| `languages` | `text[]` | |
| `poster_url` | `text` | |
| `backdrop_url` | `text` | |
| `logo_url` | `text` | |
| `network_logos` | `text[]` | |
| `vote_average` | `float8` | |
| `vote_count` | `int4` | |
| `popularity` | `float8` | |
| `last_air_date` | `timestamptz` | |
| `first_air_date` | `timestamptz` | |
| `release_date` | `timestamptz` | |
| `runtime` | `int4` | Movie runtime |
| `budget` | `int4` | |
| `revenue` | `int4` | |
| `series_status` | `text` | |
| `number_of_episodes` | `int4` | |
| `number_of_seasons` | `int4` | |
| `episode_run_time` | `int4[]` | |
| `my_tags` | `text[]` | |
| `my_tags_update_date` | `timestamptz` | |
| `my_score` | `float8` | |
| `my_score_update_date` | `timestamptz` | |
| `my_status` | `text` | `active`, `later`, `done`, `quit`, `wait`, `next` |
| `my_interest` | `text` | `excited`, `interested` |
| `my_interest_update_date` | `timestamptz` | |
| `my_status_update_date` | `timestamptz` | |
| `ai_scoop` | `text` | |
| `ai_scoop_update_date` | `timestamptz` | |
| `details_update_date` | `timestamptz` | |
| `creation_date` | `timestamptz` | |
| `is_test` | `boolean` DEFAULT false | |
| `provider_data` | `jsonb` | ProviderData blob |

- Unique constraint on `(namespace_id, user_id, id)`
- Indexes on `(namespace_id, user_id, my_status)`, `(namespace_id, user_id, my_tags)` (GIN)

#### Table: `cloud_settings`
| Column | Type | Notes |
|--------|------|-------|
| `id` | `text` DEFAULT `'globalSettings'` | |
| `namespace_id` | `text` NOT NULL | |
| `user_id` | `text` NOT NULL | |
| `user_name` | `text` | |
| `version` | `float8` | Epoch seconds for conflict resolution |
| `catalog_api_key` | `text` | |
| `ai_api_key` | `text` | |
| `ai_model` | `text` | |

- PK on `(namespace_id, user_id, id)`

#### Table: `app_metadata`
| Column | Type |
|--------|------|
| `namespace_id` | `text` PK |
| `data_model_version` | `int4` DEFAULT 3 |

### 2.2 Row Level Security (RLS)
- Enable RLS on all tables
- Policies scoped to `namespace_id` and `user_id` from request context
- In dev/benchmark mode, these come from headers or env vars

### 2.3 Namespace Reset Script
- `npm run test:reset` calls a server endpoint or Supabase function that deletes all rows matching current `namespace_id` (optionally filtered to `is_test = true`)

---

## 3. Architecture & Project Structure

```
src/
  app/
    layout.tsx                  # Root layout with sidebar + nav
    page.tsx                    # Collection Home
    find/
      page.tsx                  # Find/Discover hub (Search default)
      search/page.tsx           # Search mode
      ask/page.tsx              # Ask (AI chat) mode
      alchemy/page.tsx          # Alchemy mode
    show/[id]/page.tsx          # Show Detail
    person/[id]/page.tsx        # Person Detail
    settings/page.tsx           # Settings
    api/
      shows/route.ts            # CRUD for user shows
      shows/[id]/route.ts       # Single show operations
      shows/export/route.ts     # Export/backup
      settings/route.ts         # Cloud settings CRUD
      ai/
        scoop/route.ts          # AI Scoop generation
        ask/route.ts            # Ask chat (streaming)
        concepts/route.ts       # Concept extraction
        recommendations/route.ts # Concept-based recs
        alchemy/route.ts        # Alchemy flow
      catalog/
        search/route.ts         # External catalog search
        show/[id]/route.ts      # External catalog detail
        person/[id]/route.ts    # Person detail from catalog
      test/
        reset/route.ts          # Namespace reset
  lib/
    supabase/
      client.ts                 # Browser client (anon key)
      server.ts                 # Server client (service role)
      middleware.ts              # Identity injection
    catalog/
      tmdb.ts                   # TMDB API wrapper
      mapper.ts                 # External catalog -> Show mapping
      merge.ts                  # Merge/overwrite logic
    ai/
      prompts.ts                # All prompt templates
      personality.ts            # Voice/persona config
      parser.ts                 # Structured output parsing (showList format)
      concepts.ts               # Concept generation logic
    types/
      show.ts                   # Show, MyStatusType, MyInterestType, etc.
      filters.ts                # FilterConfiguration, FilterType
      settings.ts               # CloudSettings, LocalSettings
    business/
      save-rules.ts             # Auto-save, default status logic
      collection.ts             # Collection membership helpers
  components/
    layout/
      Sidebar.tsx               # Filter nav panel
      TopNav.tsx                # Global nav (Find, Settings)
      MediaTypeToggle.tsx       # All / Movies / TV
    home/
      StatusSection.tsx         # Grouped shows by status
      ShowTile.tsx              # Poster + badges
    detail/
      HeaderCarousel.tsx        # Backdrops/posters/logos/trailers
      CoreFacts.tsx             # Year, runtime, community score
      StatusChips.tsx           # Status/interest toolbar
      RatingBar.tsx             # My Rating slider
      TagPicker.tsx             # My Tags
      Overview.tsx              # Overview text
      ScoopSection.tsx          # AI Scoop toggle + streaming
      AskAboutShow.tsx          # "Ask about this show" CTA
      RecommendationsStrand.tsx # Traditional recs
      ExploreSimilar.tsx        # Concepts -> recs flow
      StreamingAvailability.tsx # Providers
      CastCrew.tsx              # Horizontal cast/crew
      Seasons.tsx               # TV seasons
      BudgetRevenue.tsx         # Movie financials
    find/
      ModeSwitcher.tsx          # Search / Ask / Alchemy tabs
      SearchResults.tsx         # Poster grid with collection badges
      ChatUI.tsx                # Ask chat interface
      MentionedShowsStrip.tsx   # Horizontal mentioned shows
      StarterPrompts.tsx        # 6 random starters
      AlchemyWizard.tsx         # Multi-step alchemy flow
      ConceptChips.tsx          # Selectable concept chips
      RecommendationCard.tsx    # Rec with reason text
    person/
      PersonHeader.tsx          # Image, name, bio
      AnalyticsCharts.tsx       # Ratings, genres, projects-by-year
      Filmography.tsx           # Credits grouped by year
    settings/
      SettingsForm.tsx          # All settings fields
      ExportButton.tsx          # Export My Data
    shared/
      ShowGrid.tsx              # Reusable poster grid
      RemovalConfirmation.tsx   # Status removal dialog
```

---

## 4. Identity & Auth (Benchmark Mode)

### 4.1 Dev Identity Injection
- Middleware reads `X-User-Id` header or falls back to `DEFAULT_USER_ID` env var
- Middleware reads `X-Namespace-Id` header or falls back to `NAMESPACE_ID` env var
- These values are passed to Supabase client context for RLS
- Optional: dev-only user selector dropdown in the UI header

### 4.2 Future OAuth Path
- `user_id` is stored as opaque string throughout
- Replacing dev injection with real OAuth (e.g. Supabase Auth) requires only swapping the middleware identity source, not schema changes

---

## 5. External Catalog Integration (TMDB)

### 5.1 API Wrapper (`lib/catalog/tmdb.ts`)
- Search: `GET /search/multi` — returns movies + TV
- Show detail: `GET /movie/{id}` or `GET /tv/{id}` with `append_to_response=credits,videos,recommendations,similar,watch/providers,images`
- Person detail: `GET /person/{id}` with `append_to_response=combined_credits,images`

### 5.2 Mapper (`lib/catalog/mapper.ts`)
- Converts TMDB response to `Show` type
- Title: movie → `title`, TV → `name`; missing both = reject
- ShowType: inferred from `media_type` or field presence
- Genres: map genre IDs to names via TMDB genre list
- Images: construct full URLs from TMDB base URL + path
- Logo selection: pick highest-rated English logo
- Dates: parse with multiple format support
- Providers: extract by region into `ProviderData` shape

### 5.3 Merge (`lib/catalog/merge.ts`)
- Non-my fields: `selectFirstNonEmpty(newValue, oldValue)` — never overwrite non-empty with empty/null
- My fields: compare update timestamps, keep newer
- `detailsUpdateDate` = now after merge
- `creationDate` only set on first creation

---

## 6. Collection & Business Rules (`lib/business/`)

### 6.1 Save Rules (`save-rules.ts`)
Implements PRD Section 5.2-5.3:
- Setting any status → save to collection
- Choosing Interested/Excited → save with `status=later`, `interest=interested|excited`
- Rating unsaved show → save with `status=done`
- Adding tag to unsaved show → save with `status=later`, `interest=interested`
- Default save: `status=later`, `interest=interested`

### 6.2 Removal (`collection.ts`)
Implements PRD Section 5.4:
- Clearing status triggers confirmation dialog
- On confirm: delete show from DB (clears all My Data)
- Track `statusRemovalCountKey`; after threshold, offer "don't ask again" (`hideStatusRemovalConfirmation`)

### 6.3 Re-add / Merge
Implements PRD Section 5.5:
- If show already exists, preserve latest My Data
- Refresh public metadata via catalog
- Conflicts resolved by most recent timestamp per field

---

## 7. AI System

### 7.1 Prompt Architecture (`lib/ai/prompts.ts`)
All prompts encode the persona from `ai_voice_personality.md`:
- **Shared system prompt**: fun chatty TV/movie nerd friend, spoiler-safe, opinionated, vibe-first
- **Scoop prompt**: structured mini blog post (personal take, stack-up, Scoop centerpiece, fit/warnings, verdict). 150-350 words.
- **Ask prompt**: conversational, bulleted recs, confident picks. Includes user library context.
- **Concepts prompt**: bullet list only, 1-3 words each, evocative, no generic terms, ordered by strength. 8 concepts default.
- **Concept recs prompt**: 5 recs (Explore Similar) or 6 recs (Alchemy), reasons reference selected concepts, bias toward recent shows.

### 7.2 Ask Chat with Mentions (`api/ai/ask/route.ts`)
- Streaming response via Server-Sent Events
- AI returns structured `{ commentary, showList }` where `showList` uses `Title::externalId::mediaType;;` format
- Parser (`lib/ai/parser.ts`) extracts show mentions, resolves via catalog lookup
- If parse fails: retry once with stricter instructions, then fall back to plain text + search handoff
- Context includes: user library (statuses, tags, ratings), conversation history
- After ~10 messages, older turns summarized in-persona to control token depth

### 7.3 Scoop (`api/ai/scoop/route.ts`)
- Streaming response
- Show context (title, overview, genres, ratings) included in prompt
- User library included for taste-awareness
- Response cached: `ai_scoop` + `ai_scoop_update_date` on the show record
- Freshness: regenerate if `ai_scoop_update_date` > 4 hours old
- Only persists if show is in collection

### 7.4 Concepts (`api/ai/concepts/route.ts`)
- Single-show: extract concepts for one show
- Multi-show (Alchemy): extract shared concepts across 2+ shows
- Returns bullet list parsed into array of strings
- Quality rules: specific > generic, diverse axes, strength-ordered

### 7.5 Concept-Based Recommendations (`api/ai/recommendations/route.ts`)
- Input: selected concepts + optional source shows
- Output: 5 (Explore Similar) or 6 (Alchemy) recommendations
- Each rec includes: title, external ID, media type, reason text
- Reasons must name which concepts align
- Resolve each rec against catalog; unresolved shown as non-interactive or handed to search

### 7.6 Conversation Summarization
- When Ask chat exceeds ~10 turns, summarize older turns into 1-2 sentences
- Summary preserves persona tone (not sterile system voice)

---

## 8. Feature Implementation Order

### Phase 1: Foundation
1. Project setup (Next.js, Supabase, env config)
2. Database migrations (shows, cloud_settings, app_metadata tables)
3. Identity middleware (dev injection)
4. Supabase client setup (browser + server)
5. Type definitions

### Phase 2: Catalog + Collection Core
6. TMDB API wrapper
7. Catalog-to-Show mapper + merge logic
8. Show CRUD API routes (`/api/shows`)
9. Business rules (save triggers, defaults, removal)
10. Collection Home page (status-grouped display)
11. Show tile component with badges
12. Sidebar with filters (All Shows, tags, genre, decade, score)
13. Media type toggle (All / Movies / TV)

### Phase 3: Show Detail
14. Show Detail page layout (full section hierarchy)
15. Header carousel (backdrops/posters/logos)
16. Core facts + community score
17. Status chips toolbar + interest mapping
18. Rating bar with auto-save logic
19. Tag picker with auto-save logic
20. Overview section
21. Traditional recommendations strand
22. Streaming availability (providers)
23. Cast & crew (horizontal scrollable)
24. Seasons (TV only)
25. Budget/revenue (movies)
26. Removal confirmation dialog

### Phase 4: Search
27. Find/Discover hub with mode switcher
28. Search page with text input + poster grid results
29. In-collection badge marking on search results
30. Search-on-launch setting

### Phase 5: AI Features
31. AI prompt templates (shared persona + surface-specific)
32. Scoop generation (streaming) + toggle UX
33. Ask chat UI (user/assistant turns, streaming)
34. Ask mentioned shows strip + parser
35. Starter prompts (6 random, refresh)
36. Ask About This Show (seeded context from Detail)
37. Concept extraction (single-show)
38. Explore Similar flow (concepts -> select -> recs)
39. Concept extraction (multi-show for Alchemy)
40. Alchemy wizard (select shows -> conceptualize -> select concepts -> alchemize -> chain)

### Phase 6: Person
41. Person Detail page (image, bio, analytics charts, filmography)
42. Credit navigation (person -> show detail, show detail -> person)

### Phase 7: Settings & Data
43. Settings page (font size, search on launch, username, API keys, AI model)
44. Cloud settings sync (Supabase)
45. Export My Data (JSON zip download)
46. Data model version tracking + migration support

### Phase 8: Polish & Testing
47. Empty states (no collection, no results, no concepts)
48. Filter persistence (lastSelectedFilter in local storage)
49. Status removal confirmation suppression logic
50. Local settings persistence (fontSize, autoSearch)
51. Namespace isolation tests
52. Integration tests for save/remove/merge rules
53. AI output quality validation against discovery quality bar

---

## 9. Data Sync & Conflict Resolution

- All user data stored server-side in Supabase (source of truth)
- Client caching allowed for performance but disposable
- Conflict resolution per field using most recent `*UpdateDate` timestamp
- Cloud settings use `version` (epoch seconds) for conflict resolution
- Clearing local storage must not lose data

---

## 10. Export/Backup

- `GET /api/shows/export` — authenticated endpoint
- Queries all shows for `(namespace_id, user_id)`
- Produces JSON with all Show fields + My Data
- Dates encoded ISO-8601
- Packaged as `.zip` file download
- Import/restore is out of scope (noted as open question)

---

## 11. Key Technical Decisions

| Decision | Rationale |
|----------|-----------|
| Next.js App Router | Required by infra rider; enables server components + API routes |
| Supabase with RLS | Required by infra rider; RLS enforces namespace + user isolation |
| Server-side AI calls | AI API keys stay server-only; streaming via SSE |
| TMDB as catalog | Industry-standard free movie/TV API with rich data |
| Opaque `user_id` string | Future OAuth swap without schema change |
| `namespace_id` on all tables | Build isolation per infra rider |
| Timestamp-based merge | Preserves user edits across sync + catalog refresh |
| Streaming AI responses | Users see progressive output, not blank waits |

---

## 12. Compliance Checklist (Infra Rider)

- [x] `.env.example` with all variables
- [x] `.gitignore` excludes secrets
- [x] One-command dev start (`npm run dev`)
- [x] Test + reset scripts
- [x] Repeatable migrations
- [x] `namespace_id` on all persisted data
- [x] `user_id` on all user-owned records
- [x] Dev identity injection (header or env)
- [x] No Docker requirement
- [x] Destructive tests scoped to namespace
- [x] Schema supports future OAuth without redesign
- [x] Anon key in browser, service role server-only
- [x] Server-side source of truth; local cache disposable
