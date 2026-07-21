# Implementation Plan: Personal TV and Movie Companion

## 1. Objective and delivery boundaries

Build a responsive, accessible personal entertainment companion that combines a durable user library with catalog search, show and person detail pages, conversational discovery, concept-based discovery, settings, and data export. The application will use the latest stable Next.js release available when implementation begins and Supabase through its official client library. Supabase is the authoritative store; browser state is either a cache or explicitly session-only.

This plan covers the full required product in `docs/prd/` and the benchmark infrastructure rider. It does not implement any of the product during the planning step.

### Required outcomes

- Users can create and maintain a collection through status, interest, tag, and rating actions, with the specified implicit-save and removal behavior.
- The user's overlay is merged into every catalog representation of a saved show.
- Home, Search, Ask, Alchemy, Show Detail, Person Detail, Settings, and Export work as coherent end-to-end journeys.
- Ask, Scoop, Explore Similar, and Alchemy share one spoiler-safe, warm, specific, opinionated AI persona.
- AI recommendations are resolved to real catalog shows before they become interactive.
- Every user-owned row is partitioned by a stable `(namespace_id, user_id)` pair.
- A fresh database can be migrated deterministically, destructive tests reset only their namespace, and no workflow requires Docker.
- The application is lint-clean, type-safe, tested at domain, integration, browser, contract, accessibility, and visual levels.

### Scope decisions for documented open questions

These decisions keep the first build unambiguous without turning optional ideas into hidden requirements:

- Keep `Next` in the status type and database constraint, but do not expose it as a first-class status or Home section.
- Use free-form tags as the only custom-list mechanism; do not add named lists.
- Generating a Scoop for an unsaved show does not save it. The result remains in current page memory only.
- Clearing a rating stores a `null` value with a fresh score timestamp while the show remains saved. This distinguishes a deliberate clear during field-level conflict resolution without inventing a visible "Unrated" value.
- Deliver Export, but defer Import/Restore. Make the backup versioned so a future importer can consume it.
- Do not persist or share Ask or Alchemy sessions, and do not add a Detail-page Alchemy entry.
- Do not expose a `myStatus` sidebar filter in the first release; the Home grouping already provides that view.
- Collection and normal preferences sync naturally through the server-backed data model. Offline-first editing and a separate sync engine remain out of scope.
- Support environment-injected provider credentials as the mandatory benchmark path. If editable credential fields are included in Settings, handle them as write-only encrypted server data; never return plaintext credentials to the browser or include them in exports.

Items whose values are not specified by the PRD (rating scale, removal-prompt suppression threshold, community-score buckets, default watch region, and provider/model identifiers) will live in typed configuration with documented defaults, rather than becoming scattered magic numbers. Product QA can change those values without rewriting feature logic.

## 2. Architecture

### 2.1 Runtime and trust boundaries

Use a browser -> Next.js server -> external provider/Supabase flow:

1. Client components render interactive controls and call same-origin route handlers or server actions.
2. A server-side identity resolver derives `namespace_id` and `user_id`; feature code never accepts a namespace supplied by the browser.
3. Server application services enforce domain rules and call repositories or provider adapters.
4. A Supabase repository stores collection and preference data. Catalog and AI adapters call their configured providers only from the server.
5. Responses are normalized into provider-neutral domain models, overlaid with saved My Data, and returned to the UI.

Do not initialize an elevated Supabase client in any client bundle. If browser-side Supabase is later introduced, it may use only the anon/public key and RLS-protected access. The benchmark implementation can keep all database calls server-side with a server-only service credential and deny direct anonymous access to user-owned tables.

### 2.2 Code organization

Follow the repository's fractal architecture while accommodating Next.js framework filenames:

```text
src/
  app/                         # framework-required route/layout/loading/error adapters
    page.tsx
    find/page.tsx
    shows/[mediaType]/[externalId]/page.tsx
    people/[personId]/page.tsx
    settings/page.tsx
    api/.../route.ts
    _pages/                    # private, non-route architectural page modules
      CollectionHome/
        CollectionHome.tsx
        hooks/
        features/
      FindDiscover/
        FindDiscover.tsx
        features/SearchMode/
        features/AskMode/
        features/AlchemyMode/
      ShowDetail/
        ShowDetail.tsx
        features/HeaderMedia/
        features/RelationshipToolbar/
        features/Scoop/
        features/ExploreSimilar/
        ...
      PersonDetail/
      Settings/
  config/                      # env parsing, product constants, feature flags
  theme/                       # tokens, typography scale, responsive rules
  components/                  # shared primitives only
  hooks/                       # genuinely cross-feature hooks only
  utils/                       # genuinely cross-feature pure functions only
  server/
    identity/
    domain/
    repositories/
    services/
    providers/catalog/
    providers/ai/
    export/
  types/
supabase/migrations/
scripts/
tests/
```

The route files under `src/app` are thin framework adapters. `_pages` is a Next.js private folder, so it implements the architectural Page -> Feature -> Sub-Feature hierarchy without accidentally activating a second Pages Router. Page modules and visible features use matching directory/file names and contain their own hooks, child features, utilities, tests, and constants. TSX remains humble: markup and bindings live in components; state transitions, data fetching, parsing, analytics transforms, and handlers live in hooks or pure services. There are no feature barrel `index.tsx` files, inline styles, hard-coded colors, or ad hoc pixel values.

### 2.3 Domain boundaries

Keep the following boundaries independently testable:

- `identity`: resolves and validates namespace/user context.
- `library`: collection membership, My Data commands, defaults, deletion, filters, grouping, merge semantics, and export.
- `catalog`: provider-neutral search/detail/person models, normalization, metadata refresh, recommendation lookup, and watch providers.
- `discovery`: taste-context construction, Ask sessions, prompt contracts, concept selection, recommendations, and catalog resolution.
- `settings`: preferences, username, credential-source status, model selection, and local presentation state.
- `presentation`: page/feature modules consuming typed use cases rather than provider payloads.

External catalog and AI implementations sit behind interfaces so tests can use deterministic fakes and a provider can be changed without changing domain or UI code.

## 3. Configuration, identity, and execution

### 3.1 Environment contract

Create a checked-in `.env.example` with short comments for, at minimum:

- Supabase URL, anon/public key where applicable, and a clearly server-only service credential.
- Stable application namespace ID.
- development identity flag and default development user ID.
- catalog provider name, server-side API key, optional base URL, and default watch region.
- AI provider name, server-side API key, and default model.
- optional server-side encryption key for user-entered provider credentials.
- guarded test-reset flag and test namespace variables.

Parse and validate environment variables once in `src/config`; expose separate server-only and public configuration modules so secrets cannot cross the client boundary. Production startup must fail clearly for missing required values. `.gitignore` must ignore `.env*` while explicitly retaining `.env.example`.

### 3.2 Identity resolution

- Define an opaque `RequestIdentity { namespaceId, userId }` used by all user-owned services and repositories.
- Treat the configured namespace as process/build configuration, not a URL, form field, cookie, or user-selectable concept.
- In development/test only, allow a fixed user or `X-User-Id` test header when an explicit identity-injection flag is enabled. Reject this mechanism in production regardless of a supplied header.
- Upsert the namespace/user registration record on first valid use or provide a deterministic seed script.
- Put identity resolution at the server entry boundary and require identity as the first repository argument, making an unscoped read or write difficult to express.
- Keep user IDs provider-neutral. A future OAuth resolver will map an authenticated subject to the same opaque user ID without changing collection table keys.

### 3.3 Commands and documentation

Provide documented scripts for:

- install/start/development and production build/start;
- lint, format check, typecheck, and test;
- focused unit, integration, AI-contract, and browser tests;
- applying migrations to a fresh database;
- resetting test data for one explicit namespace.

`npm test` should run the stable automated suite appropriate for CI. The reset command must require an explicit namespace, refuse blank/wildcard/known production values, require a non-production reset flag, print its target, and delete only rows matching that namespace. Docker-based local Supabase instructions may be optional, but the primary README path uses a provided hosted Supabase project.

## 4. Persistent data design and migrations

### 4.1 Tables

Use forward-only Supabase SQL migrations for the following conceptual schema. Exact SQL names may follow project conventions, but the ownership and constraints are mandatory.

#### `namespaces`

- Stable namespace ID and creation timestamp.
- Exists to establish the build partition and support scoped cleanup.

#### `app_users`

- Composite key `(namespace_id, user_id)`.
- Username (initialized to a generated friendly name on first use) and created/updated timestamps.
- Foreign key to `namespaces` with intentionally reviewed deletion behavior.

#### `user_preferences`

- Composite key `(namespace_id, user_id)` and foreign key to `app_users`.
- Font-size token, Search-on-launch flag, selected AI provider/model, removal-confirmation preference/count, settings version, and updated timestamp.
- Prefer backend persistence for meaningful preferences so clearing browser storage does not erase them. Keep only navigational/transient state, such as the active URL filter, in URL or disposable browser state.

#### `user_secrets` (only if editable credentials are delivered)

- Keyed by `(namespace_id, user_id, secret_kind)`.
- Encrypted value, algorithm/key version metadata, and updated timestamp.
- Readable only by server credential-resolution code. API responses expose only `configured` and `source`, never ciphertext or plaintext.
- Environment credentials remain the benchmark fallback and are never written to the database.

#### `library_items`

- Composite identity `(namespace_id, user_id, catalog_provider, external_id, media_type)`; foreign key to `app_users`.
- Required title and media type; external IDs JSON; normalized catalog metadata for overview, genres, dates, images, language, ratings/popularity, movie fields, TV fields, and provider-ID availability by region.
- `my_status` plus `my_status_updated_at`; status is non-null while a row represents collection membership.
- `my_interest` plus `my_interest_updated_at`.
- `my_tags` text array plus `my_tags_updated_at`.
- nullable `my_score` plus `my_score_updated_at`.
- nullable `ai_scoop` plus `ai_scoop_updated_at`.
- catalog-details refresh timestamp, immutable creation timestamp, and `is_test` marker.
- Constraints for supported media/status/interest/font values and the configured rating domain.
- Indexes beginning with `(namespace_id, user_id)` for every read path, followed as useful by status, interest, media type, update timestamp, release date, community score, and GIN indexes for tags/genres.

Do not persist cast, crew, seasons, image galleries, videos, traditional recommendations, similar titles, Person detail, Ask turns, mentioned-show strips, concepts, Explore results, or Alchemy state. These are provider-refreshable or session-only by specification.

### 4.2 Security and isolation

- Enable RLS on user-owned tables and deny direct anonymous access. In the benchmark server-proxy design, only server code uses the elevated client.
- Make every repository query include both namespace and user predicates, even when filtering by a globally unique external ID.
- Add composite foreign keys so child records cannot cross ownership partitions.
- Centralize repository construction around a required identity instead of allowing raw Supabase access throughout features.
- Add integration tests proving that same-user/different-namespace and same-namespace/different-user requests cannot observe, edit, export, or reset one another's data.
- Treat namespace-wide reset as a test/admin script, not an application endpoint exposed in production.

### 4.3 Catalog merge and data continuity

Create a pure catalog merge function and transactional repository operation:

- Match durable items by provider, external ID, and media type; use alternate external IDs only through an explicit deterministic mapping table/function, never title alone.
- For public catalog fields, accept a new non-null/non-empty scalar or collection; retain the stored value when the provider response is null or empty.
- Preserve creation time and set details-refresh time after a successful merge.
- Resolve each My Data value independently by its paired timestamp; a newer null/empty value is still an intentional edit.
- Never allow a public refresh to modify My Data or Scoop.
- Detect duplicate rows during migrations and merge them transactionally by the same field/timestamp rules before adding the final unique constraint.

Every schema change ships with a forward migration, safe backfills, and migration tests using representative older snapshots. Destructive column removal happens only after data has been copied and verified. Export files carry their own schema version independently of database migration numbers.

## 5. Library domain rules

Implement collection mutations as explicit commands in a single domain service or database transaction. Avoid generic patch endpoints that can bypass defaults.

| User command | Unsaved show | Already-saved show |
|---|---|---|
| Select `Active`, `Done`, `Quit`, or `Wait` | Create the item with that status; leave interest irrelevant/null unless supplied | Update only status and status timestamp; preserve interest for possible later reuse |
| Select `Interested` | Create as `Later + Interested` | Set status `Later`, interest `Interested`, and both timestamps |
| Select `Excited` | Create as `Later + Excited` | Set status `Later`, interest `Excited`, and both timestamps |
| Rate | Create as `Done`, set score/timestamp | Update only score/timestamp; never change existing status |
| Add first tag | Create as `Later + Interested`, set tags/timestamp | Update tags/timestamp only |
| Edit/remove tags | Not applicable unless adding at least one | Store the normalized set, including empty, with a new tags timestamp; do not remove collection membership |
| Clear rating | Does not create a show | Store null plus a new score timestamp |
| Reselect active status/interest chip | No action | Ask for removal confirmation unless suppressed; on approval delete the item and all My Data/Scoop |

Additional rules:

- Trim tags, reject empty-only values, and deduplicate case-insensitively while retaining a stable display spelling. Derive the personal tag library from saved items, including `No tags` only when at least one item has none.
- Deleting membership deletes the entire `library_items` row; no user annotations survive re-addition. If the same show is encountered while still saved, preserve all My Data and refresh only usable public metadata.
- Use server timestamps for committed updates. Return the committed row so optimistic UI reconciles to the source of truth.
- Where simultaneous clients edit different fields, field timestamps preserve both changes. For edits to the same field, latest server timestamp wins.
- Put rating range/step, removal-warning threshold, status labels, and filter buckets in typed configuration. Validate them both server-side and in accessible controls.
- Implement one `overlayCatalogShows` operation used by Search, Home, recommendations, mentioned shows, filmography credits, and Detail. It bulk-loads saved rows and ensures user values always replace catalog-only values.

## 6. External catalog layer

### 6.1 Provider-neutral models and adapter

Define an adapter supporting:

- text search with media type and stable external IDs;
- movie/TV detail, images/logos/backdrops, trailers, genres/languages, dates, runtime or season/episode counts, scores, budget/revenue, and external IDs;
- watch-provider IDs grouped by region and monetization type;
- credits, Person biography/images, and full credits;
- traditional similar/recommended shows;
- batch or individual ID lookup used for AI recommendation resolution.

Normalize provider payloads at the adapter edge. Reject items lacking a title, stable external ID, or resolvable movie/TV type. Parse dates defensively, select the best English-preferred logo deterministically, retain only provider IDs in saved snapshots, and attach transient detail-only collections without persisting them.

### 6.2 Real-show resolution

Use one resolver for Ask mentions, Explore Similar, and Alchemy:

1. Parse/validate AI title, external ID if present, and media type.
2. If an external ID exists, fetch that item and accept it only if its normalized title equals the AI title case-insensitively and media type agrees.
3. If no valid ID is available, search by title/media type and choose the first case-insensitive exact title match.
4. Normalize the result and apply the user's overlay in a bulk pass.
5. If no match is safe, retain the title/reason as non-interactive text and offer a Search handoff prefilled with the title.

Never make a card navigable from an AI-provided ID alone. Preserve AI reasons as transient presentation data, not part of the saved show.

### 6.3 Failure behavior

- Translate provider authentication, quota, timeout, malformed response, and not-found failures into typed application errors.
- Give Search/Detail retry states and retain the user's query/selection when safe.
- Use live queries; do not make correctness depend on preloading or a client catalog cache.
- Refresh the stored public snapshot opportunistically when a saved show is opened or re-encountered, using the merge policy above.

## 7. Shared AI platform

### 7.1 AI gateway and taste context

Create a server-only AI adapter with streaming and structured-output capabilities. A shared prompt builder supplies:

- the common persona: warm TV/movie nerd friend, 70/30 friend/critic, joy-forward, honest, vibe-first, concise by default, and spoiler-safe unless explicitly invited;
- an explicit TV/movie-only boundary;
- a compact taste profile built from saved titles and My Data, prioritizing directly relevant tags/titles plus strong ratings and recently updated items when the full library exceeds a documented token budget;
- current show, selected concepts, or recent chat context as required by the surface;
- surface-specific output schema and length constraints.

Do not send credentials, internal database IDs, namespace IDs, or unnecessary personal settings to the model. Log latency, provider/model, token/usage metadata when available, validation outcome, retry count, and catalog-resolution rate, but do not log secrets or full private prompts/responses by default.

### 7.2 Structured output and recovery

- Validate every non-streamed model response with a runtime schema before using it.
- For Ask mentions, require exactly `{ commentary, showList }`, where `showList` follows `Title::externalId::mediaType;;...`; commentary must not expose IDs. Parse delimiters strictly and correlate entries with titles actually mentioned.
- For concepts, require bullet-only 1-3 word items, no explanations, no duplicates, and no obvious generic placeholders.
- For concept recommendations, require title, external ID when available, media type, concise reason, and the selected concepts represented by that reason.
- On schema/format failure, retry once with a stricter repair instruction. If repair fails, preserve safe unstructured commentary where applicable and provide Search fallback instead of crashing.
- Treat catalog resolution as a second validation gate. A syntactically valid AI item is not interactive until real-show resolution succeeds.

### 7.3 Ask sessions

- Keep Ask state in the Find/Ask feature's in-memory session store. Switching away, navigating away, or choosing Reset clears turns, summary, and mentioned shows.
- Show six random, non-repeating starter prompts from a maintained prompt library; Refresh chooses another six.
- Send the compact taste profile, persona, prior summary, and recent turns with each message.
- At roughly ten messages, summarize older turns into one or two conversational, persona-consistent sentences, retain the most recent turns verbatim, and continue from the new context window.
- Stream/display the answer as appropriate, render multi-recommendation lists for scannability, and build the mentioned-show strip from the validated structured list.
- `Ask about this show` navigates to Ask with an in-memory/URL-safe handoff containing only provider/media/external identity. The server fetches canonical context; the UI visibly indicates which show anchors the conversation.
- If a user explicitly asks for spoilers, record that permission for the relevant turn/session; otherwise prompts and rendering remain spoiler-safe.

### 7.4 Scoop

- Check for a saved Scoop newer than four hours and return it immediately when present.
- Otherwise stream generation progressively with visible `Generating...`, cancel handling, retry, and an assembled final response.
- Require a 150-350 word mini-review containing a stance, honest reception stack-up, a prominent Scoop centerpiece, fit/warnings, and a `Worth it?` verdict.
- Recheck collection membership before persistence. Save the final Scoop/timestamp only for a show already in the collection; an unsaved result remains feature memory and disappears on navigation.
- Public metadata refresh cannot overwrite Scoop. A removal deletes it with the row.

### 7.5 Concepts and recommendations

- Single-show Explore generates eight diverse concepts by default.
- Multi-show Alchemy generates a larger candidate pool (for example, twelve) shared by every selected input; UI selection remains capped at eight.
- Validate concepts across structure, vibe, emotional palette, relationship dynamics, and craft so the list is not eight synonyms. Keep strongest concepts first.
- Explore Similar accepts one to eight selected concepts and asks for exactly five recommendations.
- Alchemy requires at least two input shows, accepts one to eight concepts, and asks for exactly six recommendations.
- Reasons are one to three sentences, explicitly connect selected concepts, and are not synopses. Prompts bias toward recent work but permit classics and hidden gems and request one or two defensible surprises.
- Resolve all returned items through the catalog and overlay pipeline. Render unresolved entries as non-interactive/Search handoffs without counting them as valid real-show successes in quality metrics.

### 7.6 Discovery quality suite

Create deterministic mocked contract fixtures plus an opt-in live-model evaluation harness. Score representative Scoop, Ask, Concepts, Explore, and Alchemy outputs against voice, taste alignment, surprise, specificity, and real-show integrity. Enforce the documented threshold (voice and taste at least acceptable, real-show integrity perfect, total at least 7/10), exact count/length rules, spoiler red-team cases, off-domain redirection, malformed structured output, wrong IDs, mixed-reception honesty, and catalog fallback. Keep golden scenarios versioned and expand them when regressions are found.

## 8. Application shell and shared presentation

### 8.1 Shell and navigation

- Build a responsive shell with persistent Filters/Navigation and Settings/Find entry points. Use a sidebar on wide screens and an accessible drawer or equivalent on narrow screens.
- The main routes are Collection Home, Find/Discover, Show Detail, Person Detail, and Settings.
- Make the Find mode switcher explicit and deep-linkable (`Search`, `Ask`, `Alchemy`) while ensuring session-only state is cleared according to product rules.
- On launch, respect Search-on-launch by routing to Find/Search without creating redirect loops; otherwise show Home.
- Keep selected collection filter and media type in URL search parameters so navigation/back behavior is predictable. Treat any browser copy as disposable.

### 8.2 Design system and accessibility

- Define semantic color, spacing, typography, elevation, size, focus, and motion tokens in `src/theme`; map six font-size preferences to a consistent root scale.
- Build shared buttons, chips, score/rating controls, poster tiles, horizontal strands, dialogs, empty/error/skeleton states, carousels, chart wrappers, and visually hidden announcements only when they are reused across features.
- Ensure keyboard navigation and visible focus for mode tabs, chips, grids, dialogs, carousels, and sliders; use correct labels and pressed/selected semantics.
- Announce streamed AI progress and mutation results without flooding screen readers. Restore focus after modal close and route transitions.
- Provide alt/fallback treatment for missing art, captions/labels for inline trailers, reduced-motion behavior, contrast compliance, touch targets, and responsive layouts.
- Use feature-level loading/error boundaries so a failed recommendations or AI section does not blank an otherwise usable Detail page.

### 8.3 Shared show rendering

All tiles accept the same overlaid show view model and display poster, title, saved-status indicator when status exists, and rating indicator when score exists. Keep transient reason text separate. Centralize navigation identity and fallback-art logic so Search, Home, strands, mentions, Alchemy, Explore, and filmography behave consistently.

## 9. Feature implementation details

### 9.1 Collection Home

- Query only the current identity's saved items, then layer the selected tag/data filter and All/Movies/TV toggle.
- Generate sidebar filters from current library data: All Shows; one entry per tag; conditional No tags; genre; decade; and configured community-score ranges.
- Group filtered results in order: Active, Excited (`Later + Excited`), Interested (`Later + Interested`), and one initially collapsed Other group containing Wait, Quit, Done, Next if imported/hidden, and Later without interest.
- Give Active a visibly more prominent tile treatment without inventing different data behavior.
- Sort status groups by the relevant most-recent My Data update, with a deterministic title tie-breaker.
- Show a Search/Ask invitation when the whole collection is empty and `No results found` when only the active filter is empty.
- Test media toggle composition, tagless behavior, grouping edge cases, hidden Next data, overlay badges, and empty-state distinction.

### 9.2 Find -> Search

- Provide a labeled search input with sensible debounce/cancellation, loading, empty-query, no-results, retry, and provider-auth states.
- Render a responsive poster grid using normalized, overlaid shows; mark saved items and ratings.
- Open Show Detail with provider/media/external identity. Search results never emit the AI persona.
- Consume an optional prefilled query from unresolved AI handoff and the Search-on-launch setting.

### 9.3 Find -> Ask

- Build welcome, active chat, pending/streaming, error/retry, and reset states.
- Display six refreshable starter prompts, conversational user/assistant turns, simple formatting, and a horizontal mentioned-shows strip built only from resolved items.
- Tapping a resolved mention opens Detail; unresolved mentions open Search with the title.
- Support the show-context handoff and keep the shared persona/summary behavior defined in the AI platform section.

### 9.4 Find -> Alchemy

Model the page as an explicit state machine:

1. Select at least two inputs from collection search and global catalog search; deduplicate by canonical identity.
2. `Conceptualize Shows` fetches shared concepts.
3. Select one to eight concepts.
4. `ALCHEMIZE!` fetches and resolves six recommendations.
5. `More Alchemy!` promotes chosen result shows into the next input round and permits another cycle.

Changing selected input shows clears concepts, selected concepts, and results. Changing concepts clears results. Backtracking never leaves stale downstream content visible. Give each step clear prerequisite copy, disabled/loading/error states, and selection counts. Keep the entire flow in memory and clear it on leaving Alchemy.

### 9.5 Show Detail

Fetch canonical detail and the saved overlay in parallel where possible, then render the supporting spec's narrative hierarchy:

1. Header carousel with inline trailer preference and poster/backdrop/logo fallbacks.
2. Core year/runtime-or-season facts and community score.
3. Sticky/early relationship toolbar for status/interest and My Rating, plus My Tags near the top of the content.
4. Overview and the Scoop toggle/stream.
5. `Ask about this show` handoff.
6. Genres and languages.
7. Traditional similar/recommended strand.
8. Explore Similar concepts -> selection -> five resolved recommendations.
9. `Stream It` provider availability by configured region and offer type.
10. Cast and Crew strands linking to Person Detail.
11. TV-only seasons.
12. Movie-only budget/revenue when available.

Wire relationship controls to the command matrix rather than locally patching a show. Use optimistic feedback only with rollback and authoritative server reconciliation. Reselecting the current chip opens the destructive confirmation; after the configured repeated-confirmation threshold, allow the user to suppress future prompts in Preferences. A direct Settings path can re-enable warnings.

Tags use a picker that suggests the derived personal tag library and allows free-form creation. Rating is an accessible slider/control using centralized scale constants. On auto-save, explain the resulting status with concise non-blocking feedback so implicit behavior does not surprise.

Explore Similar starts with only `Get Concepts` and a one-line ingredients explanation, supports one-to-eight chips, clears recommendations when selection changes, and handles partial/unresolved results transparently. Long-tail sections load independently and missing trailers/backdrops/providers/credits/seasons/financials degrade gracefully.

### 9.6 Person Detail

- Fetch Person biography, images, and combined movie/TV credits without persisting them.
- Deduplicate credits by provider/media/external identity and group filmography by release/first-air year, with unknown dates separated and years ordered newest first.
- Derive average project community ratings, top genres, and projects-by-year from valid credit data. Label sample size and ignore missing scores rather than treating them as zero.
- Render accessible chart summaries/tables in addition to graphical output.
- Overlay any saved credit shows in bulk and link valid movie/TV credits to Show Detail.
- Provide graceful states for missing biography, art, dates, genres, or chart-worthy data.

### 9.7 Settings and Your Data

- Preferences: six font-size options and Search on launch, applied immediately and persisted server-side.
- User: editable username scoped to the current identity.
- AI: model selection from a server-defined allowlist and credential configured/source status. If user keys are supported, accept replace/remove via a masked write-only form and store encrypted server-side.
- Catalog integration: same write-only or environment-backed credential pattern.
- Safety: never display full stored secrets, serialize them to client state, write them to logs, or export them.
- Removal warnings: expose the suppression preference so it can be reversed.
- Export: generate a server-side ZIP containing one UTF-8 JSON file with export schema version, generation timestamp, namespace-neutral user metadata, every saved show's public snapshot and My Data, and ISO-8601 timestamps. Exclude namespace, internal DB IDs, test flags, secrets, and session data unless needed for documented restoration semantics. Stream with safe filename/content headers.
- Verify the ZIP can be opened and parsed, record counts match the scoped library, null/empty user edits remain representable, and another user/namespace cannot export it.
- Label Import/Restore as unavailable rather than presenting a nonfunctional control.

## 10. Server APIs and state management

Expose small same-origin endpoints/actions around use cases, not raw tables. The exact HTTP shape can evolve, but it should cover:

- collection query/filter metadata and explicit status, interest, rating, tag, remove commands;
- catalog search, show detail/strands/providers, and Person detail/credits;
- Ask message/reset context as needed, Scoop stream, concepts, and concept recommendations;
- preferences, write-only credential replacement/removal/status, and export.

Every handler follows: validate request -> resolve identity -> authorize feature/environment -> invoke service -> map typed result/error. Use runtime schemas at external and HTTP boundaries. Add CSRF/origin protection to state-changing browser requests as appropriate, request-size limits, provider timeouts/cancellation, and rate limiting/backoff for costly AI endpoints.

Use server-fetched initial page data where it improves first render, and feature-local client hooks for mutations and sessions. A query cache may improve UX but is disposable; invalidate/reconcile collection, tag filters, badges, and Detail after My Data mutations. Do not put Ask/Alchemy state in persistent local storage.

## 11. Verification strategy

### 11.1 Unit tests

- Full mutation matrix for unsaved/saved shows, defaults, retained interest, clears, and deletion.
- Field-by-field timestamp conflict resolution, non-empty public merge, immutable creation date, duplicate detection, and overlay precedence.
- Home filtering/grouping/sorting, tag normalization/library, media toggle, decade/score buckets, and empty states.
- Catalog normalization, media inference/rejection, date parsing, logo selection, and provider mapping.
- AI context budgeting, prompt contracts, mention parser delimiters, concept validation/counts, repair fallback, summarization threshold, and recommendation resolution.
- Person credit deduplication/grouping/chart transforms and export serialization.
- Env parsing and production rejection of dev identity/test reset.

### 11.2 Database and service integration tests

- Apply all migrations to a blank test database and validate constraints/index-sensitive query shapes.
- Exercise repositories only through scoped identities; attempt cross-user and cross-namespace reads, mutations, export, duplicate merges, and reset.
- Simulate concurrent edits to different My Data fields and to the same field.
- Verify removal clears all My Data/Scoop, re-add starts fresh, and public refresh never erases user values.
- Verify client cache/local storage deletion followed by reload restores the backend library/preferences.
- Use unique per-run namespace IDs and clean only those namespaces.

### 11.3 Provider contract tests

- Use recorded/synthetic catalog fixtures for movie, TV, missing-media, malformed, empty, rate-limit, and not-found responses.
- Use deterministic AI fakes for successful structure, malformed-first/repaired-second output, unresolved/wrong IDs, stream interruption, off-domain request, explicit spoiler request, and provider failure.
- Keep live provider smoke tests opt-in and secret-dependent so normal CI is repeatable.

### 11.4 Browser journey tests

Automate the ten core journeys plus failure variants:

1. Search -> save as Interested/Excited/Active -> tag/rate -> Home grouping/filter badges.
2. Rating an unsaved show saves as Done.
3. Tagging an unsaved show saves as Later + Interested.
4. Reselect status -> confirmation -> full removal; suppression and re-enable behavior.
5. Ask starter/message -> mentioned show -> Detail -> save.
6. Detail -> Scoop cache/expiry/persistence rules and Ask-about handoff.
7. Detail -> concepts -> five recommendations -> resolved show -> save.
8. Alchemy input/concept/result state clearing, six recommendations, and chained round.
9. Cast/Crew -> Person analytics/filmography -> another Show Detail.
10. Settings persistence, Search on launch, font scaling, and valid scoped ZIP export.

Also cover empty library, no filter matches, absent media/providers/credits, provider failures, AI parse fallback, unresolved AI item, two simultaneous identities, refresh/deep link/back navigation, and narrow/wide layouts.

### 11.5 Accessibility, visual, performance, and security checks

- Run automated accessibility checks and manual keyboard/screen-reader smoke tests on shell, dialogs, chips, slider, mode switcher, carousel, chat stream, and charts.
- Add visual snapshots for Home group treatments/empty states, Search grid, Ask welcome/chat, each Alchemy step, Detail saved/unsaved/media fallbacks, Person charts, Settings, mobile drawer, and all font scales.
- Track practical budgets for initial shell, Search response rendering, image behavior, Detail section loading, AI first-token feedback, and large-library filtering. Avoid blocking initial Detail on every long-tail provider call.
- Confirm secrets are absent from client bundles, logs, exported ZIPs, error payloads, and source control; run dependency and secret scans in CI.

## 12. Phased implementation sequence

Each phase ends with passing focused tests and a reviewable vertical outcome. Do not wait until the final phase to add tests or accessibility.

### Phase 0: Scaffold and contracts

- Initialize latest-stable Next.js with strict TypeScript, linting, formatting, test runners, and the fractal module layout.
- Add theme tokens, base shell primitives, typed environment parsing, error/result conventions, and provider/domain interfaces.
- Add `.env.example`, `.gitignore`, scripts, CI skeleton, and hosted-Supabase-first README.
- Acceptance: production build, lint, typecheck, empty test suite plumbing, and environment failure checks pass without Docker.

### Phase 1: Identity, Supabase, and library domain

- Add migrations, server-only Supabase client, identity resolver, scoped repositories, seed/setup, and safe namespace reset.
- Implement catalog snapshot/My Data models, merge/overlay functions, explicit mutation commands, preferences, and isolation tests.
- Acceptance: two namespaces and two users remain isolated; mutation/merge matrix passes; fresh migration/reset is repeatable.

### Phase 2: Catalog adapter and first vertical slice

- Implement the configured catalog adapter, normalization, search/detail basics, overlays, and resilient provider errors.
- Build shell/navigation, Search grid, minimal Detail relationship controls, and Home grouping/filtering.
- Acceptance: Search -> Detail -> status/rate/tag -> Home works against hosted Supabase, survives browser storage clearing, and shows correct overlays everywhere.

### Phase 3: Complete non-AI exploration

- Complete Detail narrative sections, media fallback, traditional recommendations, providers, cast/crew, seasons, and financials.
- Build Person Detail, analytics transforms/charts, filmography grouping, and overlay/link behavior.
- Acceptance: movie, TV, sparse-detail, and Person deep-dive journeys pass with independent section failures.

### Phase 4: Shared AI foundation, Scoop, and Ask

- Add AI adapter, common persona/taste context, structured validation/repair, streaming, observability, and safe error handling.
- Implement Scoop caching/persistence and full Ask welcome/chat/summarization/mentions/show-handoff flow.
- Acceptance: persona/format contract tests pass; wrong IDs cannot become links; Scoop four-hour and unsaved behavior are correct; leaving Ask clears its session.

### Phase 5: Concepts, Explore Similar, and Alchemy

- Add concept generation/validation and resolved recommendation service.
- Complete Explore Similar and the Alchemy state machine, prerequisite states, backtracking clears, and More Alchemy chaining.
- Acceptance: exact 5/6 recommendation requests, 1-8 selection cap, multi-show shared concepts, resolution fallback, and session clearing are verified.

### Phase 6: Settings, secrets, and export

- Complete preferences/username/model integration, optional write-only encrypted credentials, warning suppression controls, and versioned ZIP export.
- Add settings and export isolation/security tests and document credential precedence.
- Acceptance: settings survive reload/device session, launch behavior/font scale apply, export is complete/parseable/scoped, and secrets never leave the server.

### Phase 7: Hardening and release readiness

- Finish full browser matrix, live-provider smoke option, discovery golden-set scoring, visual regression, accessibility, responsive, performance, security, and migration-upgrade tests.
- Audit all pages for overlay consistency, session persistence rules, missing-data/error states, and humble-component/code-location standards.
- Finalize setup/operations documentation, known provider limitations, reset safeguards, and future OAuth handoff.
- Acceptance: one-command CI passes from a clean checkout; a hosted Supabase environment can run concurrently under distinct namespaces; no mandatory journey depends on Docker, local persistence, or manual database cleanup.

## 13. Requirement traceability and final definition of done

| Requirement area | Primary implementation | Primary proof |
|---|---|---|
| Collection membership/defaults/removal | Library command service + `library_items` | Unit matrix + browser save/remove journeys |
| User overlay everywhere | Central overlay service/view model | Search/Home/strands/AI/credits integration tests |
| Tags/filters/status grouping | Home and library query modules | Filter/group unit + visual/browser tests |
| Search/catalog detail | Catalog adapter + Search/Detail pages | Provider contracts + deep-link journey |
| Ask/mentions/context | AI gateway + Ask session feature | Structured parser, summary, resolution, session tests |
| Scoop | Streaming Scoop service/feature | freshness, saved/unsaved, removal, content contract tests |
| Concepts/Explore/Alchemy | Discovery service + two feature state machines | count/cap/reset/chain/quality/resolution tests |
| Person detail | Person adapter/page analytics features | sparse/full fixture + chart accessibility tests |
| Settings/export | Preferences/secrets/export services | persistence, security, ZIP parse/isolation tests |
| Identity/isolation/backend truth | Identity resolver + scoped Supabase repositories | cross-tenant tests + storage-clear reload |
| Execution/migrations/reset | env/scripts/migrations/README | clean hosted setup + scoped destructive CI run |
| Voice/discovery quality | shared prompts + golden-set harness | rubric threshold and real-show integrity checks |
| Data continuity | forward migrations + merge/backfill tests | representative upgrade fixtures and export version |

The build is complete only when all required routes and journeys work with configured hosted services, all saved user data is scoped and durable, every interactive AI recommendation has passed catalog verification, all optional/session persistence rules are honored, the full automated suite is green, and setup/reset/export behavior is documented and reproducible from a clean checkout.
