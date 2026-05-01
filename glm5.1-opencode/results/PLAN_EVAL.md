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
| PRD-001 | Use Next.js latest stable runtime | critical | full | `Overview`; `1.1 Repo Scaffolding` | |
| PRD-002 | Use Supabase official client libraries | critical | full | `Overview`; `5.1 App Structure`: `lib/supabase` | |
| PRD-003 | Ship `.env.example` with required variables | critical | full | `1.1 Repo Scaffolding` | |
| PRD-004 | Ignore `.env*` secrets except example | important | full | `1.1 Repo Scaffolding` | |
| PRD-005 | Configure build through env without code edits | critical | partial | `1.1 Repo Scaffolding` | The plan defines the environment surface, but it never explicitly commits to running the build solely by changing env values instead of editing source. |
| PRD-006 | Keep secrets out of repo and server-only | critical | full | `1.1 Repo Scaffolding`; `9. Security` | |
| PRD-007 | Provide app, test, reset command scripts | critical | full | `1.1 Repo Scaffolding` | |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | `1.2 Supabase Setup`; `2.5 Migrations` | |
| PRD-009 | Use one stable namespace per build | critical | full | `1.3 Namespace & Identity` | |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | `1.2 Supabase Setup`; `3.4 Settings & Data Routes`; `9. Testing` | |
| PRD-011 | Attach every user record to `user_id` | critical | full | `1.3 Namespace & Identity` | |
| PRD-012 | Partition persisted data by namespace and user | critical | full | `2.1 Database Tables`; `3.5 Identity Middleware` | |
| PRD-013 | Support documented dev auth injection, prod-gated | important | partial | `1.3 Namespace & Identity`; `3.5 Identity Middleware` | The injection mechanisms and production gating are planned, but there is no explicit operator-facing documentation task for benchmark users. |
| PRD-014 | Real OAuth later needs no schema redesign | important | full | `1.3 Namespace & Identity` | |
| PRD-015 | Keep backend as persisted source of truth | critical | full | `7. Key Business Rules Summary` | |
| PRD-016 | Make client cache safe to discard | critical | full | `5.2 State Management`; `7. Key Business Rules Summary` | |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | full | `Overview`; `1.2 Supabase Setup` | |
| PRD-018 | Overlay saved user data on every show appearance | critical | full | `5.3 useShow(id)`; `7. Key Business Rules Summary` | |
| PRD-019 | Support visible statuses plus hidden `Next` | important | partial | `2.1 Database Tables`: `my_status` includes `next`; `10. Open Items` | The schema preserves `next`, but the plan does not specify how the hidden/non-primary status behaves in the current UI. |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | full | `3.2 Collection CRUD` | |
| PRD-021 | Support free-form multi-tag personal tag library | important | full | `2.1 Database Tables`; `Phase 2` item 8 | |
| PRD-022 | Define collection membership by assigned status | critical | full | `7. Key Business Rules Summary` | |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | full | `3.2 Collection CRUD` | |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | `3.2 Collection CRUD`; `7. Key Business Rules Summary` | |
| PRD-025 | Removing status deletes show and all My Data | critical | full | `3.2 Collection CRUD`; `7. Key Business Rules Summary` | |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | full | `Phase 6` item 27; `7. Key Business Rules Summary` | |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | `2.1 Database Tables` | |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | partial | `2.3 Merge Rules`; `4.5 Cache & Freshness` | Timestamp fields are planned for merging and freshness, but their use in sorting and broader sync flows is not concretely specified. |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | full | `4.5 Cache & Freshness` | |
| PRD-030 | Keep Ask and Alchemy state session-only | important | full | `2.4 Transient Data`; `4.5 Cache & Freshness` | |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | full | `3.3 AI Routes`; `4.4 AI Recommendation → Real Show Resolution` | |
| PRD-032 | Show collection and rating tile indicators | important | full | `Phase 2` item 9 | |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | partial | `2.1 cloud_settings`; `2.3 Merge Rules` | Synced settings and timestamps are present, but duplicate detection and concrete cross-device library merge behavior are left underspecified. |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | full | `2.5 Migrations`; `9. Data Continuity` | |
| PRD-035 | Persist synced settings, local settings, UI state | important | full | `2.1 cloud_settings`; `2.2 Local/Client Settings` | |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | full | `2.1 shows.provider_data`; `2.4 Transient Data` | |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | full | `2.3 Merge Rules` | |
| PRD-038 | Provide filters panel and main screen destinations | important | full | `5.1 App Structure`; `Phase 1` item 5 | |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | full | `5.1 App Structure`; `Phase 1` item 5 | |
| PRD-040 | Keep Settings in persistent primary navigation | important | full | `5.1 App Structure`; `Phase 1` item 5 | |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | `5.1 App Structure` | |
| PRD-042 | Show only library items matching active filters | important | full | `5.3 useCollection(filter?)`; `Phase 2` item 8 | |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | `Phase 2` item 7 | |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | full | `Phase 2` item 8 | |
| PRD-045 | Render poster, title, and My Data badges | important | full | `Phase 2` item 9 | |
| PRD-046 | Provide empty-library and empty-filter states | detail | full | `Phase 6` item 25 | |
| PRD-047 | Search by title or keywords | important | full | `3.1 GET /api/catalog/search`; `Phase 4` item 18 | |
| PRD-048 | Use poster grid with collection markers | important | full | `Phase 4` item 18 | |
| PRD-049 | Auto-open Search when setting is enabled | detail | partial | `2.2 Local/Client Settings`; `Phase 5` item 23 | The setting is stored, but the launch-time behavior that automatically opens Search is not explicitly planned. |
| PRD-050 | Keep Search non-AI in tone | important | full | `8. AI Voice & Quality Contract` | |
| PRD-051 | Preserve Show Detail narrative section order | important | partial | `Phase 3` items 10-17 | The plan lists the Detail components, but it does not preserve the PRD's exact narrative ordering, especially Ask and Explore Similar placement. |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | partial | `Phase 3` item 10 | Motion media is planned, but graceful fallback behavior for shows without trailers/backdrops is not called out. |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | full | `Phase 3` item 10 | |
| PRD-054 | Place status/interest controls in toolbar | important | partial | `Phase 3` item 11 | The relationship controls exist, but the plan does not explicitly place status/interest chips in the toolbar. |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | `3.2 Collection CRUD`; `Phase 3` item 11 | |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | `3.2 Collection CRUD`; `Phase 3` item 11 | |
| PRD-057 | Show overview early for fast scanning | important | partial | `Phase 3` item 12 | Overview content is planned, but its "show it early and make it scannable" requirement is not expressed as a layout rule. |
| PRD-058 | Scoop shows correct states and progressive feedback | important | partial | `4.5 Cache & Freshness`; `Phase 3` item 12 | Generation, caching, and streaming are covered, but the plan omits the distinct no-scoop, cached, and open states plus their progressive feedback copy. |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | full | `Phase 3` item 17; `4.2 Context Assembly` | |
| PRD-060 | Include traditional recommendations strand | important | full | `Phase 3` item 13 | |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | full | `Phase 4` item 20 | |
| PRD-062 | Include streaming availability and person-linking credits | important | full | `Phase 3` items 14-15 | |
| PRD-063 | Gate seasons to TV and financials to movies | important | full | `Phase 3` item 16 | |
| PRD-064 | Keep primary actions early and page not overwhelming | important | partial | `Phase 3` items 10-17 | The plan enumerates sections, but it does not translate the anti-busyness requirement into concrete layout or prioritization guidance. |
| PRD-065 | Provide conversational Ask chat interface | important | full | `Phase 4` item 19 | |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | full | `4.1 Ask prompt`; `8. AI Voice & Quality Contract` | |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | `Phase 4` item 19 | |
| PRD-068 | Open Detail from mentions or Search fallback | important | full | `Phase 4` item 19; `4.4 AI Recommendation → Real Show Resolution` | |
| PRD-069 | Show six random starter prompts with refresh | important | partial | `Phase 4` item 19 | Starter prompts are mentioned, but the plan does not commit to six random prompts plus refresh behavior. |
| PRD-070 | Summarize older turns while preserving voice | important | full | `4.1 Ask prompt`; `4.2 Context Assembly` | |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | full | `Phase 3` item 17; `4.2 Context Assembly` | |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | full | `3.3 AI Routes`; `4.3 Structured Output & Parsing` | |
| PRD-073 | Retry malformed mention output once, then fallback | important | full | `4.3 Structured Output & Parsing` | |
| PRD-074 | Redirect Ask back into TV/movie domain | important | partial | `4.1 Prompt Architecture`; `8. AI Voice & Quality Contract` | The plan captures the persona, but it does not explicitly require redirecting off-topic Ask requests back into the TV/movie domain. |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | partial | `4.1 Concepts prompt`; `8. Key voice rules` | The concepts prompt emphasizes evocative brevity, but it never explicitly states that concepts are taste ingredients rather than genres. |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | full | `4.1 Concepts prompt` | |
| PRD-077 | Order concepts by strongest aha and varied axes | important | full | `8. Key voice rules` | |
| PRD-078 | Require concept selection and guide ingredient picking | important | partial | `Phase 4` item 20; `4.1 Concepts prompt` | Concept selection is planned, but the UI guidance that teaches users to pick ingredient-like concepts is missing. |
| PRD-079 | Return exactly five Explore Similar recommendations | important | full | `4.1 Recommendations prompt` | |
| PRD-080 | Support full Alchemy loop with chaining | important | full | `Phase 4` item 21 | |
| PRD-081 | Clear downstream results when inputs change | important | partial | `Phase 4` item 21 | The Alchemy loop is planned, but the state-reset rule when users change inputs is not explicit. |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | partial | `4.1 Concepts prompt` | The plan requires shared multi-show concepts, but it does not call for a larger option pool than single-show concept generation. |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | full | `4.1 Recommendations prompt` | |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | full | `8. AI Voice & Quality Contract` | |
| PRD-085 | Keep one consistent AI persona across surfaces | important | full | `4.1 Prompt Architecture` | |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | partial | `4.1 Base personality`; `8. AI Voice & Quality Contract` | The plan captures several AI principles, but it does not consolidate or enforce the full shared guardrail set across every AI surface. |
| PRD-087 | Make AI warm, joyful, and light in critique | important | full | `4.1 Base personality` | |
| PRD-088 | Structure Scoop as personal taste mini-review | important | full | `4.1 Scoop prompt` | |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | full | `4.1 Ask prompt` | |
| PRD-090 | Feed AI the right surface-specific context inputs | important | full | `4.2 Context Assembly`; `3.3 AI Routes` | |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | partial | `8. AI Voice & Quality Contract` | The rubric is quoted, but the plan never specifies where evaluation runs or how integrity failures block regressions or releases. |
| PRD-092 | Show person gallery, name, and bio | important | partial | `Phase 5` item 22 | The page content implies identity basics, but the plan never explicitly calls out displaying the person's name. |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | partial | `Phase 5` item 22 | Analytics are mentioned generically, but the plan does not commit to ratings, genres, and projects-by-year views. |
| PRD-094 | Group filmography by year | important | full | `Phase 5` item 22 | |
| PRD-095 | Open Show Detail from selected credit | important | full | `Phase 5` item 22 | |
| PRD-096 | Include font size and Search-on-launch settings | important | full | `2.2 Local/Client Settings`; `Phase 5` item 23 | |
| PRD-097 | Support username, model, and API-key settings safely | important | full | `Phase 5` item 23; `9. Security` | |
| PRD-098 | Export saved shows and My Data as zip | critical | full | `3.4 GET /api/data/export`; `Phase 5` item 24 | |
| PRD-099 | Encode export dates using ISO-8601 | important | full | `Phase 5` item 24 | |

## 3. Coverage Scores

Critical:  (28 × 1.0 + 2 × 0.5) / 30 × 100 = 96.67%  (29.0 of 30 critical requirements)
Important: (48 × 1.0 + 19 × 0.5) / 67 × 100 = 85.82%  (57.5 of 67 important requirements)
Detail:    (1 × 1.0 + 1 × 0.5) / 2 × 100 = 75.00%  (1.5 of 2 detail requirements)
Overall:   (77 × 1.0 + 22 × 0.5) / 99 × 100 = 88.89%  (88.0 of 99 requirements)

## 4. Top Gaps

1. PRD-086 | `critical` | Enforce shared AI guardrails across all surfaces
The plan states several AI principles, but it never turns the full shared rule set into an explicit cross-surface enforcement contract. Without that, Ask, Scoop, Concepts, and recommendation flows can drift on domain boundaries, spoiler handling, and honesty/persona consistency.

2. PRD-005 | `critical` | Configure build through env without code edits
The plan defines the variables but stops short of explicitly requiring environment-only reconfiguration. That leaves room for per-run source edits, which undermines repeatable benchmark setup and makes operator handoff brittle.

3. PRD-033 | `important` | Sync libraries/settings consistently and merge duplicates
The plan includes synced settings and timestamp-based merges, but not a concrete duplicate-detection or cross-device merge flow. If implemented loosely, users can see inconsistent libraries or duplicated items, which directly erodes trust in saved data.

4. PRD-051 | `important` | Preserve Show Detail narrative section order
The plan covers most Detail subfeatures, but it does not preserve the intended storytelling order of the page. That matters because the PRD treats the Detail screen as the product's emotional and functional centerpiece, not just a bucket of sections.

5. PRD-091 | `important` | Validate discovery with rubric and hard-fail integrity
The quality rubric is quoted, but the plan does not say how or where it will be enforced. Without a concrete validation gate, hallucinated titles or off-brand AI behavior can regress silently even if the core app ships.

## 5. Coverage Narrative

#### Overall Posture

This is a structurally strong plan with a high-coverage backbone, especially on runtime constraints, persistence, and the main feature set. The main weakness is not missing product areas outright, but underspecifying the product-feel and AI-behavior contracts that make this app faithful to the PRD rather than merely functional.

#### Strength Clusters

The strongest coverage is in Benchmark Runtime & Isolation and Collection Data & Persistence: namespace/user partitioning, migrations, reset flows, timestamps, autosave triggers, and export are all concretely planned. App Navigation & Discover Shell, most of Collection Home & Search, and most of Ask Chat are also well covered with explicit routes, APIs, and implementation phases.

#### Weakness Clusters

The partials cluster around two patterns. One is craft-level UX behavior in Show Detail and discovery flows: exact section order, toolbar placement, scoop states, starter-prompt specifics, and concept-guidance copy. The other is AI behavioral governance: shared guardrails, domain redirection, discovery validation, and concept semantics are present in spirit but not fully locked down as explicit contracts.

#### Risk Assessment

If this plan were executed as-is, the app would likely work end-to-end and store data correctly, but it could feel noticeably off-spec in the places users and reviewers care about most. QA would probably first flag the Detail page rhythm and AI behavior: the screen could have the right components in the wrong order, and the AI could sound close to the intended persona while still drifting on domain boundaries, guardrails, or quality enforcement.

#### Remediation Guidance

The remaining planning work is mostly about tightening acceptance criteria, not inventing new subsystems. The plan needs explicit behavioral specs for the Detail page layout/order, Ask starter-prompt behavior, concept UX guidance, and Search-on-launch behavior; a single shared AI contract that applies across surfaces; and concrete sync/duplicate-merge and benchmark-operator documentation so the strong architecture is matched by equally strong execution constraints.
