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
| PRD-001 | Use Next.js latest stable runtime | critical | full | 2.1 Application Stack |  |
| PRD-002 | Use Supabase official client libraries | critical | full | 2.1 Application Stack |  |
| PRD-003 | Ship `.env.example` with required variables | critical | full | 3.1 Required Environment Variables |  |
| PRD-004 | Ignore `.env*` secrets except example | important | full | 3.1 Required Environment Variables |  |
| PRD-005 | Configure build through env without code edits | critical | full | 3.1 Required Environment Variables |  |
| PRD-006 | Keep secrets out of repo and server-only | critical | full | 2.1 Application Stack; 3.1 Required Environment Variables |  |
| PRD-007 | Provide app, test, reset command scripts | critical | full | 3.2 Scripts |  |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | 4.1 Supabase Schema |  |
| PRD-009 | Use one stable namespace per build | critical | full | 3.1 Required Environment Variables; 5. Identity and Namespace Isolation |  |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | 5. Identity and Namespace Isolation |  |
| PRD-011 | Attach every user record to `user_id` | critical | full | 4.1 Supabase Schema; 5. Identity and Namespace Isolation |  |
| PRD-012 | Partition persisted data by namespace and user | critical | full | 4.1 Supabase Schema |  |
| PRD-013 | Support documented dev auth injection, prod-gated | important | partial | 3.1 Required Environment Variables; 5. Identity and Namespace Isolation | The plan defines dev identity mechanisms and gating, but it never explicitly calls for documenting that workflow for operators or developers. |
| PRD-014 | Real OAuth later needs no schema redesign | important | partial | 4.1 Supabase Schema; 5. Identity and Namespace Isolation | The plan keeps identity auth-agnostic, but it does not explicitly state that swapping in real OAuth later must avoid any schema redesign. |
| PRD-015 | Keep backend as persisted source of truth | critical | full | 1. Product Understanding |  |
| PRD-016 | Make client cache safe to discard | critical | full | 1. Product Understanding; 10.2 Integration Tests |  |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | full | 3.2 Scripts |  |
| PRD-018 | Overlay saved user data on every show appearance | critical | full | 1. Product Understanding; 8.4 Show Detail |  |
| PRD-019 | Support visible statuses plus hidden `Next` | important | partial | 8.2 Collection Home; 12. Key Risks and Mitigations | The plan mentions Next only as an optional/deferred case and never clearly commits to keeping it in the persisted status model while hidden from the main UI. |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | full | 4.3 Merge and Save Semantics; 8.4 Show Detail |  |
| PRD-021 | Support free-form multi-tag personal tag library | important | full | 1. Product Understanding; 8.1 Shared UI Foundations; 8.2 Collection Home |  |
| PRD-022 | Define collection membership by assigned status | critical | full | 4.3 Merge and Save Semantics |  |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | full | 4.3 Merge and Save Semantics |  |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | 4.3 Merge and Save Semantics |  |
| PRD-025 | Removing status deletes show and all My Data | critical | full | 4.3 Merge and Save Semantics; Phase 5: Show Detail Core |  |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | full | 4.3 Merge and Save Semantics; Phase 3: Catalog Integration |  |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | 4.1 Supabase Schema |  |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | partial | 4.1 Supabase Schema; 4.2 Row-Level Safety; 7.2 Scoop | The plan covers conflict resolution and Scoop freshness, but it does not clearly specify timestamp-driven sort behavior or broader sync semantics for user-facing views. |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | full | 7.2 Scoop |  |
| PRD-030 | Keep Ask and Alchemy state session-only | important | full | 7.3 Ask; 12. Key Risks and Mitigations |  |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | full | 6. External Catalog Integration; 7.3 Ask; 7.4 Concepts, Explore Similar, and Alchemy |  |
| PRD-032 | Show collection and rating tile indicators | important | full | 8.1 Shared UI Foundations |  |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | partial | 4.1 Supabase Schema; 4.3 Merge and Save Semantics | The plan mentions synced settings and per-field conflict resolution, but it does not define duplicate detection and transparent merge behavior for multi-device library consistency. |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | partial | 4.1 Supabase Schema; Phase 1: Project Foundation | The plan introduces app metadata and migrations, but it never specifies a concrete upgrade path that guarantees existing saved libraries survive data-model changes. |
| PRD-035 | Persist synced settings, local settings, UI state | important | partial | 4.1 Supabase Schema; 8.6 Settings and Data; 9. Data Export | Synced settings are planned, but local settings and UI state persistence are only partially specified and some state is left optional. |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | full | 6. External Catalog Integration |  |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | full | 4.3 Merge and Save Semantics |  |
| PRD-038 | Provide filters panel and main screen destinations | important | full | 8.2 Collection Home; Phase 4: Collection Home and Search |  |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | partial | 2.2 Directory Shape; Phase 4: Collection Home and Search | The plan defines a Find/Discover hub, but persistent primary-navigation placement across screens is only implied, not specified. |
| PRD-040 | Keep Settings in persistent primary navigation | important | partial | 2.2 Directory Shape; Phase 9: Person Detail, Settings, and Export | Settings is planned as a route and phase, but the requirement that it stay in persistent primary navigation is not stated directly. |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | 8.3 Find / Discover |  |
| PRD-042 | Show only library items matching active filters | important | full | 8.2 Collection Home |  |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | 8.2 Collection Home |  |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | full | 8.2 Collection Home |  |
| PRD-045 | Render poster, title, and My Data badges | important | full | 8.1 Shared UI Foundations; 8.2 Collection Home |  |
| PRD-046 | Provide empty-library and empty-filter states | detail | full | 8.2 Collection Home |  |
| PRD-047 | Search by title or keywords | important | full | 6. External Catalog Integration; 8.3 Find / Discover |  |
| PRD-048 | Use poster grid with collection markers | important | full | 8.3 Find / Discover |  |
| PRD-049 | Auto-open Search when setting is enabled | detail | full | 8.3 Find / Discover; 8.6 Settings and Data |  |
| PRD-050 | Keep Search non-AI in tone | important | full | 8.3 Find / Discover |  |
| PRD-051 | Preserve Show Detail narrative section order | important | partial | 8.4 Show Detail | The plan includes the required sections, but it reorders the narrative hierarchy instead of preserving the spec's tags/overview/Ask sequence. |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | full | 8.1 Shared UI Foundations; 8.4 Show Detail |  |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | full | 8.4 Show Detail |  |
| PRD-054 | Place status/interest controls in toolbar | important | full | 8.4 Show Detail |  |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | 4.3 Merge and Save Semantics; 8.4 Show Detail |  |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | 4.3 Merge and Save Semantics; 8.4 Show Detail |  |
| PRD-057 | Show overview early for fast scanning | important | full | 8.4 Show Detail |  |
| PRD-058 | Scoop shows correct states and progressive feedback | important | full | 7.2 Scoop; 8.4 Show Detail |  |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | full | 7.3 Ask; 8.4 Show Detail |  |
| PRD-060 | Include traditional recommendations strand | important | full | 8.4 Show Detail |  |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | partial | 7.4 Concepts, Explore Similar, and Alchemy; 8.4 Show Detail | The mechanics are covered, but the plan does not preserve the CTA-first affordance and lightweight entry pattern for Explore Similar. |
| PRD-062 | Include streaming availability and person-linking credits | important | full | 8.4 Show Detail |  |
| PRD-063 | Gate seasons to TV and financials to movies | important | full | 8.4 Show Detail |  |
| PRD-064 | Keep primary actions early and page not overwhelming | important | partial | 8.1 Shared UI Foundations; 8.4 Show Detail | The plan keeps primary controls prominent, but it does not define concrete anti-busyness constraints to keep the detail page from feeling overloaded. |
| PRD-065 | Provide conversational Ask chat interface | important | full | 7.3 Ask; 8.3 Find / Discover |  |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | partial | 7.1 Shared AI Layer; 10.4 AI Quality Validation | The plan captures spoiler safety and taste alignment, but it does not explicitly require Ask answers to lead with direct, confident recommendations. |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | 7.3 Ask |  |
| PRD-068 | Open Detail from mentions or Search fallback | important | full | 7.3 Ask |  |
| PRD-069 | Show six random starter prompts with refresh | important | full | 7.3 Ask |  |
| PRD-070 | Summarize older turns while preserving voice | important | full | 7.1 Shared AI Layer; 7.3 Ask |  |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | full | 7.3 Ask |  |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | full | 7.3 Ask |  |
| PRD-073 | Retry malformed mention output once, then fallback | important | full | 7.3 Ask |  |
| PRD-074 | Redirect Ask back into TV/movie domain | important | full | 7.1 Shared AI Layer |  |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | partial | 7.4 Concepts, Explore Similar, and Alchemy | The plan steers concepts toward vibe and structure, but it never explicitly frames them as taste ingredients rather than genres. |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | full | 7.4 Concepts, Explore Similar, and Alchemy |  |
| PRD-077 | Order concepts by strongest aha and varied axes | important | partial | 7.4 Concepts, Explore Similar, and Alchemy | The plan requires ordering by strength, but it omits the varied-axes rule that keeps concept lists from collapsing into near-synonyms. |
| PRD-078 | Require concept selection and guide ingredient picking | important | partial | 7.4 Concepts, Explore Similar, and Alchemy; 8.1 Shared UI Foundations | The plan requires concept selection, but it does not include UX guidance or copy that teaches users to pick the ingredients they want more of. |
| PRD-079 | Return exactly five Explore Similar recommendations | important | full | 7.4 Concepts, Explore Similar, and Alchemy |  |
| PRD-080 | Support full Alchemy loop with chaining | important | full | 7.4 Concepts, Explore Similar, and Alchemy |  |
| PRD-081 | Clear downstream results when inputs change | important | full | 7.4 Concepts, Explore Similar, and Alchemy |  |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | partial | 7.4 Concepts, Explore Similar, and Alchemy | Multi-show shared concept generation is planned, but the larger candidate pool expected for Alchemy is not specified. |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | full | 7.4 Concepts, Explore Similar, and Alchemy |  |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | partial | 7.1 Shared AI Layer; 10.4 AI Quality Validation | Taste alignment is covered, but the plan does not explicitly optimize for recommendations that are surprising without breaking the user's vibe. |
| PRD-085 | Keep one consistent AI persona across surfaces | important | full | 1. Product Understanding; 7.1 Shared AI Layer |  |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | full | 7.1 Shared AI Layer |  |
| PRD-087 | Make AI warm, joyful, and light in critique | important | partial | 7.1 Shared AI Layer | The plan captures warmth and honesty, but it does not explicitly preserve the spec's joyful, light-touch handling of criticism. |
| PRD-088 | Structure Scoop as personal taste mini-review | important | full | 7.2 Scoop |  |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | partial | 7.3 Ask | The Ask section defines structure and state, but it does not explicitly constrain default responses to stay brisk and dialogue-like. |
| PRD-090 | Feed AI the right surface-specific context inputs | important | full | 7.1 Shared AI Layer |  |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | full | 10.4 AI Quality Validation |  |
| PRD-092 | Show person gallery, name, and bio | important | full | 8.5 Person Detail |  |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | full | 8.5 Person Detail |  |
| PRD-094 | Group filmography by year | important | full | 8.5 Person Detail |  |
| PRD-095 | Open Show Detail from selected credit | important | full | 8.5 Person Detail |  |
| PRD-096 | Include font size and Search-on-launch settings | important | full | 8.6 Settings and Data |  |
| PRD-097 | Support username, model, and API-key settings safely | important | full | 8.6 Settings and Data |  |
| PRD-098 | Export saved shows and My Data as zip | critical | full | 8.6 Settings and Data; 9. Data Export |  |
| PRD-099 | Encode export dates using ISO-8601 | important | full | 8.6 Settings and Data; 9. Data Export |  |

## 3. Coverage Scores

Overall score = (79 × 1.0 + 20 × 0.5) / 99 × 100 = 89.9%

Critical:  (29 × 1.0 + 1 × 0.5) / 30 × 100 = 98.3%  (29.5 of 30 critical requirements)
Important: (48 × 1.0 + 19 × 0.5) / 67 × 100 = 85.8%  (57.5 of 67 important requirements)
Detail:    (2 × 1.0 + 0 × 0.5) / 2 × 100 = 100.0%  (2 of 2 detail requirements)
Overall:   89.9%  (89 of 99 total requirements)

## 4. Top Gaps

- PRD-034 | `critical` | Preserve saved libraries across data-model upgrades: Without an explicit upgrade path, a schema migration can strand or silently drop saved shows, ratings, tags, and Scoop data, which is the highest-impact trust failure in the benchmark.
- PRD-051 | `important` | Preserve Show Detail narrative section order: If the detail page is implemented in the planned order, the screen will still work, but it will lose the scanning flow and editorial rhythm that the spec treats as part of the product contract.
- PRD-066 | `important` | Answer directly with confident, spoiler-safe recommendations: Ask can easily become verbose or hedged unless the response contract is explicit, and users will notice that drift immediately in the flagship conversational surface.
- PRD-084 | `important` | Deliver surprising but defensible taste-aligned recommendations: A plan that targets only generic taste alignment risks safe but forgettable recommendations, which undercuts the app's promised discovery value even if the mechanics technically work.
- PRD-033 | `important` | Sync libraries/settings consistently and merge duplicates: Cross-device consistency is part of the persistence contract, and leaving duplicate detection and merge behavior vague invites subtle library corruption and support churn later.

## 5. Coverage Narrative

#### Overall Posture
This is a strong, structurally sound plan. It covers the major product surfaces, the benchmark isolation model, and most of the persistence and AI contracts with concrete implementation phases. The remaining issues are concentrated in a small number of nuanced but meaningful contracts rather than broad feature omissions.

#### Strength Clusters
The plan is strongest in Benchmark Runtime & Isolation, Collection Home & Search, Person Detail, and Settings & Export. It is also notably solid in the core persistence model and in the main feature decomposition for Show Detail, Ask, Explore Similar, and Alchemy, where the plan usually names concrete behaviors, storage rules, and verification paths.

#### Weakness Clusters
The gaps cluster around behavioral fidelity rather than missing screens. The biggest pattern is under-specified quality contracts: upgrade continuity and sync semantics in Collection Data & Persistence, navigation permanence in App Navigation & Discover Shell, and voice/interaction nuance in Show Detail, Ask, Concepts, and AI Voice.

#### Risk Assessment
If executed as-is, the app would likely ship with the right pages and data model, but some of the product-defining feel would drift. QA would probably first notice that Show Detail does not follow the expected narrative flow and that Ask/recommendation behavior is functional but not tightly constrained to the direct, surprising, on-brand experience the PRD expects. The longer-term operational risk is schema evolution without an explicit continuity plan for existing user libraries.

#### Remediation Guidance
The plan needs another pass on specification-level contracts, not a new feature list. Tighten the upgrade and sync story with explicit migration and duplicate-merge rules, make the navigation and detail-page ordering requirements explicit, and add sharper acceptance criteria for Ask, concept UX, and recommendation quality so the implementation team is not left to infer the product's most distinctive behaviors.
