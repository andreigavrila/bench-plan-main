# Implementation Plan — Personal TV & Movie Companion

## Scope and implementation stance

Build a new full-stack application from this documentation-only seed. The implementation will use the current stable Next.js release with the App Router, TypeScript, and Supabase's official libraries, as required by the infrastructure rider. Next.js route files will be deliberately thin routing/server boundaries; the product UI will live in the required fractal `src/pages` feature structure. Supabase is the backend source of truth. Browser state may cache request results or hold transient sessions, but clearing it must not lose a library, settings, or any other persisted user data.

Use adapters at the server boundary for the catalog and AI providers. The PRD does not name a catalog or AI vendor, so their vendor-specific requests, credentials, and payload normalization must not leak into page features or persistence. The completed app must accept configured providers through environment variables and settings where allowed, without source edits or committed secrets.

Out of scope for this build: offline-first storage, a full OAuth experience, import/restore, named custom lists, saved/shareable Alchemy sessions, and elevating `Next` to a visible primary status. The data model will retain `Next` so it can be surfaced later without migration.

## 1. Establish the runnable project and execution boundary

1. Create the Next.js/TypeScript project baseline and add the UI, test, validation, archive-generation, Supabase, and provider-client dependencies. Set a Node version compatible with the selected current stable Next.js release.
2. Add `.env.example` and document every variable, separating browser-safe public values from server-only secrets. Include at minimum:
   - `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_ANON_KEY` for the public Supabase client;
   - `SUPABASE_SERVICE_ROLE_KEY` for server-only privileged operations;
   - stable `APP_NAMESPACE_ID` and a dev/test identity value such as `DEV_USER_ID`;
   - server-only catalog and AI provider API keys, base URLs if configurable, and a default AI model;
   - an environment/mode flag that controls the development identity-injection mechanism.
3. Update `.gitignore` to exclude every `.env*` secret while explicitly retaining `.env.example`. Ensure no client bundle, error response, log, or export contains secret keys.
4. Add documented package scripts for development, unit/integration tests, end-to-end tests, lint/type checking, production build, and a namespace-scoped `test:reset`. The normal cloud-agent path must use hosted Supabase; Docker may be documented only as an optional local convenience.
5. Centralize configuration validation in `src/config`. Fail fast with actionable startup errors for missing required server configuration, but allow optional user-entered provider settings where the product permits them.

## 2. Define the identity, isolation, and server-access model

1. Resolve one request context at the beginning of every route handler/server action: `{ namespaceId, userId, isTest, isDevelopmentIdentity }`. `namespaceId` comes from the stable build configuration and `userId` is an opaque stable string; do not encode auth-provider assumptions into either.
2. In development/test only, accept the documented injected identity (for example, a guarded `X-User-Id` header or a development selector), with a safe configured default. Reject that mechanism in production mode. Keep the context interface independent of this mechanism so an OAuth session adapter can replace it later without changing schema or business services.
3. Make all user-owned reads and writes go through authenticated Next.js server boundaries. Use the Supabase anon key only for intentionally safe browser use; keep service-role use exclusively in server modules. Apply Supabase RLS and/or server-side query constraints so a request can access only its `(namespace_id, user_id)` data and cannot substitute another namespace in input.
4. Include `namespace_id` in all persistence whose records are created by a run, including user data, settings, metadata, and any catalog cache. Make namespace + user a visible predicate in repository methods, never an optional caller convention.
5. Implement the reset endpoint/script as development/test-only, require the configured namespace, and delete only records in that namespace in dependency order. It must never issue global teardown operations.

## 3. Create repeatable Supabase schema, migrations, and persistence services

1. Add versioned, idempotent Supabase migrations and a small test fixture/seed mechanism. Include indexes and uniqueness constraints for the primary query paths and external catalog identity. A fresh hosted database must be reproducible by applying migrations alone.
2. Model public catalog facts separately from a user's overlay so a catalog refresh cannot overwrite another user's data. A practical relational shape is:
   - `namespace_users`: opaque `user_id`, namespace, creation metadata;
   - `catalog_shows`: normalized canonical movie/TV identity, external IDs, title/type, catalog metadata, media URLs, provider-ID blob, and catalog refresh timestamps;
   - `user_shows`: one overlay per `(namespace_id, user_id, catalog_show_id)` containing status, interest, score, scoop, all per-field update timestamps, creation timestamp, and test marker;
   - `user_show_tags`: normalized free-form tags tied to the overlay; expose both per-tag changes and a canonical `my_tags_update_date` on the overlay so the set has last-writer-wins behavior;
   - `user_settings` and `user_ui_preferences`: username, selected AI model, optional provider key references/values per product policy, font size, search-on-launch, removal-confirmation preferences/count, and last filter;
   - `app_metadata` (per namespace/user as appropriate) for model version and forward migrations.
   Store dates as timezone-aware timestamps and serialize every backup date as ISO-8601. Store provider availability as IDs by country and fulfillment type rather than duplicating provider display metadata.
3. Preserve the technical reference's full `Show` capabilities: movies versus TV, external IDs, summaries/taglines/genres/languages, score/popularity, images/logos, dates, movie financial/runtime fields, TV status/season/episode fields, and provider data. Persist only re-pullable catalog fields; attach cast, crew, videos, image galleries, seasons, traditional recommendations/similar titles, and person credits as transient provider responses.
4. Give every catalog item a stable provider/type-aware identity, and constrain it to prevent duplicate saves. When a catalog result is fetched, upsert public metadata with `selectFirstNonEmpty(new, old)` semantics: no empty/null refresh may erase known title, image, array, or fact. Set `detailsUpdateDate` on refresh and set creation time only on initial creation.
5. Implement user-overlay mutation services as the only place that enforce business rules and timestamp each modified field:
   - setting `Active`, `Wait`, `Done`, `Quit`, or hidden `Next` saves/updates that status;
   - selecting `Interested` or `Excited` writes `Later` plus the corresponding interest;
   - setting status away from Later leaves historical interest available but unused;
   - rating an unsaved show creates the overlay as `Done`; tag addition to an unsaved show creates it as `Later + Interested`; status-free saving otherwise defaults to the latter;
   - clearing/reselecting the active status only deletes after confirmation and removes the overlay, tag rows, score, status/interest, and persisted scoop together;
   - a new timestamp wins per user field during concurrent saves/sync. Tags are resolved as a last-updated set, while catalog fields never override user fields.
6. Write an explicit migration policy before release: every schema change gets a forward migration, preserves current overlays and timestamps, backfills safely, and advances metadata only after verification. Do not use destructive changes for normal upgrades.

## 4. Build catalog, library, settings, and export APIs

1. Implement a server-side catalog adapter interface supporting title/keyword search, detailed movie/TV lookup, images/logos/trailers, credit/person lookup, provider availability, seasons, traditional similar/recommended titles, and the facts needed for person analytics. Normalize its payload into the catalog domain model and select a deterministic best logo. Missing media must become valid empty/transient states, not provider errors exposed to the UI.
2. Add catalog routes/services for search, detail refresh/read, person detail, and selectable-title resolution. Search returns a poster-friendly grid and overlays collection state/rating for the current user. Detail reads fresh public data where appropriate, writes merged catalog data, then applies the current user's overlay to form the response view model.
3. Add library routes/services that return only the user's saved overlays joined with catalog data, tag library, generated sidebar filters, and filter counts. Support `all`, tag, `No tags`, genre, decade, community-score range, and internal `myStatus` filter types plus an independent `all | movie | tv` media toggle. Group results as Active, Excited, Interested, then collapsed Other (`Wait`, `Quit`, `Done`, and Later without interest); sort each sensible group by most recently updated relationship data.
4. Add narrowly scoped mutation APIs for status, rating (including clearing to an unrated/null state), complete tag-set edits, and persisted Scoop updates. Validate media type, input ranges, tag trimming/deduplication, ownership, and removal-confirmation state on the server rather than trusting UI state.
5. Add settings APIs for username, font/readability token, auto-search, model selection, optional integration configuration, and UI preferences. Treat user-entered keys as optional, never return them after writing, and document the security tradeoff if they are synced; deployment-provided keys remain server-only.
6. Add `Export My Data`: authorize the current context, collect exactly that user's library overlays/settings needed by the product, serialize a versioned JSON document with ISO-8601 dates, wrap it in a `.zip`, stream it with a safe filename, and exclude API keys/secrets and transient AI sessions. Validate the archive schema in tests. Do not expose an Import UI/API until its conflict, validation, and overwrite rules are specified.

## 5. Build provider-agnostic, taste-aware AI services

1. Create server-only AI provider and prompt-context adapters. Each request constructs minimal context from the current library's public facts plus My Data, selected current show(s)/concepts, and only the active in-memory session turns. All surfaces share the same base persona: warm, chatty TV/movie nerd; specific, opinionated, honest, vibe-first, and spoiler-safe by default. Redirect non-TV/movie requests gracefully.
2. Implement Ask with a structured response contract of `commentary` plus `showList` in the exact `Title::externalId::mediaType;;...` format. Validate model output using a schema; parse defensively; retry once with stricter format instructions on malformed output; then retain unstructured commentary with a Search handoff if parsing still fails. Exclude external IDs from user-facing commentary.
3. Keep Ask messages, mentioned-title strips, and summaries in feature/session memory only. After approximately ten turns, replace older history with a one-to-two-sentence persona-consistent summary while retaining recent turns. Reset/leaving Ask discards the session. “Ask about this show” seeds the Ask session with exact current-show context and an explicit handoff marker.
4. Implement Scoop as a structured, stream-capable response. Its display contract is a 150–350 word mini taste blog with a clear personal take, honest stack-up, emotionally central Scoop paragraph, practical fit/warnings, and verdict. Stream tokens to the UI when supported; display a generating state rather than blank space. Cache freshness is four hours; persist only when the show is in the collection, otherwise retain it only in the current detail session.
5. Implement concept generation for one show and for 2+ Alchemy inputs. Enforce bullet-only output, one-to-three-word spoiler-free concepts, specificity/diversity across vibe/structure/emotion/craft, and shared commonality for multi-show generation. Generate eight concepts by default; generate a larger candidate pool for multi-show where useful. Do not accept generic placeholders such as “good characters.”
6. Implement concept-based recommendation calls with selected concepts made explicit in prompt and in each returned reason. Request five Explore Similar recommendations and six Alchemy recommendations; bias toward newer work without excluding classics. Alchemy requires at least two input shows and permits one through eight selected concepts.
7. Centralize recommendation resolution: prefer supplied external ID and accept the first catalog result whose title matches case-insensitively; otherwise perform a constrained search and only make the result interactive after deterministic title/type validation. Preserve the AI reason as transient view data. Non-resolvable entries are visibly non-interactive with an accessible Search handoff. This resolver is also used by Ask mentions and must be covered by tests for mismatched IDs/titles and hallucinations.

## 6. Build the shared UI system and route shells

1. Establish `src/theme` tokens for color, typography, spacing, radii, breakpoints, elevations, and readable font-size scales. Create accessible shared primitives under `src/components` (buttons, chips, segmented controls, dialogs, poster tile, horizontal strand, empty/error/loading states, streaming panel, slider, form controls) with no inline styles or magic values in TSX.
2. Use thin App Router entries in `src/app` for layout, route metadata, and route-specific loading/error boundaries. Place page behavior in the fractal structure below, keeping TSX to composition/binding and extracting logic to feature hooks:

   ```text
   src/
     config/                     # validated environment and domain constants
     theme/                      # CSS/tokens and readability themes
     components/                 # shared accessible primitives
     hooks/                      # cross-page query, auth-context, and media hooks
     utils/                      # pure formatting/validation helpers
     pages/
       CollectionHome/
         CollectionHome.tsx
         features/SidebarFilters/
         features/LibrarySections/
         features/MediaTypeToggle/
       Discover/
         Discover.tsx
         features/ModeSwitcher/
         features/Search/
         features/Ask/
         features/Alchemy/
       ShowDetail/
         ShowDetail.tsx
         features/HeaderMedia/
         features/MyRelationship/
         features/Scoop/
         features/ExploreSimilar/
         features/Recommendations/
         features/Streaming/
         features/Credits/
       PersonDetail/
         PersonDetail.tsx
         features/Gallery/
         features/Analytics/
         features/Filmography/
       Settings/
         Settings.tsx
         features/AppPreferences/
         features/AiAndIntegrations/
         features/YourData/
   ```

3. Define routes for Collection Home, Discover, Show Detail keyed by provider/type-safe external identity, Person Detail, and Settings. Keep filter/mode state shareable through validated URL query parameters where it improves navigation; persist only the documented last selected filter and UI preferences on the server.
4. Make loading, provider-failure, no-result, no-media, and unauthenticated/dev-context errors intentional UI states. Support keyboard navigation, labelled controls, focus restoration after the removal dialog, semantic headings/landmarks, responsive layouts, reduced-motion preferences, and the configured readability scale.

## 7. Implement collection Home and universal overlay presentation

1. Build the navigation/filter panel with All Shows, generated tag filters, No tags only when it exists, data filters, persistent Discover and Settings entries, and the top media-type toggle. Reflect the selected filter in the Home response and persist the documented last-filter preference.
2. Render status sections in the required hierarchy: visually prominent/larger Active tiles; Excited (`Later + Excited`); Interested (`Later + Interested`); and a collapsible Other group. Supply distinct empty states for an entirely empty collection (CTA to Search/Ask) and a filter with no matches (“No results found”).
3. Build the shared show tile and response mapper once, then use it in Home, search, traditional recommendations, AI results, mentioned strips, and person credits. It must always merge the current user overlay over public catalog facts and show in-collection and user-rating indicators whenever applicable.
4. Keep mutations optimistic only with rollback/revalidation; server responses remain authoritative. After changes, invalidate/refetch all affected Home sections, current detail controls, tag filters, and tile instances so My Data remains consistent everywhere.

## 8. Implement Discover flows

1. Build a clear Search / Ask / Alchemy switcher. Honor the server-backed Search-on-Launch preference by opening Search at the appropriate entry point without preventing the user from changing modes.
2. Search: debounce user input accessibly, query the live catalog, display poster-grid results, overlay saved state, and navigate each selectable result to Show Detail. Provide a clear empty query/no-result/provider-failure experience.
3. Ask: render a welcome state with six randomly sampled starter prompts and a refresh action, accessible chat transcript, composer, loading/stream/error states, inline selectable mentions, and a horizontal mentioned-shows strip. Use the session manager to send contextual history and to cleanly reset when leaving or resetting.
4. Alchemy: provide a catalog/library search-and-select surface; prevent conceptualization until at least two unique shows are selected; fetch common concepts; permit one to eight selected chips; require a selection before ALCHEMIZE; render six resolved recommendation cards with reasons. Let users go back, and ensure changing selected shows or concepts clears all downstream concepts/results. “More Alchemy!” creates a new round using chosen results as inputs while retaining the same ephemeral session only.

## 9. Implement Show Detail as the personal relationship and discovery hub

1. Assemble the page in the specified narrative order: header media carousel (inline trailer when available, premium poster/logo fallback otherwise); core facts and community score; My Tags; overview plus Scoop; Ask-about CTA; genres/languages; traditional recommendation strand; Explore Similar; providers; Cast/Crew; TV seasons; movie budget/revenue. Omit or gracefully collapse inapplicable/missing sections.
2. Keep My Status/Interest toolbar chips, rating, and tags immediately reachable. Map Interested/Excited to Later plus interest; protect status re-selection with a confirmation dialog tied to the saved hide/count preference; make auto-save defaults visible through updated chips/toasts; and ensure deletion clears every My Data field, including Scoop.
3. Implement rating as an accessible labelled control with clear unset/unrated behavior. It must save an unsaved item as Done. Implement free-form tag picking/creation with deduplication and immediate filter refresh; it must save an unsaved item as Later + Interested.
4. Implement Scoop copy/state transitions (“Give me the scoop!”, “Show the scoop”, “The Scoop”), streaming/generating presentation, four-hour freshness checks, and the saved-versus-ephemeral persistence behavior.
5. Implement Explore Similar locally within the Detail feature: Get Concepts, select one or more ingredient chips with the agreed cap, Explore Shows, then show five mapped recommendations plus transient reasons. A change to selected concepts clears existing recommendations. The Ask-about handoff must carry the current show context rather than just navigating to empty Ask.

## 10. Implement Person Detail and optional-depth content

1. Map cast and crew cards from Show Detail into a typed Person Detail route. Fetch a gallery, bio, and credits; render safe fallbacks for sparse profiles and images.
2. Derive lightweight analytics from resolved filmography/catalog data: average project community ratings, top genres, and projects by year. Keep the chart calculations pure/testable and label charts with textual alternatives; do not invent ratings for unavailable credits.
3. Group filmography by year, display the same overlay-aware show tiles/cards for saved credits, and open the corresponding Show Detail on selection.

## 11. Verify behavior, quality, and operations

1. Unit-test pure domain services adjacent to source: status/interest transitions, implicit-save defaults, remove/clear semantics, tag normalization, per-field timestamp conflict selection, catalog `selectFirstNonEmpty` merge, filter/grouping rules, date/score formatting, provider-response normalization, structured mention parsing, and recommendation resolution.
2. Add Supabase-backed integration tests against a unique test namespace per invocation. Cover RLS/context enforcement, multi-user isolation in one namespace, cross-namespace isolation, atomic overlay updates, catalog-refresh preservation, migration forward compatibility, export contents, and a reset that proves no other namespace was touched.
3. Add route/API tests for validation failures, secret redaction, dev-identity gating, AI parse retry/fallback, four-hour Scoop rules, streaming error handling, and unresolved recommendation Search handoffs. Mock AI and catalog adapters deterministically; do not call paid/external providers in normal tests.
4. Add browser end-to-end coverage for the ten specified journeys: build collection, rate-to-save, tag-to-save, maintain data, tag filtering, Ask discovery, Explore Similar, Alchemy and chaining, person deep-dive, and ZIP backup. Add regression cases for status removal, no tags, empty filters, missing trailers, TV/movie conditional sections, cleared local storage, and reopened data from the backend.
5. Add visual/accessibility checks for the status hierarchy, Discover switcher, dense Detail page, dialogs, responsive layouts, keyboard-only workflows, loading/error states, and font-size settings. Run lint, type check, unit/integration tests, E2E tests, and a production build in CI.
6. Create a living AI quality harness using the supplied scoring rubric. Seed representative library contexts and evaluate Scoop, Ask, concepts, Explore Similar, and Alchemy for voice, taste alignment, surprise without betrayal, specific reasons, required counts, and deterministic real-show integrity. Block releases on unresolved/mismatched recommendation IDs; record scores and prompts/model versions without storing user conversation data.
7. Document local/cloud setup, environment variables, hosted Supabase migrations, development identity use and production restriction, namespace reset behavior, backup scope, adapter configuration, test commands, and the future OAuth replacement seam. Confirm the documented cloud path does not require Docker.

## Delivery checkpoints and acceptance traceability

1. **Foundation checkpoint:** app starts from `.env.example`, migrations apply to empty hosted Supabase, identity/namespace context is enforced, and `test:reset` is namespace-only.
2. **Data checkpoint:** catalog refresh, per-field overlay conflict resolution, implicit saves/removal, filters, settings, migration metadata, and export pass unit/integration coverage.
3. **Core product checkpoint:** Home, Search, overlay-aware tiles, Show Detail controls, and all conditional catalog content work against deterministic adapter fixtures.
4. **Discovery checkpoint:** Ask, Scoop, concept extraction, Explore Similar, and Alchemy meet their session-lifetime, count, parsing, mapping, and voice contracts.
5. **Completion checkpoint:** Person Detail, accessibility/responsive states, all stated user journeys, AI golden-set quality gate, lint/type/build, and hosted namespace-isolation tests pass. Re-run a saved-library scenario after client storage is cleared and after a forward migration to prove backend authority and data continuity.

## Decisions requiring product confirmation before expanding scope

- Whether clearing a rating should be an explicit stored “Unrated” sentinel or the specified nullable score (this plan uses nullable score plus a visible unset state).
- Whether Scoop generation should itself save an otherwise unsaved show (this plan keeps it ephemeral until another save trigger occurs).
- Exact provider choices, regional streaming defaults, and credential-storage policy for user-entered keys.
- Future semantics/UI for `Next`, named lists, Import/Restore conflict rules, and saved Alchemy sessions.

