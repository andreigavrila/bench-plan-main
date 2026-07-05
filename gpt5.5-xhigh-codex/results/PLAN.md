# Implementation Plan

## 1. Objective

Build a Next.js and Supabase application for a personal TV and movie companion that lets users maintain a durable collection, overlay personal data on catalog items, and use taste-aware AI discovery through Search, Ask, Alchemy, Explore Similar, and AI Scoop.

The implementation must satisfy three non-negotiable constraints:

1. User-owned persisted data is always scoped by `(namespace_id, user_id)`.
2. Supabase is the backend source of truth; browser/local storage is disposable.
3. Every surface that displays a saved show must display the user's overlaid version of that show, with user data winning over catalog refreshes.

This plan intentionally does not implement product code. It is the build plan for the application.

## 2. Source Documents Reviewed

- `docs/prd/product_prd.md`
- `docs/prd/infra_rider_prd.md`
- `docs/prd/supporting_docs/ai_voice_personality.md`
- `docs/prd/supporting_docs/ai_prompting_context.md`
- `docs/prd/supporting_docs/detail_page_experience.md`
- `docs/prd/supporting_docs/concept_system.md`
- `docs/prd/supporting_docs/discovery_quality_bar.md`
- `docs/prd/supporting_docs/technical_docs/storage-schema.md`
- `docs/prd/supporting_docs/technical_docs/storage-schema.ts`
- `INSTRUCTIONS.md`

## 3. Technical Baseline

Use the benchmark-required stack:

- Next.js latest stable, App Router, TypeScript.
- Supabase as persistence, accessed through official Supabase client libraries.
- Server route handlers and server actions as the controlled backend boundary.
- Browser/client code may use the Supabase anon key only. Any elevated key, if needed for namespace reset or migration tooling, must stay server-side or script-only.
- No Docker requirement. Hosted Supabase is the primary path; local Supabase can be optional.

Recommended supporting libraries:

- Zod for request/response validation and parsing AI structured output.
- TanStack Query or equivalent client cache for interactive client state, with server data remaining canonical.
- React Hook Form for settings/tag entry forms if form complexity grows.
- Playwright for end-to-end and visual smoke tests.
- Vitest or Jest plus Testing Library for unit and component tests.
- JSZip or equivalent for export zip generation.

## 4. Repository Deliverables

Create or maintain these top-level implementation deliverables:

- `.env.example`
  - Lists required environment variables with short comments.
  - Must include Supabase URL and anon key, namespace, default user identity, catalog key, AI key/model defaults, and any optional reset/admin secret.
- `.gitignore`
  - Excludes `.env*` secrets while allowing `.env.example`.
- `package.json`
  - Scripts for app start, tests, lint/build, database migrations, and namespace reset.
- `supabase/migrations/`
  - Repeatable schema evolution artifacts.
- `scripts/reset-namespace.*`
  - Deletes only records for the selected namespace.
- `README.md`
  - Local setup, hosted Supabase setup, benchmark identity injection, reset procedure, and test commands.

Required script shape:

- `npm run dev` - starts the Next.js app.
- `npm test` - runs unit/component tests.
- `npm run test:e2e` - runs browser journeys.
- `npm run test:reset -- --namespace <id>` - clears test data for one namespace only.
- `npm run db:migrate` - applies Supabase migrations to the configured database.

## 5. Environment and Identity Model

Define the environment contract before feature work.

Required variables:

- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- `APP_NAMESPACE_ID`
- `DEFAULT_USER_ID`
- `CATALOG_API_KEY`
- `AI_PROVIDER`
- `AI_API_KEY`
- `AI_MODEL`

Optional variables:

- `SUPABASE_SERVICE_ROLE_KEY` for server-only reset/migration utilities.
- `DEV_IDENTITY_ENABLED=true` for benchmark/dev identity injection.
- `NEXT_PUBLIC_DEFAULT_REGION=US` for provider availability.

Identity rules:

- `namespace_id` is stable for the lifetime of a run/build and is not presented as a user concept.
- `user_id` is an opaque stable string.
- In benchmark mode, resolve identity from a dev-only source in this order:
  1. `X-User-Id` header in server route tests.
  2. Dev-only user selector if enabled.
  3. `DEFAULT_USER_ID`.
- Gate dev identity injection behind `DEV_IDENTITY_ENABLED` and never allow arbitrary header identity in production.
- All server data access helpers must require both namespace and user where user-owned data is involved.

## 6. Architecture

Use a feature-first, fractal structure from `INSTRUCTIONS.md`. Avoid `index.tsx`; main files match their directory names.

Suggested layout:

```text
src/
  app/
    layout.tsx
    page.tsx
    find/page.tsx
    shows/[showType]/[id]/page.tsx
    people/[id]/page.tsx
    settings/page.tsx
    api/
      ai/
      catalog/
      library/
      settings/
      export/
      admin/
  components/
  config/
  hooks/
  lib/
    ai/
    catalog/
    identity/
    supabase/
    validation/
  pages/
    HomePage/
    FindPage/
    ShowDetailPage/
    PersonDetailPage/
    SettingsPage/
  theme/
  utils/
```

Feature directories follow this shape:

```text
pages/ShowDetailPage/
  ShowDetailPage.tsx
  hooks/
  utils/
  features/
    HeaderMedia/
      HeaderMedia.tsx
    RelationshipToolbar/
      RelationshipToolbar.tsx
      hooks/
    ScoopPanel/
      ScoopPanel.tsx
    ExploreSimilar/
      ExploreSimilar.tsx
```

Component rules:

- TSX files bind data and render UI only.
- Feature logic lives in hooks and local utilities.
- Shared pure business logic lives in `src/lib` or `src/utils`.
- Constants live in `src/config` or feature-local `constants.ts`.
- Theme tokens own colors, spacing, type, and responsive values. Avoid magic numbers and inline styles in TSX.

## 7. Data Model

Implement a Supabase schema that preserves the conceptual `Show` shape while separating catalog snapshots from user overlays. This makes multi-user support and conflict resolution straightforward.

Core tables:

### 7.1 `catalog_shows`

Stores namespace-scoped catalog snapshots.

Important columns:

- `namespace_id text not null`
- `show_id text not null`
- `show_type text not null check in ('movie', 'tv', 'person', 'unknown')`
- `title text not null`
- `external_ids jsonb`
- `overview text`
- `genres text[] not null default '{}'`
- `tagline text`
- `homepage text`
- `original_language text`
- `spoken_languages text[] not null default '{}'`
- `languages text[] not null default '{}'`
- `poster_url text`
- `backdrop_url text`
- `logo_url text`
- `network_logos text[] not null default '{}'`
- `vote_average numeric`
- `vote_count integer`
- `popularity numeric`
- `release_date timestamptz`
- `first_air_date timestamptz`
- `last_air_date timestamptz`
- `runtime integer`
- `budget bigint`
- `revenue bigint`
- `series_status text`
- `number_of_episodes integer`
- `number_of_seasons integer`
- `episode_run_time integer[] not null default '{}'`
- `last_episode_run_time integer`
- `provider_data jsonb`
- `details_update_date timestamptz`
- `creation_date timestamptz not null default now()`
- `is_test boolean not null default false`

Primary key:

- `(namespace_id, show_id)`

### 7.2 `user_show_overlays`

Stores collection membership and My Data.

Important columns:

- `namespace_id text not null`
- `user_id text not null`
- `show_id text not null`
- `my_status text null check in ('active', 'next', 'later', 'done', 'quit', 'wait')`
- `my_status_update_date timestamptz`
- `my_interest text null check in ('excited', 'interested')`
- `my_interest_update_date timestamptz`
- `my_score numeric`
- `my_score_update_date timestamptz`
- `my_tags text[] not null default '{}'`
- `my_tags_update_date timestamptz`
- `ai_scoop text`
- `ai_scoop_update_date timestamptz`
- `creation_date timestamptz not null default now()`
- `is_test boolean not null default false`

Primary key:

- `(namespace_id, user_id, show_id)`

Foreign key:

- `(namespace_id, show_id)` references `catalog_shows(namespace_id, show_id)`.

Collection membership:

- A show is in collection when `my_status is not null`.
- Clearing status deletes the overlay row or clears all My Data and then deletes the row. Prefer delete to match "removed from storage" semantics.

### 7.3 `cloud_settings`

Stores synced settings.

Columns:

- `namespace_id text not null`
- `user_id text not null`
- `id text not null default 'globalSettings'`
- `user_name text not null`
- `version numeric not null`
- `catalog_api_key text`
- `ai_api_key text`
- `ai_model text not null`

Primary key:

- `(namespace_id, user_id, id)`

Security note:

- User-entered API keys are optional. If stored, document that they are synced user settings. Never commit configured keys.

### 7.4 `app_metadata`

Tracks namespace-level data model version.

Columns:

- `namespace_id text primary key`
- `data_model_version integer not null default 3`
- `updated_at timestamptz not null default now()`

### 7.5 Optional Normalized Tables

Add only if needed for performance or clean querying:

- `user_show_tag_index(namespace_id, user_id, show_id, tag)` for fast tag filters.
- `catalog_people` for cached person profiles.
- `catalog_show_credits` only if person/detail performance requires it. Credits can remain transient per the schema reference.

If normalized tag rows are used, still maintain `my_tags` and `my_tags_update_date` as the conflict-resolution source of truth.

## 8. Persistence and Merge Rules

Create a central data service for all catalog and overlay merging. Do not spread merge logic through UI code.

Rules:

- External catalog data maps into a fresh catalog show snapshot.
- Existing non-user catalog fields use `selectFirstNonEmpty(newValue, oldValue)`:
  - Empty strings, empty arrays, and nulls never overwrite non-empty stored data.
  - Non-empty new values may fill missing stored values.
- User fields resolve by their update timestamps:
  - If both sides have timestamps, newer wins.
  - If only one side has a timestamp, that side wins.
- `details_update_date` updates whenever catalog details are refreshed.
- `creation_date` is set only once.
- `ai_scoop` uses its own update timestamp and expires after 4 hours for regeneration on demand.

Implement and unit test these functions:

- `mergeCatalogShow`
- `mergeUserOverlay`
- `isCollectionMember`
- `applyStatusChange`
- `applyInterestChange`
- `applyRatingChange`
- `applyTagChange`
- `removeFromCollection`
- `overlayShowForDisplay`

## 9. Catalog Provider Layer

Create a provider adapter abstraction so the app is not hard-wired throughout the UI.

Adapter responsibilities:

- Search title/keyword across movies and TV.
- Fetch show details.
- Fetch videos, backdrops, posters, logos, images.
- Fetch recommendations and similar shows.
- Fetch watch providers by region.
- Fetch cast and crew.
- Fetch seasons for TV.
- Fetch person details, images, and combined credits.
- Resolve AI recommendations by external ID and title/media type.

The first implementation can be a TMDB-like adapter because the PRD references fields such as movie/TV media types, providers, credits, similar, recommendations, logos, and community scores that map cleanly to that style of catalog.

Resolution rule for AI recommendations:

1. If AI provides an external ID, fetch that catalog item.
2. Accept it only when media type matches and title matches case-insensitively against the AI title or known alternate title.
3. If no ID or mismatch, search by title and accept the first deterministic match.
4. If unresolved, render non-interactive text and provide a Search handoff.

Every catalog item returned to UI should be passed through `overlayShowForDisplay` before rendering.

## 10. API and Server Boundary

Use route handlers or server actions as the boundary for all mutations and secret-bearing operations.

Recommended API groups:

### 10.1 Catalog

- `GET /api/catalog/search?q=&type=`
- `GET /api/catalog/shows/[showType]/[id]`
- `GET /api/catalog/shows/[showType]/[id]/media`
- `GET /api/catalog/shows/[showType]/[id]/recommendations`
- `GET /api/catalog/shows/[showType]/[id]/providers`
- `GET /api/catalog/people/[id]`

### 10.2 Library

- `GET /api/library`
- `PATCH /api/library/[showId]/status`
- `PATCH /api/library/[showId]/interest`
- `PATCH /api/library/[showId]/rating`
- `PATCH /api/library/[showId]/tags`
- `DELETE /api/library/[showId]`

All library endpoints must:

- Resolve `namespace_id` and `user_id`.
- Validate request body with Zod.
- Fetch or upsert catalog snapshot before writing overlay when the show came from Search or AI.
- Return the overlaid show object.

### 10.3 AI

- `POST /api/ai/ask`
- `POST /api/ai/ask/resolve-mentions`
- `POST /api/ai/scoop`
- `POST /api/ai/concepts`
- `POST /api/ai/concept-recommendations`

### 10.4 Settings and Data

- `GET /api/settings`
- `PATCH /api/settings`
- `GET /api/export`

### 10.5 Test/Admin

- `POST /api/admin/reset-namespace`

Gate admin/reset routes to test or development mode and require a server-only secret if exposed over HTTP.

## 11. Application Shell and Routing

Build the app as the first screen, not a marketing landing page.

Top-level shell:

- Left or responsive navigation/filter panel.
- Main content area.
- Persistent Find/Discover entry point.
- Persistent Settings entry point.
- Media-type toggle state available on Home filters.

Routes:

- `/` - Collection Home.
- `/find?mode=search|ask|alchemy` - Find/Discover hub.
- `/shows/[showType]/[id]` - Show Detail.
- `/people/[id]` - Person Detail.
- `/settings` - Settings and Your Data.

Client state that may remain local:

- Last selected filter.
- Status removal confirmation suppression/count.
- Current Ask conversation.
- Current Alchemy session.
- Current Explore Similar concepts/results.
- UI-only expansion/collapse state.

Persisted user data must not depend on local state.

## 12. Core Feature Plan

### 12.1 Collection Home

Build Home after persistence and catalog overlay helpers are in place.

Functional requirements:

- Load collection for `(namespace_id, user_id)`.
- Apply selected sidebar filter plus media type toggle.
- Group results into:
  1. Active.
  2. Excited: `my_status = later` and `my_interest = excited`.
  3. Interested: `my_status = later` and `my_interest = interested`.
  4. Other: Wait, Quit, Done, Next if present, and Later without interest.
- Active uses more prominent/larger tiles.
- Tile displays poster, title, in-collection indicator, and rating badge when present.
- Empty states:
  - No collection: prompt to Search or Ask.
  - Filter yields none: "No results found."

Filters:

- All Shows.
- Tag filters for every user tag.
- No tags if any saved show has no tags.
- Genre filters.
- Decade filters.
- Community score ranges.
- Media toggle: All / Movies / TV applied on top.

Implementation notes:

- Derive tag library from overlays.
- Use stable sort helpers, with recently updated user fields first where applicable.
- Always render overlaid show data.

### 12.2 Search

Functional requirements:

- Text search by title/keywords.
- Poster grid results.
- In-collection items marked.
- Selecting a result opens Show Detail.
- If user setting `autoSearch` is enabled, launch into Search on app load.

Implementation notes:

- Search results are transient until saved or details are opened.
- When opening details, fetch full detail and merge into `catalog_shows`.
- Overlay saved state onto every result by matching catalog show ID.

### 12.3 Show Detail Page

This page is the single source of truth for public facts, My Data, and discovery actions.

Preserve the narrative hierarchy:

1. Header media carousel with trailer/backdrop/poster/logo fallback.
2. Core facts row: year, runtime or seasons/episodes, community score.
3. Tag chips.
4. Overview plus Scoop toggle/stream.
5. "Ask about this show" CTA.
6. Genres and languages.
7. Traditional recommendations strand.
8. Explore Similar.
9. Streaming providers.
10. Cast and Crew.
11. Seasons for TV.
12. Budget vs Revenue for movies where available.

Relationship controls:

- Put status/interest chips in the toolbar.
- Chips: Active, Interested, Excited, Done, Quit, Wait.
- Interested sets `my_status = later` and `my_interest = interested`.
- Excited sets `my_status = later` and `my_interest = excited`.
- Reselecting an active status asks for removal confirmation unless suppressed.
- Clearing status removes the show and clears My Data.
- Rating an unsaved show auto-saves as Done.
- Adding a tag to an unsaved show auto-saves as Later + Interested.
- Setting any status saves the show.

Scoop:

- Toggle copy:
  - No scoop: "Give me the scoop!"
  - Cached scoop: "Show the scoop"
  - Open: "The Scoop"
- Stream progressively where possible.
- Generate spoiler-safe content by default.
- Cache for 4 hours.
- Persist only if the show is in collection; otherwise keep ephemeral.

Critical states:

- Unsaved show can generate ephemeral Scoop.
- Missing trailers/backdrops gracefully fall back.
- TV/movie-specific facts render conditionally.
- No concepts yet shows only Get Concepts CTA.

### 12.4 Ask

Functional requirements:

- Chat UI with user and assistant turns.
- Welcome view presents 6 random starter prompts and a refresh action.
- General Ask starts from Find.
- Ask About This Show enters Ask with show context seeded.
- Conversation context is session-only.
- Older turns summarize automatically after about 10 messages.
- AI may mention shows inline.
- Mentioned shows render in a horizontal strip.
- Tapping a mentioned show opens Detail if resolved, or hands off to Search if unresolved.

AI response contract:

- Use a shared AI persona.
- Stay in TV/movies.
- Spoiler-safe unless user asks for spoilers.
- Be warm, playful, opinionated, and honest.
- Direct answer within first few lines.
- Use bullets for multiple recommendations.
- Structured mention output:
  - `commentary`
  - `showList` as `Title::externalId::mediaType;;Title2::externalId::mediaType`

Fallback:

- If parsing fails, retry once with stricter formatting.
- If still invalid, show commentary and provide Search handoff.

### 12.5 Alchemy

Functional requirements:

1. User selects at least 2 starting shows from library and global catalog.
2. Tap Conceptualize Shows.
3. AI returns shared concept catalysts.
4. User selects 1 to 8 concepts.
5. Tap ALCHEMIZE!
6. AI returns 6 recommendations grounded in selected concepts.
7. User can choose More Alchemy! to chain results as new inputs.

State rules:

- Alchemy session is not persisted.
- Changing input shows clears concepts and results.
- Selecting/unselecting concepts clears downstream results.
- Results carry transient reasons.
- Saved results go through normal library save rules.

Quality rules:

- Concepts must be shared across all input shows.
- Concepts are 1 to 3 words, bullet-only, evocative, spoiler-free, and non-generic.
- Reasons explicitly name selected concepts.
- Recommendations resolve to real catalog items where possible.

### 12.6 Explore Similar

Functional requirements:

1. From Show Detail, user taps Get Concepts.
2. AI returns concepts for the single show.
3. User selects at least 1 concept.
4. User taps Explore Shows.
5. AI returns 5 recommendations.

Rules:

- Same concept quality bar as Alchemy.
- Same recommendation resolution pipeline.
- Results are session-only and can be saved through normal My Data controls.
- UI copy should imply "pick the ingredients you want more of."

### 12.7 Person Detail

Functional requirements:

- Reachable from cast/crew strands.
- Displays image gallery, name, and bio.
- Shows filmography/credits grouped by year.
- Provides lightweight analytics:
  - Average project ratings.
  - Top genres.
  - Projects by year.
- Selecting a credit opens Show Detail.

Implementation notes:

- Person and credit data can be transient unless caching is needed.
- Overlay saved state on every credit that maps to a show.

### 12.8 Settings and Your Data

Functional requirements:

- Font size/readability setting.
- Search on Launch toggle.
- Username.
- AI provider API key input, optional.
- AI model selection.
- Catalog provider API key input, optional.
- Export My Data.

Export:

- Produces a `.zip`.
- Contains JSON backup of saved shows, My Data, cloud settings, app metadata, local settings, and UI state where relevant.
- Dates encoded ISO-8601.
- Scope export to `(namespace_id, user_id)`.

Import/Restore:

- Document as desired but not implemented unless explicitly added later.

## 13. AI System Plan

Create a dedicated `src/lib/ai` layer.

Modules:

- `provider.ts` - AI provider interface.
- `prompts/persona.ts` - shared voice pillars and guardrails.
- `prompts/ask.ts`
- `prompts/scoop.ts`
- `prompts/concepts.ts`
- `prompts/recommendations.ts`
- `context/libraryContext.ts`
- `context/showContext.ts`
- `parsers/mentions.ts`
- `parsers/concepts.ts`
- `parsers/recommendations.ts`
- `quality/validation.ts`

Shared persona requirements:

- Fun, chatty TV/movie nerd friend.
- Water-cooler gossip plus critic brain plus hype friend.
- 70 percent friend, 30 percent critic.
- Joy-forward and warm.
- Opinionated honesty.
- Vibe-first and spoiler-safe.
- Specific, not generic.
- Brisk by default, richer for Scoop.

Surface-specific behavior:

- Search has no AI voice.
- Ask is conversational, direct, and low-friction.
- Scoop is a 150 to 350 word mini taste review with personal take, stack-up, Scoop centerpiece, fit/warnings, and gut-check verdict.
- Concepts are bullet-only, 1 to 3 words each, no explanation.
- Concept recommendations include concise reasons tied to selected concepts.

Context construction:

- Include saved library and My Data in compact form.
- Include current show context for Scoop and Ask About This Show.
- Include selected concepts for Explore Similar and Alchemy.
- Include recent conversation turns.
- Summarize older turns into 1 to 2 persona-consistent sentences after about 10 messages.

AI quality enforcement:

- Reject generic concepts such as "good characters" or "great story".
- Enforce counts:
  - Concepts: 8 by default.
  - Explore Similar recs: 5.
  - Alchemy recs: 6.
- Validate real-show resolution before displaying interactive result tiles.
- Score prompt outputs during tests against:
  - Voice adherence.
  - Taste alignment.
  - Surprise without betrayal.
  - Specificity.
  - Real-show integrity.

## 14. UI and Interaction Plan

Design principles:

- Build the usable app as the first screen.
- Keep operational UI dense, clear, and direct.
- Use familiar controls: segmented toggles for modes, chips for status/concepts/tags, sliders for ratings, icon buttons for compact actions, tabs or segmented control for Find modes.
- Cards only for repeated items, modal surfaces, and framed tools. Avoid nested cards.
- Use responsive constraints for poster tiles, media headers, toolbars, and grids to prevent layout shift.
- Ensure text fits within buttons/chips across mobile and desktop.
- Use full-width sections or unframed layouts for page sections.

Accessibility:

- Keyboard navigable status chips, concept chips, rating control, carousels, and mode switchers.
- Visible focus states.
- ARIA labels for icon-only buttons.
- Sufficient contrast for badges and text.
- Reduced-motion handling for carousels or media transitions.

## 15. Namespace Reset and Test Isolation

Implement deterministic destructive reset:

- Reset accepts a namespace ID.
- Deletes rows only where `namespace_id = target`.
- Does not truncate global tables.
- Can optionally filter `is_test = true` for test-only reset modes, but benchmark reset should be able to clear the entire namespace.
- Requires explicit confirmation or test/admin secret.

Tables touched by reset:

- `user_show_overlays`
- `catalog_shows`
- `cloud_settings`
- `app_metadata`
- Optional normalized tag/person/cache tables

Tests must create their own namespace and never depend on shared data.

## 16. Milestone Plan

### Milestone 0: Project Bootstrap

- Create Next.js TypeScript app structure.
- Add lint, format, test, build, and dev scripts.
- Add `.env.example` and secure `.gitignore`.
- Add theme tokens and base app shell.
- Add Supabase client factories:
  - Browser anon client.
  - Server client.
  - Server-only admin client if reset requires it.
- Add identity resolution helper.

Acceptance:

- App starts with `npm run dev`.
- Build and test commands run.
- Missing environment variables fail with clear messages.

### Milestone 1: Supabase Schema and Data Services

- Create migrations for core tables.
- Add namespace and user scoping helpers.
- Implement catalog and overlay repositories.
- Implement merge/default/removal business logic.
- Implement namespace reset script.

Acceptance:

- Unit tests cover save defaults, timestamp merges, status removal, and overlay display.
- Integration tests prove two namespaces cannot see each other's data through app services.
- Reset clears only the target namespace.

### Milestone 2: Catalog Adapter

- Implement provider abstraction and first catalog adapter.
- Implement search, detail, media, recommendations, providers, credits, seasons, and person fetches.
- Implement catalog-to-show mapper.
- Implement AI recommendation resolver.

Acceptance:

- Search and detail fetches map to canonical `Show` shape.
- Empty catalog values do not erase stored non-empty fields.
- Recommendations can be resolved by ID/title/media type.

### Milestone 3: Collection Home and Filters

- Build navigation/filter panel.
- Build grouped collection home.
- Build media type toggle.
- Build tile badges.
- Build empty states.

Acceptance:

- Saved shows group correctly by Active, Excited, Interested, and Other.
- Tag, no-tag, genre, decade, community score, and media-type filters compose correctly.
- Saved user overlays appear on all tiles.

### Milestone 4: Search and Basic Detail

- Build Find Search mode.
- Build result grid and detail navigation.
- Build Show Detail with header media, facts, overview, genres/languages, traditional recommendations, providers, cast/crew, seasons, and budget/revenue.
- Build relationship toolbar, rating, and tags.

Acceptance:

- Status, interest, rating, and tag mutations follow save defaults.
- Rating an unsaved show saves as Done.
- Tagging an unsaved show saves as Later + Interested.
- Clearing status confirms and removes all My Data.
- Refreshing details preserves user edits.

### Milestone 5: AI Foundation and Scoop

- Build AI provider interface and prompt/context modules.
- Implement Scoop generation with streaming if supported.
- Implement 4-hour freshness and saved-vs-ephemeral persistence.
- Add AI settings model selection.

Acceptance:

- Scoop includes required sections/intent.
- Unsaved show Scoop does not persist long-term.
- Saved show Scoop persists and refreshes after expiry on demand.

### Milestone 6: Ask

- Build Ask chat UI.
- Add starter prompts with refresh.
- Add session-only chat state.
- Add conversation summarization after about 10 messages.
- Add structured mentioned shows parsing and row rendering.
- Add Ask About This Show handoff.

Acceptance:

- Ask stays within TV/movie domain and uses product voice.
- Mentioned shows resolve to selectable show tiles where possible.
- Parser retries once on structured output failure.
- Clearing/resetting Ask removes session chat.

### Milestone 7: Concepts, Explore Similar, and Alchemy

- Implement single-show concepts.
- Implement multi-show shared concepts.
- Implement concept chip selection with cap of 8.
- Implement Explore Similar with 5 recs.
- Implement Alchemy with 6 recs and chaining.
- Clear downstream results when inputs or concepts change.

Acceptance:

- Concepts are 1 to 3 words, evocative, no explanation, and non-generic.
- Multi-show concepts represent shared ingredients.
- Reasons explicitly cite selected concepts.
- Interactive recs resolve to real catalog shows.

### Milestone 8: Person Detail, Settings, and Export

- Build Person Detail page.
- Build analytics charts.
- Build Settings page.
- Build synced settings and local settings.
- Build export zip.

Acceptance:

- Cast/crew navigation to person and credits back to shows works.
- Settings persist according to their intended storage.
- Export zip contains ISO-8601 JSON for saved shows and My Data scoped to the active user.

### Milestone 9: Hardening, Visual QA, and Benchmark Compliance

- Run full unit, integration, and E2E suite.
- Add visual smoke screenshots for Home, Search, Detail, Ask, Alchemy, Person, and Settings on desktop and mobile.
- Audit `.env.example`, `.gitignore`, and README.
- Confirm no product data depends on local storage.
- Confirm namespace reset and user scoping.

Acceptance:

- Clean build.
- Clean test suite.
- Verified benchmark scripts.
- No committed secrets.

## 17. Testing Plan

### Unit Tests

Cover:

- `selectFirstNonEmpty`.
- Catalog mapping for movie and TV payloads.
- Timestamp conflict resolution.
- Save defaults for status, interest, rating, and tags.
- Removing from collection clears all My Data.
- Filter grouping and media toggle composition.
- Mention parser exact format.
- Concept parser and generic concept rejection.
- Recommendation resolver title/media matching.
- Export JSON date serialization.

### Integration Tests

Cover:

- Supabase repository operations with namespace and user scoping.
- Two users in one namespace do not see each other's overlays.
- Two namespaces do not collide.
- Reset deletes only one namespace.
- Detail refresh preserves My Data.
- AI endpoints with mocked provider and parser retry.

### Component Tests

Cover:

- Home grouped sections and empty states.
- Search result badges.
- Detail relationship toolbar behavior.
- Removal confirmation suppression.
- Scoop cached/open/generating states.
- Ask mentioned shows row.
- Concept selection limits and downstream clearing.
- Alchemy chaining.

### E2E Journeys

Cover the PRD journeys:

1. Search -> Detail -> Interested/Excited/Active -> tag/rate.
2. Rating an unsaved show auto-saves as Done.
3. Tagging an unsaved show auto-saves as Later + Interested.
4. Home filtering by status/tag/media type.
5. Ask discovery -> select recommendation -> save.
6. Detail -> Get Concepts -> Explore Shows -> save one.
7. Alchemy -> conceptualize -> select catalysts -> recommendations -> chain.
8. Detail -> Person -> credit -> Detail.
9. Settings -> Export My Data.
10. Clear browser storage -> reload -> collection still present from Supabase.

### AI Quality Tests

Use mocked deterministic AI outputs for CI, plus optional manual/golden-set review for live models.

Score outputs against:

- Voice adherence >= 1.
- Taste alignment >= 1.
- Real-show integrity = 2.
- Total >= 7 out of 10.

Live AI tests should not block normal CI unless credentials are present.

## 18. Security and Privacy Plan

- Never commit secrets.
- Keep service-role key out of browser bundles.
- Validate all server inputs.
- Scope all user-owned queries by namespace and user.
- Avoid exposing raw AI or catalog keys to client code unless they are explicitly user-provided and intended for client use. Prefer server-side calls.
- Document benchmark dev identity and production gating.
- Prepare schema for future OAuth by keeping `user_id` opaque.
- Avoid storing chat history, Alchemy sessions, and transient AI recommendation reasons in the database.

## 19. Performance Plan

- Server-render initial Home and Detail data where practical.
- Use client cache for interactive mutations and optimistic feedback.
- Debounce search input.
- Lazy-load long-tail detail sections such as providers, cast/crew, seasons, and budget/revenue.
- Use responsive image sizes and poster/backdrop placeholders.
- Cache catalog details with `details_update_date`, while preserving user overlays.
- Keep AI context compact by summarizing library and older chat turns.
- Avoid preloading the entire catalog.

## 20. Data Continuity and Migration Plan

- Set `data_model_version` in `app_metadata`.
- Each migration must be additive or include a backfill path.
- Preserve saved shows and My Data through schema changes.
- Use per-field timestamps for conflict resolution.
- Keep export format versioned so future import/restore can be added without guessing.

## 21. Key Product Decisions to Lock for v1

- `Next` remains in the data model but is not a first-class UI status unless later required.
- Tags are the v1 list mechanism; named custom lists are out of scope.
- AI Scoop on an unsaved show is ephemeral and does not implicitly save.
- Clearing My Rating sets `my_score = null` and updates `my_score_update_date`; no separate explicit Unrated state for v1 unless later required.
- Import/Restore is documented as future work; Export is required.
- Alchemy sessions are not persisted.
- Chat history is not persisted.

## 22. Risks and Mitigations

### Real-show resolution can fail or mismatch

Mitigation:

- Prefer external IDs.
- Validate title and media type.
- Fall back to deterministic search.
- Render unresolved recommendations as non-interactive with Search handoff.

### AI output may drift off-brand or break structure

Mitigation:

- Central prompt builders.
- Strict parsers.
- One retry with stricter formatting.
- Mocked contract tests plus manual quality rubric.

### Namespace/user scoping can be accidentally bypassed

Mitigation:

- Central identity helper.
- Repository functions require namespace and user explicitly.
- Integration tests for cross-namespace and cross-user isolation.
- Code review checklist item for every query.

### Detail page can become cluttered

Mitigation:

- Preserve narrative hierarchy.
- Keep primary relationship actions in toolbar.
- Put optional depth lower on the page.
- Use progressive loading for long-tail sections.

### Catalog provider rate limits or missing data can degrade UX

Mitigation:

- Graceful empty states.
- Cache catalog snapshots.
- Avoid required preloading.
- Fetch long-tail detail sections on demand.

### Secret handling in benchmark mode can leak into client

Mitigation:

- Server-only AI and catalog calls by default.
- Only expose Supabase anon key publicly.
- Automated check for env files and secret-like values before final delivery.

## 23. Definition of Done

The build is complete when:

- The app runs with one command after filling `.env`.
- Supabase migrations produce a deterministic fresh schema.
- All user-owned records include `namespace_id` and `user_id`.
- Namespace reset works without global teardown.
- Clearing browser storage does not delete user data.
- Home, Search, Detail, Ask, Alchemy, Explore Similar, Person, Settings, and Export are implemented.
- User overlays display everywhere and survive catalog refreshes.
- AI surfaces follow the shared persona and structured output contracts.
- Recommendations either resolve to real selectable catalog items or fall back cleanly.
- Unit, integration, and E2E tests cover the key journeys.
- No secrets are committed.
