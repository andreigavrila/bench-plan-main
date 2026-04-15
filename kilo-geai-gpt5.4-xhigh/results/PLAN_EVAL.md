## 1. Requirements Extraction

### Benchmark Runtime & Isolation

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

### Collection Data & Persistence

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

### App Navigation & Discover Shell

- PRD-038 | `important` | Provide filters panel and main screen destinations | `product_prd.md > 6. App Structure & Navigation`
- PRD-039 | `important` | Keep Find/Discover in persistent primary navigation | `product_prd.md > 6. App Structure & Navigation`
- PRD-040 | `important` | Keep Settings in persistent primary navigation | `product_prd.md > 6. App Structure & Navigation`
- PRD-041 | `important` | Offer Search, Ask, Alchemy discover modes | `product_prd.md > 6. App Structure & Navigation`

### Collection Home & Search

- PRD-042 | `important` | Show only library items matching active filters | `product_prd.md > 7.1 Collection Home`
- PRD-043 | `important` | Group home into Active, Excited, Interested, Others | `product_prd.md > 7.1 Collection Home`
- PRD-044 | `important` | Support All, tag, genre, decade, score, media filters | `product_prd.md > 4.5 Filters (Ways to View the Collection)`
- PRD-045 | `important` | Render poster, title, and My Data badges | `product_prd.md > 7.1 Collection Home`
- PRD-046 | `detail` | Provide empty-library and empty-filter states | `product_prd.md > 7.1 Collection Home`
- PRD-047 | `important` | Search by title or keywords | `product_prd.md > 7.2 Search (Find → Search)`
- PRD-048 | `important` | Use poster grid with collection markers | `product_prd.md > 7.2 Search (Find → Search)`
- PRD-049 | `detail` | Auto-open Search when setting is enabled | `product_prd.md > 7.2 Search (Find → Search)`
- PRD-050 | `important` | Keep Search non-AI in tone | `supporting_docs/ai_voice_personality.md > 1. Persona Summary`

### Show Detail & Relationship UX

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

### Ask Chat

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

### Concepts, Explore Similar & Alchemy

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

### AI Voice, Persona & Quality

- PRD-085 | `important` | Keep one consistent AI persona across surfaces | `supporting_docs/ai_voice_personality.md > 1. Persona Summary`
- PRD-086 | `critical` | Enforce shared AI guardrails across all surfaces | `supporting_docs/ai_prompting_context.md > 1. Shared Rules (All AI Surfaces)`
- PRD-087 | `important` | Make AI warm, joyful, and light in critique | `supporting_docs/ai_voice_personality.md > 2. Non-Negotiable Voice Pillars`
- PRD-088 | `important` | Structure Scoop as personal taste mini-review | `supporting_docs/ai_voice_personality.md > 4.1 Scoop (Show Detail "The Scoop")`
- PRD-089 | `important` | Keep Ask brisk and dialogue-like by default | `supporting_docs/ai_voice_personality.md > 4.2 Ask (Find → Ask)`
- PRD-090 | `important` | Feed AI the right surface-specific context inputs | `supporting_docs/ai_prompting_context.md > 2. Shared Inputs (Typical)`
- PRD-091 | `important` | Validate discovery with rubric and hard-fail integrity | `supporting_docs/discovery_quality_bar.md > 4. Scoring Rubric (Quick)`

### Person Detail

- PRD-092 | `important` | Show person gallery, name, and bio | `product_prd.md > 7.6 Person Detail Page`
- PRD-093 | `important` | Include ratings, genres, and projects-by-year analytics | `product_prd.md > 7.6 Person Detail Page`
- PRD-094 | `important` | Group filmography by year | `product_prd.md > 7.6 Person Detail Page`
- PRD-095 | `important` | Open Show Detail from selected credit | `product_prd.md > 7.6 Person Detail Page`

### Settings & Export

- PRD-096 | `important` | Include font size and Search-on-launch settings | `product_prd.md > 7.7 Settings & Your Data`
- PRD-097 | `important` | Support username, model, and API-key settings safely | `product_prd.md > 7.7 Settings & Your Data`
- PRD-098 | `critical` | Export saved shows and My Data as zip | `product_prd.md > 7.7 Settings & Your Data`
- PRD-099 | `important` | Encode export dates using ISO-8601 | `product_prd.md > 7.7 Settings & Your Data`

Total: 99 requirements (30 critical, 67 important, 2 detail) across 10 functional areas

## 2. Coverage Table

| PRD-ID | Requirement | Severity | Coverage | Evidence | Gap |
| ------ | ----------- | -------- | -------- | -------- | --- |
| PRD-001 | Use Next.js latest stable runtime | critical | full | 2. Planning Principles; 3.1 Application Shape |  |
| PRD-002 | Use Supabase official client libraries | critical | partial | 2. Planning Principles; 3.1 Application Shape | The plan commits to Supabase but never specifies using the official Supabase client libraries. |
| PRD-003 | Ship `.env.example` with required variables | critical | full | 16. Benchmark Deliverables Plan |  |
| PRD-004 | Ignore `.env*` secrets except example | important | full | 16. Benchmark Deliverables Plan |  |
| PRD-005 | Configure build through env without code edits | critical | full | 3.1 Application Shape; 16. Benchmark Deliverables Plan |  |
| PRD-006 | Keep secrets out of repo and server-only | critical | full | 5.3 Security and Access; 16. Benchmark Deliverables Plan |  |
| PRD-007 | Provide app, test, reset command scripts | critical | full | 16. Benchmark Deliverables Plan |  |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | 5.1 Schema Deliverables; 14. Migration and Continuity Plan |  |
| PRD-009 | Use one stable namespace per build | critical | full | 6.1 Namespace Resolution |  |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | 6.4 Destructive Test Reset; 15.2 Integration Tests |  |
| PRD-011 | Attach every user record to `user_id` | critical | full | 2. Planning Principles; 6.2 User Identity Resolution |  |
| PRD-012 | Partition persisted data by namespace and user | critical | full | 2. Planning Principles; 6.1 Namespace Resolution; 6.2 User Identity Resolution |  |
| PRD-013 | Support documented dev auth injection, prod-gated | important | full | 6.3 Dev/Test Identity Injection; 16. Benchmark Deliverables Plan |  |
| PRD-014 | Real OAuth later needs no schema redesign | important | full | 6.3 Dev/Test Identity Injection |  |
| PRD-015 | Keep backend as persisted source of truth | critical | full | 2. Planning Principles; 13. State Management and Caching Plan |  |
| PRD-016 | Make client cache safe to discard | critical | full | 2. Planning Principles; 13. State Management and Caching Plan |  |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | missing | none | The plan never states Docker is optional or disallowed, so cloud-agent compatibility remains unstated. |
| PRD-018 | Overlay saved user data on every show appearance | critical | full | 9.2 Collection Home; 9.4 Search; 10. Business Rules Implementation Checklist |  |
| PRD-019 | Support visible statuses plus hidden `Next` | important | partial | 4.2 Primary Entities; 19. Open Product Decisions To Preserve As Explicit TODOs | The plan keeps the surfaced statuses explicit but never commits to carrying hidden `Next` support in the underlying status model. |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | full | 9.5 Show Detail; 10. Business Rules Implementation Checklist |  |
| PRD-021 | Support free-form multi-tag personal tag library | important | full | 4.2 Primary Entities; 9.3 Filters and Sidebar |  |
| PRD-022 | Define collection membership by assigned status | critical | full | 4.5 Removal Semantics; 10. Business Rules Implementation Checklist |  |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | full | 10. Business Rules Implementation Checklist |  |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | 10. Business Rules Implementation Checklist |  |
| PRD-025 | Removing status deletes show and all My Data | critical | full | 4.5 Removal Semantics; 10. Business Rules Implementation Checklist |  |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | full | 4.4 Merge and Conflict Rules; 7.3 Refresh Strategy |  |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | 4.2 Primary Entities; 4.4 Merge and Conflict Rules |  |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | full | 4.4 Merge and Conflict Rules; 8.5 Scoop Design; 9.2 Collection Home |  |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | full | 8.5 Scoop Design |  |
| PRD-030 | Keep Ask and Alchemy state session-only | important | full | 8.4 Ask Chat Design; 13. State Management and Caching Plan |  |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | full | 7.1 Responsibilities; 8.7 Recommendation Design; 10. Business Rules Implementation Checklist |  |
| PRD-032 | Show collection and rating tile indicators | important | full | 9.2 Collection Home; 10. Business Rules Implementation Checklist |  |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | full | 4.2 Primary Entities; 4.4 Merge and Conflict Rules; 10. Business Rules Implementation Checklist |  |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | full | 14. Migration and Continuity Plan |  |
| PRD-035 | Persist synced settings, local settings, UI state | important | full | 4.2 Primary Entities |  |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | full | 4.1 Core Persistence Strategy; 4.3 Supporting Persistence Decisions; 7.2 Mapping Layer |  |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | full | 4.4 Merge and Conflict Rules |  |
| PRD-038 | Provide filters panel and main screen destinations | important | full | 9.1 App Shell and Navigation; 9.3 Filters and Sidebar |  |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | full | 9.1 App Shell and Navigation |  |
| PRD-040 | Keep Settings in persistent primary navigation | important | full | 9.1 App Shell and Navigation |  |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | 3.2 Major Layers; 9.1 App Shell and Navigation |  |
| PRD-042 | Show only library items matching active filters | important | full | 9.2 Collection Home; 9.3 Filters and Sidebar |  |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | 9.2 Collection Home |  |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | full | 9.3 Filters and Sidebar |  |
| PRD-045 | Render poster, title, and My Data badges | important | partial | 9.2 Collection Home; 12.2 Shared Components | The plan calls for show tiles and badges but does not explicitly specify that Home tiles always render poster and title alongside those badges. |
| PRD-046 | Provide empty-library and empty-filter states | detail | full | 9.2 Collection Home |  |
| PRD-047 | Search by title or keywords | important | full | 9.4 Search |  |
| PRD-048 | Use poster grid with collection markers | important | full | 9.4 Search |  |
| PRD-049 | Auto-open Search when setting is enabled | detail | full | 9.4 Search; 9.10 Settings and Your Data |  |
| PRD-050 | Keep Search non-AI in tone | important | partial | 9.4 Search | Search is planned as a catalog mode, but the plan never explicitly preserves the non-AI tone requirement from the voice spec. |
| PRD-051 | Preserve Show Detail narrative section order | important | partial | 9.5 Show Detail | The plan captures most sections but collapses toolbar controls and tag placement into a different sequence than the required narrative hierarchy. |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | full | 9.5 Show Detail; 15.5 Manual QA Matrix |  |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | full | 9.5 Show Detail |  |
| PRD-054 | Place status/interest controls in toolbar | important | full | 3.3 Suggested Directory Structure; 9.5 Show Detail |  |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | 9.5 Show Detail |  |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | 9.5 Show Detail |  |
| PRD-057 | Show overview early for fast scanning | important | full | 9.5 Show Detail |  |
| PRD-058 | Scoop shows correct states and progressive feedback | important | full | 8.5 Scoop Design; 9.5 Show Detail |  |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | full | 9.5 Show Detail |  |
| PRD-060 | Include traditional recommendations strand | important | full | 9.5 Show Detail |  |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | partial | 9.8 Explore Similar | The plan covers concept selection and recommendation generation but does not explicitly preserve the CTA-first "Get Concepts" then "Explore Shows" interaction framing. |
| PRD-062 | Include streaming availability and person-linking credits | important | full | 9.5 Show Detail; 9.9 Person Detail |  |
| PRD-063 | Gate seasons to TV and financials to movies | important | full | 9.5 Show Detail; 15.5 Manual QA Matrix |  |
| PRD-064 | Keep primary actions early and page not overwhelming | important | full | 12.1 Visual and Interaction Priorities; 18. Risks and Mitigations |  |
| PRD-065 | Provide conversational Ask chat interface | important | full | 9.6 Ask |  |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | full | 8.2 Shared AI Contracts; 15.4 AI Quality Validation |  |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | 9.6 Ask |  |
| PRD-068 | Open Detail from mentions or Search fallback | important | full | 9.6 Ask |  |
| PRD-069 | Show six random starter prompts with refresh | important | full | 9.6 Ask |  |
| PRD-070 | Summarize older turns while preserving voice | important | full | 8.3 Context Assembly; 8.4 Ask Chat Design |  |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | full | 9.5 Show Detail; 8.3 Context Assembly |  |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | full | 8.4 Ask Chat Design |  |
| PRD-073 | Retry malformed mention output once, then fallback | important | full | 8.4 Ask Chat Design |  |
| PRD-074 | Redirect Ask back into TV/movie domain | important | partial | 8.2 Shared AI Contracts | The plan restricts Ask to TV and movies, but it does not specify the redirect-back behavior when users push the chat outside that domain. |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | partial | 8.2 Shared AI Contracts; 8.6 Concepts Design | The plan emphasizes specific concept axes, but it never explicitly states that concepts are taste ingredients rather than disguised genres. |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | full | 8.6 Concepts Design; 15.4 AI Quality Validation |  |
| PRD-077 | Order concepts by strongest aha and varied axes | important | full | 8.6 Concepts Design |  |
| PRD-078 | Require concept selection and guide ingredient picking | important | partial | 9.7 Alchemy; 9.8 Explore Similar | The plan requires concept selection, but it never includes the UX guidance or copy that tells users to pick the ingredients they want more of. |
| PRD-079 | Return exactly five Explore Similar recommendations | important | full | 8.7 Recommendation Design; 9.8 Explore Similar |  |
| PRD-080 | Support full Alchemy loop with chaining | important | full | 9.7 Alchemy |  |
| PRD-081 | Clear downstream results when inputs change | important | full | 9.7 Alchemy; 9.5 Show Detail |  |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | partial | 8.6 Concepts Design; 9.7 Alchemy | The plan requires shared multi-show concepts, but it does not plan the larger option pool that the concept-system spec calls for in Alchemy. |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | full | 8.7 Recommendation Design; 9.7 Alchemy; 9.8 Explore Similar |  |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | full | 8.7 Recommendation Design; 15.4 AI Quality Validation |  |
| PRD-085 | Keep one consistent AI persona across surfaces | important | full | 8.2 Shared AI Contracts; 8.8 AI Provider Abstraction |  |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | full | 8.1 AI Surfaces to Implement; 8.2 Shared AI Contracts; 8.8 AI Provider Abstraction |  |
| PRD-087 | Make AI warm, joyful, and light in critique | important | partial | 8.2 Shared AI Contracts | The plan names warmth and playfulness, but it does not explicitly preserve the spec's joy-forward tone and light-touch criticism balance. |
| PRD-088 | Structure Scoop as personal taste mini-review | important | full | 8.5 Scoop Design |  |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | full | 8.4 Ask Chat Design; 15.4 AI Quality Validation |  |
| PRD-090 | Feed AI the right surface-specific context inputs | important | full | 8.3 Context Assembly |  |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | partial | 15.4 AI Quality Validation | The plan includes quality checks, but it never commits to the rubric thresholds or the non-negotiable hard-fail for real-show integrity. |
| PRD-092 | Show person gallery, name, and bio | important | full | 9.9 Person Detail |  |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | full | 9.9 Person Detail |  |
| PRD-094 | Group filmography by year | important | full | 9.9 Person Detail |  |
| PRD-095 | Open Show Detail from selected credit | important | full | 9.9 Person Detail |  |
| PRD-096 | Include font size and Search-on-launch settings | important | full | 9.10 Settings and Your Data |  |
| PRD-097 | Support username, model, and API-key settings safely | important | full | 9.10 Settings and Your Data; 5.3 Security and Access |  |
| PRD-098 | Export saved shows and My Data as zip | critical | full | 4.6 Export Semantics; 9.10 Settings and Your Data |  |
| PRD-099 | Encode export dates using ISO-8601 | important | full | 4.6 Export Semantics |  |

## 3. Coverage Scores

Overall score:

```
(86 × 1.0 + 12 × 0.5) / 99 × 100 = 92.93%
```

Score by severity tier:

```
Critical:  (29 × 1.0 + 1 × 0.5) / 30 × 100 = 98.33%  (29.5 of 30 critical requirements)
Important: (55 × 1.0 + 11 × 0.5) / 67 × 100 = 90.30%  (60.5 of 67 important requirements)
Detail:    (2 × 1.0 + 0 × 0.5) / 2 × 100 = 100.00%  (2 of 2 detail requirements)
Overall:   92.93% (99 total requirements)
```

## 4. Top Gaps

- `PRD-002` | `critical` | Use Supabase official client libraries: The plan commits to Supabase at a platform level but leaves the access mechanism open, which could produce a benchmark-incompatible implementation even if the rest of the architecture is sound.
- `PRD-017` | `important` | Avoid Docker requirement for cloud-agent compatibility: Without an explicit no-Docker path, the implementation could accidentally depend on local container tooling and fail in the benchmark's hosted-agent environment.
- `PRD-091` | `important` | Validate discovery with rubric and hard-fail integrity: The plan proposes AI quality checks, but without explicit thresholds and a hard failure on real-show integrity, regressions could slip through while still appearing "tested."
- `PRD-051` | `important` | Preserve Show Detail narrative section order: The Detail page is the product's emotional center, so losing the intended hierarchy would make the experience feel functionally complete but noticeably less polished and on-brand.
- `PRD-082` | `important` | Generate shared multi-show concepts with larger option pool: If Alchemy uses the same narrow concept pool as single-show exploration, the core multi-input blending feature becomes less varied, less steerable, and less distinctive.

## 5. Coverage Narrative

### Overall Posture

This is a strong implementation plan with minor but meaningful gaps. It is structurally sound, benchmark-aware, and concrete on data ownership, persistence, AI contracts, and major user flows, but it underspecifies a handful of evaluator-sensitive baseline rules and experience-shaping UX details.

### Strength Clusters

The plan is strongest in Benchmark Runtime & Isolation, Collection Data & Persistence, Ask Chat, and Settings & Export. It is especially concrete on namespace and `user_id` scoping, save/remove semantics, timestamp-based merge behavior, structured Ask output, session-only AI state, export behavior, migration safety, and automated test coverage.

### Weakness Clusters

The weaker spots cluster around spec-fidelity details rather than core architecture. Most partial or missing items sit in three patterns: benchmark baseline compliance details (`official` Supabase clients and no-Docker expectations), fine-grained Show Detail and Explore Similar interaction choreography, and AI behavior quality nuances such as voice posture, domain redirection, and explicit rubric thresholds.

### Risk Assessment

If this plan were executed as-is, the first failure mode would likely be subtle spec drift rather than a broken app. A reviewer or QA pass would probably notice that the Detail page and concept flows feel close but not exact, while evaluator checks could also flag infrastructure drift if the implementation quietly chooses non-official Supabase access or introduces Docker assumptions.

### Remediation Guidance

The remaining work is mostly tighter planning, not new architecture. Add a short benchmark compliance subsection that locks in official Supabase clients and cloud-agent-safe execution, a spec-fidelity subsection for Detail and Explore Similar interaction order/copy, and explicit AI acceptance criteria that codify domain redirection plus the discovery rubric thresholds and hard-fail integrity rule.
