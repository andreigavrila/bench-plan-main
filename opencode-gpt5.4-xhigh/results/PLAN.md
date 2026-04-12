# Implementation Plan

## Scope and Starting Point

- The repo currently contains benchmark docs only, so implementation begins with a fresh Next.js + Supabase application scaffold.
- This is a planning-only deliverable. No source code, schema, or app behavior is being implemented in this step.
- The companion "heart" documents referenced at the end of `docs/prd/product_prd.md` are not present under `docs/prd/`. This plan therefore treats the available PRD files, AI specs, and quality bar as the authoritative source, and keeps the AI prompt layer configurable so those missing docs can be incorporated later without reworking the app.
- No offline-first or device-only persistence work is planned beyond normal loading/error handling. The backend remains the source of truth.

## Architecture Decisions

### Runtime and Boundaries

1. Use Next.js App Router as the runtime and server boundary.
2. Keep route entrypoints thin in `src/app/...` and place actual screens/features under `src/pages/.../features/...` to match the repo's fractal architecture guidance.
3. Put all persistence, AI calls, catalog calls, export generation, and test-reset logic behind server route handlers or server modules so:
   - the backend remains the source of truth,
   - service-role Supabase access stays server-only,
   - identity and namespace scoping live in one place,
   - future OAuth only changes the identity resolver, not the schema.
4. Treat client storage as disposable and limit it to local UI preferences and session-only AI state.

### Proposed Directory Shape

```text
src/
  app/
    page.tsx
    discover/page.tsx
    shows/[showId]/page.tsx
    people/[personId]/page.tsx
    settings/page.tsx
    api/
      collection/...
      discover/...
      settings/...
      export/...
      test/reset/route.ts
  config/
  theme/
  components/
  hooks/
  utils/
  pages/
    CollectionHome/
    Discover/
    ShowDetail/
    PersonDetail/
    Settings/
  server/
    context/
    db/
    catalog/
    ai/
    export/
```

### Route Map

1. `/` -> Collection Home.
2. `/discover?mode=search|ask|alchemy` -> Discover hub with an explicit mode switcher.
3. `/shows/[showId]` -> Show Detail.
4. `/people/[personId]` -> Person Detail.
5. `/settings` -> Settings and Your Data.
6. `/api/...` -> mutations, AI requests, export download, and test reset.

### Core Persistence Model

1. `shows`
   - Composite key: `(namespace_id, user_id, id)`.
   - Stores the persisted fields described in `storage-schema.md`: public catalog snapshot, all `my*` fields, AI Scoop, provider data, timestamps, and `is_test`.
   - `myInterest` is retained even when status leaves `Later`, but ignored in UI/query logic until the show returns to `Later`.
   - Clearing status deletes the row entirely so removal also clears tags, rating, interest, and Scoop.
2. `cloud_settings`
   - Keyed by `(namespace_id, user_id)`.
   - Stores synced settings: username, AI model, optional user-entered AI/catalog keys, and a monotonically increasing `version` for conflict resolution.
   - Create a row on first use with a generated default username and environment-backed model defaults.
3. `app_metadata`
   - Tracks data model version per namespace and supports forward migrations and import/export compatibility.
4. Local client storage
   - Stores `fontSize`, `autoSearch`, `hideStatusRemovalConfirmation`, `statusRemovalCountKey`, and `lastSelectedFilter`.
   - Loss of this storage must not affect collection data or synced settings.

### Shared Domain Services

1. Request context resolver
   - Produces `{ namespaceId, userId }` for every server request.
   - Supports dev/test identity injection via environment defaults plus a gated dev-only header or cookie override.
   - Keeps `namespace_id` and `user_id` opaque and stable.
2. Catalog adapter
   - Wraps the chosen movie/TV API and maps results into the app's `Show` shape.
   - Handles title/media-type inference, date parsing, image URL selection, provider-region payloads, person details, credits, similar/recommended items, and detail fetches.
3. Show merge service
   - Implements `selectFirstNonEmpty(newValue, oldValue)` for non-user fields.
   - Resolves `myTags`, `myScore`, `myStatus`, `myInterest`, and `aiScoop` by per-field update timestamp.
   - Preserves `creationDate`, updates `detailsUpdateDate`, and prevents duplicate rows via DB constraints plus migration backfills.
4. Overlay hydration service
   - Accepts any show list from search, recommendations, AI, or person credits and overlays saved `my*` data before UI rendering.
   - This enforces the rule that the user's version always wins everywhere.
5. AI orchestration service
   - Centralizes shared persona and guardrail rules and exposes surface-specific operations for Ask, Scoop, Concepts, Explore Similar, and Alchemy.
6. Export service
   - Produces a ZIP containing a JSON snapshot with ISO-8601 dates and version metadata.

## Functional Workstreams

### 1. Benchmark Runtime & Isolation

1. `RT-01` Bootstrap a new Next.js app with TypeScript, linting, unit/integration test support, and Playwright end-to-end support because the repo currently has no application scaffold.
2. `RT-02` Add `.env.example` documenting every required variable:
   - `APP_NAMESPACE_ID`
   - `DEFAULT_USER_ID`
   - `SUPABASE_URL`
   - `SUPABASE_ANON_KEY`
   - `SUPABASE_SERVICE_ROLE_KEY`
   - default catalog API credentials
   - default AI API credentials and model
   - dev-only identity flags
3. `RT-03` Verify `.gitignore` excludes `.env*` secrets while preserving `.env.example`.
4. `RT-04` Create repeatable SQL migrations for `shows`, `cloud_settings`, and `app_metadata`, plus any indexes needed for status, type, timestamps, and tag lookups.
5. `RT-05` Implement a namespace-scoped reset path used by `npm run test:reset` so destructive tests only delete rows for the active `namespace_id`.
6. `RT-06` Add standard scripts for `dev`, `test`, `test:reset`, `lint`, and `build`; Docker must remain optional, not required.
7. `RT-07` Gate dev identity injection so benchmark and dev runs can use a fixed default user or `X-User-Id`, but production mode can later swap to real OAuth without schema changes.

### 2. Collection Data & Persistence

1. `DATA-01` Implement the persisted `Show` repository around the full schema reference, including public catalog fields, all `my*` fields, `aiScoop`, provider IDs by region, timestamps, and `isTest`.
2. `DATA-02` Implement catalog-to-show mapping rules:
   - external catalog IDs map to `id` and `externalIds`
   - title resolves from movie title or TV name
   - media type infers `movie` or `tv`
   - genre IDs map to names
   - images become renderable URLs
   - provider data stores IDs only
   - transient data like credits, videos, seasons, and recommendations are not persisted
3. `DATA-03` Implement merge rules exactly as specified:
   - public fields never overwrite a non-empty stored value with empty or nil
   - user fields and Scoop resolve by newer per-field timestamp
   - `creationDate` is first-write only
   - `detailsUpdateDate` is refreshed on catalog merges
4. `DATA-04` Implement all save triggers and defaults:
   - setting any status saves the show
   - selecting `Interested` or `Excited` saves as `Later + interest`
   - rating an unsaved show saves as `Done`
   - tagging an unsaved show saves as `Later + Interested`
5. `DATA-05` Implement removal semantics:
   - reselecting the active status after confirmation deletes the saved row
   - all My Data and persisted Scoop are cleared with that delete
   - the local UI confirmation counter and hide flag are updated without affecting server data
6. `DATA-06` Implement cross-device conflict handling by generating timestamps on the server for every user-field mutation and resolving collisions per field, not per row.
7. `DATA-07` Add migration and backfill tests that prove stored shows survive schema evolution without losing status, interest, tags, rating, or Scoop.
8. `DATA-08` Build filter and query services for:
   - All Shows
   - tag filters
   - `No tags` when relevant
   - genre filters
   - decade filters
   - community score filters
   - media-type toggle layered on top of any filter
9. `DATA-09` Define score bucket constants during implementation because the PRD names community-score filters but does not prescribe exact ranges.
10. `DATA-10` Enforce transparent duplicate prevention with a unique composite key and a cleanup migration for any legacy duplicates, using per-field timestamps to decide survivors.

### 3. App Navigation & Discover Shell

1. `NAV-01` Build a shell with a persistent primary navigation and filter surface plus a main content area containing Home, Discover, Detail, Person, and Settings destinations.
2. `NAV-02` Make Find/Discover and Settings persistent global entry points, matching the PRD's top-level navigation.
3. `NAV-03` Use a clear Discover mode switcher for Search, Ask, and Alchemy; Search must remain straightforward catalog search with no AI voice.
4. `NAV-04` Preserve selected filter state locally so the user returns to the same collection view after moving between pages.
5. `NAV-05` Respect the Search-on-launch preference by auto-opening Discover Search on initial load when `autoSearch` is enabled.
6. `NAV-06` Implement responsive behavior so the filter panel becomes a mobile-friendly drawer or sheet without changing core flows.
7. `NAV-07` Reset session-only AI state when the user explicitly leaves or resets Ask or Alchemy, while keeping persisted collection and settings untouched.

### 4. Collection Home & Search

1. `HOME-01` Build Collection Home around grouped status sections:
   - Active
   - Excited (`Later + Excited`)
   - Interested (`Later + Interested`)
   - Other statuses (collapsed group containing Wait, Quit, Done, and any Later items missing interest)
2. `HOME-02` Make Active visually more prominent than the other groups and keep poster, title, and badge information lightweight on all tiles.
3. `HOME-03` Apply the media-type toggle (`All / Movies / TV`) on top of whichever sidebar filter is selected.
4. `HOME-04` Show correct empty states for:
   - empty collection
   - filter with no matching results
5. `HOME-05` Implement live Search with debounced catalog queries, no heavy preload assumptions, and in-collection and rating indicators on result tiles.
6. `HOME-06` Selecting any tile from Home or Search opens Show Detail.
7. `HOME-07` Ensure Home, Search, and recommendation tiles always render the saved overlay version when a row exists in `shows`.
8. `HOME-08` Populate the sidebar dynamically from the user's current tag library and tagless state instead of hardcoding filter lists.
9. `HOME-09` Use timestamp-aware sorting inside groups so recently edited shows surface predictably when a group needs ordering.

### 5. Show Detail & Relationship UX

1. `DET-01` Build the Show Detail route as the single source of truth for a show by fetching catalog details, merging saved data, and rendering sections in the narrative order documented in `detail_page_experience.md`.
2. `DET-02` Implement a premium header media area that prefers trailers when available but falls back gracefully to poster, backdrop, and logo layouts without blocking the rest of the page.
3. `DET-03` Place status and interest chips in the toolbar, not deep in the body. The visible chips must be:
   - Active
   - Interested
   - Excited
   - Done
   - Quit
   - Wait
   The hidden `Next` status remains supported in the data model but not exposed as a first-class UI chip.
4. `DET-04` Map `Interested` and `Excited` chip clicks to `myStatus = Later` plus the correct `myInterest`, while keeping existing interest values dormant when status changes away from `Later`.
5. `DET-05` Implement rating controls beside the community score so rating an unsaved show auto-saves it as `Done`.
6. `DET-06` Implement tag display plus picker so adding the first tag to an unsaved show auto-saves it as `Later + Interested`.
7. `DET-07` Implement destructive removal confirmation on status reselect, including the local opt-out after repeated confirmations.
8. `DET-08` Render overview early and place the Scoop affordance beside it with the exact state progression:
   - no scoop -> `Give me the scoop!`
   - cached scoop -> `Show the scoop`
   - open state title -> `The Scoop`
9. `DET-09` Implement Scoop generation and caching rules:
   - generate on demand
   - show `Generating...` or streaming content instead of blank waiting
   - treat 4 hours as stale
   - persist the Scoop only if the show is already in the collection
   - allow ephemeral Scoop viewing for unsaved shows
10. `DET-10` Add the `Ask about this show` CTA that opens Discover Ask with hidden seeded show context and a visible handoff banner, rather than depending on a rigid auto-filled prompt.
11. `DET-11` Render traditional similar and recommended shows as a low-effort discovery strand separate from the AI features.
12. `DET-12` Implement the Explore Similar block in-page, followed by streaming availability, cast, crew, seasons for TV, and budget versus revenue for movies when available.
13. `DET-13` Keep core facts visible near the top: year, runtime or season and episode context, community score, user rating and status, genres, and languages.
14. `DET-14` Carry AI recommendation reasons as transient UI text only; they are useful on cards but should not be persisted to the database.

### 6. Ask Chat

1. `ASK-01` Build a chat surface with user and assistant turns, a welcome state, 6 random starter prompts, and a refresh action that swaps in a different prompt set.
2. `ASK-02` Model chat memory as session-only state:
   - recent turns stay verbatim
   - older turns summarize into 1-2 sentences after roughly 10 messages
   - summaries must keep the same friendly voice, not sterile system language
   - resetting or leaving Ask clears the session
3. `ASK-03` Assemble AI context from the saved library, My Data, optional handoff show context, and the active session summary and recent turns so Ask feels taste-aware rather than generic.
4. `ASK-04` Enforce shared AI rules:
   - TV and movie domain only
   - spoiler-safe by default
   - opinionated honesty
   - specific reasoning over genre boilerplate
5. `ASK-05` Require the structured response contract for mentions:
   - `commentary` contains the user-facing text and no external IDs
   - `showList` uses the exact `Title::externalId::mediaType;;...` format
6. `ASK-06` Build a strict parser that retries once on malformed structured output, then falls back to commentary plus Search handoff if parsing still fails.
7. `ASK-07` Resolve mentioned shows to real catalog items by external ID first and title matching second, then render them in a horizontal mentioned-shows strip.
8. `ASK-08` If a mentioned title cannot be resolved, show it as non-interactive or offer a Search handoff instead of pretending it is a real item.
9. `ASK-09` Keep Ask answers concise by default: direct answer in the first few lines, then short paragraphs and bullet lists when recommending multiple titles.

### 7. Concepts, Explore Similar & Alchemy

1. `CON-01` Implement a concept generation operation that returns bullet-list-only outputs, 1-3 word concepts, no spoilers, no explanations, and no generic filler.
2. `CON-02` Generate concepts across multiple axes so the list covers structure, vibe, emotion, relationship dynamics, and craft instead of repeating near-synonyms. In multi-show generation, every concept must represent shared commonality across all seed shows.
3. `CON-03` Generate 8 concepts by default for single-show flows to satisfy the quality bar. For multi-show Alchemy flows, return a somewhat larger option pool while still capping user selection at 8.
4. `CON-04` Order concepts by strength and clarity so the best "aha" ingredients appear first.
5. `EXP-01` On Show Detail, implement the Explore Similar loop:
   - Get Concepts
   - select 1+ concept chips
   - Explore Shows
   - render 5 recommendations with concise concept-linked reasons
6. `EXP-02` Reset Explore Similar recommendations whenever the user changes concept selection, keeping the flow playful and backtrack-friendly.
7. `ALC-01` Build Alchemy as a step-based workspace where the user selects 2+ seed shows from both the saved library and the global catalog.
8. `ALC-02` After seed selection, conceptualize the shows, let the user choose up to 8 catalysts, and return 6 recommendations with concise reasons explicitly tied to the selected concepts.
9. `ALC-03` Bias concept-based recommendations toward recent shows without excluding classics or hidden gems when the concept fit is stronger.
10. `ALC-04` Allow chaining via `More Alchemy!`, using the current round's outputs as fresh inputs without persisting sessions to the backend.
11. `ALC-05` Clear downstream concepts and results whenever seed shows change so the state never drifts out of sync.
12. `ALC-06` Keep Alchemy results, reasons, and selected concepts session-only. Leaving Alchemy clears them.
13. `CON-05` Use the same recommendation resolution contract across Explore Similar and Alchemy:
    - prefer valid external IDs
    - resolve to real catalog items
    - keep unresolved results non-interactive or hand them off to Search
14. `CON-06` Make the UI copy explain the concept system in plain language, including the nudge to "pick the ingredients you want more of."

### 8. AI Voice, Persona & Quality

1. `AI-01` Implement one shared persona layer used by Scoop, Ask, Concepts, Explore Similar, and Alchemy:
   - joy-forward and warm
   - opinionated but not snobby
   - vibe-first and spoiler-safe
   - specific, not generic
   - brief by default, more lyrical only when earned
2. `AI-02` Keep Search intentionally non-AI in tone so catalog search remains direct and low-friction.
3. `AI-03` Create surface-specific prompt and contract modules instead of one giant prompt so each surface can honor its output format and length target:
   - Scoop: roughly 150-350 words with personal take, honest stack-up, centerpiece paragraph, fit and warnings, and verdict
   - Ask: 1-3 tight paragraphs plus lists when helpful
   - Concepts: bullet-only ingredients
   - Concept recommendations: 1-3 sentence reasons per title
4. `AI-04` Add explicit guardrails for mixed-reception honesty, spoiler handling, domain redirection, and actionable real-show outputs.
5. `AI-05` Build a small discovery quality harness using fixed scenarios and the `discovery_quality_bar.md` rubric so the team can review:
   - voice adherence
   - taste alignment
   - surprise without betrayal
   - specificity of reasoning
   - real-show integrity
6. `AI-06` Treat real-show integrity as non-negotiable in testing and manual review; a recommendation without a valid catalog match is a failed output unless it falls back gracefully to Search.
7. `AI-07` Keep the AI layer configurable because `product_prd.md` references companion "heart" documents that are not currently present in `docs/prd/`.

### 9. Person Detail

1. `PER-01` Implement Person Detail pages reachable from cast and crew sections on Show Detail.
2. `PER-02` Fetch and render the person's gallery, name, bio, and full credit list.
3. `PER-03` Group filmography and credits by year and make every credit tile navigate to that show's Detail page.
4. `PER-04` Add lightweight analytics charts for project ratings, top genres, and projects-by-year, using catalog and community data plus saved overlay data where available.
5. `PER-05` Degrade gracefully when a person has sparse images or incomplete metadata so the page remains useful without fabricated insights.

### 10. Settings & Export

1. `SET-01` Build Settings sections for App, User, AI, Integrations, and Your Data.
2. `SET-02` Implement local App settings for font size and readability plus Search on Launch; apply font size through theme tokens rather than inline values.
3. `SET-03` Implement synced User, AI, and Integration settings in `cloud_settings`:
   - username
   - AI model selection
   - optional user-entered AI API key
   - optional user-entered catalog API key
   Environment defaults should be used when user-specific keys are absent.
4. `SET-04` Keep secrets out of source control and client bundles. Any elevated credentials remain server-only.
5. `SET-05` Implement `Export My Data` as a ZIP download containing a JSON snapshot of saved shows and My Data, synced settings, and schema metadata with ISO-8601 timestamps.
6. `SET-06` Do not partially ship Import or Restore in v1. Surface it as a future enhancement only, because the PRD explicitly calls it desired but not currently implemented.
7. `SET-07` Seed a friendly default username on first launch so synced settings have a stable starting point even in benchmark mode.

## Delivery Sequence

1. Phase 1: Foundation
   - `RT-01` through `RT-07`
   - `DATA-01` through `DATA-03`
   - Outcome: working app shell, schema, environment contract, request context, and repositories
2. Phase 2: Collection and Discover shell
   - `DATA-04` through `DATA-10`
   - `NAV-01` through `NAV-07`
   - `HOME-01` through `HOME-09`
   - Outcome: persistent library, filtering, search, overlays, and benchmark-safe data isolation
3. Phase 3: Show Detail and relationship controls
   - `DET-01` through `DET-14`
   - Outcome: source-of-truth detail experience with status, rating, tags, Scoop, and traditional discovery
4. Phase 4: AI discovery
   - `ASK-01` through `ASK-09`
   - `CON-01` through `CON-06`
   - `ALC-01` through `ALC-06`
   - `AI-01` through `AI-07`
   - Outcome: Ask, Explore Similar, and Alchemy all working against the same persona and real-show resolution rules
5. Phase 5: Person, Settings, Export, and hardening
   - `PER-01` through `PER-05`
   - `SET-01` through `SET-07`
   - migration and backfill hardening plus full QA pass
   - Outcome: remaining surfaces complete, export working, and benchmark verification ready

## Validation Plan

1. Unit tests
   - catalog-to-show mapping
   - `selectFirstNonEmpty` merge behavior
   - per-field timestamp conflict resolution
   - save defaults for status, rating, and tag flows
   - removal semantics
   - filter and grouping logic
   - Ask structured parsing and retry
   - concept output validation
   - export serialization with ISO timestamps
2. Integration tests
   - server routes against a test Supabase namespace
   - catalog resolution fallback behavior
   - AI response parsing plus real-show lookup
   - settings persistence
   - namespace-scoped reset script
3. End-to-end tests
   - build collection from Search
   - rate-to-save
   - tag-to-save
   - status removal confirmation
   - Ask recommendation to Detail to save
   - Explore Similar concept-to-rec flow
   - Alchemy multi-seed chaining flow
   - Person Detail to credit to Show Detail
   - Export My Data
4. Visual and polish checks
   - Home grouping on desktop and mobile
   - Discover mode switching
   - Detail page section order and fallback states
   - Scoop loading, cached, and open states
5. Manual AI review
   - score a fixed set of Ask, Scoop, Concept, Explore Similar, and Alchemy scenarios against the discovery quality bar before calling the app feature-complete

## Key Risks and Decisions To Track

1. `product_prd.md` references companion "heart" documents that are not present in `docs/prd/`. The implementation should not block on them, but the AI prompt and config layer must stay easy to tune if those docs are later restored.
2. The PRD leaves exact community-score filter buckets undefined. Decide and document fixed ranges during implementation rather than inventing them ad hoc in the UI.
3. `Next` should remain a data-model-only status unless product guidance changes.
4. Unsaved Scoop should remain ephemeral and should not implicitly save a show unless a later product decision changes the rule.
5. Clearing My Rating should use the existing nullable model (`null` or unset) until the open "explicit unrated state" question is answered.
6. Import and Restore remain out of scope for v1, but the export format should be structured so future import is possible without schema redesign.
