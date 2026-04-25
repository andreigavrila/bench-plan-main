# Implementation Plan

## 1. Planning Basis

This plan covers the product described by:

- `docs/prd/product_prd.md`
- `docs/prd/infra_rider_prd.md`
- all supporting documents under `docs/prd/supporting_docs/`, including the technical storage schema

The build target is a planning-only benchmark implementation of a personal TV/movie companion with collection management, catalog discovery, taste-aware AI discovery, concept blending, person detail exploration, settings, export, and benchmark-safe persistence.

The implementation must use:

- Next.js as the application runtime and server boundary.
- Supabase as the persistence layer through official client libraries.
- Environment-variable configuration with no committed secrets.
- Server-side persisted user data as the source of truth.
- Explicit `(namespace_id, user_id)` ownership on every user-owned record.

## 2. Product Interpretation

The app has two equally important halves:

1. A durable personal entertainment library.
2. Discovery experiences that use that library as taste context.

The central invariant is that every show shown anywhere should be enriched with the user's saved overlay when it exists. Public catalog data can refresh over time, but user-owned fields win according to timestamp-based merge rules.

The primary object is a `Show`, representing a movie or TV series with:

- catalog metadata such as title, media type, dates, overview, images, genres, runtime, ratings, providers, cast, crew, seasons, recommendations, and similar items;
- user metadata such as status, interest, tags, rating, and timestamps;
- optional AI metadata, currently AI Scoop, with a four-hour freshness rule and persistence only for saved shows.

The user's collection is defined by shows with a non-null `my_status`. Setting status, interest, rating, or tags can implicitly save a show. Clearing status removes the show from the collection and clears all My Data after confirmation.

## 3. Technology and Project Setup

### 3.1 Application Stack

Use a single Next.js application with:

- App Router for pages and layouts.
- React Server Components where useful for initial data fetches.
- Server Actions or Route Handlers for all mutations and API-key-protected integrations.
- Supabase JavaScript client for database access.
- A component library strategy based on local UI primitives and design tokens rather than ad hoc inline styles.
- TypeScript in strict mode.
- Unit tests for business logic and integration tests for server routes/actions.
- Browser-level tests for core journeys where feasible.

### 3.2 Required Repo Deliverables

Add or maintain:

- `.env.example`
  - `NEXT_PUBLIC_SUPABASE_URL`
  - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
  - server-only Supabase key only if needed for migrations/test reset
  - `APP_NAMESPACE_ID`
  - `DEFAULT_USER_ID`
  - `CATALOG_API_KEY`
  - `AI_API_KEY`
  - `AI_MODEL`
  - catalog image base URL / provider config if required by the selected catalog API
- `.gitignore`
  - exclude `.env*` except `.env.example`
- package scripts:
  - `dev`
  - `build`
  - `test`
  - `test:reset`
  - `lint`
  - optional `db:migrate` / `db:seed`
- Supabase migration files for deterministic schema setup.
- README setup notes documenting hosted Supabase configuration, namespace isolation, and development identity injection.

### 3.3 Development Identity

Implement a benchmark-friendly identity adapter:

- In development/test, resolve `user_id` from a dev-only selector, header, or `DEFAULT_USER_ID`.
- Resolve `namespace_id` from `APP_NAMESPACE_ID`, with a generated fallback only for local development.
- Keep auth resolution behind a small server-side interface so future OAuth can replace it without schema changes.
- Never put identity trust decisions in browser-only code.

## 4. Architecture

### 4.1 Directory Structure

Follow the fractal architecture guidance:

```text
src/
  app/
    page.tsx
    find/
    show/[mediaType]/[id]/
    person/[id]/
    settings/
  config/
  theme/
  components/
  hooks/
  utils/
  server/
    auth/
    supabase/
    catalog/
    ai/
    collection/
    export/
  pages/
    Home/
      Home.tsx
      features/
    Find/
      Find.tsx
      features/
    ShowDetail/
      ShowDetail.tsx
      features/
    PersonDetail/
      PersonDetail.tsx
      features/
    Settings/
      Settings.tsx
      features/
```

Use `app/` for Next.js routing and thin route composition. Put page-level UI and hooks under `src/pages/...` so each screen can contain its own features, hooks, utilities, and tests. Avoid `index.tsx`; main files should match directory names.

### 4.2 Layering

Use these boundaries:

- UI components: render only markup and bind handlers.
- Feature hooks: orchestrate client state for that feature.
- Server actions/routes: validate input, resolve identity, call services, return typed results.
- Domain services: implement collection rules, merge behavior, AI contracts, catalog mapping, and export.
- Repository layer: Supabase reads/writes scoped by `(namespace_id, user_id)`.

Critical shared services:

- `identityService`: resolves namespace and user.
- `showRepository`: persisted show records and merge operations.
- `settingsRepository`: synced settings and local preference support.
- `catalogService`: external search/details/person/provider calls.
- `showMergeService`: public catalog refresh plus My Data timestamp merge.
- `collectionService`: save/remove/default status business rules.
- `aiService`: provider abstraction, prompt construction, structured parsing, retries.
- `recommendationResolver`: maps AI outputs to real catalog shows.
- `exportService`: zip backup creation.
- `testDataService`: namespace-scoped reset.

## 5. Persistence Plan

### 5.1 Supabase Tables

Create migrations for:

#### `shows`

Stores saved collection items and durable user overlays.

Key columns:

- `namespace_id text not null`
- `user_id text not null`
- `show_id text not null`
- `title text not null`
- `show_type text not null check (...)`
- `external_ids jsonb`
- catalog metadata columns matching the technical reference where practical
- `genres text[] not null default '{}'`
- `spoken_languages text[] not null default '{}'`
- `languages text[] not null default '{}'`
- `network_logos text[] not null default '{}'`
- `episode_run_time integer[] not null default '{}'`
- `provider_data jsonb`
- `my_tags text[] not null default '{}'`
- `my_tags_update_date timestamptz`
- `my_score numeric`
- `my_score_update_date timestamptz`
- `my_status text check (...)`
- `my_status_update_date timestamptz`
- `my_interest text check (...)`
- `my_interest_update_date timestamptz`
- `ai_scoop text`
- `ai_scoop_update_date timestamptz`
- `details_update_date timestamptz`
- `creation_date timestamptz not null default now()`
- `is_test boolean not null default false`

Constraints:

- primary key `(namespace_id, user_id, show_id)`
- indexes on `(namespace_id, user_id)`, status, tags, genre, dates, media type, score, and `is_test`

#### `cloud_settings`

Stores synced user settings.

- primary key `(namespace_id, user_id, id)`
- `id text not null default 'globalSettings'`
- `user_name text not null`
- `version numeric not null`
- `catalog_api_key text`
- `ai_api_key text`
- `ai_model text not null`

If API keys are stored at all, keep them server-readable only and consider encryption before production. For benchmark mode, prefer environment-provided keys.

#### `app_metadata`

Tracks migration/model version.

- `namespace_id text not null`
- `user_id text not null`
- `data_model_version integer not null default 3`

#### Optional `user_preferences`

Because browser local storage is disposable, store user preferences that matter across devices:

- `auto_search boolean`
- `font_size text`
- `hide_status_removal_confirmation boolean`
- `status_removal_count integer`
- `last_selected_filter jsonb`

Local storage may mirror these for responsiveness but must not be the only durable copy for user-owned data.

### 5.2 Row-Level Security and Scoping

Use RLS policies if direct browser Supabase access is used. Because benchmark identity may not use real Supabase Auth, prefer server-side data access for user-owned records initially.

All repository methods must require an identity context:

```ts
{
  namespaceId: string;
  userId: string;
}
```

No repository method should read or write user-owned data without both fields.

### 5.3 Merge Rules

Implement a deterministic merge service:

- Catalog/public fields use first non-empty new value, then old value.
- Empty strings, empty arrays, and null values never wipe non-empty stored public data.
- My Data fields resolve independently by update timestamp.
- AI Scoop resolves by `ai_scoop_update_date`.
- `details_update_date` updates on successful catalog refresh.
- `creation_date` is set only on initial insert.

Add unit tests covering:

- catalog refresh preserving user tags/status/rating;
- newer user field replacing older field;
- older user field not replacing newer field;
- empty catalog values not erasing stored values;
- re-adding a show preserving prior user overlay when present.

### 5.4 Data Removal

Clearing status removes the show row for that `(namespace_id, user_id, show_id)`, which clears status, interest, tags, rating, and AI Scoop together. If future requirements need tombstones or sync conflict handling, add a deleted marker, but the initial product behavior can use deletion.

## 6. External Catalog Integration

### 6.1 Catalog Abstraction

Create a catalog provider interface independent of vendor details:

- `searchShows(query, mediaType?)`
- `getShowDetails(mediaType, id)`
- `getShowCredits(mediaType, id)`
- `getShowImages(mediaType, id)`
- `getShowVideos(mediaType, id)`
- `getShowRecommendations(mediaType, id)`
- `getShowSimilar(mediaType, id)`
- `getWatchProviders(mediaType, id, region)`
- `getPersonDetails(personId)`
- `getPersonCredits(personId)`
- `resolveShow({ title, externalId, mediaType })`

Keep vendor IDs in `external_ids` and normalize all catalog responses into the app's `Show` shape.

### 6.2 Mapping Rules

Implement mappers for:

- movie vs TV title fields;
- media type inference and rejection of unknown/person where a show is required;
- date parsing with tolerant accepted formats;
- genre ID to display-name conversion;
- image path to renderable URL;
- best logo selection;
- provider data storing provider IDs by country;
- transient details such as cast, crew, seasons, videos, images, recommendations, and similar results.

Every catalog show rendered in UI should pass through an overlay step:

1. Fetch public catalog result.
2. Check saved show by `(namespace_id, user_id, show_id)`.
3. Merge/overlay My Data if present.
4. Return a display model with `inCollection` and `hasMyRating` indicators.

## 7. AI System Plan

### 7.1 Provider Abstraction

Create an AI provider interface:

- `generateScoop(show, libraryContext)`
- `askChat(messages, libraryContext, optionalShowContext)`
- `askWithMentions(messages, libraryContext, optionalShowContext)`
- `generateConcepts(shows, mode)`
- `generateConceptRecommendations(inputShows, concepts, count, libraryContext, mode)`
- `summarizeConversation(turns)`

Provider details, model choice, and API keys come from server-side configuration or synced settings. Browser code never receives raw AI keys.

### 7.2 Shared AI Guardrails

All prompts and response handlers enforce:

- TV/movie domain only.
- Spoiler-safe by default.
- warm, playful, opinionated, honest persona.
- specific vibe/structure/craft reasoning.
- no generic recommendation filler.
- real-show integrity for actionable recs.

### 7.3 Ask

Implement a chat state model that is session-only:

- user and assistant turns kept in client/session state;
- after roughly 10 messages, summarize older turns into one or two persona-preserving sentences;
- no persistent chat history;
- mentioned shows derived from current chat context.

Structured Ask output:

- `commentary`: user-facing response, no IDs shown.
- `showList`: `Title::externalId::mediaType;;...`

Parser behavior:

- parse exact delimiter format;
- resolve each show through catalog lookup;
- mark resolved shows interactive;
- unresolved shows remain non-interactive or open Search;
- retry once with stricter formatting if parsing fails.

### 7.4 Scoop

Scoop behavior:

- generated from Show Detail on demand;
- streamed if practical, otherwise show progressive loading state;
- about 150-350 words;
- includes personal take, honest stack-up, centerpiece Scoop paragraph, fit/warnings, and verdict;
- spoiler-safe unless explicitly requested;
- cached for four hours;
- persisted only if show is already in collection;
- if generated for an unsaved show, keep ephemeral unless the user later saves during that detail session.

### 7.5 Concepts

Concept generation:

- return bullet list only;
- 1-3 words per concept;
- evocative, spoiler-free, non-generic;
- ordered strongest first;
- varied across structure, tone, emotion, relationship dynamics, and craft;
- for multi-show Alchemy, concepts must be shared by all selected inputs.

Use 8 concepts by default for validation parity. Allow the UI to cap selected concepts at 8.

### 7.6 Explore Similar and Alchemy Recommendations

Explore Similar:

- input: one show plus selected concepts;
- output: 5 recommendations;
- every reason names selected concepts.

Alchemy:

- input: two or more shows plus selected concepts;
- output: 6 recommendations;
- supports chaining by using selected result shows as new inputs.

Recommendation resolution:

- AI returns title, external ID if available, media type, and reason.
- Resolve by external ID first.
- Confirm title case-insensitively against catalog result.
- Fall back to search by title/media type.
- Show unresolved recs as non-interactive or Search handoff.

### 7.7 AI Quality Validation

Create a small golden-test harness that scores or snapshots:

- voice adherence;
- taste alignment;
- surprise without betrayal;
- specificity;
- real-show integrity.

The real-show integrity requirement is non-negotiable for passing concept-based recommendation tests.

## 8. UI and Feature Plan

### 8.1 Global Layout

Implement a persistent app shell:

- left or responsive navigation/filter panel;
- main content area;
- persistent Find/Discover entry;
- persistent Settings entry;
- media type toggle where applicable;
- responsive layout for desktop and mobile.

The visual system should feel like a polished personal media tool:

- restrained, information-rich layouts;
- clear scan hierarchy;
- poster/backdrop imagery as first-class visual material;
- no decorative marketing hero replacing the app experience;
- compact controls using icons where appropriate;
- feature-specific empty/loading/error states.

### 8.2 Collection Home

Features:

- load saved shows for current namespace/user;
- apply selected filter and media type;
- group into:
  - Active
  - Excited (`Later + Excited`)
  - Interested (`Later + Interested`)
  - Other statuses collapsed: Wait, Quit, Done, and unclassified Later
- prominent larger tiles for Active;
- tile badges for in-collection and user rating;
- empty collection state pointing to Search/Ask;
- filter-empty state saying no results found.

Filters:

- All Shows
- tag filters, including No Tags when any tagless saved show exists
- genre
- decade
- community score range
- media type toggle: All / Movies / TV

### 8.3 Find / Discover Hub

Build a clear mode switcher with:

- Search
- Ask
- Alchemy

Respect Search on Launch by opening Search automatically when enabled.

### 8.4 Search

Features:

- text search by title/keywords;
- optional media type filter;
- poster grid;
- in-collection indicators;
- user rating indicators;
- click result to Show Detail;
- loading, no results, and provider error states.

Search itself should remain straightforward catalog UI with no AI persona.

### 8.5 Ask

Features:

- welcome view with six random starter prompts and refresh;
- chat transcript;
- input composer;
- mentioned shows horizontal strip;
- selectable mentioned shows opening Detail if resolved;
- unresolved mentions hand off to Search;
- seeded show context when launched from Show Detail's "Ask about this show" CTA;
- session reset/clear behavior.

### 8.6 Alchemy

Flow:

1. Select two or more starting shows from library and global catalog.
2. Tap Conceptualize Shows.
3. Render concepts as selectable chips.
4. Allow up to eight selected concepts.
5. Tap ALCHEMIZE.
6. Render six resolved recommendations with reasons.
7. Support More Alchemy chaining.

Rules:

- changing selected shows clears concepts and results;
- changing selected concepts clears downstream results;
- each recommendation preserves transient AI reason;
- saving a result follows normal collection rules.

### 8.7 Show Detail

Implement as the single source of truth for one show.

Section order:

1. Header media carousel with backdrops/posters/logos/videos and graceful fallback.
2. Core facts row: year, runtime or seasons/episodes, community score.
3. My Tags.
4. Overview and Scoop toggle/stream.
5. Ask about this show CTA.
6. Genres and languages.
7. Traditional recommendations strand.
8. Explore Similar concepts and recommendations.
9. Streaming availability.
10. Cast and Crew.
11. Seasons for TV.
12. Budget/Revenue for movies when available.

Toolbar relationship controls:

- status chips: Active, Interested, Excited, Done, Quit, Wait;
- Interested and Excited map to `my_status = later` plus matching `my_interest`;
- selecting any status saves the show;
- reselecting the active status triggers removal confirmation;
- confirmation can be suppressed after repeated removals;
- removal deletes the saved show and clears My Data;
- rating an unsaved show saves as Done;
- adding a tag to an unsaved show saves as Later + Interested.

Scoop states:

- no scoop: "Give me the scoop!"
- cached scoop: "Show the scoop"
- open title: "The Scoop"
- generating state visible during request
- regenerate after four hours on demand

Explore Similar states:

- initial Get Concepts CTA;
- concept chip selection;
- Explore Shows CTA requiring at least one concept;
- five recommendation results with reasons and selectable resolved shows.

### 8.8 Person Detail

Features:

- image gallery;
- name and bio;
- filmography/credits grouped by year;
- analytics charts:
  - average project ratings;
  - top genres;
  - projects by year;
- selecting a credit opens Show Detail.

Person data is catalog-derived and not stored as a saved user show unless future requirements add person collection behavior.

### 8.9 Settings and Your Data

Settings:

- font size/readability;
- Search on Launch;
- username;
- AI provider API key if user entry is supported;
- AI model selection;
- catalog provider API key if user entry is supported;
- display active namespace and dev user in benchmark/dev mode.

Data:

- Export My Data creates a `.zip` containing JSON backup of saved shows, My Data, settings, and metadata for current `(namespace_id, user_id)`.
- Dates are ISO-8601.
- Import/Restore is not required unless chosen as an optional extension; show as unavailable or omit from first implementation.

## 9. Business Rules Checklist

Implement and test:

- A show is in collection iff it has `my_status`.
- Setting any status saves the show.
- Choosing Interested or Excited saves as Later plus that interest.
- Rating an unsaved show saves as Done.
- Adding a tag to an unsaved show saves as Later + Interested.
- Saving without explicit status defaults to Later + Interested.
- Removing status confirms and then deletes the saved show plus My Data.
- Re-adding an existing show preserves latest My Data.
- User fields track independent update timestamps.
- Interest only applies to Later in UI, but previous interest may be retained for later reuse.
- User overlay wins everywhere.
- AI Scoop persists only for saved shows.
- Ask, Alchemy, and Explore Similar are session-only except saved shows and persisted Scoop.
- Namespace/user scoping applies to every persisted user record.

## 10. Implementation Milestones

### Milestone 1: Foundation and Compliance

Deliver:

- Next.js app scaffold.
- TypeScript, linting, testing, formatting.
- environment variable interface and `.env.example`.
- Supabase client setup.
- migration runner documentation.
- identity adapter for namespace/user.
- base app shell and design tokens.

Acceptance:

- app starts with one command;
- build/test scripts run;
- environment configuration requires no source edits;
- no committed secrets.

### Milestone 2: Database and Domain Model

Deliver:

- Supabase schema migrations.
- typed domain models.
- repository layer scoped by identity.
- merge service.
- collection service.
- test reset script scoped to namespace.

Acceptance:

- tests prove merge and collection save/remove rules;
- reset deletes only current namespace test data;
- clearing browser storage does not delete server-side collection data.

### Milestone 3: Catalog Integration

Deliver:

- catalog provider abstraction.
- search, detail, credits, images, videos, providers, recommendations, similar, and person calls.
- normalization into app display models.
- overlay saved My Data onto catalog results.

Acceptance:

- search results open detail;
- saved status/rating indicators appear across search and recommendation strands;
- detail page loads public data and gracefully handles missing media.

### Milestone 4: Collection Home and Filters

Deliver:

- Home page.
- status grouping.
- filters for tags, no tags, genre, decade, community score.
- media type toggle.
- saved show tiles and badges.

Acceptance:

- collection organization matches PRD grouping;
- filter combinations preserve status grouping;
- empty states are correct.

### Milestone 5: Show Detail My Data

Deliver:

- full detail page skeleton and major sections.
- toolbar status/interest chips.
- rating control.
- tag management.
- destructive removal confirmation.
- traditional recommendations, providers, cast/crew, seasons, budget/revenue.

Acceptance:

- all implicit save behaviors work;
- removal clears My Data;
- user overlay appears immediately after mutation and persists after reload.

### Milestone 6: Ask

Deliver:

- Ask mode UI.
- starter prompts and refresh.
- chat session state.
- conversation summarization.
- structured mentioned-shows parsing.
- catalog resolution and mentioned shows strip.
- Show Detail "Ask about this show" handoff.

Acceptance:

- Ask can recommend shows and render interactive resolved mentions;
- unresolved mentions fall back cleanly;
- chat does not persist after reset/leaving session.

### Milestone 7: Scoop

Deliver:

- Scoop generation API.
- streaming/progressive UI.
- four-hour freshness check.
- saved-show persistence.
- unsaved-show ephemeral handling.

Acceptance:

- Scoop voice and structure match spec;
- cached Scoop is reused until stale;
- unsaved generated Scoop does not become durable unless the show is saved.

### Milestone 8: Concepts, Explore Similar, and Alchemy

Deliver:

- single-show concept generation.
- multi-show shared concept generation.
- concept chip selection and max cap.
- Explore Similar five-rec flow.
- Alchemy six-rec flow.
- chaining support.
- real-show resolution with retry/fallback.

Acceptance:

- concepts are concise, evocative, and non-generic;
- reasons explicitly cite selected concepts;
- interactive recommendations resolve to real catalog items.

### Milestone 9: Person Detail

Deliver:

- person profile route.
- image gallery and bio.
- filmography grouped by year.
- analytics charts.
- credit-to-show navigation.

Acceptance:

- cast/crew links from Show Detail open Person Detail;
- credits open Show Detail with overlay behavior.

### Milestone 10: Settings, Export, and Polish

Deliver:

- Settings page.
- synced username/model settings.
- font size and Search on Launch preferences.
- Export My Data zip.
- loading/error states.
- responsive pass.
- accessibility pass.

Acceptance:

- backup zip includes current user/namespace data with ISO-8601 dates;
- settings survive reload and, where synced, device/browser changes;
- core journeys are usable on mobile and desktop.

### Milestone 11: Verification and Benchmark Hardening

Deliver:

- unit tests for domain logic.
- integration tests for server actions/routes.
- browser tests for key journeys.
- AI quality smoke/golden checks.
- namespace collision tests.
- documentation for setup, reset, and test execution.

Acceptance:

- all tests pass with a hosted Supabase instance;
- destructive tests are namespace-scoped;
- app can run repeatedly without collisions.

## 11. Testing Strategy

### 11.1 Unit Tests

Cover:

- save defaults;
- status/interest mapping;
- tag-to-save;
- rating-to-save;
- removal semantics;
- merge behavior;
- filter grouping;
- concept selection clearing downstream results;
- AI structured output parsing;
- recommendation resolver matching.

### 11.2 Integration Tests

Cover:

- repository scoping by namespace/user;
- Supabase schema constraints;
- test reset only deleting current namespace records;
- export data shape;
- settings persistence;
- server route validation and error handling.

### 11.3 Browser Tests

Cover the key journeys:

- Search -> Detail -> set Interested -> Home shows under Interested.
- Search -> Detail -> rate -> Home shows under Done/Other.
- Search -> Detail -> add tag -> sidebar tag filter appears.
- Detail -> remove status -> confirmation -> collection removal.
- Ask -> recommendation mention -> Detail -> save.
- Detail -> Get Concepts -> Explore Shows -> save recommendation.
- Alchemy -> select shows -> concepts -> recommendations -> chain.
- Detail -> Person -> credit -> Detail.
- Settings -> Export My Data.

### 11.4 AI Quality Tests

For deterministic test mode, use mock AI responses. For optional live checks:

- verify concepts are 1-3 words and bullet-only;
- verify Explore Similar returns 5 recs;
- verify Alchemy returns 6 recs;
- verify every actionable rec resolves to catalog;
- score selected outputs against the discovery quality bar.

## 12. Error Handling and Fallbacks

Catalog failures:

- show retry affordance;
- preserve existing saved data;
- do not wipe public fields with empty failed responses.

AI failures:

- show concise error;
- allow retry;
- if parsing fails, retry once with stricter instructions;
- fall back to commentary plus Search handoff.

Supabase failures:

- mutations return clear failure states;
- optimistic UI rolls back if write fails;
- no local-only persistence masquerades as saved data.

Missing media:

- use poster/backdrop fallbacks;
- never block core detail reading.

Missing providers/seasons/budget:

- omit or show neutral unavailable state, depending on section.

## 13. Security and Privacy

- Never commit secrets.
- Keep elevated Supabase keys server-only.
- Keep AI and catalog API calls server-side when using secret keys.
- Validate all server action inputs.
- Scope every user-owned query by namespace and user.
- Document benchmark identity as non-production.
- Design schema so real OAuth maps to the existing opaque `user_id`.

## 14. Data Export Shape

The export zip should contain at least:

```text
backup.json
manifest.json
```

`manifest.json`:

- app name/version;
- export timestamp;
- namespace ID;
- user ID;
- data model version.

`backup.json`:

- saved shows;
- My Data fields and timestamps;
- AI Scoop fields and timestamps;
- cloud settings;
- preferences/UI state where implemented.

All dates should be ISO-8601 strings.

## 15. Open Questions and Recommended Defaults

- `Next` status: keep in schema, do not expose as first-class UI yet.
- Custom named lists: defer; tags already satisfy current organization requirements.
- AI Scoop on unsaved show: generate ephemerally, do not implicitly save.
- Clearing My Rating: treat as null/unrated unless later product direction requires explicit unrated tombstone.
- Import/Restore: defer; export is required.
- Saved Alchemy sessions: defer; sessions are transient in current PRD.
- Explicit status filters: schema supports them, but initial sidebar should follow required filter set unless time allows.
- API key storage: prefer environment variables for benchmark mode; if user-entered keys are implemented, keep them server-side and document limitations.

## 16. Risk Areas

- AI recommendations may hallucinate or return mismatched IDs; mitigate with strict structured output, resolver validation, and fallback UI.
- Namespace/user scoping can be accidentally omitted; mitigate by requiring identity context in repository APIs and testing cross-namespace isolation.
- My Data overlay must appear everywhere, not just Home; mitigate by centralizing overlay enrichment.
- Detail page can become cluttered; mitigate with the specified narrative hierarchy and progressive sections.
- Supabase Auth may not exist in benchmark mode; mitigate with server-side dev identity abstraction that can later be replaced.
- Catalog provider variability can break mapping; mitigate with normalization tests and graceful missing-field handling.

## 17. Definition of Done

The implementation is complete when:

- The app can be configured from environment variables and run with one command.
- User-owned data persists in Supabase and survives client storage clearing.
- Every user-owned record is scoped by `(namespace_id, user_id)`.
- Collection save, update, merge, and removal rules match the PRD.
- Search, Home, Show Detail, Ask, Alchemy, Explore Similar, Person Detail, Settings, and Export are implemented.
- AI surfaces share the specified voice and satisfy real-show integrity rules for actionable recommendations.
- Destructive tests reset only the current namespace.
- Tests cover core domain rules, persistence scoping, and key user journeys.
- No product source implementation was created during this planning step.
