# Implementation Plan: Personal TV & Movie Companion

## 1. Delivery boundaries and technical decisions

Build a Next.js (latest stable) TypeScript application using the App Router, with Next route handlers/server actions as the server boundary and Supabase (official client libraries) as the durable backend. The implementation will be a responsive web app; no offline-first behavior is required and browser storage is only allowed for disposable UI/cache state.

Use adapters at the server boundary for both the external content catalog and AI provider. This keeps provider keys server-side, makes catalog/AI responses testable with fixtures, and allows the product behavior to remain unchanged if either provider changes. The catalog adapter must supply search, full detail, people/credits, providers, and ID lookup. The AI adapter must support structured recommendation/mention output and streaming Scoop text.

The Supabase database is the source of truth. Every user-owned row is partitioned by both `namespace_id` and opaque `user_id`; all reads, writes, exports, and test-reset operations use that pair. In development/test, resolve these identities from documented, production-gated configuration/header injection (with a stable default), behind one `getRequestIdentity` abstraction so future OAuth only replaces that implementation.

Explicitly defer the PRD's open questions: visible `Next` status, named custom lists, Scoop-save behavior for an unsaved show, explicit unrated state, import/restore, saved Alchemy blends, and sidebar status filters. Do not silently implement any of them as required product behavior.

## 2. Repository foundation and operational contract

1. Scaffold the Next application and configure strict TypeScript, linting, unit tests, and browser/integration tests. Add a style system with design tokens for color, type scale, spacing, radii, and readable font-size variants. Avoid inline pixel/color values in TSX.
2. Add `.env.example` with comments for Supabase URL, Supabase anon/public key, server-only Supabase service key (only when required for reset/admin work), namespace ID, dev user ID and gating flag, catalog provider key/base URL, and AI provider key/model. Update `.gitignore` to ignore `.env*` while retaining `.env.example`; never expose elevated keys to client bundles.
3. Supply documented scripts for development, unit/integration tests, production build/start, lint/type check, database migration application, and `test:reset -- --namespace <id>` (or equivalent). The reset script must require an explicit namespace and only delete rows in that namespace.
4. Add repeatable Supabase SQL migrations, local test fixtures/mocks, and a short setup guide covering hosted Supabase as the primary path. Docker/local Supabase may be optional convenience only, never a requirement.
5. Establish server-side error normalization, request validation, logging without secrets, loading/error/empty UI states, and accessible focus/keyboard behavior before layering feature flows on top.

## 3. Data model, access policy, and migrations

Model catalog facts separately from a user's overlay so refreshed public metadata can never erase personal data. Use a stable external key that includes provider and media type to avoid movie/TV collisions.

| Entity | Key fields and purpose |
| --- | --- |
| `catalog_shows` | Provider/media external ID, title, type, catalog snapshot, normalized filter fields, image URLs, provider-ID blob, details refresh timestamp, and schema version. Stores the persistent fields from the technical schema that are public rather than user-specific. |
| `user_shows` | `namespace_id`, `user_id`, catalog-show key, status, interest, score, Scoop, tags (or a companion relation), creation timestamp, and the five required per-field update timestamps. A row exists only while a show belongs to the collection. |
| `user_show_tags` | Normalized case-insensitive tag rows scoped to `namespace_id`, `user_id`, and show; supports tag-library/sidebar queries and preserves tag update semantics. |
| `user_settings` | Namespace/user-scoped username, AI model, catalog preference values that are appropriate to sync, and a version/update timestamp for conflict resolution. Do not persist user-entered secrets unless intentionally supported and encrypted server-side; benchmark credentials should come from environment. |
| `user_ui_preferences` | Namespace/user-scoped font size, search-on-launch, removal-confirmation suppression/count, and last selected filter. This can be server-persisted so it survives browser clearing. |
| `app_metadata` | Namespace-scoped schema/data version and migration bookkeeping needed to bring prior saved libraries forward safely. |

Implementation details:

1. Create SQL constraints/enums for media type, status (`active`, `next`, `later`, `done`, `quit`, `wait`), and interest (`interested`, `excited`). Permit `next` in data but do not present it as a normal UI choice. Enforce one overlay per `(namespace_id, user_id, catalog_show_id)` and unique normalized tag values per overlay.
2. Add indexes for namespace/user collection queries, status, score, media type, tag joins, public catalog lookup, and recent field updates. All user-owned foreign keys and composite lookups include the isolation dimensions.
3. Enable Row Level Security. Route normal application reads/writes through an identity-aware Supabase client/policy that restricts `(namespace_id, user_id)`; reserve service-role access for server-only migration/reset operations. Validate identity inputs rather than trusting a client-provided namespace.
4. Implement a versioned data-migration path from any legacy/snapshot shape: map public Show data into `catalog_shows`, split every `my*` property into `user_shows`/tags, preserve ISO dates, and retain AI Scoop. Make migrations idempotent, transactional where possible, and verify counts before/after; never discard a user overlay because a catalog refresh is incomplete.
5. Centralize a `mergeCatalogShowWithOverlay` domain function. Public values use first-non-empty-new-or-old behavior; each personal field uses its own latest timestamp; initial creation time never changes; details refresh time updates after a successful merge. Use it for catalog refreshes, re-encountered recommendations, and sync/import-facing operations.
6. Centralize collection mutations. Status saves a show; Interested/Excited translate to `later` plus the matching interest; rating/tagging an unsaved show creates an overlay with respectively `done` or `later + interested`; status changes away from Later leave interest stored but irrelevant; clearing confirmed status atomically deletes the overlay and all tags/Scoop.

## 4. Backend services and route contracts

Create typed domain services (catalog, collection, filters, settings, AI, export, identity) and keep route handlers thin: authenticate/resolve identity, validate input, call a service, return typed DTOs. All catalog data sent to the client is merged with the caller's overlay, so the same show always displays the user's version.

Planned server endpoints/actions:

- Collection and filters: list grouped/filterable library, list available tags/filters, get a merged show, upsert status/interest, score, tags, removal confirmation preference, and delete collection membership.
- Catalog: keyword search, detail/refresh by provider ID/media type, person detail/credits, and recommendation/streaming lookups. Persist eligible catalog snapshots during detail/search mapping, then merge with the overlay before returning.
- Settings: read/update readability, search-on-launch, username, permitted integration/model settings, scoped to the effective identity.
- AI: Ask (structured commentary plus mentioned-show list), Scoop streaming/generation, single/multi-show concepts, and concept recommendations. Require valid current-show/selected-input context server-side; never call AI directly from the browser with a secret key.
- Data portability: authenticated `GET`/action to stream a ZIP containing a JSON versioned backup of all saved shows, overlays, tags, settings relevant to the product, and ISO-8601 dates. Exclude raw API keys and transient Ask/Alchemy state.
- Test-only reset: production-gated endpoint/script using a validated namespace argument, deleting only that namespace's user/configuration/catalog test data in dependency order. Require explicit opt-in so it cannot become a general destructive endpoint.

For every mutation, return the authoritative merged show/list state (or invalidate/refetch a typed query key) so Home, Detail, Search, and AI recommendation tiles stay consistent without relying on local persistence.

## 5. Client architecture and reusable UI

Follow the required fractal organization and humble-component rule. TSX files compose accessible markup and bind hook outputs only; hooks own fetching, mutation orchestration, view state, and handlers; pure transforms and constants remain co-located. Use directory-named main components rather than `index.tsx`.

```text
src/
  app/                         # routes, layouts, route handlers
  config/                      # validated public config and product constants
  theme/                       # tokens, global styles, font-size mappings
  components/                  # shared primitives: Button, Dialog, Chip, Tile, Strand, etc.
  hooks/                       # global query/identity/accessibility hooks
  utils/                       # date, validation, filtering, formatting utilities
  server/
    identity/ catalog/ collection/ ai/ settings/ export/ repositories/
  pages/
    Home/features/LibraryGrid/
    Find/features/Search/, Ask/, Alchemy/
    ShowDetail/features/HeaderMedia/, MyRelationship/, Scoop/, ExploreSimilar/, ...
    PersonDetail/features/PersonAnalytics/, Filmography/
    Settings/features/AppPreferences/, AccountPreferences/, DataExport/
```

Build shared presentational primitives first: responsive app shell/sidebar and mobile navigation, mode switcher, poster tile with collection/rating badges, media strands, chips, segmented toggle, slider, dialogs, skeletons, error/retry blocks, empty states, and streamed-text display. Ensure all click/tap surfaces have labels, semantic controls, focus handling, and non-color-only state indicators.

## 6. Collection, navigation, and show-detail implementation

1. Implement the root shell with persistent Find/Discover and Settings entry points, filter/navigation panel, and main route area. Derive sidebar tag filters plus a `No tags` filter only when applicable; include All Shows, genre, decade, and community-score filtering. Keep any supported persisted selected filter stable across reloads.
2. Build Home as a query-driven filtered collection view. Layer the All/Movies/TV toggle on top of the selected filter and group results exactly as Active (prominent tiles), Excited (`later + excited`), Interested (`later + interested`), then collapsed Other (Wait, Quit, Done, and Later without interest). Supply distinct empty states for an empty library and a non-matching filter.
3. Build Find/Search with debounced, cancellable catalog title/keyword requests, a poster grid, collection badges, and navigation to merged Show Detail. Honor Search-on-Launch safely after settings resolve.
4. Build the Show Detail route as the single source of truth, refreshing/falling back gracefully when catalog data is partial. Preserve the specified narrative order: media header; core facts/community score; tags; overview/Scoop; Ask CTA; genres/languages; traditional recs; Explore Similar; providers; cast/crew; TV seasons; movie budget/revenue. Hide inapplicable/missing sections without breaking hierarchy.
5. Place status/interest chips in the detail toolbar, and use the centralized mutation service for all status, rating, and tag behavior. Reselecting an active status opens the warning confirmation; honor the suppression preference after repeated removals; a confirmed removal clears all My Data by deleting the overlay. Optimistically reflect safe mutations but reconcile from the server and show failure recovery.
6. Make the header cinematic but resilient: use inline trailer/media when available, then backdrop/logo/poster fallbacks. Show year/runtime or season/episode facts without assuming one media type.
7. Implement normal catalog recommendations as an immediately actionable strand. Map cast/crew to Person Detail and expose provider availability, seasons, and financial data only where catalog data supports them.

## 7. AI discovery behavior

### Shared AI foundation

Construct prompts on the server from a versioned shared persona template plus surface-specific instructions. Include a compact, sanitized taste profile from saved titles and My Data, relevant current show/selected concepts, and only needed session turns. Enforce TV/movie scope, spoiler safety by default, warm opinionated honesty, specific vibe/craft language, and no generic filler. Log provider/model/latency/error metadata without storing private prompt contents or API secrets.

Validate AI results with schemas. Recommendation results must contain title, provider external ID when available, and media type plus a concise reason; resolve each by external ID and case-insensitive title match. Return a selectable merged Show for successful resolutions; otherwise return a clearly non-interactive item with Search handoff. On parse failure, retry once with stricter structured instructions, then preserve commentary and provide the same Search fallback.

### Scoop and Ask

1. Implement Scoop generation on demand with progressive streaming states (`Generating…`, partial text, retry/error). Require the mini-review contract: personal take, honest stack-up, prominent emotional Scoop paragraph, fit/warnings, and verdict; target 150–350 words.
2. Check the Scoop timestamp before reuse. A Scoop under four hours old is cached; an expired Scoop regenerates only when requested. Persist it and its update timestamp only when the show has a collection overlay; otherwise retain it only in detail-page memory for that visit.
3. Implement Ask as session-only chat state. Start with six randomly selected, refreshable starter prompts; retain recent turns and replace older turns after roughly ten messages with a 1–2 sentence in-persona summary. Do not write chat history/mentioned strips to Supabase.
4. Require Ask-with-mentions output as `commentary` and a strictly parsed `Title::externalId::mediaType;;…` string. Render the commentary and deduplicated, resolved mentioned-show strip; each successful item opens Detail and unresolved entries hand off to Search.
5. Add Ask About This Show from Detail by handing its complete catalog/overlay context into a new Ask session and visibly indicating the subject; leave exact text prefill absent unless product direction later specifies it.

### Concepts, Explore Similar, and Alchemy

1. Create one reusable concept-selection feature. Concepts are bullet/chip candidates of one to three evocative, spoiler-free words; reject/generate again for generic placeholders and deduplicate near-identical phrases. Default to eight generated concepts, ordered by strength and varied across structure, vibe, emotional palette, relationship dynamics, craft, and genre-flavor.
2. For Explore Similar, request single-show concepts only after the user presses Get Concepts, require one or more selections, then request exactly five recommendations. Reasons explicitly name selected concepts. Clear recommendations when selections change.
3. For Alchemy, offer a selector that searches both the library and global catalog, requires at least two starting shows, then requests concepts shared by every selected input. Permit one to eight concept selections, require one before Alchemize, and return exactly six resolved recommendations with reasons. Backtracking/changing inputs clears concepts and results.
4. Implement More Alchemy as a session-only chaining control that seeds a new input-selection round from returned results. Clear all Alchemy session data on leaving/resetting the mode.

## 8. Person detail and settings

1. Build Person Detail using the catalog adapter: gallery, accessible biography, lightweight rating/genre/projects-by-year charts derived from filmography data, credits grouped by year, and Show Detail navigation from every credit. Provide useful missing-data fallbacks rather than empty chart chrome.
2. Implement Settings routes/features for font/readability size, Search on Launch, username, AI model selection, catalog configuration, and benchmark-safe key guidance. Sync only settings that are permitted by the selected configuration and scope all user data to the active identity.
3. Add Export My Data with progress/error feedback and a versioned ZIP/JSON schema. Include every saved show, overlay field/timestamp, tags, persisted Scoop, and appropriate preferences; serialize all dates in ISO-8601. Make no Import UI, because restore is explicitly desired but currently unimplemented.

## 9. Testing, verification, and release sequencing

Implement in vertical slices so every user-facing flow is backed by the durable model before adding refinements:

1. **Foundation:** app shell, configuration validation, Supabase migrations/RLS, identity/namespace resolution, repositories, fixtures, and reset script.
2. **Library core:** catalog adapter, merge function, collection mutations, Home filters/grouping, Search, and basic Detail with status/rating/tags.
3. **Detail depth:** media fallbacks, all conditional catalog sections, traditional recommendations, Person Detail, Settings, and ZIP export.
4. **AI surfaces:** shared prompting/validation/resolution layer, Scoop, Ask/mentions/session summarization, Concepts/Explore Similar, then Alchemy/chaining.
5. **Hardening:** responsiveness/accessibility, migration verification, failure/retry states, observability, docs, and production build review.

Test at the following levels:

- Unit-test collection defaults/removal, status-interest translations, filter/grouping logic, tag normalization, timestamp conflict resolution, first-non-empty catalog merge behavior, recommendation parser/resolver, concept selection limits, four-hour Scoop freshness, chat summarization threshold, and export serialization.
- Repository/route integration-test RLS/identity enforcement, namespace isolation, user isolation within one namespace, server-authoritative recovery after cleared client storage, catalog refresh preservation, migrations, settings, scoped destructive reset, and secret non-exposure.
- Browser-test the ten named journeys: build collection; rating-to-save; tag-to-save; maintenance; tag filters; Ask-to-save; Explore Similar-to-save; full Alchemy/chaining; person-credit navigation; and ZIP backup. Also cover empty/error/missing-media states and removal-confirmation suppression.
- Add AI fixture/contract tests plus a golden-set harness scored on the supplied rubric: Voice >= 1, Taste Alignment >= 1, Real-Show Integrity = 2, total >= 7/10. Mock the AI/catalog for deterministic CI; run opt-in provider smoke tests only when credentials are present.
- Final verification: run migrations on a fresh hosted-compatible Supabase project, execute `test:reset` against a disposable namespace while proving another namespace remains intact, clear browser storage and reload, run lint/type checks/tests/production build, and manually validate keyboard/screen-reader basics and mobile/desktop layouts.

## 10. Acceptance checklist

The build is complete only when it satisfies these non-negotiable outcomes:

- User overlays always win visually and survive catalog refreshes, updates, browser data clearing, and versioned migrations.
- Every user-owned record is isolated by `(namespace_id, user_id)`; reset never affects other namespaces.
- All auto-save defaults, removal clearing/confirmation, interest semantics, filtering/grouping, and tile badges match the PRD.
- Every discovery recommendation is either a resolved selectable real show with an on-brand reason or an explicit Search handoff—never a misleading interactive hallucination.
- Scoop cache/persistence and Ask/Alchemy session-only lifetimes match the specified rules.
- Detail, Person, Settings, and export provide all required sections/actions with graceful missing-data and network-error handling.
- Configuration, migrations, test/reset scripts, and hosted-Supabase documentation allow a cloud agent to run the app without Docker or source edits.
