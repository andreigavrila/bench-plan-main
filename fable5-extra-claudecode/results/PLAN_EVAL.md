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
| PRD-001 | Use Next.js latest stable runtime | critical | full | `C1`; `4.1 Stack`; `Phase 0` |  |
| PRD-002 | Use Supabase official client libraries | critical | full | `C2`; `4.1 Stack`; `Supabase JS` |  |
| PRD-003 | Ship `.env.example` with required variables | critical | full | `6.3 Environment interface`; `.env.example` block |  |
| PRD-004 | Ignore `.env*` secrets except example | important | full | `6.3 Environment interface`; `.gitignore excludes .env* except .env.example` |  |
| PRD-005 | Configure build through env without code edits | critical | full | `6.3 Environment interface`; `No source edits needed to configure a run` |  |
| PRD-006 | Keep secrets out of repo and server-only | critical | full | `D1`; `6.3 Environment interface`; server-only key comments |  |
| PRD-007 | Provide app, test, reset command scripts | critical | full | `6.4 Scripts`; `npm run dev`, `npm test`, `npm run test:reset` |  |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | `5.4 Migrations & seed`; `supabase/migrations/` |  |
| PRD-009 | Use one stable namespace per build | critical | full | `6.1 Namespace`; `NAMESPACE_ID` stable lifetime |  |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | `6.1 Namespace`; `12.4 Destructive-test compliance` |  |
| PRD-011 | Attach every user record to `user_id` | critical | full | `C8`; `5.1 shows`; `5.2 cloud_settings` |  |
| PRD-012 | Partition persisted data by namespace and user | critical | full | `Primary key: (namespace_id, user_id, id)`; `scopedDb(namespaceId, userId)` |  |
| PRD-013 | Support documented dev auth injection, prod-gated | important | full | `6.2 User identity`; `X-User-Id` only when `AUTH_MODE=dev` |  |
| PRD-014 | Real OAuth later needs no schema redesign | important | full | `6.2 User identity`; `No schema change` |  |
| PRD-015 | Keep backend as persisted source of truth | critical | full | `Scope Understanding`; `all user-owned data... lives in Supabase` |  |
| PRD-016 | Make client cache safe to discard | critical | full | `4.2 Client caching policy`; `10.5 Session-state stores` |  |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | full | `C2`; `5.4 Migrations & seed`; `Docker is never required` |  |
| PRD-018 | Overlay saved user data on every show appearance | critical | full | `User overlay wins everywhere`; `10.3 The overlay rule` |  |
| PRD-019 | Support visible statuses plus hidden `Next` | important | full | `11.1 Collection Home`; hidden `next` grouped under Others |  |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | full | `7.1 Upsert semantics`; `11.5 Relationship toolbar` |  |
| PRD-021 | Support free-form multi-tag personal tag library | important | full | `11.5 Tags`; `/api/tags` distinct tag list |  |
| PRD-022 | Define collection membership by assigned status | critical | full | `5.1 shows`; `In collection` invariant |  |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | full | `7.1 Upsert semantics`; `Any intent on an unsaved show creates the row` |  |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | `7.1 Upsert semantics`; defaults and rating exception |  |
| PRD-025 | Removing status deletes show and all My Data | critical | full | `/api/library/:id DELETE`; `11.5 Relationship toolbar` |  |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | full | `D2`; `8.2 Merge engine`; `On load... user data survives` |  |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | `5.1 shows` timestamp columns; `Each changed my* field stamps` |  |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | full | `5.1 shows`; `11.1 sort`; `8.2 Merge engine` |  |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | full | `/api/library/:id/scoop`; `11.5 Scoop` |  |
| PRD-030 | Keep Ask and Alchemy state session-only | important | full | `10.5 Session-state stores`; `7.3 AI persistence policy` |  |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | full | `9.5 Show-resolution pipeline`; `/api/catalog/resolve` |  |
| PRD-032 | Show collection and rating tile indicators | important | full | `10.3 The overlay rule`; `11.1 Collection Home`; `11.2 Search` |  |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | partial | `8.2 Merge engine`; `5.2 cloud_settings`; `future sync/duplicate-merge` | Library sync and duplicate merge are only described as future reuse of the merge engine, not as a concrete implemented sync flow. |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | full | `5.5 Data continuity across versions`; `Phase 6` |  |
| PRD-035 | Persist synced settings, local settings, UI state | important | full | `5.2 cloud_settings`; `5.6 Local storage`; `11.7 Settings` |  |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | full | `5.1 shows` notes; `8.1 CatalogProvider` |  |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | full | `8.2 Merge engine`; `12.1 Unit` |  |
| PRD-038 | Provide filters panel and main screen destinations | important | full | `10.2 Global layout & navigation`; `10.1 Directory skeleton` |  |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | full | `10.2 Global layout & navigation`; persistent Find entry |  |
| PRD-040 | Keep Settings in persistent primary navigation | important | full | `10.2 Global layout & navigation`; persistent Settings entry |  |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | `10.2 Global layout & navigation`; `/find?mode=search/ask/alchemy` |  |
| PRD-042 | Show only library items matching active filters | important | full | `10.4 Filter model`; `11.1 Collection Home` |  |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | `11.1 Collection Home`; fixed group order |  |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | full | `10.4 Filter model`; `FilterSidebar` skeleton |  |
| PRD-045 | Render poster, title, and My Data badges | important | full | `11.1 Collection Home`; `Tiles: poster, title, badges` |  |
| PRD-046 | Provide empty-library and empty-filter states | detail | full | `11.1 Collection Home`; empty states bullet |  |
| PRD-047 | Search by title or keywords | important | full | `/api/catalog/search`; `11.2 Search` |  |
| PRD-048 | Use poster grid with collection markers | important | full | `11.2 Search`; `poster grid with overlay badges` |  |
| PRD-049 | Auto-open Search when setting is enabled | detail | full | `10.2 Global layout`; `11.2 Search` |  |
| PRD-050 | Keep Search non-AI in tone | important | full | `User overlay wins... Search has no AI voice`; `11.2 Search` |  |
| PRD-051 | Preserve Show Detail narrative section order | important | full | `11.5 Show Detail`; section order preserved exactly |  |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | full | `11.5 Show Detail`; trailers and fallback |  |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | full | `11.5 Show Detail`; core facts + community score early |  |
| PRD-054 | Place status/interest controls in toolbar | important | full | `11.5 Relationship toolbar`; not in scroll body |  |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | `11.5 Tags`; `7.1 Upsert semantics` |  |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | `11.5 Rating bar`; `7.1 Upsert semantics` |  |
| PRD-057 | Show overview early for fast scanning | important | full | `11.5 Show Detail`; overview + Scoop early in order |  |
| PRD-058 | Scoop shows correct states and progressive feedback | important | full | `11.5 Scoop`; toggle copy and `Generating...` |  |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | full | `11.3 Ask`; Detail CTA with seed show |  |
| PRD-060 | Include traditional recommendations strand | important | full | `11.5 Show Detail`; recommendations strand |  |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | full | `11.5 Explore Similar`; Get Concepts to Explore Shows |  |
| PRD-062 | Include streaming availability and person-linking credits | important | full | `11.5 Show Detail`; Stream It, Cast, Crew; `11.6 Person Detail` |  |
| PRD-063 | Gate seasons to TV and financials to movies | important | full | `11.5 Show Detail`; TV vs movie section variance |  |
| PRD-064 | Keep primary actions early and page not overwhelming | important | partial | `11.5 Show Detail`; primary action sections placed early | The plan preserves ordering but does not specify layout density or clutter controls to ensure the page feels powerful without becoming overwhelming. |
| PRD-065 | Provide conversational Ask chat interface | important | full | `11.3 Ask`; Chat thread and composer skeleton |  |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | full | `9.2 Persona layer`; `9.4 Surface contracts` |  |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | `11.3 Ask`; Mentioned shows strip |  |
| PRD-068 | Open Detail from mentions or Search fallback | important | full | `11.3 Ask`; tap to Detail or Search handoff |  |
| PRD-069 | Show six random starter prompts with refresh | important | full | `11.3 Ask`; `9.4 Starter prompts` |  |
| PRD-070 | Summarize older turns while preserving voice | important | full | `9.4 Surface contracts`; `11.3 Ask` |  |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | full | `11.3 Ask`; seed show context |  |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | full | `D6`; `9.4 Surface contracts` |  |
| PRD-073 | Retry malformed mention output once, then fallback | important | full | `D6`; `9.4 Parsing & fallbacks` |  |
| PRD-074 | Redirect Ask back into TV/movie domain | important | full | `9.2 Persona layer`; shared hard rules |  |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | full | `11.4 Alchemy`; `pick the ingredients`; generic rejection |  |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | full | `9.4 Surface contracts`; concept validator |  |
| PRD-077 | Order concepts by strongest aha and varied axes | important | full | `9.4 Surface contracts`; varied axes and ordered by strength |  |
| PRD-078 | Require concept selection and guide ingredient picking | important | full | `11.4 Alchemy`; `11.5 Explore Similar` |  |
| PRD-079 | Return exactly five Explore Similar recommendations | important | full | `11.5 Explore Similar`; `9.4 Surface contracts` |  |
| PRD-080 | Support full Alchemy loop with chaining | important | full | `11.4 Alchemy`; More Alchemy chains results |  |
| PRD-081 | Clear downstream results when inputs change | important | full | `11.4 Alchemy`; backtracking invariant |  |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | full | `9.4 Surface contracts`; 12 multi-show concepts |  |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | full | `9.4 Surface contracts`; concept-citing reasons |  |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | partial | `9.6 Quality bar integration`; `9.4 Concept recs` | The plan validates discovery quality broadly but does not design an explicit surprise-without-betrayal generation strategy. |
| PRD-085 | Keep one consistent AI persona across surfaces | important | full | `9.2 Persona layer`; single source of truth |  |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | full | `9.2 Persona layer`; shared hard rules |  |
| PRD-087 | Make AI warm, joyful, and light in critique | important | full | `9.2 Persona layer`; joy-forward, opinionated honesty |  |
| PRD-088 | Structure Scoop as personal taste mini-review | important | full | `9.4 Surface contracts`; Scoop mini blog post structure |  |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | full | `9.4 Surface contracts`; friend-in-dialogue, direct answer |  |
| PRD-090 | Feed AI the right surface-specific context inputs | important | full | `9.3 Taste-profile builder`; `9.4 Surface contracts` |  |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | full | `9.6 Quality bar integration`; real-show integrity threshold |  |
| PRD-092 | Show person gallery, name, and bio | important | full | `11.6 Person Detail`; `10.1 Person skeleton` |  |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | full | `11.6 Person Detail`; analytics charts |  |
| PRD-094 | Group filmography by year | important | full | `11.6 Person Detail`; grouped by year |  |
| PRD-095 | Open Show Detail from selected credit | important | full | `11.6 Person Detail`; credit tap to Show Detail |  |
| PRD-096 | Include font size and Search-on-launch settings | important | full | `11.7 Settings`; `5.6 Local storage` |  |
| PRD-097 | Support username, model, and API-key settings safely | important | full | `11.7 Settings`; env-first keys server-side |  |
| PRD-098 | Export saved shows and My Data as zip | critical | full | `11.8 Export / Backup`; `/api/export` |  |
| PRD-099 | Encode export dates using ISO-8601 | important | full | `11.8 Export / Backup`; dates ISO-8601 |  |

### 3. Coverage Scores

Overall score:

```
score = (96 full × 1.0 + 3 partial × 0.5) / 99 total × 100 = 98.5%
```

Score by severity tier:

```
Critical:  (30 × 1.0 + 0 × 0.5) / 30 × 100 = 100.0%  (30.0 of 30 critical requirements)
Important: (64 × 1.0 + 3 × 0.5) / 67 × 100 = 97.8%  (65.5 of 67 important requirements)
Detail:    (2 × 1.0 + 0 × 0.5) / 2 × 100 = 100.0%  (2.0 of 2 detail requirements)
Overall:   98.5% (99 total requirements)
```

### 4. Top Gaps

1. PRD-033 (`important`) | Sync libraries/settings consistently and merge duplicates

   This matters because the plan's data model is strong, but cross-device integrity and transparent duplicate handling are only treated as future reuse of the merge engine; if sync is enabled, users could still see drift or duplicate library entries without a concrete reconciliation flow.

2. PRD-064 (`important`) | Keep primary actions early and page not overwhelming

   This matters because the Detail page has many required sections; preserving order alone does not guarantee the page remains scannable, and QA could find a technically complete page that feels crowded or hard to maintain.

3. PRD-084 (`important`) | Deliver surprising but defensible taste-aligned recommendations

   This matters because real-show resolution and concept citation can still produce obvious or flat recommendations; without a generation strategy for calibrated surprise, the AI discovery surface may feel competent but not distinctive.

### 5. Coverage Narrative

#### Overall Posture

This is a strong plan with minor gaps. It directly addresses every critical requirement and most important requirements with concrete architecture, routes, domain rules, UI sections, tests, and delivery phases. The remaining issues are not foundational omissions; they are places where the plan relies on broad quality goals or future-facing language instead of specifying the exact implementation behavior.

#### Strength Clusters

The plan is strongest in Benchmark Runtime & Isolation, Collection Data & Persistence, Ask Chat, AI Voice, Persona & Quality, and Settings & Export. It is unusually explicit about namespace/user scoping, Supabase server-only access, schema migrations, environment configuration, cache disposability, saving rules, timestamped merge behavior, the exact Ask `showList` contract, AI session persistence, and export format.

#### Weakness Clusters

The partial items cluster around qualitative or distributed behaviors rather than concrete features. Library sync and duplicate merging span persistence and future sync semantics; Detail page busyness spans layout craft; recommendation surprise spans AI generation quality. These are all requirements where simply naming the feature is not enough to prove the implemented experience will meet the PRD's intent.

#### Risk Assessment

If executed as-is, the most likely failure mode is not a broken app but a few under-specified edge behaviors. Stakeholders would first notice either that cross-device library reconciliation is not truly finished, that the Show Detail page carries every required section but feels dense, or that AI recommendations are accurate and resolved but too predictable to deliver the intended "alchemy" feeling.

#### Remediation Guidance

The plan needs targeted specification depth, not a rewrite. Add an explicit library/settings sync and duplicate-reconciliation design, add layout acceptance criteria for Detail density and action priority, and add AI recommendation guidance that operationalizes "surprising but defensible" as prompt strategy, ranking criteria, or quality-test scenarios.
