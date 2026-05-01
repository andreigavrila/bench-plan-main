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
- PRD-047 | `important` | Search by title or keywords | `product_prd.md > 7.2 Search (Find â†’ Search)`
- PRD-048 | `important` | Use poster grid with collection markers | `product_prd.md > 7.2 Search (Find â†’ Search)`
- PRD-049 | `detail` | Auto-open Search when setting is enabled | `product_prd.md > 7.2 Search (Find â†’ Search)`
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

##### Concepts, Explore Similar & Alchemy

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

##### AI Voice, Persona & Quality

- PRD-085 | `important` | Keep one consistent AI persona across surfaces | `supporting_docs/ai_voice_personality.md > 1. Persona Summary`
- PRD-086 | `critical` | Enforce shared AI guardrails across all surfaces | `supporting_docs/ai_prompting_context.md > 1. Shared Rules (All AI Surfaces)`
- PRD-087 | `important` | Make AI warm, joyful, and light in critique | `supporting_docs/ai_voice_personality.md > 2. Non-Negotiable Voice Pillars`
- PRD-088 | `important` | Structure Scoop as personal taste mini-review | `supporting_docs/ai_voice_personality.md > 4.1 Scoop (Show Detail "The Scoop")`
- PRD-089 | `important` | Keep Ask brisk and dialogue-like by default | `supporting_docs/ai_voice_personality.md > 4.2 Ask (Find â†’ Ask)`
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
| PRD-001 | Use Next.js latest stable runtime | critical | full | `2.1 Runtime & Framework`: "Next.js (latest stable) with App Router." |  |
| PRD-002 | Use Supabase official client libraries | critical | partial | `2.2 Persistence`: "Supabase ... as the single source of truth"; `src/lib/supabaseClient` | The plan commits to Supabase but does not explicitly require official Supabase client libraries. |
| PRD-003 | Ship `.env.example` with required variables | critical | full | `11.1 Environment Variables`: "Create `.env.example`" with Supabase, identity, AI, and catalog variables. |  |
| PRD-004 | Ignore `.env*` secrets except example | important | full | `11.1 Environment Variables`: "`.gitignore` must exclude `.env*` except `.env.example`." |  |
| PRD-005 | Configure build through env without code edits | critical | full | `11.1 Environment Variables`; `5.1 Namespace Isolation`: read `NAMESPACE_ID` from environment. |  |
| PRD-006 | Keep secrets out of repo and server-only | critical | full | `11.1 Environment Variables`: service role marked server-only; keys "never committed to repo." |  |
| PRD-007 | Provide app, test, reset command scripts | critical | full | `11.2 Scripts`: `npm run dev`, `npm test`, `npm run test:reset`. |  |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | `4.3 Migrations`: Supabase CLI migrations and deterministic seed fixtures. |  |
| PRD-009 | Use one stable namespace per build | critical | full | `5.1 Namespace Isolation`: read `NAMESPACE_ID` at build/start time. |  |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | `5.1 Namespace Isolation`: all reads/writes include namespace and reset deletes by namespace. |  |
| PRD-011 | Attach every user record to `user_id` | critical | full | `4.1 Core Tables`: `user_id` required on `shows` and `settings`; `10.3 Sync`. |  |
| PRD-012 | Partition persisted data by namespace and user | critical | full | `4.2 Row-Level Security`: enforce `namespace_id` and `user_id`. |  |
| PRD-013 | Support documented dev auth injection, prod-gated | important | full | `5.2 User Identity`: dev header or fixed user; `12`: gate dev-only routes. |  |
| PRD-014 | Real OAuth later needs no schema redesign | important | full | `5.2 User Identity`; `12 Migration Path to Real Auth & Production`. |  |
| PRD-015 | Keep backend as persisted source of truth | critical | full | `2.2 Persistence`: Supabase is "the single source of truth." |  |
| PRD-016 | Make client cache safe to discard | critical | full | `6.3 Transient Data Strategy`: React Query cache is "safe to clear without data loss." |  |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | partial | `2.2 Persistence`: "Supabase (hosted or local)" | The hosted/local wording implies a non-local path but never states Docker is optional or not required. |
| PRD-018 | Overlay saved user data on every show appearance | critical | partial | `7.2 Search`: overlay `my_status`, `my_score`; `7.6 Person Detail`: overlay badges. | The plan covers several surfaces but lacks a global rule that every list, recommendation, AI output, and show appearance must use the user-overlaid version. |
| PRD-019 | Support visible statuses plus hidden `Next` | important | full | `4.1 Core Tables` includes `next`; `13 Open Questions`: Next is modeled but not surfaced. |  |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | full | `7.5 My Relationship Controls`: Interested/Excited sets `my_status = 'later'` plus `my_interest`. |  |
| PRD-021 | Support free-form multi-tag personal tag library | important | full | `7.5 My Relationship Controls`: free-form add/remove; `7.1 FilterSidebar`: tag filters from existing tags. |  |
| PRD-022 | Define collection membership by assigned status | critical | full | `9.1 Collection Membership`: "in collection" when `my_status IS NOT NULL`. |  |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | full | `9.2 Saving Triggers`: status, interest chip, rating, tag. |  |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | `9.3 Default Values When Saving`: Later/Interested; rating first save goes to Done. |  |
| PRD-025 | Removing status deletes show and all My Data | critical | full | `7.5 My Relationship Controls`: reselecting status confirms removal, clears My Data, and deletes row. |  |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | full | `9.5 Re-adding the Same Show`: preserve My Data, refresh metadata, timestamp conflicts. |  |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | `4.1 Core Tables`: individual update dates for tags, score, status, interest, scoop. |  |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | full | `9.6 Timestamps`: sorting, sync conflict resolution, AI cache freshness. |  |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | full | `7.5 Scoop`: stale after 4 hours and persisted only if `my_status IS NOT NULL`. |  |
| PRD-030 | Keep Ask and Alchemy state session-only | important | full | `9.7 AI Data Persistence`: Alchemy and Ask are session only. |  |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | full | `8.4 Streaming & Parsing`: resolve recommendations by external ID or title search; `8.5 Fallbacks`. |  |
| PRD-032 | Show collection and rating tile indicators | important | full | `7.1 Sub-features`: `ShowTile` has in-collection badge and user rating badge. |  |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | full | `10.3 Sync`: settings, per-field conflict resolution, duplicate detection by external ID. |  |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | full | `10.2 Data Continuity Across Versions`: migrations bring forward saved shows and My Data. |  |
| PRD-035 | Persist synced settings, local settings, UI state | important | partial | `7.7 Settings & Export`; `9.4 Removing from Collection`; `11.1 Environment Variables`. | Synced settings and some local/UI preferences are covered, but the plan omits full UI state such as `lastSelectedFilter`. |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | full | `4.1 Core Tables`: `provider_data`; `6.3 Transient Data Strategy`: details fetched on demand. |  |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | full | `6.2 Mapping & Merge Strategy`: `selectFirstNonEmpty`, My fields by timestamp, preserve creation date. |  |
| PRD-038 | Provide filters panel and main screen destinations | important | full | `3 Repo Structure` routes and `7.1 FilterSidebar`. |  |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | partial | `3 Repo Structure`: `/find/page.tsx`; `7.2-7.4` Find hub modes. | The plan defines the route and hub but does not explicitly require a persistent primary navigation entry. |
| PRD-040 | Keep Settings in persistent primary navigation | important | partial | `3 Repo Structure`: `/settings/page.tsx`; `7.7 Settings & Export`. | The plan defines the route but does not explicitly require Settings to remain in persistent primary navigation. |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | `7.2 Search`, `7.3 Ask`, `7.4 Alchemy`. |  |
| PRD-042 | Show only library items matching active filters | important | full | `7.1 Server Query`: `my_status IS NOT NULL` and active filter predicates. |  |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | `7.1 Status Grouping Logic`: four required groups. |  |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | full | `7.1 Responsibilities`: All, tags, genre, decade, community score, media-type toggle. |  |
| PRD-045 | Render poster, title, and My Data badges | important | full | `7.1 Sub-features`: `ShowTile` poster, title, in-collection badge, user rating badge. |  |
| PRD-046 | Provide empty-library and empty-filter states | detail | full | `7.1 Empty States`: no shows prompt and filter no-results message. |  |
| PRD-047 | Search by title or keywords | important | full | `7.2 Search`: text search by title/keywords. |  |
| PRD-048 | Use poster grid with collection markers | important | full | `7.2 Search`: poster grid with in-collection items marked. |  |
| PRD-049 | Auto-open Search when setting is enabled | detail | full | `7.2 Search`: controlled by local setting `autoSearch`. |  |
| PRD-050 | Keep Search non-AI in tone | important | partial | `7.2 Search`: external catalog text search; AI features are separated into Ask and Alchemy. | The plan implies Search is plain catalog search but does not explicitly state Search must avoid AI persona/tone. |
| PRD-051 | Preserve Show Detail narrative section order | important | partial | `7.5 Show Detail Page`: "Narrative hierarchy (must preserve order unless intentionally changed)." | The plan lists a concrete hierarchy, but it combines relationship toolbar/tags and does not exactly match the supporting doc's section order. |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | full | `7.5 Header Media Carousel`: backdrops, posters, logos, trailers, graceful fallback. |  |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | full | `7.5 Core Facts Row`: year, runtime/seasons, community score. |  |
| PRD-054 | Place status/interest controls in toolbar | important | full | `7.5 My Relationship Toolbar`: status chips, rating slider, tags. |  |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | `7.5 My Relationship Controls`: tags auto-save unsaved show as Later/Interested. |  |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | `7.5 My Relationship Controls`: rating unsaved show auto-saves as Done. |  |
| PRD-057 | Show overview early for fast scanning | important | full | `7.5 Narrative hierarchy`: Overview + Scoop Toggle appears early at step 4. |  |
| PRD-058 | Scoop shows correct states and progressive feedback | important | full | `7.5 Scoop`: generated if absent/stale, streams progressively, shows "Generating..." state. |  |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | full | `7.5 Ask About This Show CTA`: seeds Ask with this show. |  |
| PRD-060 | Include traditional recommendations strand | important | full | `7.5 Traditional Recommendations Strand`: similar/recommended from catalog. |  |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | full | `7.5 Explore Similar`: Get Concepts, select concepts, Explore Shows. |  |
| PRD-062 | Include streaming availability and person-linking credits | important | full | `7.5`: Streaming Availability and Cast & Crew links to Person Detail. |  |
| PRD-063 | Gate seasons to TV and financials to movies | important | full | `7.5`: Seasons TV only; Budget/Revenue movies. |  |
| PRD-064 | Keep primary actions early and page not overwhelming | important | full | `7.5 Narrative hierarchy`; `10.5 Performance`: lazy-load heavy sections. |  |
| PRD-065 | Provide conversational Ask chat interface | important | full | `7.3 Ask`: chat UI with user/assistant turns. |  |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | full | `8.2 askPrompt`: conversational discovery; `8.2 basePersona`: warm, opinionated, spoiler-safe. |  |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | `7.3 Ask`: horizontally scrollable mentioned shows row. |  |
| PRD-068 | Open Detail from mentions or Search fallback | important | full | `7.3 Ask`: resolve titles, render selectable tiles, fallback to Search. |  |
| PRD-069 | Show six random starter prompts with refresh | important | full | `7.3 Ask`: welcome view with 6 random starter prompts and refresh. |  |
| PRD-070 | Summarize older turns while preserving voice | important | partial | `7.3 Ask`: auto-summarize after ~10 turns; `8.3 Context Injection`. | The plan includes summarization but does not say summaries must preserve the same persona/tone. |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | full | `7.3 Variants`: Ask About a Show launched with pre-seeded show context. |  |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | full | `7.3 AI Contract`: `{ commentary, showList: "Title::externalId::mediaType;;..." }`. |  |
| PRD-073 | Retry malformed mention output once, then fallback | important | full | `8.5 Fallbacks`: structured parsing failure retries once, then unstructured fallback. |  |
| PRD-074 | Redirect Ask back into TV/movie domain | important | partial | `8.2 basePersona`: "TV/movie nerd friend." | The plan implies domain focus but does not explicitly require redirecting off-domain Ask prompts back to TV/movies. |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | partial | `7.4 Alchemy`: "shared concept catalysts"; `8.2 conceptsPrompt`. | The plan uses concept language but does not explicitly forbid genre/plot concepts or frame them as taste ingredients. |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | partial | `8.2 conceptsPrompt`: bullet list only, 1-3 words, no explanations. | Non-generic enforcement is only touched as non-blocking monitoring, not a hard output requirement. |
| PRD-077 | Order concepts by strongest aha and varied axes | important | missing | none | The plan does not specify concept ordering by strongest aha or diversity across axes. |
| PRD-078 | Require concept selection and guide ingredient picking | important | partial | `7.4 Alchemy`: user selects 1-8 concepts; `7.5 Explore Similar`: user selects 1+ concepts. | Selection is required, but the plan does not include guidance copy about picking ingredients the user wants more of. |
| PRD-079 | Return exactly five Explore Similar recommendations | important | full | `7.5 Explore Similar`: AI returns 5 recommendations. |  |
| PRD-080 | Support full Alchemy loop with chaining | important | full | `7.4 Alchemy Flow`: select inputs, conceptualize, select concepts, alchemize, chain. |  |
| PRD-081 | Clear downstream results when inputs change | important | full | `7.4 Alchemy`: changing inputs clears concepts/results. |  |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | partial | `7.4 AI Contract`: multi-show concepts must be shared/common. | The plan covers shared concepts but caps returned concepts at 8 and does not specify a larger multi-show option pool. |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | full | `7.4 AI Contract`; `7.5 Explore Similar`: reasons explicitly name matched concepts. |  |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | partial | `1 Overview & Goals`: high-quality, taste-aware discovery; `8.6 Quality Heuristics`. | Taste alignment is covered, but surprise-without-betrayal and defensibility are not specified as acceptance criteria. |
| PRD-085 | Keep one consistent AI persona across surfaces | important | full | `8.2 Prompt Orchestration`: shared `basePersona.ts` for all prompts. |  |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | partial | `8.2 basePersona`: warm, opinionated, spoiler-safe TV/movie nerd friend. | The plan centralizes persona, but it does not explicitly enumerate and enforce all shared guardrails such as domain redirect, specific reasoning, and actionable real-show outputs across every surface. |
| PRD-087 | Make AI warm, joyful, and light in critique | important | partial | `1 Overview & Goals`: warm, opinionated, spoiler-safe AI voice; `8.2 basePersona`. | Warmth is explicit, but joy-forward behavior and light critique are not spelled out as non-negotiable voice pillars. |
| PRD-088 | Structure Scoop as personal taste mini-review | important | full | `7.5 Scoop`; `8.2 scoopPrompt`: personal take, stack-up, centerpiece, fit/warnings, verdict. |  |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | full | `8.2 askPrompt`: "responds like a friend in dialogue (not an essay)." |  |
| PRD-090 | Feed AI the right surface-specific context inputs | important | full | `8.3 Context Injection`: library, current show, selected concepts, conversation turns. |  |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | partial | `8.6 Quality Heuristics`: generic-concept logging and reason checks. | The plan has non-blocking monitoring but no scoring rubric and no hard-fail real-show integrity gate. |
| PRD-092 | Show person gallery, name, and bio | important | full | `7.6 Person Detail Page`: image gallery, name, bio. |  |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | full | `7.6 Person Detail Page`: average project ratings, top genres, projects-by-year. |  |
| PRD-094 | Group filmography by year | important | full | `7.6 Person Detail Page`: filmography grouped by year. |  |
| PRD-095 | Open Show Detail from selected credit | important | full | `7.6 Person Detail Page`: credit selection navigates to `/show/[id]`. |  |
| PRD-096 | Include font size and Search-on-launch settings | important | full | `7.7 Settings`: font size and search-on-launch toggle. |  |
| PRD-097 | Support username, model, and API-key settings safely | important | full | `7.7 Settings`: username, AI key, model, catalog key; `Security`: keys never committed. |  |
| PRD-098 | Export saved shows and My Data as zip | critical | full | `7.7 Your Data`: zip containing JSON backup of all saved shows and My Data. |  |
| PRD-099 | Encode export dates using ISO-8601 | important | full | `7.7 Your Data`: "Dates ISO-8601"; `10.1 User Data Ownership`. |  |

### 3. Coverage Scores

Overall score:

```
score = (80 × 1.0 + 18 × 0.5) / 99 × 100 = 89.9%
```

Critical:  (27 × 1.0 + 3 × 0.5) / 30 × 100 = 95.0%  (28.5 of 30 critical requirements)
Important: (51 × 1.0 + 15 × 0.5) / 67 × 100 = 87.3%  (58.5 of 67 important requirements)
Detail:    (2 × 1.0 + 0 × 0.5) / 2 × 100 = 100.0%  (2 of 2 detail requirements)
Overall:   89.9% (99 total requirements)

### 4. Top Gaps

1. PRD-086 | `critical` | Enforce shared AI guardrails across all surfaces

   This matters because the plan treats shared AI behavior mostly as a persona/prompt organization problem, while the PRD requires enforceable guardrails for domain scope, spoiler safety, specific reasoning, and actionable outputs across Scoop, Ask, Alchemy, and Explore Similar.

2. PRD-018 | `critical` | Overlay saved user data on every show appearance

   This matters because users will notice inconsistency immediately if a saved show displays status/rating in Search but not in AI recommendations, relationship strands, or other show tiles.

3. PRD-002 | `critical` | Use Supabase official client libraries

   This matters because the infrastructure rider is explicit about the Supabase integration boundary; omitting official client libraries leaves room for ad hoc database access that may weaken auth, RLS, and maintainability assumptions.

4. PRD-077 | `important` | Order concepts by strongest aha and varied axes

   This matters because the concept system is the core of Explore Similar and Alchemy; without ordering and axis diversity, the recommendations can feel generic even when the mechanics work.

5. PRD-091 | `important` | Validate discovery with rubric and hard-fail integrity

   This matters because the plan's discovery quality checks are non-blocking, so hallucinated or poorly grounded recommendations could reach users despite the PRD making real-show integrity non-negotiable.

### 5. Coverage Narrative

#### Overall Posture

This is a structurally strong plan with mostly complete infrastructure, persistence, navigation, core UI, and export coverage. The main concern is not broad feature omission; it is that several AI behavior and concept-quality requirements are captured as prompt intent or monitoring rather than as enforceable product contracts.

#### Strength Clusters

Coverage is strongest in Benchmark Runtime & Isolation, Collection Home & Search, Person Detail, and Settings & Export. The plan is especially concrete about Supabase schema shape, namespace/user partitioning, migration artifacts, collection grouping, search behavior, detail-page business rules, and backup export.

#### Weakness Clusters

The partial and missing items cluster around AI behavioral contracts and taste-discovery craft. Concepts, Explore Similar & Alchemy has the only missing requirement and several partials, while AI Voice, Persona & Quality has guardrail and validation gaps that suggest the plan under-specifies how AI outputs are tested and rejected.

#### Risk Assessment

If executed as-is, the most likely failure mode is a functionally complete app whose AI discovery feels inconsistent or insufficiently curated. QA would probably find the app can save, search, and navigate correctly, but concept chips, Ask behavior, and recommendation quality may drift from the intended "taste ingredient" model and allow generic or weakly validated outputs.

#### Remediation Guidance

The remaining planning work should add explicit acceptance criteria and guardrail enforcement for AI surfaces, not just more implementation detail. The plan needs firmer contracts for concept generation quality, off-domain redirection, voice-preserving summarization, global user-overlay display rules, persistent navigation, and discovery validation with hard-fail real-show integrity.
