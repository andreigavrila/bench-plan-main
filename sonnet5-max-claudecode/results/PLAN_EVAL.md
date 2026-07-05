### 1. Requirements Extraction

#### Pass 1: Identify Functional Areas

1. Benchmark Runtime & Isolation
2. Collection Data & Persistence
3. App Navigation & Discover Shell
4. Collection Home & Search
5. Show Detail & Relationship UX
6. Ask Chat
7. Concepts, Explore Similar & Alchemy
8. AI Voice, Persona & Quality
9. Person Detail
10. Settings & Export

#### Pass 2: Extract Requirements Within Each Area

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
| PRD-001 | Use Next.js latest stable runtime | critical | full | Section 3: "Next.js (latest stable), App Router" | |
| PRD-002 | Use Supabase official client libraries | critical | full | Section 3: "accessed via `@supabase/supabase-js`" | |
| PRD-003 | Ship `.env.example` with required variables | critical | full | Section 10 env sketch and Phase 0 `.env.example` task | |
| PRD-004 | Ignore `.env*` secrets except example | important | full | Section 10 checklist: "`.env.example` + `.gitignore` secret exclusion" | |
| PRD-005 | Configure build through env without code edits | critical | full | Section 10 `.env.example` variables and Section 4.2 env/header namespace resolution | |
| PRD-006 | Keep secrets out of repo and server-only | critical | full | Section 5.4: env keys never sent to browser; encrypted user overrides | |
| PRD-007 | Provide app, test, reset command scripts | critical | full | Section 10 scripts table: `dev`, `test`, `test:reset`, migration/seed scripts | |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | Section 5.5: Supabase migrations and seed.sql | |
| PRD-009 | Use one stable namespace per build | critical | full | Section 4.1 and 4.2 define `namespace_id` and default `NAMESPACE_ID` | |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | Section 4.4 `test:reset` scoped to namespace; Section 11 isolation tests | |
| PRD-011 | Attach every user record to `user_id` | critical | full | Section 5.2 `user_shows` and `user_settings`; Section 9 "no table omits `user_id`" | |
| PRD-012 | Partition persisted data by namespace and user | critical | full | Section 4.1: effective partition key `(namespace_id, user_id)` | |
| PRD-013 | Support documented dev auth injection, prod-gated | important | full | Section 4.2 dev selector gated by `ENABLE_DEV_AUTH` and non-production | |
| PRD-014 | Real OAuth later needs no schema redesign | important | full | Section 4.3 RLS/auth migration is additive with no table changes | |
| PRD-015 | Keep backend as persisted source of truth | critical | full | Section 3 server-mediated Supabase; Section 9 backend source of truth | |
| PRD-016 | Make client cache safe to discard | critical | full | Section 3: TanStack Query cache-only and clearing loses nothing | |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | full | Section 3: hosted Supabase primary, local Supabase never required | |
| PRD-018 | Overlay saved user data on every show appearance | critical | full | Section 5.3 `getDisplayShow()` used by every surface | |
| PRD-019 | Support visible statuses plus hidden `Next` | important | full | Section 5.2 `my_status` includes `next`; Section 14 keeps Next modeled but not surfaced | |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | full | Section 5.3 `computeSaveDefaults(trigger)` interest chip rule | |
| PRD-021 | Support free-form multi-tag personal tag library | important | full | Section 5.2 `my_tags` array and Section 6.2 `/api/collection/tags` | |
| PRD-022 | Define collection membership by assigned status | critical | full | Section 5.1 row existence equals in-collection; `my_status` is NOT NULL | |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | full | Section 6.2 status, interest, tags, rating routes with auto-save behavior | |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | Section 5.3 `computeSaveDefaults(trigger)` encodes default and rating exception | |
| PRD-025 | Removing status deletes show and all My Data | critical | full | Section 5.3 `computeRemoval()` and Section 6.2 `DELETE /api/collection/:showId` | |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | full | Section 5.3 overlay/catalog merge functions; Section 11 re-add merge tests | |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | Section 5.2 timestamp columns for status, interest, tags, score, scoop | |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | partial | Section 5.3 timestamp merge; Section 8.4 Scoop freshness; Section 8.5 recently-updated context | Sorting behavior for the collection is not specified as a concrete UI/query rule. |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | full | Section 8.4 cached only if saved and within `SCOOP_FRESHNESS_HOURS` | |
| PRD-030 | Keep Ask and Alchemy state session-only | important | full | Section 2/A6: session state lives in client memory only | |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | full | Section 8.3 shared `resolveShowReference()` pipeline | |
| PRD-032 | Show collection and rating tile indicators | important | full | Phase 1 "tile badges"; Section 6.1 search results annotated with `isInCollection` | |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | partial | Section 5.3 timestamp merge and Section 11 multi-device merge tests | Duplicate detection/transparent merge is not planned beyond uniqueness and timestamp conflict handling. |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | full | Section 5.5 additive migrations and no breaking migration policy | |
| PRD-035 | Persist synced settings, local settings, UI state | important | partial | Section 5.2 `user_settings`; Section 5.2 says UI state is client-local only | The plan persists synced settings but does not define durable key-value persistence for all local/UI state keys. |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | full | Section 5.2 `provider_data`; Section 6.1 credits/videos/recs/providers transient sub-resources | |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | full | Section 5.3 `mergeCatalogSnapshot` and `mergeUserOverlay` policies | |
| PRD-038 | Provide filters panel and main screen destinations | important | full | Section 3.2 routes and `FiltersSidebar`; Phase 1 filters/sidebar work | |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | partial | Section 3.2 includes `/find` and `FindDiscoverPage` | The plan defines the route/page but not a persistent primary navigation element. |
| PRD-040 | Keep Settings in persistent primary navigation | important | partial | Section 3.2 includes `/settings` and `SettingsPage` | The plan defines the route/page but not a persistent primary navigation element. |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | Section 3.2 `SearchMode`, `AskMode`, `AlchemyMode`; Phase 2 AI surfaces | |
| PRD-042 | Show only library items matching active filters | important | full | Section 6.2 `GET /api/collection?filter=&mediaType=` | |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | Phase 1 "Collection Home (grouped sections)" and Section 3.2 section components | |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | full | Phase 1 filters: tags, genre, decade, score, media-type | |
| PRD-045 | Render poster, title, and My Data badges | important | full | Section 3.2 shared `PosterTile`; Phase 1 "tile badges" | |
| PRD-046 | Provide empty-library and empty-filter states | detail | missing | none | Empty collection and empty-filter states are not called out in the plan. |
| PRD-047 | Search by title or keywords | important | full | Section 6.1 `GET /api/catalog/search?q=&mediaType=` | |
| PRD-048 | Use poster grid with collection markers | important | partial | Phase 1 "Search (catalog search + in-collection markers)" | Collection markers are explicit, but the poster-grid presentation is not specified. |
| PRD-049 | Auto-open Search when setting is enabled | detail | full | Phase 1 Search includes `"search on launch" setting`; Section 6.4 `auto-search` | |
| PRD-050 | Keep Search non-AI in tone | important | full | Section 8.1: "`Search` explicitly imports none of this" AI persona | |
| PRD-051 | Preserve Show Detail narrative section order | important | partial | Section 3.2 lists Show Detail features in an approximate order | The exact narrative hierarchy is not explicitly preserved, and relationship controls are grouped differently. |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | partial | Section 3.2 `HeaderMediaCarousel`; Phase 1 header media | The plan names header media but does not specify trailer/motion priority or graceful poster/backdrop fallback. |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | full | Section 3.2 `CoreFactsRow`; Phase 1 core facts and community score | |
| PRD-054 | Place status/interest controls in toolbar | important | partial | Section 3.2 `MyRelationshipControls/features/{StatusChips...}` | Status/interest controls are planned, but toolbar placement is not explicit. |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | Section 5.3 tag trigger defaults to later + interested | |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | Section 5.3 rating trigger defaults to done | |
| PRD-057 | Show overview early for fast scanning | important | full | Section 3.2 `OverviewAndScoop` appears before long-tail sections | |
| PRD-058 | Scoop shows correct states and progressive feedback | important | full | Section 8.4 streaming/generating; Section 11 component tests for no/cached/generating | |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | full | Phase 2 Ask includes `"about this show" handoff`; Section 8.2 optional handoff show | |
| PRD-060 | Include traditional recommendations strand | important | full | Section 3.2 `RecommendationsStrand`; Phase 1 recommendations strand | |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | full | Phase 2 Explore Similar concepts to selection to recs; Section 3.2 `ExploreSimilar` | |
| PRD-062 | Include streaming availability and person-linking credits | important | full | Section 3.2 `StreamingAvailability`, `CastCrewStrands`; Person journey in Section 13 | |
| PRD-063 | Gate seasons to TV and financials to movies | important | full | Section 3.2 `SeasonsStrand` TV only and `BudgetRevenue` movie only | |
| PRD-064 | Keep primary actions early and page not overwhelming | important | partial | Section 3.2 places core facts, controls, overview, scoop before long-tail sections | The plan implies early actions by ordering, but does not address busyness/power or clutter management directly. |
| PRD-065 | Provide conversational Ask chat interface | important | full | Section 3.2 `AskMode/features/{ChatThread...}`; Phase 2 Ask | |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | partial | Section 8.1 base persona; Section 8.2 Ask contract; Section 11 quality rubric | The plan covers persona and spoiler safety, but does not explicitly require direct answers in the opening lines. |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | Section 3.2 `MentionedShowsStrip`; Section 6.3 Ask resolves `showList` before strip render | |
| PRD-068 | Open Detail from mentions or Search fallback | important | full | Section 8.3 resolved shows selectable; unresolved hand off to Search | |
| PRD-069 | Show six random starter prompts with refresh | important | partial | Section 6.3 `GET /api/ai/ask/starters` returns 6 random prompts | Refresh behavior is not explicitly planned, only random retrieval. |
| PRD-070 | Summarize older turns while preserving voice | important | full | Section 8.6 summarizes after 10 messages in same persona voice | |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | full | Section 8.2 Ask input includes optional handoff show | |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | full | Section 8.2 exact `{ commentary, showList: "Title::externalId::mediaType;;..." }` | |
| PRD-073 | Retry malformed mention output once, then fallback | important | full | Section 8.3 `withStructuredRetry()` one retry then fallback | |
| PRD-074 | Redirect Ask back into TV/movie domain | important | partial | Section 11 AI quality checks include drift outside TV/movies via discovery rubric | The plan does not define an explicit Ask-domain redirect behavior or prompt rule. |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | partial | Section 8.2 concepts are bullet-only concepts for source shows; Section 8.5 taste context | The plan does not explicitly prohibit genre/plot concepts or encode the "taste ingredient" definition. |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | full | Section 8.2 Concepts output: bullet list, 1-3 words, no explanation | |
| PRD-077 | Order concepts by strongest aha and varied axes | important | missing | none | Concept ordering and varied-axis generation are not specified. |
| PRD-078 | Require concept selection and guide ingredient picking | important | partial | Phase 2 Explore Similar/Alchemy concepts to selection to recs; `MAX_SELECTED_CONCEPTS` | Selection is covered, but ingredient-picking guidance and empty-state nudges are not. |
| PRD-079 | Return exactly five Explore Similar recommendations | important | full | Section 6.3 `POST /api/ai/explore/recommendations` concept recs (5) | |
| PRD-080 | Support full Alchemy loop with chaining | important | full | Phase 2 Alchemy picker to concepts to recs to chaining; Section 13 journey 8 | |
| PRD-081 | Clear downstream results when inputs change | important | missing | none | Backtracking invalidation for changed shows/concepts is not planned. |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | full | Section 2/A2: Alchemy generates 12 shared concepts with cap 8 | |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | full | Section 8.2 concept recommendation reason must name matching concepts | |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | partial | Section 8.5 taste context; Section 11 discovery quality rubric | Taste alignment is planned, but "surprise without betrayal" is not explicitly made an acceptance criterion. |
| PRD-085 | Keep one consistent AI persona across surfaces | important | full | Section 8.1 shared `basePersona.ts` composed by every prompt | |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | partial | Section 8.1 shared base persona; Section 11 AI quality rubric | The shared guardrails omit an explicit all-surface TV/movie-domain redirect rule. |
| PRD-087 | Make AI warm, joyful, and light in critique | important | full | Section 8.1 encodes joy-forward/warm and opinionated honesty | |
| PRD-088 | Structure Scoop as personal taste mini-review | important | full | Section 8.2 Scoop output includes take, stack-up, Scoop paragraph, fit, verdict | |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | full | Section 8.2 Ask contract responds like a friend in dialogue | |
| PRD-090 | Feed AI the right surface-specific context inputs | important | full | Section 8.2 surface inputs and Section 8.5 `buildTasteContext()` | |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | full | Section 11 AI quality golden set with real-show integrity non-negotiable | |
| PRD-092 | Show person gallery, name, and bio | important | full | Section 3.2 PersonDetail features `ImageGallery`, `Bio`; Phase 1 Person Detail | |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | full | Section 3.2 `AnalyticsCharts`; Phase 1 Person Detail analytics | |
| PRD-094 | Group filmography by year | important | full | Section 3.2 `FilmographyByYear`; Section 13 talent journey | |
| PRD-095 | Open Show Detail from selected credit | important | full | Section 13 journey 9: Person to credit to new Detail | |
| PRD-096 | Include font size and Search-on-launch settings | important | full | Section 5.2 `font_size`, `auto_search`; Section 6.4 settings route | |
| PRD-097 | Support username, model, and API-key settings safely | important | full | Section 5.2 user settings; Section 5.4 encrypted API-key handling | |
| PRD-098 | Export saved shows and My Data as zip | critical | full | Section 6.4 `GET /api/export` streams zip with saved subset and `user_shows` | |
| PRD-099 | Encode export dates using ISO-8601 | important | full | Section 6.4 "ISO-8601-dated JSON backup" | |

### 3. Coverage Scores

```
score = (full_count x 1.0 + partial_count x 0.5) / total_count x 100
```

Critical:  (29 x 1.0 + 1 x 0.5) / 30 x 100 = 98.3%  (29.5 of 30 critical requirements)
Important: (49 x 1.0 + 16 x 0.5) / 67 x 100 = 85.1%  (57 of 67 important requirements)
Detail:    (1 x 1.0 + 0 x 0.5) / 2 x 100 = 50.0%  (1 of 2 detail requirements)
Overall:   88.4% (99 total requirements)

### 4. Top Gaps

1. PRD-086 (`critical`) - Enforce shared AI guardrails across all surfaces.
   This matters because the shared persona layer is the control point for spoiler safety, domain boundaries, honesty, and specificity; without a complete shared guardrail contract, Ask, Scoop, Explore Similar, and Alchemy can drift inconsistently even if each surface has a prompt.

2. PRD-081 (`important`) - Clear downstream results when inputs change.
   This matters because stale concepts or recommendations after input changes would make Alchemy feel logically broken: users could see results for shows or ingredients they no longer selected.

3. PRD-077 (`important`) - Order concepts by strongest aha and varied axes.
   This matters because concepts are the core taste-control mechanism; if they are unordered or clustered around one axis, Explore Similar and Alchemy become generic recommendation flows rather than ingredient-driven discovery.

4. PRD-039 (`important`) - Keep Find/Discover in persistent primary navigation.
   This matters because discovery is a first-class use case; hiding it behind route availability rather than persistent navigation would reduce repeat access to Search, Ask, and Alchemy.

5. PRD-040 (`important`) - Keep Settings in persistent primary navigation.
   This matters because settings control identity-adjacent data, model/key configuration, readability, Search-on-launch, and export; making it non-persistent would make operational controls harder to find.

### 5. Coverage Narrative

#### Overall Posture

This is a structurally strong implementation plan with a few meaningful UX and AI-behavior holes. The backend architecture, namespace isolation, Supabase persistence model, collection business rules, and real-show AI resolution are specified with enough precision to implement and test. The weaker areas are not about whether the app can be built; they are about whether the built app will preserve the exact navigation affordances, detail-page composition, and concept-flow craft called out by the PRD.

#### Strength Clusters

The plan is strongest in Benchmark Runtime & Isolation, Collection Data & Persistence, Settings & Export, Person Detail, and the machine-readable parts of Ask Chat. It gives concrete schema sketches, route shapes, migration/reset mechanics, identity scoping, pure business-rule functions, AI output contracts, retry/fallback behavior, and test targets. These areas read like implementation-ready architecture rather than feature inventory.

#### Weakness Clusters

The gaps cluster around UI shell specificity and concept-system nuance. App Navigation & Discover Shell has routes and pages but not persistent primary navigation. Show Detail & Relationship UX has the right major sections but not exact section-order and toolbar-placement commitments. Concepts, Explore Similar & Alchemy covers counts and endpoints well, but misses ordering concepts by strongest "aha," varied axes, and clearing downstream results when inputs change.

#### Risk Assessment

If executed as-is, the most likely failure mode is a technically correct app that passes data and route tests but feels slightly off in product review. QA would likely notice stale Alchemy results after changing inputs, missing empty states, non-persistent nav access to Find/Settings, and detail-page controls appearing in acceptable but non-spec locations. AI quality would be mostly covered, but domain redirection and "surprise without betrayal" could vary by surface because they are not fully encoded as shared acceptance criteria.

#### Remediation Guidance

The remaining work is mostly planning specificity, not major architecture. Add a short UI shell section defining persistent primary navigation and empty states; add a Show Detail ordering contract that mirrors the narrative hierarchy; and expand the concept-system plan with generation ordering, varied-axis criteria, ingredient-picking guidance, and invalidation rules for changed inputs. The AI persona section should also absorb the full shared guardrail list, especially TV/movie-domain redirection, so every surface inherits it consistently.
