# Implementation Plan — Personal TV & Movie Companion

## 1. Scope and implementation stance

Build the product as a new full-stack application from this documentation-only seed. Use the latest stable Next.js release with the App Router and TypeScript, and use Supabase through its official client libraries as the persisted backend. The application should remain provider-agnostic at its domain boundary: catalog and AI vendor requests, credentials, response decoding, and retries belong in server-side adapters rather than page features.

The backend is the source of truth. Browser query/cache state is allowed for responsiveness, but clearing local storage or reinstalling the client must not remove a library, settings, or My Data. The application is not offline-first.

Implement the current product scope only. Keep `Next` in the data model but do not make it a primary UI status. Do not implement Import/Restore, named custom lists beyond free-form tags, saved/shareable Alchemy sessions, or a full OAuth flow. Preserve seams for those later features without inventing their behavior.

Use the architectural conventions in `INSTRUCTIONS.md`: humble TSX components, feature-local hooks and utilities, no `index.tsx` entrypoints, no inline styles or magic visual values, and a fractal `pages → features → sub-features` structure.

## 2. Foundation, configuration, and execution boundary

1. Create the Next.js/TypeScript project baseline, package scripts, test setup, lint/type-check configuration, and production build configuration. Add the UI, validation, Supabase, ZIP-generation, streaming, and test dependencies only after selecting versions compatible with the chosen Next.js release.
2. Add `.env.example` with comments for every variable needed to run without source edits. At minimum cover:
   - `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_ANON_KEY` for browser-safe Supabase access;
   - `SUPABASE_SERVICE_ROLE_KEY` for server-only administrative/test operations;
   - stable `APP_NAMESPACE_ID`, a default development/test `DEV_USER_ID`, and an explicit runtime mode;
   - server-only catalog and AI provider keys, optional provider base URLs, and default AI model;
   - test namespace/reset settings and any allowed regional provider defaults.
3. Ensure `.gitignore` excludes `.env*` secrets while retaining `.env.example`. Keep server-only keys out of client modules, browser bundles, API responses, logs, error messages, exports, and prompt context. User-entered integration keys are optional; if the product permits syncing them, write them only through a protected server path and never return them after save.
4. Add documented scripts for starting the app, unit/integration tests, browser E2E tests, lint, type checking, production build, and `test:reset`. The primary cloud-agent path connects to hosted Supabase and does not require Docker; local Supabase/Docker may be documented as an optional convenience only.
5. Centralize environment parsing and domain constants in `src/config`. Fail fast with actionable startup errors for missing required deployment configuration while keeping user-configurable provider/model settings optional.
6. Create a request context resolver used by every server route and server action. It returns `{ namespaceId, userId, isTest, isDevelopmentIdentity }` before business logic runs. `namespaceId` is the stable build/run partition; `userId` is an opaque stable identifier.
7. Allow a documented dev/test identity injection mechanism, such as a guarded `X-User-Id` header with a configured default, only in development/test. Reject or ignore injected identities in production. Keep the context interface independent of the mechanism so a future OAuth adapter changes wiring, not the schema or repositories.
8. Use server-side repositories/service functions for all user-owned reads and writes. Apply Supabase RLS where practical and explicit `(namespace_id, user_id)` predicates everywhere. Never accept namespace or user ownership from an untrusted body as the authority.
9. Add a development/test reset endpoint and script. Require the configured namespace, delete only test-marked data in that namespace in dependency order, and prove with tests that another namespace and another user's records are untouched.

## 3. Supabase schema, migrations, and domain model

1. Add versioned, repeatable Supabase migrations plus deterministic fixtures. A fresh hosted database must be reproducible by applying migrations alone. Add foreign keys, check constraints, indexes for library/search paths, and uniqueness constraints for canonical catalog identity and user overlays.
2. Separate public catalog data from user-owned overlay data so catalog refreshes cannot overwrite another user's relationship. Use a relational shape equivalent to:
   - `namespace_users`: `(namespace_id, user_id)` registration/metadata;
   - `catalog_shows`: namespace-scoped canonical movie/TV identity, catalog provider/external IDs, media type, title, metadata, media URLs, language/genre data, scores/popularity, dates, movie facts, TV facts, provider-ID JSON, `creation_date`, and `details_update_date`;
   - `user_shows`: `(namespace_id, user_id, catalog_show_id)` overlay with nullable status/interest/score, per-field update timestamps, AI Scoop and timestamp, creation/update metadata, and `is_test`;
   - `user_show_tags`: normalized tag rows per overlay, plus a canonical tag-set update timestamp on the overlay for last-writer-wins behavior;
   - `user_settings`: username, AI model, optional integration configuration according to the key policy, and conflict/version metadata;
   - `user_ui_preferences`: font size, search-on-launch, removal-confirmation suppression/count, and last selected filter;
   - `app_metadata`: namespace/user data-model version and forward-migration metadata.
3. Put `namespace_id` on every namespace-owned record and both `namespace_id` and `user_id` on every user-owned record. Use composite keys/foreign keys and repository predicates so namespace isolation is structural, not a caller convention. Public catalog cache rows are still namespace-scoped and are never returned across namespaces.
4. Preserve the reference `Show` capabilities: movies versus TV, stable external IDs, title/name, overview/tagline/homepage, genres, original/spoken languages, poster/backdrop/logo/network images, community vote average/count/popularity, release/air dates, movie runtime/budget/revenue, TV status/season/episode counts and runtimes, provider availability, and management timestamps. Store provider IDs by country and fulfillment type (`flatrate`, `rent`, `buy`), not full provider display objects.
5. Keep re-pullable detail payloads transient: cast, crew, videos/trailers, image galleries, seasons, last episode, similar/recommended responses, and person credits are fetched/mapped for a response but are not persisted as catalog facts unless a later requirement explicitly adds that need.
6. Define stable provider/type-aware canonical identity, for example `(namespace_id, catalog_provider, external_id, media_type)`, and resolve duplicate saves to the same catalog row. Store all dates as timezone-aware timestamps and serialize exported dates as ISO-8601.
7. Implement catalog merge semantics in a domain service, not in UI code. For public fields use `selectFirstNonEmpty(new, old)`: a blank string/array or null refresh cannot erase known data. Set `details_update_date` on a successful refresh and set `creation_date` only on first creation. For user fields, use the newest per-field timestamp; catalog refreshes never win over My Data.
8. Define forward-only migrations and a versioned migration runner. Backfill safely, preserve overlays/timestamps, verify row counts and constraints, and advance `app_metadata` only after the migration succeeds. Never use destructive schema changes for routine upgrades.

## 4. Collection domain services and persistence rules

1. Make repositories and mutation services the only place that can create/update/delete a `user_shows` overlay. Every mutation accepts the resolved request context and a catalog identity, validates ownership and media type, and returns the authoritative merged show view model.
2. Define collection membership as a non-null assigned status. Support `active`, `later`, `wait`, `done`, `quit`, and hidden `next`. Selecting `interested` or `excited` always writes `status=later` plus the selected interest. Interest is only meaningful while status is `later`; preserve its historical value when changing away from Later if that is needed for a later return.
3. Implement implicit-save defaults exactly:
   - explicit status creates/updates the overlay;
   - an interest chip creates `Later + Interested` or `Later + Excited`;
   - rating an unsaved show creates it as `Done`;
   - adding the first tag to an unsaved show creates it as `Later + Interested`;
   - any other status-free save defaults to `Later + Interested`.
4. Implement rating as a validated nullable score with an explicit unset state. Clearing a rating removes the value and timestamp without deleting the overlay or changing its status. Validate the allowed range and preserve the user's rating indicator only when a value exists.
5. Normalize tags by trimming, rejecting empty values, deduplicating case-insensitively while preserving a display form, and updating the complete tag set atomically. Maintain the derived tag library and `No tags` filter from current overlays.
6. Implement status clearing/reselection as a destructive operation. Show confirmation unless the user's removal preference suppresses it; on confirmation delete the overlay, tag rows, status/interest, rating, and Scoop together. Track confirmation count and suppression preference server-side. Re-adding/upserting an item with an existing overlay must preserve its latest My Data and refresh only public facts; deliberate removal remains a full clear as specified.
7. Stamp each user field independently: status, interest, tag set, score, and Scoop. Use these timestamps for sorting, conflict resolution, sync merges, and Scoop freshness. Resolve concurrent saves per field with the newer timestamp; resolve tags as a last-updated complete set rather than merging stale individual rows.
8. Ensure every show response is a view-model join of current catalog facts and the current user's overlay. Use it for Home, Search, traditional recommendations, AI results, mentioned strips, credits, and Detail so collection/rating badges and My Data are consistent everywhere.
9. Add query services for the library, tag library, generated filter counts, and filter persistence. Support `all`, tags, `No tags`, genre, decade, community-score ranges, optional internal `myStatus`, and an independent `all | movie | tv` media toggle. Group matching results as Active, Excited (`Later + Excited`), Interested (`Later + Interested`), and collapsed Other (`Wait`, `Quit`, `Done`, and Later without interest), with sensible latest-relationship-first sorting.

## 5. Server APIs and external provider adapters

1. Define typed server contracts and validation schemas before connecting UI features. Keep Next route handlers thin: resolve context, validate input, call a service, map errors, and return a safe response. Business rules and provider-specific decoding stay outside route files.
2. Create a catalog adapter interface for title/keyword search, movie/TV detail refresh, deterministic logo selection, images/videos/trailers, credits/person lookup, provider availability, TV seasons, traditional recommendations/similar titles, and the catalog facts needed for person analytics. Normalize vendor payloads into the canonical domain model and convert absent media to valid empty/transient states.
3. Add catalog/search and detail services that search the live catalog, upsert merged public metadata, and apply the current user's overlay. Validate media type and external IDs at the route boundary; never let provider errors expose credentials or raw vendor internals.
4. Add library endpoints for grouped filtered results, counts, tags, and last-filter preferences. Add narrowly scoped mutations for status/interest, nullable rating, complete tag sets, and Scoop persistence; enforce ranges, ownership, confirmation state, and tag rules on the server.
5. Add settings endpoints for username, readability/font-size token, search-on-launch, AI model, and optional integration settings. Return redacted settings only. Deployment-provided credentials remain server-only; user-entered key storage must be explicit, protected, and documented.
6. Add person endpoints that fetch a gallery, bio, credits, and catalog facts for analytics without persisting transient person payloads. Add recommendation endpoints for traditional recommendations, concept generation, Explore Similar, Alchemy, and Ask using the AI services below.
7. Add `Export My Data` as an authenticated server stream. Collect only the current namespace/user's saved overlays and the product-required settings, serialize a versioned JSON backup with ISO-8601 dates, package it as a `.zip` with a safe filename, and exclude API keys, secrets, chat history, Alchemy results, and other transient sessions. Validate the archive schema in automated tests.

## 6. AI provider boundary and discovery services

1. Define server-only AI provider and prompt-context interfaces. The context builder sends minimal current-library public facts plus My Data, selected show/concept context, and only active Ask turns. Keep model/provider selection in configuration/settings, not in page components. Record model/prompt versions in non-sensitive quality telemetry, never user conversation data.
2. Centralize shared guardrails and persona: warm, chatty TV/movie nerd; specific, opinionated, honest, vibe-first, spoiler-safe by default, and willing to redirect non-TV/movie questions back into the domain. Search remains a straightforward non-AI experience.
3. Implement Ask with a typed response contract containing `commentary` and exact `showList` entries in `Title::externalId::mediaType;;...` format. Validate model output, parse defensively, retry once with stricter formatting instructions, then preserve safe commentary and provide Search handoffs if the structured list remains invalid. Do not include external IDs in visible commentary.
4. Keep Ask transcript, mentioned-show strip, and summaries in feature/session memory only. Retain recent turns and, after approximately ten messages, replace older turns with a one-to-two-sentence summary that preserves persona and useful taste context. Resetting Ask or leaving it clears the session. Ask-about-show passes exact current-show context and a handoff marker.
5. Implement a centralized recommendation resolver used by Ask, Explore Similar, and Alchemy. Prefer supplied external ID, but accept it only when the first resolved catalog title matches case-insensitively and media type is valid. Otherwise perform a constrained title/type search. Only validated real catalog items are interactive; unresolved or mismatched entries are visibly non-interactive with an accessible Search action. Preserve AI reasons as transient view data.
6. Implement Scoop as a structured, stream-capable response with a 150–350 word mini taste blog: clear personal take, honest stack-up, emotionally central Scoop paragraph, practical fit/warnings, and a Worth-it verdict. Show generating/progressive states. Cache for four hours; regenerate after expiry; persist only when the show is already in the collection, otherwise keep the result in the active Detail session.
7. Implement concept generation for a single show and for 2+ Alchemy inputs. Return eight default concepts for single-show flows, bullet-only, spoiler-free, one-to-three words, specific and evocative rather than generic. Cover varied axes such as structure, vibe, emotional palette, relationships, and craft; order by strongest aha. Multi-show concepts must be shared across all inputs and may use a larger candidate pool while the UI caps selection at eight.
8. Implement concept-based recommendations with selected concepts explicit in the prompt and each reason. Return exactly five Explore Similar recommendations and six Alchemy recommendations, biasing toward newer titles without excluding classics/hidden gems. Reasons should be concise, specific, and name the matched concepts; do not emit generic synopses.
9. Require Alchemy to select at least two unique input shows, then Conceptualize, choose one through eight concepts, and ALCHEMIZE. Keep results/reasons session-only. Changing inputs or concepts clears downstream concepts/results; Back is supported; More Alchemy starts a new ephemeral round using chosen results as inputs and retains no reusable session.
10. Add deterministic AI quality validation against the supplied rubric: voice, taste alignment, surprise without betrayal, specificity, and real-show integrity. Enforce Voice ≥1, Taste ≥1, Real-show integrity =2, and total ≥7/10 for the harness; treat wrong/mismatched IDs and hallucinated shows as hard failures.

## 7. Shared UI system and route shells

1. Create `src/theme` tokens for colors, typography, spacing, radii, elevation, breakpoints, reduced motion, and XS–XXL readability scales. Create accessible shared primitives in `src/components`: buttons, chips, segmented mode controls, dialogs, poster tiles, horizontal strands, sliders, forms, streaming panels, and intentional loading/empty/error states.
2. Keep styling in the theme/style system. TSX should contain markup and binding only; extract data loading, mutations, state machines, parsing, and event logic into feature-local hooks/utils. Define constants outside TSX and co-locate tests with critical feature logic.
3. Use thin App Router entries in `src/app` for layout, metadata, route params, loading, and error boundaries. Place product behavior in this fractal structure:

   ```text
   src/
     config/
     theme/
     components/
     hooks/
     utils/
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
4. Provide routes for Home, Discover, Show Detail keyed by provider/type-safe identity, Person Detail, and Settings. Use validated URL query parameters for shareable filter/mode state where useful; persist only the documented last filter and UI preferences on the server.
5. Implement semantic headings/landmarks, labelled controls, keyboard navigation, focus restoration after confirmation dialogs, reduced-motion behavior, responsive layouts, font-size changes, and deliberate loading/provider-failure/no-result/no-media/dev-context error states.

## 8. Collection Home and universal overlay presentation

1. Build persistent navigation with All Shows, generated tag filters, conditional No tags, genre/decade/score filters, the media toggle, Discover, and Settings. Restore and persist the last selected filter without making local storage authoritative.
2. Render Active with prominent larger tiles, then Excited, Interested, and a collapsible Other section. Provide an empty-library CTA to Search/Ask and a distinct `No results found` state for an otherwise non-empty library with no filter matches.
3. Build one overlay-aware Show Tile/response mapper and reuse it in Home, Search, recommendations, Ask mentions, Alchemy, Person credits, and Detail. Show poster/title, in-collection badge when status exists, rating badge when a score exists, tags/relationship details where appropriate, and safe poster fallbacks.
4. Use optimistic updates only with rollback and authoritative server revalidation. After mutations invalidate Home sections, Detail controls, tag/filter counts, and all tile instances so status, tags, ratings, and Scoop remain consistent.

## 9. Discover, Search, Ask, and Alchemy UI

1. Build an accessible Search/Ask/Alchemy switcher. Honor Search-on-launch at the appropriate entry point while allowing a user to switch modes freely.
2. Search debounces live title/keyword queries, displays poster-grid results with collection/rating markers, handles empty query/no result/provider failure, and navigates selectable entries to typed Show Detail. Search copy stays catalog-oriented, without AI persona styling.
3. Ask provides a welcome view with six randomly sampled starter prompts and refresh, a keyboard-accessible chat transcript/composer, loading/stream/error states, inline mentions, horizontal mentioned-show tiles, Search handoffs, reset behavior, and session cleanup when leaving. Mention tiles use the central resolver and the same overlay-aware tile mapper.
4. Alchemy provides catalog/library search-and-select, enforces at least two unique inputs before conceptualization, shows shared concepts and the “pick the ingredients you want more of” guidance, caps selected concepts at eight, requires at least one selection before ALCHEMIZE, and renders six resolved recommendation cards with concept-specific reasons. Backtracking and input/concept reset behavior must be explicit; More Alchemy chains from selected results.

## 10. Show Detail and relationship hub

1. Preserve the narrative order: header media carousel; core facts/community score; My Tags; overview plus Scoop; Ask-about CTA; genres/languages; traditional recommendation strand; Explore Similar; providers; Cast/Crew; TV seasons; movie budget/revenue. Hide or collapse inapplicable sections without breaking the page.
2. Make the header cinematic with inline trailer when available and premium poster/backdrop/logo fallback when media is missing. Surface year, runtime or TV season/episode facts, community score, My Rating, and toolbar relationship controls within the first scan.
3. Keep status/interest chips in the toolbar, map Interested/Excited to Later, and save explicit statuses. Reselecting the active status follows the confirmation/removal preference and clears every My Data field after confirmation. Make rating a labelled accessible control with clear null/unrated behavior; rating an unsaved item saves as Done. Tag creation/picking saves an unsaved item as Later + Interested and refreshes filters immediately.
4. Implement Scoop labels and transitions: `Give me the scoop!` when absent, `Show the scoop` when cached, and `The Scoop` when open. Show generating/progressive output, four-hour freshness, errors/retry, and saved-versus-ephemeral persistence. The Ask-about CTA seeds the current show context rather than opening an empty chat.
5. Implement traditional recommendation strands as a non-AI path, Explore Similar as Get Concepts → select one or more chips within the shared cap → Explore Shows → five mapped recommendations, providers by region/fulfillment, person-linked cast/crew, TV-only seasons, and movie-only financials. Missing data must collapse safely.

## 11. Person Detail, Settings, and export

1. Map cast/crew cards into a typed Person Detail route. Render gallery, name, bio, and safe sparse-profile fallbacks. Compute analytics with pure/testable functions: average available project community ratings, top genres, and projects by year; never invent ratings for missing credits. Provide textual alternatives for charts.
2. Group filmography by year, use overlay-aware show cards for saved credits, and open the canonical Show Detail for every selectable credit. Unresolved credits receive a safe non-interactive/search state.
3. Build Settings sections for readability/font size, Search-on-launch, username, AI model, optional AI/catalog integrations, and Your Data. Validate values, persist synchronized settings server-side, keep UI preference defaults intentional, and redact keys in reads and exports.
4. Implement Export My Data from the Settings page with progress/error/success states and a deterministic archive schema. Verify the ZIP contains saved shows and required My Data/settings, uses ISO-8601 dates, contains a schema/model version, and contains no secrets or session-only AI data. Leave Import/Restore out until validation/conflict/overwrite semantics are specified.

## 12. Verification, operations, and delivery sequence

### Test strategy

1. Unit-test pure domain logic adjacent to source: status/interest transitions, membership, implicit-save defaults, nullable rating behavior, removal clearing, re-add/upsert preservation, tag normalization, grouping/filter counts, per-field timestamp conflict resolution, catalog `selectFirstNonEmpty` merge, provider normalization, date/score formatting, concept constraints, mention parsing, and recommendation resolution.
2. Add Supabase-backed integration tests with a unique test namespace per invocation. Cover migrations from empty state, RLS/context enforcement, two users in one namespace, cross-namespace isolation, catalog refresh preserving overlays, atomic overlay/tag deletion, forward migration continuity, ZIP contents, and namespace-only reset.
3. Add route/service contract tests for invalid media IDs/types, range and tag validation, secret redaction, production rejection of dev identity injection, provider failures, AI parse retry/fallback, Ask summarization threshold, Scoop four-hour behavior, stream interruption, unresolved recommendation Search handoff, and settings conflicts. Mock catalog/AI adapters; normal tests must not call paid external services.
4. Add browser E2E coverage for the ten journeys: build collection, rate-to-save, tag-to-save, maintain collection, tag filtering, Ask discovery/save, Explore Similar/save, Alchemy/chaining, person deep-dive, and ZIP backup. Add regressions for status removal, No tags, empty filter, missing trailer/backdrop, TV/movie conditional sections, cleared local storage, and reopening data from Supabase.
5. Add visual/accessibility checks for status hierarchy, mode switcher, dense Detail layout, responsive breakpoints, font-size settings, dialogs/focus, keyboard-only actions, streaming/loading/error/empty states, and reduced motion. Run lint, type check, unit/integration tests, E2E tests, and production build in CI.
6. Add a living AI quality harness with representative library/My Data contexts. Score Scoop, Ask, Concepts, Explore Similar, and Alchemy for voice, taste alignment, surprise without betrayal, specificity, required counts, spoiler safety, and real-show integrity. Store prompts/model versions and aggregate scores without user conversation content; block release on wrong or mismatched recommendation IDs.

### Delivery checkpoints

1. **Foundation:** the app starts from `.env.example`; hosted Supabase migrations apply; context, namespace, user isolation, dev identity gating, and namespace-only reset are verified; no Docker is required.
2. **Data:** catalog normalization/merge, public-vs-user separation, implicit saves, status removal, per-field conflict rules, filters, settings, migrations, and export pass unit/integration tests.
3. **Core product:** Home, Search, overlay-aware tiles, Detail relationship controls, traditional recommendations, providers, credits, and conditional media content work against deterministic adapters.
4. **Discovery:** Ask, Scoop, concepts, Explore Similar, and Alchemy meet format, count, mapping, streaming/session, context, and voice contracts.
5. **Completion:** Person Detail, accessibility/responsive states, all ten journeys, AI quality gate, lint/type/build, and hosted namespace-isolation tests pass. Re-run a saved-library scenario after clearing client storage and after a forward migration to prove backend continuity.

## 13. Decisions and explicit follow-ups

- Use nullable rating plus a visible unset state unless product confirms a stored `Unrated` sentinel.
- Keep Scoop ephemeral for an unsaved show; only persist it when the show is already in the collection.
- Keep `Next` modeled but hidden from primary navigation until its UI semantics are confirmed.
- Treat free-form tags as the only custom lists for this release.
- Confirm catalog/streaming/AI vendors, region defaults, user-entered-key storage policy, exact Search-on-launch default, and trailer playback constraints before production configuration.
- Do not add Import/Restore, saved Alchemy sessions, or social features until their conflict and privacy rules are specified.
