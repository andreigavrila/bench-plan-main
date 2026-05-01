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

### 2. Coverage Table

| PRD-ID | Requirement | Severity | Coverage | Evidence | Gap |
| ------ | ----------- | -------- | -------- | -------- | --- |
| PRD-001 | Use Next.js latest stable runtime | critical | full | `1.3 Technical Stack Requirements (Benchmark Baseline)` | |
| PRD-002 | Use Supabase official client libraries | critical | partial | `1.3 Technical Stack Requirements (Benchmark Baseline)` | The plan commits to Supabase but never specifies the official client libraries to use across browser/server boundaries. |
| PRD-003 | Ship `.env.example` with required variables | critical | full | `7.1 Environment Configuration` | |
| PRD-004 | Ignore `.env*` secrets except example | important | full | `7.1 Environment Configuration` | |
| PRD-005 | Configure build through env without code edits | critical | partial | `7.1 Environment Configuration` | It enumerates env vars but does not state that all build configuration is exclusively env-driven with no source edits allowed. |
| PRD-006 | Keep secrets out of repo and server-only | critical | full | `4.8 Settings & Data Management`; `7.1 Environment Configuration` | |
| PRD-007 | Provide app, test, reset command scripts | critical | full | `9.1 One-Command Setup` | |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | `7.2 Database Evolution` | |
| PRD-009 | Use one stable namespace per build | critical | full | `2.2 Isolation Model (Critical for Benchmark)` | |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | `2.2 Isolation Model (Critical for Benchmark)`; `9.2 Test Data Management`; `9.3 Destructive Testing Support` | |
| PRD-011 | Attach every user record to `user_id` | critical | full | `2.2 Isolation Model (Critical for Benchmark)`; `3.1.1 Show (Primary Entity)`; `3.1.2 Cloud Settings (User Preferences)` | |
| PRD-012 | Partition persisted data by namespace and user | critical | full | `2.2 Isolation Model (Critical for Benchmark)`; `3.1.1 Show (Primary Entity)` | |
| PRD-013 | Support documented dev auth injection, prod-gated | important | partial | `2.2 Isolation Model (Critical for Benchmark)`; `7.4 Authentication Middleware` | The dev injection path is described, but the plan does not call out documentation requirements or an explicit production gate or disable mechanism. |
| PRD-014 | Real OAuth later needs no schema redesign | important | full | `7.4 Authentication Middleware` | |
| PRD-015 | Keep backend as persisted source of truth | critical | full | `2.1 High-Level Architecture`; `3.2 Local Storage (Client-Side)` | |
| PRD-016 | Make client cache safe to discard | critical | partial | `3.2 Local Storage (Client-Side)` | The plan keeps most data server-side, but it never states that clearing any client cache or local persistence is guaranteed safe. |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | full | `12.3 Benchmark Compliance Risks`; `13.3 Benchmark Compliance Checklist` | |
| PRD-018 | Overlay saved user data on every show appearance | critical | partial | `1.1 Product Summary`; `4.1 Collection Home`; `4.2 Show Detail Page` | The plan never turns overlay-everywhere into a cross-cutting rendering rule for search, recommendations, and AI outputs. |
| PRD-019 | Support visible statuses plus hidden `Next` | important | partial | `3.1.1 Show (Primary Entity)`; `8.1 Core Components` | The schema includes `next`, but the plan does not explicitly preserve it as a hidden data-model-only status while keeping the visible chip set separate. |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | partial | `4.1 Collection Home`; `6.2 Saving Triggers` | Interested and Excited appear in grouping logic, but the plan never explicitly defines the chip mapping to `Later` plus `my_interest`. |
| PRD-021 | Support free-form multi-tag personal tag library | important | full | `4.1 Collection Home`; `8.1 Core Components` | |
| PRD-022 | Define collection membership by assigned status | critical | full | `6.1 Collection Membership` | |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | full | `6.2 Saving Triggers` | |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | `6.3 Default Values` | |
| PRD-025 | Removing status deletes show and all My Data | critical | full | `6.4 Removal from Collection` | |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | full | `6.5 Re-adding Same Show` | |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | `3.1.1 Show (Primary Entity)`; `6.5 Re-adding Same Show` | |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | partial | `3.3 Data Merge & Conflict Resolution Rules`; `6.6 AI Data Persistence` | Sync and freshness are covered, but the plan never assigns timestamps to sorting behavior. |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | full | `5.2.2 Scoop (Show Detail)`; `6.6 AI Data Persistence` | |
| PRD-030 | Keep Ask and Alchemy state session-only | important | full | `3.2 Local Storage (Client-Side)`; `6.6 AI Data Persistence` | |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | full | `5.2.4 Concept-Based Recommendations`; `11.4 External Catalog ID Mapping` | |
| PRD-032 | Show collection and rating tile indicators | important | full | `4.1 Collection Home`; `6.7 Tile Indicators` | |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | partial | `3.3 Data Merge & Conflict Resolution Rules`; `4.8 Settings & Data Management` | Conflict resolution is planned, but transparent duplicate detection and merge behavior for libraries is not called out. |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | partial | `3.1.3 App Metadata (Migration Tracking)`; `7.2 Database Evolution` | It includes migrations and version tracking, but not a concrete continuity strategy ensuring existing libraries survive model upgrades unchanged. |
| PRD-035 | Persist synced settings, local settings, UI state | important | full | `3.1.2 Cloud Settings (User Preferences)`; `3.2 Local Storage (Client-Side)` | |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | partial | `3.1.1 Show (Primary Entity)` | The schema persists `provider_data`, but the plan does not explicitly state that detailed credits, media, and recommendation payloads remain transient fetches. |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | full | `3.3 Data Merge & Conflict Resolution Rules` | |
| PRD-038 | Provide filters panel and main screen destinations | important | full | `4.1 Collection Home`; `8.2 Page Layouts`; `8.3 Navigation Structure` | |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | full | `8.3 Navigation Structure` | |
| PRD-040 | Keep Settings in persistent primary navigation | important | full | `8.3 Navigation Structure` | |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | `4.3 Search (Find → Search)`; `4.4 Ask (Find → Ask) - Conversational AI`; `4.5 Alchemy (Find → Alchemy) - Concept Blending`; `8.3 Navigation Structure` | |
| PRD-042 | Show only library items matching active filters | important | full | `4.1 Collection Home` | |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | `4.1 Collection Home` | |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | full | `4.1 Collection Home` | |
| PRD-045 | Render poster, title, and My Data badges | important | full | `4.1 Collection Home`; `8.1 Core Components` | |
| PRD-046 | Provide empty-library and empty-filter states | detail | partial | `4.1 Collection Home` | The no-library state is planned, but the no-results-for-active-filter state is not explicitly covered. |
| PRD-047 | Search by title or keywords | important | full | `4.3 Search (Find → Search)` | |
| PRD-048 | Use poster grid with collection markers | important | full | `4.3 Search (Find → Search)` | |
| PRD-049 | Auto-open Search when setting is enabled | detail | full | `4.3 Search (Find → Search)`; `4.8 Settings & Data Management` | |
| PRD-050 | Keep Search non-AI in tone | important | missing | none | The plan treats Search as a feature area but never specifies that Search must remain a straightforward non-AI catalog surface. |
| PRD-051 | Preserve Show Detail narrative section order | important | full | `4.2 Show Detail Page` | |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | partial | `4.2 Show Detail Page`; `10. Implementation Phases > Phase 4: Polish & Refinement` | The motion-rich header is present, but the graceful fallback behavior for missing trailers or backdrops is not planned. |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | full | `4.2 Show Detail Page` | |
| PRD-054 | Place status/interest controls in toolbar | important | missing | none | The plan lists status chips as a component, but never specifies the required toolbar placement on the detail page. |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | `4.2 Show Detail Page` | |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | `4.2 Show Detail Page` | |
| PRD-057 | Show overview early for fast scanning | important | full | `4.2 Show Detail Page` | |
| PRD-058 | Scoop shows correct states and progressive feedback | important | partial | `5.2.2 Scoop (Show Detail)` | It mentions streaming and progressive generation, but not the detailed closed, cached, generating, and open states called out by the UX spec. |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | full | `4.4 Ask (Find → Ask) - Conversational AI` | |
| PRD-060 | Include traditional recommendations strand | important | full | `4.2 Show Detail Page` | |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | full | `4.6 Explore Similar (Per-Show Concepts)` | |
| PRD-062 | Include streaming availability and person-linking credits | important | full | `4.2 Show Detail Page`; `4.7 Person Detail Page` | |
| PRD-063 | Gate seasons to TV and financials to movies | important | full | `4.2 Show Detail Page` | |
| PRD-064 | Keep primary actions early and page not overwhelming | important | partial | `4.2 Show Detail Page` | The section order helps, but the plan never translates the "primary actions early, long-tail info down-page" principle into explicit layout constraints. |
| PRD-065 | Provide conversational Ask chat interface | important | full | `4.4 Ask (Find → Ask) - Conversational AI` | |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | full | `4.4 Ask (Find → Ask) - Conversational AI`; `5.1 AI Persona & Voice Consistency`; `5.2.1 Ask (Chat)` | |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | `4.4 Ask (Find → Ask) - Conversational AI` | |
| PRD-068 | Open Detail from mentions or Search fallback | important | partial | `4.4 Ask (Find → Ask) - Conversational AI` | Selectable mentions are planned, but the required Detail-open and Search-handoff fallback behavior is not fully specified. |
| PRD-069 | Show six random starter prompts with refresh | important | partial | `4.4 Ask (Find → Ask) - Conversational AI` | The six starter prompts are included, but the plan omits the refresh or regenerate behavior. |
| PRD-070 | Summarize older turns while preserving voice | important | partial | `4.4 Ask (Find → Ask) - Conversational AI`; `5.3 Context Management` | Summarization is included, but the plan does not say summaries must preserve the same conversational voice. |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | full | `4.4 Ask (Find → Ask) - Conversational AI` | |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | partial | `5.2.1 Ask (Chat)` | The `showList` string format appears, but the plan omits the enclosing `commentary` and `showList` structured contract the UI parser depends on. |
| PRD-073 | Retry malformed mention output once, then fallback | important | missing | none | No retry-once-then-fallback path is planned for malformed mention output. |
| PRD-074 | Redirect Ask back into TV/movie domain | important | partial | `5.1 AI Persona & Voice Consistency` | The persona is TV/movie-focused, but the plan never specifies redirecting out-of-domain requests back into the supported domain. |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | partial | `4.5 Alchemy (Find → Alchemy) - Concept Blending`; `4.6 Explore Similar (Per-Show Concepts)`; `5.2.3 Concepts Generation` | Concepts are treated as generated AI artifacts, but the plan never anchors them as taste ingredients distinct from genres. |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | full | `5.2.3 Concepts Generation` | |
| PRD-077 | Order concepts by strongest aha and varied axes | important | missing | none | The plan does not require ordering concepts by strongest aha first or diversifying them across structure, vibe, and emotion axes. |
| PRD-078 | Require concept selection and guide ingredient picking | important | partial | `4.5 Alchemy (Find → Alchemy) - Concept Blending`; `4.6 Explore Similar (Per-Show Concepts)` | Selection is required, but the guidance copy about "ingredients you want more of" and explicit empty-state prompting is absent. |
| PRD-079 | Return exactly five Explore Similar recommendations | important | full | `4.6 Explore Similar (Per-Show Concepts)`; `5.2.4 Concept-Based Recommendations` | |
| PRD-080 | Support full Alchemy loop with chaining | important | full | `4.5 Alchemy (Find → Alchemy) - Concept Blending` | |
| PRD-081 | Clear downstream results when inputs change | important | missing | none | The plan never says changing shows or concepts must clear downstream concepts and results before recomputing. |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | partial | `4.5 Alchemy (Find → Alchemy) - Concept Blending`; `5.2.3 Concepts Generation` | Shared multi-show concepts are planned, but not the larger candidate pool expected before the UI selection cap. |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | full | `4.6 Explore Similar (Per-Show Concepts)`; `5.2.4 Concept-Based Recommendations` | |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | full | `5.3 Context Management` | |
| PRD-085 | Keep one consistent AI persona across surfaces | important | full | `4.4 Ask (Find → Ask) - Conversational AI`; `5.1 AI Persona & Voice Consistency` | |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | partial | `5.1 AI Persona & Voice Consistency`; `5.3 Context Management` | Voice principles are listed, but the plan does not define a shared guardrail layer enforcing domain, spoiler, honesty, and actionable-real-show rules across every AI surface. |
| PRD-087 | Make AI warm, joyful, and light in critique | important | full | `5.1 AI Persona & Voice Consistency` | |
| PRD-088 | Structure Scoop as personal taste mini-review | important | full | `5.2.2 Scoop (Show Detail)` | |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | full | `5.2.1 Ask (Chat)` | |
| PRD-090 | Feed AI the right surface-specific context inputs | important | full | `5.3 Context Management` | |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | partial | `5.3 Context Management`; `12.2 Product Risks` | It names quality dimensions, but not a concrete scoring gate with hard-fail treatment for real-show integrity. |
| PRD-092 | Show person gallery, name, and bio | important | full | `4.7 Person Detail Page` | |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | full | `4.7 Person Detail Page` | |
| PRD-094 | Group filmography by year | important | full | `4.7 Person Detail Page` | |
| PRD-095 | Open Show Detail from selected credit | important | full | `4.7 Person Detail Page` | |
| PRD-096 | Include font size and Search-on-launch settings | important | full | `4.8 Settings & Data Management` | |
| PRD-097 | Support username, model, and API-key settings safely | important | full | `4.8 Settings & Data Management` | |
| PRD-098 | Export saved shows and My Data as zip | critical | full | `4.8 Settings & Data Management` | |
| PRD-099 | Encode export dates using ISO-8601 | important | full | `4.8 Settings & Data Management` | |

### 3. Coverage Scores

Critical:  (22 x 1.0 + 8 x 0.5) / 30 x 100 = 86.67%  (26 of 30 critical requirements)
Important: (46 x 1.0 + 16 x 0.5) / 67 x 100 = 80.60%  (54 of 67 important requirements)
Detail:    (1 x 1.0 + 1 x 0.5) / 2 x 100 = 75.00%  (1.5 of 2 detail requirements)
Overall:   (69 x 1.0 + 25 x 0.5) / 99 x 100 = 82.32%  (81.5 of 99 total requirements)

### 4. Top Gaps

- PRD-072 | critical | Emit `commentary` plus exact `showList` contract: The Ask surface can look complete in a demo yet still fail the UI integration, because the parser depends on an exact two-field contract rather than approximate structured text.
- PRD-018 | critical | Overlay saved user data on every show appearance: If overlay behavior is not treated as a global rule, search, recommendations, and AI results will show inconsistent statuses and ratings, which makes the user's library feel unreliable.
- PRD-086 | critical | Enforce shared AI guardrails across all surfaces: Without one shared guardrail layer, Ask, Scoop, Alchemy, and Explore Similar can diverge on spoilers, domain boundaries, honesty, and actionability.
- PRD-020 | critical | Map Interested/Excited chips to Later interest: This mapping is core to collection membership, home grouping, and saved-show semantics, so leaving it implicit risks storing the wrong relationship model.
- PRD-016 | critical | Make client cache safe to discard: The plan implies server persistence, but without an explicit safe-discard contract QA cannot verify that clearing storage or reinstalling the client is lossless.

### 5. Coverage Narrative

#### Overall Posture

This is a structurally sound plan with concerning fidelity gaps. It covers the major architecture, data model, primary screens, and benchmark mechanics well, but it is less reliable on the exact behavioral contracts that make this product feel correct rather than merely feature-complete.

#### Strength Clusters

The plan is strongest in Benchmark Runtime & Isolation, Collection Data & Persistence at the schema and business-rule level, App Navigation & Discover Shell, and the major feature decomposition for Collection Home, Ask, Alchemy, Person Detail, and Settings & Export. It also does a good job of turning the rider PRD into concrete infrastructure sections such as environment configuration, migrations, auth injection, and namespace-scoped test reset behavior.

#### Weakness Clusters

The gaps cluster in two places rather than being random. First, AI behavioral contracts are under-specified: Ask mention parsing, shared guardrails, domain redirection, summarization voice preservation, and quality-gate enforcement all lose precision relative to the supporting docs. Second, several high-fidelity UX semantics are only implied: overlaying My Data everywhere, hidden-vs-visible status semantics, Search's explicitly non-AI character, detail-page toolbar placement, fallback states, and concept-selection guidance.

#### Risk Assessment

If this plan were executed as-is, the first thing a QA reviewer would likely notice is that the app works at a broad feature level but misses product-defining interaction fidelity. Ask is the clearest risk: the team could ship a chat surface with recommendations and mentioned shows that still breaks the parser contract, mishandles malformed outputs, or drifts out of domain. Product review would also likely catch inconsistent user-overlay behavior across search, recommendations, and AI surfaces, making saved-state trust feel uneven.

#### Remediation Guidance

The remaining work is mostly tighter specification, not a new architecture. The plan needs explicit cross-cutting acceptance criteria for My Data overlay rules, AI I/O contracts, shared AI guardrails, and cache/source-of-truth behavior. It also needs a thin layer of UX state-machine detail for Detail, Search, Ask, Explore Similar, and Alchemy so that fallback behavior, control placement, and state-clearing rules are specified instead of implied.
