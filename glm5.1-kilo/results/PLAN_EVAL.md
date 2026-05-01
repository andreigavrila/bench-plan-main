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
| PRD-001 | Use Next.js latest stable runtime | critical | full | Section 1.1 Core Framework |  |
| PRD-002 | Use Supabase official client libraries | critical | full | Section 1.2 Persistence Layer |  |
| PRD-003 | Ship `.env.example` with required variables | critical | full | Section 8.1 Required Environment Variables |  |
| PRD-004 | Ignore `.env*` secrets except example | important | full | Section 8.1 Security Rules |  |
| PRD-005 | Configure build through env without code edits | critical | full | Sections 2.4 Namespace & User Context; 8.1 Required Environment Variables |  |
| PRD-006 | Keep secrets out of repo and server-only | critical | full | Sections 7.2 AI Settings; 8.1 Security Rules |  |
| PRD-007 | Provide app, test, reset command scripts | critical | full | Section 11. Development Scripts |  |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | Section 10.1 Migration Artifacts |  |
| PRD-009 | Use one stable namespace per build | critical | full | Sections 2.4 Namespace & User Context; 7.5 Namespace & User ID Injection |  |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | Sections 2.4 Namespace & User Context; 9.4 Test Data Management |  |
| PRD-011 | Attach every user record to `user_id` | critical | partial | Executive Summary; Section 5.3 Data Service; Section 7.5 Namespace & User ID Injection | The plan passes `user_id` through services, but the proposed `shows` schema and RLS never persist or enforce it. |
| PRD-012 | Partition persisted data by namespace and user | critical | partial | Sections 2.1 Database Schema; 2.2 RLS Policies; 5.3 Data Service | Partitioning is only explicit for `namespace_id` on `shows`, so the effective `(namespace_id, user_id)` boundary is incomplete. |
| PRD-013 | Support documented dev auth injection, prod-gated | important | partial | Sections 2.4 Namespace & User Context; 7.5 Namespace & User ID Injection | Header-based dev identity is documented, but the plan never states how that path is disabled or gated in production. |
| PRD-014 | Real OAuth later needs no schema redesign | important | partial | Sections 2.4 Namespace & User Context; 7.5 Namespace & User ID Injection | The plan hints at prod auth, but it never states that real OAuth can be added without schema changes, and the missing `shows.user_id` weakens that path. |
| PRD-015 | Keep backend as persisted source of truth | critical | full | Sections 1.2 Persistence Layer; 5.3 Data Service |  |
| PRD-016 | Make client cache safe to discard | critical | partial | Section 1.4 Data Fetching & State; Section 5.3 Data Service | It uses server-state caching, but never explicitly requires local cache/storage to be disposable without user-data loss. |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | partial | Section 1.2 Persistence Layer | The plan never explicitly says Docker is optional or unsupported for the benchmark path. |
| PRD-018 | Overlay saved user data on every show appearance | critical | full | Executive Summary; Section 14. Success Criteria |  |
| PRD-019 | Support visible statuses plus hidden `Next` | important | full | Sections 3.1 Core Types; 12. Open Questions & Decisions |  |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | full | Section 6.5 My Relationship Controls (Status Toolbar) |  |
| PRD-021 | Support free-form multi-tag personal tag library | important | full | Sections 2.1 `shows` table; 7.2 Filter System |  |
| PRD-022 | Define collection membership by assigned status | critical | full | Section 6.1 Data Query (`my_status IS NOT NULL`) |  |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | full | Section 7.1 Auto-Save Behaviors |  |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | Section 7.1 Auto-Save Behaviors |  |
| PRD-025 | Removing status deletes show and all My Data | critical | full | Section 6.5 My Relationship Controls; Section 7.1 Auto-Save Behaviors |  |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | full | Sections 2.3 Merge Logic Layer; 5.4 Show Merge Service |  |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | Sections 2.1 `shows` table; 3.1 Core Types |  |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | full | Sections 6.1 Data Query; 2.3 Merge Logic Layer; 6.5 Overview + Scoop |  |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | full | Section 6.5 Overview + Scoop |  |
| PRD-030 | Keep Ask and Alchemy state session-only | important | partial | Sections 6.3 Ask; 6.4 Alchemy; 2.1 `shows` table | Ask and Alchemy state are absent from storage, but the plan never explicitly says they are cleared when leaving or resetting those surfaces. |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | full | Sections 5.2 Catalog Service; 7.3 Recommendation Resolution |  |
| PRD-032 | Show collection and rating tile indicators | important | full | Sections 6.1 Collection Home; 6.2 Search; 14. Success Criteria |  |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | partial | Sections 2.3 Merge Logic Layer; 5.3 Data Service; 14. Success Criteria | Per-field merge rules and synced settings are planned, but duplicate detection and transparent library merge behavior are not spelled out. |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | full | Sections 10.2 Data Model Versioning; 10.3 Data Continuity Rule |  |
| PRD-035 | Persist synced settings, local settings, UI state | important | partial | Sections 7.4 Export/Backup Data Format; 6.7 Settings | The snapshot shape includes local settings and UI state, but the plan does not describe persisting last filter or removal-confirmation UI state in the product. |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | full | Sections 2.1 `shows` table; 5.2 Catalog Service |  |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | full | Sections 2.3 Merge Logic Layer; 5.4 Show Merge Service |  |
| PRD-038 | Provide filters panel and main screen destinations | important | full | Sections 4. Directory Structure; 6.1 Collection Home |  |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | partial | Sections 4. Directory Structure (`find/`); mode-switcher feature | Find/Discover exists, but the plan never explicitly places it in persistent primary navigation. |
| PRD-040 | Keep Settings in persistent primary navigation | important | partial | Sections 4. Directory Structure (`settings/`); 6.7 Settings | Settings exists, but the plan never explicitly places it in persistent primary navigation. |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | Sections 4. Directory Structure; 6.2 Search; 6.3 Ask; 6.4 Alchemy |  |
| PRD-042 | Show only library items matching active filters | important | full | Section 6.1 Key Behaviors; Section 7.2 `applyFilter` |  |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | Section 6.1 Key Behaviors |  |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | full | Section 7.2 Filter System |  |
| PRD-045 | Render poster, title, and My Data badges | important | full | Section 6.1 Key Behaviors |  |
| PRD-046 | Provide empty-library and empty-filter states | detail | missing | none | The plan does not cover either the empty-library prompt to Search/Ask or the empty-filter "No results found" state. |
| PRD-047 | Search by title or keywords | important | full | Section 6.2 Key Behaviors |  |
| PRD-048 | Use poster grid with collection markers | important | full | Section 6.2 Key Behaviors |  |
| PRD-049 | Auto-open Search when setting is enabled | detail | partial | Section 6.7 App Settings | The Search-on-launch setting is planned, but the plan never connects it to an auto-open behavior on app launch. |
| PRD-050 | Keep Search non-AI in tone | important | partial | Section 6.2 Search | Search is described as catalog search, but the plan never explicitly protects it from AI-style voice or conversational framing. |
| PRD-051 | Preserve Show Detail narrative section order | important | full | Section 6.5 Narrative Order (preserved) |  |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | full | Section 6.5 Header Media |  |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | full | Section 6.5 Core Facts + Community Score |  |
| PRD-054 | Place status/interest controls in toolbar | important | full | Section 6.5 My Relationship Controls (Status Toolbar) |  |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | Section 7.1 `autoSave` tags block |  |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | Section 6.5 My Relationship Controls; Section 7.1 `autoSave` score block |  |
| PRD-057 | Show overview early for fast scanning | important | full | Section 6.5 Narrative Order; Section 6.5 Overview + Scoop |  |
| PRD-058 | Scoop shows correct states and progressive feedback | important | partial | Section 6.5 Overview + Scoop | The plan covers toggle labels, freshness, and generating feedback, but it does not fully specify the complete Scoop state model the UX doc calls for. |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | full | Section 6.5 Ask About This Show |  |
| PRD-060 | Include traditional recommendations strand | important | full | Section 6.5 Traditional Recommendations |  |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | full | Section 6.5 Explore Similar |  |
| PRD-062 | Include streaming availability and person-linking credits | important | full | Sections 6.5 Streaming Availability; 6.5 Cast & Crew |  |
| PRD-063 | Gate seasons to TV and financials to movies | important | full | Sections 6.5 Seasons (TV only); 6.5 Budget/Revenue (Movies only) |  |
| PRD-064 | Keep primary actions early and page not overwhelming | important | partial | Section 6.5 Narrative Order | The order helps, but the plan never translates "powerful but not overwhelming" into concrete busyness-control decisions. |
| PRD-065 | Provide conversational Ask chat interface | important | full | Section 6.3 Key Behaviors; Implementation Steps |  |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | partial | Section 6.3 Prompt Template (Ask persona) | Tone and spoiler-safety are planned, but the response contract does not require a direct answer up front or list formatting for multi-recs. |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | Section 6.3 Key Behaviors; Step 4 `MentionedShows` |  |
| PRD-068 | Open Detail from mentions or Search fallback | important | full | Section 6.3 Key Behaviors |  |
| PRD-069 | Show six random starter prompts with refresh | important | full | Section 6.3 Key Behaviors; Step 5 `useRandomPrompts` |  |
| PRD-070 | Summarize older turns while preserving voice | important | partial | Section 6.3 Key Behaviors; Step 2 `useAskChat` | Summarization is planned, but the plan never says summaries must preserve the same persona and voice as the live chat. |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | full | Section 6.3 Key Behaviors |  |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | full | Section 5.1 `AIService.chat`; Section 6.3 Prompt Template |  |
| PRD-073 | Retry malformed mention output once, then fallback | important | missing | none | The plan defines parsing and Search fallback for unresolved shows, but it never adds the required one-time retry for malformed structured output. |
| PRD-074 | Redirect Ask back into TV/movie domain | important | full | Section 6.3 Prompt Template |  |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | full | Section 6.4 Concept Extraction Prompt |  |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | full | Section 6.4 Concept Extraction Prompt |  |
| PRD-077 | Order concepts by strongest aha and varied axes | important | partial | Section 6.4 Concept Extraction Prompt | The prompt covers multiple concept axes, but it never requires strongest concepts first or enforces diversity across the returned set. |
| PRD-078 | Require concept selection and guide ingredient picking | important | partial | Section 6.4 `ConceptExtraction` component; Section 6.5 Explore Similar | Selection is required, but the plan omits the ingredient-picking guidance and empty-state nudges described in the concept UX rules. |
| PRD-079 | Return exactly five Explore Similar recommendations | important | full | Section 6.5 Explore Similar |  |
| PRD-080 | Support full Alchemy loop with chaining | important | full | Section 6.4 Flow; Implementation Steps |  |
| PRD-081 | Clear downstream results when inputs change | important | missing | none | The plan supports chaining, but it never states that changing input shows or concept selections clears stale downstream concepts/results. |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | partial | Section 6.4 Concept Extraction Prompt; Section 6.5 single-show note | Shared concepts are planned, but the multi-show flow does not commit to returning a larger option pool than single-show Explore Similar. |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | full | Section 6.4 Recommendation Prompt |  |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | partial | Section 6.4 Recommendation Prompt; Section 14. Success Criteria | The plan grounds recs in concepts and library data, but it does not define a quality bar for pleasant surprise without vibe-breaking misses. |
| PRD-085 | Keep one consistent AI persona across surfaces | important | partial | Section 5.1 Prompt Templates; Section 14. Success Criteria | The plan wants on-brand consistency, but it fully specifies persona only for some surfaces rather than defining one shared cross-surface contract. |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | partial | Section 6.3 Prompt Template; Section 6.5 Scoop Prompt Structure | Guardrails appear in individual prompts, but there is no shared AI rule layer that all surfaces must inherit. |
| PRD-087 | Make AI warm, joyful, and light in critique | important | partial | Section 6.3 Prompt Template; Section 6.5 Scoop Prompt Structure | Warmth and honesty show up in Ask/Scoop, but the plan does not make joy-forward, light critique an explicit requirement for every AI surface. |
| PRD-088 | Structure Scoop as personal taste mini-review | important | full | Section 6.5 Scoop Prompt Structure |  |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | partial | Section 6.3 Prompt Template (Ask persona) | Ask is conversational, but the plan does not specify brisk default length or scan-friendly formatting. |
| PRD-090 | Feed AI the right surface-specific context inputs | important | full | Sections 6.3 Data Context Sent to AI; 6.4 AI Context; 5.1 `AIService` |  |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | partial | Sections 9.1-9.3 Testing Strategy; 14. Success Criteria | The plan includes tests and high-level success criteria, but it never adopts the discovery rubric or a hard-fail integrity gate for bad IDs/titles. |
| PRD-092 | Show person gallery, name, and bio | important | full | Section 6.6 `ProfileHeader` |  |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | full | Section 6.6 `AnalyticsCharts` |  |
| PRD-094 | Group filmography by year | important | full | Section 6.6 `Filmography` |  |
| PRD-095 | Open Show Detail from selected credit | important | full | Section 6.6 `Filmography` |  |
| PRD-096 | Include font size and Search-on-launch settings | important | full | Section 6.7 App Settings |  |
| PRD-097 | Support username, model, and API-key settings safely | important | partial | Sections 2.1 `cloud_settings` table; 6.7 AI Settings | The schema includes `user_name`, but the Settings plan omits username UI and catalog provider key management called for by the PRD. |
| PRD-098 | Export saved shows and My Data as zip | critical | full | Section 6.7 Export/Import |  |
| PRD-099 | Encode export dates using ISO-8601 | important | full | Sections 6.7 Export/Import; 7.4 Export/Backup Data Format |  |

## 3. Coverage Scores

Overall score:

`score = (full_count × 1.0 + partial_count × 0.5) / total_count × 100`

`score = (69 × 1.0 + 27 × 0.5) / 99 × 100 = 83.33%`

Critical:  (26 × 1.0 + 4 × 0.5) / 30 × 100 = 93.33%  (28.0 of 30 critical requirements)
Important: (43 × 1.0 + 22 × 0.5) / 67 × 100 = 80.60%  (54.0 of 67 important requirements)
Detail:    (0 × 1.0 + 1 × 0.5) / 2 × 100 = 25.00%  (0.5 of 2 detail requirements)
Overall:   83.33% (99 total requirements)

## 4. Top Gaps

- `PRD-011` | `critical` | Attach every user record to `user_id`
  The main `shows` entity is still modeled without `user_id`, so a user-owned library can collide with another user's data inside the same namespace and later auth work starts from the wrong persistence boundary.
- `PRD-012` | `critical` | Partition persisted data by namespace and user
  The schema and RLS isolate `shows` only by `namespace_id`, which means multi-user correctness inside a benchmark build is not actually guaranteed.
- `PRD-086` | `critical` | Enforce shared AI guardrails across all surfaces
  Without one shared AI rule set, Ask, Scoop, Explore Similar, and Alchemy can drift on domain limits, spoiler safety, and honesty, which directly erodes trust in the product's AI identity.
- `PRD-016` | `critical` | Make client cache safe to discard
  If this is not explicit, an implementation can quietly rely on local persistence for correctness and lose user-visible data after cache clears, reinstalls, or device changes.
- `PRD-081` | `important` | Clear downstream results when inputs change
  If stale concepts or recommendations survive input edits, Alchemy can present recommendations that no longer match the selected shows, producing an obvious UX correctness failure.

## 5. Coverage Narrative

#### Overall Posture

This is a structurally strong plan with a few concerning holes. It covers most of the product surface concretely, especially the page architecture, data model, detail page, and major discovery flows, but it falls short on some benchmark-critical execution rules and a handful of AI behavioral contracts.

#### Strength Clusters

The strongest coverage is in Show Detail & Relationship UX, Collection Home & Search core behaviors, and Person Detail. The plan is also solid on migrations, export format, recommendation resolution, and the main feature decomposition into Home, Search, Ask, Alchemy, Detail, Person, and Settings.

#### Weakness Clusters

The biggest gaps cluster around two patterns. First, benchmark isolation semantics are only half-carried through: the plan talks about `user_id`, but the proposed `shows` schema and RLS still behave like namespace-only partitioning. Second, AI quality rules are spread across local prompt snippets instead of being defined as shared cross-surface contracts, which leaves Ask, Scoop, Explore Similar, and Alchemy vulnerable to behavioral drift. A smaller cluster sits in edge-state UX and flow hygiene: empty states, Search-on-launch wiring, malformed Ask output recovery, and clearing stale Alchemy results.

#### Risk Assessment

If this plan were executed as-is, the first serious QA issue would likely be incorrect user isolation inside a shared namespace: saved shows would not be safely partitioned by both build and user. After that, reviewers would notice AI behavior inconsistencies and flow bugs around Ask and Alchemy, especially when structured output is malformed or downstream recommendations no longer match the current inputs.

#### Remediation Guidance

The remaining planning work is not a full rewrite; it is targeted specification tightening. The plan needs explicit schema/RLS decisions for `(namespace_id, user_id)` ownership, an explicit disposable-cache rule, and one shared AI contract section that all surfaces inherit for guardrails, tone, fallback behavior, and quality validation. It also needs a short pass over UX edge states and interaction resets so launch/settings behaviors, empty states, and downstream invalidation are planned rather than implied.
