# Implementation Plan

## 1. Objective

Build a benchmark-compliant personal TV/movie companion that lets users save shows, organize them with statuses/interest/tags/rating, and discover new titles through Search, Ask, Alchemy, and per-show concept exploration.

This plan covers:
- Product behavior from `product_prd.md`
- Execution and isolation constraints from `infra_rider_prd.md`
- AI behavior, concept rules, and quality bar from the supporting docs
- Architectural guidance from `INSTRUCTIONS.md`

This plan does not implement the app. It defines the architecture, workstreams, delivery order, and verification gates.

## 2. Scope Summary

### In scope

- Next.js latest stable application runtime
- Supabase-backed persistence using official client libraries
- Benchmark-friendly identity injection with future OAuth migration path
- Namespace-based run isolation
- Durable server-side storage for user-owned data
- Collection home with filters and grouped status sections
- Global search against an external entertainment catalog
- Show Detail page with My Data, AI Scoop, recommendations, providers, cast/crew, seasons, and budget/revenue
- Ask chat with mentioned-show row and session summarization
- Alchemy multi-show discovery flow
- Explore Similar concept flow from Show Detail
- Person Detail page with filmography and lightweight analytics
- Settings, synced cloud settings, local UI settings, and export/backup
- Deterministic migrations, env setup, tests, and namespace-scoped reset tooling

### Explicitly out of initial implementation scope

- Offline-first support beyond normal failure handling
- Real OAuth in benchmark mode
- Import/Restore from backup zip
- First-class `Next` UI status
- Named custom lists beyond free-form tags
- Persisted Ask or Alchemy history beyond the active session

## 3. Guiding Decisions

### 3.1 Runtime and routing

- Use Next.js App Router as the benchmark runtime.
- Preserve the repo's fractal architecture guidance by making each route own a `features/` subtree, with thin TSX files and logic extracted into hooks/server modules.
- Keep browser code focused on rendering, interaction wiring, and optimistic UI only.
- Put persistence, AI orchestration, external catalog access, export generation, and identity resolution behind server-only modules and route handlers.

### 3.2 Data ownership

- The backend is the source of truth for all durable user-owned data.
- Browser local storage is allowed only for disposable UI state such as font size, search-on-launch, removal-confirmation preferences, and last selected filter.
- Clearing client storage must not lose collection data, settings synced to the backend, or saved AI Scoop content.

### 3.3 Isolation and identity

- Every durable record is scoped by both `namespace_id` and `user_id`.
- `namespace_id` isolates benchmark runs and destructive tests.
- `user_id` represents the logical owner of records and must survive a future migration to real auth without schema redesign.
- Development/test identity injection will be centralized in the Next.js server boundary so future OAuth changes replace identity resolution, not the data model.

### 3.4 Persistence strategy

- Persist saved shows as a full snapshot of catalog fields plus user fields plus AI Scoop metadata.
- This matches the storage reference well, simplifies export, and makes library rendering independent of live catalog round-trips.
- Unsaved detail pages can still fetch live catalog data without persistence.

### 3.5 AI architecture

- Treat AI prompts as versioned product assets with explicit contracts per surface.
- Keep AI outputs structured where the UI depends on machine-readable fields.
- Validate and map all AI-recommended titles back to real catalog items before rendering them as actionable cards.

## 4. Proposed Architecture

## 4.1 Frontend structure

Use `src/app` for routes and keep page-local features co-located.

Illustrative structure:

```text
src/
  app/
    (app)/
      layout.tsx
      page.tsx                          # Collection Home
      find/
        page.tsx
        features/
          FindModeSwitcher/
          SearchMode/
          AskMode/
          AlchemyMode/
      shows/
        [showId]/
          page.tsx
          features/
            HeaderMedia/
            RatingAndStatusBar/
            TagsPanel/
            OverviewAndScoop/
            AskAboutShowCTA/
            RecommendationsStrand/
            ExploreSimilar/
            ProvidersPanel/
            CastAndCrew/
            SeasonsPanel/
            MovieFinancePanel/
      people/
        [personId]/
          page.tsx
          features/
            PersonHero/
            PersonAnalytics/
            FilmographyByYear/
      settings/
        page.tsx
        features/
          AppearanceSettings/
          IdentitySettings/
          AISettings/
          CatalogSettings/
          ExportData/
    api/
      collection/
      shows/
      people/
      ai/
      settings/
      export/
      test/
  components/
  config/
  hooks/
  server/
    identity/
    supabase/
    catalog/
    persistence/
    ai/
    export/
    mappers/
    validation/
  theme/
  utils/
```

### 4.2 Server layers

- `server/identity`: resolves `namespace_id`, `user_id`, environment mode, and dev-only header or cookie overrides.
- `server/supabase`: creates anon and server-only clients, ensuring elevated keys never reach the browser.
- `server/catalog`: wraps search/detail/person/provider calls to the external catalog service.
- `server/persistence`: owns save/remove/merge/filter/export operations against Supabase.
- `server/ai`: owns prompt assembly, context summarization, response parsing, retry logic, and recommendation mapping.
- `server/mappers`: turns DB rows and catalog payloads into UI DTOs with user overlay applied.
- `server/validation`: request/response schemas for route handlers and AI structured outputs.

## 5. Persistence and Data Model

## 5.1 Durable tables

### `saved_shows`

Purpose: one saved movie/TV item per `(namespace_id, user_id, show_id)`, containing the public snapshot plus My Data plus persisted AI Scoop.

Key columns:

| Area | Columns |
|---|---|
| Partitioning | `namespace_id`, `user_id`, `show_id` |
| Identity | `title`, `show_type`, `external_ids` |
| Public metadata | overview, genres, tagline, homepage, language fields, image URLs, community score, popularity, release/air dates, runtime, budget, revenue, TV season/episode fields |
| Provider data | `provider_data` JSONB |
| User data | `my_status`, `my_status_update_date`, `my_interest`, `my_interest_update_date`, `my_tags`, `my_tags_update_date`, `my_score`, `my_score_update_date` |
| AI data | `ai_scoop`, `ai_scoop_update_date` |
| Management | `details_update_date`, `creation_date`, `is_test` |

Constraints:

- Unique key on `(namespace_id, user_id, show_id)`
- Check constraints for allowed status and interest values
- Default empty arrays for tag/language/image list fields where appropriate
- JSONB for provider/external-id payloads

### `cloud_settings`

Purpose: synced settings per `(namespace_id, user_id)`.

Fields:

- `user_name`
- `ai_model`
- `ai_api_key` optional
- `catalog_api_key` optional
- `version` for conflict resolution

Notes:

- If user-entered API keys are stored, they must be server-side only and never committed.
- Encryption-at-rest should be used if the implementation stores secrets in Supabase.

### `app_metadata`

Purpose: track data model version and future migrations.

Fields:

- `namespace_id`
- `data_model_version`

## 5.2 Local-only UI settings

These remain client-local because the product/technical docs treat them as disposable UI state:

- `autoSearch`
- `fontSize`
- `hideStatusRemovalConfirmation`
- `statusRemovalCountKey`
- `lastSelectedFilter`

The implementation must tolerate their absence or reset without affecting durable data.

## 5.3 Merge and save rules

The persistence layer must codify these rules exactly:

1. A show is in the collection when it has a stored record with non-null `my_status`.
2. Setting a status saves the show if needed.
3. Selecting `Interested` or `Excited` saves the show as `Later` with the corresponding interest.
4. Adding a tag to an unsaved show saves it as `Later + Interested`.
5. Rating an unsaved show saves it as `Done`.
6. Clearing status deletes the saved row and therefore clears all My Data and AI Scoop.
7. On catalog refresh, non-user fields merge using first-non-empty semantics.
8. User fields merge by their field-specific update timestamps.
9. `details_update_date` updates on every catalog merge.
10. `creation_date` is set only once, at first save.

## 5.4 Overlay behavior

Every catalog item rendered anywhere must pass through an overlay step:

- Resolve the real show from catalog data or AI mention data.
- Look up an existing saved row for the same `(namespace_id, user_id, show_id)`.
- If found, overlay `my_status`, `my_interest`, `my_tags`, `my_score`, and persisted `ai_scoop`.
- Return the merged DTO to the UI so saved-state badges and edits are consistent everywhere.

## 6. Identity, Isolation, and Security Plan

## 6.1 Identity resolution

Use a single request-scoped resolver with this precedence:

1. Production auth session once real OAuth exists
2. Dev/test injected header or cookie when benchmark mode allows it
3. Environment-configured default `user_id`

The server layer, not browser code, decides the effective identity.

## 6.2 Namespace resolution

Use a stable `namespace_id` for the lifetime of a run:

- Default from environment variables in dev/test
- Optionally override through documented benchmark-only configuration
- Attach it to every durable row and every destructive reset operation

## 6.3 Supabase access policy

- Browser code should not write directly to user-owned tables in benchmark mode.
- All writes should go through Next.js server handlers or server actions so identity injection, validation, and merge logic stay centralized.
- Elevated Supabase credentials remain server-only.
- Future OAuth migration should replace the identity resolver and, optionally, tighten RLS without redesigning tables.

## 7. External Integration Plan

## 7.1 Catalog integration

Capabilities required:

- Search titles by text
- Fetch full show detail
- Fetch streaming/provider data by region
- Fetch cast and crew
- Fetch person detail and filmography
- Fetch traditional recommendations and similar titles

Implementation notes:

- Saved shows should persist enough public metadata for library views.
- Transient fields such as cast, crew, seasons, videos, recommendations, and similar titles can be fetched on demand.
- Mapping logic must normalize movie vs TV payload differences and choose a deterministic best logo where possible.

## 7.2 AI provider integration

Capabilities required:

- Chat completion for Ask
- Concept generation for single-show and multi-show prompts
- Recommendation generation for Explore Similar and Alchemy
- Scoop generation with progressive streaming if feasible

Implementation notes:

- Prompt templates should be stored as product assets with unit tests around parsing and formatting expectations.
- AI output must stay inside the TV/movie domain, remain spoiler-safe by default, and preserve the shared personality across surfaces.

## 8. Feature Plan by Surface

## 8.1 Collection Home

Deliver:

- Filter/navigation panel with:
  - All Shows
  - tag-derived filters
  - `No tags` filter when relevant
  - data filters for genre, decade, and community score
- Media-type toggle for All / Movies / TV
- Grouped sections:
  - Active
  - Excited
  - Interested
  - Other statuses
- Tile badges for in-collection and user rating
- Empty states for empty library and empty filter result

Backend needs:

- Filter aggregate query support
- Section grouping logic based on status plus interest
- Recent-update timestamps available for sorting where needed

## 8.2 Search

Deliver:

- Find hub defaulting to Search or respecting the local `autoSearch` preference
- Live text search against external catalog
- Poster grid results with overlay badges
- Selecting a result opens Show Detail

Backend needs:

- Search endpoint proxy/wrapper
- Overlay of saved state on search results

## 8.3 Show Detail

Preserve the documented narrative order unless intentionally revised later:

1. Header media carousel
2. Core facts and community score
3. My Tags
4. Overview and Scoop
5. Ask about this show CTA
6. Genres and languages
7. Traditional recommendations
8. Explore Similar
9. Streaming availability
10. Cast and Crew
11. Seasons for TV
12. Budget/Revenue for movies

Critical behavior:

- Status chips include Active, Interested, Excited, Done, Quit, Wait
- Interested and Excited map to `Later + Interest`
- Reselecting an active status triggers removal confirmation
- Rating auto-saves unsaved titles as `Done`
- Tagging auto-saves unsaved titles as `Later + Interested`
- Scoop is generated on demand, spoiler-safe, and persisted only if the show is in the collection
- Recommendations and Explore Similar results must resolve to real shows before becoming actionable

## 8.4 Ask

Deliver:

- Chat UI inside Find
- Welcome state with 6 random starter prompts and refresh
- Friendly, opinionated response style
- Mentioned-show strip derived from structured AI output
- Session context retention with summarization after long conversations
- Ask-about-a-show handoff from Detail page

Implementation notes:

- Keep Ask session state ephemeral to the active session
- Structure output as `commentary` plus `showList`
- Retry once on parser failure, then fall back to commentary plus Search handoff

## 8.5 Alchemy

Deliver:

1. Multi-select 2+ input shows from library and catalog
2. Concept generation across all selected titles
3. Concept selection with a max of 8
4. Recommendation output with 6 mapped shows and concept-aware reasons
5. Chaining with “More Alchemy!”

Behavior rules:

- Changing the input selection clears concepts and downstream results
- Results are session-only and not persisted
- Reasons must explicitly mention the selected concepts

## 8.6 Explore Similar

Deliver:

1. Get Concepts from a single show
2. Show concept chips
3. Select 1+ concepts
4. Explore Shows for 5 mapped recommendations

Behavior rules:

- Concepts must be 1-3 words, evocative, spoiler-safe, and not generic
- No recommendation card becomes interactive until it maps to a real catalog item

## 8.7 Person Detail

Deliver:

- Hero area with image gallery, name, and bio
- Filmography grouped by year
- Lightweight analytics:
  - average project ratings
  - top genres
  - projects by year
- Credit selection opens Show Detail

Implementation notes:

- Person data can remain primarily live-fetched rather than durably persisted
- Analytics can be computed on fetched filmography data and existing community metrics

## 8.8 Settings and Your Data

Deliver:

- Font size/readability controls
- Search-on-launch toggle
- Username
- AI provider key input if supported
- AI model selection
- Catalog provider API key input
- Export My Data to a zip containing JSON with ISO-8601 dates
- Import/Restore shown as deferred or omitted, not half-implemented

Implementation notes:

- Synced settings belong in `cloud_settings`
- Pure UI preferences may remain local
- Export should read directly from durable storage for the active `(namespace_id, user_id)`

## 9. AI Contracts and Quality Plan

## 9.1 Shared AI behavior

All AI surfaces must:

- Stay in the TV/movie domain
- Be spoiler-safe by default
- Be opinionated and honest
- Prefer vibe, structure, emotion, and craft over generic genre talk
- Preserve a single consistent persona across Scoop, Ask, Explore Similar, and Alchemy

## 9.2 Surface-specific contracts

- Scoop: mini taste review with personal take, stack-up, emotional centerpiece, fit/warnings, verdict
- Ask: short conversational answer, direct within the first few lines, bullet lists for multiple recs
- Concepts: bullet list only, 1-3 words, evocative, no explanation
- Explore Similar: 5 recs with explicit concept-aware reasons
- Alchemy: 6 recs with explicit concept-aware reasons

## 9.3 Recommendation mapping pipeline

For Ask, Explore Similar, and Alchemy:

1. Parse AI output into candidate titles with external IDs and media types when available.
2. Resolve against the catalog using ID-first lookup.
3. Confirm title match case-insensitively before accepting the result.
4. Overlay saved user data if the show already exists in the collection.
5. If mapping fails, render a non-interactive fallback or hand off to Search.

Real-show integrity is non-negotiable.

## 9.4 Quality bar enforcement

Use the discovery quality doc as a release gate:

- Voice adherence
- Taste alignment
- Surprise without betrayal
- Specificity of reasoning
- Real-show integrity

Practical enforcement:

- Prompt/formatter tests for structured outputs
- Golden scenario fixtures for manual review
- Regression checklist for Scoop, Ask, Concepts, Explore Similar, and Alchemy

## 10. Delivery Phases

## Phase 0: Foundations

- Set up Next.js app shell, theme, shared components, linting, type-checking, and test scaffolding
- Add `.env.example`
- Define server-only env parsing and validation
- Create Supabase migration structure
- Implement identity and namespace resolution helpers

Exit criteria:

- App boots from env configuration only
- Migrations exist
- Namespace and user resolution are documented and testable

## Phase 1: Durable collection core

- Create `saved_shows`, `cloud_settings`, and `app_metadata`
- Implement show snapshot persistence and merge logic
- Implement collection queries, grouping, filters, and tile overlay behavior
- Implement save/remove/status/tag/rating flows

Exit criteria:

- User can build and maintain a collection
- All autosave defaults behave correctly
- Clearing status deletes saved data

## Phase 2: Catalog and detail experience

- Integrate external search and show detail fetching
- Build Search mode
- Build Show Detail in the required narrative order
- Add traditional recommendations, providers, cast/crew, seasons, budget/revenue
- Build Ask-about-this-show handoff plumbing

Exit criteria:

- Search and detail are usable end to end
- Detail page is the single source of truth for editing My Data

## Phase 3: Settings and export

- Implement local settings
- Implement synced cloud settings
- Implement export zip generation with ISO-8601 JSON
- Document backup behavior and benchmark env expectations

Exit criteria:

- Settings persist correctly
- Export works from server data without client-only dependencies

## Phase 4: AI foundation

- Implement AI service abstraction
- Encode shared personality and surface-specific prompt contracts
- Build structured Ask output parsing
- Build concept generation contracts
- Add AI Scoop generation and freshness rules

Exit criteria:

- Ask, Scoop, and Concepts each satisfy their response contract
- Parser and fallback behavior are covered by tests

## Phase 5: Discovery surfaces

- Build Ask UI with starter prompts, mentions strip, and session summarization
- Build Explore Similar flow
- Build Alchemy flow including chaining
- Enforce real-show mapping across all recommendation flows

Exit criteria:

- Discovery flows are usable end to end
- Recommendations are actionable or gracefully fall back

## Phase 6: Person detail and hardening

- Build Person Detail and analytics
- Add benchmark reset tooling
- Add namespace-scoped destructive test support
- Run QA against all key journeys and AI quality gates

Exit criteria:

- Required product journeys are complete
- Benchmark rider requirements are satisfied

## 11. Testing and Verification Strategy

## 11.1 Unit tests

Target the highest-risk pure logic:

- save defaults and auto-save rules
- field-by-field timestamp merge logic
- catalog merge with first-non-empty semantics
- status removal behavior
- filter/grouping logic
- concept selection and downstream reset behavior
- AI parser formatting and retry/fallback behavior
- recommendation mapping validator

## 11.2 Integration tests

Cover server handlers and persistence:

- collection CRUD and overlay behavior
- export generation
- settings persistence
- namespace-scoped reset
- identity injection behavior in benchmark mode

## 11.3 End-to-end tests

Cover the core journeys from the PRD:

- build collection from Search
- rate-to-save
- tag-to-save
- maintain collection from Home to Detail
- Ask discovery to save
- Explore Similar to save
- Alchemy round and chained round
- Person detail navigation
- Export backup

## 11.4 Manual AI review

Use a short human checklist derived from `discovery_quality_bar.md`:

- Does the voice feel consistent and on-brand?
- Are recommendations grounded in the user's taste/context?
- Is there at least some defensible surprise?
- Are reasons specific and concept-aware?
- Does every actionable rec map to a real show?

## 12. Required Repo Deliverables

The finished implementation should include:

- `.env.example` with all required variables and comments
- `.gitignore` excluding secrets
- Scripts for:
  - starting the app
  - running tests
  - resetting namespace-scoped test data
- repeatable migrations
- documentation for benchmark identity injection and namespace usage

Recommended environment variables:

- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- `SUPABASE_SERVICE_ROLE_KEY`
- `APP_NAMESPACE_ID`
- `APP_DEFAULT_USER_ID`
- `APP_ENVIRONMENT`
- `CATALOG_API_KEY`
- `AI_API_KEY`
- `AI_MODEL`
- `DEFAULT_REGION`

## 13. Risks and Open Questions

## Documentation gap

`product_prd.md` references companion docs that are not present in `docs/prd/`. The implementation should follow the available AI voice, prompting, concept, and detail-experience specs, but this missing material is still a product-risk note.

## Product open questions to defer unless clarified

- Whether `Next` should become a first-class visible status
- Whether AI Scoop generation on an unsaved show should implicitly save it
- Whether clearing a rating should store explicit `Unrated` versus null
- Whether named custom lists should exist beyond tags
- When Import/Restore should be implemented

## Delivery risks

- AI outputs may drift from the required voice or structure without prompt regression checks.
- Recommendation mapping can fail unless ID-first validation is strict.
- Provider, cast, and person payloads differ across movies and TV and need careful normalization.
- Namespace-scoped destructive testing must never overreach and delete outside the active run.
- Storing user-entered API keys requires clear security boundaries and documentation.

## 14. Definition of Done

The implementation is done when:

- The app satisfies the core product journeys in the PRD.
- Durable user data is fully scoped by `namespace_id` and `user_id`.
- The backend remains the source of truth.
- The repo runs from environment configuration without code edits.
- Tests and reset tooling support repeatable benchmark runs.
- AI discovery surfaces meet their output contracts and the discovery quality bar.
