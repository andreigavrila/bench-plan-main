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
| PRD-001 | Use Next.js latest stable runtime | critical | full | Section 1 scope stance; Section 2 task 1 |  |
| PRD-002 | Use Supabase official client libraries | critical | full | Section 1 scope stance; Section 2 task 1 |  |
| PRD-003 | Ship `.env.example` with required variables | critical | full | Section 2 task 2 |  |
| PRD-004 | Ignore `.env*` secrets except example | important | full | Section 2 task 3 |  |
| PRD-005 | Configure build through env without code edits | critical | full | Section 2 tasks 2 and 5 |  |
| PRD-006 | Keep secrets out of repo and server-only | critical | full | Section 2 task 3; Section 5 task 5 |  |
| PRD-007 | Provide app, test, reset command scripts | critical | full | Section 2 tasks 4 and 9 |  |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | Section 3 task 1 |  |
| PRD-009 | Use one stable namespace per build | critical | full | Section 2 tasks 2 and 6 |  |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | Section 2 tasks 8 and 9; Section 12 test strategy task 2 |  |
| PRD-011 | Attach every user record to `user_id` | critical | full | Section 2 task 6; Section 3 tasks 2 and 3 |  |
| PRD-012 | Partition persisted data by namespace and user | critical | full | Section 2 task 8; Section 3 task 3 |  |
| PRD-013 | Support documented dev auth injection, prod-gated | important | full | Section 2 task 7; Section 12 test strategy task 3 |  |
| PRD-014 | Real OAuth later needs no schema redesign | important | full | Section 2 task 7 |  |
| PRD-015 | Keep backend as persisted source of truth | critical | full | Section 1 scope stance; Section 2 task 8 |  |
| PRD-016 | Make client cache safe to discard | critical | full | Section 1 scope stance; Section 12 delivery checkpoint 5 |  |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | full | Section 2 task 4; Section 12 delivery checkpoint 1 |  |
| PRD-018 | Overlay saved user data on every show appearance | critical | full | Section 4 task 8; Section 8 task 3 |  |
| PRD-019 | Support visible statuses plus hidden `Next` | important | full | Section 1 scope stance; Section 4 task 2 |  |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | full | Section 4 task 2; Section 10 task 3 |  |
| PRD-021 | Support free-form multi-tag personal tag library | important | full | Section 4 task 5; Section 8 task 1 |  |
| PRD-022 | Define collection membership by assigned status | critical | full | Section 4 task 2 |  |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | full | Section 4 task 3; Section 10 task 3 |  |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | Section 4 task 3 |  |
| PRD-025 | Removing status deletes show and all My Data | critical | full | Section 4 task 6; Section 10 task 3 |  |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | full | Section 4 task 6; Section 3 task 7 |  |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | Section 4 task 7; Section 3 task 2 |  |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | full | Section 4 tasks 7 and 9; Section 6 task 6 |  |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | full | Section 6 task 6; Section 10 task 4 |  |
| PRD-030 | Keep Ask and Alchemy state session-only | important | full | Section 6 tasks 4 and 9; Section 11 task 4 |  |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | full | Section 6 task 5 |  |
| PRD-032 | Show collection and rating tile indicators | important | full | Section 8 task 3; Section 9 task 2 |  |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | full | Section 3 tasks 6 and 7; Section 12 test strategy task 3 |  |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | full | Section 3 task 8; Section 12 delivery checkpoint 5 |  |
| PRD-035 | Persist synced settings, local settings, UI state | important | full | Section 3 task 2; Section 5 task 5; Section 11 task 3 |  |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | full | Section 3 tasks 4 and 5; Section 5 task 2 |  |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | full | Section 3 task 7; Section 12 test strategy task 1 |  |
| PRD-038 | Provide filters panel and main screen destinations | important | full | Section 7 tasks 3 and 4; Section 8 task 1 |  |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | full | Section 7 task 4; Section 8 task 1 |  |
| PRD-040 | Keep Settings in persistent primary navigation | important | full | Section 7 task 4; Section 8 task 1 |  |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | Section 7 task 3; Section 9 task 1 |  |
| PRD-042 | Show only library items matching active filters | important | full | Section 4 task 9; Section 8 task 1 |  |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | Section 4 task 9; Section 8 task 2 |  |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | full | Section 4 task 9; Section 8 task 1 |  |
| PRD-045 | Render poster, title, and My Data badges | important | full | Section 8 task 3 |  |
| PRD-046 | Provide empty-library and empty-filter states | detail | full | Section 8 task 2 |  |
| PRD-047 | Search by title or keywords | important | full | Section 5 task 2; Section 9 task 2 |  |
| PRD-048 | Use poster grid with collection markers | important | full | Section 9 task 2 |  |
| PRD-049 | Auto-open Search when setting is enabled | detail | full | Section 9 task 1; Section 11 task 3 |  |
| PRD-050 | Keep Search non-AI in tone | important | full | Section 6 task 2; Section 9 task 2 |  |
| PRD-051 | Preserve Show Detail narrative section order | important | full | Section 10 task 1 |  |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | full | Section 10 task 2 |  |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | full | Section 10 task 2 |  |
| PRD-054 | Place status/interest controls in toolbar | important | full | Section 10 task 3 |  |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | Section 4 task 3; Section 10 task 3 |  |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | Section 4 task 3; Section 10 task 3 |  |
| PRD-057 | Show overview early for fast scanning | important | full | Section 10 task 1; Section 10 task 2 |  |
| PRD-058 | Scoop shows correct states and progressive feedback | important | full | Section 6 task 6; Section 10 task 4 |  |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | full | Section 6 task 4; Section 10 task 4 |  |
| PRD-060 | Include traditional recommendations strand | important | full | Section 10 task 5 |  |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | full | Section 10 task 5 |  |
| PRD-062 | Include streaming availability and person-linking credits | important | full | Section 5 tasks 2 and 6; Section 10 task 5 |  |
| PRD-063 | Gate seasons to TV and financials to movies | important | full | Section 10 tasks 1 and 5; Section 12 test strategy task 4 |  |
| PRD-064 | Keep primary actions early and page not overwhelming | important | full | Section 10 task 2; Section 12 test strategy task 5 |  |
| PRD-065 | Provide conversational Ask chat interface | important | full | Section 9 task 3 |  |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | partial | Section 6 task 2; Section 6 task 10; Section 12 test strategy task 6 | The plan covers spoiler safety, opinionated voice, and quality scoring, but it does not explicitly require Ask to answer within the first few lines or make confident picks as an acceptance criterion. |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | Section 9 task 3 |  |
| PRD-068 | Open Detail from mentions or Search fallback | important | full | Section 6 task 5; Section 9 task 3 |  |
| PRD-069 | Show six random starter prompts with refresh | important | full | Section 9 task 3 |  |
| PRD-070 | Summarize older turns while preserving voice | important | full | Section 6 task 4 |  |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | full | Section 6 task 4; Section 10 task 4 |  |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | full | Section 6 task 3 |  |
| PRD-073 | Retry malformed mention output once, then fallback | important | full | Section 6 task 3 |  |
| PRD-074 | Redirect Ask back into TV/movie domain | important | full | Section 6 task 2 |  |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | full | Section 6 task 7; Section 9 task 4 |  |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | full | Section 6 task 7 |  |
| PRD-077 | Order concepts by strongest aha and varied axes | important | full | Section 6 task 7 |  |
| PRD-078 | Require concept selection and guide ingredient picking | important | full | Section 9 task 4; Section 10 task 5 |  |
| PRD-079 | Return exactly five Explore Similar recommendations | important | full | Section 6 task 8; Section 10 task 5 |  |
| PRD-080 | Support full Alchemy loop with chaining | important | full | Section 6 task 9; Section 9 task 4 |  |
| PRD-081 | Clear downstream results when inputs change | important | full | Section 6 task 9; Section 9 task 4 |  |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | partial | Section 6 task 7 | Multi-show concepts are required to be shared, but the larger candidate pool is only optional (`may use`) rather than a committed behavior. |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | full | Section 6 task 8 |  |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | full | Section 6 task 10; Section 12 test strategy task 6 |  |
| PRD-085 | Keep one consistent AI persona across surfaces | important | full | Section 6 task 2 |  |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | full | Section 6 task 2; Section 12 test strategy task 6 |  |
| PRD-087 | Make AI warm, joyful, and light in critique | important | full | Section 6 task 2 |  |
| PRD-088 | Structure Scoop as personal taste mini-review | important | full | Section 6 task 6 |  |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | full | Section 6 task 2; Section 9 task 3 |  |
| PRD-090 | Feed AI the right surface-specific context inputs | important | full | Section 6 task 1; Section 6 task 4 |  |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | full | Section 6 task 10; Section 12 test strategy task 6 |  |
| PRD-092 | Show person gallery, name, and bio | important | full | Section 11 task 1 |  |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | full | Section 11 task 1 |  |
| PRD-094 | Group filmography by year | important | full | Section 11 task 2 |  |
| PRD-095 | Open Show Detail from selected credit | important | full | Section 11 task 2 |  |
| PRD-096 | Include font size and Search-on-launch settings | important | full | Section 5 task 5; Section 11 task 3 |  |
| PRD-097 | Support username, model, and API-key settings safely | important | full | Section 5 task 5; Section 11 task 3 |  |
| PRD-098 | Export saved shows and My Data as zip | critical | full | Section 5 task 7; Section 11 task 4 |  |
| PRD-099 | Encode export dates using ISO-8601 | important | full | Section 3 task 6; Section 5 task 7; Section 11 task 4 |  |

### 3. Coverage Scores

score = (97 full × 1.0 + 2 partial × 0.5) / 99 total_count × 100 = 99.0%

Critical:  (30 full × 1.0 + 0 partial × 0.5) / 30 critical_total × 100 = 100.0%  (30 of 30 critical requirements)
Important: (65 full × 1.0 + 2 partial × 0.5) / 67 important_total × 100 = 98.5%  (66.0 weighted of 67 important requirements)
Detail:    (2 full × 1.0 + 0 partial × 0.5) / 2 detail_total × 100 = 100.0%  (2 of 2 detail requirements)
Overall:   99.0% (99 total requirements)

### 4. Top Gaps

1. PRD-066 | important | Answer directly with confident, spoiler-safe recommendations

   This matters because Ask can satisfy broad persona and safety rules while still feeling evasive or slow; users will notice first if recommendations do not answer the prompt quickly and decisively.

2. PRD-082 | important | Generate shared multi-show concepts with larger option pool

   This matters because treating the larger Alchemy pool as optional can leave multi-show discovery with too few shared concepts for meaningful user steering.

### 5. Coverage Narrative

#### Overall Posture

This is an extremely strong, execution-ready implementation plan with two narrow acceptance-criteria gaps. It does not merely name the product surfaces; it gives concrete domain services, schema boundaries, UI flows, AI contracts, persistence rules, and verification gates for nearly every catalog requirement.

#### Strength Clusters

Coverage is strongest in Benchmark Runtime & Isolation, Collection Data & Persistence, Ask Chat, Concepts/Alchemy, and AI Voice/Quality. The plan is unusually explicit about namespace/user partitioning, server-side source of truth, Supabase migrations, per-field timestamp conflict handling, structured Ask output, real-show recommendation resolution, and AI quality enforcement.

#### Weakness Clusters

The two partial items are both AI contract details rather than architecture or feature gaps. Ask lacks the first-lines/direct-answer bar, and multi-show concept generation makes the larger option pool discretionary rather than required.

#### Risk Assessment

If executed as-is, the most likely failure mode is discovery that is safe and technically valid but slightly weaker in use: Ask may take too long to recommend, while Alchemy may expose too few shared concepts for useful steering.

#### Remediation Guidance

The remaining planning work is acceptance-criteria refinement. Add an explicit Ask response-shape check requiring a direct answer within the first few lines, and make the larger multi-show concept pool mandatory with a concrete count or relative-size assertion.
