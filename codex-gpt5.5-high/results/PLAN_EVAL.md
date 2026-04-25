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
| PRD-001 | Use Next.js latest stable runtime | critical | full | `1. Planning Basis`; `3.1 Application Stack` | |
| PRD-002 | Use Supabase official client libraries | critical | full | `1. Planning Basis`; `3.1 Application Stack` | |
| PRD-003 | Ship `.env.example` with required variables | critical | full | `3.2 Required Repo Deliverables` | |
| PRD-004 | Ignore `.env*` secrets except example | important | full | `3.2 Required Repo Deliverables` | |
| PRD-005 | Configure build through env without code edits | critical | full | `1. Planning Basis`; `10.1 Milestone 1` acceptance | |
| PRD-006 | Keep secrets out of repo and server-only | critical | full | `1. Planning Basis`; `13. Security and Privacy` | |
| PRD-007 | Provide app, test, reset command scripts | critical | full | `3.2 Required Repo Deliverables`; `10.1 Milestone 1` acceptance | |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | `3.2 Required Repo Deliverables`; `5.1 Supabase Tables` | |
| PRD-009 | Use one stable namespace per build | critical | full | `3.3 Development Identity` | |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | `5.2 Row-Level Security and Scoping`; `10.2 Milestone 2` | |
| PRD-011 | Attach every user record to `user_id` | critical | full | `1. Planning Basis`; `5.1 Supabase Tables` | |
| PRD-012 | Partition persisted data by namespace and user | critical | full | `1. Planning Basis`; `5.2 Row-Level Security and Scoping` | |
| PRD-013 | Support documented dev auth injection, prod-gated | important | partial | `3.2 Required Repo Deliverables`; `3.3 Development Identity` | The plan documents dev identity injection options but does not define how those paths are explicitly gated or disabled in production. |
| PRD-014 | Real OAuth later needs no schema redesign | important | full | `3.3 Development Identity`; `13. Security and Privacy` | |
| PRD-015 | Keep backend as persisted source of truth | critical | full | `1. Planning Basis`; `10.2 Milestone 2` acceptance | |
| PRD-016 | Make client cache safe to discard | critical | full | `5.1 Optional user_preferences`; `10.2 Milestone 2` acceptance | |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | partial | `3.2 Required Repo Deliverables`; `10.11 Milestone 11` acceptance | The plan leans on hosted Supabase, but it never states outright that Docker must remain optional and not required. |
| PRD-018 | Overlay saved user data on every show appearance | critical | full | `2. Product Interpretation`; `6.2 Mapping Rules`; `10.3 Milestone 3` | |
| PRD-019 | Support visible statuses plus hidden `Next` | important | partial | `15. Open Questions and Recommended Defaults` | `Next` is only handled as a recommended default, not as a committed schema and behavior thread throughout the implementation plan. |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | full | `8.7 Show Detail` toolbar controls; `9. Business Rules Checklist` | |
| PRD-021 | Support free-form multi-tag personal tag library | important | full | `5.1 shows`; `8.7 My Tags`; `10.5 Milestone 5` | |
| PRD-022 | Define collection membership by assigned status | critical | full | `2. Product Interpretation`; `9. Business Rules Checklist` | |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | full | `2. Product Interpretation`; `9. Business Rules Checklist` | |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | `8.7 Show Detail` controls; `9. Business Rules Checklist`; `11.1 Unit Tests` | |
| PRD-025 | Removing status deletes show and all My Data | critical | full | `5.4 Data Removal`; `8.7 Show Detail` controls | |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | full | `5.3 Merge Rules`; `9. Business Rules Checklist` | |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | `5.1 shows`; `9. Business Rules Checklist` | |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | partial | `5.3 Merge Rules`; `7.4 Scoop`; `10.10 Milestone 10` acceptance | The plan uses timestamps for merge logic and Scoop freshness, but it does not explicitly plan recency sorting or broader sync semantics. |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | full | `2. Product Interpretation`; `7.4 Scoop`; `9. Business Rules Checklist` | |
| PRD-030 | Keep Ask and Alchemy state session-only | important | full | `7.3 Ask`; `8.5 Ask`; `9. Business Rules Checklist` | |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | full | `7.6 Explore Similar and Alchemy Recommendations`; `10.8 Milestone 8` acceptance | |
| PRD-032 | Show collection and rating tile indicators | important | full | `6.2 Mapping Rules`; `8.2 Collection Home`; `8.4 Search` | |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | partial | `5.1 cloud_settings`; `5.1 Optional user_preferences`; `10.10 Milestone 10` acceptance | Settings persistence is planned, but duplicate-show merging and a concrete cross-device library sync contract are not. |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | partial | `5.1 app_metadata`; `14. Data Export Shape` | The plan tracks model versioning, but it never defines the migration path that would preserve existing libraries across schema upgrades. |
| PRD-035 | Persist synced settings, local settings, UI state | important | full | `5.1 Optional user_preferences`; `10.10 Milestone 10` acceptance | |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | full | `5.1 shows`; `6.2 Mapping Rules` | |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | full | `5.3 Merge Rules`; `11.1 Unit Tests` | |
| PRD-038 | Provide filters panel and main screen destinations | important | full | `8.1 Global Layout` | |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | full | `8.1 Global Layout` | |
| PRD-040 | Keep Settings in persistent primary navigation | important | full | `8.1 Global Layout` | |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | `8.3 Find / Discover Hub` | |
| PRD-042 | Show only library items matching active filters | important | full | `8.2 Collection Home` | |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | `8.2 Collection Home` | |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | full | `8.2 Collection Home` filters; `10.4 Milestone 4` | |
| PRD-045 | Render poster, title, and My Data badges | important | full | `8.2 Collection Home` | |
| PRD-046 | Provide empty-library and empty-filter states | detail | full | `8.2 Collection Home` | |
| PRD-047 | Search by title or keywords | important | full | `8.4 Search` | |
| PRD-048 | Use poster grid with collection markers | important | full | `8.4 Search` | |
| PRD-049 | Auto-open Search when setting is enabled | detail | full | `8.3 Find / Discover Hub` | |
| PRD-050 | Keep Search non-AI in tone | important | full | `8.4 Search` | |
| PRD-051 | Preserve Show Detail narrative section order | important | full | `8.7 Show Detail` section order | |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | full | `8.7 Show Detail` section order | |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | full | `8.7 Show Detail` section order | |
| PRD-054 | Place status/interest controls in toolbar | important | full | `8.7 Show Detail` toolbar controls | |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | `8.7 Show Detail` toolbar controls; `9. Business Rules Checklist` | |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | `8.7 Show Detail` toolbar controls; `9. Business Rules Checklist` | |
| PRD-057 | Show overview early for fast scanning | important | full | `8.7 Show Detail` section order | |
| PRD-058 | Scoop shows correct states and progressive feedback | important | full | `8.7 Scoop states`; `7.4 Scoop` | |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | full | `8.5 Ask`; `8.7 Ask about this show CTA`; `10.6 Milestone 6` | |
| PRD-060 | Include traditional recommendations strand | important | full | `8.7 Traditional recommendations strand`; `10.5 Milestone 5` | |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | full | `8.7 Explore Similar states` | |
| PRD-062 | Include streaming availability and person-linking credits | important | full | `8.7 Streaming availability`; `Cast and Crew`; `8.8 Person Detail` | |
| PRD-063 | Gate seasons to TV and financials to movies | important | full | `8.7 Seasons for TV`; `Budget/Revenue for movies` | |
| PRD-064 | Keep primary actions early and page not overwhelming | important | full | `8.7 Show Detail` section order; `16. Risk Areas` | |
| PRD-065 | Provide conversational Ask chat interface | important | full | `8.5 Ask`; `10.6 Milestone 6` | |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | partial | `7.2 Shared AI Guardrails`; `8.5 Ask` | The plan covers spoiler safety and general tone, but it does not make Ask's direct, confident answer shape an explicit requirement or acceptance check. |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | `8.5 Ask` | |
| PRD-068 | Open Detail from mentions or Search fallback | important | full | `7.3 Ask` parser behavior; `8.5 Ask` | |
| PRD-069 | Show six random starter prompts with refresh | important | full | `8.5 Ask` | |
| PRD-070 | Summarize older turns while preserving voice | important | full | `7.3 Ask`; `10.6 Milestone 6` | |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | full | `8.5 Ask`; `8.7 Ask about this show CTA` | |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | full | `7.3 Ask` structured output | |
| PRD-073 | Retry malformed mention output once, then fallback | important | full | `7.3 Ask` parser behavior; `12. Error Handling and Fallbacks` | |
| PRD-074 | Redirect Ask back into TV/movie domain | important | full | `7.2 Shared AI Guardrails` | |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | full | `7.5 Concepts` | |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | full | `7.5 Concepts`; `11.4 AI Quality Tests` | |
| PRD-077 | Order concepts by strongest aha and varied axes | important | full | `7.5 Concepts` | |
| PRD-078 | Require concept selection and guide ingredient picking | important | partial | `8.6 Alchemy flow`; `8.7 Explore Similar states` | The interaction flow requires concept selection, but the plan omits the copy and guidance that helps users choose the intended taste ingredients. |
| PRD-079 | Return exactly five Explore Similar recommendations | important | full | `7.6 Explore Similar`; `8.7 Explore Similar states` | |
| PRD-080 | Support full Alchemy loop with chaining | important | full | `8.6 Alchemy flow`; `10.8 Milestone 8` | |
| PRD-081 | Clear downstream results when inputs change | important | full | `8.6 Alchemy` rules; `11.1 Unit Tests` | |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | partial | `7.5 Concepts`; `10.8 Milestone 8` | The plan requires shared multi-show concepts, but it does not plan the larger concept option pool called for in the supporting spec. |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | full | `7.6 Explore Similar and Alchemy Recommendations`; `10.8 Milestone 8` acceptance | |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | full | `7.7 AI Quality Validation`; `11.4 AI Quality Tests` | |
| PRD-085 | Keep one consistent AI persona across surfaces | important | full | `7.2 Shared AI Guardrails` | |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | full | `7.2 Shared AI Guardrails` | |
| PRD-087 | Make AI warm, joyful, and light in critique | important | partial | `7.2 Shared AI Guardrails`; `7.4 Scoop` | Warm/playful tone is preserved, but the plan does not explicitly lock in joy-forward delivery and light-touch critique. |
| PRD-088 | Structure Scoop as personal taste mini-review | important | full | `7.4 Scoop` | |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | partial | `7.3 Ask`; `8.5 Ask` | The plan covers Ask mechanics and context, but not the default response brevity and dialogue cadence described in the persona spec. |
| PRD-090 | Feed AI the right surface-specific context inputs | important | full | `7.1 Provider Abstraction`; `7.3 Ask`; `7.6 Explore Similar and Alchemy Recommendations` | |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | full | `7.7 AI Quality Validation`; `11.4 AI Quality Tests` | |
| PRD-092 | Show person gallery, name, and bio | important | full | `8.8 Person Detail`; `10.9 Milestone 9` | |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | full | `8.8 Person Detail` | |
| PRD-094 | Group filmography by year | important | full | `8.8 Person Detail`; `10.9 Milestone 9` | |
| PRD-095 | Open Show Detail from selected credit | important | full | `8.8 Person Detail`; `10.9 Milestone 9` acceptance | |
| PRD-096 | Include font size and Search-on-launch settings | important | full | `8.9 Settings and Your Data`; `10.10 Milestone 10` | |
| PRD-097 | Support username, model, and API-key settings safely | important | full | `8.9 Settings and Your Data`; `13. Security and Privacy` | |
| PRD-098 | Export saved shows and My Data as zip | critical | full | `8.9 Settings and Your Data`; `14. Data Export Shape` | |
| PRD-099 | Encode export dates using ISO-8601 | important | full | `8.9 Settings and Your Data`; `14. Data Export Shape` | |

### 3. Coverage Scores

Critical:  (29 × 1.0 + 1 × 0.5) / 30 × 100 = 98.33%  (29.5 of 30 critical requirements)
Important: (57 × 1.0 + 10 × 0.5) / 67 × 100 = 92.54%  (62.0 of 67 important requirements)
Detail:    (2 × 1.0 + 0 × 0.5) / 2 × 100 = 100.00%  (2.0 of 2 detail requirements)
Overall:   (88 × 1.0 + 11 × 0.5) / 99 × 100 = 94.44%  (93.5 of 99 total requirements)

### 4. Top Gaps

1. `PRD-034` | `critical` | Preserve saved libraries across data-model upgrades
Without an explicit upgrade/migration plan, a future schema change could strand or silently drop saved collections, which would be a direct trust failure for the product's core promise.

2. `PRD-033` | `important` | Sync libraries/settings consistently and merge duplicates
The plan covers settings persistence but not library-sync duplicate handling, so a multi-device or sync-enabled implementation could surface duplicate records or conflicting overlays with no defined resolution path.

3. `PRD-066` | `important` | Answer directly with confident, spoiler-safe recommendations
Ask is central to discovery, and if the plan never converts this into a concrete behavior bar, the shipped experience can become vague or over-explanatory while still looking superficially compliant.

4. `PRD-082` | `important` | Generate shared multi-show concepts with larger option pool
Alchemy quality depends on enough shared concept candidates to let users steer the blend; without that larger pool, the flow risks feeling repetitive or underfit for multi-show inputs.

5. `PRD-013` | `important` | Support documented dev auth injection, prod-gated
The benchmark allows injected identity, but if the production gate is underspecified, the implementation can accidentally normalize a dev-only trust path into deployable behavior.

### 5. Coverage Narrative

#### Overall Posture

This is a strong plan with a high coverage baseline and only a limited number of substantive gaps. It captures the benchmark runtime constraints, the collection model, the show-detail relationship mechanics, and most AI and discovery flows with enough specificity to guide implementation. The remaining issues are mostly around long-term data continuity, sync semantics, and a few tighter AI behavior contracts rather than missing product pillars.

#### Strength Clusters

The plan is strongest in Benchmark Runtime & Isolation, Show Detail & Relationship UX, Collection Home & Search, and Settings & Export. Those areas have concrete architecture, persistence, feature-flow, and testing language, and the plan consistently ties them back to acceptance criteria and specific business rules. Collection data handling is also broadly strong where it deals with save triggers, overlay rules, timestamps, and removal semantics.

#### Weakness Clusters

The gaps cluster in two places. One cluster is data lifecycle work inside Collection Data & Persistence: sync behavior, duplicate handling, upgrade continuity, and a few timestamp use cases are lighter than the rest of the plan. The second cluster is AI craft in Ask and Alchemy: the plan handles APIs, parsing, and resolution well, but some product-facing quality contracts such as direct Ask answers, joy-forward tone, brisk dialogue cadence, ingredient-guidance copy, and the larger multi-show concept pool are not carried through with the same rigor.

#### Risk Assessment

If this plan were executed as-is, the most likely first visible issue would not be a missing page or route. It would be behavior that feels slightly off under stress: synced data duplicating or drifting, a future schema change lacking a safe upgrade path, or AI surfaces that technically work but miss the intended confidence and conversational sharpness. A QA reviewer would probably first notice that the app is structurally complete yet underspecified in the exact places where continuity and taste-aware quality need hard behavioral contracts.

#### Remediation Guidance

The data-lifecycle gaps need explicit planning work around migration strategy, sync conflict handling, duplicate detection, and the exact responsibilities of timestamp fields beyond merge freshness. The AI gaps need tighter acceptance criteria, not new architecture: define response-shape expectations for Ask, make the persona constraints testable, add the missing concept-selection guidance, and specify the larger option pool for multi-show concept generation so Alchemy quality is protected by design rather than intent.
