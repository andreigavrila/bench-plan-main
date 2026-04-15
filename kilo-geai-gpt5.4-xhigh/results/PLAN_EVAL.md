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

### 2. Coverage Table

| PRD-ID | Requirement | Severity | Coverage | Evidence | Gap |
| ------ | ----------- | -------- | -------- | -------- | --- |
| PRD-001 | Use Next.js latest stable runtime | critical | full | `§2 Planning Principles` and `§3.1 Application Shape` specify Next.js/App Router as the baseline runtime. | |
| PRD-002 | Use Supabase official client libraries | critical | partial | `§17 Phase 1` says to set up Supabase clients. | The plan commits to Supabase but never explicitly requires the official client libraries. |
| PRD-003 | Ship `.env.example` with required variables | critical | full | `§16 Benchmark Deliverables Plan` includes `.env.example` with required environment variables and comments. | |
| PRD-004 | Ignore `.env*` secrets except example | important | full | `§16 Benchmark Deliverables Plan` includes `.gitignore` excluding `.env*` except `.env.example`. | |
| PRD-005 | Configure build through env without code edits | critical | partial | `§16 Benchmark Deliverables Plan` enumerates expected env vars and `§17 Phase 1` includes env parsing. | The plan implies environment-driven setup but does not explicitly state the build must be configurable without editing source code. |
| PRD-006 | Keep secrets out of repo and server-only | critical | full | `§5.3 Security and Access`, `§9.10 Settings and Your Data`, and `§16 Benchmark Deliverables Plan` keep elevated credentials server-only and forbid committed secrets. | |
| PRD-007 | Provide app, test, reset command scripts | critical | full | `§16 Benchmark Deliverables Plan` requires scripts for app start, tests, and namespace reset. | |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | `§5.1 Schema Deliverables` and `§16 Benchmark Deliverables Plan` call for SQL migrations and repeatable fixtures. | |
| PRD-009 | Use one stable namespace per build | critical | full | `§6.1 Namespace Resolution` says to resolve a stable `namespace_id` for the lifetime of a build. | |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | `§6.1 Namespace Resolution` and `§6.4 Destructive Test Reset` scope reads, writes, exports, and resets to the active namespace. | |
| PRD-011 | Attach every user record to `user_id` | critical | full | `§2 Planning Principles` and `§6.2 User Identity Resolution` require `user_id` for persisted records. | |
| PRD-012 | Partition persisted data by namespace and user | critical | full | `§2 Planning Principles` explicitly says to partition every persisted record by `namespace_id` and `user_id`. | |
| PRD-013 | Support documented dev auth injection, prod-gated | important | full | `§6.3 Dev/Test Identity Injection` lists benchmark-friendly mechanisms and requires production gating. | |
| PRD-014 | Real OAuth later needs no schema redesign | important | full | `§6.3 Dev/Test Identity Injection` states no schema redesign should be needed later for OAuth. | |
| PRD-015 | Keep backend as persisted source of truth | critical | full | `§2 Planning Principles` says the backend is the source of truth. | |
| PRD-016 | Make client cache safe to discard | critical | full | `§2 Planning Principles` says client caches are disposable, and `§13 State Management and Caching Plan` keeps canonical reads server-backed. | |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | missing | none | The plan never states Docker is optional or avoided, leaving cloud-agent execution compatibility underspecified. |
| PRD-018 | Overlay saved user data on every show appearance | critical | full | `§2 Planning Principles` and `§10 Business Rules Implementation Checklist` require user-overlay precedence everywhere. | |
| PRD-019 | Support visible statuses plus hidden `Next` | important | partial | `§19 Open Product Decisions To Preserve As Explicit TODOs` calls out whether `Next` becomes a first-class surfaced status. | The plan acknowledges `Next` as an open question but does not commit to hidden data-model support for it. |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | full | `§9.5 Show Detail` states Interested and Excited map to `Later` plus `myInterest`. | |
| PRD-021 | Support free-form multi-tag personal tag library | important | full | `§9.3 Filters and Sidebar` includes one filter per tag, implying a reusable personal tag library, and `§10` covers tag save behavior. | |
| PRD-022 | Define collection membership by assigned status | critical | full | `§10 Business Rules Implementation Checklist` ties collection membership to status assignment. | |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | full | `§10 Business Rules Implementation Checklist` explicitly covers status, interest, rating, and tagging save triggers. | |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | `§10 Business Rules Implementation Checklist` defines `Later + Interested` as the default except rating-driven `Done`. | |
| PRD-025 | Removing status deletes show and all My Data | critical | full | `§4.5 Removal Semantics` and `§10 Business Rules Implementation Checklist` delete the record and clear all My Data. | |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | missing | none | The plan deletes the saved-show record on removal and never introduces a re-add flow that restores prior My Data while refreshing catalog fields. |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | `§4.2 Primary Entities` includes timestamps for all `my*` fields and AI Scoop. | |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | full | `§4.4 Merge and Conflict Rules`, `§9.2 Collection Home`, and `§15.1 Unit Tests` use timestamps for conflict resolution, sorting, and freshness logic. | |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | full | `§8.5 Scoop Design` sets a 4-hour freshness target and persists Scoop only for saved shows. | |
| PRD-030 | Keep Ask and Alchemy state session-only | important | full | `§8.4 Ask Chat Design` and `§13 State Management and Caching Plan` keep chat and Alchemy state transient/session-scoped. | |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | full | `§7.1 Responsibilities`, `§8.7 Recommendation Design`, and `§10` require recommendation integrity against the real catalog. | |
| PRD-032 | Show collection and rating tile indicators | important | full | `§9.2 Collection Home` and `§10` call for in-collection and rating tile badges. | |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | full | `§4.4 Merge and Conflict Rules` and `§15.2 Integration Tests` cover duplicate merging and cross-device consistency. | |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | full | `§14 Migration and Continuity Plan` explicitly preserves user libraries through model upgrades. | |
| PRD-035 | Persist synced settings, local settings, UI state | important | full | `§4.2 Primary Entities` defines `cloud_settings`, `user_preferences`, and `ui_state`. | |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | full | `§4.1 Core Persistence Strategy` keeps large detail payloads transient, and `§4.3 Supporting Persistence Decisions` persists `providerData` and `external_ids`. | |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | full | `§4.4 Merge and Conflict Rules` defines first-non-empty catalog merge behavior and timestamp-based My Data resolution. | |
| PRD-038 | Provide filters panel and main screen destinations | important | full | `§9.1 App Shell and Navigation` includes a filter/navigation panel and the main destinations. | |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | full | `§9.1 App Shell and Navigation` includes persistent navigation to Find/Discover. | |
| PRD-040 | Keep Settings in persistent primary navigation | important | full | `§9.1 App Shell and Navigation` includes persistent navigation to Settings. | |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | `§3.2 Feature layer` and `§9.4`, `§9.6`, `§9.7` cover Search, Ask, and Alchemy modes. | |
| PRD-042 | Show only library items matching active filters | important | full | `§9.2 Collection Home` and `§9.3 Filters and Sidebar` define filtered library rendering. | |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | `§9.2 Collection Home` specifies the exact status-group order. | |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | full | `§9.3 Filters and Sidebar` lists All Shows, per-tag, No Tags, genre, decade, score ranges, and media-type toggle. | |
| PRD-045 | Render poster, title, and My Data badges | important | full | `§9.2 Collection Home` requires tile badges and `§12.2 Shared Components` includes show tiles. | |
| PRD-046 | Provide empty-library and empty-filter states | detail | full | `§9.2 Collection Home` includes both the no-collection and no-filter-results empty states. | |
| PRD-047 | Search by title or keywords | important | full | `§7.1 Responsibilities` and `§9.4 Search` define text-based search over movies and TV shows. | |
| PRD-048 | Use poster grid with collection markers | important | full | `§9.4 Search` calls for poster-grid results and in-collection badges. | |
| PRD-049 | Auto-open Search when setting is enabled | detail | full | `§9.4 Search` says to honor the Search-on-launch preference. | |
| PRD-050 | Keep Search non-AI in tone | important | partial | `§9.4 Search` treats Search as external catalog lookup rather than an AI workflow. | The plan never explicitly preserves a non-AI presentation/tone boundary for Search. |
| PRD-051 | Preserve Show Detail narrative section order | important | partial | `§9.5 Show Detail` says to preserve the intended hierarchy and lists ordered sections. | The listed order collapses toolbar/tag controls and does not fully preserve the exact narrative ordering from the detail-page spec. |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | partial | `§9.5 Show Detail` includes a header media carousel with trailers, backdrops, posters, and logos; `§15.5` tests no-trailer/no-backdrop cases. | The plan covers fallback in QA but does not concretely specify the implementation approach for graceful header fallback. |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | full | `§9.5 Show Detail` puts core facts and community score at the top of the page. | |
| PRD-054 | Place status/interest controls in toolbar | important | partial | `§9.5 Show Detail` groups status, interest, rating, and tags under personal relationship controls. | The plan never explicitly commits to toolbar placement for status/interest controls. |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | `§9.5 Show Detail` and `§10` explicitly define tag-to-save as `Later + Interested`. | |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | `§9.5 Show Detail` and `§10` explicitly define rating-to-save as `Done`. | |
| PRD-057 | Show overview early for fast scanning | important | full | `§9.5 Show Detail` places Overview and Scoop near the top of the page flow. | |
| PRD-058 | Scoop shows correct states and progressive feedback | important | full | `§8.5 Scoop Design` and `§9.5 Show Detail` define empty/cached/open states and progressive generation behavior. | |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | full | `§9.5 Show Detail` says Ask About This Show seeds Ask with show context. | |
| PRD-060 | Include traditional recommendations strand | important | full | `§9.5 Show Detail` includes a traditional recommendations strand. | |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | partial | `§9.8 Explore Similar` covers concepts, selection, and recommendation generation. | The plan does not explicitly preserve the CTA-first `Get Concepts` state before concept chips appear. |
| PRD-062 | Include streaming availability and person-linking credits | important | full | `§9.5 Show Detail` includes streaming availability plus cast and crew strands. | |
| PRD-063 | Gate seasons to TV and financials to movies | important | full | `§9.5 Show Detail` explicitly gates Seasons to TV and Budget vs Revenue to movies. | |
| PRD-064 | Keep primary actions early and page not overwhelming | important | full | `§12.1 Visual and Interaction Priorities` keeps primary actions near the top and avoids unnecessary clutter. | |
| PRD-065 | Provide conversational Ask chat interface | important | full | `§9.6 Ask` defines a chat UI with user and assistant turns. | |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | full | `§8.2 Shared AI Contracts` and `§15.4 AI Quality Validation` require spoiler-safe, opinionated Ask responses that answer directly. | |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | `§9.6 Ask` specifies a mentioned-shows horizontal strip. | |
| PRD-068 | Open Detail from mentions or Search fallback | important | full | `§9.6 Ask` defines Search handoff and non-interactive fallback for mapping failures. | |
| PRD-069 | Show six random starter prompts with refresh | important | full | `§9.6 Ask` includes six random starter prompts and a refresh action. | |
| PRD-070 | Summarize older turns while preserving voice | important | full | `§8.3 Context Assembly` and `§8.4 Ask Chat Design` summarize older turns while preserving persona continuity. | |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | full | `§9.5 Show Detail` explicitly seeds Ask with show context. | |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | full | `§8.4 Ask Chat Design` includes the exact `Title::externalId::mediaType;;...` `showList` format. | |
| PRD-073 | Retry malformed mention output once, then fallback | important | full | `§8.4 Ask Chat Design` says the parser retries once and then falls back to commentary plus Search handoff. | |
| PRD-074 | Redirect Ask back into TV/movie domain | important | full | `§8.2 Shared AI Contracts` restricts the domain to TV and movies. | |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | full | `§8.6 Concepts Design` emphasizes evocative structure/vibe/emotion/craft concepts over generic genre language. | |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | full | `§8.6 Concepts Design` requires bullet-list-only, 1-3 word, spoiler-free concepts. | |
| PRD-077 | Order concepts by strongest aha and varied axes | important | full | `§8.6 Concepts Design` orders strongest concepts first and requires diversity across axes. | |
| PRD-078 | Require concept selection and guide ingredient picking | important | partial | `§9.8 Explore Similar` requires at least one concept, and `§9.7 Alchemy` caps selection at 8. | The plan enforces selection but does not explicitly include user guidance that frames concepts as ingredients to pick from. |
| PRD-079 | Return exactly five Explore Similar recommendations | important | full | `§8.7 Recommendation Design` and `§9.8 Explore Similar` both set Explore Similar to 5 recommendations. | |
| PRD-080 | Support full Alchemy loop with chaining | important | full | `§9.7 Alchemy` defines the multi-step flow and More Alchemy chaining. | |
| PRD-081 | Clear downstream results when inputs change | important | full | `§9.7 Alchemy` explicitly clears concepts/results when shows or concepts change. | |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | missing | none | The plan requires shared multi-show concepts but never commits to a larger option pool than single-show generation. |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | full | `§8.7 Recommendation Design` requires each recommendation reason to cite the matching selected concepts. | |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | full | `§8.7 Recommendation Design` and `§15.4 AI Quality Validation` call for taste alignment and surprise without betrayal. | |
| PRD-085 | Keep one consistent AI persona across surfaces | important | full | `§8.2 Shared AI Contracts` defines one warm, playful, opinionated persona for all AI surfaces. | |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | full | `§8.2 Shared AI Contracts` centralizes domain, spoiler, persona, and recommendation-integrity rules. | |
| PRD-087 | Make AI warm, joyful, and light in critique | important | full | `§8.2 Shared AI Contracts` describes the AI as warm, playful, opinionated, and honest. | |
| PRD-088 | Structure Scoop as personal taste mini-review | important | full | `§8.5 Scoop Design` requires personal take, stack-up, Scoop centerpiece, fit/warnings, and verdict. | |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | full | `§8.4 Ask Chat Design` centers user-facing commentary plus session-style chat behavior rather than essay output. | |
| PRD-090 | Feed AI the right surface-specific context inputs | important | full | `§8.3 Context Assembly` enumerates library, My Data, show context, concepts, and chat history inputs. | |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | partial | `§15.4 AI Quality Validation` creates regression checks aligned to `discovery_quality_bar.md`. | The plan adopts the rubric but does not explicitly define hard-fail thresholds or non-negotiable gating for integrity failures. |
| PRD-092 | Show person gallery, name, and bio | important | full | `§9.9 Person Detail` includes person hero/gallery and bio. | |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | full | `§9.9 Person Detail` includes analytics for average ratings, top genres, and projects by year. | |
| PRD-094 | Group filmography by year | important | full | `§9.9 Person Detail` groups filmography by year. | |
| PRD-095 | Open Show Detail from selected credit | important | full | `§9.9 Person Detail` says credit selection opens Show Detail. | |
| PRD-096 | Include font size and Search-on-launch settings | important | full | `§9.10 Settings and Your Data` includes both font size/readability and Search on launch. | |
| PRD-097 | Support username, model, and API-key settings safely | important | full | `§9.10 Settings and Your Data` includes username, AI key handling, AI model, and catalog provider key handling. | |
| PRD-098 | Export saved shows and My Data as zip | critical | full | `§4.6 Export Semantics` and `§9.10 Settings and Your Data` define zip export of durable user data. | |
| PRD-099 | Encode export dates using ISO-8601 | important | full | `§4.6 Export Semantics` serializes dates as ISO-8601. | |

### 3. Coverage Scores

Overall score:

```text
score = (full_count × 1.0 + partial_count × 0.5) / total_count × 100
score = (86 × 1.0 + 10 × 0.5) / 99 × 100
score = 91 / 99 × 100 = 91.9%
```

Score by severity tier:

```text
Critical:  (27 × 1.0 + 2 × 0.5) / 30 × 100 = 93.3%  (28.0 of 30 critical requirements)
Important: (57 × 1.0 + 8 × 0.5) / 67 × 100 = 91.0%  (61.0 of 67 important requirements)
Detail:    (2 × 1.0 + 0 × 0.5) / 2 × 100 = 100.0%  (2.0 of 2 detail requirements)
Overall:   91.9% (99 total requirements)
```

### 4. Top Gaps

1. PRD-026, `critical`, Re-add preserves My Data and refreshes public data.
Without a re-add preservation path, a user who removes and later re-saves a show loses their prior rating, tags, interest, and Scoop history, which directly breaks one of the product's core continuity promises.

2. PRD-005, `critical`, Configure build through env without code edits.
The plan names the variables but never explicitly locks in environment-only configuration, which leaves a benchmark compliance hole around reproducible setup in fresh environments.

3. PRD-002, `critical`, Use Supabase official client libraries.
Using Supabase in the abstract is not enough for benchmark compliance; the missing library-level commitment leaves room for incompatible or ad hoc integration choices.

4. PRD-017, `important`, Avoid Docker requirement for cloud-agent compatibility.
The rider treats Docker-optional execution as part of the benchmark contract, so omitting it creates risk that implementation choices block hosted agents or require privileged local setup.

5. PRD-082, `important`, Generate shared multi-show concepts with larger option pool.
Alchemy depends on a richer concept pool than single-show exploration, and without that distinction the blend workflow is likely to feel flatter and less controllable.

### 5. Coverage Narrative

#### Overall Posture

This is a strong plan with minor-to-moderate gaps rather than a structurally weak one. It covers the benchmark architecture, persistence model, major user journeys, AI surfaces, and testing posture with enough specificity that an implementation team could start building immediately. The main concern is not missing entire feature areas; it is that a handful of benchmark-contract and experience-preservation details are either left implicit or softened into TODOs.

#### Strength Clusters

The plan is strongest in Benchmark Runtime & Isolation, Collection Data & Persistence, Ask Chat, and Settings & Export. It gives concrete architecture, persistence entities, merge rules, namespace and user isolation, explicit save/remove semantics, AI structured-output behavior, and a realistic test matrix. It is also notably strong in cross-cutting AI behavior, where persona, spoiler safety, context assembly, parsing, fallback behavior, and quality validation are all treated as first-class planning concerns rather than hand-waved implementation details.

#### Weakness Clusters

The gaps cluster around specification fidelity rather than breadth. One cluster sits in Benchmark Runtime & Isolation, where the plan adopts the right stack but leaves compliance-critical constraints like official Supabase clients, environment-only configuration, and Docker-optional execution less explicit than the rider expects. The second cluster sits in Show Detail & Relationship UX and concept workflows, where the plan broadly covers the surfaces but blurs a few experience-shaping contracts such as exact section ordering, toolbar placement, CTA-first Explore Similar flow, and the larger multi-show concept pool for Alchemy.

#### Risk Assessment

If executed as-is, the first thing a stakeholder or QA reviewer would likely notice is not that major features are absent, but that some benchmark and UX edge contracts drift from the PRD. The most visible product regression would be continuity around remove-and-re-add behavior: users could lose their personal history for a show after removal even though the PRD expects that history to survive. The most visible benchmark risk would be environment/setup ambiguity, where a build may technically use Next.js and Supabase but still fail strict runner expectations because configuration and cloud-agent compatibility were never nailed down as hard requirements.

#### Remediation Guidance

The remaining work is mostly tighter specification, not a new architecture. Benchmark Runtime & Isolation needs explicit compliance language in the plan: official Supabase clients, environment-only setup, and Docker-optional assumptions should be stated as binding implementation constraints. Show Detail and concept workflows need sharper acceptance criteria that preserve the intended interaction choreography, especially around toolbar placement, CTA sequencing, and Alchemy concept-pool behavior. Data continuity needs one explicit architectural decision for re-add semantics so removal behavior and long-term user-memory preservation are no longer in tension.
