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
| PRD-001 | Use Next.js latest stable runtime | critical | full | Phase 0.1 Repository Setup | |
| PRD-002 | Use Supabase official client libraries | critical | full | Phase 0.2 Supabase Schema & Migrations; Phase 0.4 Supabase Client Setup | |
| PRD-003 | Ship `.env.example` with required variables | critical | full | Phase 0.1 Repository Setup | |
| PRD-004 | Ignore `.env*` secrets except example | important | full | Phase 0.1 Repository Setup | |
| PRD-005 | Configure build through env without code edits | critical | full | Phase 0.1 Repository Setup | |
| PRD-006 | Keep secrets out of repo and server-only | critical | full | Phase 0.1 Repository Setup; Phase 0.4 Supabase Client Setup; Phase 1.4 External Catalog Service; Phase 1.5 AI Service Layer | |
| PRD-007 | Provide app, test, reset command scripts | critical | full | Phase 0.5 NPM Scripts | |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | Phase 0.2 Supabase Schema & Migrations | |
| PRD-009 | Use one stable namespace per build | critical | full | Phase 0.3 Identity & Namespace Injection | |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | Phase 0.2 Supabase Schema & Migrations; Phase 1.2 Show Repository; Phase 10.4 Test Data Management | |
| PRD-011 | Attach every user record to `user_id` | critical | full | Phase 0.2 Supabase Schema & Migrations | |
| PRD-012 | Partition persisted data by namespace and user | critical | full | Phase 0.2 Supabase Schema & Migrations; Phase 0.4 Supabase Client Setup | |
| PRD-013 | Support documented dev auth injection, prod-gated | important | full | Phase 0.3 Identity & Namespace Injection | |
| PRD-014 | Real OAuth later needs no schema redesign | important | full | Phase 0.3 Identity & Namespace Injection; Key Technical Decisions & Rationale | |
| PRD-015 | Keep backend as persisted source of truth | critical | full | Phase 0.2 Supabase Schema & Migrations; Phase 2.4 Client-Side State Management | |
| PRD-016 | Make client cache safe to discard | critical | partial | Phase 2.4 Client-Side State Management | The plan uses disposable client caches by implication but never states or tests that clearing browser storage leaves user-owned backend data intact. |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | partial | Phase 0.2 Supabase Schema & Migrations | The plan assumes Supabase but never explicitly documents a non-Docker cloud-agent path or states that Docker stays optional. |
| PRD-018 | Overlay saved user data on every show appearance | critical | full | Phase 9.2 User Data Overlay | |
| PRD-019 | Support visible statuses plus hidden `Next` | important | full | Phase 0.2 Supabase Schema & Migrations; Phase 2.3 Shared Components | |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | full | Phase 2.3 Shared Components | |
| PRD-021 | Support free-form multi-tag personal tag library | important | full | Phase 2.3 Shared Components; Phase 1.2 Show Repository | |
| PRD-022 | Define collection membership by assigned status | critical | full | Phase 3.2 Saving Business Logic | |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | full | Phase 3.2 Saving Business Logic | |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | Phase 3.2 Saving Business Logic | |
| PRD-025 | Removing status deletes show and all My Data | critical | full | Phase 1.2 Show Repository; Phase 3.2 Saving Business Logic | |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | full | Phase 9.4 Data Merge on Re-Add / Catalog Refresh | |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | Phase 0.2 Supabase Schema & Migrations; Phase 1.2 Show Repository | |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | partial | Phase 1.2 Show Repository; Phase 9.5 AI Data Lifecycle | Timestamp usage is defined for conflict resolution and Scoop freshness, but the plan does not turn those timestamps into any sorting behavior. |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | full | Phase 5.1 Overview + AI Scoop; Phase 9.5 AI Data Lifecycle | |
| PRD-030 | Keep Ask and Alchemy state session-only | important | full | Phase 4.3 Ask Mode; Phase 4.4 Alchemy Mode; Phase 9.5 AI Data Lifecycle | |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | full | Phase 1.5 AI Service Layer | |
| PRD-032 | Show collection and rating tile indicators | important | full | Phase 2.3 Shared Components; Phase 9.1 Show Tile Indicators | |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | full | Phase 0.2 Supabase Schema & Migrations; Phase 1.2 Show Repository; Phase 1.3 Settings Repository | |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | full | Phase 11.1 Migration Strategy | |
| PRD-035 | Persist synced settings, local settings, UI state | important | full | Phase 1.3 Settings Repository; Phase 2.4 Client-Side State Management; Phase 7.1 Settings Page | |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | partial | Phase 0.2 Supabase Schema & Migrations; Phase 1.4 External Catalog Service | The plan persists `provider_data`, but it never explicitly calls out the transient-only policy for credits, seasons, videos, images, and similar detail fetches. |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | full | Phase 1.2 Show Repository; Phase 9.4 Data Merge on Re-Add / Catalog Refresh | |
| PRD-038 | Provide filters panel and main screen destinations | important | full | Phase 2.1 Layout & Routing Structure; Phase 2.2 Sidebar / Filter Panel | |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | full | Phase 2.1 Layout & Routing Structure | |
| PRD-040 | Keep Settings in persistent primary navigation | important | full | Phase 2.1 Layout & Routing Structure | |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | Phase 4.1 Find Layout | |
| PRD-042 | Show only library items matching active filters | important | full | Phase 3.1 Collection Home Page | |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | Phase 3.1 Collection Home Page | |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | full | Phase 2.2 Sidebar / Filter Panel | |
| PRD-045 | Render poster, title, and My Data badges | important | full | Phase 2.3 Shared Components; Phase 3.1 Collection Home Page | |
| PRD-046 | Provide empty-library and empty-filter states | detail | full | Phase 3.3 Empty States | |
| PRD-047 | Search by title or keywords | important | full | Phase 4.2 Search Mode | |
| PRD-048 | Use poster grid with collection markers | important | full | Phase 4.2 Search Mode; Phase 2.3 Shared Components | |
| PRD-049 | Auto-open Search when setting is enabled | detail | partial | Phase 4.1 Find Layout; Phase 7.1 Settings Page | The plan stores `autoSearch` and autofocuses the search field, but it does not clearly navigate the user into Search on app launch. |
| PRD-050 | Keep Search non-AI in tone | important | partial | Phase 4.2 Search Mode | Search is implemented as a plain catalog panel, but the plan never explicitly guards it from AI-style copy or personality bleed. |
| PRD-051 | Preserve Show Detail narrative section order | important | full | Phase 5.1 Show Detail Page Structure | |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | full | Phase 5.1 Header Media Carousel | |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | full | Phase 5.1 Core Facts + Community Score | |
| PRD-054 | Place status/interest controls in toolbar | important | full | Phase 5.1 My Relationship Controls (Toolbar) | |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | Phase 5.1 My Relationship Controls (Toolbar); Phase 3.2 Saving Business Logic | |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | Phase 5.1 My Relationship Controls (Toolbar); Phase 3.2 Saving Business Logic | |
| PRD-057 | Show overview early for fast scanning | important | full | Phase 5.1 Overview + AI Scoop | |
| PRD-058 | Scoop shows correct states and progressive feedback | important | full | Phase 5.1 Overview + AI Scoop; Phase 9.7 Streaming / Progressive Loading for AI | |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | full | Phase 5.1 Ask About This Show; Phase 8.4 Ask About Show Prompt | |
| PRD-060 | Include traditional recommendations strand | important | full | Phase 5.1 Traditional Recommendations Strand | |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | full | Phase 5.1 Explore Similar (Concept Discovery) | |
| PRD-062 | Include streaming availability and person-linking credits | important | full | Phase 5.1 Streaming Availability; Phase 5.1 Cast & Crew | |
| PRD-063 | Gate seasons to TV and financials to movies | important | full | Phase 5.1 Seasons (TV only); Phase 5.1 Budget vs Revenue (Movies) | |
| PRD-064 | Keep primary actions early and page not overwhelming | important | partial | Phase 5.1 Show Detail Page Structure | The section order preserves early actions, but the plan does not add any explicit strategy for keeping the page visually restrained as more modules accumulate. |
| PRD-065 | Provide conversational Ask chat interface | important | full | Phase 4.3 Ask Mode | |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | partial | Phase 8.1 Shared System Prompt Base; Phase 8.3 Ask Prompt | The plan captures confidence and spoiler safety, but it does not explicitly require the answer to land within the first 3–5 lines. |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | Phase 4.3 Ask Mode | |
| PRD-068 | Open Detail from mentions or Search fallback | important | full | Phase 4.3 Ask Mode; Phase 1.5 AI Service Layer | |
| PRD-069 | Show six random starter prompts with refresh | important | full | Phase 4.3 Ask Mode; Phase 8.7 Starter Prompts | |
| PRD-070 | Summarize older turns while preserving voice | important | full | Phase 4.3 Ask Mode; Phase 8.3 Ask Prompt | |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | full | Phase 5.1 Ask About This Show; Phase 8.4 Ask About Show Prompt | |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | full | Phase 8.3 Ask Prompt; Phase 1.5 AI Service Layer | |
| PRD-073 | Retry malformed mention output once, then fallback | important | full | Phase 1.5 AI Service Layer; Phase 9.8 Error Handling & Fallbacks | |
| PRD-074 | Redirect Ask back into TV/movie domain | important | full | Phase 8.1 Shared System Prompt Base | |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | partial | Phase 5.1 Explore Similar (Concept Discovery); Phase 8.5 Concepts Prompt | The plan frames concepts as ingredients, but it never explicitly forbids genre-style outputs as part of the contract. |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | full | Phase 8.5 Concepts Prompt | |
| PRD-077 | Order concepts by strongest aha and varied axes | important | partial | Phase 8.5 Concepts Prompt | The plan covers varied axes, but it does not require concepts to be ordered by strongest “aha” value. |
| PRD-078 | Require concept selection and guide ingredient picking | important | full | Phase 5.1 Explore Similar (Concept Discovery); Phase 4.4 Alchemy Mode | |
| PRD-079 | Return exactly five Explore Similar recommendations | important | full | Phase 5.1 Explore Similar (Concept Discovery); Phase 8.6 Concept Recommendations Prompt | |
| PRD-080 | Support full Alchemy loop with chaining | important | full | Phase 4.4 Alchemy Mode | |
| PRD-081 | Clear downstream results when inputs change | important | full | Phase 4.4 Alchemy Mode | |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | full | Phase 8.5 Concepts Prompt | |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | full | Phase 8.6 Concept Recommendations Prompt | |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | partial | Phase 8.6 Concept Recommendations Prompt | The plan asks for concept-grounded reasons, but it does not explicitly demand pleasantly surprising yet defensible recommendations. |
| PRD-085 | Keep one consistent AI persona across surfaces | important | full | Phase 8.1 Shared System Prompt Base | |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | full | Phase 8.1 Shared System Prompt Base; Phase 1.5 AI Service Layer | |
| PRD-087 | Make AI warm, joyful, and light in critique | important | full | Phase 8.1 Shared System Prompt Base | |
| PRD-088 | Structure Scoop as personal taste mini-review | important | full | Phase 8.2 Scoop Prompt | |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | full | Phase 8.3 Ask Prompt | |
| PRD-090 | Feed AI the right surface-specific context inputs | important | full | Phase 8.2 Scoop Prompt; Phase 8.3 Ask Prompt; Phase 8.4 Ask About Show Prompt; Phase 8.6 Concept Recommendations Prompt | |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | partial | Phase 10.1 Unit Tests; Phase 1.5 AI Service Layer | The plan validates parsing and show resolution, but it omits a rubric-based discovery QA pass and an explicit hard-fail gate for low-integrity outputs. |
| PRD-092 | Show person gallery, name, and bio | important | full | Phase 6.1 Person Detail | |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | full | Phase 6.1 Person Detail | |
| PRD-094 | Group filmography by year | important | full | Phase 6.1 Person Detail | |
| PRD-095 | Open Show Detail from selected credit | important | full | Phase 6.1 Person Detail | |
| PRD-096 | Include font size and Search-on-launch settings | important | full | Phase 7.1 Settings Page | |
| PRD-097 | Support username, model, and API-key settings safely | important | full | Phase 7.1 Settings Page; Phase 1.4 External Catalog Service; Phase 1.5 AI Service Layer | |
| PRD-098 | Export saved shows and My Data as zip | critical | full | Phase 7.1 Settings Page; Phase 1.6 API Routes | |
| PRD-099 | Encode export dates using ISO-8601 | important | full | Phase 7.1 Settings Page | |

## 3. Coverage Scores

```text
score = (87 × 1.0 + 12 × 0.5) / 99 × 100 = 93.9%
```

```text
Critical:  (29 × 1.0 + 1 × 0.5) / 30 × 100 = 98.3%  (29.5 of 30 critical requirements)
Important: (57 × 1.0 + 10 × 0.5) / 67 × 100 = 92.5%  (62 of 67 important requirements)
Detail:    (1 × 1.0 + 1 × 0.5) / 2 × 100 = 75.0%  (1.5 of 2 detail requirements)
Overall:   93.9% (99 total requirements)
```

## 4. Top Gaps

- PRD-016 | `critical` | Make client cache safe to discard: This matters because the infra rider treats backend persistence as the safety net; without an explicit “clear storage and recover cleanly” contract, the app can still look durable in design while failing a basic benchmark resilience expectation.
- PRD-017 | `important` | Avoid Docker requirement for cloud-agent compatibility: This matters because benchmark runners need an explicitly supported hosted/non-Docker path; leaving that implicit invites implementation drift toward local-only tooling that breaks automated runs.
- PRD-091 | `important` | Validate discovery with rubric and hard-fail integrity: This matters because AI features can technically ship while still violating the product’s quality bar; QA would have no concrete gate to reject generic, off-brand, or unresolved recommendations.
- PRD-084 | `important` | Deliver surprising but defensible taste-aligned recommendations: This matters because Alchemy and Explore Similar differentiate the product; if the plan does not ask for “surprise without betrayal,” those surfaces can degrade into safe but unremarkable rec lists.
- PRD-066 | `important` | Answer directly with confident, spoiler-safe recommendations: This matters because Ask is supposed to feel fast and chatty; without a crisp “answer first” rule, the experience can become wordy before it becomes useful.

## 5. Coverage Narrative

#### Overall Posture

This is a strong implementation plan with minor but real gaps. It covers the app’s structural architecture, persistence model, major UX surfaces, and most behavioral contracts in concrete enough terms to execute, but it is less rigorous on a handful of benchmark-operability details and the highest-fidelity AI quality requirements.

#### Strength Clusters

The plan is strongest in Benchmark Runtime & Isolation, Collection Data & Persistence, Show Detail & Relationship UX, and Settings & Export. Those areas get concrete schema decisions, route structure, save/remove rules, migration handling, detail-page composition, and explicit export behavior rather than vague intent.

#### Weakness Clusters

The gaps cluster in two places. First, benchmark and data-durability nuance: Docker-optional execution and cache-discard safety are touched only indirectly. Second, AI behavioral precision: the plan captures persona, structure, and output formats well, but it is looser on the qualitative bar that makes Ask, Concepts, Explore Similar, and Alchemy feel distinctively on spec.

#### Risk Assessment

If executed as-is, the most likely failure mode is not a broken CRUD app; it is a product that works mechanically while missing some of the benchmark’s sharper behavioral edges. A QA reviewer would probably notice bland or insufficiently surprising AI recommendations, slightly under-specified Ask pacing, and unclear Search-on-launch or cloud-agent execution behavior before they noticed deeper architectural issues.

#### Remediation Guidance

The remaining work is mostly tighter planning, not a new architecture. The plan needs explicit acceptance criteria for cache-discard recovery, non-Docker benchmark operation, Search-on-launch behavior, and the AI quality bar: direct-answer rules, concept ordering, anti-genre concept constraints, surprise-with-defensibility, and rubric-driven validation with a hard fail for integrity misses.
