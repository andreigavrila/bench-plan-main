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
| PRD-001 | Use Next.js latest stable runtime | critical | full | `1.1 Technology Stack` states `Next.js (latest stable)` |  |
| PRD-002 | Use Supabase official client libraries | critical | full | `1.1 Technology Stack` states Supabase is accessed via official client libraries |  |
| PRD-003 | Ship `.env.example` with required variables | critical | full | `10.1 Repository Deliverables` requires `.env.example` with variables and comments |  |
| PRD-004 | Ignore `.env*` secrets except example | important | full | `10.1 Repository Deliverables` requires `.gitignore` excluding `.env*` except `.env.example` |  |
| PRD-005 | Configure build through env without code edits | critical | full | `10.1 Repository Deliverables` says build runs by filling environment variables without editing source |  |
| PRD-006 | Keep secrets out of repo and server-only | critical | full | `10.1 Credential Handling` covers uncommitted secrets, anon browser key, server-only service role |  |
| PRD-007 | Provide app, test, reset command scripts | critical | full | `10.1 One-Command Developer Experience` lists `npm run dev`, `npm test`, `npm run test:reset` |  |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | `10.1 Database Evolution Artifacts` requires migrations and deterministic fresh database state |  |
| PRD-009 | Use one stable namespace per build | critical | full | `3.2 Namespace Isolation` states each build uses a single stable `namespace_id` |  |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | `3.2 Namespace Isolation` and `10.3 Destructive Testing Rules` scope reads, writes, and resets to namespace |  |
| PRD-011 | Attach every user record to `user_id` | critical | full | `1.2 Core Architectural Principles` and table schemas scope user-owned records to `user_id` |  |
| PRD-012 | Partition persisted data by namespace and user | critical | full | `1.2 Core Architectural Principles` states effective partition is `(namespace_id, user_id)` |  |
| PRD-013 | Support documented dev auth injection, prod-gated | important | full | `3.1 Benchmark Mode Identity` specifies dev-only `X-User-Id`, selector, default user, and production gating |  |
| PRD-014 | Real OAuth later needs no schema redesign | important | full | `1.2 Core Architectural Principles` and `13. Success Criteria` require OAuth migration without schema redesign |  |
| PRD-015 | Keep backend as persisted source of truth | critical | full | `1.2 Core Architectural Principles` states backend is the single source of truth |  |
| PRD-016 | Make client cache safe to discard | critical | full | `10.2 Data Ownership & Local Storage` says clearing local storage or reinstalling does not lose data |  |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | full | `1.1 Technology Stack` and `10.4 Cloud Agent Compatibility` say Docker is not required |  |
| PRD-018 | Overlay saved user data on every show appearance | critical | full | `8. Cross-Cutting Rules` says the user's version takes precedence everywhere |  |
| PRD-019 | Support visible statuses plus hidden `Next` | important | full | `2.1 shows` includes `my_status` with `next`; UI chips omit `Next` and `12. Open Questions` keeps it non-first-class |  |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | full | `4.5 My Relationship Controls` says Interested/Excited map to `Later + Interest` |  |
| PRD-021 | Support free-form multi-tag personal tag library | important | partial | `2.1 shows` has `my_tags` array and `4.1 Filters` creates one filter per user tag | The plan stores and filters multiple tags, but it does not explicitly specify free-form tag creation/editing or a reusable personal tag library UX. |
| PRD-022 | Define collection membership by assigned status | critical | full | `4.5 Saving Triggers` and removal semantics make status assignment the save/removal boundary |  |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | full | `4.5 Saving Triggers` lists status, interest chip, rating, and tag saves |  |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | `4.5 Default Values When Saving` states Later/Interested default and Done exception for rating |  |
| PRD-025 | Removing status deletes show and all My Data | critical | full | `4.5 Removing from Collection` removes storage and clears status, interest, tags, rating, AI Scoop |  |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | full | `4.5 Re-adding Same Show` preserves user data and refreshes public metadata |  |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | `2.1 shows` lists update timestamps for tags, score, status, interest, and scoop |  |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | full | `2.2 Merge Rules`, `2.3 Data Continuity`, and Scoop freshness use timestamps for conflict and freshness behavior |  |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | full | `4.5 Overview + Scoop` says 4-hour freshness and persistence only if show is in collection |  |
| PRD-030 | Keep Ask and Alchemy state session-only | important | partial | `4.4 Data Persistence` says Alchemy results are session-only; Ask keeps short-term context | Ask chat history is not explicitly declared non-persistent or cleared when leaving/resetting Ask. |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | full | `8. Cross-Cutting Rules` says every recommendation maps to a selectable real show |  |
| PRD-032 | Show collection and rating tile indicators | important | full | `4.1 Collection Home` tiles show in-collection and rating indicators |  |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | partial | `2.2 Merge Rules` and `cloud_settings` cover consistent sync; duplicate show constraint avoids duplicates per user namespace | The plan covers sync conflict rules and duplicate prevention, but not explicit duplicate detection and transparent merge of already duplicated records. |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | full | `2.3 Data Continuity` says saved shows and user data migrate without loss |  |
| PRD-035 | Persist synced settings, local settings, UI state | important | full | `2.1 cloud_settings`, `local_settings`, and `ui_state` cover synced, local, and UI settings |  |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | partial | `2.1 shows` includes `provider_data` JSONB and Search stores external IDs | The plan does not specify provider IDs only, nor does it explicitly mark credits, seasons, videos, recommendations, and similar data as transient fetches. |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | full | `2.2 Merge Rules` defines non-empty merge, timestamp conflict resolution, and update date handling |  |
| PRD-038 | Provide filters panel and main screen destinations | important | full | `4.1 Collection Home` has `FilterSidebar`; routes cover Home, Find, Detail, Person, Settings |  |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | partial | `4.2`, `4.3`, and `4.4` define Find mode routes | The plan defines Find routes but does not explicitly require a persistent primary navigation entry. |
| PRD-040 | Keep Settings in persistent primary navigation | important | partial | `4.7 Settings & Your Data` defines `/settings` route | The plan defines Settings but does not explicitly require it in persistent primary navigation. |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | `4.2 Search`, `4.3 Ask`, and `4.4 Alchemy` define the three Find modes |  |
| PRD-042 | Show only library items matching active filters | important | full | `4.1 Collection Home` filters query shows with filter params and display matching library items |  |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | `4.1 Collection Home` lists Active, Excited, Interested, and Other sections |  |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | full | `4.1 Filters` lists All, tag, no tags, genre, decade, score ranges, and media toggle |  |
| PRD-045 | Render poster, title, and My Data badges | important | full | `4.1 Collection Home` says tiles show poster, title, and user data badges |  |
| PRD-046 | Provide empty-library and empty-filter states | detail | full | `4.1 Empty States` defines no-collection and no-filter-results states |  |
| PRD-047 | Search by title or keywords | important | full | `4.2 Search` supports text search by title/keywords |  |
| PRD-048 | Use poster grid with collection markers | important | full | `4.2 Search` uses a poster grid and marks in-collection items |  |
| PRD-049 | Auto-open Search when setting is enabled | detail | full | `4.2 Search` auto-opens when Search on Launch is enabled |  |
| PRD-050 | Keep Search non-AI in tone | important | partial | `4.2 Search` describes straightforward external catalog text search | The plan keeps Search functionally non-AI, but it never states the non-AI tone requirement or Search-specific copy boundary. |
| PRD-051 | Preserve Show Detail narrative section order | important | full | `4.5 Show Detail Page` lists the prescribed component order |  |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | full | `4.5 Header Media` prioritizes trailers and falls back to poster/backdrop |  |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | full | `4.5 Core Facts + Community Score` includes year, runtime/seasons, and score bar |  |
| PRD-054 | Place status/interest controls in toolbar | important | full | `4.5 My Relationship Controls` puts status/interest chips in the toolbar |  |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | `4.5 Tags` says adding a tag to an unsaved show auto-saves as Later + Interested |  |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | `4.5 My Rating bar` says rating an unsaved show auto-saves as Done |  |
| PRD-057 | Show overview early for fast scanning | important | full | `4.5 Show Detail Page` places Overview immediately after tags and before deeper sections |  |
| PRD-058 | Scoop shows correct states and progressive feedback | important | full | `4.5 Overview + Scoop` defines no-scoop, cached, open, generating, freshness, and persistence states |  |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | full | `4.5 Ask About This Show` says entering Ask seeds context with this show |  |
| PRD-060 | Include traditional recommendations strand | important | full | `4.5 Traditional Recommendations Strand` defines low-effort similar/recommended shows |  |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | full | `4.5 Explore Similar` specifies Get Concepts, select concepts, Explore Shows |  |
| PRD-062 | Include streaming availability and person-linking credits | important | full | `4.5 Streaming Availability` and `CastCrew` sections cover watch providers and cast/crew navigation |  |
| PRD-063 | Gate seasons to TV and financials to movies | important | full | `4.5 Components` marks `SeasonsSection` TV only and `BudgetRevenue` movies only |  |
| PRD-064 | Keep primary actions early and page not overwhelming | important | full | `4.5 Cast, Crew, Seasons, Budget/Revenue` says optional depth is never mandatory to reach discovery |  |
| PRD-065 | Provide conversational Ask chat interface | important | full | `4.3 Ask` defines `ChatInterface` with user/assistant turns |  |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | full | `7.2 Ask / Explore Search Chat` requires direct answer in first 3-5 lines, bulleted recs, confident picks |  |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | `4.3 Ask` defines `MentionedShowsStrip` as a horizontal strip |  |
| PRD-068 | Open Detail from mentions or Search fallback | important | full | `4.3 Ask Behavior` says tapping a mention opens Detail or hands off to Search |  |
| PRD-069 | Show six random starter prompts with refresh | important | full | `4.3 Ask Behavior` says the welcome view shows 6 random starter prompts with refresh |  |
| PRD-070 | Summarize older turns while preserving voice | important | partial | `4.3 Ask Behavior` summarizes older turns after about 10 messages | The plan does not say summaries must preserve the same persona or avoid sterile summary voice. |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | full | `4.3 Variants` says Ask About a Show seeds conversation with show context |  |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | full | `4.3 AI Contract` defines `commentary`, `showList`, and exact string format |  |
| PRD-073 | Retry malformed mention output once, then fallback | important | missing | none | The plan has the structured output format but no malformed-output retry or fallback policy. |
| PRD-074 | Redirect Ask back into TV/movie domain | important | full | `5.4 Explore Search Chat` and `5.6 Do / Don't` keep AI in the TV/movie domain |  |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | full | `6.1 What a Concept Is` defines concepts as ingredients, not genres or plot points |  |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | full | `6.3 Generation Rules` requires bullet list, 1-3 words, evocative, non-generic |  |
| PRD-077 | Order concepts by strongest aha and varied axes | important | full | `6.3 Quality Constraints` requires diversity and strongest aha concepts first |  |
| PRD-078 | Require concept selection and guide ingredient picking | important | full | `6.4 Selection UX Rules` requires concept selection and ingredient guidance |  |
| PRD-079 | Return exactly five Explore Similar recommendations | important | full | `6.5 Concepts -> Recommendations Contract` says Explore Similar returns 5 recommendations |  |
| PRD-080 | Support full Alchemy loop with chaining | important | full | `4.4 Alchemy` defines select shows, conceptualize, select concepts, alchemize, and chain another round |  |
| PRD-081 | Clear downstream results when inputs change | important | full | `4.4 UX Rules` says changing shows and selecting/unselecting concepts clears downstream results |  |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | partial | `4.4 AI Contract` requires shared concepts for 2+ shows | The plan does not specify a larger concept option pool for multi-show Alchemy than for single-show Explore Similar. |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | full | `6.5 Recommendations` requires reasons to reference selected concepts explicitly |  |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | full | `7.1 Taste Alignment` and `Surprise Without Betrayal` define grounded, defensible rec quality |  |
| PRD-085 | Keep one consistent AI persona across surfaces | important | full | `5.1 Persona Summary` and `5.4 Surface-Specific Adaptations` define shared persona across surfaces |  |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | full | `5.6 Do / Don't` and `8. Cross-Cutting Rules` enforce spoiler safety, domain, and real recs |  |
| PRD-087 | Make AI warm, joyful, and light in critique | important | full | `5.2 Voice Pillars` includes joy-forward warmth and friendly critique |  |
| PRD-088 | Structure Scoop as personal taste mini-review | important | full | `5.4 Scoop` requires personal take, stack-up, centerpiece, fit/warnings, and gut check |  |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | full | `5.4 Ask` defines friend-in-dialogue behavior, 1-3 paragraphs, lists when recommending |  |
| PRD-090 | Feed AI the right surface-specific context inputs | important | full | `4.3 AI Contract`, `4.4 AI Contract`, and `8. Cross-Cutting Rules` feed library, My Data, concepts, and session context |  |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | full | `7.3 Scoring Rubric` requires voice, taste alignment, real-show integrity, and total score threshold |  |
| PRD-092 | Show person gallery, name, and bio | important | full | `4.6 Person Detail Page` includes image gallery, name, and bio |  |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | full | `4.6 AnalyticsCharts` includes average ratings, top genres, and projects-by-year |  |
| PRD-094 | Group filmography by year | important | full | `4.6 FilmographySection` groups credits by year |  |
| PRD-095 | Open Show Detail from selected credit | important | full | `4.6 Behavior` says selecting a credit opens Show Detail |  |
| PRD-096 | Include font size and Search-on-launch settings | important | full | `4.7 App Settings` includes font size and Search on launch |  |
| PRD-097 | Support username, model, and API-key settings safely | important | full | `4.7 User`, `AI`, and `Integrations` cover username, model, API keys, and no committed keys |  |
| PRD-098 | Export saved shows and My Data as zip | critical | full | `4.7 Your Data` exports a `.zip` containing saved shows and My Data JSON |  |
| PRD-099 | Encode export dates using ISO-8601 | important | full | `4.7 Your Data` says export dates are encoded ISO-8601 |  |

### 3. Coverage Scores

Critical:  (30 × 1.0 + 0 × 0.5) / 30 × 100 = 100.0%  (30 of 30 critical requirements)
Important: (57 × 1.0 + 9 × 0.5) / 67 × 100 = 91.8%  (61.5 of 67 important requirements)
Detail:    (2 × 1.0 + 0 × 0.5) / 2 × 100 = 100.0%  (2 of 2 detail requirements)
Overall:   94.4% (99 total requirements)

### 4. Top Gaps

1. PRD-073 (`important`) Retry malformed mention output once, then fallback

This matters because Ask depends on structured `showList` output to render selectable mentioned shows; without retry and fallback behavior, malformed model output can silently break a core discovery path.

2. PRD-033 (`important`) Sync libraries/settings consistently and merge duplicates

The plan's uniqueness constraint helps avoid future duplicate records, but the PRD asks for duplicate items to be detected and merged transparently; without that, sync/import edge cases can leave repeated library entries or split My Data.

3. PRD-030 (`important`) Keep Ask and Alchemy state session-only

The plan clearly handles Alchemy as session-only but leaves Ask persistence ambiguous, which can create privacy, stale-context, and expectation problems if chat history is accidentally stored.

4. PRD-036 (`important`) Keep provider IDs persisted and detail fetches transient

The plan stores provider data but does not constrain it to provider IDs or identify transient detail fetches, risking bloated persisted records and stale public data.

5. PRD-082 (`important`) Generate shared multi-show concepts with larger option pool

Alchemy quality depends on giving users enough shared concept choices to steer the blend; the plan covers shared concepts but not the larger multi-show option pool.

### 5. Coverage Narrative

#### Overall Posture

This is a strong plan with minor but real gaps. It covers all critical requirements, most product flows, the infrastructure rider, the persistence model, and the AI voice system with enough specificity to guide implementation. The remaining issues are concentrated in reliability details, data-integrity edge cases, and navigation guarantees rather than fundamental architecture.

#### Strength Clusters

Coverage is strongest in Benchmark Runtime & Isolation, Show Detail & Relationship UX, AI Voice, Persona & Quality, Person Detail, and Settings & Export. The plan is especially concrete on Supabase/Next.js setup, namespace and user scoping, implicit save behaviors, detail-page ordering, Scoop states, concept recommendation contracts, and export.

#### Weakness Clusters

The weak spots cluster around operational edge contracts: Ask malformed-output handling, session-only persistence boundaries, transient catalog/detail storage, duplicate library merge behavior, and primary navigation persistence. A smaller product-detail gap is that tags are modeled but the free-form personal tag-library UX is not specified. These are mostly important-tier requirements that protect reliability and consistency after the happy path is built.

#### Risk Assessment

If executed as-is, the most likely failure mode is an app that looks complete but has brittle edges around AI and data consistency. QA would likely notice malformed Ask responses failing to populate mentioned-show tiles, Ask history sticking around longer than intended, duplicate saved items not merging cleanly, or Find/Settings being reachable by route but not consistently present in the shell.

#### Remediation Guidance

The plan needs a small round of acceptance-criteria tightening rather than a new architecture. Add explicit AI parser retry/fallback criteria, state which Ask and Alchemy objects are session-only and when they clear, define persisted-versus-transient catalog fields, specify duplicate detection/merge behavior, spell out free-form tag entry/library behavior, and make persistent primary navigation entries part of the shell contract.
