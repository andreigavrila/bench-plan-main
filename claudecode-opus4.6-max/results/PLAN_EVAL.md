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
| PRD-001 | Use Next.js latest stable runtime | critical | full | `0. Overview`; `1.1 Repository Bootstrap` | |
| PRD-002 | Use Supabase official client libraries | critical | full | `0. Overview`; `1.2 Supabase Client Setup` | |
| PRD-003 | Ship `.env.example` with required variables | critical | full | `1.1 Repository Bootstrap` | |
| PRD-004 | Ignore `.env*` secrets except example | important | full | `1.1 Repository Bootstrap` | |
| PRD-005 | Configure build through env without code edits | critical | full | `1.1 Repository Bootstrap`; `Phase 7 Task 8` | |
| PRD-006 | Keep secrets out of repo and server-only | critical | full | `1.1 Repository Bootstrap`; `8.2 API Routes as the Integration Boundary`; `Phase 7 Task 7` | |
| PRD-007 | Provide app, test, reset command scripts | critical | full | `1.1 Repository Bootstrap` | |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | `2.2 Migration Strategy` | |
| PRD-009 | Use one stable namespace per build | critical | full | `1.3 Namespace & Identity Middleware` | |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | `1.4 Row-Level Security (RLS)`; `2.3 Test Reset Script`; `Phase 7 Tasks 3-5` | |
| PRD-011 | Attach every user record to `user_id` | critical | full | `1.3 Namespace & Identity Middleware`; `2.1 Tables` | |
| PRD-012 | Partition persisted data by namespace and user | critical | full | `2.1 Tables`; `1.4 Row-Level Security (RLS)` | |
| PRD-013 | Support documented dev auth injection, prod-gated | important | partial | `1.3 Namespace & Identity Middleware` | The injection path and production gating are specified, but the plan never assigns a documentation task for benchmark operators. |
| PRD-014 | Real OAuth later needs no schema redesign | important | full | `1.3 Namespace & Identity Middleware`; `8.4 Opaque user_id String`; `Phase 7 Task 8` | |
| PRD-015 | Keep backend as persisted source of truth | critical | full | `8.1 Server-Side Data as Source of Truth` | |
| PRD-016 | Make client cache safe to discard | critical | full | `2.1 user_preferences`; `8.1 Server-Side Data as Source of Truth` | |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | partial | `0. Overview`; `1. Project Scaffolding & Infrastructure` | The plan chooses cloud-friendly technologies, but it never explicitly commits to a no-Docker-required path or documents Docker as optional only. |
| PRD-018 | Overlay saved user data on every show appearance | critical | full | `6.2 Shared Components`; `Phase 6 Task 4` | |
| PRD-019 | Support visible statuses plus hidden `Next` | important | full | `2.1 shows`; `6.2 StatusChips` | |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | full | `4.2 Business Rule Enforcement`; `6.2 StatusChips` | |
| PRD-021 | Support free-form multi-tag personal tag library | important | full | `2.1 shows`; `4.1 Collection API Routes`; `6.2 TagPicker` | |
| PRD-022 | Define collection membership by assigned status | critical | full | `4.2 Business Rule Enforcement`; `2.1 shows` | |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | full | `4.2 Business Rule Enforcement` | |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | `4.2 Business Rule Enforcement` | |
| PRD-025 | Removing status deletes show and all My Data | critical | full | `4.2 Business Rule Enforcement`; `6.2 RemovalConfirmation` | |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | full | `4.2 Business Rule Enforcement`; `3.4 Merge Logic` | |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | `2.1 shows`; `4.2 Business Rule Enforcement` | |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | partial | `4.2 Business Rule Enforcement`; `Phase 6 Task 1` | Freshness and conflict resolution are covered, but timestamp-driven sorting behavior is not planned. |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | full | `5.5 AI Scoop Caching` | |
| PRD-030 | Keep Ask and Alchemy state session-only | important | partial | `6.4.2 Ask Page`; `6.4.3 Alchemy Page`; `8.1 Server-Side Data as Source of Truth` | Alchemy is explicitly session-only, but Ask is only described as client-side state and the plan does not explicitly say it clears on leave/reset. |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | full | `5.4 Show Resolution from AI Output` | |
| PRD-032 | Show collection and rating tile indicators | important | full | `6.2 Shared Components`; `Phase 3 Task 8` | |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | partial | `3.4 Merge Logic`; `Phase 6 Task 1` | The plan covers settings conflict resolution and show-field merges, but it does not plan duplicate detection or a fuller cross-device library sync strategy. |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | partial | `2.2 Migration Strategy`; `9. Risk Mitigation` | The plan mentions versioning and additive migrations, but it does not plan concrete upgrade/backfill steps that guarantee legacy libraries carry forward safely. |
| PRD-035 | Persist synced settings, local settings, UI state | important | full | `2.1 user_preferences`; `6.7 Settings Page` | |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | full | `2.1 shows`; `3.3 Catalog -> Show Mapping` | |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | full | `3.4 Merge Logic` | |
| PRD-038 | Provide filters panel and main screen destinations | important | full | `6.1 Layout & Navigation` | |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | full | `6.1 Layout & Navigation` | |
| PRD-040 | Keep Settings in persistent primary navigation | important | full | `6.1 Layout & Navigation` | |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | `6.1 Layout & Navigation`; `6.4 Find/Discover Hub` | |
| PRD-042 | Show only library items matching active filters | important | full | `4.3 Collection Home Queries`; `6.3 Collection Home Page` | |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | `4.3 Collection Home Queries`; `6.3 Collection Home Page` | |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | full | `4.3 Collection Home Queries`; `6.1 Layout & Navigation` | |
| PRD-045 | Render poster, title, and My Data badges | important | full | `6.2 Shared Components`; `6.3 Collection Home Page` | |
| PRD-046 | Provide empty-library and empty-filter states | detail | full | `6.3 Collection Home Page` | |
| PRD-047 | Search by title or keywords | important | full | `3.1 Server-Side Proxy Layer`; `6.4.1 Search Page` | |
| PRD-048 | Use poster grid with collection markers | important | full | `6.2 ShowGrid`; `6.4.1 Search Page` | |
| PRD-049 | Auto-open Search when setting is enabled | detail | full | `6.4.1 Search Page`; `6.7 Settings Page` | |
| PRD-050 | Keep Search non-AI in tone | important | partial | `6.4.1 Search Page` | The Search flow is non-AI by design, but the plan does not explicitly preserve a straight catalog-search tone as a UX constraint. |
| PRD-051 | Preserve Show Detail narrative section order | important | partial | `6.5 Show Detail Page` | The plan front-loads rating and status controls and does not preserve the supporting doc's exact narrative section order. |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | full | `6.5 Show Detail Page item 1`; `State handling` | |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | full | `6.5 Show Detail Page item 2` | |
| PRD-054 | Place status/interest controls in toolbar | important | full | `6.5 Show Detail Page item 4` | |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | `4.2 Business Rule Enforcement`; `6.5 Show Detail Page item 5` | |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | `4.2 Business Rule Enforcement`; `6.5 Show Detail Page item 3` | |
| PRD-057 | Show overview early for fast scanning | important | full | `6.5 Show Detail Page item 6` | |
| PRD-058 | Scoop shows correct states and progressive feedback | important | full | `6.5 Show Detail Page item 7` | |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | full | `6.5 Show Detail Page item 8`; `6.4.2 Ask Page` | |
| PRD-060 | Include traditional recommendations strand | important | full | `6.5 Show Detail Page item 10` | |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | full | `6.5 Show Detail Page item 11` | |
| PRD-062 | Include streaming availability and person-linking credits | important | full | `6.5 Show Detail Page items 12-13` | |
| PRD-063 | Gate seasons to TV and financials to movies | important | full | `6.5 Show Detail Page items 14-15`; `State handling` | |
| PRD-064 | Keep primary actions early and page not overwhelming | important | partial | `6.5 Show Detail Page` | The plan places actions early, but it does not specify any approach for keeping the dense page from feeling visually overwhelming. |
| PRD-065 | Provide conversational Ask chat interface | important | full | `6.4.2 Ask Page` | |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | partial | `5.2 ask.ts`; `6.4.2 Ask Page` | Spoiler safety and taste awareness are planned, but the prompt contract does not explicitly require the answer-first, confident response pattern from the quality bar. |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | `6.4.2 Ask Page` | |
| PRD-068 | Open Detail from mentions or Search fallback | important | full | `6.4.2 Ask Page`; `5.4 Show Resolution from AI Output` | |
| PRD-069 | Show six random starter prompts with refresh | important | full | `6.4.2 Ask Page` | |
| PRD-070 | Summarize older turns while preserving voice | important | full | `5.2 summarize.ts`; `6.4.2 Ask Page` | |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | full | `5.2 ask.ts`; `6.4.2 Ask Page` | |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | full | `5.2 ask.ts` | |
| PRD-073 | Retry malformed mention output once, then fallback | important | full | `9. Risk Mitigation` | |
| PRD-074 | Redirect Ask back into TV/movie domain | important | partial | `5.2 AI Prompt Modules` | The plan references shared prompting docs, but it never explicitly calls out redirecting off-domain Ask prompts back to TV and movies. |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | partial | `5.2 concepts.ts` | The concept plan emphasizes evocative outputs, but it does not explicitly frame concepts as ingredients rather than genre labels. |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | full | `5.2 concepts.ts` | |
| PRD-077 | Order concepts by strongest aha and varied axes | important | partial | `5.2 concepts.ts` | The axes are listed, but the plan does not require strongest-first ordering or explicitly enforce cross-axis variety in output ranking. |
| PRD-078 | Require concept selection and guide ingredient picking | important | partial | `6.5 Show Detail Page item 11`; `6.4.3 Alchemy Page` | Selection is implemented, but the plan omits the guidance copy that teaches users to pick the ingredients they want more of. |
| PRD-079 | Return exactly five Explore Similar recommendations | important | full | `5.2 recommendations.ts`; `6.5 Show Detail Page item 11` | |
| PRD-080 | Support full Alchemy loop with chaining | important | full | `6.4.3 Alchemy Page` | |
| PRD-081 | Clear downstream results when inputs change | important | full | `6.4.3 Alchemy Page` | |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | partial | `5.2 concepts.ts`; `6.4.3 Alchemy Page` | The multi-show concept flow is covered, but the plan does not reserve a larger concept pool for Alchemy than single-show Explore Similar. |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | full | `5.2 recommendations.ts` | |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | partial | `Phase 5 Task 8`; `Phase 6 Task 6` | The plan reviews taste alignment and surprise late, but it does not bake surprising-but-defensible recommendation behavior into the recommendation contract itself. |
| PRD-085 | Keep one consistent AI persona across surfaces | important | full | `5.2 AI Prompt Modules` | |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | full | `5.2 AI Prompt Modules`; `9. Risk Mitigation` | |
| PRD-087 | Make AI warm, joyful, and light in critique | important | full | `5.2 ask.ts`; `5.2 scoop.ts` | |
| PRD-088 | Structure Scoop as personal taste mini-review | important | full | `5.2 scoop.ts` | |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | partial | `5.2 ask.ts`; `6.4.2 Ask Page` | The Ask persona is defined, but the plan does not explicitly constrain default responses to brisk, dialogue-like length and rhythm. |
| PRD-090 | Feed AI the right surface-specific context inputs | important | full | `5.2 AI Prompt Modules`; `5.3 AI API Routes` | |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | partial | `Phase 6 Task 6` | The plan calls for a qualitative review, but it does not define the rubric thresholds or hard-fail handling for integrity regressions. |
| PRD-092 | Show person gallery, name, and bio | important | full | `6.6 Person Detail Page` | |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | full | `6.6 Person Detail Page` | |
| PRD-094 | Group filmography by year | important | full | `6.6 Person Detail Page` | |
| PRD-095 | Open Show Detail from selected credit | important | full | `6.6 Person Detail Page` | |
| PRD-096 | Include font size and Search-on-launch settings | important | full | `6.7 Settings Page`; `Phase 6 Task 2` | |
| PRD-097 | Support username, model, and API-key settings safely | important | full | `6.7 Settings Page`; `2.1 cloud_settings` | |
| PRD-098 | Export saved shows and My Data as zip | critical | full | `4.4 Export / Backup`; `6.7 Settings Page` | |
| PRD-099 | Encode export dates using ISO-8601 | important | full | `4.4 Export / Backup` | |

### 3. Coverage Scores

Overall score:

```text
score = (81 x 1.0 + 18 x 0.5) / 99 x 100 = 90.9%
```

Score by severity tier:

```text
Critical:  (29 x 1.0 + 1 x 0.5) / 30 x 100 = 98.3%  (29.5 of 30 critical requirements)
Important: (50 x 1.0 + 17 x 0.5) / 67 x 100 = 87.3%  (58.5 of 67 important requirements)
Detail:    (2 x 1.0 + 0 x 0.5) / 2 x 100 = 100.0%  (2.0 of 2 detail requirements)
Overall:   (81 x 1.0 + 18 x 0.5) / 99 x 100 = 90.9%  (90.0 of 99 requirements)
```

### 4. Top Gaps

- PRD-034 | `critical` | Preserve saved libraries across data-model upgrades: The plan only gestures at versioning and additive migrations. Without an explicit backfill and verification strategy, a schema change can silently damage the one user asset the PRD treats as non-negotiable: the saved library and My Data history.
- PRD-033 | `important` | Sync libraries/settings consistently and merge duplicates: Cross-device consistency is only partially planned. If duplicate detection and library-level merge behavior are left undefined, users can end up with diverging collections and trust-eroding sync behavior.
- PRD-091 | `important` | Validate discovery with rubric and hard-fail integrity: The plan says to review AI quality, but not how to fail it. That makes it easy to ship recommendations that are off-brand or, worse, not real shows, even if the implementation seems broadly functional.
- PRD-051 | `important` | Preserve Show Detail narrative section order: The plan's Detail ordering drifts from the experience spec. If implemented as written, the page is likely to feel more like a control surface than the intended "facts + feeling + discovery" narrative.
- PRD-017 | `important` | Avoid Docker requirement for cloud-agent compatibility: Benchmark execution depends on low-friction setup. If the implementation drifts into Docker-dependent Supabase or reset workflows, cloud agents can fail before product behavior is even evaluated.

### 5. Coverage Narrative

#### Overall Posture

This is a strong plan with broad structural coverage and only a small number of true requirement gaps. It clearly understands the benchmark runtime, the data model, the major UX surfaces, and the AI feature map. The remaining issues are mostly about behavioral precision and long-term safety rather than missing whole product areas.

#### Strength Clusters

The plan is strongest in Benchmark Runtime & Isolation, Collection Data & Persistence, and the core page architecture spanning App Navigation & Discover Shell, Collection Home & Search, and Person Detail. It also covers the major AI surface plumbing well: prompt modules, API routes, resolution of recommendations into real shows, and the main Ask/Scoop/Alchemy flows are all concretely planned.

#### Weakness Clusters

The weaker spots cluster in three places. First, several AI requirements are only partially captured because the plan references the AI specs at a high level but does not translate all of their behavioral contracts into concrete acceptance criteria. Second, long-term data continuity and sync semantics are underspecified relative to the PRD's durability promises. Third, a few benchmark-operational constraints, especially documentation and no-Docker execution expectations, are implied rather than explicitly planned.

#### Risk Assessment

If this plan were executed as-is, the most likely result is a functionally complete app that still misses parity in subtle but important ways. A QA reviewer would probably notice AI behavior drift first: Ask might work, but not consistently answer in the required voice, pacing, and domain-bounded way, while discovery quality checks could remain too subjective. Over a longer horizon, migration and sync edge cases would create the more serious product risk because they threaten user trust in data durability.

#### Remediation Guidance

The next planning pass should add tighter behavioral acceptance criteria, not just more feature bullets. The AI surfaces need explicit prompt/output requirements tied to the quality bar, including domain redirects, pacing, concept quality, and hard-fail integrity gates. The data layer needs concrete upgrade, duplicate-merge, and sync semantics. The benchmark runtime section needs explicit operator-facing documentation and a stated no-Docker-required execution path. The Detail page section should be revised to match the intended narrative hierarchy exactly.
