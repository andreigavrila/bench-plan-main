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
| PRD-001 | Use Next.js latest stable runtime | critical | full | `1.1 Technology Stack` ("Frontend: Next.js (latest stable)") |  |
| PRD-002 | Use Supabase official client libraries | critical | partial | `1.1 Technology Stack`; `Phase 1 > Project Setup` | The plan selects Supabase but never commits to the official Supabase client SDKs. |
| PRD-003 | Ship `.env.example` with required variables | critical | partial | `Phase 1 > Project Setup` ("Configure environment variables"); `5.3 AI Configuration` | `.env.example` and a complete variable contract are not explicitly planned. |
| PRD-004 | Ignore `.env*` secrets except example | important | missing | none | The plan never addresses `.gitignore` coverage for `.env*` secrets versus `.env.example`. |
| PRD-005 | Configure build through env without code edits | critical | partial | `Phase 1 > Project Setup`; `5.3 AI Configuration` | It assumes env-driven config, but it never states the build must be runnable without source edits. |
| PRD-006 | Keep secrets out of repo and server-only | critical | partial | `5.3 AI Configuration` (env keys) | Secrets are parameterized, but repo hygiene and server-only handling for elevated credentials are not specified. |
| PRD-007 | Provide app, test, reset command scripts | critical | missing | none | No explicit start, test, and namespace-reset scripts are planned. |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | `Phase 1 > Core Data Layer` ("Implement database schemas and migration scripts") |  |
| PRD-009 | Use one stable namespace per build | critical | partial | `Executive Summary`; `3.1 Authentication & Context Middleware` | Namespace isolation is planned, but the plan does not define one stable namespace per build lifetime. |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | partial | `Executive Summary`; `Phase 1 > Authentication & Context` | It plans namespace isolation, but not namespace-scoped destructive reset flows or reset safeguards. |
| PRD-011 | Attach every user record to `user_id` | critical | full | `2.1 Core Entities` (`shows`, `cloud_settings`, and `local_settings` include `user_id`) |  |
| PRD-012 | Partition persisted data by namespace and user | critical | full | `2.1 Core Entities`; `2.3 Row Level Security (RLS)` |  |
| PRD-013 | Support documented dev auth injection, prod-gated | important | partial | `1.1 Technology Stack` ("Development identity injection"); `3.1 Authentication & Context Middleware` | Dev identity injection is present, but the plan does not cover documentation or production gating. |
| PRD-014 | Real OAuth later needs no schema redesign | important | partial | `1.1 Technology Stack` ("migration path to OAuth") | The plan states intent, but it does not explain why the schema/API boundary avoids later redesign. |
| PRD-015 | Keep backend as persisted source of truth | critical | full | `Executive Summary`; `2.1 Core Entities`; `3.2 Core API Endpoints` |  |
| PRD-016 | Make client cache safe to discard | critical | missing | none | Client caching is proposed via IndexedDB, but there is no requirement that clearing client storage be harmless. |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | missing | none | Docker avoidance and hosted-agent compatibility are not addressed. |
| PRD-018 | Overlay saved user data on every show appearance | critical | partial | `2.1 Core Entities` (single `shows` record combines catalog and My Data); `Phase 2 > Search & Browse` | The schema supports overlays, but the plan never commits to showing saved My Data everywhere a show appears. |
| PRD-019 | Support visible statuses plus hidden `Next` | important | partial | `2.1 Core Entities` (`my_status` includes `next`) | The hidden-in-data but not primary-UI treatment of `Next` is not spelled out. |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | partial | `Phase 2 > Collection Management` ("Status, interest, tags, rating functionality") | Status and interest exist, but the Interested/Excited to Later-plus-interest mapping is not specified. |
| PRD-021 | Support free-form multi-tag personal tag library | important | partial | `2.1 Core Entities` (`my_tags TEXT[]`); `Phase 2 > Collection Management` | Multi-tag storage is planned, but the personal tag-library behavior and management flow are not described. |
| PRD-022 | Define collection membership by assigned status | critical | partial | `Phase 2 > Collection Management` | The plan centers collection operations around status, but it never defines collection membership as "status assigned". |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | partial | `Phase 2 > Collection Management` | The plan covers status/tag/rating controls, but it does not explicitly state that each of those actions triggers a save when unsaved. |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | missing | none | Default save behavior for unsaved items, including rating-save to Done, is absent. |
| PRD-025 | Removing status deletes show and all My Data | critical | partial | `Phase 2 > Collection Management` ("Save/remove functionality with confirmations") | Removal confirmation is planned, but clearing all My Data on status removal is not specified. |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | missing | none | Re-add semantics, My Data preservation, and public-data refresh behavior are not planned. |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | `2.1 Core Entities` (per-field `*_update_date` columns for status, interest, tags, score, and Scoop) |  |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | partial | `2.1 Core Entities`; `Phase 5 > Settings & Data Management` | Timestamps are stored, but their use for sorting, sync conflict resolution, and freshness is not laid out. |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | partial | `Phase 4 > AI Scoop` ("Caching with 4-hour freshness"); `2.1 Core Entities` (`ai_scoop`) | The 4-hour cache is planned, but persistence only for saved shows is not specified. |
| PRD-030 | Keep Ask and Alchemy state session-only | important | partial | `6.1 Ask (Chat) Implementation`; `6.2 Alchemy` | Ask and Alchemy services are session-oriented, but the plan never states that this state must remain non-persistent. |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | partial | `Phase 3 > Concept System` ("Real catalog mapping for recommendations") | Real-item mapping is planned, but the exact selectable-show resolution and fallback behavior are under-specified. |
| PRD-032 | Show collection and rating tile indicators | important | partial | `Phase 2 > Search & Browse` ("Results grid with collection indicators"); `Phase 2 > Collection Management` | Collection markers are planned, but explicit rating indicators across tiles are not. |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | partial | `Phase 5 > Settings & Data Management` ("cloud sync") | Sync is mentioned, but duplicate detection/merge behavior and per-field consistency rules are missing. |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | missing | none | The plan does not cover data-model upgrades or migration strategies that preserve user libraries. |
| PRD-035 | Persist synced settings, local settings, UI state | important | partial | `2.1 Core Entities` (`cloud_settings`, `local_settings`) | Synced and local settings are modeled, but persisted UI state is not. |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | partial | `2.1 Core Entities` (`provider_data JSONB`); `3.3 External Catalog Integration` | Provider IDs are stored, but transient-only detail fetch boundaries are not called out. |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | missing | none | No merge/overwrite policy is planned for catalog refreshes versus user-edited fields or timestamps. |
| PRD-038 | Provide filters panel and main screen destinations | important | full | `4.2 Component Hierarchy` (`NavigationPanel` plus `MainContent`) |  |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | partial | `4.1 Page Structure & Routing`; `4.2 Component Hierarchy` | Find/Discover routes exist, but the plan does not explicitly preserve them in persistent primary navigation. |
| PRD-040 | Keep Settings in persistent primary navigation | important | partial | `4.1 Page Structure & Routing`; `4.2 Component Hierarchy` | Settings routes exist, but the plan does not explicitly preserve them in persistent primary navigation. |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | `4.1 Page Structure & Routing` (`/find/search`, `/find/ask`, `/find/alchemy`) |  |
| PRD-042 | Show only library items matching active filters | important | full | `4.1 Page Structure & Routing` ("Home - Collection view (filtered)"); `Phase 2 > Collection home with filtering` |  |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | partial | `4.2 Component Hierarchy` (`StatusSections`) | Status grouping is planned, but the required Active/Excited/Interested/Others breakdown is not. |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | partial | `Phase 2 > Search & Browse` ("Basic filtering by genre, decade, media type") | The plan omits tag, all/no-tag, and community-score filters. |
| PRD-045 | Render poster, title, and My Data badges | important | partial | `4.2 Component Hierarchy` (`ShowGrid`); `Phase 2 > Collection Management` | It plans show tiles, but not the required poster/title/My Data badge content. |
| PRD-046 | Provide empty-library and empty-filter states | detail | partial | `Phase 5 > User Experience Polish` ("Empty states and onboarding") | Empty states are planned generically, but collection-home and filter-specific states are not defined. |
| PRD-047 | Search by title or keywords | important | partial | `3.3 External Catalog Integration` (`searchShows(query)`); `Phase 2 > Search page with TMDB integration` | Search exists, but title-versus-keyword behavior is not specified. |
| PRD-048 | Use poster grid with collection markers | important | full | `Phase 2 > Search & Browse` ("Results grid with collection indicators") |  |
| PRD-049 | Auto-open Search when setting is enabled | detail | partial | `2.1 Core Entities` (`auto_search BOOLEAN`); `Phase 5 > Settings page implementation` | The setting is modeled, but launch behavior that auto-opens Search is not planned. |
| PRD-050 | Keep Search non-AI in tone | important | missing | none | The plan never distinguishes Search as a non-AI catalog surface with no AI voice. |
| PRD-051 | Preserve Show Detail narrative section order | important | partial | `4.2 Component Hierarchy` (`ShowDetailPage` sections) | The plan lists Detail subcomponents, but not the PRD's required narrative ordering. |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | partial | `4.2 Component Hierarchy` (`MediaCarousel`) | Header media is present, but trailer prioritization and graceful fallback behavior are not specified. |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | partial | `ShowDetailPage`; `TMDBService.getShowDetails` | Core facts are implied, but the plan never requires them to appear early on the page. |
| PRD-054 | Place status/interest controls in toolbar | important | partial | `Phase 2 > Collection Management` ("Show detail page with My Data controls") | Controls are planned, but toolbar placement for status/interest is not. |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | missing | none | Tagging an unsaved show does not have the required auto-save-to-Later/Interested behavior in the plan. |
| PRD-056 | Auto-save unsaved rated show as Done | critical | missing | none | Rating an unsaved show does not have the required auto-save-to-Done behavior in the plan. |
| PRD-057 | Show overview early for fast scanning | important | partial | `4.2 Component Hierarchy` (`Overview & Scoop`) | Overview is included, but the plan does not commit to surfacing it early for scanability. |
| PRD-058 | Scoop shows correct states and progressive feedback | important | partial | `Phase 4 > AI Scoop` ("Progressive loading"; "4-hour freshness") | Loading and freshness are planned, but the exact Scoop state model and on-page copy states are not. |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | full | `Phase 3 > Ask Implementation` (`"Ask about this show" integration`); `5.2 Prompt Management System` (`withShow`) |  |
| PRD-060 | Include traditional recommendations strand | important | full | `3.2 Core API Endpoints` (`/api/recommendations/traditional/[id]`); `4.2 ShowDetailPage > Recommendations` |  |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | partial | `6.3 Explore Similar Implementation`; `Phase 4 > Explore Similar` | The recommendation flow exists, but the CTA-first UX and concept-picking guidance are not specified. |
| PRD-062 | Include streaming availability and person-linking credits | important | partial | `3.3 External Catalog Integration` (`getProviders`, `getCastCrew`); `4.2 ShowDetailPage > CastCrew` | Data sources are planned, but explicit streaming UI and cast/crew-to-person linking behavior are not. |
| PRD-063 | Gate seasons to TV and financials to movies | important | missing | none | The plan never gates seasons to TV or budget/revenue to movies. |
| PRD-064 | Keep primary actions early and page not overwhelming | important | missing | none | The plan does not address page pacing, early action clustering, or anti-overwhelm layout rules. |
| PRD-065 | Provide conversational Ask chat interface | important | full | `4.2 AskPage > ChatInterface`; `6.1 Ask (Chat) Implementation` |  |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | partial | `5.2 Prompt Management System` (`ask` base prompt); `9.2 Product Risks` (`AI quality consistency`) | Ask tone is planned broadly, but direct-answer, confident, spoiler-safe behavior is not operationalized. |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | `4.2 AskPage > MentionedShowsStrip`; `6.1` ("Parse mentioned shows for UI strip") |  |
| PRD-068 | Open Detail from mentions or Search fallback | important | partial | `6.1 Ask (Chat) Implementation` (`mentionedShows`) | Mention rendering is planned, but Detail-opening and Search fallback behavior are not. |
| PRD-069 | Show six random starter prompts with refresh | important | partial | `4.2 AskPage > StarterPrompts`; `Phase 3 > Ask Implementation` | Starter prompts are planned, but not the exact six-random-with-refresh behavior. |
| PRD-070 | Summarize older turns while preserving voice | important | partial | `6.1 Ask (Chat) Implementation` (`contextSummary`) | Turn summarization is implied, but preserving the same persona and voice is not specified. |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | full | `Phase 3 > Ask Implementation` (`"Ask about this show" integration`); `5.2 Prompt Management System` (`withShow`) |  |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | partial | `6.1 Ask (Chat) Implementation` (`response.commentary`, `parseMentionedShows(response.structuredOutput)`) | The plan anticipates structured mentions, but it does not commit to the exact `commentary` plus `showList` string contract. |
| PRD-073 | Retry malformed mention output once, then fallback | important | missing | none | No retry-once-then-fallback handling is planned for malformed structured mention output. |
| PRD-074 | Redirect Ask back into TV/movie domain | important | missing | none | Ask-domain guardrails that redirect users back to TV and movies are not specified. |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | full | `5.2 Prompt Management System` (`Extract 1-3 word concept ingredients`); `Phase 3 > Concept System` |  |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | partial | `5.2 Prompt Management System` (`1-3 word concept ingredients`) | The plan does not require bullet-only formatting or explicitly ban generic concepts. |
| PRD-077 | Order concepts by strongest aha and varied axes | important | missing | none | Concept ordering by strongest aha and varied axes is absent. |
| PRD-078 | Require concept selection and guide ingredient picking | important | partial | `Phase 3 > Concept selection UI`; `Phase 4 > Step-by-step wizard UI` | Selection is planned, but the ingredient-guidance copy and explicit requirement to select concepts are not. |
| PRD-079 | Return exactly five Explore Similar recommendations | important | full | `6.3 Explore Similar Implementation` (`limit: 5`) |  |
| PRD-080 | Support full Alchemy loop with chaining | important | full | `6.2 AlchemyService`; `Phase 4 > Alchemy Implementation` (`Results display and chaining`) |  |
| PRD-081 | Clear downstream results when inputs change | important | missing | none | The plan does not clear downstream concepts or results when the user changes inputs. |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | partial | `6.2 AlchemyService.generateConcepts(shows)` | Multi-show concepts are planned, but a larger option pool than single-show generation is not. |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | partial | `6.2/6.3 getRecommendations` | Recommendation generation exists, but no explicit rule ties each reason back to selected concepts. |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | partial | `10.3 Quality Metrics`; `9.2 Product Risks` | The plan cares about AI quality, but it does not define how recommendations stay surprising while still defensible and taste-aligned. |
| PRD-085 | Keep one consistent AI persona across surfaces | important | full | `5.1 AI Service Architecture` (`Personality management`); `5.2 Prompt Management System` |  |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | partial | `5.1 AI Service Architecture`; `5.2 Prompt Management System` | Prompt centralization exists, but shared cross-surface guardrails like spoiler safety and domain limits are not specified. |
| PRD-087 | Make AI warm, joyful, and light in critique | important | partial | `5.2 Prompt Management System` (`fun, chatty TV/movie nerd friend`) | A friendly persona is planned, but the warm, joyful, light-in-critique voice pillars are not concretely encoded. |
| PRD-088 | Structure Scoop as personal taste mini-review | important | full | `5.2 Prompt Management System > scoop` (`mini blog-post of taste review`, structure bullets) |  |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | partial | `6.1 Ask (Chat) Implementation`; `5.2 ask` | Ask is conversational, but brisk dialogue-length defaults are not specified. |
| PRD-090 | Feed AI the right surface-specific context inputs | important | full | `6.1` (library plus recent conversation); `5.2` (`withContext`, `withShow`); `6.2/6.3` (concepts and baseShow) |  |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | partial | `9.2 Product Risks` (`golden set validation`); `10.3 Quality Metrics` | Quality measurement is planned, but the PRD's rubric-based validation and hard-fail integrity gate are not. |
| PRD-092 | Show person gallery, name, and bio | important | partial | `4.2 Component Hierarchy` (`PersonDetailPage`) | A Person Detail page exists, but the required gallery, name, and bio content is not specified. |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | missing | none | Person analytics for ratings, genres, and projects-by-year are not planned. |
| PRD-094 | Group filmography by year | important | missing | none | Filmography grouping by year is not planned. |
| PRD-095 | Open Show Detail from selected credit | important | partial | `4.2 Component Hierarchy` (`PersonDetailPage`) | The page exists, but tapping a credit to open Show Detail is not specified. |
| PRD-096 | Include font size and Search-on-launch settings | important | full | `2.1 Core Entities > local_settings`; `Phase 5 > Settings page implementation` |  |
| PRD-097 | Support username, model, and API-key settings safely | important | partial | `2.1 Core Entities` (`username`, `catalog_api_key`, `ai_api_key`, `ai_model`); `Phase 5 > Settings page implementation` | The settings are modeled, but safe handling rules for user-entered secrets are not specified. |
| PRD-098 | Export saved shows and My Data as zip | critical | partial | `3.2 Core API Endpoints` (`GET /api/export`); `Phase 5 > Data export/import functionality` | Export is planned, but the required zip format containing saved shows and My Data is not specified. |
| PRD-099 | Encode export dates using ISO-8601 | important | missing | none | The export plan does not mention ISO-8601 date encoding. |

### 3. Coverage Scores

score = (full_count × 1.0 + partial_count × 0.5) / total_count × 100

Critical:  (6 × 1.0 + 16 × 0.5) / 30 × 100 = 46.7%  (14.0 of 30 critical requirements)
Important: (16 × 1.0 + 39 × 0.5) / 67 × 100 = 53.0%  (35.5 of 67 important requirements)
Detail:    (0 × 1.0 + 2 × 0.5) / 2 × 100 = 50.0%  (1.0 of 2 detail requirements)
Overall:   (22 × 1.0 + 57 × 0.5) / 99 × 100 = 51.0%  (99 total requirements)

### 4. Top Gaps

1. PRD-037 | `critical` | Merge catalog fields safely and maintain timestamps
Without an explicit merge/overwrite policy, catalog refreshes and sync flows can overwrite user edits, invalidate timestamp-based conflict resolution, and make the collection feel unreliable.

2. PRD-010 | `critical` | Isolate namespaces and scope destructive resets
The plan mentions namespace isolation but not scoped destructive resets, so benchmark runs can still collide or require unsafe global teardown when tests need a clean state.

3. PRD-055 | `critical` | Auto-save unsaved tagged show as Later/Interested
Tagging is one of the core implicit save triggers; if it does not auto-save correctly, tag-driven organization becomes inconsistent and users can silently lose intended collection entries.

4. PRD-056 | `critical` | Auto-save unsaved rated show as Done
Rating-to-save is a key journey in the PRD, and missing it breaks the app's watched-state semantics while making ratings behave inconsistently for unsaved titles.

5. PRD-072 | `critical` | Emit `commentary` plus exact `showList` contract
Ask can only render reliable mentioned-show strips if the AI output matches the exact contract, so under-specifying it creates immediate UX breakage on one of the flagship AI surfaces.

### 5. Coverage Narrative

#### Overall Posture

This is a structurally sound architecture-first plan with concerning behavioral gaps. It is usable as a high-level build roadmap, but it is not execution-ready against this PRD because many critical product contracts and benchmark-operability details remain implicit or absent.

#### Strength Clusters

The plan is strongest in Benchmark Runtime & Isolation at the stack-and-schema level, App Navigation & Discover Shell, and the broad decomposition of Ask, Explore Similar, and Alchemy into distinct services and pages. It also covers several settings foundations and the core persistence scaffolding well enough to show the intended system shape.

#### Weakness Clusters

The biggest gaps cluster in Collection Data & Persistence and Show Detail & Relationship UX, especially around implicit save/remove semantics, merge behavior, upgrade continuity, and exact My Data rules. A second cluster sits in benchmark-operability and AI behavioral contracts: env-file handling, reset workflows, structured Ask output, shared guardrails, and explicit fallback rules are all under-specified.

#### Risk Assessment

If this plan were executed as-is, the most likely outcome is a plausible app shell that demos well but fails under real benchmark and QA conditions. Reviewers would first notice inconsistent save behavior on tagged or rated unsaved shows, brittle Ask mentioned-show handling, and data-integrity regressions when refreshing catalog data or running destructive test flows.

#### Remediation Guidance

The plan needs a second pass focused on behavioral contracts, not more broad architecture. Add explicit acceptance criteria and implementation notes for save defaults, re-add/remove behavior, merge/timestamp policy, session-only AI state, Ask output contracts, and namespace-scoped reset operations. Separate plan sections are also needed for Person Detail behavior and export format details rather than leaving them to later polish.
