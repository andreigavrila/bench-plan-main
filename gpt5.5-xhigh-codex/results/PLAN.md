# Implementation Plan

## 1. Scope and Product Reading

Build a personal TV and movie companion that lets each user maintain their own overlay on top of public catalog data, then uses that taste profile for search, AI chat, concept-based discovery, and per-show recommendations.

Documents read for this plan:

- `docs/prd/product_prd.md`
- `docs/prd/infra_rider_prd.md`
- `docs/prd/supporting_docs/ai_voice_personality.md`
- `docs/prd/supporting_docs/ai_prompting_context.md`
- `docs/prd/supporting_docs/concept_system.md`
- `docs/prd/supporting_docs/detail_page_experience.md`
- `docs/prd/supporting_docs/discovery_quality_bar.md`
- `docs/prd/supporting_docs/technical_docs/storage-schema.md`
- `docs/prd/supporting_docs/technical_docs/storage-schema.ts`
- `INSTRUCTIONS.md`

This is a planning-only deliverable. No application source files should be created until implementation begins.

## 2. Core Decisions and Assumptions

1. Use Next.js with the App Router, TypeScript, and React for the application runtime.
2. Use Supabase as the persistence layer through official Supabase client libraries.
3. Do not require Docker. Hosted Supabase is the primary path; local Supabase can be optional documentation later.
4. Store all user-owned records with both `namespace_id` and `user_id`. Treat the effective data boundary as `(namespace_id, user_id)`.
5. Use a development identity provider in benchmark/dev mode:
   - `APP_NAMESPACE_ID` defines the run namespace.
   - `DEFAULT_USER_ID` defines the default dev user.
   - `X-User-Id` may override the user only in development/test.
   - Production mode must disable header-based identity injection.
6. Keep the backend as source of truth. Client storage may cache UI state, but clearing browser storage must not delete the library.
7. Use a catalog adapter abstraction with an initial TMDB-compatible implementation because the PRD field set maps naturally to TMDB-style movies, TV, credits, providers, videos, and people.
8. Use an AI provider abstraction with an OpenAI-compatible first implementation. API keys and model names come from environment variables first; user-entered key storage is optional and must be encrypted/server-only if implemented.
9. Persist `next` as a possible status but do not expose it as a first-class UI status unless a later product decision promotes it.
10. Import/Restore is an optional extension. Implement Export/Backup first.

## 3. Target Architecture

### 3.1 Application Layers

- UI: Next.js route pages and feature components.
- Feature logic: colocated hooks and utilities per page/feature, following the fractal structure in `INSTRUCTIONS.md`.
- Server boundary: route handlers/server actions for catalog, AI, collection, settings, export, and test reset operations.
- Domain services: pure business logic for save defaults, merge rules, filters, grouping, AI parsing, and export serialization.
- Persistence: Supabase migrations, tables, indexes, and server-only repository functions.
- Integrations: catalog provider adapter and AI provider adapter.

### 3.2 Directory Shape

Use the repo's fractal pattern and avoid `index.tsx`:

```text
src/
  app/
    layout.tsx
    page.tsx
    discover/
      page.tsx
    show/
      [mediaType]/
        [externalId]/
          page.tsx
    person/
      [personId]/
        page.tsx
    settings/
      page.tsx
    api/
      catalog/
      ai/
      collection/
      settings/
      export/
      test/
  components/
  config/
  domain/
    shows/
    collection/
    ai/
    filters/
    export/
  integrations/
    catalog/
    ai/
    supabase/
  pages/
    HomePage/
    DiscoverPage/
    ShowDetailPage/
    PersonDetailPage/
    SettingsPage/
  theme/
  utils/
```

Each page directory contains `features/FeatureName/FeatureName.tsx`, local hooks, local constants, and local utilities. TSX files should stay humble: markup and bindings only, with business behavior moved into hooks and domain utilities.

### 3.3 Server Boundary

The browser should not write directly to Supabase tables in the benchmark implementation. Client components call Next.js server routes/actions; server code injects `namespace_id` and `user_id`, validates payloads, and uses the Supabase client.

This keeps benchmark identity explicit while preserving a clean path to real OAuth later. When OAuth is added, the identity provider changes, but table keys and repository methods remain stable.

## 4. Environment, Scripts, and Repo Deliverables

### 4.1 Required Environment Variables

Create `.env.example` with comments for:

- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- `SUPABASE_SERVICE_ROLE_KEY` server-only, optional for migrations/admin/test reset
- `APP_NAMESPACE_ID`
- `DEFAULT_USER_ID`
- `ENABLE_DEV_IDENTITY_HEADER`
- `CATALOG_API_KEY`
- `CATALOG_PROVIDER`
- `CATALOG_DEFAULT_REGION`
- `AI_PROVIDER`
- `AI_API_KEY`
- `AI_MODEL`
- `AI_BASE_URL` optional for compatible providers
- `SETTINGS_ENCRYPTION_KEY` only if user-entered synced API keys are stored

Ensure `.gitignore` excludes `.env*` but allows `.env.example`.

### 4.2 Required Scripts

Add package scripts during implementation:

- `npm run dev`: start Next.js locally.
- `npm run build`: production build.
- `npm run lint`: lint and type-aware checks.
- `npm test`: unit and integration tests.
- `npm run test:e2e`: Playwright journey tests.
- `npm run test:reset -- --namespace <id>`: delete test data only inside one namespace.
- `npm run db:migrate`: apply Supabase migrations.
- `npm run db:types`: generate database TypeScript types.

### 4.3 Migration Artifacts

Use `supabase/migrations/` as the repeatable schema source. Include seed/fixture scripts only for deterministic development and tests. Test reset must be namespace-scoped and must never require global database teardown.

## 5. Data Model and Persistence Plan

### 5.1 Tables

Use these core Supabase tables:

#### `saved_shows`

Purpose: canonical saved show rows containing public catalog fields, user overlay, AI scoop, and provider data.

Key columns:

- `namespace_id text not null`
- `user_id text not null`
- `show_id text not null`
- `title text not null`
- `show_type text not null check in ('movie','tv','person','unknown')`
- `external_ids jsonb`
- public catalog fields from the storage schema: overview, genres, tagline, homepage, languages, image URLs, vote metrics, dates, runtime, TV fields, budget/revenue, provider data
- user fields: `my_tags text[]`, `my_score numeric`, `my_status text`, `my_interest text`
- user timestamp fields: `my_tags_update_date`, `my_score_update_date`, `my_status_update_date`, `my_interest_update_date`
- AI fields: `ai_scoop text`, `ai_scoop_update_date timestamptz`
- management fields: `details_update_date`, `creation_date`, `is_test`

Primary key: `(namespace_id, user_id, show_id)`.

Indexes:

- `(namespace_id, user_id, my_status)`
- GIN index on `my_tags`
- GIN index on `genres`
- expression/index support for decade and community score filters if needed
- `(namespace_id, user_id, details_update_date)`

#### `user_settings`

Purpose: synced settings and preferences.

Columns:

- `namespace_id`
- `user_id`
- `user_name`
- `font_size`
- `auto_search`
- `ai_model`
- encrypted optional `catalog_api_key`
- encrypted optional `ai_api_key`
- `settings_version`
- `updated_at`

Primary key: `(namespace_id, user_id)`.

For the first benchmark implementation, prefer environment API keys and leave synced key storage behind an explicit encrypted path.

#### `app_metadata`

Purpose: track data model version per namespace.

Columns:

- `namespace_id`
- `data_model_version`
- `updated_at`

Primary key: `namespace_id`.

#### Optional `ui_preferences`

Purpose: sync or store non-critical UI choices if desired.

Columns:

- `namespace_id`
- `user_id`
- `hide_status_removal_confirmation`
- `status_removal_count`
- `last_selected_filter jsonb`
- `updated_at`

These preferences can also be local client settings because they are not the user's entertainment library. The saved library must remain server-side.

### 5.2 ID Strategy

Use a canonical show id that avoids movie/TV collisions:

```text
tmdb:movie:<id>
tmdb:tv:<id>
```

Store catalog provider ids in `external_ids`, for example:

```json
{
  "tmdb": "123",
  "imdb": "tt1234567"
}
```

AI recommendations can resolve by external id first and title/media type second.

### 5.3 Collection Membership and Save Rules

Implement collection membership as `my_status is not null`.

Saving triggers:

- Setting any status saves the show.
- Choosing Interested or Excited saves the show as `my_status = later` and sets `my_interest`.
- Rating an unsaved show saves it as `done`.
- Adding at least one tag to an unsaved show saves it as `later` and `interested`.

Default save behavior:

- Generic save: `later` + `interested`.
- Rating-first save: `done`.
- Tag-first save: `later` + `interested`.

Removal:

- Reselecting an active status asks for confirmation unless the user has suppressed it.
- Removing status deletes the saved show row and clears all My Data and persisted AI scoop.
- If implementation needs an audit trail later, add a separate history table; do not leave a row that appears in collection.

### 5.4 Merge and Conflict Rules

Implement pure functions for merge behavior:

- Public catalog fields use `selectFirstNonEmpty(newValue, oldValue)`.
- Never overwrite non-empty stored strings/arrays with empty values.
- Never overwrite stored non-null values with null.
- User fields resolve by their corresponding update timestamps.
- If only one side has an update timestamp, keep that side.
- `creation_date` is set once.
- `details_update_date` updates whenever public details are refreshed.
- User edits always win over catalog refreshes.

Unit tests must cover every merge branch.

### 5.5 Data Continuity

Every schema change must ship as a migration. Migrations must preserve saved shows, statuses, interest, tags, ratings, and AI scoop. Add migration tests with representative rows before any data model change.

## 6. Catalog Integration Plan

### 6.1 Adapter Interface

Create a provider-neutral interface:

- `searchShows(query, mediaType?)`
- `getShowDetails(mediaType, externalId)`
- `getShowCredits(mediaType, externalId)`
- `getShowImages(mediaType, externalId)`
- `getShowVideos(mediaType, externalId)`
- `getSimilarShows(mediaType, externalId)`
- `getRecommendedShows(mediaType, externalId)`
- `getWatchProviders(mediaType, externalId, region)`
- `getPersonDetails(personId)`
- `getPersonCredits(personId)`
- `resolveRecommendation({ title, externalId, mediaType })`

### 6.2 Normalization

Normalize every catalog payload into the domain `Show` shape:

- Reject entries without a usable title/name.
- Infer media type only when catalog media type is missing.
- Map genre ids to display names.
- Convert image paths to full renderable URLs.
- Choose one deterministic best logo, preferring English where available.
- Store provider ids only in `provider_data`.
- Keep credits, seasons, images, videos, similar, recommendations, and person details transient unless the user saves the show.

### 6.3 API Routes

Use server routes to hide catalog keys:

- `GET /api/catalog/search`
- `GET /api/catalog/show/:mediaType/:externalId`
- `GET /api/catalog/show/:mediaType/:externalId/credits`
- `GET /api/catalog/show/:mediaType/:externalId/recommendations`
- `GET /api/catalog/show/:mediaType/:externalId/providers`
- `GET /api/catalog/person/:personId`
- `POST /api/catalog/resolve`

## 7. AI and Discovery Plan

### 7.1 Shared AI Infrastructure

Create an AI service with:

- Provider abstraction.
- Prompt/context builders by surface.
- Structured output validators.
- Retry-on-parse-failure once for strict formats.
- Domain guardrails for TV/movie scope.
- Library context assembler that summarizes saved shows with status, interest, tags, rating, and notable AI scoop when useful.
- Recommendation resolver that maps AI output to real catalog entries.

All AI surfaces must share the same persona: warm, chatty, opinionated, spoiler-safe, specific, and honest.

### 7.2 Ask

Behavior:

- Session-only chat state, cleared on reset/leaving Ask.
- General Ask from Discover starts without a show.
- Ask About This Show starts Ask with the current show context.
- Older turns summarize after roughly 10 messages into 1-2 persona-preserving sentences.
- Multi-recommendation replies use scannable bullets.
- The first answer should be direct within the first few lines.

Structured mentions:

- AI response contains user-facing `commentary`.
- AI response contains `showList` formatted exactly as `Title::externalId::mediaType;;Title2::externalId::mediaType`.
- The UI renders a mentioned-shows strip from resolved real catalog items.
- If resolution fails, show a non-interactive title or hand off to Search.

### 7.3 Scoop

Behavior:

- Available on Show Detail.
- Spoiler-safe mini taste review, roughly 150-350 words.
- Must include personal take, honest stack-up, Scoop centerpiece, fit/warnings, and verdict.
- Stream progressively where possible.
- Cached for 4 hours when the show is saved.
- Unsaved show scoop can be generated ephemerally but should not persist unless the show is later saved.

### 7.4 Concepts

Behavior:

- Generate 8 concepts by default.
- Bullet list only.
- Each concept is 1-3 words.
- Concepts are spoiler-free, specific, evocative, and varied across structure, tone, emotion, relationships, and craft.
- Multi-show Alchemy concepts must represent commonality across all input shows.

### 7.5 Explore Similar

Flow:

1. User opens Show Detail.
2. User selects Get Concepts.
3. User selects one or more concept chips, capped consistently with Alchemy.
4. User selects Explore Shows.
5. AI returns 5 recommendations.
6. Each recommendation resolves to a real catalog item where possible and includes a concept-specific reason.

### 7.6 Alchemy

Flow:

1. User selects 2 or more starting shows from library and global catalog.
2. User selects Conceptualize Shows.
3. User selects 1-8 concept catalysts.
4. User selects Alchemize.
5. AI returns 6 real-show recommendations with short reasons tied to selected concepts.
6. User can choose More Alchemy to start another round with results as inputs.

Rules:

- Changing starting shows clears concepts and results.
- Changing selected concepts clears downstream results.
- Alchemy sessions are session-only and not persisted.

### 7.7 Discovery Quality Validation

Add a lightweight AI quality harness with human-reviewable fixtures:

- Voice adherence.
- Taste alignment.
- Surprise without betrayal.
- Specific reasoning.
- Real-show integrity.

Automated tests should verify structure, parser behavior, and catalog resolution. Human/manual review should score output quality using the 0-2 rubric in the PRD.

## 8. UI and Feature Plan

### 8.1 Global Layout

Create a persistent app shell:

- Left navigation/filter panel on desktop.
- Mobile-friendly drawer or tab navigation.
- Main content area for Home, Discover, Show Detail, Person Detail, and Settings.
- Persistent Find/Discover entry point.
- Persistent Settings entry point.

Use design tokens for spacing, color, type, and radii. Keep cards to repeated items and framed tools; do not nest cards inside cards.

### 8.2 Collection Home

Features:

- Fetch saved shows for `(namespace_id, user_id)`.
- Apply selected sidebar filter.
- Apply media type toggle: All, Movies, TV.
- Group into:
  1. Active
  2. Excited (`later` + `excited`)
  3. Interested (`later` + `interested`)
  4. Other statuses: Wait, Quit, Done, and unclassified Later
- Active uses more prominent tiles.
- Tiles show poster, title, collection badge, and user rating badge.

Filters:

- All Shows.
- One filter per tag.
- No Tags if any tagless saved show exists.
- Genre.
- Decade.
- Community score ranges.
- Media type toggle composes with the active filter.

Empty states:

- Empty collection: prompt to Search or Ask.
- Empty filter result: "No results found."

### 8.3 Discover Hub

Use a mode switcher for:

- Search.
- Ask.
- Alchemy.

Search:

- Text query against external catalog.
- Poster grid.
- In-collection items display the user-overlaid version and badge.
- Selecting a show opens Detail.
- If Search on Launch is enabled, open Discover/Search on startup.

Ask:

- Welcome view with 6 random starter prompts and refresh.
- Chat transcript.
- Mentioned-shows horizontal strip.
- Detail handoff for resolved shows.

Alchemy:

- Starting show picker supporting saved library and global catalog search.
- Concept generation step.
- Concept chip selection with max 8.
- Results list/grid with reasons and selectable show tiles.
- More Alchemy chaining.

### 8.4 Show Detail Page

Preserve the required narrative hierarchy:

1. Header media carousel: backdrops, posters, logos, trailers when available.
2. Core facts row: year, runtime or seasons/episodes, community score.
3. My Tags.
4. Overview and Scoop toggle/stream.
5. Ask About This Show CTA.
6. Genres and languages.
7. Traditional recommendations strand.
8. Explore Similar.
9. Streaming availability.
10. Cast and Crew.
11. Seasons for TV.
12. Budget/Revenue for movies.

Relationship controls:

- Status/interest chips live in the toolbar, not buried in the scroll body.
- Chips: Active, Interested, Excited, Done, Quit, Wait.
- Interested maps to `later` + `interested`.
- Excited maps to `later` + `excited`.
- Reselecting the active status starts the removal confirmation flow.
- Rating control auto-saves unsaved shows as Done.
- Tag picker auto-saves unsaved shows as Later + Interested.

Critical states:

- No trailer/backdrop: premium poster/logo fallback.
- Unsaved show: My Data controls still work and trigger save rules.
- No concepts: only Get Concepts CTA is shown.
- TV/movie-specific data appears only when relevant.

### 8.5 Person Detail

Features:

- Person image gallery.
- Name and bio.
- Filmography grouped by year.
- Cast/crew credits open Show Detail.
- Lightweight analytics charts:
  - average project ratings,
  - top genres,
  - projects by year.

Credits remain transient catalog data unless the user saves a show from the filmography.

### 8.6 Settings and Your Data

Settings:

- Username.
- Font size/readability.
- Search on Launch.
- AI model selection.
- AI provider key entry if encrypted storage is implemented; otherwise explain env-based benchmark configuration.
- Catalog provider key entry if encrypted storage is implemented; otherwise env-based benchmark configuration.

Your Data:

- Export My Data creates a `.zip` containing JSON backup of all saved shows and My Data for the current `(namespace_id, user_id)`.
- Dates encoded ISO-8601.
- Do not implement Import/Restore in the first pass unless scope expands.

## 9. Business Logic Modules

Implement and unit test pure modules before wiring UI:

- `applySaveTrigger`
- `setStatus`
- `setInterestChip`
- `setRating`
- `setTags`
- `removeFromCollection`
- `mergeCatalogShowWithStoredShow`
- `resolveUserFieldByTimestamp`
- `groupCollectionByStatus`
- `buildAvailableFilters`
- `applyCollectionFilter`
- `parseMentionedShows`
- `parseConceptList`
- `parseRecommendationList`
- `isScoopFresh`
- `serializeExportSnapshot`

These modules are the highest-value test targets because they encode the PRD's implicit behaviors.

## 10. Testing Plan

### 10.1 Unit Tests

Cover:

- Save defaults for status, interest, rating, and tags.
- Interested/Excited mapping to Later plus interest.
- Removing status clears collection membership and My Data.
- Timestamp-based conflict resolution.
- Public catalog merge never overwrites stored values with empty/null.
- Filter generation for tags, No Tags, genre, decade, community score.
- Status grouping order.
- Media type toggle composition.
- AI mention parser exact format.
- Concept parser: bullet-only, 1-3 word validation.
- Scoop freshness window.
- Export JSON date serialization.

### 10.2 Integration Tests

Cover:

- Supabase CRUD scoped by namespace and user.
- Test reset deletes only the requested namespace.
- Server routes inject identity consistently.
- Catalog normalization for movie, TV, and person payloads.
- Recommendation resolution by external id and title/media type.
- AI parser retry path and fallback path.
- Settings read/write and version conflict behavior.

### 10.3 E2E Tests

Use Playwright against a test namespace:

1. Search for a show, open Detail, set Interested, verify Home grouping.
2. Rate an unsaved show, verify it saves as Done.
3. Add a tag to an unsaved show, verify it saves as Later + Interested and tag filter appears.
4. Remove a status, confirm warning, verify show leaves collection.
5. Ask for recommendations, verify mentioned shows strip resolves at least one item.
6. Generate Scoop on a saved show, reload, verify cached scoop.
7. Explore Similar: Get Concepts, select concepts, get 5 recommendations.
8. Alchemy: select 2+ shows, conceptualize, select catalysts, get 6 recommendations, chain.
9. Person Detail: open cast member, inspect credits, open a credit.
10. Export data and verify zip contains ISO-8601 JSON for current user only.

### 10.4 Visual and Accessibility Checks

- Responsive screenshots for Home, Discover modes, Detail, Person, and Settings.
- Keyboard navigation for mode switchers, chips, chat input, and carousels.
- Accessible labels for icon-only controls.
- Contrast and text overflow checks across font-size settings.

## 11. Implementation Milestones

### Milestone 0: Project Foundation

Deliver:

- Next.js app scaffold.
- TypeScript, linting, formatting, test runner, Playwright.
- Theme tokens and shared UI primitives.
- `.env.example`, `.gitignore`, scripts.
- Supabase client setup.

Acceptance:

- `npm run dev`, `npm run build`, `npm run lint`, and `npm test` run.
- No source code requires hardcoded credentials.

### Milestone 1: Supabase Schema and Identity Boundary

Deliver:

- Supabase migrations for `saved_shows`, `user_settings`, `app_metadata`, and optional `ui_preferences`.
- Server identity resolver for namespace/user.
- Repository layer that requires namespace and user for every user-owned operation.
- Namespace-scoped reset script.

Acceptance:

- Tests prove namespace isolation and user isolation.
- Test reset cannot delete data outside the target namespace.

### Milestone 2: Domain Logic

Deliver:

- Pure business logic modules for save triggers, merge rules, grouping, filters, and export serialization.
- Unit tests for PRD edge cases.

Acceptance:

- Save, remove, merge, filter, and grouping behavior matches the PRD.

### Milestone 3: Catalog Integration

Deliver:

- Catalog adapter interface.
- TMDB-compatible adapter.
- Search, detail, credits, providers, recommendations, person endpoints.
- Normalization to domain `Show`.

Acceptance:

- Search and detail payloads normalize consistently.
- Existing saved shows render with My Data overlay after catalog refresh.

### Milestone 4: Collection Home and Search

Deliver:

- App shell/navigation.
- Home grouped collection view.
- Sidebar filters and media type toggle.
- Search mode in Discover.
- Show tiles and in-collection/rating badges.

Acceptance:

- User can search, open a show, save it, and see it grouped correctly on Home.

### Milestone 5: Show Detail and My Data Controls

Deliver:

- Detail page narrative hierarchy.
- Header media fallback behavior.
- Status/interest toolbar.
- Rating and tag controls.
- Traditional recommendations strand.
- Providers, cast/crew, seasons, and financial sections.

Acceptance:

- Rating/tag/status save triggers behave correctly for saved and unsaved shows.
- Removing status clears collection membership and My Data.

### Milestone 6: AI Scoop and Ask

Deliver:

- AI provider abstraction.
- Shared persona/context builders.
- Scoop streaming and 4-hour saved-show cache.
- Ask chat with session state, starter prompts, show handoff, summarization, structured mentions, and catalog resolution.

Acceptance:

- Scoop feels on-voice and caches only when allowed.
- Ask recommendations produce a mentioned-shows row with real resolved items when possible.

### Milestone 7: Concepts, Explore Similar, and Alchemy

Deliver:

- Concept generation.
- Explore Similar flow.
- Alchemy flow.
- Recommendation resolution and fallback UI.
- Chaining for Alchemy.

Acceptance:

- Concepts are 1-3 word evocative chips.
- Explore Similar returns 5 recommendations.
- Alchemy returns 6 recommendations.
- Reasons explicitly reference selected concepts.

### Milestone 8: Person Detail, Settings, and Export

Deliver:

- Person detail with charts and filmography.
- Settings page.
- Export My Data zip.
- Optional encrypted synced API key storage if time allows.

Acceptance:

- Export contains only current `(namespace_id, user_id)` saved data.
- Settings persist without client-only dependence for user-owned data.

### Milestone 9: Hardening and Benchmark Readiness

Deliver:

- E2E coverage for key journeys.
- Visual regression screenshots.
- AI quality review fixtures.
- Documentation for environment setup, dev identity, test reset, and optional local Supabase.

Acceptance:

- Build is repeatable in a fresh namespace.
- No Docker requirement.
- No secret committed.
- Clearing browser storage does not lose saved shows.

## 12. Risk Register

| Risk | Mitigation |
| --- | --- |
| AI returns malformed structured mentions or recommendations | Validate output, retry once with stricter instructions, fall back to commentary plus Search handoff. |
| AI recommends hallucinated or mismatched titles | Require catalog resolution by external id and case-insensitive title/media type check before rendering as selectable. |
| Namespace isolation is missed in one route | Centralize identity resolution and repository constructors; add integration tests that create two namespaces and verify no cross-read/write. |
| User API keys are exposed to client code | Prefer env keys for benchmark; if user-entered storage is added, encrypt server-side and never expose elevated keys. |
| Public catalog refresh overwrites user edits | Keep merge logic pure and heavily tested; never mutate My Data in catalog normalization. |
| Detail page becomes too busy | Preserve narrative hierarchy and keep primary relationship controls in the toolbar; move long-tail detail down-page. |
| AI voice drifts across surfaces | Centralize persona rules and add human-review fixtures using the discovery quality rubric. |
| Test reset deletes production-like data | Require explicit namespace argument, reject empty/default production namespace, and scope SQL deletes by namespace. |

## 13. Open Questions to Defer

- Whether `next` should become a first-class UI status.
- Whether users need named custom lists beyond tags.
- Whether generating Scoop on an unsaved show should save the show.
- Whether clearing My Rating should store explicit Unrated rather than null.
- Whether Import/Restore should ship alongside Export.
- Whether Alchemy sessions should be saved or shared.
- Whether explicit myStatus sidebar filters should be promoted beyond the current grouped Home view.

The implementation should leave room for these decisions without blocking the required benchmark scope.
