## 1. Requirements Extraction

### Pass 1: Identify Functional Areas

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

### Pass 2: Extract Requirements Within Each Area

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
- PRD-047 | `important` | Search by title or keywords | `product_prd.md > 7.2 Search (Find → Search)`
- PRD-048 | `important` | Use poster grid with collection markers | `product_prd.md > 7.2 Search (Find → Search)`
- PRD-049 | `detail` | Auto-open Search when setting is enabled | `product_prd.md > 7.2 Search (Find → Search)`
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

#### Concepts, Explore Similar & Alchemy
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

#### AI Voice, Persona & Quality
- PRD-085 | `important` | Keep one consistent AI persona across surfaces | `supporting_docs/ai_voice_personality.md > 1. Persona Summary`
- PRD-086 | `critical` | Enforce shared AI guardrails across all surfaces | `supporting_docs/ai_prompting_context.md > 1. Shared Rules (All AI Surfaces)`
- PRD-087 | `important` | Make AI warm, joyful, and light in critique | `supporting_docs/ai_voice_personality.md > 2. Non-Negotiable Voice Pillars`
- PRD-088 | `important` | Structure Scoop as personal taste mini-review | `supporting_docs/ai_voice_personality.md > 4.1 Scoop (Show Detail "The Scoop")`
- PRD-089 | `important` | Keep Ask brisk and dialogue-like by default | `supporting_docs/ai_voice_personality.md > 4.2 Ask (Find → Ask)`
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

## 2. Coverage Table

| PRD-ID | Requirement | Severity | Coverage | Evidence | Gap |
| ------ | ----------- | -------- | -------- | -------- | --- |
| PRD-001 | Use Next.js latest stable runtime | critical | partial | 2. Technical Stack & Architecture - "Framework: Next.js (App Router)" | The plan names Next.js but does not commit to the latest stable release policy. |
| PRD-002 | Use Supabase official client libraries | critical | partial | 2. Technical Stack & Architecture - "Persistence: Supabase for relational data storage" | The plan selects Supabase but never specifies the official client libraries. |
| PRD-003 | Ship `.env.example` with required variables | critical | missing | none | The plan never commits to shipping a `.env.example` or enumerating required variables. |
| PRD-004 | Ignore `.env*` secrets except example | important | missing | none | The plan does not mention repo ignore rules for `.env` secrets. |
| PRD-005 | Configure build through env without code edits | critical | partial | 2. Technical Stack & Architecture - `src/config/` is described as "Environment variables, constants, API endpoints" | It references environment variables, but it does not state that the app must be fully configurable without source edits. |
| PRD-006 | Keep secrets out of repo and server-only | critical | partial | 2. Technical Stack & Architecture - "AI Integration ... via server-side routes" | Server-side AI routes are noted, but repo secret handling and client/server key boundaries are not specified. |
| PRD-007 | Provide app, test, reset command scripts | critical | partial | 6. Implementation Phases - Phase 5: "Implement namespace reset scripts for benchmark testing" | Reset scripting is planned, but start and test command scripts are not called out. |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | 6. Implementation Phases - Phase 1: "Define migrations for `shows` and `settings`" |  |
| PRD-009 | Use one stable namespace per build | critical | full | 3. Data Model & Persistence - "Every build/run will be assigned a `namespace_id`" |  |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | partial | 3. Data Model & Persistence and 6. Phase 5 - namespace-scoped queries plus reset scripts | The plan covers isolation and reset tooling separately, but it never states that destructive resets are scoped only to a namespace. |
| PRD-011 | Attach every user record to `user_id` | critical | partial | 3. Data Model & Persistence - both `shows` and `settings` include `user_id` | The core tables include `user_id`, but the plan does not state that every user-owned record must follow that rule. |
| PRD-012 | Partition persisted data by namespace and user | critical | partial | 3. Data Model & Persistence - `shows` and `settings` carry `user_id` and `namespace_id` | The schema sketches both keys, but the partitioning rule for all persisted data is not made explicit. |
| PRD-013 | Support documented dev auth injection, prod-gated | important | partial | 6. Implementation Phases - Phase 1: "Implement `theme` tokens and `X-User-Id` injection" | It plans dev identity injection, but it does not document the mechanism or state how production mode disables it. |
| PRD-014 | Real OAuth later needs no schema redesign | important | partial | 3. Data Model & Persistence - `user_id` is modeled as an ownership field, not an OAuth-specific ID | The schema direction is compatible with later OAuth, but the plan does not explicitly protect against auth-driven schema redesign. |
| PRD-015 | Keep backend as persisted source of truth | critical | full | 7. Success & Compliance - "Server-side Supabase as the single source of truth" |  |
| PRD-016 | Make client cache safe to discard | critical | partial | 7. Success & Compliance - "Server-side Supabase as the single source of truth" | This implies disposable client state, but the plan never states that clearing local caches must be safe. |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | missing | none | The plan never states Docker is optional or avoided for benchmark runs. |
| PRD-018 | Overlay saved user data on every show appearance | critical | partial | 3. Data Model & Persistence - "`shows` stores public catalog data + user overlay" | The overlay model is present, but the plan never requires every list and recommendation surface to render the overlaid version. |
| PRD-019 | Support visible statuses plus hidden `Next` | important | missing | none | The status model omits the hidden `Next` state entirely. |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | partial | 3. Data Model & Persistence - `my_status` and `my_interest`; 4.2 Collection Home groups Excited and Interested | It acknowledges interest as separate data, but it does not explicitly define Interested and Excited chips as Later + interest mappings. |
| PRD-021 | Support free-form multi-tag personal tag library | important | partial | 3. Data Model & Persistence - `my_tags` array; 1. Project Overview mentions free-form tags | Tags exist, but the plan does not describe the emergent personal tag library or multi-tag behavior. |
| PRD-022 | Define collection membership by assigned status | critical | partial | 4.2 Core Features - Collection Home uses status-based grouping | Status-centric library behavior is implied, but the plan never defines collection membership as "has an assigned status." |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | partial | 6. Implementation Phases - Phase 2: "Implement 'Auto-save' and 'Removal confirmation' logic" | Auto-save is planned, but the trigger matrix for status, interest, rating, and tagging is not spelled out. |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | partial | 6. Implementation Phases - Phase 2: "Implement 'Auto-save' and 'Removal confirmation' logic" | Default save behavior is mentioned only generically, without explicit Later/Interested and rating-to-Done rules. |
| PRD-025 | Removing status deletes show and all My Data | critical | partial | 6. Implementation Phases - Phase 2: "Implement 'Auto-save' and 'Removal confirmation' logic" | Removal confirmation is planned, but the plan does not say removal clears the show and all My Data fields. |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | missing | none | The plan never covers re-adding a previously saved show, timestamp-based merge, or metadata refresh behavior. |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | 3. Data Model & Persistence - "`*_update_date`: Timestamps for all user-editable fields" |  |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | partial | 3. Data Model & Persistence - "`*_update_date`: Timestamps for all user-editable fields" | Timestamps are modeled, but the plan does not allocate work for sort, sync, and freshness policies that consume them. |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | partial | 3. Data Model & Persistence - `ai_scoop` field; 4.2 Show Detail has progressive Scoop streaming | Scoop storage and streaming are planned, but the saved-only persistence rule and 4-hour freshness window are not specified. |
| PRD-030 | Keep Ask and Alchemy state session-only | important | missing | none | The plan does not define Ask or Alchemy state as session-only or disposable on exit. |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | partial | 5. AI Service Strategy - "strict mapping rules to ensure discovery is actionable" | Actionable mapping is a goal, but the plan does not define resolution behavior, deterministic matching, or fallback when mapping fails. |
| PRD-032 | Show collection and rating tile indicators | important | partial | 3. Data Model & Persistence - user overlay model; 2. Technical Stack & Architecture lists `PosterGrid` | Tiles are implied, but the plan never explicitly requires collection and rating indicators on them. |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | missing | none | Cross-device sync, duplicate merging, and per-field conflict resolution are absent from the implementation phases. |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | missing | none | The plan never addresses preserving user libraries across schema or data-model upgrades. |
| PRD-035 | Persist synced settings, local settings, UI state | important | partial | 3. Data Model & Persistence - `settings` entity with `user_name`, `catalog_api_key`, `ai_api_key`, `ai_model` | Synced settings are sketched, but local settings and persisted UI state are not planned. |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | missing | none | The plan does not mention persisted provider IDs or the transient-only detail fetch boundary. |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | partial | 3. Data Model & Persistence - `catalog_data` plus `*_update_date` fields | The schema carries the ingredients, but the plan never defines the non-empty merge policy or timestamp resolution rules. |
| PRD-038 | Provide filters panel and main screen destinations | important | full | 2. Technical Stack & Architecture - top-level routes plus 4.2 Collection Home sidebar filters |  |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | partial | 2. Technical Stack & Architecture - `Find/` is a top-level page | Find exists structurally, but the plan never says it is persistent primary navigation. |
| PRD-040 | Keep Settings in persistent primary navigation | important | partial | 2. Technical Stack & Architecture - `Settings/` is a top-level page | Settings exists structurally, but persistent primary navigation is not specified. |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | 4.2 Core Features - Find/Discover Hub with Search, Ask, and Alchemy |  |
| PRD-042 | Show only library items matching active filters | important | partial | 4.2 Core Features - Collection Home has a "Sidebar for Tag and Data filters" | Filtering is planned, but the plan does not explicitly require the home view to show only items matching active filters. |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | 4.2 Core Features - "Dynamic grouping by status: Active (hero), Excited, Interested, and Collapsed Others" |  |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | partial | 4.2 Core Features - Collection Home has a "Sidebar for Tag and Data filters" | The plan mentions tag and data filtering, but it does not enumerate All, genre, decade, score-range, and media-type coverage. |
| PRD-045 | Render poster, title, and My Data badges | important | partial | 2. Technical Stack & Architecture - shared `PosterGrid`; 3. Data Model & Persistence - user overlay model | The basic tile ingredients are implied, but the plan never explicitly commits to poster, title, and My Data badges on home tiles. |
| PRD-046 | Provide empty-library and empty-filter states | detail | missing | none | Empty-library and empty-filter states are not mentioned. |
| PRD-047 | Search by title or keywords | important | partial | 4.2 Core Features - "Search: Direct external catalog query" | Search is planned, but title and keyword semantics are not defined. |
| PRD-048 | Use poster grid with collection markers | important | partial | 2. Technical Stack & Architecture - shared `PosterGrid`; 4.2 Core Features - Search route | A poster-grid component exists architecturally, but Search does not explicitly promise poster-grid results with collection markers. |
| PRD-049 | Auto-open Search when setting is enabled | detail | missing | none | The Search-on-launch behavior is not planned anywhere. |
| PRD-050 | Keep Search non-AI in tone | important | partial | 4.2 Core Features - Search is separated from Ask and Alchemy as a direct catalog mode | The plan separates Search from AI modes, but it never states the surface must stay non-AI in voice and tone. |
| PRD-051 | Preserve Show Detail narrative section order | important | missing | none | The plan never preserves or references the required section order for the Detail page narrative. |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | partial | 4.2 Core Features - "Immersive header with trailers (inline playback) and cinematic media" | Motion-rich header behavior is planned, but graceful non-trailer fallback is not described. |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | missing | none | The plan does not specify early placement of year, runtime/seasons, and community score. |
| PRD-054 | Place status/interest controls in toolbar | important | partial | 4.2 Core Features - "Toolbar for 'One-tap' status updates" | Toolbar status controls are planned, but interest controls are not explicitly included there. |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | partial | 6. Implementation Phases - Phase 2: auto-save logic plus status, rating, and tags controls | Tag-triggered auto-save is implied, but the exact Later + Interested default is not stated. |
| PRD-056 | Auto-save unsaved rated show as Done | critical | partial | 6. Implementation Phases - Phase 2: auto-save logic plus status, rating, and tags controls | Rating-triggered auto-save is implied, but the plan never explicitly says unsaved ratings save as Done. |
| PRD-057 | Show overview early for fast scanning | important | missing | none | Overview placement and fast-scan intent are not covered. |
| PRD-058 | Scoop shows correct states and progressive feedback | important | partial | 4.2 Core Features - "Progressive streaming for 'The Scoop'" | Progressive Scoop loading is covered, but toggle states, cached-state copy, and feedback states are not. |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | missing | none | The plan does not mention an Ask-about-this-show CTA or seeded Ask context from Detail. |
| PRD-060 | Include traditional recommendations strand | important | missing | none | Traditional non-AI recommendations are not planned on the Detail page. |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | partial | 6. Implementation Phases - Phase 3: "Implement per-show 'Explore Similar' (Concepts -> Recs)" | The feature exists, but the CTA-first flow of Get Concepts -> select -> Explore Shows is not spelled out. |
| PRD-062 | Include streaming availability and person-linking credits | important | missing | none | Streaming availability and cast/crew links into Person Detail are not explicitly included. |
| PRD-063 | Gate seasons to TV and financials to movies | important | missing | none | TV-only seasons and movie-only financials are not addressed. |
| PRD-064 | Keep primary actions early and page not overwhelming | important | partial | 4.2 Core Features - Show Detail focuses on header, toolbar, and Scoop first | The plan hints at early primary actions, but it does not define the clutter-management or sequencing rule for the full page. |
| PRD-065 | Provide conversational Ask chat interface | important | full | 4.2 Core Features - "Ask: Chat interface returning structured objects" |  |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | partial | 5. AI Service Strategy - "Ask: Conversational, picks favorites, spoiler-safe by default" | Tone and spoiler safety are covered, but the direct-answer quality bar is not explicit. |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | 6. Implementation Phases - Phase 3: "Build 'Ask' chat interface with mentioned-shows row" |  |
| PRD-068 | Open Detail from mentions or Search fallback | important | partial | 6. Implementation Phases - Phase 3: mentioned-shows row | The row is planned, but the open-Detail behavior and Search fallback are not specified. |
| PRD-069 | Show six random starter prompts with refresh | important | missing | none | Starter prompts and prompt-refresh behavior are absent. |
| PRD-070 | Summarize older turns while preserving voice | important | missing | none | Conversation summarization and persona-preserving summaries are not planned. |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | missing | none | Ask-about-show handoff behavior is not covered. |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | full | 4.2 Core Features and 5. Structured Output Contracts - `commentary` + `showList` and exact `Title::externalId::mediaType` format |  |
| PRD-073 | Retry malformed mention output once, then fallback | important | missing | none | The plan does not include a malformed-output retry path or fallback sequence. |
| PRD-074 | Redirect Ask back into TV/movie domain | important | missing | none | The plan never states Ask must redirect users back into the TV/movie domain when prompted otherwise. |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | partial | 5. AI Service Strategy - "Concepts: 1-3 evocative words, vibe-based" | Concepts are treated as vibes, but the plan never explicitly draws the line against genre labels. |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | partial | 5. AI Service Strategy - "Concepts: 1-3 evocative words, vibe-based, no generic filler" | The plan captures 1-3 evocative words, but it omits the bullet-only formatting rule. |
| PRD-077 | Order concepts by strongest aha and varied axes | important | missing | none | Ordering concepts by strongest aha and ensuring axis diversity are not addressed. |
| PRD-078 | Require concept selection and guide ingredient picking | important | partial | 4.2 Core Features - "Alchemy: Step-based blending UI (Select Shows -> Conceptualize -> Alchemize)" | The staged flow implies concept interaction, but required concept selection rules and ingredient-guidance copy are not defined. |
| PRD-079 | Return exactly five Explore Similar recommendations | important | missing | none | The plan never commits Explore Similar to exactly five recommendations. |
| PRD-080 | Support full Alchemy loop with chaining | important | full | 6. Implementation Phases - Phase 4: "Implement 'Alchemy' multi-round blending logic" |  |
| PRD-081 | Clear downstream results when inputs change | important | missing | none | The plan does not state that changing inputs clears downstream concepts or results. |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | missing | none | Multi-show concept generation scale and larger option pools are not planned. |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | full | 5. Structured Output Contracts - "Alchemy Reasons: Explicitly referencing selected concepts in 1-3 sentences" |  |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | partial | 1. Project Overview - "taste-aware" AI discovery; 5. Structured Output Contracts | Taste alignment is a goal, but surprise-without-betrayal and defensibility are not turned into explicit planning requirements. |
| PRD-085 | Keep one consistent AI persona across surfaces | important | full | 5. Personality Enforcement - "persona will be maintained via specific system prompts across all surfaces" |  |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | partial | 5. Personality Enforcement - shared persona plus spoiler-safe Ask behavior | The plan covers persona consistency and some surface rules, but it does not enumerate the shared cross-surface guardrail set. |
| PRD-087 | Make AI warm, joyful, and light in critique | important | partial | 5. Personality Enforcement - "TV/movie nerd friend" persona | The persona is named, but warmth, joy-forward tone, and light-touch critique are not explicitly preserved as non-negotiables. |
| PRD-088 | Structure Scoop as personal taste mini-review | important | partial | 5. Personality Enforcement - "Scoop: Magazine sidebar style, opinionated, 150-350 words" | This captures flavor and length, but not the full mini-review structure of take, stack-up, fit, and verdict. |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | partial | 5. Personality Enforcement - "Ask: Conversational, picks favorites" | Dialogue-like tone is present, but the plan never makes briskness and default brevity explicit. |
| PRD-090 | Feed AI the right surface-specific context inputs | important | missing | none | The plan does not specify the library, show-context, concept, and chat-history inputs each AI surface needs. |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | missing | none | No validation rubric, scoring loop, or hard-fail integrity check is planned for discovery quality. |
| PRD-092 | Show person gallery, name, and bio | important | partial | 6. Implementation Phases - Phase 4: "Create Person Detail page with filmography and analytics" | The page exists in the roadmap, but gallery, name, and bio requirements are not explicit. |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | partial | 6. Implementation Phases - Phase 4: "Create Person Detail page with filmography and analytics" | Analytics are planned, but ratings, genres, and projects-by-year metrics are not specified. |
| PRD-094 | Group filmography by year | important | partial | 6. Implementation Phases - Phase 4: "Create Person Detail page with filmography and analytics" | Filmography is planned, but the required year grouping is not called out. |
| PRD-095 | Open Show Detail from selected credit | important | missing | none | Credit-to-Show Detail navigation is not mentioned. |
| PRD-096 | Include font size and Search-on-launch settings | important | missing | none | Font size and Search-on-launch settings are not included in the settings plan. |
| PRD-097 | Support username, model, and API-key settings safely | important | partial | 3. Data Model & Persistence - `settings` entity includes `user_name`, `catalog_api_key`, `ai_api_key`, and `ai_model` | The fields are present, but safe storage boundaries and sync behavior are not described. |
| PRD-098 | Export saved shows and My Data as zip | critical | partial | 6. Implementation Phases - Phase 4: "Build Settings page with Data Export (.zip/JSON)" | Export is planned, but the exact scope of saved shows plus My Data is not stated. |
| PRD-099 | Encode export dates using ISO-8601 | important | missing | none | ISO-8601 encoding for exported dates is not specified. |

## 3. Coverage Scores

Overall score: `(13 x 1.0 + 54 x 0.5) / 99 x 100 = 40.40%`

Critical: `(5 x 1.0 + 22 x 0.5) / 30 x 100 = 53.33%` (16.0 of 30 critical requirements)
Important: `(8 x 1.0 + 32 x 0.5) / 67 x 100 = 35.82%` (24.0 of 67 important requirements)
Detail: `(0 x 1.0 + 0 x 0.5) / 2 x 100 = 0.00%` (0.0 of 2 detail requirements)
Overall: `(13 x 1.0 + 54 x 0.5) / 99 x 100 = 40.40%` (40.0 of 99 total requirements)

## 4. Top Gaps

- PRD-003 | `critical` | Ship `.env.example` with required variables. This matters because benchmark setup stops being repeatable and auditable if the repository never defines its required environment contract.
- PRD-010 | `critical` | Isolate namespaces and scope destructive resets. This matters because test resets can corrupt or erase data from other runs if namespace scoping is not an explicit implementation rule.
- PRD-022 | `critical` | Define collection membership by assigned status. This matters because save, remove, grouping, and overlay behavior all depend on a single unambiguous rule for when a show is "in" the library.
- PRD-031 | `critical` | Resolve AI recommendations to real selectable shows. This matters because discovery becomes decorative instead of actionable if recommendations cannot reliably open real Detail pages or fall back cleanly.
- PRD-034 | `critical` | Preserve saved libraries across data-model upgrades. This matters because schema evolution can silently destroy the user's collection, ratings, tags, and Scoop data if continuity work is never planned.

## 5. Coverage Narrative

#### Overall Posture

This is a structurally sound high-level plan with major semantic holes. It covers the stack, the major screens, and the headline AI surfaces, but it does not yet plan enough of the benchmark-specific repo deliverables, data lifecycle rules, and behavioral contracts to execute the PRD safely or faithfully.

#### Strength Clusters

The strongest coverage is in App Navigation & Discover Shell, the broad shape of Collection Home, and the headline AI surface map across Ask, Explore Similar, and Alchemy. Benchmark Runtime & Isolation also has a solid skeleton around Next.js, Supabase, namespace IDs, user IDs, migrations, and server-side source of truth, even though several compliance details are still missing.

#### Weakness Clusters

The gaps cluster in three places. First, Benchmark Runtime & Isolation lacks explicit repo-operability details such as `.env.example`, secret-handling rules, Docker posture, and reset scoping. Second, Collection Data & Persistence is weak on edge semantics like save triggers, re-add flows, upgrade continuity, sync, merge policy, and session-only AI state. Third, the plan underspecifies detailed UX and AI contracts in Show Detail, Ask, Concepts, AI Voice, Person Detail, and Settings, where the PRD expects much tighter behavioral precision.

#### Risk Assessment

If this plan were executed as-is, the most likely outcome is a polished shell that looks plausible but fails benchmark review on hidden rules. A QA reviewer would first notice missing repo/configuration deliverables and then run into deeper parity issues: ambiguous save/remove behavior, non-deterministic AI recommendation handoff, absent Search and Detail edge states, and no explicit protection against data loss during schema evolution.

#### Remediation Guidance

The next planning pass needs more than extra tasks; it needs tighter contracts. Add a benchmark compliance section for environment variables, scripts, reset safety, auth injection, and cloud-agent constraints; a persistence rules section for membership, save/remove/re-add defaults, merge semantics, sync, continuity, and transient-vs-persisted AI state; and page-level acceptance criteria for Detail, Ask, Concepts, Person Detail, and Settings that capture exact UI states, AI guardrails, and fallback behavior.
