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
| PRD-001 | Use Next.js latest stable runtime | critical | full | 2. Technology Stack | |
| PRD-002 | Use Supabase official client libraries | critical | full | 2. Technology Stack | |
| PRD-003 | Ship `.env.example` with required variables | critical | full | 3. Repository Structure; 4. Environment Variables | |
| PRD-004 | Ignore `.env*` secrets except example | important | full | 3. Repository Structure; 4. Environment Variables | |
| PRD-005 | Configure build through env without code edits | critical | full | 4. Environment Variables | |
| PRD-006 | Keep secrets out of repo and server-only | critical | full | 4. Environment Variables; 8.1 Server Route Handlers | |
| PRD-007 | Provide app, test, reset command scripts | critical | full | 7. NPM Scripts | |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | 3. Repository Structure; 5.3 Migration Strategy | |
| PRD-009 | Use one stable namespace per build | critical | full | 6.1 Namespace | |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | 5.3 Migration Strategy; 6.1 Namespace | |
| PRD-011 | Attach every user record to `user_id` | critical | full | 5.1 Core Tables | |
| PRD-012 | Partition persisted data by namespace and user | critical | full | 5.1 Core Tables; 5.2 Row-Level Security | |
| PRD-013 | Support documented dev auth injection, prod-gated | important | full | 6.2 User Identity (Dev Mode); 15. Phase 7 - Settings + Export + Polish | |
| PRD-014 | Real OAuth later needs no schema redesign | important | full | 5.2 Row-Level Security; 6.3 Production Migration Path | |
| PRD-015 | Keep backend as persisted source of truth | critical | full | 8.3 Client-Side Caching; 12. Cross-Cutting Rules Implementation | |
| PRD-016 | Make client cache safe to discard | critical | full | 8.3 Client-Side Caching | |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | full | 2. Technology Stack | |
| PRD-018 | Overlay saved user data on every show appearance | critical | partial | 10.2 Search; 12. Cross-Cutting Rules Implementation | The plan states precedence and search markers, but it does not specify full My Data overlay behavior for every show surface and AI output. |
| PRD-019 | Support visible statuses plus hidden `Next` | important | full | 9.1 Status System | |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | full | 9.2 Saving Triggers & Defaults | |
| PRD-021 | Support free-form multi-tag personal tag library | important | partial | 10.1 Collection Home; 10.5 Show Detail Page | Tags exist in storage and filters, but the plan does not define free-form tag creation and library-management behavior in detail. |
| PRD-022 | Define collection membership by assigned status | critical | full | 9.2 Saving Triggers & Defaults; 9.3 Removal Semantics | |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | full | 9.2 Saving Triggers & Defaults | |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | 9.2 Saving Triggers & Defaults | |
| PRD-025 | Removing status deletes show and all My Data | critical | full | 9.3 Removal Semantics | |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | full | 8.2 Merge Logic (Show Upsert) | |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | 5.1 Core Tables | |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | partial | 10.5 Show Detail Page; 13. Data Sync & Conflict Resolution | Freshness and conflict resolution are planned, but timestamp-driven sorting behavior is not specified. |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | full | 10.5 Show Detail Page | |
| PRD-030 | Keep Ask and Alchemy state session-only | important | partial | 10.3 Ask; 10.4 Alchemy | Alchemy is explicitly session-only, but Ask is not explicitly defined to clear on leave/reset and avoid persistence beyond the live session. |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | full | 11.4 Recommendation Resolution | |
| PRD-032 | Show collection and rating tile indicators | important | full | 9.4 Tile Indicators | |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | full | 13. Data Sync & Conflict Resolution; 10.7 Settings & Your Data | |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | full | 14. Data Model Migration | |
| PRD-035 | Persist synced settings, local settings, UI state | important | full | 9.3 Removal Semantics; 10.1 Collection Home; 10.7 Settings & Your Data | |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | full | 5.1 Core Tables; 10.5 Show Detail Page | |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | full | 8.2 Merge Logic (Show Upsert) | |
| PRD-038 | Provide filters panel and main screen destinations | important | full | 3. Repository Structure; 10.1 Collection Home | |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | partial | 3. Repository Structure | The route/layout structure implies Find exists, but the plan does not explicitly require it to remain persistently visible in primary navigation. |
| PRD-040 | Keep Settings in persistent primary navigation | important | partial | 3. Repository Structure | The route/layout structure implies Settings exists, but the plan does not explicitly require it to remain persistently visible in primary navigation. |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | 3. Repository Structure; 10.2 Search; 10.3 Ask; 10.4 Alchemy | |
| PRD-042 | Show only library items matching active filters | important | full | 10.1 Collection Home | |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | 10.1 Collection Home | |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | full | 10.1 Collection Home | |
| PRD-045 | Render poster, title, and My Data badges | important | full | 10.1 Collection Home | |
| PRD-046 | Provide empty-library and empty-filter states | detail | full | 10.1 Collection Home | |
| PRD-047 | Search by title or keywords | important | full | 10.2 Search | |
| PRD-048 | Use poster grid with collection markers | important | full | 10.2 Search | |
| PRD-049 | Auto-open Search when setting is enabled | detail | full | 10.2 Search; 10.7 Settings & Your Data | |
| PRD-050 | Keep Search non-AI in tone | important | full | 10.2 Search | |
| PRD-051 | Preserve Show Detail narrative section order | important | full | 10.5 Show Detail Page | |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | full | 10.5 Show Detail Page | |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | full | 10.5 Show Detail Page | |
| PRD-054 | Place status/interest controls in toolbar | important | full | 10.5 Show Detail Page | |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | 9.2 Saving Triggers & Defaults; 10.5 Show Detail Page | |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | 9.2 Saving Triggers & Defaults; 10.5 Show Detail Page | |
| PRD-057 | Show overview early for fast scanning | important | full | 10.5 Show Detail Page | |
| PRD-058 | Scoop shows correct states and progressive feedback | important | full | 10.5 Show Detail Page | |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | full | 10.3 Ask; 10.5 Show Detail Page | |
| PRD-060 | Include traditional recommendations strand | important | full | 10.5 Show Detail Page | |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | full | 10.5 Show Detail Page | |
| PRD-062 | Include streaming availability and person-linking credits | important | full | 10.5 Show Detail Page | |
| PRD-063 | Gate seasons to TV and financials to movies | important | full | 10.5 Show Detail Page | |
| PRD-064 | Keep primary actions early and page not overwhelming | important | partial | 10.5 Show Detail Page | The order brings actions early, but the plan does not specify concrete anti-clutter rules to keep the page powerful without feeling busy. |
| PRD-065 | Provide conversational Ask chat interface | important | full | 10.3 Ask | |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | partial | 10.3 Ask; 11.2 AI Personality | The tone contract is covered, but the plan does not require Ask to answer directly within the opening lines. |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | 10.3 Ask | |
| PRD-068 | Open Detail from mentions or Search fallback | important | partial | 10.3 Ask; 11.4 Recommendation Resolution | The resolution engine is defined, but the tap path from a mentioned show into Detail versus Search fallback is only implied. |
| PRD-069 | Show six random starter prompts with refresh | important | full | 10.3 Ask | |
| PRD-070 | Summarize older turns while preserving voice | important | full | 10.3 Ask | |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | full | 10.3 Ask | |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | full | 10.3 Ask; 11.3 Structured Output for Ask | |
| PRD-073 | Retry malformed mention output once, then fallback | important | full | 11.3 Structured Output for Ask | |
| PRD-074 | Redirect Ask back into TV/movie domain | important | missing | none | The plan never states that Ask must redirect out-of-domain prompts back into TV/movie discovery. |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | partial | 10.4 Alchemy; 11.2 AI Personality | The plan supports concepts and ingredient-style selection, but it does not explicitly forbid genre-like concepts as a planning constraint. |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | partial | 11.2 AI Personality | The format and length are specified, but the plan does not explicitly require rejection of generic concept outputs. |
| PRD-077 | Order concepts by strongest aha and varied axes | important | missing | none | The plan does not define ordering concepts by strongest aha or enforcing variety across structure, vibe, emotion, and craft axes. |
| PRD-078 | Require concept selection and guide ingredient picking | important | partial | 10.4 Alchemy; 10.5 Show Detail Page | Selection is required, but the UX guidance to help users pick ingredients is not specified. |
| PRD-079 | Return exactly five Explore Similar recommendations | important | full | 10.5 Show Detail Page; 11.5 Concept Generation Counts | |
| PRD-080 | Support full Alchemy loop with chaining | important | full | 10.4 Alchemy | |
| PRD-081 | Clear downstream results when inputs change | important | full | 10.4 Alchemy | |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | full | 10.4 Alchemy; 11.5 Concept Generation Counts | |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | full | 11.2 AI Personality | |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | partial | 12. Cross-Cutting Rules Implementation; 15. Phase 8 - Tests + QA | Taste-aware inputs and rubric checks are planned, but surprise-without-betrayal is not turned into a concrete generation constraint. |
| PRD-085 | Keep one consistent AI persona across surfaces | important | full | 11.2 AI Personality | |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | partial | 11.2 AI Personality; 12. Cross-Cutting Rules Implementation | Shared persona and spoiler rules are planned, but the full shared guardrail set is not codified across every AI surface, especially domain redirection and specificity constraints. |
| PRD-087 | Make AI warm, joyful, and light in critique | important | full | 11.2 AI Personality | |
| PRD-088 | Structure Scoop as personal taste mini-review | important | full | 10.5 Show Detail Page; 11.2 AI Personality | |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | full | 11.2 AI Personality | |
| PRD-090 | Feed AI the right surface-specific context inputs | important | full | 10.3 Ask; 10.4 Alchemy; 12. Cross-Cutting Rules Implementation | |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | partial | 15. Phase 8 - Tests + QA | The plan schedules rubric-based QA, but it does not specify pass thresholds or a hard-fail rule for real-show integrity. |
| PRD-092 | Show person gallery, name, and bio | important | full | 10.6 Person Detail Page | |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | full | 10.6 Person Detail Page | |
| PRD-094 | Group filmography by year | important | full | 10.6 Person Detail Page | |
| PRD-095 | Open Show Detail from selected credit | important | full | 10.6 Person Detail Page | |
| PRD-096 | Include font size and Search-on-launch settings | important | full | 10.7 Settings & Your Data | |
| PRD-097 | Support username, model, and API-key settings safely | important | full | 10.7 Settings & Your Data; 11.1 Server-Side AI Client | |
| PRD-098 | Export saved shows and My Data as zip | critical | full | 10.7 Settings & Your Data | |
| PRD-099 | Encode export dates using ISO-8601 | important | full | 10.7 Settings & Your Data | |

### 3. Coverage Scores

Overall score:

`score = (82 * 1.0 + 15 * 0.5) / 99 * 100 = 90.40%`

Critical:  `(28 * 1.0 + 2 * 0.5) / 30 * 100 = 96.67%`  (29 of 30 critical requirements)
Important: `(52 * 1.0 + 13 * 0.5) / 67 * 100 = 87.31%`  (58.5 of 67 important requirements)
Detail:    `(2 * 1.0 + 0 * 0.5) / 2 * 100 = 100.00%`  (2 of 2 detail requirements)
Overall:   `(82 * 1.0 + 15 * 0.5) / 99 * 100 = 90.40%`  (89.5 of 99 total requirements)

### 4. Top Gaps

- `PRD-018` | `critical` | Overlay saved user data on every show appearance: Without one explicit overlay rule across search, recommendations, and AI-derived tiles, the same show can present inconsistent saved-state context depending on where the user encounters it.
- `PRD-086` | `critical` | Enforce shared AI guardrails across all surfaces: The plan covers persona and some safety rules, but leaving the shared guardrails incomplete risks divergent AI behavior between Scoop, Ask, Explore Similar, and Alchemy.
- `PRD-074` | `important` | Redirect Ask back into TV/movie domain: If this is omitted, Ask can drift outside the product's domain and break the app's core promise of focused entertainment discovery.
- `PRD-077` | `important` | Order concepts by strongest aha and varied axes: Without ordering and diversity rules, concepts are likely to become generic or redundant, which weakens both Explore Similar and Alchemy.
- `PRD-091` | `important` | Validate discovery with rubric and hard-fail integrity: If discovery QA lacks explicit pass/fail gates, hallucinated or weakly grounded recommendations can slip through despite the rest of the feature set looking complete.

### 5. Coverage Narrative

#### Overall Posture

This is a strong implementation plan with high critical-requirement coverage and only a small number of outright misses. It is structurally sound for infrastructure, persistence, and core product flows, but it still leaves some important AI-behavior contracts and shell-level UX requirements underspecified.

#### Strength Clusters

The plan is strongest in Benchmark Runtime & Isolation, Collection Data & Persistence, Collection Home & Search, Show Detail & Relationship UX, Person Detail, and Settings & Export. Those areas are covered with concrete schema, routes, save/remove rules, section ordering, and phased delivery details rather than broad intent statements.

#### Weakness Clusters

The gaps cluster around AI behavioral contracts and a smaller set of experience-specification details. Ask/Concept/quality requirements are where most partial or missing items sit, especially around domain guardrails, concept-quality heuristics, and explicit quality gates; outside AI, the remaining gaps are mostly about global show-overlay consistency and persistent navigation wording.

#### Risk Assessment

If this plan were executed as-is, the product would likely feel functionally complete but behaviorally uneven. A stakeholder or QA reviewer would probably notice first that AI surfaces can drift in rules and output quality - for example, Ask not redirecting off-domain prompts, concept lists lacking the intended "aha" ordering, or recommendation quality being checked informally rather than against explicit hard-fail criteria.

#### Remediation Guidance

The remaining work is mostly specification-tightening, not broad replanning. The plan needs a sharper shared AI contract that every surface inherits, explicit acceptance criteria for concept generation and recommendation quality, one reusable rule for overlaying saved My Data on every show render path, and a clearer app-shell/navigation requirement so persistent entry points are unambiguous.
