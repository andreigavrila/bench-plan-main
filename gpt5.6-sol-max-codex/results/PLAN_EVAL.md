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
| PRD-001 | Use Next.js latest stable runtime | critical | full | Section 3.1 Runtime and boundaries; Phase 1 |  |
| PRD-002 | Use Supabase official client libraries | critical | full | Section 3.1 Runtime and boundaries; Section 4.1 Environment contract |  |
| PRD-003 | Ship `.env.example` with required variables | critical | full | Section 4.1 Environment contract |  |
| PRD-004 | Ignore `.env*` secrets except example | important | full | Section 4.1 Environment contract |  |
| PRD-005 | Configure build through env without code edits | critical | full | Section 4.1 Environment contract; Section 12 Definition of Done |  |
| PRD-006 | Keep secrets out of repo and server-only | critical | full | Sections 3.1, 5.3, and 11 |  |
| PRD-007 | Provide app, test, reset command scripts | critical | full | Section 4.1 Environment contract; Phase 1 |  |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | Section 5.8 Migrations and continuity; Phase 2 |  |
| PRD-009 | Use one stable namespace per build | critical | full | Sections 4.2 and 4.3 |  |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | Section 4.3 Namespace-safe destructive testing; Section 10.2 |  |
| PRD-011 | Attach every user record to `user_id` | critical | full | Sections 4.2, 5.1, and 5.3 |  |
| PRD-012 | Partition persisted data by namespace and user | critical | full | Sections 4.2 and 5.1 |  |
| PRD-013 | Support documented dev auth injection, prod-gated | important | full | Section 4.2 Trusted request scope; Phase 7 |  |
| PRD-014 | Real OAuth later needs no schema redesign | important | full | Sections 2 and 4.2 |  |
| PRD-015 | Keep backend as persisted source of truth | critical | full | Section 1 Outcome; Section 5.4 Persistence lifetime matrix |  |
| PRD-016 | Make client cache safe to discard | critical | full | Sections 3.1, 5.4, 10.2, and 12 |  |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | full | Sections 4.1 and 12 |  |
| PRD-018 | Overlay saved user data on every show appearance | critical | full | Sections 1, 5.5, 7.2, and 12 |  |
| PRD-019 | Support visible statuses plus hidden `Next` | important | full | Sections 2, 5.3, 5.7, and 7.3 |  |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | full | Sections 2, 5.7, and 7.7 |  |
| PRD-021 | Support free-form multi-tag personal tag library | important | full | Sections 5.3 and 7.7 |  |
| PRD-022 | Define collection membership by assigned status | critical | full | Section 5.3; Section 12 Definition of Done |  |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | full | Section 5.7 Collection transition service |  |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | Sections 2 and 5.7 |  |
| PRD-025 | Removing status deletes show and all My Data | critical | full | Sections 5.6, 5.7, and 12 |  |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | full | Sections 1, 5.5, and 5.7 |  |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | Sections 5.3 and 5.6 |  |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | full | Sections 5.6, 7.3, and 8.5 |  |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | full | Sections 5.4, 7.7, and 8.5 |  |
| PRD-030 | Keep Ask and Alchemy state session-only | important | full | Sections 5.4, 7.5, and 7.6 |  |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | full | Sections 1 and 8.4 |  |
| PRD-032 | Show collection and rating tile indicators | important | full | Section 7.2 Shared ShowTile and strands |  |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | full | Sections 2, 5.1, 5.3, 5.7, and 10.2 |  |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | full | Sections 5.8 and 10.2 |  |
| PRD-035 | Persist synced settings, local settings, UI state | important | full | Sections 5.3, 5.4, and 7.9 |  |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | full | Sections 5.2 and 6.2 |  |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | full | Sections 5.5 and 5.6 |  |
| PRD-038 | Provide filters panel and main screen destinations | important | full | Section 7.1 App shell and navigation |  |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | full | Section 7.1 App shell and navigation |  |
| PRD-040 | Keep Settings in persistent primary navigation | important | full | Section 7.1 App shell and navigation |  |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | Section 7.4 Find/Discover shell and Search |  |
| PRD-042 | Show only library items matching active filters | important | full | Section 7.3 Collection Home |  |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | Section 7.3 Collection Home |  |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | full | Sections 7.1 and 7.3 |  |
| PRD-045 | Render poster, title, and My Data badges | important | full | Sections 7.2 and 7.3 |  |
| PRD-046 | Provide empty-library and empty-filter states | detail | full | Section 7.3 Collection Home |  |
| PRD-047 | Search by title or keywords | important | full | Sections 6.2 and 7.4 |  |
| PRD-048 | Use poster grid with collection markers | important | full | Sections 7.2 and 7.4 |  |
| PRD-049 | Auto-open Search when setting is enabled | detail | full | Sections 7.1 and 7.9 |  |
| PRD-050 | Keep Search non-AI in tone | important | full | Sections 2, 7.4, and 8.1 |  |
| PRD-051 | Preserve Show Detail narrative section order | important | full | Section 7.7 Show Detail |  |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | full | Section 7.7 Show Detail |  |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | full | Section 7.7 Show Detail |  |
| PRD-054 | Place status/interest controls in toolbar | important | full | Section 7.7 Show Detail |  |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | Sections 5.7 and 7.7 |  |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | Sections 5.7 and 7.7 |  |
| PRD-057 | Show overview early for fast scanning | important | full | Section 7.7 Show Detail |  |
| PRD-058 | Scoop shows correct states and progressive feedback | important | full | Section 7.7 Show Detail |  |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | full | Sections 7.5 and 7.7 |  |
| PRD-060 | Include traditional recommendations strand | important | full | Section 7.7 Show Detail |  |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | full | Section 7.7 Show Detail |  |
| PRD-062 | Include streaming availability and person-linking credits | important | full | Sections 7.7 and 7.8 |  |
| PRD-063 | Gate seasons to TV and financials to movies | important | full | Section 7.7 Show Detail |  |
| PRD-064 | Keep primary actions early and page not overwhelming | important | full | Section 7.7 Show Detail; Section 13 Principal risks |  |
| PRD-065 | Provide conversational Ask chat interface | important | full | Section 7.5 Ask |  |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | full | Sections 8.1 and 8.3 |  |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | Section 7.5 Ask |  |
| PRD-068 | Open Detail from mentions or Search fallback | important | full | Sections 7.5 and 8.4 |  |
| PRD-069 | Show six random starter prompts with refresh | important | full | Section 7.5 Ask |  |
| PRD-070 | Summarize older turns while preserving voice | important | full | Sections 7.5 and 8.3 |  |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | full | Sections 7.5 and 7.7 |  |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | full | Sections 8.3 and 8.4 |  |
| PRD-073 | Retry malformed mention output once, then fallback | important | full | Section 8.4 Parsing and catalog resolution |  |
| PRD-074 | Redirect Ask back into TV/movie domain | important | full | Section 8.1 Shared persona and policy |  |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | full | Sections 7.7 and 8.3 |  |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | full | Section 8.3 Surface contracts |  |
| PRD-077 | Order concepts by strongest aha and varied axes | important | full | Section 8.3 Surface contracts |  |
| PRD-078 | Require concept selection and guide ingredient picking | important | full | Sections 7.6 and 7.7 |  |
| PRD-079 | Return exactly five Explore Similar recommendations | important | full | Sections 7.7 and 8.3 |  |
| PRD-080 | Support full Alchemy loop with chaining | important | full | Section 7.6 Alchemy |  |
| PRD-081 | Clear downstream results when inputs change | important | full | Sections 7.6 and 7.7 |  |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | full | Sections 2 and 8.3 |  |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | full | Sections 7.7 and 8.3 |  |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | full | Sections 8.3 and 10.5 |  |
| PRD-085 | Keep one consistent AI persona across surfaces | important | full | Section 8.1 Shared persona and policy |  |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | full | Sections 8.1 and 8.5 |  |
| PRD-087 | Make AI warm, joyful, and light in critique | important | full | Section 8.1 Shared persona and policy |  |
| PRD-088 | Structure Scoop as personal taste mini-review | important | full | Sections 7.7 and 8.3 |  |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | full | Section 8.3 Surface contracts |  |
| PRD-090 | Feed AI the right surface-specific context inputs | important | full | Section 8.2 Provider and prompt architecture |  |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | full | Sections 8.5 and 10.5 |  |
| PRD-092 | Show person gallery, name, and bio | important | full | Section 7.8 Person Detail |  |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | full | Section 7.8 Person Detail |  |
| PRD-094 | Group filmography by year | important | full | Section 7.8 Person Detail |  |
| PRD-095 | Open Show Detail from selected credit | important | full | Section 7.8 Person Detail |  |
| PRD-096 | Include font size and Search-on-launch settings | important | full | Section 7.9 Settings and Your Data |  |
| PRD-097 | Support username, model, and API-key settings safely | important | full | Sections 5.3 and 7.9 |  |
| PRD-098 | Export saved shows and My Data as zip | critical | full | Section 7.9 Settings and Your Data |  |
| PRD-099 | Encode export dates using ISO-8601 | important | full | Sections 7.9 and 10.1 |  |

### 3. Coverage Scores

score = (99 full × 1.0 + 0 partial × 0.5) / 99 total_count × 100 = 100.0%

Critical:  (30 full × 1.0 + 0 partial × 0.5) / 30 critical_total × 100 = 100.0%  (30 of 30 critical requirements)
Important: (67 full × 1.0 + 0 partial × 0.5) / 67 important_total × 100 = 100.0%  (67 of 67 important requirements)
Detail:    (2 full × 1.0 + 0 partial × 0.5) / 2 detail_total × 100 = 100.0%  (2 of 2 detail requirements)
Overall:   100.0% (99 total requirements)

### 4. Top Gaps

No gaps identified. The plan explicitly addresses all 99 catalog requirements with concrete implementation sections, acceptance gates, or verification coverage.

### 5. Coverage Narrative

#### Overall Posture

This is a fully coverage-complete implementation plan for the benchmark denominator. It does not merely name the major screens; it converts the PRD's data, AI, UX, and infrastructure rules into scoped architecture, UI behavior, lifecycle rules, and verification gates.

#### Strength Clusters

Coverage is especially strong in Benchmark Runtime & Isolation, Collection Data & Persistence, Ask Chat, Concepts/Explore Similar/Alchemy, and AI Voice/Quality. The plan is unusually explicit about namespace and user scoping, server-side source of truth, per-field timestamp behavior, strict AI parsing, real-catalog recommendation resolution, fixed result counts, and AI quality scoring.

#### Weakness Clusters

There are no missing or partial catalog requirements. The only residual planning risk is outside the frozen denominator: several content/constants decisions are intentionally deferred to a decision log, but the plan identifies those dependencies and blocks final acceptance on closing them.

#### Risk Assessment

If executed as written, the most likely failure mode is implementation discipline rather than plan coverage. The riskiest areas are the high-complexity integrations: maintaining strict scoped persistence across Supabase, preserving overlay consistency on every show surface, and keeping AI output both on-brand and mechanically parseable under provider variability.

#### Remediation Guidance

No additional benchmark requirement sections are needed. The remaining work is execution governance: keep the Phase 0 decision log from drifting, preserve the domain transition table as the source of truth, and make the specified integration, visual, migration, and AI quality gates non-optional before release.
