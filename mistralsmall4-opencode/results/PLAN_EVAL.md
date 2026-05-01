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
| PRD-001 | Use Next.js latest stable runtime | critical | partial | `3.1 Runtime & Frontend` (`Next.js 14+`) | The plan pins `Next.js 14+` instead of explicitly requiring the latest stable release. |
| PRD-002 | Use Supabase official client libraries | critical | partial | `3.4 Persistence Layer (Supabase)` | It chooses Supabase but never commits to using the official client libraries. |
| PRD-003 | Ship `.env.example` with required variables | critical | full | `9.1 Environment Variables (.env.example Required)` | |
| PRD-004 | Ignore `.env*` secrets except example | important | missing | none | The plan never calls for `.gitignore` coverage that excludes `.env*` secrets while preserving `.env.example`. |
| PRD-005 | Configure build through env without code edits | critical | full | `9.1 Environment Variables (.env.example Required)` | |
| PRD-006 | Keep secrets out of repo and server-only | critical | partial | `9.1 Environment Variables (.env.example Required)` | It lists env vars and a public anon key, but does not explicitly require that secrets never be committed and elevated keys remain server-only. |
| PRD-007 | Provide app, test, reset command scripts | critical | full | `9.2 Commands (Package.json)`; `9.3 Reset Mechanism (test:reset)` | |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | `9.4 Schema Evolution` | |
| PRD-009 | Use one stable namespace per build | critical | full | `5.1 Namespace (namespace_id)` | |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | `5.1 Namespace (namespace_id)`; `9.3 Reset Mechanism (test:reset)` | |
| PRD-011 | Attach every user record to `user_id` | critical | full | `5.2 User Identity (user_id)`; `18. Success Criteria` | |
| PRD-012 | Partition persisted data by namespace and user | critical | full | `3.4 Persistence Layer (Supabase)` ("All writes scoped to `(namespace_id, user_id)`") | |
| PRD-013 | Support documented dev auth injection, prod-gated | important | partial | `3.3 Auth & Identity (Benchmark Mode)` | It includes dev-only identity injection, but does not explicitly require documentation and production gating for that path. |
| PRD-014 | Real OAuth later needs no schema redesign | important | full | `3.3 Auth & Identity (Benchmark Mode)` ("drop-in replacement with real OAuth ... no schema changes required") | |
| PRD-015 | Keep backend as persisted source of truth | critical | full | `3.5 No-Runtime Guarantee` | |
| PRD-016 | Make client cache safe to discard | critical | full | `3.5 No-Runtime Guarantee` | |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | full | `3.4 Persistence Layer (Supabase)` ("No Docker Requirement"); `9.5 Cloud Compatibility` | |
| PRD-018 | Overlay saved user data on every show appearance | critical | partial | `4. Data Model (Core Entity: Show)`; `6.2 Search (Global Catalog)` | It defines stored overlay fields, but never makes the universal rule explicit that every show presentation must prefer the saved user-overlaid version. |
| PRD-019 | Support visible statuses plus hidden `Next` | important | missing | none | The plan omits hidden `Next` support and instead relegates it to future work. |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | full | `4.1 Default Save Rules` ("Choose Interested/Excited → Status = Later, Interest = value") | |
| PRD-021 | Support free-form multi-tag personal tag library | important | full | `4. Data Model (Core Entity: Show)` (`myTags`); `12. Filters & Sidebar Navigation` ("Tag Filters: One per tag") | |
| PRD-022 | Define collection membership by assigned status | critical | full | `4. Data Model (Core Entity: Show)` ("In Collection: A show is 'in collection' when any status is set") | |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | full | `4.1 Default Save Rules`; `10.1 Saving Triggers` | |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | `4.1 Default Save Rules`; `10.2 Defaults on First Save` | |
| PRD-025 | Removing status deletes show and all My Data | critical | full | `10.3 Removal from Collection` | |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | full | `10.4 Re-adding Same Show` | |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | `4. Data Model (Core Entity: Show)` ("Each field tracks `*UpdateDate`") | |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | partial | `4. Data Model (Core Entity: Show)`; `10.4 Re-adding Same Show`; `14. AI Scoop Freshness & Cache` | The plan uses timestamps for conflict resolution and freshness, but not for sorting behavior. |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | full | `6.6 The Scoop (AI Review)`; `14. AI Scoop Freshness & Cache` | |
| PRD-030 | Keep Ask and Alchemy state session-only | important | full | `14. AI Scoop Freshness & Cache` | |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | partial | `11.3 Output Contracts` ("real catalog IDs (or full title match)") | It never specifies the resolver flow that turns every AI recommendation into a real selectable show or the fallback when resolution fails. |
| PRD-032 | Show collection and rating tile indicators | important | partial | `6.1 Collection Home`; `6.2 Search (Global Catalog)` | It marks in-collection items and mentions My Data generally, but does not explicitly require both collection and rating indicators on tiles. |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | partial | `15. Backup & Recovery Strategy` | Conflict resolution is noted, but duplicate detection and transparent merging across synced libraries and settings are not planned. |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | partial | `9.4 Schema Evolution` | Version tracking is present, but the plan does not define a continuity strategy that guarantees existing saved libraries survive upgrades unchanged. |
| PRD-035 | Persist synced settings, local settings, UI state | important | partial | `13.3 Configurable Settings`; `15. Backup & Recovery Strategy` | It lists some settings, but does not specify persistent local settings and UI state alongside synced settings. |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | partial | `7. Show Detail Page (Complete Layout)`; `4. Data Model (Core Entity: Show)` | Provider usage is mentioned, but the persistence rule of storing provider IDs while keeping detail fetches transient is not spelled out. |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | partial | `10.4 Re-adding Same Show`; `4. Data Model (Core Entity: Show)` | It covers timestamp-based conflict resolution, but not the non-empty overwrite safeguards and management timestamps in the merge policy. |
| PRD-038 | Provide filters panel and main screen destinations | important | full | `12. Filters & Sidebar Navigation`; `16. High-Level Component Tree (UI/UX)` | |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | full | `16. High-Level Component Tree (UI/UX)` | |
| PRD-040 | Keep Settings in persistent primary navigation | important | full | `16. High-Level Component Tree (UI/UX)` | |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | `6.2 Search (Global Catalog)`; `6.3 Ask (Conversational Discovery)`; `6.4 Alchemy (Multi-Show Concept Blending)` | |
| PRD-042 | Show only library items matching active filters | important | full | `6.1 Collection Home`; `12. Filters & Sidebar Navigation` | |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | `6.1 Collection Home` | |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | full | `12. Filters & Sidebar Navigation` | |
| PRD-045 | Render poster, title, and My Data badges | important | partial | `6.1 Collection Home` | The grouping logic is planned, but the tile-level poster/title/My Data badge contract is not explicitly defined for Home. |
| PRD-046 | Provide empty-library and empty-filter states | detail | full | `6.1 Collection Home` ("No shows? Try Search or Ask") | |
| PRD-047 | Search by title or keywords | important | full | `6.2 Search (Global Catalog)` | |
| PRD-048 | Use poster grid with collection markers | important | full | `6.2 Search (Global Catalog)` | |
| PRD-049 | Auto-open Search when setting is enabled | detail | full | `6.2 Search (Global Catalog)` ("Auto-open on launch (optional)") | |
| PRD-050 | Keep Search non-AI in tone | important | partial | `6.2 Search (Global Catalog)` | Search is separated from AI features, but the plan never explicitly preserves Search as a non-AI, straightforward catalog surface. |
| PRD-051 | Preserve Show Detail narrative section order | important | partial | `7. Show Detail Page (Complete Layout)` | The plan captures most sections, but it reorders several early elements and does not preserve the documented narrative sequence exactly. |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | partial | `7. Show Detail Page (Complete Layout)` ("trailer if available") | It prioritizes rich media, but does not define the graceful fallback behavior when trailers or backdrops are missing. |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | full | `7. Show Detail Page (Complete Layout)` | |
| PRD-054 | Place status/interest controls in toolbar | important | full | `7. Show Detail Page (Complete Layout)` ("status chips (toolbar)") | |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | `10.1 Saving Triggers`; `7. Show Detail Page (Complete Layout)` | |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | `10.1 Saving Triggers`; `7. Show Detail Page (Complete Layout)` | |
| PRD-057 | Show overview early for fast scanning | important | full | `7. Show Detail Page (Complete Layout)` | |
| PRD-058 | Scoop shows correct states and progressive feedback | important | partial | `6.6 The Scoop (AI Review)`; `7. Show Detail Page (Complete Layout)` | Progressive streaming is planned, but the detailed Scoop state model and user feedback transitions are not specified. |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | full | `7. Show Detail Page (Complete Layout)` ("Ask About This Show"); `6.3 Ask (Conversational Discovery)` | |
| PRD-060 | Include traditional recommendations strand | important | full | `7. Show Detail Page (Complete Layout)` ("Traditional Recs") | |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | full | `6.5 Explore Similar (Per-Show Concepts)`; `7. Show Detail Page (Complete Layout)` | |
| PRD-062 | Include streaming availability and person-linking credits | important | full | `7. Show Detail Page (Complete Layout)` ("Streaming"; "Cast/Crew | Person detail links") | |
| PRD-063 | Gate seasons to TV and financials to movies | important | full | `7. Show Detail Page (Complete Layout)` ("Seasons (TV)"; "Budget/Revenue (Movies)") | |
| PRD-064 | Keep primary actions early and page not overwhelming | important | partial | `7. Show Detail Page (Complete Layout)` | The section list is broad, but it does not articulate the busyness-management rules that keep primary actions early and the page readable. |
| PRD-065 | Provide conversational Ask chat interface | important | full | `6.3 Ask (Conversational Discovery)` | |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | partial | `6.3 Ask (Conversational Discovery)`; `8. Surface-Specific Modes` | It covers spoiler-safe conversational Ask, but not the explicit bar of answering directly with confident recommendations up front. |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | `6.3 Ask (Conversational Discovery)` ("Mentioned Shows row") | |
| PRD-068 | Open Detail from mentions or Search fallback | important | partial | `6.3 Ask (Conversational Discovery)`; `11.3 Output Contracts` | The plan defines mentions and structured IDs, but not the explicit Detail-open and Search-fallback behavior when a mention is selected. |
| PRD-069 | Show six random starter prompts with refresh | important | missing | none | The welcome-state starter prompts and refresh behavior are not planned. |
| PRD-070 | Summarize older turns while preserving voice | important | partial | `6.3 Ask (Conversational Discovery)`; `8. Surface-Specific Modes` | Summarization is present, but the plan does not preserve the requirement that summaries keep the same chat persona and voice. |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | full | `7. Show Detail Page (Complete Layout)`; `6.3 Ask (Conversational Discovery)` | |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | full | `6.3 Ask (Conversational Discovery)` (structured output block) | |
| PRD-073 | Retry malformed mention output once, then fallback | important | missing | none | The plan does not include the required one-time retry and fallback path for malformed mention output. |
| PRD-074 | Redirect Ask back into TV/movie domain | important | full | `11.3 Output Contracts` ("Domain: TV/movies only") | |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | full | `6.5 Explore Similar (Per-Show Concepts)` ("ingredient-like hooks") | |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | full | `6.5 Explore Similar (Per-Show Concepts)` ("8 concept bullets (1-3 words)") | |
| PRD-077 | Order concepts by strongest aha and varied axes | important | missing | none | The plan never requires concept ordering by strongest aha or deliberate variation across structure, vibe, and emotion axes. |
| PRD-078 | Require concept selection and guide ingredient picking | important | partial | `6.4 Alchemy (Multi-Show Concept Blending)`; `6.5 Explore Similar (Per-Show Concepts)` | It requires concept selection, but does not plan the UX guidance that teaches users to pick desired ingredients. |
| PRD-079 | Return exactly five Explore Similar recommendations | important | full | `6.5 Explore Similar (Per-Show Concepts)` ("Returns 5 AI recommendations") | |
| PRD-080 | Support full Alchemy loop with chaining | important | full | `6.4 Alchemy (Multi-Show Concept Blending)` | |
| PRD-081 | Clear downstream results when inputs change | important | missing | none | Backtracking is implied, but the plan never states that changing shows or concepts clears downstream results. |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | partial | `6.4 Alchemy (Multi-Show Concept Blending)` | Shared multi-show concept generation is planned, but not the larger option pool expected for Alchemy versus single-show concepts. |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | full | `6.4 Alchemy (Multi-Show Concept Blending)` ("reasons rooted in selected concepts"); `11.1 Core AI Responsibilities` | |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | partial | `2. Core Product Goals (Reiterated)`; `11.1 Core AI Responsibilities` | The plan targets taste-aware discovery, but does not codify the surprise-without-betrayal quality bar or acceptance criteria. |
| PRD-085 | Keep one consistent AI persona across surfaces | important | full | `6.3 Ask (Conversational Discovery)` ("Uses same persona as Scoop/Alchemy"); `8. Shared Persona` | |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | partial | `8. AI Voice & Personality (Compliance Contract)`; `11.3 Output Contracts` | It captures some shared rules, but not the full cross-surface guardrail set and enforcement or fallback behavior from the prompting guide. |
| PRD-087 | Make AI warm, joyful, and light in critique | important | full | `8. Shared Persona`; `8. Voice Pillars (Non-Negotiable)` | |
| PRD-088 | Structure Scoop as personal taste mini-review | important | full | `6.6 The Scoop (AI Review)`; `8. Surface-Specific Modes` | |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | full | `6.3 Ask (Conversational Discovery)`; `8. Surface-Specific Modes` | |
| PRD-090 | Feed AI the right surface-specific context inputs | important | full | `11.2 Inputs Sent to AI` | |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | missing | none | The plan does not include the discovery scoring rubric or the non-negotiable integrity check for real-show resolution. |
| PRD-092 | Show person gallery, name, and bio | important | partial | `16. High-Level Component Tree (UI/UX)` ("Person Detail"); `7. Show Detail Page (Complete Layout)` ("Person detail links") | The route exists, but the person page content contract of gallery, name, and bio is not actually planned. |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | missing | none | Ratings, genre, and projects-by-year analytics are absent from the plan. |
| PRD-094 | Group filmography by year | important | missing | none | The plan never specifies filmography grouped by year. |
| PRD-095 | Open Show Detail from selected credit | important | missing | none | It links from Show Detail to Person Detail, but not from a selected person credit back into Show Detail. |
| PRD-096 | Include font size and Search-on-launch settings | important | full | `13.3 Configurable Settings` | |
| PRD-097 | Support username, model, and API-key settings safely | important | partial | `13.3 Configurable Settings`; `9.1 Environment Variables (.env.example Required)` | The settings are listed, but the plan does not define safe handling boundaries for user-entered or synced API keys. |
| PRD-098 | Export saved shows and My Data as zip | critical | full | `13.1 Export / Backup` | |
| PRD-099 | Encode export dates using ISO-8601 | important | full | `13.1 Export / Backup` ("dates encoded ISO-8601") | |

### 3. Coverage Scores
Critical: `(22 × 1.0 + 8 × 0.5) / 30 × 100 = 86.7%` (26 of 30 critical requirements)
Important: `(37 × 1.0 + 20 × 0.5) / 67 × 100 = 70.1%` (47 of 67 important requirements)
Detail: `(2 × 1.0 + 0 × 0.5) / 2 × 100 = 100.0%` (2 of 2 detail requirements)
Overall: `(61 × 1.0 + 28 × 0.5) / 99 × 100 = 75.8%` (99 total requirements)

### 4. Top Gaps
1. PRD-031 | `critical` | Resolve AI recommendations to real selectable shows
Without a concrete resolver and fallback plan, Ask, Explore Similar, and Alchemy can produce recommendations users cannot open or save, which breaks the app's core "discovery must be actionable" promise.

2. PRD-037 | `critical` | Merge catalog fields safely and maintain timestamps
If merge semantics stay underspecified, catalog refreshes or sync can overwrite non-empty stored data, scramble freshness logic, or lose user edits.

3. PRD-034 | `critical` | Preserve saved libraries across data-model upgrades
Schema versioning alone does not protect existing libraries; upgrades could silently drop statuses, tags, ratings, or Scoop data.

4. PRD-086 | `critical` | Enforce shared AI guardrails across all surfaces
Without a complete shared guardrail contract, Ask, Scoop, and concept flows can drift in tone, spoil content, leave the domain, or fail the product's behavioral consistency bar.

5. PRD-018 | `critical` | Overlay saved user data on every show appearance
If the saved overlay rule is not universal, the same show can appear with conflicting status, rating, or tag state across Home, Search, and AI recommendations, eroding trust quickly.

### 5. Coverage Narrative
#### Overall Posture
This is a structurally sound plan with concerning holes. It covers the benchmark scaffold, the core collection model, and the main feature map well enough to start implementation, but it does not carry enough supporting-doc detail to guarantee faithful behavior in AI discovery, cross-surface data integrity, or Person Detail UX. No critical requirement is entirely absent, but several critical requirements are only partially specified.

#### Strength Clusters
The strongest coverage is in Benchmark Runtime & Isolation, Collection Home & Search, and the core save/remove/default behaviors inside Collection Data & Persistence. The plan is also solid at a high level on Show Detail structure and AI persona framing: it names the main surfaces, the main flows, and the benchmark isolation model concretely enough to support implementation sequencing.

#### Weakness Clusters
The gaps cluster around supporting-doc-derived behavioral contracts rather than top-level feature enumeration. Ask Chat, Concepts/Explore Similar/Alchemy, AI Voice/Persona/Quality, and Person Detail all miss the more exacting rules about fallback behavior, quality bars, concept ordering, UX guidance, and analytics/detail content. A second cluster sits in Collection Data & Persistence, where timestamps are mentioned but overlay, merge, sync, migration continuity, provider persistence, and UI-state persistence stay only partially planned.

#### Risk Assessment
If this plan were executed as-is, the most likely result is an app that has the right screens and broad data model but feels less reliable and less polished than the PRD intends. QA would probably notice first that AI-driven discovery is not fully actionable or robust, Person Detail is underbuilt, and edge cases around refresh, sync, and upgrades are missing the explicit merge and continuity rules needed to protect user data.

#### Remediation Guidance
The remaining work is mostly tighter specification, not wholesale replanning. The plan needs explicit acceptance criteria for AI outputs, retries, fallbacks, and discovery quality scoring; a dedicated data lifecycle section covering overlay, merge, sync, and migration guarantees; and fuller feature sections for Person Detail and the exact Search, Ask, and Show Detail states drawn from the supporting docs. Broad feature summaries are already present, but the missing behavioral contracts need to be made executable.
