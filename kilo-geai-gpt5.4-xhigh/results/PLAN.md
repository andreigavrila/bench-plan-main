# Implementation Plan

## 1. Objective

Build a personal TV and movie companion in benchmark mode that lets users collect, organize, rate, and discover entertainment through traditional search, conversational AI, concept-based exploration, and multi-show Alchemy. The implementation must preserve the product's taste-aware behavior, user-data precedence rules, AI voice, and backend-backed durability while satisfying benchmark execution constraints around `namespace_id`, `user_id`, Supabase persistence, Next.js runtime, and repeatable destructive testing.

## 2. Planning Principles

- Implement the benchmark baseline with Next.js as the app and server boundary and Supabase as the persistence layer.
- Treat the backend as the source of truth; client caches are disposable.
- Partition every persisted record by `namespace_id` and `user_id`.
- Preserve user-owned fields across catalog refreshes and sync merges using per-field timestamps.
- Keep the UI faithful to the product's emotional design: direct collection management, strong discovery affordances, spoiler-safe AI, and actionable recommendations.
- Favor a feature-fractal structure from `INSTRUCTIONS.md`: route/page-level containers, feature directories, humble TSX components, logic in hooks/services, theme-token styling, and adjacent tests for critical logic.

## 3. Proposed Architecture

## 3.1 Application Shape

- Next.js App Router for route composition, server actions/API routes, and a clean UI/server boundary.
- Supabase for persisted entities, settings, migrations, and namespace-scoped test reset.
- Server-side integration layer for external catalog and AI providers so secrets stay off the client.
- React client for interactive collection management, chat, Alchemy workflows, detail actions, and optimistic updates backed by server confirmation.

## 3.2 Major Layers

1. Presentation layer
- Routes for Home, Find/Discover, Show Detail, Person Detail, Settings.
- Shared UI primitives for chips, tiles, strands, dialogs, forms, chat, and charts.

2. Feature layer
- Collection home and filters.
- Search.
- Ask chat.
- Alchemy.
- Detail page with My Data controls, Scoop, Explore Similar, and supporting metadata strands.
- Person detail.
- Settings and export.

3. Domain layer
- Show merge logic.
- Collection save/remove semantics.
- Filter generation and grouping.
- AI request assembly and response validation.
- Recommendation-to-real-show resolution.
- Export serialization.

4. Data/integration layer
- Supabase repositories.
- External catalog adapters.
- AI provider adapters.
- Namespace/user identity context resolver.

## 3.3 Suggested Directory Structure

```text
src/
  app/
    (app shell routes and server endpoints)
  config/
    env.ts
    constants.ts
  theme/
    tokens.ts
    typography.ts
  components/
    ui primitives
  hooks/
    app-wide hooks
  utils/
    shared pure helpers
  server/
    auth/
    namespace/
    supabase/
    catalog/
    ai/
    export/
  pages/
    Home/
      Home.tsx
      features/
        FilterSidebar/
        CollectionGroups/
    Find/
      Find.tsx
      features/
        ModeSwitcher/
        Search/
        Ask/
        Alchemy/
    ShowDetail/
      ShowDetail.tsx
      features/
        HeaderMedia/
        RatingControl/
        StatusToolbar/
        TagsControl/
        Scoop/
        ExploreSimilar/
        Recommendations/
        Providers/
        CastCrew/
        Seasons/
        Financials/
    PersonDetail/
      PersonDetail.tsx
      features/
        Gallery/
        Analytics/
        Filmography/
    Settings/
      Settings.tsx
      features/
        Preferences/
        Credentials/
        ExportData/
```

## 4. Data Model Plan

## 4.1 Core Persistence Strategy

Model the product around a canonical saved-show record plus synced settings and app metadata. Persist only durable user and catalog fields; keep large, re-fetchable data such as credits, videos, recommendations, similar titles, and image galleries transient.

## 4.2 Primary Entities

1. `saved_shows`
- Composite uniqueness on `(namespace_id, user_id, show_id)`.
- Fields covering the conceptual `Show` record from `storage-schema.md`.
- Separate columns for all `my*` and AI Scoop timestamps.
- Catalog metadata and provider data snapshot for fast rendering.
- `is_test` flag for fixtures and destructive test setup.

2. `cloud_settings`
- One row per `(namespace_id, user_id)`.
- Username, synced API keys if allowed, AI model, catalog provider key, version timestamp.
- Keep any elevated credentials server-only and never persist service-role secrets.

3. `app_metadata`
- Per namespace or per user metadata for schema/data model version tracking.

4. `user_preferences`
- Search on launch, font size, and other local-or-sync policy choices.
- If some preferences remain client-local by design, ensure they do not affect correctness.

5. `ui_state`
- Last selected filter, status removal confirmation suppression, confirmation count.
- Can be local or persisted; if persisted, still scope by namespace and user.

## 4.3 Supporting Persistence Decisions

- Represent `providerData` as JSONB.
- Store all dates as ISO-8601-compatible timestamptz.
- Persist `external_ids` as JSONB to support deterministic recommendation resolution.
- Preserve nullable `myInterest` even when status leaves `Later`, so restoring `Later` can revive prior interest.

## 4.4 Merge and Conflict Rules

Implement a dedicated merge service with these rules:

- Non-user fields use first-non-empty semantics, never replacing meaningful stored values with empty values.
- `myStatus`, `myInterest`, `myTags`, `myScore`, `aiScoop` resolve field-by-field by latest update timestamp.
- `detailsUpdateDate` refreshes after catalog merges.
- `creationDate` is immutable after first save.
- Duplicate records within a namespace/user pair are merged transparently.

## 4.5 Removal Semantics

- Clearing status removes the saved show record entirely.
- Removal also clears status, interest, tags, rating, and AI Scoop.
- If product history preservation is desired later, implement it as an audit layer, not by violating current delete semantics.

## 4.6 Export Semantics

- Export generates a `.zip` containing a JSON payload of all durable user data for the active namespace/user.
- Dates serialized as ISO-8601.
- Export format should include enough metadata to support a future import/restore feature.

## 5. Database and Supabase Plan

## 5.1 Schema Deliverables

- SQL migrations creating all tables, indexes, constraints, and row-level security policies.
- Seed or fixture scripts for optional benchmark/dev bootstrap.
- Deterministic reset path scoped to `namespace_id`.

## 5.2 Required Tables and Indexing

- `saved_shows`: indexes on `(namespace_id, user_id)`, status, interest, tag arrays/JSON, media type, updated timestamps.
- `cloud_settings`: unique `(namespace_id, user_id)`.
- `user_preferences`: unique `(namespace_id, user_id)`.
- `app_metadata`: unique scope key.

Optional normalized tables if needed for performance/clarity:

- `show_tags` for indexed tag filtering if array queries are insufficient.
- `test_runs` or equivalent if benchmark tooling needs explicit run bookkeeping.

## 5.3 Security and Access

- Use Supabase anon/public key on the client only where safe.
- Keep privileged operations, export generation, AI provider calls, and reset operations on the server.
- Enforce namespace and user scoping in queries and policies.
- Gate any dev identity injection and destructive endpoints to non-production environments.

## 6. Identity and Isolation Plan

## 6.1 Namespace Resolution

- Resolve a stable `namespace_id` for the lifetime of a build from environment/config.
- Expose it to server-side repository code, not as mutable user input.
- All persisted reads, writes, exports, and resets require `namespace_id`.

## 6.2 User Identity Resolution

- Resolve `user_id` via benchmark-friendly identity injection.
- Support one default user initially, but design storage and APIs for multiple users within a namespace.
- Treat `user_id` as opaque and stable.

## 6.3 Dev/Test Identity Injection

Accept one benchmark-mode mechanism, documented and production-gated:

- Header-based `X-User-Id` on server routes, or
- Dev-only user selector, or
- Configured default user.

Implementation requirements:

- No schema redesign needed later for OAuth.
- Production build disables or gates the dev-only path.
- Server establishes trusted identity context before data access.

## 6.4 Destructive Test Reset

- Provide a server-backed script/endpoint that deletes test data only for the active namespace.
- Never require global teardown.
- Ensure fixture creation and cleanup can run repeatedly in hosted Supabase.

## 7. External Catalog Integration Plan

## 7.1 Responsibilities

- Search movies and TV shows by text.
- Fetch show details, credits, images, videos, seasons, recommendations, similar titles, and provider availability.
- Fetch person details and filmography.
- Resolve AI-recommended shows to canonical catalog items using external IDs first, then title matching fallback rules.

## 7.2 Mapping Layer

Build a catalog adapter that:

- Converts provider payloads into canonical app shapes.
- Maps genre IDs to display names.
- Normalizes date formats.
- Selects a deterministic best logo.
- Stores provider IDs by country.
- Leaves transient-only fields out of persistence.

## 7.3 Refresh Strategy

- Search and detail fetches return the latest catalog data.
- When a saved item is encountered, merge refreshed catalog data with stored user data.
- Use server-side fetch wrappers with cache control appropriate to freshness and rate limits.

## 8. AI Platform Plan

## 8.1 AI Surfaces to Implement

1. Ask chat.
2. Ask with mentions structured output.
3. Scoop generation.
4. Single-show concept generation.
5. Multi-show concept generation for Alchemy.
6. Concept-based recommendations for Explore Similar and Alchemy.

## 8.2 Shared AI Contracts

- Domain restricted to TV and movies.
- Spoiler-safe by default.
- Warm, playful, opinionated, honest persona.
- Specific vibe/craft reasoning over generic genre language.
- Recommendations should resolve to real catalog items whenever possible.

## 8.3 Context Assembly

Create an AI context builder that can compose:

- user library summary,
- selected saved shows with My Data,
- current show context,
- selected concepts,
- recent conversation turns,
- summarized older chat turns in the same voice.

The builder must cap payload size predictably and preserve the feel of continuity.

## 8.4 Ask Chat Design

- Session-scoped conversation history, not persisted long-term.
- After roughly 10 messages, summarize older turns into 1-2 sentences while preserving persona.
- AI response includes user-facing commentary plus a machine-readable `showList` string in the exact `Title::externalId::mediaType;;...` format when structured mentions are required.
- Parser retries once on formatting failure, then falls back to commentary plus Search handoff.

## 8.5 Scoop Design

- On-demand generation from the detail page.
- Progressive streaming if supported.
- Cache freshness target of 4 hours.
- Persist only for saved shows; keep ephemeral for unsaved shows.
- Output structure should cover personal take, stack-up, centerpiece Scoop paragraph, fit/warnings, and a verdict.

## 8.6 Concepts Design

- Default generation target: 8 concepts.
- Output is bullet-list-only, 1-3 words each, spoiler-free, evocative, and diverse across structure/vibe/emotion/craft.
- Multi-show concepts must be shared across all inputs.
- Order strongest concepts first.

## 8.7 Recommendation Design

- Explore Similar returns 5 recommendations.
- Alchemy returns 6 recommendations.
- Each recommendation reason explicitly cites matching selected concepts.
- Bias somewhat toward recent titles without excluding classics or hidden gems.
- Validate recommendation integrity against the real catalog before rendering as selectable items.

## 8.8 AI Provider Abstraction

- Encapsulate prompt templates, provider API calls, parsing, retries, and telemetry behind service interfaces.
- Allow settings-driven model selection.
- Keep provider-specific details isolated so benchmark changes do not force UI rewrites.

## 9. Feature Implementation Plan

## 9.1 App Shell and Navigation

- Build the main shell with persistent navigation to Home, Find/Discover, and Settings.
- Include a filter/navigation panel for collection-focused browsing.
- Maintain clear route transitions between Home, Detail, Person, Find, and Settings.

## 9.2 Collection Home

Implement the main library view with:

- grouped status sections in this order: Active, Excited, Interested, Other statuses,
- prominent larger tiles for Active,
- media-type toggle for All / Movies / TV,
- empty state for no collection,
- empty state for filter misses,
- tile badges for in-collection and rating indicators.

Sorting and grouping considerations:

- recently updated items first where appropriate,
- consistent placement of items with hidden or missing interest values,
- user-overlay data visible wherever a saved show appears.

## 9.3 Filters and Sidebar

Implement filter generation for:

- All Shows,
- one filter per tag,
- No Tags when applicable,
- genre,
- decade,
- community score ranges,
- media-type toggle applied on top.

Persist last selected filter according to product expectations.

## 9.4 Search

- Text input with live or debounced search.
- Poster-grid results from external catalog.
- In-collection badges on already-saved items.
- Selecting a result opens Show Detail with merged user overlay if saved.
- Honor Search-on-launch preference.

## 9.5 Show Detail

Implement the detail page as the product's single source of truth, preserving the intended section hierarchy:

1. Header media carousel with trailers/backdrops/posters/logos.
2. Core facts and community score.
3. Personal relationship controls: status, interest, rating, tags.
4. Overview and Scoop.
5. Ask About This Show CTA.
6. Genres and languages.
7. Traditional recommendations strand.
8. Explore Similar.
9. Streaming availability.
10. Cast and Crew strands.
11. Seasons for TV.
12. Budget vs revenue for movies.

Critical business behavior on this page:

- status chips include Active, Interested, Excited, Done, Quit, Wait,
- Interested and Excited map to `Later` plus `myInterest`,
- reselecting the active status prompts for removal confirmation,
- rating an unsaved show auto-saves it as `Done`,
- adding a tag to an unsaved show auto-saves it as `Later + Interested`,
- Scoop toggles among empty, cached, and open states,
- Ask About This Show seeds Ask with show context,
- Explore Similar clears downstream results when concept selections change.

## 9.6 Ask

- Chat UI with user and assistant turns.
- Welcome state with 6 random starter prompts and refresh action.
- Mentioned-shows horizontal strip driven by structured AI output.
- Mapping failures fall back to non-interactive rendering or Search handoff.
- Session reset/leave clears conversation and mentioned shows.

## 9.7 Alchemy

Implement the multi-step blending flow:

1. Select 2 or more starting shows from library and/or catalog.
2. Generate shared concepts.
3. Let user select up to 8 concepts.
4. Produce 6 recommendations with concise concept-grounded reasons.
5. Support chaining with More Alchemy.

UX rules:

- clear step framing,
- backtracking allowed,
- changing selected shows clears concepts and results,
- changing concepts clears results.

## 9.8 Explore Similar

- From Show Detail, fetch 8 concepts for the current show.
- Render concepts as selectable chips.
- Require at least one concept to continue.
- Generate 5 recommendations with explicit concept reasoning.

## 9.9 Person Detail

- Person hero and gallery.
- Bio.
- Filmography grouped by year.
- Lightweight analytics charts covering average project ratings, top genres, and projects by year.
- Credit selection opens Show Detail.

## 9.10 Settings and Your Data

Implement settings sections for:

- font size/readability,
- Search on launch,
- username,
- AI provider API key handling,
- AI model selection,
- content catalog provider API key,
- export my data.

Rules:

- benchmark mode may receive keys via env,
- user-entered secrets must never be committed,
- synced settings, if supported, still obey namespace/user scoping.

## 10. Business Rules Implementation Checklist

- Any status assignment saves to collection.
- Interest chip selection saves as `Later` with matching interest.
- Rating unsaved show saves as `Done`.
- Tagging unsaved show saves as `Later + Interested`.
- Saving without explicit status defaults to `Later + Interested` except rating-driven `Done`.
- Clearing status removes the record and all My Data after confirmation.
- User overlay always supersedes refreshed public data in UI.
- Tile badges reflect collection membership and rating.
- AI Scoop persistence depends on collection membership.
- AI recs resolve to real shows via external ID plus case-insensitive title verification.
- Cloud conflicts resolve per field by latest timestamp.
- Libraries survive app version changes through safe data migration.

## 11. API and Server Endpoint Plan

Define server endpoints or actions for:

- identity/bootstrap context,
- collection list retrieval with filters,
- show save/update/remove operations,
- tag update operations,
- rating update operations,
- settings read/update,
- export generation,
- search proxying,
- show detail/person detail fetches,
- Ask chat,
- concepts generation,
- Explore Similar recommendations,
- Alchemy recommendations,
- namespace-scoped test reset.

Endpoint design requirements:

- server validates `namespace_id` and `user_id`,
- consistent error envelopes for UI handling,
- support optimistic UI where safe,
- no secret exposure to the client.

## 12. UI/UX and Design System Plan

## 12.1 Visual and Interaction Priorities

- Emphasize a cinematic, taste-driven experience over utilitarian CRUD.
- Keep primary actions near the top of high-value screens.
- Preserve directness: no unnecessary modals except destructive confirmation.
- Use theme tokens only, no inline magic values in TSX.

## 12.2 Shared Components

- show tiles,
- chip controls,
- filter sidebar,
- horizontal media strands,
- score bars/sliders,
- dialog/confirmation components,
- chat transcript and composer,
- concept chips,
- charts,
- empty states and error states.

## 12.3 Accessibility and Responsiveness

- Responsive layout for sidebar/navigation and content panes.
- Keyboard navigation for chips, dialogs, carousels, and chat controls.
- Visible states for selected concepts/statuses.
- Font-size setting integrated with the theme.
- Semantic headings and alt text for image-heavy surfaces.

## 13. State Management and Caching Plan

- Use server data fetching for canonical reads.
- Use client state for transient workflows: selected concepts, chat transcript, mentioned shows, Alchemy inputs/results.
- Use optimistic updates for status, tags, and ratings, with rollback on failure.
- Keep client caches disposable and rehydratable from backend data.
- Store ephemeral AI session data in memory or short-lived client state, not long-term persistence.

## 14. Migration and Continuity Plan

- Create explicit migration scripts for schema evolution.
- Store data model version metadata.
- On startup or deploy, run safe forward migrations.
- Add migration tests that prove legacy saved libraries can be upgraded without losing tags, statuses, interest, ratings, or Scoop.

## 15. Testing and Quality Plan

## 15.1 Unit Tests

Cover critical pure/domain logic:

- save defaults and implicit save triggers,
- removal semantics,
- merge conflict resolution by timestamp,
- filter generation and grouping,
- recommendation mapping and validation,
- concept selection and downstream invalidation,
- export serialization,
- AI structured output parsing and retry/fallback.

## 15.2 Integration Tests

- repository operations against a test Supabase instance,
- namespace/user isolation,
- reset script behavior,
- detail-page save/update flows,
- settings persistence,
- export endpoint behavior.

## 15.3 End-to-End Tests

Cover key journeys from the PRD:

- build collection,
- rate-to-save,
- tag-to-save,
- maintain collection,
- tag-driven organization,
- Ask discovery to save,
- Explore Similar to save,
- Alchemy chain,
- talent deep-dive,
- backup export.

These tests must run without global teardown and operate in a dedicated namespace.

## 15.4 AI Quality Validation

Create regression checks aligned to `discovery_quality_bar.md`:

- voice adherence,
- taste alignment,
- surprise without betrayal,
- specificity of reasoning,
- real-show integrity.

Minimum validations:

- Scoop has the expected section balance,
- Ask answers directly and uses lists when helpful,
- concepts generate 8 evocative 1-3 word bullets,
- Explore Similar returns 5 recs and Alchemy 6,
- every rec maps to a real catalog item.

## 15.5 Manual QA Matrix

- movie vs TV detail differences,
- saved vs unsaved show behavior,
- no-trailer/no-backdrop fallbacks,
- no-tag and no-results states,
- cache-cleared client still restoring backend truth,
- dev identity injection off in production mode.

## 16. Benchmark Deliverables Plan

The repo implementation should include:

- `.env.example` with all required environment variables and comments,
- `.gitignore` excluding `.env*` except `.env.example`,
- scripts for app start, tests, and namespace reset,
- migrations and any repeatable fixtures,
- documentation for benchmark identity injection and namespace isolation.

Expected environment variables likely include:

- Next.js public Supabase URL,
- Supabase anon key,
- server-only Supabase/service credentials if required,
- external catalog API key,
- AI provider API key,
- default AI model,
- benchmark `namespace_id`,
- default `user_id` or dev identity mode flags.

## 17. Delivery Phases

## Phase 1: Foundation

- Initialize Next.js app structure and theme/config foundations.
- Set up env parsing, Supabase clients, migrations, and identity/namespace context.
- Implement core repositories and domain models.

## Phase 2: Collection Backbone

- Build collection list retrieval, save/update/remove flows, tags, rating, status logic, and filters.
- Implement Home and basic Show Detail without AI features.

## Phase 3: Catalog and Discovery Basics

- Implement external search, detail enrichment, traditional recommendations, providers, cast/crew, and person detail.

## Phase 4: AI Surfaces

- Implement Ask, Scoop, concepts, Explore Similar, and Alchemy.
- Add structured parsing, retries, and recommendation resolution.

## Phase 5: Settings, Export, and Hardening

- Implement settings, export, migrations for continuity, namespace reset flow, and benchmark docs.
- Add comprehensive automated tests and AI quality checks.

## 18. Risks and Mitigations

1. AI outputs drift off-brand or unstructured.
- Mitigation: strict output contracts, parser validation, retry logic, golden prompt tests, human QA against the discovery quality bar.

2. Recommendation mapping fails or hallucinates.
- Mitigation: require external IDs where possible, validate title/media-type matches, provide Search fallback.

3. Timestamp-based merge bugs overwrite user data.
- Mitigation: central merge service with focused unit tests and fixture-based integration tests.

4. Namespace leakage in tests or production usage.
- Mitigation: namespace-scoped repositories, RLS or server-side guards, dedicated reset tests.

5. Overly complex detail page becomes cluttered.
- Mitigation: preserve narrative hierarchy, cluster primary actions early, relegate optional depth lower on the page.

6. Secret handling becomes unsafe.
- Mitigation: server-only credential boundaries, `.env.example`, no committed secrets, client use limited to public keys.

## 19. Open Product Decisions To Preserve As Explicit TODOs

- Whether `Next` becomes a first-class surfaced status.
- Whether custom named lists should extend beyond tags.
- Whether generating Scoop for an unsaved show should implicitly save it.
- Whether clearing rating should create an explicit unrated state.
- Whether import/restore should be implemented now or deferred.
- Whether Alchemy sessions should become saveable/shareable.
- Whether explicit my-status filters should be added to the sidebar.

## 20. Definition of Done

The implementation is complete when:

- all core collection, detail, discovery, person, settings, and export journeys are functional,
- every persisted user-owned record is scoped by `namespace_id` and `user_id`,
- backend persistence remains correct after client cache clearing,
- destructive test reset works within a namespace without global teardown,
- AI surfaces meet the specified voice and structure contracts,
- user-overlay precedence and merge rules are enforced everywhere,
- benchmark repo deliverables and scripts are present,
- automated tests cover critical logic and primary journeys.
