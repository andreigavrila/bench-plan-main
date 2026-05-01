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

##### Benchmark Runtime & Isolation

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

##### Collection Data & Persistence

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

##### App Navigation & Discover Shell

- PRD-038 | `important` | Provide filters panel and main screen destinations | `product_prd.md > 6. App Structure & Navigation`
- PRD-039 | `important` | Keep Find/Discover in persistent primary navigation | `product_prd.md > 6. App Structure & Navigation`
- PRD-040 | `important` | Keep Settings in persistent primary navigation | `product_prd.md > 6. App Structure & Navigation`
- PRD-041 | `important` | Offer Search, Ask, Alchemy discover modes | `product_prd.md > 6. App Structure & Navigation`

##### Collection Home & Search

- PRD-042 | `important` | Show only library items matching active filters | `product_prd.md > 7.1 Collection Home`
- PRD-043 | `important` | Group home into Active, Excited, Interested, Others | `product_prd.md > 7.1 Collection Home`
- PRD-044 | `important` | Support All, tag, genre, decade, score, media filters | `product_prd.md > 4.5 Filters (Ways to View the Collection)`
- PRD-045 | `important` | Render poster, title, and My Data badges | `product_prd.md > 7.1 Collection Home`
- PRD-046 | `detail` | Provide empty-library and empty-filter states | `product_prd.md > 7.1 Collection Home`
- PRD-047 | `important` | Search by title or keywords | `product_prd.md > 7.2 Search (Find → Search)`
- PRD-048 | `important` | Use poster grid with collection markers | `product_prd.md > 7.2 Search (Find → Search)`
- PRD-049 | `detail` | Auto-open Search when setting is enabled | `product_prd.md > 7.2 Search (Find → Search)`
- PRD-050 | `important` | Keep Search non-AI in tone | `supporting_docs/ai_voice_personality.md > 1. Persona Summary`

##### Show Detail & Relationship UX

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

##### Ask Chat

- PRD-065 | `important` | Provide conversational Ask chat interface | `product_prd.md > 7.3 Ask (Find → Ask)`
- PRD-066 | `important` | Answer directly with confident, spoiler-safe recommendations | `supporting_docs/discovery_quality_bar.md > 2.2 Ask / Explore Search Chat`
- PRD-067 | `important` | Show horizontal mentioned-shows strip from chat | `product_prd.md > 7.3 Ask (Find → Ask)`
- PRD-068 | `important` | Open Detail from mentions or Search fallback | `product_prd.md > 7.3 Ask (Find → Ask)`
- PRD-069 | `important` | Show six random starter prompts with refresh | `product_prd.md > 7.3 Ask (Find → Ask)`
- PRD-070 | `important` | Summarize older turns while preserving voice | `supporting_docs/ai_prompting_context.md > 4. Conversation Summarization (Chat Surfaces)`
- PRD-071 | `important` | Seed Ask-about-show sessions with show handoff | `product_prd.md > 7.3 Ask (Find → Ask)`
- PRD-072 | `critical` | Emit `commentary` plus exact `showList` contract | `supporting_docs/ai_prompting_context.md > 3.2 Ask with Mentions (Structured "Mentioned Shows")`
- PRD-073 | `important` | Retry malformed mention output once, then fallback | `supporting_docs/ai_prompting_context.md > 5. Guardrails & Fallbacks`
- PRD-074 | `important` | Redirect Ask back into TV/movie domain | `supporting_docs/ai_prompting_context.md > 1. Shared Rules (All AI Surfaces)`

##### Concepts, Explore Similar & Alchemy

- PRD-075 | `important` | Treat concepts as taste ingredients, not genres | `supporting_docs/concept_system.md > 1. What a Concept Is (User Definition)`
- PRD-076 | `important` | Return bullet-only, 1-3 word, non-generic concepts | `supporting_docs/ai_prompting_context.md > 3.4 Concepts (Single-Show and Multi-Show)`
- PRD-077 | `important` | Order concepts by strongest aha and varied axes | `supporting_docs/concept_system.md > 4. Generation Rules`
- PRD-078 | `important` | Require concept selection and guide ingredient picking | `supporting_docs/concept_system.md > 5. Selection UX Rules`
- PRD-079 | `important` | Return exactly five Explore Similar recommendations | `supporting_docs/concept_system.md > 6. Concepts → Recommendations Contract`
- PRD-080 | `important` | Support full Alchemy loop with chaining | `product_prd.md > 7.4 Alchemy (Find → Alchemy)`
- PRD-081 | `important` | Clear downstream results when inputs change | `product_prd.md > 7.4 Alchemy (Find → Alchemy)`
- PRD-082 | `important` | Generate shared multi-show concepts with larger option pool | `supporting_docs/concept_system.md > 8. Notes`
- PRD-083 | `important` | Cite selected concepts in concise recommendation reasons | `supporting_docs/concept_system.md > 6. Concepts → Recommendations Contract`
- PRD-084 | `important` | Deliver surprising but defensible taste-aligned recommendations | `supporting_docs/discovery_quality_bar.md > 1.2 Taste Alignment`

##### AI Voice, Persona & Quality

- PRD-085 | `important` | Keep one consistent AI persona across surfaces | `supporting_docs/ai_voice_personality.md > 1. Persona Summary`
- PRD-086 | `critical` | Enforce shared AI guardrails across all surfaces | `supporting_docs/ai_prompting_context.md > 1. Shared Rules (All AI Surfaces)`
- PRD-087 | `important` | Make AI warm, joyful, and light in critique | `supporting_docs/ai_voice_personality.md > 2. Non-Negotiable Voice Pillars`
- PRD-088 | `important` | Structure Scoop as personal taste mini-review | `supporting_docs/ai_voice_personality.md > 4.1 Scoop (Show Detail "The Scoop")`
- PRD-089 | `important` | Keep Ask brisk and dialogue-like by default | `supporting_docs/ai_voice_personality.md > 4.2 Ask (Find → Ask)`
- PRD-090 | `important` | Feed AI the right surface-specific context inputs | `supporting_docs/ai_prompting_context.md > 2. Shared Inputs (Typical)`
- PRD-091 | `important` | Validate discovery with rubric and hard-fail integrity | `supporting_docs/discovery_quality_bar.md > 4. Scoring Rubric (Quick)`

##### Person Detail

- PRD-092 | `important` | Show person gallery, name, and bio | `product_prd.md > 7.6 Person Detail Page`
- PRD-093 | `important` | Include ratings, genres, and projects-by-year analytics | `product_prd.md > 7.6 Person Detail Page`
- PRD-094 | `important` | Group filmography by year | `product_prd.md > 7.6 Person Detail Page`
- PRD-095 | `important` | Open Show Detail from selected credit | `product_prd.md > 7.6 Person Detail Page`

##### Settings & Export

- PRD-096 | `important` | Include font size and Search-on-launch settings | `product_prd.md > 7.7 Settings & Your Data`
- PRD-097 | `important` | Support username, model, and API-key settings safely | `product_prd.md > 7.7 Settings & Your Data`
- PRD-098 | `critical` | Export saved shows and My Data as zip | `product_prd.md > 7.7 Settings & Your Data`
- PRD-099 | `important` | Encode export dates using ISO-8601 | `product_prd.md > 7.7 Settings & Your Data`

Total: 99 requirements (30 critical, 67 important, 2 detail) across 10 functional areas

### 2. Coverage Table

| PRD-ID | Requirement | Severity | Coverage | Evidence | Gap |
| ------ | ----------- | -------- | -------- | -------- | --- |
| PRD-001 | Use Next.js latest stable runtime | critical | full | `2. Infrastructure & Execution Architecture` - "`Stack`: Next.js (latest stable)" | |
| PRD-002 | Use Supabase official client libraries | critical | full | `2. Infrastructure & Execution Architecture` - "`Persistence Layer`: Supabase ... official client SDKs" | |
| PRD-003 | Ship `.env.example` with required variables | critical | partial | `2. Infrastructure & Execution Architecture` - "Secretless execution using a standard `.env.example` skeleton" | The plan commits to an `.env.example` file but does not enumerate the required variables or comments. |
| PRD-004 | Ignore `.env*` secrets except example | important | missing | none | The plan never mentions `.gitignore` rules for excluding `.env*` secrets while preserving `.env.example`. |
| PRD-005 | Configure build through env without code edits | critical | partial | `2. Infrastructure & Execution Architecture` - "Secretless execution using a standard `.env.example` skeleton" | The plan implies env-driven setup but never states that builds run without source edits. |
| PRD-006 | Keep secrets out of repo and server-only | critical | partial | `2. Infrastructure & Execution Architecture` - "platform is designed to run ... securely" and `.env.example` skeleton | Security intent is present, but the plan does not define repo-secret exclusion or server-only handling for elevated keys. |
| PRD-007 | Provide app, test, reset command scripts | critical | full | `2. Infrastructure & Execution Architecture` - "`npm run dev`, `npm test`, `npm run test:reset`" | |
| PRD-008 | Include repeatable schema evolution artifacts | critical | missing | none | The plan describes models but never proposes migrations or another repeatable schema-definition artifact. |
| PRD-009 | Use one stable namespace per build | critical | full | `2. Infrastructure & Execution Architecture` - "`namespace_id`: Every execution, test, or local run operates explicitly in an isolated namespace partition" | |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | `2. Infrastructure & Execution Architecture` and `6. Implementation Stages & Build Steps` - "`test:reset`" for isolated cleanup testing | |
| PRD-011 | Attach every user record to `user_id` | critical | full | `2. Infrastructure & Execution Architecture` - "`user_id`: An opaque, stable identifier used to scope user-owned information" | |
| PRD-012 | Partition persisted data by namespace and user | critical | full | `3. Data Model Schema (Supabase)` - "Partitioned by combination of `(namespace_id, user_id, id)`" and settings scoped by `(namespace_id, user_id)` | |
| PRD-013 | Support documented dev auth injection, prod-gated | important | partial | `2. Infrastructure & Execution Architecture` - "header-based injection ... or local dev-mode selectors" | The plan names dev auth injection paths but does not say they will be documented or gated out of production. |
| PRD-014 | Real OAuth later needs no schema redesign | important | partial | `2. Infrastructure & Execution Architecture` - opaque `user_id` and no benchmark OAuth requirement | The identity model points in the right direction, but the plan does not explicitly preserve a no-schema-redesign migration path to real OAuth. |
| PRD-015 | Keep backend as persisted source of truth | critical | full | `3. Data Model Schema (Supabase)` - "Backend-as-SSOT (Single Source of Truth)" | |
| PRD-016 | Make client cache safe to discard | critical | partial | `3. Data Model Schema (Supabase)` - "Backend-as-SSOT (Single Source of Truth)" | Backend SSOT is stated, but the plan never calls out disposable local cache or safe storage clearing/reinstall behavior. |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | missing | none | The plan never states that Docker is optional or unnecessary for benchmark execution. |
| PRD-018 | Overlay saved user data on every show appearance | critical | partial | `1. Project Overview & Objectives` - "catalog integration ... seamlessly merged with local data" | The plan captures merge intent but does not require overlaid user data everywhere shows appear. |
| PRD-019 | Support visible statuses plus hidden `Next` | important | missing | none | The status list omits the hidden `Next` state entirely. |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | full | `4. Application Layout & Routing (Next.js)` - "Excited (Later + Excited interest)" and "Interested (Later + Interested interest)" | |
| PRD-021 | Support free-form multi-tag personal tag library | important | partial | `1. Project Overview & Objectives` - "Flexible, free-form user tags" | The plan supports free-form tags but does not define the persistent personal tag library behavior around them. |
| PRD-022 | Define collection membership by assigned status | critical | partial | `1. Project Overview & Objectives` - "collection grouped by distinct statuses" | Statuses are central to the plan, but membership-by-status is not defined as the authoritative collection rule. |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | partial | `6. Implementation Stages & Build Steps` and `1. Project Overview & Objectives` - status, tags, and rating are planned | The plan includes the surfaces, but it does not spell out the save triggers for each action. |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | missing | none | The plan never defines the default save state or the rating-triggered `Done` exception. |
| PRD-025 | Removing status deletes show and all My Data | critical | missing | none | The plan does not specify destructive removal semantics for clearing status and wiping related user data. |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | full | `3. Data Model Schema (Supabase)` - "Re-adding or updating a show fetches public metadata ... without destroying user modifications" | |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | `3. Data Model Schema (Supabase)` - "Each user-owned field possesses a corresponding `UpdateDate`" | |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | partial | `3. Data Model Schema (Supabase)` - "`UpdateDate` to resolve synchronization collisions" | Timestamps are used for sync conflict handling, but sorting and freshness uses are not planned explicitly. |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | partial | `4. Application Layout & Routing (Next.js)` - "`The Scoop` ... cache-busting roughly every ~4 hours" | The freshness window is covered, but the saved-shows-only persistence rule is absent. |
| PRD-030 | Keep Ask and Alchemy state session-only | important | missing | none | The plan does not specify that Ask and Alchemy histories/results are non-persistent session state. |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | full | `4. Application Layout & Routing (Next.js)` - Ask parser `Title::externalId::mediaType`; `5. AI Services & Discovery Ecology` - "resolving strictly to valid data nodes" | |
| PRD-032 | Show collection and rating tile indicators | important | missing | none | The plan never defines in-collection or rating badges for tiles. |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | partial | `3. Data Model Schema (Supabase)` - user data conflicts resolved by `*UpdateDate` comparisons | Conflict-resolution intent exists, but duplicate detection/merge and cross-device consistency are not described. |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | missing | none | Metadata versioning is mentioned, but there is no upgrade-continuity plan for existing saved libraries and My Data. |
| PRD-035 | Persist synced settings, local settings, UI state | important | partial | `3. Data Model Schema (Supabase)` - settings capture cloud settings, keys, theme toggles, and metadata versioning | The plan covers some synced settings, but it omits the full local-settings and UI-state persistence contract. |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | missing | none | The plan does not address provider-ID persistence or the transient nature of detail-only fetches. |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | full | `3. Data Model Schema (Supabase)` - "`selectFirstNonEmpty`" merge and `*UpdateDate` conflict handling | |
| PRD-038 | Provide filters panel and main screen destinations | important | partial | `4. Application Layout & Routing (Next.js)` - routes for `/`, `/search`, `/ask`, `/alchemy`, `/detail`, `/person`, `/settings` | The plan defines destinations, but it does not specify the filters/navigation panel shell. |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | partial | `4. Application Layout & Routing (Next.js)` - explicit `/search`, `/ask`, and `/alchemy` routes | Discover destinations exist, but persistence in primary navigation is not planned. |
| PRD-040 | Keep Settings in persistent primary navigation | important | partial | `4. Application Layout & Routing (Next.js)` - explicit `/settings` route | The settings destination exists, but persistent primary-navigation placement is unspecified. |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | `4. Application Layout & Routing (Next.js)` - `/search`, `/ask`, and `/alchemy` | |
| PRD-042 | Show only library items matching active filters | important | full | `4. Application Layout & Routing (Next.js)` - "Dynamic filtering capability (Tags, Genres, Media Type toggles)" | |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | `4. Application Layout & Routing (Next.js)` - grouped explicitly into Active, Excited, Interested, and a collapsed other-status block | |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | partial | `4. Application Layout & Routing (Next.js)` - "Tags, Genres, Media Type toggles" | The plan covers some filters but omits explicit decade, community-score, and `All` filter handling. |
| PRD-045 | Render poster, title, and My Data badges | important | missing | none | The plan never specifies tile contents or My Data badge rendering. |
| PRD-046 | Provide empty-library and empty-filter states | detail | missing | none | Empty states are not mentioned for either an empty library or an empty filtered view. |
| PRD-047 | Search by title or keywords | important | partial | `4. Application Layout & Routing (Next.js)` - "`/search` ... external content catalog allowing user-initiated curation" | Search is planned at a high level, but title/keyword query behavior is not explicit. |
| PRD-048 | Use poster grid with collection markers | important | missing | none | The search route exists, but the poster-grid presentation and collection markers are not planned. |
| PRD-049 | Auto-open Search when setting is enabled | detail | missing | none | The plan omits the Search-on-launch behavior entirely. |
| PRD-050 | Keep Search non-AI in tone | important | partial | `4. Application Layout & Routing (Next.js)` - "`/search` ... direct proxy UI for the external content catalog" | The route reads as a non-AI search surface, but the plan never states the tone rule explicitly. |
| PRD-051 | Preserve Show Detail narrative section order | important | missing | none | The plan lists some detail-page features but does not preserve or specify the required narrative section order. |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | missing | none | Header media is not described, so neither trailer-first presentation nor fallback behavior is planned. |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | missing | none | The plan does not say these core facts appear early in the Detail experience. |
| PRD-054 | Place status/interest controls in toolbar | important | missing | none | Status controls are mentioned generically, but their required toolbar placement is absent. |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | missing | none | The plan includes tags but never defines the tag-to-save auto-save rule. |
| PRD-056 | Auto-save unsaved rated show as Done | critical | missing | none | Rating exists in the plan, but the rating-triggered save-as-`Done` behavior is not specified. |
| PRD-057 | Show overview early for fast scanning | important | missing | none | The Detail plan never places the overview early or frames it as a first-scan element. |
| PRD-058 | Scoop shows correct states and progressive feedback | important | partial | `4. Application Layout & Routing (Next.js)` - "Streaming generation for `The Scoop`" | Progressive loading is planned, but the no-scoop/cached/open state contract is missing. |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | missing | none | The plan has Ask and Detail surfaces, but no show-handoff or seeded-context behavior between them. |
| PRD-060 | Include traditional recommendations strand | important | full | `4. Application Layout & Routing (Next.js)` - "Component strands for Similar items" | |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | partial | `4. Application Layout & Routing (Next.js)` - "Interactive `Get Concepts` discovery gateway" | The entry CTA is named, but the required CTA-first concept-selection flow is not fully planned. |
| PRD-062 | Include streaming availability and person-linking credits | important | partial | `4. Application Layout & Routing (Next.js)` - "Person/Crew horizontal profiles" | The person-linking credit strand is present, but streaming-availability coverage is missing. |
| PRD-063 | Gate seasons to TV and financials to movies | important | partial | `4. Application Layout & Routing (Next.js)` - "Component strands for ... Seasons" | The plan includes seasons, but it does not define media-type gating or movie financials. |
| PRD-064 | Keep primary actions early and page not overwhelming | important | missing | none | The plan lacks any information architecture guidance about early actions or avoiding an overloaded Detail page. |
| PRD-065 | Provide conversational Ask chat interface | important | full | `4. Application Layout & Routing (Next.js)` - "`/ask` ... Conversational chat UI" | |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | partial | `5. AI Services & Discovery Ecology` - "opinionated, concise, and spoiler-safe" | The plan captures tone and safety, but it does not define direct-answer behavior for recommendation responses. |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | partial | `4. Application Layout & Routing (Next.js)` - "Inline `Mentioned Shows` extraction parser" | Mention parsing is covered, but the required horizontal UI strip is not. |
| PRD-068 | Open Detail from mentions or Search fallback | important | missing | none | The plan never specifies interaction behavior for mentioned shows or the Search fallback path. |
| PRD-069 | Show six random starter prompts with refresh | important | missing | none | Starter prompts and refresh behavior are not planned for Ask. |
| PRD-070 | Summarize older turns while preserving voice | important | partial | `5. AI Services & Discovery Ecology` - "Automatically summarizes history roughly every ~10 segments" | Summarization is planned, but the requirement to preserve persona/voice through summaries is not. |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | missing | none | The plan does not define the Ask-about-show entry variant or its show-context handoff. |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | partial | `4. Application Layout & Routing (Next.js)` - "`Title::externalId::mediaType`" mention parser | The string format is referenced, but the exact `commentary` + `showList` structured contract is not specified. |
| PRD-073 | Retry malformed mention output once, then fallback | important | missing | none | Ask fallback/retry behavior for malformed mention output is absent. |
| PRD-074 | Redirect Ask back into TV/movie domain | important | partial | `4. Application Layout & Routing (Next.js)` - "Conversational chat UI resolving context over TV/Movies" | The surface is in-domain, but the redirect-back guardrail for off-domain prompts is not described. |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | full | `1. Project Overview & Objectives` - "conceptual ingredients" and `5. AI Services & Discovery Ecology` concept pipeline | |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | partial | `5. AI Services & Discovery Ecology` - "1-3 word bulleted abstractions" | The plan covers bullet-only short concepts, but it does not prevent generic outputs. |
| PRD-077 | Order concepts by strongest aha and varied axes | important | missing | none | The plan never addresses concept ordering quality or diversity across axes. |
| PRD-078 | Require concept selection and guide ingredient picking | important | partial | `4. Application Layout & Routing (Next.js)` - "Select Catalyst Concepts" and `Get Concepts` gateway | Concept selection exists, but there is no guidance around "pick the ingredients you want more of" or explicit requirement gating. |
| PRD-079 | Return exactly five Explore Similar recommendations | important | missing | none | Explore Similar is planned, but the exact five-recommendation contract is missing. |
| PRD-080 | Support full Alchemy loop with chaining | important | partial | `4. Application Layout & Routing (Next.js)` - "multi-step blending wizard" | The main Alchemy flow is present, but the chaining/"More Alchemy" loop is not. |
| PRD-081 | Clear downstream results when inputs change | important | missing | none | The plan does not specify clearing concepts/results when source selections change. |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | partial | `5. AI Services & Discovery Ecology` - "user-supplied combinations to isolate specific overlapping concepts" | Shared concept generation is implied, but the larger multi-show option pool is not planned. |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | full | `5. AI Services & Discovery Ecology` - "1-3 sentence rationales tied to concepts" | |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | partial | `1. Project Overview & Objectives` - "AI discovery driven by user's personal tastes" | Taste-aware intent exists, but the plan never sets a quality bar around surprising yet defensible recommendations. |
| PRD-085 | Keep one consistent AI persona across surfaces | important | full | `5. AI Services & Discovery Ecology` - "The AI layer maintains consistent persona requirements" | |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | partial | `5. AI Services & Discovery Ecology` - "warm ... opinionated, concise, and spoiler-safe" | Some shared guardrails are named, but the full cross-surface guardrail set is not planned as an enforced contract. |
| PRD-087 | Make AI warm, joyful, and light in critique | important | partial | `5. AI Services & Discovery Ecology` - "warm ... opinionated, concise, and spoiler-safe" | Warmth is covered, but joy-forward tone and lightness in critique are not explicit. |
| PRD-088 | Structure Scoop as personal taste mini-review | important | full | `5. AI Services & Discovery Ecology` - "`The Scoop` ... strong subjective stances, fit-warnings, and a core conversational recommendation paragraph" | |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | full | `5. AI Services & Discovery Ecology` - "Ask (Conversational Engine)" plus "concise" persona requirement | |
| PRD-090 | Feed AI the right surface-specific context inputs | important | partial | `5. AI Services & Discovery Ecology` - Ask uses the user's library and Alchemy uses user-supplied combinations | The plan references some context inputs, but it does not define the full surface-specific context contracts. |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | missing | none | No validation rubric, scoring pass, or hard-fail integrity check is planned for AI discovery quality. |
| PRD-092 | Show person gallery, name, and bio | important | partial | `4. Application Layout & Routing (Next.js)` - "Person-focused insights: bios, credits, and lightweight analytics widgets" | Bio coverage exists, but the gallery/name presentation is not specified. |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | partial | `4. Application Layout & Routing (Next.js)` - "lightweight analytics widgets" | Analytics are planned generically, but ratings/genres/projects-by-year are not enumerated. |
| PRD-094 | Group filmography by year | important | missing | none | The plan mentions credits, but not year-grouped filmography. |
| PRD-095 | Open Show Detail from selected credit | important | full | `4. Application Layout & Routing (Next.js)` - person page analytics "mapping back to `/detail`" | |
| PRD-096 | Include font size and Search-on-launch settings | important | missing | none | The settings plan omits both font-size and Search-on-launch controls. |
| PRD-097 | Support username, model, and API-key settings safely | important | partial | `4. Application Layout & Routing (Next.js)` - "AI selection, API Key injections" | Model and key settings are covered, but username and safe handling expectations are not fully planned. |
| PRD-098 | Export saved shows and My Data as zip | critical | full | `4. Application Layout & Routing (Next.js)` - "robust ZIP/JSON `Export My Data` functions" | |
| PRD-099 | Encode export dates using ISO-8601 | important | missing | none | The export format is planned at a high level, but ISO-8601 date encoding is not specified. |

### 3. Coverage Scores

Critical:  (14 x 1.0 + 10 x 0.5) / 30 x 100 = 63.33%  (19 of 30 critical requirements)
Important: (11 x 1.0 + 30 x 0.5) / 67 x 100 = 38.81%  (26 of 67 important requirements)
Detail:    (0 x 1.0 + 0 x 0.5) / 2 x 100 = 0.00%  (0 of 2 detail requirements)
Overall:   (25 x 1.0 + 40 x 0.5) / 99 x 100 = 45.45%  (45 of 99 total requirements)

### 4. Top Gaps

- `PRD-008` | `critical` | Include repeatable schema evolution artifacts. Without migrations or an equivalent repeatable schema mechanism, the build cannot guarantee deterministic fresh environments or benchmark resets.
- `PRD-025` | `critical` | Removing status deletes show and all My Data. This is a core collection-state contract; if it is implemented ad hoc, users can end up with orphaned tags/ratings/scoop data or destructive behavior that does not match the product model.
- `PRD-034` | `critical` | Preserve saved libraries across data-model upgrades. The plan has no continuity strategy, so a schema change could silently lose or corrupt the user's saved library during upgrades.
- `PRD-024` | `critical` | Default save to Later/Interested except rating-save Done. These defaults govern multiple primary journeys, and without them the same action can produce inconsistent collection states across surfaces.
- `PRD-055` | `critical` | Auto-save unsaved tagged show as Later/Interested. Tagging is one of the core save entry points; omitting this rule breaks the "tag-to-save" journey and makes Detail interactions inconsistent with the PRD.

### 5. Coverage Narrative

#### Overall Posture

This is a structurally sound plan with concerning holes. It covers the benchmark stack, isolation model, top-level routes, and the high-level AI architecture, but it leaves many product-behavior contracts unspecified, especially the collection-state rules and the detailed Detail-page interaction model.

#### Strength Clusters

The plan is strongest in `Benchmark Runtime & Isolation`, where it clearly commits to Next.js, Supabase, namespace isolation, `user_id` scoping, backend source-of-truth semantics, and reset scripts. It is also reasonably strong in `AI Voice, Persona & Quality` and the high-level discover surfaces, where it establishes a consistent persona, conversational Ask, concept generation, and concept-linked recommendation reasoning.

#### Weakness Clusters

The gaps cluster heavily in `Show Detail & Relationship UX` and `Collection Data & Persistence`. The plan repeatedly names surfaces and data fields without locking down the behavioral contracts that make them correct: auto-save defaults, removal semantics, session-only AI state, tile indicators, Detail-page ordering, toolbar placement, and specific save triggers. A secondary weakness cluster appears in `Ask Chat` and `Settings & Export`, where the plan has the shell of the features but omits fallback contracts, starter states, and specific setting/export requirements.

#### Risk Assessment

If this plan were executed as-is, the most likely outcome is a technically credible app shell that still fails acceptance because collection behavior is inconsistent. A QA reviewer would probably notice first that rating, tagging, status changes, and removal do not deterministically save or clear data the way the PRD requires, and that the Detail page lacks the prescribed hierarchy and early-action layout that ties the product experience together.

#### Remediation Guidance

The plan needs more behavioral specification and acceptance criteria, not just more implementation steps. Add explicit planning sections for collection state transitions, save/remove defaults, Detail-page information architecture, Ask output/fallback contracts, Explore Similar/Alchemy flow contracts, and repo/runtime deliverables such as migrations, Docker-free execution, and upgrade continuity guarantees.
