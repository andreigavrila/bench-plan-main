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
| PRD-001 | Use Next.js latest stable runtime | critical | full | `RT-01`; `Runtime and Boundaries` | |
| PRD-002 | Use Supabase official client libraries | critical | partial | `Scope and Starting Point`; `RT-04` | The plan commits to Supabase, but it never explicitly requires the official Supabase SDKs, leaving room for a non-compliant integration choice. |
| PRD-003 | Ship `.env.example` with required variables | critical | full | `RT-02` | |
| PRD-004 | Ignore `.env*` secrets except example | important | full | `RT-03` | |
| PRD-005 | Configure build through env without code edits | critical | full | `RT-02` | |
| PRD-006 | Keep secrets out of repo and server-only | critical | full | `RT-03`; `SET-04`; `Runtime and Boundaries` | |
| PRD-007 | Provide app, test, reset command scripts | critical | full | `RT-05`; `RT-06` | |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | `RT-04` | |
| PRD-009 | Use one stable namespace per build | critical | full | `RT-05`; `Request context resolver` | |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | `RT-05`; `shows` composite key | |
| PRD-011 | Attach every user record to `user_id` | critical | full | `Core Persistence Model`; `Request context resolver` | |
| PRD-012 | Partition persisted data by namespace and user | critical | full | `shows` and `cloud_settings` composite keys | |
| PRD-013 | Support documented dev auth injection, prod-gated | important | partial | `RT-02`; `RT-07`; `Request context resolver` | The plan covers gating and supported injection paths, but it does not add a concrete documentation deliverable for how developers and tests should use them. |
| PRD-014 | Real OAuth later needs no schema redesign | important | full | `Runtime and Boundaries`; `RT-07` | |
| PRD-015 | Keep backend as persisted source of truth | critical | full | `Scope and Starting Point`; `Runtime and Boundaries` | |
| PRD-016 | Make client cache safe to discard | critical | full | `Runtime and Boundaries`; `Local client storage` | |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | full | `RT-06` | |
| PRD-018 | Overlay saved user data on every show appearance | critical | full | `Overlay hydration service`; `HOME-07` | |
| PRD-019 | Support visible statuses plus hidden `Next` | important | full | `DET-03`; `Key Risks and Decisions To Track` item 3 | |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | full | `DATA-04`; `DET-04` | |
| PRD-021 | Support free-form multi-tag personal tag library | important | full | `DET-06`; `HOME-08` | |
| PRD-022 | Define collection membership by assigned status | critical | full | `Core Persistence Model`; `DATA-04`; `DATA-05` | |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | full | `DATA-04` | |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | `DATA-04` | |
| PRD-025 | Removing status deletes show and all My Data | critical | full | `DATA-05`; `Core Persistence Model` | |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | full | `Show merge service`; `Overlay hydration service`; `DATA-03` | |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | `DATA-01`; `DATA-03`; `DATA-06` | |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | full | `DATA-06`; `HOME-09`; `DET-09` | |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | full | `DET-09` | |
| PRD-030 | Keep Ask and Alchemy state session-only | important | full | `ASK-02`; `NAV-07`; `ALC-06` | |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | full | `ASK-07`; `ASK-08`; `CON-05`; `AI-06` | |
| PRD-032 | Show collection and rating tile indicators | important | full | `HOME-02`; `HOME-05` | |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | full | `DATA-06`; `DATA-10`; `cloud_settings.version` | |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | full | `DATA-07`; `app_metadata` | |
| PRD-035 | Persist synced settings, local settings, UI state | important | full | `Core Persistence Model`; `SET-02`; `SET-03` | |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | full | `DATA-02` | |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | full | `DATA-03`; `Show merge service` | |
| PRD-038 | Provide filters panel and main screen destinations | important | full | `NAV-01` | |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | full | `NAV-02` | |
| PRD-040 | Keep Settings in persistent primary navigation | important | full | `NAV-02` | |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | `Route Map`; `NAV-03` | |
| PRD-042 | Show only library items matching active filters | important | full | `DATA-08`; `HOME-03` | |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | `HOME-01` | |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | full | `DATA-08`; `HOME-03` | |
| PRD-045 | Render poster, title, and My Data badges | important | full | `HOME-02` | |
| PRD-046 | Provide empty-library and empty-filter states | detail | full | `HOME-04` | |
| PRD-047 | Search by title or keywords | important | full | `HOME-05` | |
| PRD-048 | Use poster grid with collection markers | important | partial | `HOME-05` | The plan covers search tiles and indicators, but it does not explicitly lock the Search results into the poster-grid presentation the PRD calls for. |
| PRD-049 | Auto-open Search when setting is enabled | detail | full | `NAV-05` | |
| PRD-050 | Keep Search non-AI in tone | important | full | `NAV-03`; `AI-02` | |
| PRD-051 | Preserve Show Detail narrative section order | important | full | `DET-01` | |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | full | `DET-02` | |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | full | `DET-13` | |
| PRD-054 | Place status/interest controls in toolbar | important | full | `DET-03` | |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | `DET-06` | |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | `DET-05` | |
| PRD-057 | Show overview early for fast scanning | important | full | `DET-08` | |
| PRD-058 | Scoop shows correct states and progressive feedback | important | full | `DET-08`; `DET-09` | |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | full | `DET-10` | |
| PRD-060 | Include traditional recommendations strand | important | full | `DET-11` | |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | full | `EXP-01`; `DET-12` | |
| PRD-062 | Include streaming availability and person-linking credits | important | full | `DET-12`; `PER-01` | |
| PRD-063 | Gate seasons to TV and financials to movies | important | full | `DET-12` | |
| PRD-064 | Keep primary actions early and page not overwhelming | important | partial | `DET-01`; `DET-13` | The plan preserves section order, but it does not add explicit planning work for density management or for enforcing the page’s “powerful but not overwhelming” constraint. |
| PRD-065 | Provide conversational Ask chat interface | important | full | `ASK-01` | |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | full | `ASK-04`; `ASK-09` | |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | `ASK-07` | |
| PRD-068 | Open Detail from mentions or Search fallback | important | full | `ASK-07`; `ASK-08` | |
| PRD-069 | Show six random starter prompts with refresh | important | full | `ASK-01` | |
| PRD-070 | Summarize older turns while preserving voice | important | full | `ASK-02` | |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | full | `ASK-03`; `DET-10` | |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | full | `ASK-05` | |
| PRD-073 | Retry malformed mention output once, then fallback | important | full | `ASK-06` | |
| PRD-074 | Redirect Ask back into TV/movie domain | important | full | `ASK-04` | |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | full | `CON-02`; `CON-06` | |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | full | `CON-01` | |
| PRD-077 | Order concepts by strongest aha and varied axes | important | full | `CON-02`; `CON-04` | |
| PRD-078 | Require concept selection and guide ingredient picking | important | full | `EXP-01`; `ALC-02`; `CON-06` | |
| PRD-079 | Return exactly five Explore Similar recommendations | important | full | `EXP-01` | |
| PRD-080 | Support full Alchemy loop with chaining | important | full | `ALC-01`; `ALC-02`; `ALC-04` | |
| PRD-081 | Clear downstream results when inputs change | important | full | `EXP-02`; `ALC-05` | |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | full | `CON-02`; `CON-03` | |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | full | `EXP-01`; `ALC-02` | |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | full | `ALC-03`; `AI-05` | |
| PRD-085 | Keep one consistent AI persona across surfaces | important | full | `AI-01` | |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | full | `AI orchestration service`; `AI-04` | |
| PRD-087 | Make AI warm, joyful, and light in critique | important | full | `AI-01` | |
| PRD-088 | Structure Scoop as personal taste mini-review | important | full | `AI-03` | |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | full | `ASK-09`; `AI-03` | |
| PRD-090 | Feed AI the right surface-specific context inputs | important | partial | `AI orchestration service`; `ASK-03`; `DET-10` | The plan defines Ask context assembly well, but it does not spell out comparable context contracts for Scoop, Explore Similar, and Alchemy. |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | full | `AI-05`; `AI-06` | |
| PRD-092 | Show person gallery, name, and bio | important | full | `PER-02` | |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | full | `PER-04` | |
| PRD-094 | Group filmography by year | important | full | `PER-03` | |
| PRD-095 | Open Show Detail from selected credit | important | full | `PER-03` | |
| PRD-096 | Include font size and Search-on-launch settings | important | full | `SET-02` | |
| PRD-097 | Support username, model, and API-key settings safely | important | full | `SET-03`; `SET-04` | |
| PRD-098 | Export saved shows and My Data as zip | critical | full | `SET-05` | |
| PRD-099 | Encode export dates using ISO-8601 | important | full | `SET-05` | |

### 3. Coverage Scores

Overall score:

```text
score = (94 × 1.0 + 5 × 0.5) / 99 × 100
      = 96.5 / 99 × 100
      = 97.47%
```

Score by severity tier:

```text
Critical:  (29 × 1.0 + 1 × 0.5) / 30 × 100 = 98.33%  (29 full, 1 partial, 0 missing of 30 critical requirements)
Important: (63 × 1.0 + 4 × 0.5) / 67 × 100 = 97.01%  (63 full, 4 partial, 0 missing of 67 important requirements)
Detail:    (2 × 1.0 + 0 × 0.5) / 2 × 100 = 100.00%  (2 full, 0 partial, 0 missing of 2 detail requirements)
Overall:   97.47% (94 full, 5 partial, 0 missing across 99 requirements)
```

### 4. Top Gaps

1. PRD-002 | critical | Use Supabase official client libraries
The plan locks in Supabase, but not the official SDK requirement. If implemented loosely, the build could drift out of benchmark compliance even while the product features appear correct.

2. PRD-090 | important | Feed AI the right surface-specific context inputs
Ask context is specified, but the other AI surfaces do not get equally explicit context contracts. Without that, Scoop, Explore Similar, and Alchemy are more likely to feel generic or inconsistent with the user’s library and current flow state.

3. PRD-013 | important | Support documented dev auth injection, prod-gated
The plan defines the mechanism, but not how it will be documented for operators and tests. That creates avoidable setup ambiguity in benchmark runs, especially when a fresh evaluator needs to know which header, cookie, or env path is canonical.

4. PRD-064 | important | Keep primary actions early and page not overwhelming
The section order is covered, but the anti-clutter principle is not planned as a concrete UX constraint. If this slips, the Detail page can become technically complete yet feel crowded and slower to scan.

5. PRD-048 | important | Use poster grid with collection markers
Search behavior is planned, but the grid presentation is not locked down. That risks a Search experience that technically works while drifting from the fast visual browsing model the PRD expects.

### 5. Coverage Narrative

#### Overall Posture

This is a strong plan with minor but real gaps. It covers the benchmark baseline, persistence rules, major routes, AI discovery flows, and verification strategy in concrete workstreams, but a handful of requirements still rely on implication instead of an explicit planning commitment.

#### Strength Clusters

The plan is strongest in Benchmark Runtime & Isolation, Collection Data & Persistence, and Show Detail & Relationship UX. Those areas have concrete task IDs, clear sequencing, explicit data rules, and matching validation work, so the core app shape and benchmark-safe storage model are well accounted for.

#### Weakness Clusters

The gaps cluster around specification precision rather than missing feature areas. One cluster is benchmark-operational specificity, where the plan names Supabase and dev auth injection but leaves exact compliance details under-specified. The other cluster is behavioral craft details, where Search presentation, Detail page density, and non-Ask AI context contracts are only partially nailed down.

#### Risk Assessment

If this plan were executed as-is, the most likely failure mode is not a missing page or broken flow; it is drift from the benchmark’s stricter behavioral contract. QA or an evaluator would most likely notice that the implementation works broadly but misses a few exact expectations, such as the official Supabase SDK requirement, operator-facing auth injection guidance, or AI surfaces that do not consistently feel grounded in the right context.

#### Remediation Guidance

The remaining planning work is mostly specification tightening, not new product design. Add explicit implementation constraints for official Supabase client usage, add a concrete documentation artifact for benchmark/dev identity injection, lock Search to a poster-grid result model, state the Detail page’s density/priority rules as acceptance criteria, and define per-surface AI context payloads so every AI entry point is grounded as deliberately as Ask.
