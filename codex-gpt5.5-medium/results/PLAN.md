# Implementation Plan

## 1. Product Understanding

Build a personal TV and movie companion where the user's saved version of each catalog item is the source of truth everywhere it appears. The application must support a durable collection, status and interest workflows, free-form tags, personal ratings, AI Scoop, conversational Ask, concept-driven Explore Similar, Alchemy blending, person detail pages, settings, and export. Discovery quality is part of the product contract: AI output must use the shared warm, opinionated, spoiler-safe persona and all actionable recommendations must resolve to real catalog items.

The benchmark baseline requires Next.js latest stable and Supabase. Backend persistence is authoritative; local storage is only disposable UI/cache state. Every persisted user-owned record must be partitioned by both `namespace_id` and `user_id`, with reset tooling scoped to a namespace.

## 2. Architecture

### 2.1 Application Stack

- Use Next.js App Router with TypeScript.
- Use Supabase official clients for database access.
- Keep browser Supabase access limited to anon/public operations; place any privileged reset, migration helper, or service-role operation behind server-only code.
- Use server actions or route handlers for mutations that require identity, namespace enforcement, catalog enrichment, AI orchestration, or export generation.
- Use React client components only for interactive surfaces such as rating sliders, chips, chat, concept selection, carousels, and filters.

### 2.2 Directory Shape

Follow the repo instructions' fractal architecture:

- `src/config/`: environment parsing, constants, status/interest definitions, catalog and AI provider constants.
- `src/theme/`: design tokens, typography scale, responsive layout tokens.
- `src/components/`: shared primitives such as tiles, chips, segmented controls, sliders, modal, carousel, horizontal strand, loading skeletons, error states.
- `src/lib/`: Supabase clients, catalog client, AI client, zip/export utilities, identity and namespace helpers.
- `src/domain/`: pure domain logic for show merging, status transitions, filters, concept parsing, recommendation resolution, timestamp conflict resolution.
- `src/pages/` or App Router route folders following equivalent page/feature structure:
  - Home collection
  - Find with Search, Ask, Alchemy features
  - Show Detail
  - Person Detail
  - Settings

TSX files should bind state and markup only. Business logic should live in hooks and pure utilities colocated with the feature when feature-specific.

## 3. Environment and Developer Workflow

### 3.1 Required Environment Variables

Create `.env.example` with documented variables:

- `NEXT_PUBLIC_SUPABASE_URL`: Supabase project URL.
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`: browser-safe Supabase anon key.
- `SUPABASE_SERVICE_ROLE_KEY`: server-only key for namespace reset/test utilities, never exposed to client code.
- `NEXT_PUBLIC_NAMESPACE_ID`: stable build/run namespace used by client-visible reads and writes.
- `DEFAULT_USER_ID`: default benchmark user for dev/test identity injection.
- `CATALOG_API_KEY`: server-side catalog provider key.
- `AI_API_KEY`: server-side AI provider key.
- `AI_MODEL`: default AI model key.
- Optional `NEXT_PUBLIC_DEV_IDENTITY_ENABLED`: gates dev-only identity selector/header behavior.

Ensure `.gitignore` excludes all `.env*` except `.env.example`.

### 3.2 Scripts

Add one-command workflows:

- `npm run dev`: start the Next app.
- `npm test`: run unit/integration tests.
- `npm run build`: production build.
- `npm run lint`: lint and type-oriented static checks.
- `npm run test:reset`: delete test data for the configured namespace only.
- `npm run db:migrate`: apply Supabase migrations.
- `npm run db:seed`: optional namespace-scoped seed data.

Document hosted Supabase as the primary path. Docker/local Supabase may be optional, but must not be required.

## 4. Persistence Model

### 4.1 Supabase Schema

Create repeatable migrations for:

- `shows`: catalog item plus user overlay, scoped by `namespace_id` and `user_id`.
- `cloud_settings`: synced user settings, scoped by `namespace_id` and `user_id`.
- `app_metadata`: namespace-scoped data model version.
- Optional `users` or `dev_identities`: opaque user records for benchmark/dev flows.

Recommended `shows` unique key:

- `(namespace_id, user_id, show_id)`

Core columns should represent the technical schema:

- Catalog identity and metadata: title, media type, external IDs, overview, genres, images, dates, ratings, runtime/TV fields, provider data.
- User fields: tags, score, status, interest.
- Per-field update timestamps for tags, score, status, interest, and AI Scoop.
- AI fields: `ai_scoop`, `ai_scoop_update_date`.
- Management fields: details update date, creation date, `is_test`.

Use JSONB for flexible objects such as `external_ids`, `provider_data`, arrays that benefit from JSON storage, and migration-compatible catalog metadata. Use constraints/enums or check constraints for status, interest, media type, and font sizes.

### 4.2 Row-Level Safety

Even if the benchmark uses dev identity injection, all queries must include namespace and user scope. Add database indexes for common filters:

- `(namespace_id, user_id, my_status)`
- `(namespace_id, user_id, show_type)`
- GIN index for tags/genres if stored as arrays or JSONB
- date/rating indexes as needed for sorting/filtering

If Supabase RLS is enabled, policies must enforce namespace/user ownership. If RLS is not practical for the benchmark, centralize all data access behind server helpers that require `RequestContext { namespaceId, userId }`.

### 4.3 Merge and Save Semantics

Implement pure domain functions for:

- `mergeCatalogShow(existing, incoming)`: non-user fields use first non-empty new value, never overwriting stored non-empty values with empty/nil values.
- `mergeUserFieldsByTimestamp(existing, incoming)`: newer per-field timestamp wins.
- `saveByStatus(status)`: setting any status saves the show.
- `saveByInterest(interest)`: sets status `later` and selected interest.
- `saveByRating(score)`: unsaved shows default to status `done`.
- `saveByTag(tag)`: unsaved shows default to status `later` and interest `interested`.
- `clearStatus()`: confirms removal, deletes the stored show, and clears all My Data.
- `refreshCatalogDetails()`: updates public metadata and `details_update_date` while preserving user overlay.

Treat collection membership as `my_status != null`.

## 5. Identity and Namespace Isolation

Implement a request context layer used by every server action and route handler:

- Resolve `namespace_id` from environment or a controlled test header.
- Resolve `user_id` from dev-only identity injection, header, selector, or fixed default.
- Treat user IDs as opaque strings.
- Gate header-based identity injection to development/test or an explicit env flag.

Build `test:reset` as a server script that deletes only rows matching the active namespace. Do not perform global database teardown.

## 6. External Catalog Integration

Create a provider abstraction so product code is not tightly coupled to one catalog vendor:

- Search by text and media type.
- Fetch full show/movie details.
- Fetch images/logos/backdrops/videos.
- Fetch similar and recommended shows.
- Fetch credits, crew, people, images, and filmography.
- Fetch seasons for TV.
- Fetch streaming providers by region.
- Resolve AI recommendations by external ID first, then title/media type match.

Mapping rules:

- Decode external payloads into a normalized `Show`.
- Infer media type if missing; reject unknown items for actionable recommendations.
- Choose deterministic poster, backdrop, and logo URLs.
- Store provider IDs by country, not full provider objects.
- Keep transient details such as cast, crew, seasons, videos, recommendations, similar, and image galleries out of persisted show rows.

## 7. AI System

### 7.1 Shared AI Layer

Create an AI service with provider abstraction, prompt builders, structured parsing, retry behavior, and test doubles. Every AI request should receive only the context needed for the surface:

- User library with status, interest, tags, ratings, and relevant AI Scoop.
- Current show context for Scoop and Ask about this show.
- Selected concepts for Explore Similar and Alchemy.
- Recent chat turns and a short persona-preserving summary when history grows beyond roughly 10 messages.

All surfaces must enforce:

- TV/movie domain only.
- Spoiler-safe by default.
- Warm, playful, opinionated, honest voice.
- Concrete vibe/structure/craft reasoning.
- No generic filler.

### 7.2 Scoop

Implement on-demand generation from Show Detail:

- If cached Scoop exists and is fresher than 4 hours, show cached content.
- If stale or absent, regenerate on demand.
- Stream progressive text where possible.
- Persist only if the show is in the collection; otherwise keep ephemeral.
- Include personal take, honest stack-up, the emotional Scoop centerpiece, fit/warnings, and verdict.

### 7.3 Ask

Implement session-only chat state:

- Welcome screen with 6 random starter prompts and refresh.
- Chat turns retained during the session only.
- Older turns summarized after about 10 messages.
- Structured mentioned-show extraction: `commentary` plus `showList` in `Title::externalId::mediaType;;...` format.
- Parse and resolve mentioned shows into a horizontal strip.
- Retry once if structured parsing fails, then fall back to unstructured text plus Search handoff.
- Support "Ask about this show" by seeding show context when launched from Detail.

### 7.4 Concepts, Explore Similar, and Alchemy

Concept generation:

- Single-show concepts for Explore Similar.
- Multi-show shared concepts for Alchemy.
- Bullet-list only, 1-3 words, evocative, spoiler-free, ordered by strength.
- Avoid generic concepts and plot details.

Explore Similar:

- Get concepts for one show.
- Allow selecting at least 1 concept, consistent with Alchemy's cap.
- Fetch 5 real catalog-backed recommendations.
- Each reason must name selected concepts.

Alchemy:

- Select 2+ input shows from library and global catalog.
- Conceptualize shared concepts.
- Select 1-8 concepts.
- Fetch 6 real catalog-backed recommendations.
- Changing inputs clears concepts and results; changing concepts clears results.
- "More Alchemy" starts another round using selected/result shows as inputs.

## 8. UI Implementation Plan

### 8.1 Shared UI Foundations

Build accessible, responsive primitives:

- Show tile with poster, title, in-collection badge, and user-rating badge.
- Status/interest chip controls.
- Rating slider/control.
- Tag picker and tag chips.
- Media type segmented control: All, Movies, TV.
- Filter navigation.
- Horizontal strands.
- Modal confirmation.
- Carousel/video header with graceful fallback.
- Streaming provider row.
- Chat message list and composer.
- Concept chips with capped selection.

Keep status chips and primary relationship controls prominent and direct. Avoid modal walls except destructive removal confirmation.

### 8.2 Collection Home

Implement default library view:

- Sidebar/filter panel: All Shows, tag filters, No tags when applicable, genre, decade, community score.
- Media-type toggle applies on top of selected filter.
- Group filtered collection into:
  1. Active with prominent tiles.
  2. Excited (`later` + `excited`).
  3. Interested (`later` + `interested`).
  4. Collapsed other statuses: Wait, Quit, Done, Later without interest, optional Next if present.
- Empty collection state points to Search/Ask.
- Empty filtered state says no results found.

### 8.3 Find / Discover

Create one hub with a clear mode switcher:

- Search: straightforward catalog search, no AI voice, poster grid, in-collection markers, opens Detail.
- Ask: chat flow described above.
- Alchemy: multi-step concept blending flow.

Support Search on Launch by reading the user setting and opening Find/Search on app load.

### 8.4 Show Detail

Implement as the single source of truth for public facts plus My Data:

1. Header media carousel with trailers/backdrops/posters/logos and fallback.
2. Core facts row: year, runtime or seasons/episodes, community score.
3. Toolbar status/interest chips: Active, Interested, Excited, Done, Quit, Wait; Interested and Excited map to Later plus interest.
4. My Rating: rating unsaved show auto-saves as Done.
5. My Tags: adding a tag to unsaved show auto-saves as Later/Interested.
6. Overview.
7. Scoop toggle with cached/generated states.
8. Ask about this show CTA.
9. Genres and languages.
10. Traditional recommendations strand.
11. Explore Similar concept flow.
12. Streaming availability.
13. Cast and Crew strands.
14. TV seasons when relevant.
15. Movie budget/revenue when relevant.

Ensure any instance of a show displayed on this page or elsewhere uses the saved user overlay when present.

### 8.5 Person Detail

Implement person pages from cast/crew:

- Image gallery, name, bio.
- Filmography grouped by year.
- Analytics charts for average project ratings, top genres, and projects by year.
- Credits open Show Detail with normalized catalog mapping and user overlay.

### 8.6 Settings and Data

Implement:

- Font size/readability selection.
- Search on launch toggle.
- Username setting.
- AI provider key/model fields if supported by benchmark mode, with no secrets committed and server-only handling for sensitive values.
- Catalog provider key handling through environment/server configuration.
- Export My Data to a `.zip` containing JSON backup of all saved shows and My Data with ISO-8601 dates.

Import/Restore is optional/open and should be deferred unless time remains.

## 9. Data Export

Add a server route/action for export:

- Query all saved shows for the active `(namespace_id, user_id)`.
- Include cloud settings, app metadata, local settings that are relevant and safe, and UI state if desired.
- Serialize dates as ISO-8601.
- Package JSON in a zip.
- Exclude secrets such as API keys unless product explicitly allows user-entered key export; safest benchmark default is to omit secrets.

## 10. Testing and Quality Gates

### 10.1 Unit Tests

Prioritize pure domain tests for:

- Status and interest transitions.
- Rating-to-save and tag-to-save defaults.
- Removal clearing all My Data.
- Merge behavior for catalog fields.
- Timestamp conflict resolution for My Data.
- Filter grouping and media-type filtering.
- Concept parser and structured Ask parser.
- AI cache freshness.
- Recommendation resolution by external ID and title/media type.

### 10.2 Integration Tests

Cover:

- Supabase data access always scopes by namespace and user.
- Namespace reset deletes only matching namespace data.
- Collection CRUD flows persist server-side.
- Clearing client storage does not remove backend data.
- Export contains only current user's namespace data.
- Search result overlay displays saved status/rating/tags.

### 10.3 UI and Journey Tests

Use Playwright or equivalent for:

- Build collection through Search -> Detail -> Interested/Excited.
- Rating unsaved show saves as Done.
- Tag unsaved show saves as Later/Interested.
- Home grouping and tag filters.
- Ask returns commentary and mentioned shows strip.
- Explore Similar concept selection and recommendation results.
- Alchemy full flow and chaining.
- Person Detail -> credit -> Show Detail.
- Settings search-on-launch behavior.
- Export zip download.

### 10.4 AI Quality Validation

Create deterministic mocks for automated tests, plus a manual golden-set checklist based on the discovery quality bar:

- Voice adherence >= 1.
- Taste alignment >= 1.
- Real-show integrity = 2.
- Total >= 7/10.
- Concepts are 1-3 words, varied, specific, and spoiler-free.
- Explore Similar returns 5 recs; Alchemy returns 6 recs.

## 11. Implementation Sequence

### Phase 1: Project Foundation

- Scaffold Next.js, TypeScript, lint, test runner, app shell, and theme tokens.
- Add `.env.example`, `.gitignore` updates, and scripts.
- Add Supabase clients and request context helpers.
- Create migrations for namespace/user-scoped schema.
- Implement namespace reset script.

Exit criteria:

- App starts.
- Build/test commands run.
- Empty database can be migrated.
- Test reset is namespace-scoped.

### Phase 2: Domain and Persistence

- Implement normalized Show types and mapping utilities.
- Implement merge, save, removal, and filter domain functions.
- Implement server-side collection repository with mandatory context scope.
- Add unit and integration tests for data behavior.

Exit criteria:

- All core save/remove/merge rules are covered by tests.
- Data remains after clearing browser storage.

### Phase 3: Catalog Integration

- Implement catalog provider abstraction and first concrete provider.
- Add search, detail, credits, person, recommendations, videos/images, providers, and seasons fetches.
- Implement external catalog to Show mapping.
- Implement recommendation resolution contract.

Exit criteria:

- Search and detail data can be fetched and normalized.
- Saved overlays are merged into catalog results.

### Phase 4: Collection Home and Search

- Build app shell with navigation/filter panel.
- Implement Home grouping, filters, media toggle, tile badges, and empty states.
- Implement Find/Search with result grid and Detail navigation.

Exit criteria:

- User can search, open details, save shows, and see collection grouping update.

### Phase 5: Show Detail Core

- Build header media, facts, rating, status/interest controls, tags, overview, recommendations, providers, cast/crew, seasons, and budget/revenue.
- Implement removal confirmation with suppression/count UI state.
- Ensure all My Data writes use server-side persistence and timestamps.

Exit criteria:

- Detail page satisfies save defaults and removal semantics.
- UI reflects user's overlaid version everywhere.

### Phase 6: AI Foundation and Scoop

- Implement AI provider abstraction, prompt builders, parser/retry utilities, and mock provider.
- Implement Scoop generation, streaming, 4-hour freshness, and collection-only persistence.
- Add tests for cache behavior and persistence rules.

Exit criteria:

- Scoop works on saved and unsaved shows with correct persistence behavior.

### Phase 7: Ask

- Build Ask welcome prompts, chat UI, session state, summarization, and mentioned shows strip.
- Implement structured `commentary` + `showList` parsing and resolution.
- Implement Ask about this show handoff from Detail.

Exit criteria:

- Ask is session-only, taste-aware, resolves actionable shows, and gracefully falls back on parse failures.

### Phase 8: Concepts, Explore Similar, and Alchemy

- Implement concept generation for single and multi-show inputs.
- Build Explore Similar inside Detail.
- Build Alchemy selection, concept, recommendation, and chaining flow.
- Enforce selection caps and downstream clearing rules.

Exit criteria:

- Explore Similar returns 5 resolved recs.
- Alchemy returns 6 resolved recs and supports chaining.

### Phase 9: Person Detail, Settings, and Export

- Implement Person Detail pages with analytics charts and filmography.
- Implement settings for font size, search on launch, username, model/key configuration as appropriate.
- Implement export zip.

Exit criteria:

- Talent deep-dive and backup journeys are complete.

### Phase 10: Hardening and Acceptance

- Complete journey tests.
- Run lint, tests, build.
- Verify namespace/user isolation manually and via tests.
- Run AI golden-set manual checks with real provider if credentials are available.
- Polish loading, error, and empty states.

Exit criteria:

- All required user journeys pass.
- Build is compliant with the infrastructure rider.
- No secrets are committed.

## 12. Key Risks and Mitigations

- AI hallucinated recommendations: require structured output, resolve by external ID, verify title/media type, and fall back to non-interactive/Search handoff.
- Namespace leakage: centralize context construction, make repository functions require context, and test cross-namespace isolation.
- User overlay loss during catalog refresh: keep merge behavior pure and heavily tested.
- Prompt drift: centralize persona and surface contracts, use manual quality rubric and deterministic mocks.
- Secret exposure: keep provider keys server-side, document env setup, and exclude `.env*` from commits.
- Overbuilding optional features: defer Import/Restore, named custom lists, first-class Next status, and saved Alchemy sessions unless required later.

## 13. Definition of Done

- Next.js app runs with hosted Supabase through environment configuration.
- Fresh database can be migrated deterministically.
- All user-owned records are scoped by `(namespace_id, user_id)`.
- Namespace reset works without global teardown.
- Collection, Search, Detail, Ask, Alchemy, Explore Similar, Person, Settings, and Export journeys are implemented.
- User edits always override refreshed public catalog data.
- AI outputs follow voice, concept, count, spoiler-safety, and real-show integrity requirements.
- Tests cover core domain behavior, isolation, and required journeys.
- `npm run build`, `npm test`, and lint/static checks pass.
