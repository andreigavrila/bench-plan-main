# Implementation Plan — Personal TV & Movie Companion

## 1. Scope, assumptions, and delivery shape

Build the product from this documentation-only repository as a full-stack Next.js application using the latest stable App Router release, TypeScript, and Supabase's official libraries. Supabase is the durable source of truth; browser state is limited to disposable request caches and the explicitly ephemeral Ask, Alchemy, Explore Similar, and unsaved-Scoop sessions. Clearing browser storage must not remove the library or server-backed preferences.

Keep catalog and AI vendors behind server-side adapters because the PRD deliberately leaves both unspecified. At implementation start, select providers that cover movie/TV search, details, credits, people, images/videos, providers, seasons, recommendations, and stable external IDs, and an AI provider/model that supports schema-constrained responses and streaming. Pin the chosen SDK versions and expose provider selection through validated configuration rather than feature code.

Do not expand the first release into the open questions: `Next` remains modeled but hidden; named custom lists, Import/Restore, saved/shared Alchemy sessions, and a Detail-page Alchemy entry remain out of scope. Use nullable rating as the unrated state. Generating a Scoop for an unsaved show does not itself save the show; it remains session-only until another documented save trigger occurs.

## 2. Establish the runnable foundation

1. Scaffold the Next.js App Router project with strict TypeScript, linting, formatting, unit/integration testing, browser E2E testing, accessibility checks, ZIP generation, schema validation, Supabase, and the chosen query/cache library. Pin a supported Node version and lock dependencies.
2. Add `.env.example` with short comments for every setting: public Supabase URL/anon key, server-only service credential, stable `APP_NAMESPACE_ID`, guarded development/test user identity, catalog provider configuration, AI provider/model configuration, default provider country, and environment flags. Validate variables once in `src/config`; keep separate public and server-only schemas so importing secrets from client code fails at build time.
3. Retain `.env.example` while ignoring every other `.env*` file. Never include service-role, catalog, AI, or user-entered credentials in client bundles, logs, telemetry, API errors, exports, fixtures, or snapshots.
4. Add one-command scripts for development, lint/typecheck, unit tests, integration tests, E2E tests, production build, migration application, and namespace-only test reset. The documented primary path connects to hosted Supabase and requires no Docker; local Supabase is an optional convenience only.
5. Add route-level error/loading boundaries, structured server logging with secrets and user prompts redacted, and CI that runs static checks, deterministic adapter tests, database integration tests, E2E, and the production build.

## 3. Enforce identity, namespace isolation, and authorization

1. Resolve an immutable request context at every server entry point: `{ namespaceId, userId, mode, isTest }`. Read `namespaceId` only from trusted deployment configuration, never request input. Treat `userId` as an opaque stable string.
2. For development/test, support a documented fixed identity or guarded `X-User-Id` injection. Reject injection outside development/test. Put identity resolution behind an interface so a future Supabase/OAuth session resolver replaces it without changing tables or domain services.
3. Route all user-owned persistence through server handlers/actions. Repository methods require the request context as a non-optional first argument and always filter by `(namespace_id, user_id)`. Do not expose arbitrary namespace or user predicates to clients.
4. Make database constraints and policies defense-in-depth: deny direct public mutation of user tables, constrain composite foreign keys by namespace/user, and add RLS policies for a future authenticated session path. If a server-only service client is used during benchmark identity injection, recognize that it bypasses RLS and retain mandatory repository predicates plus authorization tests.
5. Implement reset only in development/test. Require an exact configured namespace and a second explicit test-mode guard; delete that namespace's dependent rows in a transaction. Never truncate or reset the database globally. Integration tests create a unique namespace per run and prove a neighboring namespace survives reset.

## 4. Design repeatable Supabase persistence and migrations

Create versioned, forward-only SQL migrations and deterministic fixtures. Every table populated by a run carries `namespace_id`; every user-owned table also carries `user_id`. Use timezone-aware timestamps, database defaults for creation times, check constraints for enums/ranges, composite foreign keys, and indexes matching filters and joins.

Recommended relational model:

- `namespace_users`: `(namespace_id, user_id)`, creation/test metadata.
- `catalog_shows`: namespace, catalog provider, external ID, media type, canonical title and all persisted public facts: overview/tagline, external IDs, genres/languages, homepage, image/logo URLs, community score/count/popularity, release/air dates, runtime/budget/revenue, TV status/episode/season fields, provider-ID-by-country JSON, `details_updated_at`, and immutable `created_at`. Unique on `(namespace_id, provider, media_type, external_id)`.
- `user_shows`: one overlay per `(namespace_id, user_id, catalog_show_id)` with status, interest, rating, Scoop, each field's update timestamp, creation/update/test metadata. Status supports `active | next | later | done | quit | wait`; `next` has no first-class UI.
- `user_show_tags`: normalized tag rows tied to an overlay, with case-insensitive uniqueness. Treat the collection of tags as one last-writer-wins field using `my_tags_updated_at` on `user_shows`, while preserving display casing consistently.
- `user_settings`: username, AI model choice, auto-search, readability size, and a version/update timestamp. Deployment credentials stay outside this table. If optional user-provided keys are supported, encrypt them server-side, return only a configured/not-configured flag, and exclude them from export.
- `user_ui_preferences`: removal-confirmation suppression/count and validated last-selected filter.
- `app_metadata`: namespaced data-model version/migration bookkeeping.

Persist the reference schema's catalog facts, but keep re-pullable payloads transient: cast, crew, seasons, image galleries, videos, traditional recommendations/similar items, last episode, person credits, tile state, and selection state. Store streaming availability as provider IDs grouped by country and fulfillment type; resolve display metadata separately.

Implement persistence through focused domain repositories and transactional services:

1. Catalog upsert uses provider/type-aware identity and `selectFirstNonEmpty(incoming, stored)` per field: null, empty strings, or empty arrays cannot erase known facts. Refresh `details_updated_at`; never rewrite `created_at`.
2. User overlay mutations are atomic and server-authoritative. Each changed field receives its own server timestamp. Merge/sync chooses the newer timestamp per status, interest, score, Scoop, and complete tag set; catalog refresh never overwrites user data.
3. Encode save transitions once in a pure relationship service: any explicit status saves; Interested/Excited maps to Later plus that interest; a first rating saves as Done; a first tag or status-free save uses Later + Interested. Moving away from Later may retain interest but does not surface it.
4. Clearing/reselecting the active status invokes a confirmed remove command that atomically deletes the overlay and tags, thereby clearing status, interest, rating, tags, and Scoop together. The client cannot send a partial delete.
5. Add a forward migration policy: schema changes are additive or staged, existing overlays and per-field timestamps are backfilled safely, verification runs before advancing `app_metadata`, and destructive column/table removal is deferred until data has been proven migrated.

## 5. Create server/domain boundaries and provider adapters

Use thin App Router handlers/actions for parsing, request-context resolution, authorization, and response mapping. Place business rules in framework-independent services and persistence behind repositories.

1. Define a `CatalogProvider` interface for title/keyword search, movie/TV detail, external-ID resolution, images/logos/trailers, provider availability, cast/crew, person detail/credits/images, TV seasons, and traditional similar/recommended titles. Normalize vendor payloads into domain types; reject unknown media types/missing titles and choose the best logo deterministically (language/rating/fallback order).
2. Define an `AiProvider` interface for structured completion and streaming. Provider SDK types do not cross the adapter. Centralize timeouts, aborts, rate-limit handling, bounded retry, output validation, and safe user-facing errors.
3. Add catalog queries for search, overlay-aware show detail, person detail, and selectable-title resolution. A detail refresh merges public facts before composing `catalog + current user's overlay + transient detail sections`.
4. Add library queries for overlays joined to catalog facts, tag inventory, generated filter options/counts, and grouped collection output. Support `all`, tag, No tags, genre, decade, community-score range, and internal `myStatus`, plus independent `all | movie | tv` selection. Sort within groups by the latest relevant relationship timestamp.
5. Add narrow mutation contracts for status/interest, rating (including null), full tag-set replacement, and Scoop. Validate ownership, enum values, rating range/step, tag trimming/length/count/case-insensitive deduplication, and confirmation state on the server.
6. Add settings read/update contracts and an authenticated Export endpoint. The export streams a safe-named ZIP containing a versioned JSON snapshot of only the current user's saved shows, all My Data, and portable settings, with ISO-8601 dates and no credentials or ephemeral AI sessions. Validate the JSON and archive entries before streaming.

## 6. Implement shared AI context, contracts, and resolution

1. Build a server-only context assembler that supplies the smallest relevant slice of the user's library and My Data, current show(s), selected concepts, and active session turns. Apply a shared persona contract across Scoop, Ask, concepts, Explore Similar, and Alchemy: warm and joy-forward, opinionated but honest, specific/vibe-first, spoiler-safe by default, concise unless depth is earned, and restricted to TV/movies.
2. Keep prompts/version identifiers in configuration and make response schemas explicit. Record provider/model/prompt version and quality metrics without retaining user conversation text. Cap library/session context deterministically and define truncation behavior.
3. Ask returns `{ commentary, showList }`; `showList` is exactly `Title::externalId::mediaType;;...`, while commentary contains no IDs. Validate the object and grammar, retry malformed structured output once with stricter instructions, then retain useful unstructured commentary and present a Search handoff.
4. Manage Ask in feature/session memory only. After roughly ten messages, summarize older turns into one or two persona-consistent sentences and retain recent turns. Reset, mode exit, or navigation out discards transcript, summary, and mentioned strip. “Ask about this show” creates a new/continued Ask session seeded with exact canonical show context and a visible handoff.
5. Scoop produces a streamable 150–350 word mini taste blog with a clear take, honest stack-up, emotionally central Scoop passage, fit/warnings, and verdict. Show a generating state immediately. A saved Scoop is fresh for four hours; regenerate only on demand after expiry. Persist only for an already-saved overlay, otherwise cache in the current Detail session and discard on exit unless a later save explicitly adopts it.
6. Concepts return bullets only: eight by default, each one to three words, spoiler-free, specific, diverse across structure/vibe/emotion/relationships/craft, ordered strongest first, and never generic placeholders. Multi-show concepts must be common to all inputs and may request a larger candidate pool while UI selection remains one through eight.
7. Explore Similar requests exactly five recommendations; Alchemy requests exactly six. Reasons are one to three sentences, name selected concepts explicitly, favor recent work without excluding classics/hidden gems, and provide title, media type, and external ID when possible.
8. Centralize one recommendation resolver for Ask mentions and both concept flows. Prefer external ID, but accept it only when the resolved title matches case-insensitively and media type is compatible; otherwise do a constrained title/type search. Interactive output must be a real canonical show with the current user's overlay applied. Unresolved/mismatched/hallucinated entries remain visibly non-interactive with an accessible Search handoff; transient AI reasons are never persisted into catalog facts.

## 7. Build the design system and fractal frontend architecture

Use App Router files in `src/app` only as route/layout/server boundaries. Product page composition follows the mandated fractal pattern, with feature logic in hooks/services and TSX limited to markup and binding:

```text
src/
  app/                         # thin routes, metadata, loading/error boundaries, APIs
  config/                      # environment schemas, constants, prompt versions
  theme/                       # colors, type/readability scales, spacing, radii, breakpoints
  components/                  # accessible shared primitives and overlay-aware ShowTile
  hooks/                       # cross-page request/cache/session hooks
  utils/                       # global pure formatting/validation helpers
  server/                      # context, repositories, domain services, provider adapters
  pages/
    CollectionHome/
      CollectionHome.tsx
      features/{SidebarFilters,MediaTypeToggle,LibrarySections}/
    Discover/
      Discover.tsx
      features/{ModeSwitcher,Search,Ask,Alchemy}/
    ShowDetail/
      ShowDetail.tsx
      features/{HeaderMedia,MyRelationship,Scoop,ExploreSimilar,Streaming,Credits}/
    PersonDetail/
      PersonDetail.tsx
      features/{Gallery,Analytics,Filmography}/
    Settings/
      Settings.tsx
      features/{AppPreferences,AiAndIntegrations,YourData}/
```

Co-locate feature-only hooks, utilities, constants, tests, and subfeatures beneath their owner; promote code only when genuinely shared. Main files match directory names and avoid `index.tsx`. Put all styling values in theme/local style tokens—no inline styles, hex values, pixels, or magic numbers in TSX. Build reusable labelled buttons/chips, segmented controls, dialogs, forms, rating control, poster tile, media carousel, horizontal strand, streaming panel, charts, skeletons, and empty/error states.

Define typed routes for Home, Discover, provider/type-safe Show Detail, Person Detail, and Settings. Use validated URL parameters for shareable filter/media/mode state where useful, while persisting only documented preferences. Ensure semantic landmarks/headings, keyboard operation, visible focus, dialog focus trapping/restoration, labelled charts with textual equivalents, reduced-motion support, responsive layouts, and all six readability sizes.

## 8. Implement Collection Home and universal show presentation

1. Create a single response mapper and `ShowTile` used everywhere: Home, Search, traditional recommendations, AI results, mentioned shows, and filmography. It always overlays current-user status/tags/rating/Scoop over catalog facts and displays saved/rating indicators where applicable.
2. Build navigation with All Shows, generated tag filters, conditional No tags, genre/decade/community-score filters, and persistent Discover/Settings entries. Place the All/Movies/TV toggle above collection content and apply it in addition to the selected filter. Validate and persist the last filter; gracefully fall back to All if it no longer exists.
3. Render Active with larger/prominent tiles, then Excited (`later + excited`), Interested (`later + interested`), and a collapsed Other containing Wait, Quit, Done, and Later without interest. Distinguish a truly empty library (Search/Ask CTAs) from an empty filter (“No results found”).
4. Mutations may update optimistically only with rollback and server reconciliation. Invalidate the current Detail, Home groups/counts, tag filters, and all cached appearances of that show after every My Data change.

## 9. Implement Discover: Search, Ask, and Alchemy

1. Add a clear Search/Ask/Alchemy switcher. Honor Search on Launch at the Discover entry point without locking the user into Search.
2. Search debounces accessible title/keyword input, cancels stale requests, renders a poster grid with overlay badges, and covers empty query, no results, loading, rate-limit/provider failure, retry, and selection into Detail. Search copy stays neutral rather than adopting the AI persona.
3. Ask presents six randomly sampled starter prompts with refresh, an accessible transcript/composer, pending/stream/error states, inline/selectable mentions, and a horizontal mentioned-show strand. Keep unresolved titles readable and offer Search. Reset/exit applies the ephemeral session rules.
4. Alchemy searches both library and catalog, deduplicates provider/type identities, and requires at least two inputs before Conceptualize. Render concepts as selectable chips with a maximum of eight and require at least one before ALCHEMIZE. Show six overlay-aware cards with reasons. Changing inputs clears concepts/selections/results; changing concepts clears results. Backtracking is safe. “More Alchemy!” uses chosen results as new inputs in the same ephemeral session and starts a clean downstream round.

## 10. Implement Show Detail and Person Detail

1. Preserve the required Show Detail narrative: media carousel; year/length and community score; My Tags; Overview plus Scoop; Ask-about CTA; genres/languages; traditional recommendations; Explore Similar; providers; cast/crew; TV seasons; movie budget/revenue. Keep relationship toolbar/rating immediately available. Omit or collapse missing/inapplicable sections cleanly.
2. Prefer inline trailer playback in the header, with cinematic backdrop/poster/logo fallback. Handle sparse catalog data, no media, provider errors, and movie/TV differences without blocking saved My Data controls.
3. Map visible Interested/Excited chips to Later plus interest. Reselecting the active choice opens the removal dialog unless the saved suppression rule applies; record confirmation count/preferences. On success, visibly clear all My Data. Rating has an explicit unset state and rate-to-save behavior; tag creation/picking deduplicates and applies tag-to-save behavior.
4. Implement Scoop states/copy exactly: “Give me the scoop!”, “Show the scoop”, open heading “The Scoop”, generating/stream/error/stale states, and the four-hour saved-versus-ephemeral rules.
5. Implement Explore Similar inside the Detail feature: explain concepts in one line, Get Concepts, select one to eight ingredients, Explore Shows, and render exactly five resolved recommendations with transient reasons. Any concept selection change clears prior results. Ask-about passes full canonical context rather than merely switching modes.
6. Cast/crew selection opens typed Person Detail. Fetch gallery, biography, and credits; group filmography by year and use overlay-aware show cards. Derive average available community rating, top genres, and projects-by-year from resolved credits with pure calculations, never inventing missing ratings; provide text summaries for charts.

## 11. Implement settings, export, and continuity

1. Build settings for username, XS–XXL readability, Search on Launch, AI model, optional integration configured-state, removal-confirmation preferences, and Export My Data. Save server-backed settings by namespace/user and immediately apply readability/accessibility changes.
2. Prefer deployment-provided provider credentials. If user-entered credentials are enabled, accept write-only values over protected server routes, encrypt at rest using a deployment secret, never echo them, and provide replace/remove controls. Document security and sync implications.
3. Export the versioned ZIP/JSON schema and document what is and is not included. Do not add an import UI until validation, version compatibility, conflict, credential, and overwrite semantics are specified.
4. Prove data continuity by applying forward migrations to fixtures representing earlier data-model versions and by reopening a saved library after browser storage/cache is cleared.

## 12. Verification strategy and acceptance matrix

### Unit and component tests

- Relationship transition table, implicit saves, retained-but-inactive interest, and atomic removal semantics.
- Tag normalization/full-set timestamps, rating clear/save behavior, per-field newer-wins merge, and catalog non-empty merge.
- Grouping/filter intersections, conditional No tags, sorting, score/date formatting, provider normalization, best-logo selection, and person analytics.
- Ask grammar/parser and retry/fallback, concept validation, Scoop freshness boundary, recommendation title/ID/type resolution, and unresolved handoffs.
- Humble component bindings, all loading/empty/error states, keyboard controls, removal-dialog focus restoration, and readability tokens.

### Supabase and route integration tests

- Apply migrations to a clean hosted-compatible database; exercise all repository/service transactions.
- Same namespace/multiple-user isolation, cross-namespace isolation, forged identity/namespace rejection, direct-public-access denial, and production rejection of development identity injection.
- Concurrent field edits, complete tag-set last-writer-wins, catalog refresh preserving overlays, duplicate external identity merge, and rollback on failed atomic removal.
- Namespace reset deletes only its target; export contains exactly one user and valid ISO dates while excluding secrets/sessions; migrations preserve legacy overlays and timestamps.
- Mock catalog/AI providers for normal CI, including timeout, rate limit, partial stream, malformed structured output, wrong ID/title, unknown media type, and secret-redaction paths.

### End-to-end and quality acceptance

Automate all ten journeys: build a collection, rate-to-save, tag-to-save, maintain My Data, tag-filter organization, Ask-to-save, Explore Similar-to-save, Alchemy plus chaining, person deep-dive, and ZIP backup. Add regression coverage for removal, unrated state, tagless items, empty filters/library, missing trailers/images, TV/movie conditional sections, provider failures, navigation/reset session cleanup, multiple appearances staying in sync, and browser-storage clearing.

Run accessibility scans plus keyboard/screen-reader smoke tests on navigation, mode switcher, rating/tags/status, dialogs, chat, concept chips, carousels, charts, and streaming states at responsive breakpoints and every readability size. Add visual regression snapshots for Active hierarchy, dense Detail, Discover modes, empty/error/loading states, and mobile layouts.

Maintain an AI quality harness with representative taste profiles and deterministic scenario inputs. Human/recorded evaluations score Voice, Taste Alignment, Surprise Without Betrayal, Specificity, and Real-Show Integrity from 0–2. Require Voice ≥1, Taste ≥1, Real-Show Integrity =2, total ≥7/10; also enforce eight valid concepts, five Explore recs, six Alchemy recs, concept-specific reasons, and Scoop structure/length. Never release with unresolved/mismatched entries presented as interactive.

## 13. Delivery sequence and exit criteria

1. **Foundation:** runnable app, configuration validation, hosted-Supabase path, migrations, request context, namespace/user enforcement, and safe reset. Exit when clean-database and isolation tests pass.
2. **Core data:** catalog normalization/merge, user overlays and transitions, settings, filters, export, and forward-migration fixtures. Exit when business-rule and continuity tests pass.
3. **Core experience:** theme/primitives, navigation, Home, Search, shared tiles, Detail relationship controls, transient detail content, and Person Detail. Exit when core journeys work with deterministic catalog fixtures and accessibility basics pass.
4. **AI discovery:** shared persona/context, Ask, Scoop, concepts, resolver, Explore Similar, Alchemy, session cleanup, and fallbacks. Exit when structural contracts, exact counts, real-show integrity, and quality threshold pass.
5. **Hardening:** responsive/visual polish, failure/race handling, full E2E suite, production build, cloud-agent setup docs, secret audit, and migration/reset rehearsal. Exit only after clearing client storage and a forward migration both preserve the library and all CI/quality gates are green.

Document setup, variables, migrations, provider configuration, development identity and its production restriction, namespace reset safety, export scope, all commands, and the OAuth replacement seam alongside implementation. Keep open product decisions recorded without silently adding them to scope.
