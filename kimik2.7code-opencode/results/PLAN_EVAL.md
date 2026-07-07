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
| PRD-001 | Use Next.js latest stable runtime | critical | full | `2.1 Tech Stack`: "Next.js (App Router)"; Phase 1 initializes Next.js |  |
| PRD-002 | Use Supabase official client libraries | critical | full | `2.1 Tech Stack`: "Supabase (Postgres)"; Phase 1 adds Supabase client |  |
| PRD-003 | Ship `.env.example` with required variables | critical | full | `8. Phase 1`: "Create `.env.example`"; checklist repeats it |  |
| PRD-004 | Ignore `.env*` secrets except example | important | partial | `8. Phase 1`: "`.gitignore`"; checklist says "`.gitignore` for secrets" | It does not explicitly require ignoring `.env*` while preserving `.env.example`. |
| PRD-005 | Configure build through env without code edits | critical | full | `2.1 Tech Stack`: keys from env; `5.2 Identity Injection`: env fallback |  |
| PRD-006 | Keep secrets out of repo and server-only | critical | full | `2.3 Key Architectural Decisions`: "AI calls are server-only"; `4.5`: "Never commit keys" |  |
| PRD-007 | Provide app, test, reset command scripts | critical | full | `12. Deliverables Checklist`: "`npm run dev`, `npm test`, `npm run test:reset` scripts" |  |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | `2.2 Fractal Directory Structure`: `supabase/migrations`; Phase 1 migrations |  |
| PRD-009 | Use one stable namespace per build | critical | full | `1. Executive Summary`: isolated runs via `namespace_id`; `5.2 Identity Injection` |  |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | `5.1`: `resetNamespaceData()`; `9.2`: namespace isolation E2E |  |
| PRD-011 | Attach every user record to `user_id` | critical | full | `2.3`: "Every persisted record includes `(namespace_id, user_id)`" |  |
| PRD-012 | Partition persisted data by namespace and user | critical | full | `3.1 Supabase Tables`: `namespace_id` and `user_id`; RLS note |  |
| PRD-013 | Support documented dev auth injection, prod-gated | important | full | `5.2 Identity Injection`: headers/env and production gate |  |
| PRD-014 | Real OAuth later needs no schema redesign | important | full | `2.1 Tech Stack`: "swappable for real OAuth later without schema changes" |  |
| PRD-015 | Keep backend as persisted source of truth | critical | full | `2.3`: "Server is source of truth"; server actions write to Supabase |  |
| PRD-016 | Make client cache safe to discard | critical | full | `2.1 Tech Stack`: "client cache is disposable"; `2.3` repeats it |  |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | partial | Plan uses Supabase clients and env-based hosted persistence path | It never explicitly says Docker is not required or only optional. |
| PRD-018 | Overlay saved user data on every show appearance | critical | partial | `2.3`: "only public metadata is refreshed, never user overlay"; `5.1 getShowDetails` merges saved show | The plan does not explicitly require overlaying My Data in every list, search result, AI recommendation, and mention surface. |
| PRD-019 | Support visible statuses plus hidden `Next` | important | partial | `3.2 TypeScript Shapes`: `active`, `later`, `wait`, `done`, `quit`; `11. Open Questions` asks if Next should surface | The data model omits hidden `next`, so the hidden status is not actually supported. |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | full | `3.3 Merge & Persistence Rules`: selecting Interested/Excited sets `later` and interest |  |
| PRD-021 | Support free-form multi-tag personal tag library | important | full | `3.1 shows`: `my_tags TEXT[]`; `4.1 FilterSidebar`: derives tag filters |  |
| PRD-022 | Define collection membership by assigned status | critical | full | `3.3`: "A show is in collection when `my_status` is non-null" |  |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | full | `3.3 Auto-save triggers` lists all four triggers |  |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | `3.3 Defaults` and auto-save trigger for rating as `done` |  |
| PRD-025 | Removing status deletes show and all My Data | critical | full | `3.3 Removal`: confirmation, delete row or nullify all My Data |  |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | full | `2.3`: public refreshed, never user overlay; `3.3 Catalog refresh merge` |  |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | `3.1 shows`: separate updated_at fields for status, interest, tags, score, scoop |  |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | partial | `3.3 Catalog refresh merge`: timestamp resolution; `6.3`: chat summaries; Scoop freshness | Sorting and full sync usage are not planned explicitly. |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | full | `3.3 AI Scoop`: "Persisted only when show is in collection; 4-hour freshness" |  |
| PRD-030 | Keep Ask and Alchemy state session-only | important | full | `4.2 Ask`: React state; `4.2 Alchemy`: `useAlchemySession` tracks inputs/concepts/results |  |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | full | `6.2`: validate IDs resolve; unresolved titles non-interactive |  |
| PRD-032 | Show collection and rating tile indicators | important | full | `4.1 ShowTile`: "in-collection indicator, user rating indicator" |  |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | partial | `3.1 user_settings`; unique show constraint; timestamp merge tests | The plan lacks explicit duplicate detection/merge behavior and cross-device sync consistency rules. |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | full | `8. Phase 4`: "data migration/versioning safeguard"; risk mitigation "merge-forward logic" |  |
| PRD-035 | Persist synced settings, local settings, UI state | important | partial | `3.1 user_settings`; settings page covers font size and search-on-launch | Local-only UI state such as last selected filter and status-removal counts is only partly represented. |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | full | `5.3 Catalog Mapping`: store provider IDs only; transient fields not persisted |  |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | full | `3.3 Catalog refresh merge`: non-empty fields, My Data timestamp resolution, update details date |  |
| PRD-038 | Provide filters panel and main screen destinations | important | full | `4.1 Home`: sidebar + main content; directory includes Home, Find, Detail, Person, Settings |  |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | partial | `4.2 Find / Discover Hub`; `7.2 PageShell`: nav/main area | The plan identifies Find but does not explicitly make it persistent primary navigation. |
| PRD-040 | Keep Settings in persistent primary navigation | important | partial | Directory includes `Settings`; `7.2 PageShell`: nav/main area | The plan builds Settings but does not explicitly place it in persistent primary navigation. |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | `4.2 Find / Discover Hub`: modes Search, Ask, Alchemy |  |
| PRD-042 | Show only library items matching active filters | important | full | `4.1 Logic`: apply selected filter and media type |  |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | `4.1 StatusSection`: Active, Excited, Interested, Other |  |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | full | `4.1 FilterSidebar`: All Shows, tag, No tags, genre/decade/community-score; media toggle |  |
| PRD-045 | Render poster, title, and My Data badges | important | full | `4.1 ShowTile`: poster, title, in-collection and rating indicators |  |
| PRD-046 | Provide empty-library and empty-filter states | detail | full | `4.1 Empty states`: no collection CTA and "No results found" |  |
| PRD-047 | Search by title or keywords | important | full | `4.2 Search`: text input and TMDB search |  |
| PRD-048 | Use poster grid with collection markers | important | full | `4.2 SearchResultsGrid`: poster grid; mark items already in collection |  |
| PRD-049 | Auto-open Search when setting is enabled | detail | partial | `3.2 UserSettings`: `searchOnLaunch`; `4.5 AppearanceSettings` includes search-on-launch toggle | It defines the setting but does not explicitly plan launch behavior that auto-opens Search. |
| PRD-050 | Keep Search non-AI in tone | important | full | `4.2 Search`: external catalog search; AI is confined to Ask/Alchemy/Explore/Scoop |  |
| PRD-051 | Preserve Show Detail narrative section order | important | full | `4.3 Show Detail`: ordered section list marked "preserve existing narrative hierarchy" |  |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | full | `4.3 HeaderMedia`: backdrops/posters/logos/trailers; fallback gracefully |  |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | full | `4.3 CoreFacts`: year/runtime, community score |  |
| PRD-054 | Place status/interest controls in toolbar | important | full | `4.3 MyRelationshipToolbar`: status chips, rating slider, tags |  |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | `3.3 Auto-save triggers`: first tag on unsaved show saves later/interested |  |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | `3.3 Auto-save triggers`: rating unsaved show saves as done |  |
| PRD-057 | Show overview early for fast scanning | important | full | `4.3 Section order`: overview appears immediately after relationship toolbar |  |
| PRD-058 | Scoop shows correct states and progressive feedback | important | partial | `4.3 OverviewAndScoop`: toggle and streaming generation; `6.4`: progressive streaming | It does not specify cached/open/generating state copy and fallback states in detail. |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | full | `4.3 AskAboutShow`: CTA to Ask seeded with this show |  |
| PRD-060 | Include traditional recommendations strand | important | full | `4.3 RecommendationsStrand`: similar/recommended shows |  |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | full | `4.3 ExploreSimilar`: Get Concepts -> select -> Explore Shows -> 5 recs |  |
| PRD-062 | Include streaming availability and person-linking credits | important | full | `4.3 StreamingProviders` and `CastCrewStrand` to Person Detail |  |
| PRD-063 | Gate seasons to TV and financials to movies | important | full | `4.3 Seasons`: TV only; `BudgetRevenue`: movies only |  |
| PRD-064 | Keep primary actions early and page not overwhelming | important | full | `10. Risks`: preserve hierarchy, cluster primary actions early, lazy-load tail sections |  |
| PRD-065 | Provide conversational Ask chat interface | important | full | `4.2 Ask`: chat UI with user/assistant turns |  |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | partial | `6.1 Ask`: friend mode, taste-aware, bulleted recs, spoiler-safe | It covers tone and safety but not the direct-answer-in-first-lines/confident-picks quality bar explicitly. |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | `4.2 Ask`: `MentionedShowsStrip` parses and resolves showList |  |
| PRD-068 | Open Detail from mentions or Search fallback | important | full | `6.2`: unresolved titles shown non-interactively or Search handoff; resolved IDs selectable |  |
| PRD-069 | Show six random starter prompts with refresh | important | full | `4.2 Ask`: `StarterPrompts`: 6 random prompts, refreshable |  |
| PRD-070 | Summarize older turns while preserving voice | important | full | `6.3 Context Inclusion`: summarize older chat turns while preserving persona |  |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | full | `4.3 AskAboutShow`: CTA to Ask seeded with this show |  |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | full | `6.1 Ask with mentions`: `commentary` plus `showList` format exactly shown |  |
| PRD-073 | Retry malformed mention output once, then fallback | important | full | `6.2 Parsing & Fallbacks`: retry once, then fallback |  |
| PRD-074 | Redirect Ask back into TV/movie domain | important | full | `6.1 Ask`: "stay in TV/movies" |  |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | partial | `4.2 Alchemy`: concept catalysts; `4.3 ExploreSimilar`: concepts drive recs | The plan does not explicitly prohibit genre/plot concepts or define concepts as taste ingredients. |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | full | `6.1 Concepts`: "Bullet list, 1-3 words... no spoilers"; tests include concept parser |  |
| PRD-077 | Order concepts by strongest aha and varied axes | important | partial | `6.1 Concepts`: centralized concept prompt; `9.3` quality validation | It does not explicitly require strongest-first ordering or varied conceptual axes. |
| PRD-078 | Require concept selection and guide ingredient picking | important | full | `4.2 Alchemy`: selectable chips max 8; `4.3 ExploreSimilar`: Get Concepts -> select -> Explore Shows |  |
| PRD-079 | Return exactly five Explore Similar recommendations | important | full | `4.3 ExploreSimilar`: "5 recs"; `6.1 Concept recs`: 5 or 6 recs |  |
| PRD-080 | Support full Alchemy loop with chaining | important | full | `4.2 Alchemy`: input picker -> concepts -> results; "More Alchemy!" chains |  |
| PRD-081 | Clear downstream results when inputs change | important | full | `4.2 Alchemy`: track inputs -> concepts -> results; `useConceptSelection`; "Backtracking allowed" in phase flow |  |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | partial | `6.1 Concepts`: shared across all inputs for Alchemy; `5.1 getConcepts` returns 8 | The plan supports shared multi-show concepts but not the larger option pool; it even states 8 for single or multi-show. |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | full | `6.1 Concept recs`: reasons name concepts |  |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | full | `9.3 Quality Bar Validation`: taste alignment, surprise without betrayal, specificity, real-show integrity |  |
| PRD-085 | Keep one consistent AI persona across surfaces | important | full | `6.1 Prompt Architecture`: centralized prompts; `9.3`: voice adherence |  |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | full | `6.1`: spoiler-safe/stay in TV-movies; `6.2`: parser fallbacks; `9.3`: quality bar |  |
| PRD-087 | Make AI warm, joyful, and light in critique | important | partial | `6.1 Ask`: friend mode; `6.1 Scoop`: personal taste mini-review | The plan does not explicitly encode joy-forward warmth or friendly, non-snobby critique as guardrails. |
| PRD-088 | Structure Scoop as personal taste mini-review | important | full | `6.1 Scoop`: personal take, stack-up, centerpiece, fit/warnings, verdict |  |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | full | `6.1 Ask`: "Friend mode"; `4.2 Ask`: conversational chat UI |  |
| PRD-090 | Feed AI the right surface-specific context inputs | important | full | `6.3 Context Inclusion`: Ask/Alchemy/Explore include library; show context for Scoop |  |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | full | `9.3 Quality Bar Validation`: rubric dimensions and real-show integrity must be 2/2 |  |
| PRD-092 | Show person gallery, name, and bio | important | full | `4.4 Person Detail`: `PersonHeader` image gallery, name, bio |  |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | full | `4.4 PersonAnalytics`: average project ratings, top genres, projects-by-year |  |
| PRD-094 | Group filmography by year | important | full | `4.4 Filmography`: credits grouped by year |  |
| PRD-095 | Open Show Detail from selected credit | important | full | `4.4 Filmography`: tapping credit opens Show Detail |  |
| PRD-096 | Include font size and Search-on-launch settings | important | full | `4.5 AppearanceSettings`: font size, search-on-launch toggle |  |
| PRD-097 | Support username, model, and API-key settings safely | important | full | `3.1 user_settings`; `4.5 AISettings` and `CatalogSettings`; encrypted keys |  |
| PRD-098 | Export saved shows and My Data as zip | critical | full | `4.5 DataManagement`: export My Data as `.zip`; `5.1 exportMyData()` |  |
| PRD-099 | Encode export dates using ISO-8601 | important | full | `4.5 DataManagement`: ISO-8601 JSON backup |  |

### 3. Coverage Scores

Overall score:

```
score = (83 x 1.0 + 16 x 0.5) / 99 x 100 = 91.9%
```

Critical:  (29 x 1.0 + 1 x 0.5) / 30 x 100 = 98.3%  (29.5 of 30 critical requirements)
Important: (53 x 1.0 + 14 x 0.5) / 67 x 100 = 89.6%  (60 of 67 important requirements)
Detail:    (1 x 1.0 + 1 x 0.5) / 2 x 100 = 75.0%  (1.5 of 2 detail requirements)
Overall:   91.9% (99 total requirements)

### 4. Top Gaps

1. PRD-018 (`critical`) - Overlay saved user data on every show appearance. The plan protects user overlay during detail merges, but it does not make overlay behavior a universal rendering contract for search, recommendations, mentioned shows, and all tiles; users could see stale or generic versions of shows outside Detail.
2. PRD-019 (`important`) - Support visible statuses plus hidden `Next`. The plan omits `next` from both SQL and TypeScript status types, so future surfacing or migrations would require data-model changes instead of merely enabling UI.
3. PRD-033 (`important`) - Sync libraries/settings consistently and merge duplicates. The plan has namespace/user scoping and timestamp merge logic, but not an explicit duplicate detection and transparent merge strategy; cross-device or repeated catalog mappings could create trust-eroding inconsistencies.
4. PRD-035 (`important`) - Persist synced settings, local settings, UI state. The plan covers user settings but only partially handles local/UI preferences; status-removal suppression, last selected filters, and similar state could be lost or behave inconsistently.
5. PRD-082 (`important`) - Generate shared multi-show concepts with larger option pool. The plan says concept generation returns 8 for single or multi-show, which weakens Alchemy by giving multi-show blends no extra room to find varied shared ingredients.

### 5. Coverage Narrative

#### Overall Posture

This is a strong and executable plan with no fully missing catalog requirement, but it is not perfect parity. The foundation, persistence model, major screens, AI surfaces, and export story are well covered. The remaining gaps are mostly about exact behavioral contracts that turn a plausible implementation into one that matches the PRD under edge cases and quality review.

#### Strength Clusters

Coverage is strongest in Benchmark Runtime & Isolation, Show Detail & Relationship UX, Ask Chat, Person Detail, and Settings & Export. The plan is especially concrete about Next.js/Supabase, namespace and user scoping, server-side source of truth, auto-save rules, Ask structured mentions, Show Detail ordering, Person Detail analytics, and zip export.

#### Weakness Clusters

The partials cluster around subtle product semantics rather than basic feature presence. Collection Data & Persistence has the highest-impact ambiguity: universal My Data overlays, hidden `Next`, timestamp usage, duplicate sync, and local UI state. Concepts and AI Voice also have several partials where the plan names the feature but under-specifies the quality contract that makes it feel like the intended product.

#### Risk Assessment

If executed as-is, the most likely failure mode is a product that works functionally but feels inconsistent at the edges. QA would probably notice saved shows appearing with incomplete My Data in discovery surfaces, `Next` being impossible to represent, Alchemy concepts feeling too generic or cramped, and AI responses passing basic prompts while missing the warmer, sharper voice rules.

#### Remediation Guidance

The plan needs targeted acceptance criteria, not a wholesale rewrite. Add explicit cross-surface overlay rules, complete the status enum with hidden `Next`, define duplicate/sync and local UI persistence behavior, and tighten AI/concept prompt contracts around voice, ordering, variety, and multi-show option counts. These are planning precision fixes that should become tests or checklist items before implementation begins.
