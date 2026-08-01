# Implementation Plan

## 1. Scope and Delivery Strategy

Build a responsive personal TV and movie companion with five connected capabilities:

1. A durable, filterable personal collection whose user-owned fields override refreshed catalog data everywhere.
2. Catalog search, show detail, and person detail experiences.
3. Taste-aware Ask, Scoop, Explore Similar, and Alchemy AI surfaces with one consistent voice.
4. Settings and a portable ZIP/JSON data export.
5. A benchmark-safe Next.js and Supabase runtime with strict build namespace and user isolation.

Implementation should proceed as tested vertical slices, starting with identity, persistence, catalog normalization, and collection business rules. Those foundations are shared by every page and AI workflow; building UI or prompts before them would create inconsistent overlays and unsafe test isolation.

The first release will not implement OAuth, offline-first behavior, import/restore, first-class `Next` status UI, named lists, or saved/shared Alchemy sessions. The schema and service boundaries will permit later OAuth and import work without redesign.

## 2. Product Decisions for Open or Ambiguous Areas

- Keep `next` in the status enum and export format, but do not expose it as a primary status control.
- Represent an unrated show as `my_score = null`. A clear-rating mutation still advances `my_score_updated_at`, so a newer clear wins sync conflicts.
- Generating a Scoop does not save an unsaved show. Its result remains in the current detail-page state only. A Scoop generated for a show already in the collection is persisted.
- Use Interested and Excited as visible status chips that atomically set `status = later` and the corresponding interest. Other status chips set the status but retain the prior interest value for a later return to `later`; interest is ignored while another status is active.
- Preserve tag display values exactly after trimming surrounding whitespace. Reject blanks and exact duplicates; do not case-fold or merge existing tags without a future product-approved migration.
- Use the catalog provider's movie/TV identifier plus media type as the canonical external identity. Never assume movie and TV identifier spaces are interchangeable.
- Choose one catalog provider per namespace through environment configuration and keep that provider immutable for v1 so saved identities cannot split when settings change. Implement its adapter and an initial configurable AI adapter, but keep provider DTOs outside the domain. Provider keys and model names come from environment or encrypted server-side settings, not source code.
- Use a single shared user-rating contract of 0.5 through 10.0 in 0.5 increments; `null` means unrated. Apply it consistently in the slider, API validator, database constraint, export, and tests.
- Preserve the documented detail-page section order. Status/interest and rating controls remain sticky or adjacent to the header rather than becoming a late body section.
- Keep Alchemy entry on the Find hub only. Do not add the currently hidden detail-page entry.
- Treat cross-device sync as inherent when two clients use the same backend partition. No separate sync engine or local source of truth is needed.

## 3. Technical Architecture

### 3.1 Runtime and Libraries

- Use the latest stable Next.js release available at implementation time, TypeScript, React, and the App Router.
- Use Supabase Postgres through official Supabase libraries. Browser code does not directly mutate persistence; Next.js server routes/services enforce identity, validation, and domain rules.
- Use SQL migrations for deterministic schema evolution and generated database types for compile-time query safety.
- Use a schema validator such as Zod at environment, route, provider, AI-output, import/export, and client/server boundaries.
- Use a server-capable ZIP library for export and a streaming response mechanism supported by Next.js for Scoop and Ask.
- Use a lightweight accessible chart library for person analytics, loaded only on the person page.
- Use Vitest and Testing Library for unit/component tests, Playwright for end-to-end journeys, and provider fixtures for deterministic integration tests.

### 3.2 Application Layers

Keep dependencies flowing inward:

1. **Routes and pages** render feature components and invoke typed client APIs.
2. **Feature hooks** own interaction state, loading/error state, and event handlers; TSX stays focused on markup and binding.
3. **Server route handlers** resolve identity, validate requests, call application services, and serialize responses/streams.
4. **Application services** implement collection transitions, catalog overlay assembly, AI workflows, export, and settings behavior.
5. **Repositories and provider adapters** isolate Supabase, catalog-provider, and AI-provider details.
6. **Domain modules** contain provider-neutral types, invariants, merge functions, filter/group logic, freshness rules, and parsers.

Server-only modules must be marked and kept outside client import graphs. Secrets, raw provider payloads, and elevated Supabase clients never cross into browser bundles.

### 3.3 Suggested Repository Shape

Follow the required fractal feature structure and avoid `index.tsx` files:

```text
src/
  app/
    layout.tsx
    page.tsx
    find/page.tsx
    shows/[mediaType]/[showId]/page.tsx
    people/[personId]/page.tsx
    settings/page.tsx
    api/
      catalog/search/route.ts
      shows/[mediaType]/[showId]/route.ts
      shows/[mediaType]/[showId]/my-data/route.ts
      collection/route.ts
      tags/route.ts
      people/[personId]/route.ts
      settings/route.ts
      export/route.ts
      ai/ask/route.ts
      ai/summarize/route.ts
      ai/scoop/route.ts
      ai/concepts/route.ts
      ai/recommendations/route.ts
  ui/pages/
    CollectionPage/
      CollectionPage.tsx
      hooks/useCollectionPage.ts
      features/CollectionSections/
      features/FilterNavigation/
    FindPage/
      FindPage.tsx
      features/SearchMode/
      features/AskMode/
      features/AlchemyMode/
    ShowDetailPage/
      ShowDetailPage.tsx
      features/HeaderMedia/
      features/MyRelationshipControls/
      features/OverviewAndScoop/
      features/TraditionalRecommendations/
      features/ExploreSimilar/
      features/StreamingAvailability/
      features/CastAndCrew/
      features/Seasons/
      features/Financials/
    PersonDetailPage/
      PersonDetailPage.tsx
      features/PersonGallery/
      features/PersonAnalytics/
      features/Filmography/
    SettingsPage/
      SettingsPage.tsx
      features/AppPreferences/
      features/ProviderSettings/
      features/DataExport/
  components/
    AppShell/
    ShowTile/
    ShowRail/
    MediaCarousel/
    Chip/
    RatingControl/
    EmptyState/
    ErrorState/
  server/
    identity/
    repositories/
    services/
    providers/catalog/
    providers/ai/
    prompts/
  domain/
    shows/
    collection/
    filters/
    settings/
    ai/
    export/
  config/
  theme/
  utils/
supabase/migrations/
scripts/reset-test-namespace.ts
tests/e2e/
```

Only promote a component, hook, or utility to a shared directory after at least two features need it. Feature-specific logic, constants, and critical unit tests remain colocated. Global constants belong in `src/config`; no TSX file contains inline styles, raw colors, or layout numbers. The `src/ui/pages` name deliberately avoids Next.js's reserved `src/pages` router directory.

### 3.4 Routes and Responsive Shell

- `/`: collection home, optionally redirecting to `/find?mode=search` when Search on Launch is enabled.
- `/find?mode=search|ask|alchemy`: one Find hub with a keyboard- and screen-reader-accessible mode switcher.
- `/shows/[mediaType]/[showId]`: show detail. Preserve the return URL so search, Ask, Alchemy, and person journeys can return to their prior state.
- `/people/[personId]`: person detail.
- `/settings`: app, user, provider, and data controls.

Desktop uses a persistent filter/navigation panel and main content region. Mobile uses the same navigation content in a drawer/sheet, maintains visible Find and Settings entry points, and converts dense grids/rails and detail controls without horizontal viewport overflow. Define typography, spacing, colors, breakpoints, chart colors, tile sizes, and media aspect ratios as theme/config tokens; do not place pixel values or colors in TSX.

## 4. Identity, Isolation, and Security

### 4.1 Effective Identity

Create one server-side identity resolver returning:

```text
RequestIdentity { namespaceId, userId, mode }
```

- `namespaceId` is a required, stable environment value for the lifetime of a build/run.
- Support an explicit `benchmark` identity mode that reads one opaque fixed user ID from environment and works under both `next dev` and a production `next build && next start`; this is the primary no-OAuth benchmark path. An `X-User-Id` override is accepted only in development/test and is always rejected by a production build.
- A separate production-auth mode obtains the opaque user ID from a verified OAuth/Supabase Auth session. No table or foreign key changes should be required when that mode is enabled later. Startup validation rejects production-auth mode without auth configuration and rejects benchmark mode without its fixed user ID.
- Never accept `namespaceId` from a browser request. This prevents a caller from selecting another build partition.
- Every repository operation requires an identity argument and adds both partition predicates for user-owned records.

### 4.2 Supabase Access and RLS

- Keep elevated/service credentials server-only. If any Supabase browser client is introduced later, it uses only the anon/public key.
- Enable RLS and deny anonymous direct access to user-owned tables by default. Server routes are the benchmark access boundary; future authenticated policies can bind `user_id` to `auth.uid()` without schema changes.
- Add composite keys/unique constraints beginning with `namespace_id` and, for user-owned data, `user_id`.
- Add repository tests proving two users in one namespace and the same user ID in two namespaces cannot see or alter each other's data.
- Reset tooling takes the configured namespace explicitly, validates it is non-empty, deletes only rows in that namespace in a transaction, and never truncates global tables.

### 4.3 Secret Handling

- Add `.env.example` with comments for namespace/default user, Supabase URL and server/anon keys as applicable, catalog API configuration, AI API configuration, model defaults, encryption key if synced user-entered secrets are supported, and test toggles.
- Keep `.env*` ignored except `.env.example`.
- Prefer environment-provided benchmark credentials. V1 also supports user-entered provider keys: encrypt them before server-side storage, never return plaintext after saving, expose only configured/not-configured/source status, and exclude them from logs and exports. A user key takes precedence when present; deleting it falls back to environment configuration. Key create, replace/rotation, and delete are field-level server operations, and encrypted values sync only within the effective user partition.
- Validate model names against provider-supported configuration rather than interpolating arbitrary values into requests.
- Add request size limits, AI/catalog timeouts, safe Markdown rendering, outbound URL allowlists for catalog media/trailers, and per-identity rate limits on expensive AI routes.

## 5. Persistence Model and Migrations

### 5.1 Tables

Use normalized ownership boundaries while returning a merged `Show` view to the UI.

**`namespaces`**

- `id`, `created_at`.
- Optional bookkeeping only; no user-facing concept.

**`catalog_items`**

- Composite identity: `(namespace_id, catalog_provider, media_type, external_id)`.
- Required: title and media type.
- Public fields: overview, genres, tagline, homepage, `original_language`, `spoken_languages`, `languages`, poster/backdrop/logo URLs, community score/count, popularity, `first_air_date`, `last_air_date`, `release_date`, runtime, budget, revenue, series status, episode/season counts, episode runtimes, provider-data JSON, external-IDs JSON.
- Management fields: `details_updated_at`, `created_at`.
- Scope catalog snapshots by namespace so resets and separate benchmark builds cannot collide. They are not user-owned and therefore do not require `user_id`.

**`collection_items`**

- Composite primary key: `(namespace_id, user_id, catalog_provider, media_type, external_id)`. A separate foreign key on `(namespace_id, catalog_provider, media_type, external_id)` references the namespace catalog item.
- User fields: `my_status`, `my_interest`, `my_tags text[]`, `my_score`, `ai_scoop`.
- One timestamp per mutable user field: `my_status_updated_at`, `my_interest_updated_at`, `my_tags_updated_at`, `my_score_updated_at`, `ai_scoop_updated_at`.
- Management: `created_at`, `is_test`.
- `my_status` is non-null while the row exists, making row existence equivalent to collection membership.
- Check constraints enforce valid enums, the 0.5-10.0 score range/step, and non-empty trimmed tags. A non-null Scoop requires a timestamp; a null Scoop with a newer timestamp remains valid for conflict resolution.
- Add indexes for partition lookup, status/interest grouping, score/date sorting, and a GIN index for tags.

**`user_settings`**

- Composite key `(namespace_id, user_id)`.
- Username, font-size enum, Search on Launch, AI provider/model, configured streaming country (default `US`), optional encrypted AI/catalog credential references, removal-confirmation preference/count, last selected filter JSON, version/update timestamp. Catalog-provider identity itself is namespace environment configuration, not a mutable user setting.
- Keep server-side settings authoritative. A client may mirror font size or last filter for faster paint, but clearing browser storage must not lose them.
- Create the row on first access with a server-generated random display name and defaults, then retain that name until the user changes it. Field-specific PATCH operations plus optimistic row version checks prevent one device from overwriting unrelated settings changed by another.

**`app_metadata`**

- Namespace-scoped data-model version and migration bookkeeping where SQL migration history alone is insufficient for user-data transformations.

### 5.2 Catalog Mapping and Merge

Implement a pure catalog mapper and merge function with fixture tests:

1. Normalize provider IDs to strings and require title plus a valid movie/TV media type.
2. Map genre IDs to display names and parse provider date variants into ISO values.
3. Build renderable image URLs; choose the best logo deterministically, preferring an appropriate language and provider ranking.
4. Store streaming provider IDs by country and the exact offer keys `flatrate`, `rent`, and `buy`, not full provider payloads.
5. Keep cast, crew, seasons, image galleries, videos, traditional recommendations, similar results, and person details transient.
6. During refresh, use each non-empty incoming public value; retain the stored value when the new value is null, an empty string, or an empty array. Set `details_updated_at` to server time and never change original `created_at`.
7. Never include collection fields in the catalog merge. Overlay them after fetching the current user's row, guaranteeing user data cannot be replaced by provider refreshes.

### 5.3 User-Field Conflict Resolution

- All mutations use database/server time, not browser clocks.
- Update only fields explicitly present in a mutation. Each changed field gets its own timestamp.
- For future imports or sync payloads, compare each incoming field's timestamp independently: newer wins; a timestamped null can win over an older non-null value; if only one side has a timestamp, use that side.
- Make multi-field transitions atomic in a database transaction. For example, selecting Excited updates status, interest, and both timestamps together.
- Preserve `created_at` on updates and re-encounters. Refresh public metadata independently.
- Apply additive, versioned migrations. Backfill and validate before adding non-null constraints, and test migration from representative prior snapshots to protect collection continuity.

### 5.4 Collection Mutation State Machine

Centralize all save/removal behavior in one service used by every UI surface:

| Action | Unsaved behavior | Saved behavior |
|---|---|---|
| Set Active/Wait/Done/Quit | Create with selected status | Update status |
| Set Interested | Create/update `Later + Interested` | Atomically set both fields |
| Set Excited | Create/update `Later + Excited` | Atomically set both fields |
| Rate | Create as `Done`; leave interest unset | Update score only |
| Add first tag | Create as `Later + Interested` | Update trimmed, exact-value tag set |
| Remove/clear rating | No implicit save | Store null plus score timestamp |
| Reselect current visible status | Ask for destructive confirmation | Delete collection row after confirmation |
| Confirm status removal | Not applicable | Delete row, clearing all My Data and persisted Scoop |

Before any implicit save, upsert a normalized catalog snapshot. Returning payloads always contain the merged catalog plus current overlay so every caller updates consistently. Prevent concurrent duplicate saves with composite upserts and transactions.

The removal dialog always explains that status, interest, tags, rating, and Scoop will be deleted. Track confirmation count and, after a centralized configurable threshold, offer "do not ask again"; Settings must allow the warning to be re-enabled. Even when suppression is enabled, reselecting the active chip remains the deliberate removal gesture.

## 6. Server Interfaces and Provider Boundaries

### 6.1 Catalog and Collection APIs

- `GET /api/catalog/search?q=&page=&mediaType=`: debounced provider search with normalized tiles and current-user overlays.
- `GET /api/shows/:mediaType/:showId`: fetch provider detail and transient sections, merge non-empty public data, then attach current-user overlay.
- `GET /api/collection?filterType=&value=&mediaType=`: return merged saved shows plus available filter facets.
- `PATCH /api/shows/:mediaType/:showId/my-data`: accept a discriminated mutation (`setStatus`, `setInterest`, `setScore`, `addTag`, `removeTag`, `clearScore`) and execute the state machine.
- `DELETE /api/shows/:mediaType/:showId/my-data`: confirmed full collection removal.
- `GET /api/tags`: return the current user's trimmed, exact-value tag library and whether tagless shows exist.
- `GET /api/people/:personId`: normalize person profile, images, combined credits, and chart-ready source metrics.
- `GET/PATCH /api/settings`: read and validate authoritative user settings.
- `GET /api/export`: stream the generated ZIP.

Use a consistent error envelope with stable codes for validation, unauthenticated identity, provider configuration, provider timeout/rate limit, not found, and internal failure. Client features distinguish retryable provider failures from empty results.

### 6.2 Catalog Adapter

Define methods for search, show details, media assets/videos, credits, seasons, recommendations/similar, watch providers, person details/images/credits, lookup by external ID, and title search. Hide provider pagination, language codes, image URL construction, and payload schemas inside the adapter.

Provider failure behavior:

- Return partial detail when an optional transient section fails; mark that section retryable rather than failing the entire page.
- Use request deduplication/short server cache only for performance. Correctness cannot depend on cache.
- Do not overwrite good stored fields with sparse provider responses.
- Use accessible image fallbacks when no poster/backdrop/logo exists, and render a premium static header when no trailer is available.

### 6.3 AI Adapter and Prompt Modules

Create one provider-neutral interface supporting text generation, schema-constrained generation, and streaming. Store versioned prompt builders by surface, sharing a base persona and guardrails:

- TV/movie domain only.
- Spoiler-safe unless explicitly requested.
- Warm, joy-forward, opinionated, and honest rather than encyclopedic or indiscriminately positive.
- Vibe, structure, emotional palette, relationships, and craft over generic genre summaries.
- Concise by default, with more room for Scoop.

The server loads taste context for the effective identity and applies an explicit context matrix:

- General Ask always receives a bounded compact library/My Data profile plus recent turns and any conversation summary.
- Ask About This Show receives that taste profile plus full current-show context and the typed handoff identity.
- Scoop receives current-show facts, community reception signals, and the user's overlay when present.
- Single-show concepts receive current-show facts; Explore recommendations additionally receive selected concepts and the user's taste profile.
- Multi-show concepts receive every selected source show; Alchemy recommendations additionally receive selected shared concepts and the user's taste profile.

Compact library entries include status, interest, tags, score, and Scoop where relevant. Bound context by deterministic relevance/token rules while favoring high-rated, recently edited, tagged, and currently discussed shows. Never let one user's library enter another user's prompt.

### 6.4 AI Output Validation and Real-Show Resolution

- Validate all structured output at runtime. For Ask mentions, support the specified `commentary` plus exact `Title::externalId::mediaType;;...` `showList` contract; commentary must not expose IDs.
- Retry one time with stricter format instructions after structured parse failure. Then return usable unstructured commentary and Search handoff data rather than a broken interactive item.
- Parse concept output as bullets, trim bullet markers, enforce 1-3 words, remove duplicates/generic placeholders, cap returned count, and reject plot-heavy text.
- Resolve each recommendation by external ID first. Accept it only when media type is valid and resolved title matches case-insensitively. If no usable ID is present, perform deterministic title/media-type search and accept only an exact case-insensitive match.
- Deduplicate results, exclude input shows, preserve AI reasons only as transient session data, and return unresolved titles as non-interactive items with a Search action.
- Validate required unique cardinality after parsing and catalog resolution: eight concepts, five resolved Explore recommendations, or six resolved Alchemy recommendations. If filtering or resolution leaves a short set, retry once while asking for replacements for only the missing slots and excluding prior candidates. If the result remains short, return an explicit retryable incomplete-result error rather than presenting an undersized successful round; unresolved names may still be included in the error's Search handoff details.
- AI recommendations are never silently saved. Opening a resolved result uses normal Show Detail and collection rules.

## 7. Feature Implementation

### 7.1 App Shell and Collection Home

Build the shared shell, persistent Find/Settings actions, responsive filter navigation, page-level error boundary, and loading skeletons. Collection behavior:

- Fetch All Shows by default or restore a valid last filter.
- Derive tag filters, `No tags`, genres, decades, and community-score ranges from the current collection. Normalize community scores to the provider's 0-10 scale and use fixed ranges `0.0-4.9`, `5.0-6.9`, `7.0-7.9`, and `8.0-10.0`, inclusive at the displayed endpoints; items without a community score are excluded from score facets.
- Apply All/Movies/TV media type on top of the active filter.
- Group results in this order: Active with larger/prominent tiles; Excited (`Later + Excited`); Interested (`Later + Interested`); collapsed Other containing Wait, Quit, Done, and Later without interest.
- Sort every group by the greatest non-null My Data update timestamp (status, interest, tags, score, Scoop), newest first, then `created_at` newest first, then title and external ID for stable ties. This makes any recent personal edit visible and gives tests one deterministic rule.
- Show poster, title, in-collection badge, and user-score badge on reusable tiles.
- Use a collection-empty invitation to Search/Ask, and a separate "No results found" state for empty filters.

Test filter composition, decade/score boundaries, no-tag appearance, media toggle, grouping, stable sorting, collapsed state, and responsive navigation.

### 7.2 Search

- Implement straightforward catalog search without AI voice.
- Debounce non-empty terms, cancel stale requests, support pagination/load-more, and preserve query/results when returning from detail.
- Render a poster grid with collection and rating indicators from server overlays.
- Open Show Detail for valid results.
- On launch, redirect to Search only when the server setting is enabled; avoid a flash through Home.
- Provide initial guidance, no-result, missing-key/configuration, rate-limit, offline/network, and retry states.

### 7.3 Show Detail Foundation

Render the documented narrative hierarchy:

1. Header media carousel with inline trailer, backdrop/poster/logo fallback.
2. Core year/runtime or seasons/episodes and community-score bar.
3. My Tags, with relationship controls in the header/toolbar.
4. Overview and Scoop control/stream.
5. Ask About This Show.
6. Genres and languages.
7. Traditional recommendations.
8. Explore Similar.
9. Streaming availability for the user's configured country, separated into flatrate, rent, and buy offers, with an explicit unavailable-in-this-region state.
10. Cast and crew rails.
11. Seasons for TV.
12. Budget versus revenue for movies when present.

Implement status chips in the exact order `Active, Interested, Excited, Done, Quit, Wait`; do not show raw `Later` or hidden `Next`. Add the 0.5-10.0 rating control, tag picker/creation, optimistic pending states, mutation rollback, and destructive confirmation using the single collection service. Make the current state and implicit-save result clear without adding modal friction to non-destructive actions. Rating controls must expose an accessible label/value and keyboard operation.

Prioritize trailer motion when available without blocking reading, keep the early overview scan-length, and lay out long-tail cast/crew/seasons/financial sections full-bleed or otherwise visually separated so the page remains powerful without feeling crowded. Cover these density rules in desktop and mobile visual tests.

Transient section errors should not erase core detail or My Data. Missing optional data suppresses or explains only the relevant section.

### 7.4 Scoop

- The closed control reads "Give me the scoop!" when no valid Scoop exists and "Show the scoop" when a fresh cached Scoop exists; the open section is titled "The Scoop".
- For a stored Scoop younger than four hours, return it without an AI call. At or after expiry, regenerate only when requested.
- Stream visible text progressively with a Generating state and cancellation handling.
- Target 150-350 words with a personal take, honest stack-up against reception, a larger emotional Scoop centerpiece, fit/warnings, and a "Worth it?" verdict.
- Capture collection membership at request start. Persist generated content and server timestamp only when the show was already saved at that point and the same collection row still exists at completion. A save that occurs during an originally unsaved request does not make that Scoop persistent, and a concurrent removal never recreates the show.
- Keep an unsaved show's generated Scoop in page/session state only.

Unit-test the four-hour boundary, saved/unsaved persistence, concurrent removal, prompt sections, stream error recovery, and cached control copy.

### 7.5 Ask

Welcome state:

- Keep a curated pool of starter prompts in configuration and show six unique random prompts. Provide a visible, accessible `Refresh starters` control that chooses a new six without submitting a message or resetting a conversation.
- Selecting a starter submits it as a normal user turn.

Conversation state:

- Store turns, summary, mentioned shows, pending state, and handoff-show context in the current browser session only. Reset and leaving Ask clear them; do not write chat content to Supabase or durable browser storage.
- Render user/assistant dialogue, streaming response state, retry, cancel, and a horizontal deduplicated mentioned-shows rail.
- Send recent turns plus a 1-2 sentence persona-consistent summary of older turns. Trigger summarization after approximately ten messages, retain enough recent turns for conversational continuity, and replace older content only after successful summary generation.
- Resolve structured mentions to real show tiles. Unresolved mentions remain text/Search handoffs.
- Ask About This Show navigates to Ask with a typed handoff containing the show identity and seeds system/context state visibly (for example, a "Talking about ..." banner) without fabricating a user message. Its prompt mirrors the show's emotional color, remains brief/showman-like, and may include small verified insider context such as reception or cancellation status.
- Keep direct answers within the first 3-5 lines, default to 1-3 tight paragraphs, use bullets for multiple recommendations, and stay in the entertainment domain.
- Across Ask outputs, prefer casual contractions, vivid specific flavor, quick contrasts, and practical fit framing. Human/fixture evaluation rejects sterile encyclopedia voice, hedging walls, moralizing, excessive preambles, and unverified insider claims.

### 7.6 Explore Similar

- Initial detail-page state shows a one-line explanation of why concepts matter and a `Get Concepts` action.
- Generate exactly eight single-show concepts as 1-3 word, spoiler-free, varied chips ordered by strength.
- Require at least one selection and cap selection at eight. Explain that the user is choosing ingredients they want more of.
- Changing concept selection clears prior recommendations.
- `Explore Shows` requests exactly five recommendations, each with a 1-3 sentence reason explicitly naming aligned concepts.
- Bias toward recent titles without excluding classics or hidden gems. Exclude the source show.
- Keep concepts, recommendations, and reasons in detail-page session state only. Render resolved real tiles and Search handoffs for unresolved titles.

### 7.7 Alchemy

Implement a clear staged state machine inside Find:

1. Select at least two source shows from both the current library and catalog search; deduplicate by media type/external ID.
2. `Conceptualize Shows` requests exactly 12 concepts shared across every selected input, providing a larger pool than the single-show flow.
3. Select one to eight concepts.
4. `ALCHEMIZE!` requests exactly six recommendations with concept-specific reasons.
5. `More Alchemy!` requires at least two selected resolved results, replaces the prior source set with those results, and clears concepts, selections, and recommendations before the next Conceptualize step.

Backtracking rules:

- Adding/removing source shows clears concepts, selections, and results.
- Changing concept selection clears results.
- Leaving/resetting Alchemy clears all session state and reasons.
- Disable downstream actions with actionable guidance until prerequisites are met.
- Preserve the 2+ source and 1-8 concept constraints on both client and server.

Multi-show concepts must be shared commonalities, not a union of unrelated traits. Ensure diversity across structure, vibe, emotion, relationship, and craft axes and order strongest "aha" concepts first.
Alchemy recommendations share Explore's recent-title bias without excluding classics or hidden gems.

### 7.8 Person Detail

- Fetch and render profile images, name, biography, and graceful missing-image/bio states.
- Normalize acting and crew credits, deduplicate repeated jobs where appropriate, and group filmography by year with unknown dates last.
- Compute chart data in pure utilities: average community rating by release/first-air year, top genres by credited-project count, and project count by year. Exclude missing ratings from averages, place missing dates in an Unknown filmography group, and label low-sample data.
- Make charts responsive, provide accessible text/table summaries, and use theme tokens.
- Selecting any movie/TV credit opens Show Detail and receives the normal current-user overlay.

### 7.9 Settings and Export

Settings:

- Persist font sizes XS through XXL and apply the selected root typography token across the application.
- Persist Search on Launch, username, AI provider/model, streaming country, catalog/AI credential status, and removal-confirmation preference. The catalog provider name is read-only namespace configuration rather than a user-selectable identity source.
- Validate settings on both client and server, save field-level changes without overwriting concurrent unrelated fields, and show pending/success/error feedback.
- Let a stored user credential override the corresponding benchmark environment credential; deleting it restores the environment fallback. Support create/replace/delete without ever revealing either source's secret in the UI, and document the precedence.

Export:

- Query all saved collection items for only the effective `(namespace_id, user_id)` and join current catalog snapshots.
- Produce `my-data-YYYY-MM-DD.zip` containing one human-readable `my-data.json`. Its versioned root DTO is `{ formatVersion, exportedAt, shows }`; `shows` is stably ordered by media type, title, and external ID.
- Each exported show includes every persisted catalog field (identity/external IDs, title/type, overview, genres, tagline/homepage, separate language arrays/codes, image URLs, community/popularity values, all air/release dates, movie/TV facts, provider IDs by country/offer type, catalog creation/details timestamps) and every collection field (status, interest, exact tags, score, Scoop, each field's update timestamp, collection creation timestamp, and test marker). Every date is ISO-8601 and nullable fields remain explicit.
- Exclude settings in v1, along with API keys, credential ciphertext, transient cast/crew/media/recommendations, Ask history, and Alchemy state.
- Stream the archive without writing it to the repository/server disk, and return a valid empty `shows` array for an empty library rather than failing.
- Add schema snapshot and ZIP-content tests so future migrations can maintain export compatibility. Import remains out of scope, but the versioned format is designed for it.

## 8. AI Quality Assurance

Create deterministic prompt/parse tests plus an opt-in live-model evaluation suite. The live suite must not run as part of ordinary offline CI unless credentials are supplied.

Score representative Scoop, Ask, concepts, Explore Similar, and Alchemy outputs from 0-2 on:

- Voice adherence.
- Taste alignment.
- Surprise without betrayal.
- Specific reasoning.
- Real-show integrity.

Passing requires voice at least 1, taste alignment at least 1, real-show integrity exactly 2, and total at least 7/10. Add curated golden scenarios over time for high-rated/tagged libraries, mixed-reception shows, cross-genre concept blends, classics versus recent titles, and intentionally unresolvable recommendations.

Automated hard checks cover counts (8 single-show concepts, 12 multi-show concepts, 5 Explore recs, 6 Alchemy recs), concept length/format, reason presence and concept references, spoilers in fixture scenarios, duplicate/input recommendations, and catalog ID/title agreement. Human review remains necessary for warmth, honesty, surprise, and specificity.

## 9. Implementation Phases and Exit Criteria

### Phase 0: Bootstrap and Contracts

- Scaffold latest stable Next.js/TypeScript, linting, formatting, tests, theme, and responsive shell primitives. Establish adjacent critical unit tests, feature-local `constants.ts`, global `src/config` constants, humble TSX components, and no-inline-style conventions.
- Add validated environment loading, `.env.example`, safe `.gitignore`, and scripts for dev, build, lint, test, end-to-end test, migrations, and namespace reset.
- Establish domain/provider types and test-fixture conventions.

Exit: a clean install can lint, test, build, and start by filling environment variables only; no secret is committed; Docker is not required.

### Phase 1: Database, Identity, and Isolation

- Add migrations, generated DB types, identity resolver, Supabase server client, repositories, RLS defaults, and namespace reset script.
- Add catalog, collection, settings, and metadata tables with keys, constraints, and indexes.
- Test partition isolation, production rejection of dev identity headers, fixed benchmark identity under `next start`, scoped reset, and representative migration/backfill.

Exit: destructive integration tests can seed/reset one namespace without touching another, and all user records require an opaque user ID.

### Phase 2: Catalog and Collection Domain

- Implement provider adapter, fixture-backed normalization, non-empty catalog merge, overlay assembly, filter facets, and collection mutation state machine.
- Add search/detail/collection/my-data/tags APIs.
- Cover all explicit-save, implicit-save, removal, re-add, timestamp, duplicate, and concurrent mutation rules.

Exit: API tests prove one canonical merged show is returned everywhere and catalog refresh cannot erase My Data or good public metadata.

### Phase 3: Collection Home and Search

- Build App Shell, filter navigation, grouped Home, shared tiles/rails, media toggle, empty states, Search mode, pagination, and Search on Launch.
- Add component, accessibility, visual, and mobile/desktop end-to-end coverage.

Exit: users can find a title, see collection indicators, open it, save it through each trigger, and find it correctly grouped/filtered on Home.

### Phase 4: Core Show Detail and Person

- Build header media, core facts, relationship controls, tags/rating, overview, traditional recs, providers, credits, seasons, finances, and partial-error behavior in required order.
- Build Person page, analytics, filmography, and detail navigation.

Exit: movie and TV fixture journeys render correct conditional sections, all mutations obey domain rules, and talent deep-dives round-trip to show detail.

### Phase 5: Shared AI Foundation and Scoop

- Add AI adapter, versioned base persona, taste-context builder, structured-output validation/retry, streaming infrastructure, rate limiting, and logging redaction.
- Implement Scoop freshness, streaming, and conditional persistence.

Exit: cached/expired, saved/unsaved, missing-key, timeout, malformed-output, and concurrent-removal cases pass; voice contract receives human review.

### Phase 6: Ask

- Implement starters, ephemeral chat state, streaming turns, summarization, exact mention parsing, catalog resolution, mentioned rail, reset, and show-context handoff.

Exit: a mocked multi-turn session summarizes after the threshold, keeps persona/context, opens resolved mentions, hands unresolved names to Search, and leaves no durable chat data.

### Phase 7: Concepts, Explore Similar, and Alchemy

- Implement concept generation/validation/chips, recommendation resolution/reasons, Explore's five-result flow, Alchemy's six-result staged/chained flow, and state invalidation.
- Add quality hard checks and opt-in golden evaluations.

Exit: both workflows enforce counts and selection constraints, reasons reference selected concepts, results resolve with exact ID/title integrity, and all session data clears at documented boundaries.

### Phase 8: Settings, Export, and Production Hardening

- Complete settings, encrypted user-credential handling, export, removal-warning preferences, and readability scaling.
- Add error boundaries, retry/cancel behavior, accessibility audit, responsive visual tests, provider-contract tests, security checks, and operational documentation.
- Run full lint, typecheck, unit, integration, end-to-end, migration, production build, and namespace-isolation suites against hosted Supabase without Docker.

Exit: all key user journeys pass, export contains complete My Data and no secrets, client storage can be cleared without data loss, and a second namespace/user remains isolated throughout destructive tests.

## 10. Test Matrix

### Unit Tests

- Catalog mapping, media identity, separate date/language/provider-offer fields, sparse merge, image/logo selection, and date parsing.
- Status/interest transitions, implicit saves, rating range/step/clear, exact tag normalization, removal, per-field timestamps, and conflict resolution.
- Filter facets/composition, status grouping, sorting, score/decade ranges, and person chart calculations.
- Scoop freshness, context selection, concept parser/quality filters, mention parser, recommendation resolver, deduplication, and state-machine invalidation.
- Export serialization, ISO dates, format version, and secret exclusion.

### Integration and Contract Tests

- SQL constraints/migrations and generated types.
- Repository partition predicates for two namespaces and two users.
- Namespace-only reset behavior.
- Every route's validation, identity resolution, and error envelope.
- Catalog and AI adapters against recorded fixtures, including sparse, malformed, timeout, rate-limit, and not-found responses.
- Atomic concurrent save/removal/Scoop scenarios.

### Component and Visual Tests

- Show tiles and badges, grouped collection, filter navigation, relationship controls, tag picker, rating keyboard behavior, removal dialog, media fallbacks, Ask turns/mentions, concept selection, Alchemy stages, charts, and all empty/loading/error states.
- Desktop and mobile snapshots for Collection, Search, Detail movie/TV, Person, Ask, Alchemy, and Settings using stable fixtures.

### End-to-End Journeys

1. Search, save as Interested/Excited/Active, tag/rate, and observe Home grouping/filtering.
2. Rate an unsaved show and verify `Done`; tag an unsaved show and verify `Later + Interested`.
3. Reselect a status, confirm removal, and verify every My Data field and Scoop is gone.
4. Re-encounter/upsert a show while it remains saved and verify newest user fields survive refreshed catalog details.
5. Remove and later re-add a show and verify old My Data stays cleared and the triggering action supplies fresh defaults.
6. Ask for recommendations, refresh starter prompts, open a resolved mention, save it, reset, and verify chat is not persisted.
7. Generate a Scoop before and after save and around the four-hour boundary, including save/remove changes during generation.
8. Complete Explore Similar and save a result.
9. Complete and chain Alchemy from at least two selected results, backtrack, and verify downstream state clears.
10. Open cast/crew, inspect analytics/filmography, and open a credit.
11. Change readability/Search on Launch/streaming country, clear browser storage, and verify backend settings/data remain.
12. Export and inspect the fixed, complete, ISO-dated, secret-free `my-data.json` inside the ZIP.
13. Run simultaneous namespace/user fixtures and prove no reads, writes, exports, or resets cross partitions.

## 11. Operational and Documentation Deliverables

- `README` setup for hosted Supabase as the primary path and optional local Supabase without making Docker mandatory.
- Environment variable reference and credential precedence.
- One-command dev, test, production build/start, migration, and namespace reset instructions.
- Benchmark fixed-identity mode documentation, including its production-build behavior, plus the development-only header override and production-auth migration path.
- Migration and rollback/forward-fix procedure that never drops user collections.
- Provider adapter and AI prompt versioning guidance.
- Export schema documentation.
- Known optional extensions: OAuth wiring, import/restore, first-class Next status, named lists, saved Alchemy sessions, and richer golden-set evaluation.

## 12. Final Acceptance Checklist

- Every saved item and user setting is scoped by `(namespace_id, user_id)`; every reset is namespace-only.
- Supabase is the source of truth; clearing local storage loses no collection or authoritative settings.
- User overlays and their independent timestamps survive catalog refreshes, re-encounters, concurrency, and schema migrations.
- All saving defaults and destructive removal semantics match the PRD from every entry surface.
- Home grouping, filters, type toggle, indicators, empty states, and Search on Launch behave consistently on desktop and mobile.
- Show Detail preserves the required narrative order and movie/TV conditional sections, with graceful media/data fallbacks.
- Person profiles, filmography, charts, and credit navigation are complete and accessible.
- Ask, Scoop, Explore Similar, and Alchemy share one spoiler-safe, warm, specific, opinionated voice grounded in the current user's taste.
- Concepts and recommendations meet exact counts, selection caps, transient-storage rules, reason requirements, and real-catalog integrity.
- Scoop alone persists as AI data, only for saved shows, and respects four-hour on-demand freshness.
- Export contains all saved shows/My Data and ISO timestamps in a versioned ZIP/JSON format, with no secrets.
- The project is lint-clean, type-safe, migration-tested, accessible, responsive, provider-failure tolerant, and runnable against hosted Supabase without Docker or source edits.
