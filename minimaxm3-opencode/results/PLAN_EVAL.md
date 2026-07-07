### 1. Requirements Extraction

#### Benchmark Runtime & Isolation

- PRD-001 | `critical` | Use Next.js latest stable runtime | `infra_rider_prd.md > 2. Benchmark Baseline (Current Round)`
- PRD-002 | `critical` | Use Supabase official client libraries | `infra_rider_prd.md > 2. Benchmark Baseline (Current Round)`
- PRD-003 | `critical` | Ship `.env.example` with required variables | `infra_rider_prd.md > 3.1 Environment variable interface`
- PRD-004 | `important` | Ignore `.env*` secrets except example | `infra_rider_prd.md > 3.1 Environment variable interface`
- PRD-005 | `critical` | Configure build through env without code edits | `infra_rider_prd.md > 3.1 Environment variable interface`
- PRD-006 | `critical` | Keep secrets out of repo and server-only | `infra_rider_prd.md > 3.1 Environment variable interface`
- PRD-007 | `critical` | Provide app, test, reset command scripts | `infra_rider_prd.md > 3.2 One-command developer experience`
- PRD-008 | `critical` | Include repeatable schema evolution artifacts | `infra_rider_prd.md > 3.3 Database evolution artifacts`
- PRD-009 | `critical` | Use one stable namespace per build | `infra_rider_prd.md > 4.1 Build/run namespace (required)`
- PRD-010 | `critical` | Isolate namespaces and scope destructive resets | `infra_rider_prd.md > 4.1 Build/run namespace (required)`
- PRD-011 | `critical` | Attach every user record to `user_id` | `infra_rider_prd.md > 4.2 User identity (required)`
- PRD-012 | `critical` | Partition persisted data by namespace and user | `infra_rider_prd.md > 4.3 Relationship between namespace and user`
- PRD-013 | `important` | Support documented dev auth injection, prod-gated | `infra_rider_prd.md > 5.1 Auth is not required to be "real" in benchmark mode`
- PRD-014 | `important` | Real OAuth later needs no schema redesign | `infra_rider_prd.md > 5.2 Migration to real OAuth must be straightforward`
- PRD-015 | `critical` | Keep backend as persisted source of truth | `infra_rider_prd.md > 6.1 Source of truth`
- PRD-016 | `critical` | Make client cache safe to discard | `infra_rider_prd.md > 6.2 Cache is disposable`
- PRD-017 | `important` | Avoid Docker requirement for cloud-agent compatibility | `infra_rider_prd.md > 2. Benchmark Baseline (Current Round)`

#### Collection Data & Persistence

- PRD-018 | `critical` | Overlay saved user data on every show appearance | `product_prd.md > 4.1 Show (Movie or TV)`
- PRD-019 | `important` | Support visible statuses plus hidden `Next` | `product_prd.md > 4.2 Status System ("My Status")`
- PRD-020 | `critical` | Map Interested/Excited chips to Later interest | `product_prd.md > 4.2 Status System ("My Status")`
- PRD-021 | `important` | Support free-form multi-tag personal tag library | `product_prd.md > 4.4 Tags (User Lists)`
- PRD-022 | `critical` | Define collection membership by assigned status | `product_prd.md > 5.1 Collection Membership`
- PRD-023 | `critical` | Save shows from status, interest, rating, tagging | `product_prd.md > 5.2 Saving Triggers`
- PRD-024 | `critical` | Default save to Later/Interested except rating-save Done | `product_prd.md > 5.3 Default Values When Saving`
- PRD-025 | `critical` | Removing status deletes show and all My Data | `product_prd.md > 5.4 Removing from Collection`
- PRD-026 | `critical` | Re-add preserves My Data and refreshes public data | `product_prd.md > 5.5 Re-adding the Same Show`
- PRD-027 | `critical` | Track per-field My Data modification timestamps | `product_prd.md > 5.6 Timestamps`
- PRD-028 | `important` | Use timestamps for sorting, sync, freshness | `product_prd.md > 5.6 Timestamps`
- PRD-029 | `critical` | Persist Scoop only for saved shows, 4h freshness | `product_prd.md > 4.9 AI Scoop ("The Scoop")`
- PRD-030 | `important` | Keep Ask and Alchemy state session-only | `product_prd.md > 5.7 AI Data Persistence`
- PRD-031 | `critical` | Resolve AI recommendations to real selectable shows | `product_prd.md > 5.8 AI Recommendations Map to Real Shows`
- PRD-032 | `important` | Show collection and rating tile indicators | `product_prd.md > 5.9 Tile Indicators`
- PRD-033 | `important` | Sync libraries/settings consistently and merge duplicates | `product_prd.md > 5.10 Data Sync & Integrity`
- PRD-034 | `critical` | Preserve saved libraries across data-model upgrades | `product_prd.md > 5.11 Data Continuity Across Versions`
- PRD-035 | `important` | Persist synced settings, local settings, UI state | `supporting_docs/technical_docs/storage-schema.md > Other persistent storage (key-value settings)`
- PRD-036 | `important` | Keep provider IDs persisted and detail fetches transient | `supporting_docs/technical_docs/storage-schema.md > Show (movie or TV series)`
- PRD-037 | `critical` | Merge catalog fields safely and maintain timestamps | `supporting_docs/technical_docs/storage-schema.md > Merge / overwrite policy (important)`

#### App Navigation & Discover Shell

- PRD-038 | `important` | Provide filters panel and main screen destinations | `product_prd.md > 6. App Structure & Navigation`
- PRD-039 | `important` | Keep Find/Discover in persistent primary navigation | `product_prd.md > 6. App Structure & Navigation`
- PRD-040 | `important` | Keep Settings in persistent primary navigation | `product_prd.md > 6. App Structure & Navigation`
- PRD-041 | `important` | Offer Search, Ask, Alchemy discover modes | `product_prd.md > 6. App Structure & Navigation`

#### Collection Home & Search

- PRD-042 | `important` | Show only library items matching active filters | `product_prd.md > 7.1 Collection Home`
- PRD-043 | `important` | Group home into Active, Excited, Interested, Others | `product_prd.md > 7.1 Collection Home`
- PRD-044 | `important` | Support All, tag, genre, decade, score, media filters | `product_prd.md > 4.5 Filters (Ways to View the Collection)`
- PRD-045 | `important` | Render poster, title, and My Data badges | `product_prd.md > 7.1 Collection Home`
- PRD-046 | `detail` | Provide empty-library and empty-filter states | `product_prd.md > 7.1 Collection Home`
- PRD-047 | `important` | Search by title or keywords | `product_prd.md > 7.2 Search (Find â†’ Search)`
- PRD-048 | `important` | Use poster grid with collection markers | `product_prd.md > 7.2 Search (Find â†’ Search)`
- PRD-049 | `detail` | Auto-open Search when setting is enabled | `product_prd.md > 7.2 Search (Find â†’ Search)`
- PRD-050 | `important` | Keep Search non-AI in tone | `supporting_docs/ai_voice_personality.md > 1. Persona Summary`

#### Show Detail & Relationship UX

- PRD-051 | `important` | Preserve Show Detail narrative section order | `supporting_docs/detail_page_experience.md > 3. Narrative Hierarchy (Section Intent)`
- PRD-052 | `important` | Prioritize motion-rich header with graceful fallback | `supporting_docs/detail_page_experience.md > 3.1 Header Media`
- PRD-053 | `important` | Surface year, runtime/seasons, and community score early | `supporting_docs/detail_page_experience.md > 3.2 Core Facts + Community Score`
- PRD-054 | `important` | Place status/interest controls in toolbar | `supporting_docs/detail_page_experience.md > 3.3 My Relationship Controls`
- PRD-055 | `critical` | Auto-save unsaved tagged show as Later/Interested | `supporting_docs/detail_page_experience.md > 3.3 My Relationship Controls`
- PRD-056 | `critical` | Auto-save unsaved rated show as Done | `supporting_docs/detail_page_experience.md > 3.3 My Relationship Controls`
- PRD-057 | `important` | Show overview early for fast scanning | `supporting_docs/detail_page_experience.md > 2. First-15-Seconds Experience`
- PRD-058 | `important` | Scoop shows correct states and progressive feedback | `supporting_docs/detail_page_experience.md > 3.4 Overview + Scoop`
- PRD-059 | `important` | Ask-about-show deep-link seeds Ask context | `supporting_docs/detail_page_experience.md > 3.5 Ask About This Show`
- PRD-060 | `important` | Include traditional recommendations strand | `supporting_docs/detail_page_experience.md > 3.6 Traditional Recommendations Strand`
- PRD-061 | `important` | Explore Similar uses CTA-first concept flow | `supporting_docs/detail_page_experience.md > 3.7 Explore Similar (Concept Discovery)`
- PRD-062 | `important` | Include streaming availability and person-linking credits | `supporting_docs/detail_page_experience.md > 3.8 Streaming Availability`
- PRD-063 | `important` | Gate seasons to TV and financials to movies | `supporting_docs/detail_page_experience.md > 5. Critical States`
- PRD-064 | `important` | Keep primary actions early and page not overwhelming | `supporting_docs/detail_page_experience.md > 4. Busyness vs Power`

#### Ask Chat

- PRD-065 | `important` | Provide conversational Ask chat interface | `product_prd.md > 7.3 Ask (Find â†’ Ask)`
- PRD-066 | `important` | Answer directly with confident, spoiler-safe recommendations | `supporting_docs/discovery_quality_bar.md > 2.2 Ask / Explore Search Chat`
- PRD-067 | `important` | Show horizontal mentioned-shows strip from chat | `product_prd.md > 7.3 Ask (Find â†’ Ask)`
- PRD-068 | `important` | Open Detail from mentions or Search fallback | `product_prd.md > 7.3 Ask (Find â†’ Ask)`
- PRD-069 | `important` | Show six random starter prompts with refresh | `product_prd.md > 7.3 Ask (Find â†’ Ask)`
- PRD-070 | `important` | Summarize older turns while preserving voice | `supporting_docs/ai_prompting_context.md > 4. Conversation Summarization (Chat Surfaces)`
- PRD-071 | `important` | Seed Ask-about-show sessions with show handoff | `product_prd.md > 7.3 Ask (Find â†’ Ask)`
- PRD-072 | `critical` | Emit `commentary` plus exact `showList` contract | `supporting_docs/ai_prompting_context.md > 3.2 Ask with Mentions (Structured "Mentioned Shows")`
- PRD-073 | `important` | Retry malformed mention output once, then fallback | `supporting_docs/ai_prompting_context.md > 5. Guardrails & Fallbacks`
- PRD-074 | `important` | Redirect Ask back into TV/movie domain | `supporting_docs/ai_prompting_context.md > 1. Shared Rules (All AI Surfaces)`

#### Concepts, Explore Similar & Alchemy

- PRD-075 | `important` | Treat concepts as taste ingredients, not genres | `supporting_docs/concept_system.md > 1. What a Concept Is (User Definition)`
- PRD-076 | `important` | Return bullet-only, 1-3 word, non-generic concepts | `supporting_docs/ai_prompting_context.md > 3.4 Concepts (Single-Show and Multi-Show)`
- PRD-077 | `important` | Order concepts by strongest aha and varied axes | `supporting_docs/concept_system.md > 4. Generation Rules`
- PRD-078 | `important` | Require concept selection and guide ingredient picking | `supporting_docs/concept_system.md > 5. Selection UX Rules`
- PRD-079 | `important` | Return exactly five Explore Similar recommendations | `supporting_docs/concept_system.md > 6. Concepts â†’ Recommendations Contract`
- PRD-080 | `important` | Support full Alchemy loop with chaining | `product_prd.md > 7.4 Alchemy (Find â†’ Alchemy)`
- PRD-081 | `important` | Clear downstream results when inputs change | `product_prd.md > 7.4 Alchemy (Find â†’ Alchemy)`
- PRD-082 | `important` | Generate shared multi-show concepts with larger option pool | `supporting_docs/concept_system.md > 8. Notes`
- PRD-083 | `important` | Cite selected concepts in concise recommendation reasons | `supporting_docs/concept_system.md > 6. Concepts â†’ Recommendations Contract`
- PRD-084 | `important` | Deliver surprising but defensible taste-aligned recommendations | `supporting_docs/discovery_quality_bar.md > 1.2 Taste Alignment`

#### AI Voice, Persona & Quality

- PRD-085 | `important` | Keep one consistent AI persona across surfaces | `supporting_docs/ai_voice_personality.md > 1. Persona Summary`
- PRD-086 | `critical` | Enforce shared AI guardrails across all surfaces | `supporting_docs/ai_prompting_context.md > 1. Shared Rules (All AI Surfaces)`
- PRD-087 | `important` | Make AI warm, joyful, and light in critique | `supporting_docs/ai_voice_personality.md > 2. Non-Negotiable Voice Pillars`
- PRD-088 | `important` | Structure Scoop as personal taste mini-review | `supporting_docs/ai_voice_personality.md > 4.1 Scoop (Show Detail "The Scoop")`
- PRD-089 | `important` | Keep Ask brisk and dialogue-like by default | `supporting_docs/ai_voice_personality.md > 4.2 Ask (Find â†’ Ask)`
- PRD-090 | `important` | Feed AI the right surface-specific context inputs | `supporting_docs/ai_prompting_context.md > 2. Shared Inputs (Typical)`
- PRD-091 | `important` | Validate discovery with rubric and hard-fail integrity | `supporting_docs/discovery_quality_bar.md > 4. Scoring Rubric (Quick)`

#### Person Detail

- PRD-092 | `important` | Show person gallery, name, and bio | `product_prd.md > 7.6 Person Detail Page`
- PRD-093 | `important` | Include ratings, genres, and projects-by-year analytics | `product_prd.md > 7.6 Person Detail Page`
- PRD-094 | `important` | Group filmography by year | `product_prd.md > 7.6 Person Detail Page`
- PRD-095 | `important` | Open Show Detail from selected credit | `product_prd.md > 7.6 Person Detail Page`

#### Settings & Export

- PRD-096 | `important` | Include font size and Search-on-launch settings | `product_prd.md > 7.7 Settings & Your Data`
- PRD-097 | `important` | Support username, model, and API-key settings safely | `product_prd.md > 7.7 Settings & Your Data`
- PRD-098 | `critical` | Export saved shows and My Data as zip | `product_prd.md > 7.7 Settings & Your Data`
- PRD-099 | `important` | Encode export dates using ISO-8601 | `product_prd.md > 7.7 Settings & Your Data`

Total: 99 requirements (30 critical, 67 important, 2 detail) across 10 functional areas

### 2. Coverage Table

| PRD-ID | Requirement | Severity | Coverage | Evidence | Gap |
| ------ | ----------- | -------- | -------- | -------- | --- |
| PRD-001 | Use Next.js latest stable runtime | critical | full | `0.2 Tech baseline`: "Next.js (App Router, latest stable)" |  |
| PRD-002 | Use Supabase official client libraries | critical | full | `0.2 Tech baseline`: "Supabase"; `1. Repository layout`: `src/lib/supabase/` |  |
| PRD-003 | Ship `.env.example` with required variables | critical | full | `2.1 Environment, secrets, and scripts` lists `.env.example` variables |  |
| PRD-004 | Ignore `.env*` secrets except example | important | full | `2.1 Environment, secrets, and scripts`: `.gitignore` excludes `.env*` except `.env.example` |  |
| PRD-005 | Configure build through env without code edits | critical | full | `2.1 Environment, secrets, and scripts` documents env-driven Supabase, catalog, AI, namespace, and dev user config |  |
| PRD-006 | Keep secrets out of repo and server-only | critical | full | `0.2 Tech baseline`: anon key only in browser, service role server-only; `4.1 Catalog client surface`: API key never reaches browser |  |
| PRD-007 | Provide app, test, reset command scripts | critical | full | `2.1 Environment, secrets, and scripts`: `dev`, `test`, `test:reset` |  |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | `2.3 Database schema`: forward-only deterministic migrations; `Migrations + seed` list |  |
| PRD-009 | Use one stable namespace per build | critical | full | `0.2 Tech baseline`: every persisted record carries `namespace_id`; `NAMESPACE_ID` in `.env.example` |  |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | `8.1 Identity, namespaces, isolation`: all queries pass both IDs and reset deletes by namespace only |  |
| PRD-011 | Attach every user record to `user_id` | critical | full | `2.3 Database schema`: `shows`, `cloud_settings`, and `chat_sessions` include `user_id`; `0.2 Tech baseline` |  |
| PRD-012 | Partition persisted data by namespace and user | critical | full | `2.3 Database schema`: unique `(namespace_id, user_id, id)`; RLS asserts both settings |  |
| PRD-013 | Support documented dev auth injection, prod-gated | important | full | `2.2 Namespace + identity injection`: reads headers in development/test only and rejects in production |  |
| PRD-014 | Real OAuth later needs no schema redesign | important | full | `2.2 Namespace + identity injection`: `user_id` opaque; data model OAuth-ready |  |
| PRD-015 | Keep backend as persisted source of truth | critical | full | `8.2 Source of truth`: server is the only writer and client refreshes from server |  |
| PRD-016 | Make client cache safe to discard | critical | full | `3.4 Local settings / UI state`: backend is source of truth for user-owned data; `8.2 Source of truth` |  |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | full | `0.2 Tech baseline`: "No Docker required" |  |
| PRD-018 | Overlay saved user data on every show appearance | critical | partial | `useShowDetail(id)` returns merged stored and live catalog; `PosterTile` shows collection and rating badges | The plan covers merge and badges but does not explicitly require the complete My Data overlay everywhere shows appear, including all search, recommendation, AI, and person-credit tiles. |
| PRD-019 | Support visible statuses plus hidden `Next` | important | full | `11. Risks & open questions handled`: model supports `next`, UI does not surface a chip |  |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | full | `3.1 Library Home page`: `later+excited` and `later+interested`; `3.2 Auto-save semantics`: interest sets `later` |  |
| PRD-021 | Support free-form multi-tag personal tag library | important | full | `3.2 Show Detail page`: `MyTags` and `TagPicker`; `3.3 Filters`: distinct tags auto-derived |  |
| PRD-022 | Define collection membership by assigned status | critical | full | `2.5 Storage / domain layer`: `isInCollection(show): myStatus != null` |  |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | full | `3.2 Auto-save semantics` table covers status, interest, rating, and tag |  |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | `2.5 Storage / domain layer`: `defaultSavePolicy`; `3.2 Auto-save semantics` table |  |
| PRD-025 | Removing status deletes show and all My Data | critical | partial | `3.2 Show Detail page`: `removeFromCollection()` and confirmation dialog | The plan defines the removal action but does not explicitly state that the stored show and all My Data fields, including tags, rating, interest, and AI Scoop, are deleted or cleared. |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | full | `2.5 Storage / domain layer`: `ensureShowExists` upsert with merge; `4.3 Catalog to Show mapping`: merge on save or refresh |  |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | `2.3 Database schema`: individual update date fields for tags, score, status, interest, and scoop |  |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | full | `3.1 Library Home page`: sort by most recent `my*UpdateDate`; `2.5 mergeShow`; `5.1 AI Scoop` freshness |  |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | full | `5.1 AI Scoop`: stored only if `my_status IS NOT NULL`; regenerate after 4 h |  |
| PRD-030 | Keep Ask and Alchemy state session-only | important | full | `5.2 Ask`: ephemeral `chat_sessions`; `5.5 Alchemy`: never persisted past the session |  |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | full | `4.5 Mentioned shows & AI to catalog resolution`: lookup by external ID, title fallback, resolved shows become real objects |  |
| PRD-032 | Show collection and rating tile indicators | important | full | `8.5 Tile indicators`: `PosterTile` shows in-collection and user rating badges |  |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | partial | `2.5 mergeShow`; `7. Settings & Your Data`; unique `(namespace_id, user_id, id)` | The plan covers conflict merging and synced settings, but duplicate detection and transparent duplicate merging are only implied by uniqueness, not planned as a sync behavior. |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | partial | `8.3 Schema evolution`: `data_model_version`, forward-only idempotent migrations, migration test | The plan defines migration mechanics but not an explicit continuity policy or migration tests proving saved shows and My Data survive model upgrades. |
| PRD-035 | Persist synced settings, local settings, UI state | important | full | `3.4 Local settings / UI state`; `7. Settings & Your Data`: cloud settings and local settings boundaries |  |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | full | `4.3 Catalog to Show mapping`: providers stored as IDs, credits/seasons/videos/recommendations/similar transient |  |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | full | `2.5 Storage / domain layer`: non-my fields select first non-empty, my fields resolve by timestamps |  |
| PRD-038 | Provide filters panel and main screen destinations | important | full | `1. Repository layout`: routes for home, find, show, person, settings; `3.1 Library Home page`: `Sidebar` filter list |  |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | partial | `1. Repository layout`: `/find` routes; `12. Coverage map`: App Structure routes and nav | The plan creates Find routes but does not define a persistent primary navigation component or placement that keeps Find/Discover globally available. |
| PRD-040 | Keep Settings in persistent primary navigation | important | partial | `1. Repository layout`: `/settings/page.tsx`; `12. Coverage map`: App Structure routes and nav | The plan creates the Settings route but does not specify persistent primary navigation access to it. |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | `1. Repository layout`: `/find/search`, `/find/ask`, `/find/alchemy`; `0.4 Build order` |  |
| PRD-042 | Show only library items matching active filters | important | full | `3.1 Library Home page`: `useLibraryHome()` queries by selected filter and media type |  |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | `3.1 Library Home page`: `StatusSections` renders Active, Excited, Interested, Other collapsed |  |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | full | `3.1 Sidebar`; `3.3 Filters & data views`: all, genre, myStatus, communityScore, decade, myTag plus media type |  |
| PRD-045 | Render poster, title, and My Data badges | important | full | `PosterGrid` and `PosterTile`; `8.5 Tile indicators` |  |
| PRD-046 | Provide empty-library and empty-filter states | detail | full | `3.1 Library Home page`: no collection and filter-empty states |  |
| PRD-047 | Search by title or keywords | important | full | `4.1 Catalog client surface`: `searchShows(query)`; `4.6 Search`: `SearchBar` |  |
| PRD-048 | Use poster grid with collection markers | important | full | `4.6 Search`: `PosterGrid` of results and in-collection indicator |  |
| PRD-049 | Auto-open Search when setting is enabled | detail | full | `8.6 Search on Launch`: redirects to `/find/search` when `autoSearch` is true |  |
| PRD-050 | Keep Search non-AI in tone | important | partial | `4.6 Search` is implemented as a catalog search page outside `5. AI surfaces` | The plan separates Search from AI implementation, but it does not explicitly call out the non-AI tone or acceptance criteria for keeping Search straightforward. |
| PRD-051 | Preserve Show Detail narrative section order | important | partial | `4.4 Show Detail page (full build)` lists major sections; `12. Coverage map` maps `detail_page_experience.md` | The full-build list is not the exact prescribed narrative hierarchy and omits an explicit ordering guarantee tying all sections together. |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | full | `4.4 Show Detail page`: carousel uses videos when available and graceful poster fallback |  |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | full | `3.2 Show Detail page`: `CoreFactsRow` includes year, runtime/seasons, community score |  |
| PRD-054 | Place status/interest controls in toolbar | important | full | `3.2 Show Detail page`: `MyStatusToolbar` chips for status and interest |  |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | `3.2 Auto-save semantics`: add tag results in `later` and `interested` |  |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | `3.2 Auto-save semantics`: set rating results in `done` |  |
| PRD-057 | Show overview early for fast scanning | important | full | `4.4 Show Detail page`: `Overview` plus Scoop; Show Detail skeleton builds core facts first |  |
| PRD-058 | Scoop shows correct states and progressive feedback | important | full | `5.1 AI Scoop`: CTA copy for no cached/cached/open and streaming "Generating..." feedback |  |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | full | `4.4 Show Detail page`: Ask CTA seeds conversation; `5.2 Ask`: launched from Detail with show context |  |
| PRD-060 | Include traditional recommendations strand | important | full | `4.4 Show Detail page`: `Recommendations` strand of similar and recommended catalog-native items |  |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | full | `5.4 Explore Similar`: Get Concepts, select concepts, Explore Shows |  |
| PRD-062 | Include streaming availability and person-linking credits | important | full | `4.4 Show Detail page`: `Providers` strip and `CastCrew` strands to Person Detail |  |
| PRD-063 | Gate seasons to TV and financials to movies | important | full | `4.4 Show Detail page`: `Seasons (TV only)` and `BudgetRevenue (movies)` |  |
| PRD-064 | Keep primary actions early and page not overwhelming | important | partial | `3.2 Show Detail page` puts status, rating, tags in the initial skeleton; `4.4` adds sections | The plan places several actions early but does not specify the busyness/power layout rules or how long-tail information is visually de-emphasized. |
| PRD-065 | Provide conversational Ask chat interface | important | full | `5.2 Ask`: `MessageList`, assistant/user bubbles, `Composer` |  |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | partial | `5.2 Ask`: tone is low-friction and fast; `5.6 Persona`: shared rules included | The plan covers persona and spoiler safety, but it does not explicitly require direct answers within the first few lines or a confidence acceptance check for Ask responses. |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | `5.2 Ask`: `MentionedShowsStrip` horizontal row below assistant message |  |
| PRD-068 | Open Detail from mentions or Search fallback | important | full | `4.5 Mentioned shows & AI to catalog resolution`: unresolved titles offer Search handoff; resolved shows become real objects |  |
| PRD-069 | Show six random starter prompts with refresh | important | full | `5.2 Ask`: Welcome view has 6 random starter prompts and refresh re-roll |  |
| PRD-070 | Summarize older turns while preserving voice | important | full | `5.2 Ask`: summarize older turns in 1-2 sentences with same voice after more than 10 turns |  |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | full | `5.2 Ask`: `prefilledShowId` and show context when launched from Show Detail |  |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | full | `5.2 Ask`: model returns `{ commentary, showList }` and validates `Title::externalId::mediaType;;` |  |
| PRD-073 | Retry malformed mention output once, then fallback | important | full | `5.2 Ask`: retry once with stricter formatting, then unstructured commentary plus Search handoff |  |
| PRD-074 | Redirect Ask back into TV/movie domain | important | full | `5. AI surfaces`: centralizes shared rules; `5.6 Persona & prompt loading`: all prompts include shared rules |  |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | full | `5.3 Concepts`: specificity, diversity across structure, vibe, emotion, craft; `5.4 UX copy` |  |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | full | `5.3 Concepts`: bullet list only, 1-3 words, no generic concepts |  |
| PRD-077 | Order concepts by strongest aha and varied axes | important | full | `5.3 Concepts`: diversity across axes and order by strength |  |
| PRD-078 | Require concept selection and guide ingredient picking | important | full | `5.4 Explore Similar`: select 1+ concepts; copy says "pick the ingredients you want more of" |  |
| PRD-079 | Return exactly five Explore Similar recommendations | important | full | `5.4 Explore Similar`: returns 5 recommendations |  |
| PRD-080 | Support full Alchemy loop with chaining | important | full | `5.5 Alchemy`: pick shows, conceptualize, select, alchemize, More Alchemy chain |  |
| PRD-081 | Clear downstream results when inputs change | important | full | `5.5 Alchemy`: changing shows clears concepts and results; changing concepts clears results |  |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | partial | `5.5 Alchemy`: returns about 8 shared concepts | The plan requires shared multi-show concepts but uses about the same count as single-show concepts, so the larger multi-show option pool is not satisfied. |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | full | `5.4 Explore Similar` and `5.5 Alchemy`: recommendations include reasons naming aligned concepts |  |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | partial | `5. AI surfaces`: taste context builder; `5.4` and `5.5` require concept-grounded reasons | The plan covers taste alignment and defensibility through reasons, but it does not plan for the surprise-without-betrayal quality bar. |
| PRD-085 | Keep one consistent AI persona across surfaces | important | full | `5. AI surfaces`: all AI surfaces share one engine and persona |  |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | full | `5.6 Persona & prompt loading`: all prompts include persona block, shared rules, and surface contract |  |
| PRD-087 | Make AI warm, joyful, and light in critique | important | full | `5.1 AI Scoop`: friend/critic and hype/measured tone; `5.6` persona block |  |
| PRD-088 | Structure Scoop as personal taste mini-review | important | full | `5.1 AI Scoop`: Personal Take, Stack-Up, The Scoop, Fit & Warnings, Worth It |  |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | full | `5.2 Ask`: 1-3 tight paragraphs, bulleted lists for multi-recs |  |
| PRD-090 | Feed AI the right surface-specific context inputs | important | full | `5. AI surfaces`: taste context builder; `5.2 Ask`: library digest and show context |  |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | full | `9.1 Test layers`: concept validator, parser, endpoint tests; `13. Definition of Done`: discovery surfaces satisfy rubric |  |
| PRD-092 | Show person gallery, name, and bio | important | full | `6. Person Detail`: `PersonHeader` and `ImageGallery` |  |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | full | `6. Person Detail`: average project rating, top genres, projects-by-year charts |  |
| PRD-094 | Group filmography by year | important | full | `6. Person Detail`: `FilmographyByYear` grouped by year |  |
| PRD-095 | Open Show Detail from selected credit | important | full | `6. Person Detail`: tapping a tile opens `ShowDetail` |  |
| PRD-096 | Include font size and Search-on-launch settings | important | full | `7. Settings & Your Data`: `FontSize` and `AutoSearch` |  |
| PRD-097 | Support username, model, and API-key settings safely | important | full | `7. Settings & Your Data`: username, masked API keys, model selector, env-injected keys |  |
| PRD-098 | Export saved shows and My Data as zip | critical | full | `7. Settings & Your Data`: `ExportMyData` zip with `backup.json`; `8.7 Backup export` |  |
| PRD-099 | Encode export dates using ISO-8601 | important | full | `7. Settings & Your Data`: ISO-8601 dates; `9.1 Test layers`: export schema dates in ISO-8601 |  |

### 3. Coverage Scores

Overall score:

```
score = (87 x 1.0 + 12 x 0.5) / 99 x 100 = 93.9%
```

Critical:  (27 x 1.0 + 3 x 0.5) / 30 x 100 = 95.0%  (28.5 of 30 critical requirements)
Important: (58 x 1.0 + 9 x 0.5) / 67 x 100 = 93.3%  (62.5 of 67 important requirements)
Detail:    (2 x 1.0 + 0 x 0.5) / 2 x 100 = 100.0%  (2 of 2 detail requirements)
Overall:   93.9% (99 total requirements)

### 4. Top Gaps

1. PRD-034 (`critical`) - Preserve saved libraries across data-model upgrades. The plan has migrations and a version field, but without explicit continuity scenarios, upgrade work could accidentally preserve schema shape while losing or corrupting saved shows, ratings, tags, statuses, interest, or Scoop.
2. PRD-018 (`critical`) - Overlay saved user data on every show appearance. If overlay behavior is not made universal, users will see inconsistent relationship state across Search, AI results, recommendation rows, and detail screens, which undermines the core "your version of the show" promise.
3. PRD-025 (`critical`) - Removing status deletes show and all My Data. The plan provides a removal control but does not spell out the destructive data effect, so an implementation could leave stale tags, ratings, interest, or Scoop behind after collection removal.
4. PRD-033 (`important`) - Sync libraries/settings consistently and merge duplicates. The plan has merge rules and uniqueness constraints, but no explicit duplicate reconciliation path; sync edge cases could create confusing duplicate or stale library records.
5. PRD-051 (`important`) - Preserve Show Detail narrative section order. The plan includes the sections but does not lock the exact narrative hierarchy, so the page could ship functionally complete while losing the intended first-15-seconds flow.

### 5. Coverage Narrative

#### Overall Posture

This is a strong and implementation-ready plan with minor but meaningful gaps. It is especially solid on infrastructure, persistence primitives, AI surface contracts, and end-to-end feature breadth. The remaining weaknesses are not broad omissions; they are places where the plan relies on implication rather than writing down strict behavioral acceptance criteria.

#### Strength Clusters

The strongest areas are Benchmark Runtime & Isolation, Ask Chat, Concepts/Explore Similar/Alchemy, AI Voice/Persona/Quality, Person Detail, and Settings & Export. These sections include concrete routes, server boundaries, persistence tables, endpoint contracts, validation behavior, and test coverage. The plan also does a good job translating product behaviors like auto-save defaults, Scoop freshness, structured Ask mentions, and namespace isolation into implementable units.

#### Weakness Clusters

The partial items cluster around cross-surface consistency and UX intent rather than missing feature inventory. Collection Data & Persistence has a few critical gaps where the plan names the mechanism but not the exact user-data guarantee. App Navigation and Show Detail have partials where routes or sections exist, but persistent navigation and the detail narrative hierarchy are not specified enough to prevent drift. AI discovery quality is covered technically, but the "surprising but defensible" and direct-answer quality bars need sharper acceptance language.

#### Risk Assessment

If executed as-is, the most likely failure mode is a build that passes functional smoke tests but feels inconsistent at the product edges. QA would probably notice saved-state mismatches on non-detail tiles, ambiguous behavior after removing a show from the collection, or a Show Detail page that contains the right components in a less useful order. Stakeholders focused on durability would also flag that migrations are present but user-library continuity is not tested as a first-class promise.

#### Remediation Guidance

The plan needs targeted acceptance criteria rather than new architecture. Add explicit invariants for My Data overlay on every show renderer, full destructive removal semantics, data-upgrade continuity tests, duplicate merge behavior, persistent primary navigation, and exact Show Detail section order. For AI quality, add rubric-backed checks for direct Ask answers and surprise-without-betrayal recommendations so those qualities are not left to prompt intent alone.
