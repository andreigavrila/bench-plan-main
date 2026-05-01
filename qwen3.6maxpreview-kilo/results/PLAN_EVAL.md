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
| PRD-001 | Use Next.js latest stable runtime | critical | full | `1.1 Technology Stack` | |
| PRD-002 | Use Supabase official client libraries | critical | full | `1.1 Technology Stack`; `1.2 Fractal Feature Architecture > lib/supabase/` | |
| PRD-003 | Ship `.env.example` with required variables | critical | full | `9.1 Required Environment Variables` | |
| PRD-004 | Ignore `.env*` secrets except example | important | partial | `9.3 Git Ignore` | The proposed `.gitignore` covers common env files but does not commit to ignoring all `.env*` secrets except `.env.example`. |
| PRD-005 | Configure build through env without code edits | critical | full | `9.1 Required Environment Variables`; `12 Success Criteria` | |
| PRD-006 | Keep secrets out of repo and server-only | critical | full | `1.1 AI Integration`; `9.1 Required Environment Variables` (`SUPABASE_SERVICE_ROLE_KEY  # Server-only`) | |
| PRD-007 | Provide app, test, reset command scripts | critical | full | `9.2 Scripts` | |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | `2.2 Migrations` | |
| PRD-009 | Use one stable namespace per build | critical | full | `3.1 Namespace Management`; `12 Success Criteria` | |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | `3.1 Namespace Management`; `8.4 Destructive Testing` | |
| PRD-011 | Attach every user record to `user_id` | critical | full | `2.1 Tables > shows`; `2.1 Tables > cloud_settings`; `3.2 User Identity (Benchmark Mode)` | |
| PRD-012 | Partition persisted data by namespace and user | critical | full | `1.3 Data Flow Principles`; `2.1 Tables > RLS Policies` | |
| PRD-013 | Support documented dev auth injection, prod-gated | important | full | `3.2 User Identity (Benchmark Mode)`; `10 Phase 1` (`Auth/identity injection middleware`) | |
| PRD-014 | Real OAuth later needs no schema redesign | important | full | `3.2 User Identity (Benchmark Mode) > Production Migration Path` | |
| PRD-015 | Keep backend as persisted source of truth | critical | full | `1.3 Data Flow Principles` | |
| PRD-016 | Make client cache safe to discard | critical | full | `1.3 Data Flow Principles`; `2.1 Tables > local_settings`; `2.1 Tables > ui_state` | |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | partial | `1.1 Technology Stack`; `9.2 Scripts` | The plan uses Supabase and hosted workflows but never states Docker is optional or excluded from the required path. |
| PRD-018 | Overlay saved user data on every show appearance | critical | partial | `4.1 Collection Home > Show Tiles`; `4.3 Search > Catalog Integration`; `4.4 Ask > Mentioned Shows` | The plan covers badges and some merged views, but it does not explicitly require the full saved-show overlay everywhere recommendations and AI surfaces render shows. |
| PRD-019 | Support visible statuses plus hidden `Next` | important | full | `13 Open Questions & Future Extensions`; `Appendix A Key Type Definitions` | |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | full | `4.2 Show Detail Page > My Relationship Controls`; `4.2 Show Detail Page > Auto-Save Logic` | |
| PRD-021 | Support free-form multi-tag personal tag library | important | full | `4.2 Show Detail Page > Tag Picker`; `4.1 Collection Home > Filter Sidebar` | |
| PRD-022 | Define collection membership by assigned status | critical | partial | `4.2 Show Detail Page > Auto-Save Logic`; `5.3 Context Assembly` (`shows.filter(s => s.myStatus)`) | The plan implies saved membership through `myStatus` but never makes that rule the canonical collection-membership definition across the system. |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | full | `4.2 Show Detail Page > My Relationship Controls`; `4.2 Show Detail Page > Auto-Save Logic` | |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | `4.2 Show Detail Page > Auto-Save Logic` | |
| PRD-025 | Removing status deletes show and all My Data | critical | full | `4.2 Show Detail Page > Removal Confirmation` | |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | missing | none | The removal flow hard-deletes the show with `deleteShow(showId)` and the plan never adds a mechanism to preserve prior My Data for later re-adds. |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | `2.1 Tables > shows` | |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | full | `4.1 Collection Home > Data Fetching`; `6.3 Merge Strategy`; `4.2 Show Detail Page > Overview + Scoop` | |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | full | `4.2 Show Detail Page > Overview + Scoop` | |
| PRD-030 | Keep Ask and Alchemy state session-only | important | partial | `4.4 Ask > Conversation Context`; `4.5 Alchemy > State Machine` | Ask and Alchemy are kept in component state, but the plan does not explicitly require clearing those states when the user leaves or resets the surface. |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | full | `4.4 Ask > Mentioned Shows`; `5.4 Error Handling & Fallbacks`; `5.2 Prompt Templates > Concept-Based Recommendations` | |
| PRD-032 | Show collection and rating tile indicators | important | full | `4.1 Collection Home > Show Tiles` | |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | partial | `2.1 Tables > cloud_settings`; `6.3 Merge Strategy` | The plan covers timestamp merges and synced settings, but it does not specify duplicate detection and transparent library merging. |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | partial | `2.1 Tables > app_metadata`; `2.2 Migrations`; `7.3 Import/Restore (Future)` | It introduces versioning and migrations, but it does not define how existing saved libraries are migrated forward safely across model-version changes. |
| PRD-035 | Persist synced settings, local settings, UI state | important | full | `2.1 Tables > cloud_settings`; `2.1 Tables > local_settings`; `2.1 Tables > ui_state` | |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | full | `2.1 Tables > shows.provider_data`; `4.6 Person Detail > Data Fetching`; `6.4 Provider Data (Streaming Availability)` | |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | full | `6.3 Merge Strategy` | |
| PRD-038 | Provide filters panel and main screen destinations | important | partial | `1.2 Fractal Feature Architecture`; `10 Phase 1` (`Basic app shell with routing`) | The plan defines pages and routing, but it does not explicitly specify the top-level shell with the filters panel plus main destinations. |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | partial | `1.2 Fractal Feature Architecture > pages/Find`; `10 Phase 1` (`Basic app shell with routing`) | Find exists as a route, but the plan never explicitly commits to keeping it in persistent primary navigation. |
| PRD-040 | Keep Settings in persistent primary navigation | important | partial | `1.2 Fractal Feature Architecture > pages/Settings`; `10 Phase 1` (`Basic app shell with routing`) | Settings exists as a route, but the plan never explicitly commits to keeping it in persistent primary navigation. |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | `1.2 Fractal Feature Architecture > Find/ModeSwitcher`; `4.3 Search`; `4.4 Ask`; `4.5 Alchemy` | |
| PRD-042 | Show only library items matching active filters | important | full | `4.1 Collection Home > Data Fetching` | |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | `4.1 Collection Home > Status Sections` | |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | full | `4.1 Collection Home > Filter Sidebar` | |
| PRD-045 | Render poster, title, and My Data badges | important | full | `4.1 Collection Home > Show Tiles` | |
| PRD-046 | Provide empty-library and empty-filter states | detail | full | `4.1 Collection Home > Empty States` | |
| PRD-047 | Search by title or keywords | important | full | `4.3 Search > Search Input` | |
| PRD-048 | Use poster grid with collection markers | important | full | `4.3 Search > Results Grid`; `4.3 Search > Catalog Integration` | |
| PRD-049 | Auto-open Search when setting is enabled | detail | full | `4.3 Search > Auto-Open on Launch` | |
| PRD-050 | Keep Search non-AI in tone | important | partial | `4.3 Search` | The plan implements Search as catalog lookup, but it does not explicitly preserve the requirement that Search copy and tone remain non-AI. |
| PRD-051 | Preserve Show Detail narrative section order | important | partial | `4.2 Show Detail Page > Implementation Details` | The plan covers the required sections but rearranges the detail-page hierarchy instead of preserving the specified order from the detail experience spec. |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | full | `4.2 Show Detail Page > Header Media Carousel` | |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | full | `4.2 Show Detail Page > Core Facts` | |
| PRD-054 | Place status/interest controls in toolbar | important | full | `4.2 Show Detail Page > My Relationship Controls (Toolbar)` | |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | `4.2 Show Detail Page > My Relationship Controls`; `4.2 Show Detail Page > Auto-Save Logic` | |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | `4.2 Show Detail Page > My Relationship Controls`; `4.2 Show Detail Page > Auto-Save Logic` | |
| PRD-057 | Show overview early for fast scanning | important | full | `4.2 Show Detail Page > Overview + Scoop` | |
| PRD-058 | Scoop shows correct states and progressive feedback | important | full | `4.2 Show Detail Page > Overview + Scoop` | |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | full | `4.2 Show Detail Page > Ask About This Show`; `4.4 Ask > Ask About a Show` | |
| PRD-060 | Include traditional recommendations strand | important | full | `4.2 Show Detail Page > Traditional Recommendations` | |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | full | `4.2 Show Detail Page > Explore Similar (Concept Discovery)` | |
| PRD-062 | Include streaming availability and person-linking credits | important | full | `4.2 Show Detail Page > Streaming Availability`; `4.2 Show Detail Page > Cast & Crew` | |
| PRD-063 | Gate seasons to TV and financials to movies | important | full | `4.2 Show Detail Page > Seasons (TV Only)`; `4.2 Show Detail Page > Budget vs Revenue (Movies)` | |
| PRD-064 | Keep primary actions early and page not overwhelming | important | partial | `4.2 Show Detail Page > Implementation Details` | Primary actions are early in the section list, but the plan does not add concrete anti-overwhelm layout guidance comparable to the source spec. |
| PRD-065 | Provide conversational Ask chat interface | important | full | `4.4 Ask > Chat Interface` | |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | full | `4.4 Ask > Tone & Personality`; `5.2 Prompt Templates > Ask Prompt (System)` | |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | `4.4 Ask > Mentioned Shows` | |
| PRD-068 | Open Detail from mentions or Search fallback | important | full | `4.4 Ask > Mentioned Shows`; `5.4 Error Handling & Fallbacks` | |
| PRD-069 | Show six random starter prompts with refresh | important | full | `4.4 Ask > Welcome View` | |
| PRD-070 | Summarize older turns while preserving voice | important | full | `4.4 Ask > Conversation Summarization` | |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | full | `4.4 Ask > Ask About a Show`; `5.3 Context Assembly > Show Context` | |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | partial | `4.4 Ask > Structured Output Parsing`; `5.2 Prompt Templates > Ask with Mentions Prompt Extension` | The plan defines a custom `||SHOWS||` delimiter and array parser, not the exact `commentary` plus string `showList` contract required by the PRD. |
| PRD-073 | Retry malformed mention output once, then fallback | important | full | `5.4 Error Handling & Fallbacks` | |
| PRD-074 | Redirect Ask back into TV/movie domain | important | full | `5.2 Prompt Templates > Ask Prompt (System)` | |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | full | `5.2 Prompt Templates > Concept Extraction Prompt (Single Show)` | |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | full | `5.2 Prompt Templates > Concept Extraction Prompt (Single Show)` | |
| PRD-077 | Order concepts by strongest aha and varied axes | important | full | `5.2 Prompt Templates > Concept Extraction Prompt (Single Show)`; `5.2 Prompt Templates > Concept Extraction Prompt (Multi-Show / Alchemy)` | |
| PRD-078 | Require concept selection and guide ingredient picking | important | partial | `4.2 Show Detail Page > Explore Similar`; `4.5 Alchemy > Step 3: Select Concepts` | The flow requires concept selection, but it omits the UX guidance and copy that explains concepts as ingredients the user should choose. |
| PRD-079 | Return exactly five Explore Similar recommendations | important | full | `5.2 Prompt Templates > Concept-Based Recommendations Prompt (Explore Similar)` | |
| PRD-080 | Support full Alchemy loop with chaining | important | full | `4.5 Alchemy > Step 5: Chain Another Round` | |
| PRD-081 | Clear downstream results when inputs change | important | full | `4.5 Alchemy > Backtracking` | |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | full | `4.5 Alchemy > Step 2: Conceptualize`; `5.2 Prompt Templates > Concept Extraction Prompt (Multi-Show / Alchemy)` | |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | full | `4.5 Alchemy > Step 4: Alchemize`; `5.2 Prompt Templates > Concept-Based Recommendations` | |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | full | `5.2 Prompt Templates > Concept-Based Recommendations Prompt (Alchemy)`; `8.5 AI Quality Tests` | |
| PRD-085 | Keep one consistent AI persona across surfaces | important | full | `5.2 Prompt Templates`; `Appendix B AI Prompt Evolution Guidelines` | |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | full | `5.2 Prompt Templates`; `Appendix B AI Prompt Evolution Guidelines` | |
| PRD-087 | Make AI warm, joyful, and light in critique | important | full | `5.2 Prompt Templates`; `Appendix B AI Prompt Evolution Guidelines` | |
| PRD-088 | Structure Scoop as personal taste mini-review | important | full | `5.2 Prompt Templates > Scoop Prompt` | |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | full | `4.4 Ask > Tone & Personality`; `5.2 Prompt Templates > Ask Prompt (System)` | |
| PRD-090 | Feed AI the right surface-specific context inputs | important | full | `5.3 Context Assembly`; `4.4 Ask > Ask About a Show` | |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | full | `8.5 AI Quality Tests` | |
| PRD-092 | Show person gallery, name, and bio | important | full | `4.6 Person Detail > Person Header`; `4.6 Person Detail > Image Gallery` | |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | full | `4.6 Person Detail > Analytics Charts` | |
| PRD-094 | Group filmography by year | important | full | `4.6 Person Detail > Filmography` | |
| PRD-095 | Open Show Detail from selected credit | important | full | `4.6 Person Detail > Filmography` | |
| PRD-096 | Include font size and Search-on-launch settings | important | full | `4.7 Settings > App Settings` | |
| PRD-097 | Support username, model, and API-key settings safely | important | partial | `4.7 Settings > User Settings`; `4.7 Settings > AI Settings`; `9.1 Required Environment Variables` | The plan includes the settings fields, but it does not spell out a safe handling strategy for user-entered API keys beyond storage and sync. |
| PRD-098 | Export saved shows and My Data as zip | critical | full | `4.7 Settings > Data Export`; `7.1 Export Flow` | |
| PRD-099 | Encode export dates using ISO-8601 | important | full | `4.7 Settings > Export Implementation`; `7.1 Export Flow` | |

### 3. Coverage Scores

score = (full_count × 1.0 + partial_count × 0.5) / total_count × 100

Critical:  (25 × 1.0 + 4 × 0.5) / 30 × 100 = 90.0%  (27 of 30 critical requirements)
Important: (55 × 1.0 + 12 × 0.5) / 67 × 100 = 91.0%  (61 of 67 important requirements)
Detail:    (2 × 1.0 + 0 × 0.5) / 2 × 100 = 100.0%  (2 of 2 detail requirements)
Overall:   (82 × 1.0 + 16 × 0.5) / 99 × 100 = 90.9%  (99 total requirements)

### 4. Top Gaps

1. PRD-026 | `critical` | Re-add preserves My Data and refreshes public data
The plan’s removal flow hard-deletes shows and never introduces a retention/tombstone strategy, so users would lose tags, ratings, status history, and Scoop when they save the same title again later.

2. PRD-072 | `critical` | Emit `commentary` plus exact `showList` contract
The Ask plan uses a different delimiter-based format than the canonical contract, which creates a high risk that mentioned-show parsing breaks even if the chat UX looks correct.

3. PRD-018 | `critical` | Overlay saved user data on every show appearance
The plan clearly covers badges in some surfaces, but it never turns “user-overlaid show everywhere” into a cross-cutting implementation rule, so recommendations and AI result surfaces may drift from the saved-library truth.

4. PRD-034 | `critical` | Preserve saved libraries across data-model upgrades
The plan adds version metadata and migrations but not an actual forward-migration strategy, so schema evolution could silently strand or reshape saved user data on upgrade.

5. PRD-022 | `critical` | Define collection membership by assigned status
Without a single canonical membership rule, save/remove/filter logic can diverge across features, producing inconsistent counts, exports, and library visibility.

### 5. Coverage Narrative

#### Overall Posture

This is a structurally strong plan with a small number of material behavioral gaps. It covers most of the benchmark baseline, the core data model, the major feature surfaces, and the AI system in concrete terms, but a few critical contracts around data lifecycle and exact AI I/O semantics remain under-specified.

#### Strength Clusters

The plan is strongest in Benchmark Runtime & Isolation, Collection Home & Search, Person Detail, and most of Show Detail & Relationship UX. It also does a good job on the main AI surface scaffolding: prompt families, context assembly, fallback handling, and quality validation are all described concretely enough to guide implementation.

#### Weakness Clusters

The gaps cluster in two patterns rather than being random. One cluster is cross-cutting behavioral semantics in Collection Data & Persistence, especially re-add continuity, canonical collection membership, duplicate handling, and upgrade continuity. The second cluster is exact product-contract fidelity in App Navigation & Discover Shell and Ask Chat, where the plan often implies the right outcome but does not lock down the precise shell/navigation behavior or the exact `commentary`/`showList` wire format.

#### Risk Assessment

If this plan were executed as-is, the app would likely look complete and pass many happy-path demos, but QA would find silent spec mismatches in persistence and AI integration. The first visible failures would likely be that removing and re-saving a show loses prior My Data, and that Ask mention parsing does not match the required contract even though the chat itself appears functional.

#### Remediation Guidance

The remaining work is mostly specification tightening, not a wholesale re-plan. The plan needs explicit lifecycle rules for delete/re-add/version-upgrade behavior, a canonical collection-membership rule, an exact Ask output contract that matches the PRD verbatim, and a clearer top-level shell/navigation section. A smaller follow-up pass should also pin down non-AI Search tone, concept-selection guidance copy, and safe handling expectations for user-entered API keys.
