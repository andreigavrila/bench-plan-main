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
| PRD-001 | Use Next.js latest stable runtime | critical | partial | 2 Core Decisions and Assumptions | The plan chooses Next.js, but it does not explicitly pin the latest stable release as the benchmark baseline. |
| PRD-002 | Use Supabase official client libraries | critical | full | 2 Core Decisions and Assumptions; 3.3 Server Boundary; 4 Environment, Scripts, and Repo Deliverables; Milestones 0-1 |  |
| PRD-003 | Ship `.env.example` with required variables | critical | full | 2 Core Decisions and Assumptions; 3.3 Server Boundary; 4 Environment, Scripts, and Repo Deliverables; Milestones 0-1 |  |
| PRD-004 | Ignore `.env*` secrets except example | important | full | 2 Core Decisions and Assumptions; 3.3 Server Boundary; 4 Environment, Scripts, and Repo Deliverables; Milestones 0-1 |  |
| PRD-005 | Configure build through env without code edits | critical | full | 2 Core Decisions and Assumptions; 3.3 Server Boundary; 4 Environment, Scripts, and Repo Deliverables; Milestones 0-1 |  |
| PRD-006 | Keep secrets out of repo and server-only | critical | full | 2 Core Decisions and Assumptions; 3.3 Server Boundary; 4 Environment, Scripts, and Repo Deliverables; Milestones 0-1 |  |
| PRD-007 | Provide app, test, reset command scripts | critical | full | 2 Core Decisions and Assumptions; 3.3 Server Boundary; 4 Environment, Scripts, and Repo Deliverables; Milestones 0-1 |  |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | 2 Core Decisions and Assumptions; 3.3 Server Boundary; 4 Environment, Scripts, and Repo Deliverables; Milestones 0-1 |  |
| PRD-009 | Use one stable namespace per build | critical | full | 2 Core Decisions and Assumptions; 3.3 Server Boundary; 4 Environment, Scripts, and Repo Deliverables; Milestones 0-1 |  |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | 2 Core Decisions and Assumptions; 3.3 Server Boundary; 4 Environment, Scripts, and Repo Deliverables; Milestones 0-1 |  |
| PRD-011 | Attach every user record to `user_id` | critical | full | 2 Core Decisions and Assumptions; 3.3 Server Boundary; 4 Environment, Scripts, and Repo Deliverables; Milestones 0-1 |  |
| PRD-012 | Partition persisted data by namespace and user | critical | full | 2 Core Decisions and Assumptions; 3.3 Server Boundary; 4 Environment, Scripts, and Repo Deliverables; Milestones 0-1 |  |
| PRD-013 | Support documented dev auth injection, prod-gated | important | full | 2 Core Decisions and Assumptions; 3.3 Server Boundary; 4 Environment, Scripts, and Repo Deliverables; Milestones 0-1 |  |
| PRD-014 | Real OAuth later needs no schema redesign | important | full | 2 Core Decisions and Assumptions; 3.3 Server Boundary; 4 Environment, Scripts, and Repo Deliverables; Milestones 0-1 |  |
| PRD-015 | Keep backend as persisted source of truth | critical | full | 2 Core Decisions and Assumptions; 3.3 Server Boundary; 4 Environment, Scripts, and Repo Deliverables; Milestones 0-1 |  |
| PRD-016 | Make client cache safe to discard | critical | full | 2 Core Decisions and Assumptions; 3.3 Server Boundary; 4 Environment, Scripts, and Repo Deliverables; Milestones 0-1 |  |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | full | 2 Core Decisions and Assumptions; 3.3 Server Boundary; 4 Environment, Scripts, and Repo Deliverables; Milestones 0-1 |  |
| PRD-018 | Overlay saved user data on every show appearance | critical | partial | 8.3 Discover Hub; Milestone 3 Acceptance | The plan covers overlay behavior in Search and refreshed saved shows, but it does not explicitly extend that rule to every show-rendering surface. |
| PRD-019 | Support visible statuses plus hidden `Next` | important | full | 5.1 Tables; 5.3 Collection Membership and Save Rules; 5.4 Merge and Conflict Rules; 7 AI and Discovery Plan |  |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | full | 5.1 Tables; 5.3 Collection Membership and Save Rules; 5.4 Merge and Conflict Rules; 7 AI and Discovery Plan |  |
| PRD-021 | Support free-form multi-tag personal tag library | important | full | 5.1 Tables; 5.3 Collection Membership and Save Rules; 5.4 Merge and Conflict Rules; 7 AI and Discovery Plan |  |
| PRD-022 | Define collection membership by assigned status | critical | full | 5.1 Tables; 5.3 Collection Membership and Save Rules; 5.4 Merge and Conflict Rules; 7 AI and Discovery Plan |  |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | full | 5.1 Tables; 5.3 Collection Membership and Save Rules; 5.4 Merge and Conflict Rules; 7 AI and Discovery Plan |  |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | 5.1 Tables; 5.3 Collection Membership and Save Rules; 5.4 Merge and Conflict Rules; 7 AI and Discovery Plan |  |
| PRD-025 | Removing status deletes show and all My Data | critical | full | 5.1 Tables; 5.3 Collection Membership and Save Rules; 5.4 Merge and Conflict Rules; 7 AI and Discovery Plan |  |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | partial | 5.4 Merge and Conflict Rules | The plan preserves My Data when a stored row still exists, but it does not define how deleted My Data is restored when a show is re-added. |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | 5.1 Tables; 5.3 Collection Membership and Save Rules; 5.4 Merge and Conflict Rules; 7 AI and Discovery Plan |  |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | partial | 5.1 Tables; 5.4 Merge and Conflict Rules; 7.3 Scoop | Timestamps are used for conflict resolution and freshness, but the plan does not specify sorting behavior driven by those timestamps. |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | full | 5.1 Tables; 5.3 Collection Membership and Save Rules; 5.4 Merge and Conflict Rules; 7 AI and Discovery Plan |  |
| PRD-030 | Keep Ask and Alchemy state session-only | important | full | 5.1 Tables; 5.3 Collection Membership and Save Rules; 5.4 Merge and Conflict Rules; 7 AI and Discovery Plan |  |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | full | 5.1 Tables; 5.3 Collection Membership and Save Rules; 5.4 Merge and Conflict Rules; 7 AI and Discovery Plan |  |
| PRD-032 | Show collection and rating tile indicators | important | full | 5.1 Tables; 5.3 Collection Membership and Save Rules; 5.4 Merge and Conflict Rules; 7 AI and Discovery Plan |  |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | partial | 5.4 Merge and Conflict Rules; 10.2 Integration Tests | The plan covers merge logic and settings version conflicts, but it does not explicitly define duplicate-show merge behavior across synced libraries. |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | full | 5.1 Tables; 5.3 Collection Membership and Save Rules; 5.4 Merge and Conflict Rules; 7 AI and Discovery Plan |  |
| PRD-035 | Persist synced settings, local settings, UI state | important | partial | 5.1 Tables | Settings persistence is planned, but UI-state storage remains optional and is not fully mapped field by field. |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | full | 5.1 Tables; 5.3 Collection Membership and Save Rules; 5.4 Merge and Conflict Rules; 7 AI and Discovery Plan |  |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | full | 5.1 Tables; 5.3 Collection Membership and Save Rules; 5.4 Merge and Conflict Rules; 7 AI and Discovery Plan |  |
| PRD-038 | Provide filters panel and main screen destinations | important | full | 8.1 Global Layout; 8.3 Discover Hub |  |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | full | 8.1 Global Layout; 8.3 Discover Hub |  |
| PRD-040 | Keep Settings in persistent primary navigation | important | full | 8.1 Global Layout; 8.3 Discover Hub |  |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | 8.1 Global Layout; 8.3 Discover Hub |  |
| PRD-042 | Show only library items matching active filters | important | full | 8.2 Collection Home; 8.3 Discover Hub |  |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | 8.2 Collection Home; 8.3 Discover Hub |  |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | full | 8.2 Collection Home; 8.3 Discover Hub |  |
| PRD-045 | Render poster, title, and My Data badges | important | full | 8.2 Collection Home; 8.3 Discover Hub |  |
| PRD-046 | Provide empty-library and empty-filter states | detail | full | 8.2 Collection Home; 8.3 Discover Hub |  |
| PRD-047 | Search by title or keywords | important | full | 8.2 Collection Home; 8.3 Discover Hub |  |
| PRD-048 | Use poster grid with collection markers | important | full | 8.2 Collection Home; 8.3 Discover Hub |  |
| PRD-049 | Auto-open Search when setting is enabled | detail | full | 8.2 Collection Home; 8.3 Discover Hub |  |
| PRD-050 | Keep Search non-AI in tone | important | partial | 8.3 Discover Hub | Search is described as a catalog flow, but the plan does not explicitly preserve the non-AI tone requirement. |
| PRD-051 | Preserve Show Detail narrative section order | important | full | 7.3 Scoop; 7.5 Explore Similar; 8.4 Show Detail Page |  |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | full | 7.3 Scoop; 7.5 Explore Similar; 8.4 Show Detail Page |  |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | full | 7.3 Scoop; 7.5 Explore Similar; 8.4 Show Detail Page |  |
| PRD-054 | Place status/interest controls in toolbar | important | full | 7.3 Scoop; 7.5 Explore Similar; 8.4 Show Detail Page |  |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | 7.3 Scoop; 7.5 Explore Similar; 8.4 Show Detail Page |  |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | 7.3 Scoop; 7.5 Explore Similar; 8.4 Show Detail Page |  |
| PRD-057 | Show overview early for fast scanning | important | full | 7.3 Scoop; 7.5 Explore Similar; 8.4 Show Detail Page |  |
| PRD-058 | Scoop shows correct states and progressive feedback | important | partial | 7.3 Scoop; 8.4 Show Detail Page | The plan covers streaming and caching, but it does not define the detailed Scoop state model and progressive copy states from the experience spec. |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | full | 7.3 Scoop; 7.5 Explore Similar; 8.4 Show Detail Page |  |
| PRD-060 | Include traditional recommendations strand | important | full | 7.3 Scoop; 7.5 Explore Similar; 8.4 Show Detail Page |  |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | full | 7.3 Scoop; 7.5 Explore Similar; 8.4 Show Detail Page |  |
| PRD-062 | Include streaming availability and person-linking credits | important | full | 7.3 Scoop; 7.5 Explore Similar; 8.4 Show Detail Page |  |
| PRD-063 | Gate seasons to TV and financials to movies | important | full | 7.3 Scoop; 7.5 Explore Similar; 8.4 Show Detail Page |  |
| PRD-064 | Keep primary actions early and page not overwhelming | important | partial | 8.4 Show Detail Page; 12 Risk Register | It protects section order and toolbar placement, but it does not set concrete acceptance criteria for keeping the page powerful without feeling overwhelming. |
| PRD-065 | Provide conversational Ask chat interface | important | full | 7.1 Shared AI Infrastructure; 7.2 Ask; 8.3 Discover Hub |  |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | full | 7.1 Shared AI Infrastructure; 7.2 Ask; 8.3 Discover Hub |  |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | 7.1 Shared AI Infrastructure; 7.2 Ask; 8.3 Discover Hub |  |
| PRD-068 | Open Detail from mentions or Search fallback | important | full | 7.1 Shared AI Infrastructure; 7.2 Ask; 8.3 Discover Hub |  |
| PRD-069 | Show six random starter prompts with refresh | important | full | 7.1 Shared AI Infrastructure; 7.2 Ask; 8.3 Discover Hub |  |
| PRD-070 | Summarize older turns while preserving voice | important | full | 7.1 Shared AI Infrastructure; 7.2 Ask; 8.3 Discover Hub |  |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | full | 7.1 Shared AI Infrastructure; 7.2 Ask; 8.3 Discover Hub |  |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | full | 7.1 Shared AI Infrastructure; 7.2 Ask; 8.3 Discover Hub |  |
| PRD-073 | Retry malformed mention output once, then fallback | important | full | 7.1 Shared AI Infrastructure; 7.2 Ask; 8.3 Discover Hub |  |
| PRD-074 | Redirect Ask back into TV/movie domain | important | full | 7.1 Shared AI Infrastructure; 7.2 Ask; 8.3 Discover Hub |  |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | full | 7.4 Concepts; 7.5 Explore Similar; 7.6 Alchemy; 8.3 Discover Hub |  |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | full | 7.4 Concepts; 7.5 Explore Similar; 7.6 Alchemy; 8.3 Discover Hub |  |
| PRD-077 | Order concepts by strongest aha and varied axes | important | partial | 7.4 Concepts | The plan requires varied concepts, but it does not specify ordering concepts by strongest aha first. |
| PRD-078 | Require concept selection and guide ingredient picking | important | partial | 7.5 Explore Similar; 8.3 Discover Hub | Concept selection is required, but the ingredient-guidance UX copy is not specified. |
| PRD-079 | Return exactly five Explore Similar recommendations | important | full | 7.4 Concepts; 7.5 Explore Similar; 7.6 Alchemy; 8.3 Discover Hub |  |
| PRD-080 | Support full Alchemy loop with chaining | important | full | 7.4 Concepts; 7.5 Explore Similar; 7.6 Alchemy; 8.3 Discover Hub |  |
| PRD-081 | Clear downstream results when inputs change | important | full | 7.4 Concepts; 7.5 Explore Similar; 7.6 Alchemy; 8.3 Discover Hub |  |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | partial | 7.4 Concepts | The plan requires shared multi-show concepts, but not the larger option pool expected for multi-show generation. |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | full | 7.4 Concepts; 7.5 Explore Similar; 7.6 Alchemy; 8.3 Discover Hub |  |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | partial | 7.7 Discovery Quality Validation | The plan measures taste alignment and surprise, but it does not turn them into concrete recommendation-generation rules. |
| PRD-085 | Keep one consistent AI persona across surfaces | important | full | 7.1 Shared AI Infrastructure; 7.2 Ask; 7.3 Scoop; 7.7 Discovery Quality Validation |  |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | full | 7.1 Shared AI Infrastructure; 7.2 Ask; 7.3 Scoop; 7.7 Discovery Quality Validation |  |
| PRD-087 | Make AI warm, joyful, and light in critique | important | partial | 7.1 Shared AI Infrastructure | The persona summary is close, but it does not explicitly preserve the joy-forward, light-in-critique behavior from the voice spec. |
| PRD-088 | Structure Scoop as personal taste mini-review | important | full | 7.1 Shared AI Infrastructure; 7.2 Ask; 7.3 Scoop; 7.7 Discovery Quality Validation |  |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | full | 7.1 Shared AI Infrastructure; 7.2 Ask; 7.3 Scoop; 7.7 Discovery Quality Validation |  |
| PRD-090 | Feed AI the right surface-specific context inputs | important | full | 7.1 Shared AI Infrastructure; 7.2 Ask; 7.3 Scoop; 7.7 Discovery Quality Validation |  |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | partial | 7.7 Discovery Quality Validation | The validation harness is present, but the explicit scoring thresholds and hard-fail integrity rule are not locked in. |
| PRD-092 | Show person gallery, name, and bio | important | full | 8.5 Person Detail |  |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | full | 8.5 Person Detail |  |
| PRD-094 | Group filmography by year | important | full | 8.5 Person Detail |  |
| PRD-095 | Open Show Detail from selected credit | important | full | 8.5 Person Detail |  |
| PRD-096 | Include font size and Search-on-launch settings | important | full | 5.1 Tables; 8.6 Settings and Your Data; 10 Testing Plan |  |
| PRD-097 | Support username, model, and API-key settings safely | important | partial | 8.6 Settings and Your Data | Safe key handling is addressed, but user-editable API-key settings remain optional instead of a committed deliverable. |
| PRD-098 | Export saved shows and My Data as zip | critical | full | 5.1 Tables; 8.6 Settings and Your Data; 10 Testing Plan |  |
| PRD-099 | Encode export dates using ISO-8601 | important | full | 5.1 Tables; 8.6 Settings and Your Data; 10 Testing Plan |  |

### 3. Coverage Scores

Critical:  (27 × 1.0 + 3 × 0.5) / 30 × 100 = 95.0%  (28.5 of 30 critical requirements)
Important: (54 × 1.0 + 13 × 0.5) / 67 × 100 = 90.3%  (60.5 of 67 important requirements)
Detail:    (2 × 1.0 + 0 × 0.5) / 2 × 100 = 100.0%  (2.0 of 2 detail requirements)
Overall:   (83 × 1.0 + 16 × 0.5) / 99 × 100 = 91.9%  (91.0 of 99 total requirements)

### 4. Top Gaps

1. PRD-026 | critical | Re-add preserves My Data and refreshes public data
Why this matters: Without a re-add recovery model, users can permanently lose tags, ratings, and Scoop data after a remove-and-save-again cycle, and the plan risks failing a frozen critical requirement.

2. PRD-018 | critical | Overlay saved user data on every show appearance
Why this matters: If overlay rules are not explicit on every show surface, the same show can appear with inconsistent status or rating state across Search, recommendations, and AI-driven surfaces.

3. PRD-001 | critical | Use Next.js latest stable runtime
Why this matters: A loose runtime baseline invites benchmark drift across Next.js releases, which can change build behavior and make runs harder to compare fairly.

4. PRD-091 | important | Validate discovery with rubric and hard-fail integrity
Why this matters: Without explicit pass thresholds and a non-negotiable integrity gate, structurally valid AI output can still ship with off-brand or unresolved recommendations.

5. PRD-033 | important | Sync libraries/settings consistently and merge duplicates
Why this matters: Unspecified duplicate-merge behavior can fork a user library or silently lose the more recent field value during sync-heavy scenarios.

### 5. Coverage Narrative

#### Overall Posture
This is a strong, implementation-ready plan with solid architecture, sequencing, and test coverage. The misses are not in core feature presence; they are in a handful of benchmark-specific behavioral contracts where the plan stays high level instead of locking down the exact denominator requirement.

#### Strength Clusters
The plan is strongest in Benchmark Runtime & Isolation, App Navigation & Discover Shell, Collection Home & Search, Ask Chat, and the main Show Detail flows. It is concrete on namespace and user partitioning, repo deliverables, save and remove rules, Discover mode structure, Ask contracts, milestone sequencing, and the associated test strategy.

#### Weakness Clusters
The gaps cluster around cross-surface consistency and edge-case behavior rather than missing whole product areas. Collection Data & Persistence has the sharpest semantic gaps, especially universal overlay behavior and the catalog-frozen re-add preservation rule. A second cluster sits in AI quality and concept behavior, where the plan acknowledges the surface but does not always carry through the exact ordering, guidance, or acceptance-bar language from the supporting specs.

#### Risk Assessment
If this plan is executed as written, the first QA-visible failures are likely to be parity issues rather than missing screens: a saved show may not render the same user overlay everywhere, a removed-and-re-added show may lose prior My Data, and AI output may pass structural validation without meeting the stricter quality bar. Those failures would be noticeable because the product would feel mostly complete while still violating core behavioral expectations.

#### Remediation Guidance
The remaining work is mostly specification tightening, not a new architecture. The plan needs a few explicit contract decisions: define overlay behavior for every show-rendering surface, resolve how re-add preservation works alongside deletion semantics, pin the runtime baseline to the benchmark wording, and turn AI quality goals into pass-fail acceptance criteria instead of advisory checks. For the UX-contract gaps, add short acceptance bullets to Search, Scoop, Detail, and Concepts rather than creating new milestones.
