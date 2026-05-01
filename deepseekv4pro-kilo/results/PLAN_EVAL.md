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
| PRD-001 | Use Next.js latest stable runtime | critical | full | §1.1 Stack |  |
| PRD-002 | Use Supabase official client libraries | critical | full | §1.1 Stack |  |
| PRD-003 | Ship `.env.example` with required variables | critical | full | §1.2 Environment Configuration |  |
| PRD-004 | Ignore `.env*` secrets except example | important | full | §1.2 Environment Configuration |  |
| PRD-005 | Configure build through env without code edits | critical | full | §1.2 Environment Configuration |  |
| PRD-006 | Keep secrets out of repo and server-only | critical | full | §1.2 Environment Configuration; §11.1 Secrets |  |
| PRD-007 | Provide app, test, reset command scripts | critical | full | §1.3 One-Command DX |  |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | §1.4 Database; §6 Phase 1 item 3 |  |
| PRD-009 | Use one stable namespace per build | critical | full | §2.1 Namespace Isolation |  |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | §2.1 Namespace Isolation; §10.1 Isolation |  |
| PRD-011 | Attach every user record to `user_id` | critical | full | §2.2 User Identity |  |
| PRD-012 | Partition persisted data by namespace and user | critical | full | §2.2 User Identity |  |
| PRD-013 | Support documented dev auth injection, prod-gated | important | full | §2.2 User Identity; §7.2 Identity Injection |  |
| PRD-014 | Real OAuth later needs no schema redesign | important | full | §2.2 User Identity |  |
| PRD-015 | Keep backend as persisted source of truth | critical | full | §2.3 Data Ownership |  |
| PRD-016 | Make client cache safe to discard | critical | full | §2.3 Data Ownership |  |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | full | §1.1 Stack |  |
| PRD-018 | Overlay saved user data on every show appearance | critical | partial | §6 Phase 5 item 24; §6 Phase 6 item 29 | The plan covers overlays and badges in some surfaces, but it does not make merged user-overlay rendering an explicit rule for every show appearance, including AI strips and all recommendation contexts. |
| PRD-019 | Support visible statuses plus hidden `Next` | important | full | §4.1 shows table; §4.2 Auto-Save Triggers |  |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | full | §4.2 Auto-Save Triggers |  |
| PRD-021 | Support free-form multi-tag personal tag library | important | full | §6 item 22 Tag controls; §6 item 11 FilterPanel |  |
| PRD-022 | Define collection membership by assigned status | critical | full | §4.2 Collection Membership |  |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | full | §4.2 Auto-Save Triggers |  |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | §4.2 Auto-Save Triggers |  |
| PRD-025 | Removing status deletes show and all My Data | critical | full | §4.2 Removal |  |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | missing | none | The plan deletes the row on removal and never specifies any tombstone or restore path, so prior My Data is not preserved when the same show is added again. |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | §4.1 shows table update-date columns |  |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | partial | §4.2 Merge Policy; §5.3.2 AI Scoop; §10.3 Key Business Logic Tests | The plan uses timestamps for conflict resolution and Scoop freshness, but it never turns them into an explicit sorting policy. |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | full | §5.3.2 AI Scoop; §4.2 AI Data Persistence |  |
| PRD-030 | Keep Ask and Alchemy state session-only | important | full | §4.2 AI Data Persistence |  |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | full | §5.3.1 Ask; §5.3.5 Explore Similar; §5.3.6 Alchemy |  |
| PRD-032 | Show collection and rating tile indicators | important | full | §6 Phase 5 item 24 |  |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | partial | §4.1 cloud_settings; §8 Schema Evolution & Data Continuity | Cross-device storage is planned, but duplicate show detection and transparent merge behavior are not called out as explicit implementation work. |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | full | §8 Schema Evolution & Data Continuity; §6 item 37 |  |
| PRD-035 | Persist synced settings, local settings, UI state | important | partial | §4.1 cloud_settings; §6 item 35; §4.2 Removal | Cloud settings are planned, but explicit persisted structures for local settings and UI state, such as last filter selection, are not fully specified. |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | partial | §4.1 shows.provider_data; §6 item 27 | The plan persists provider data, but it does not explicitly define the broader transient-only treatment for credits, videos, seasons, and other detail fetches. |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | full | §4.2 Merge Policy |  |
| PRD-038 | Provide filters panel and main screen destinations | important | full | §6 items 10-12 |  |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | full | §6 item 12 Global navigation |  |
| PRD-040 | Keep Settings in persistent primary navigation | important | full | §6 item 12 Global navigation |  |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | §6 item 28 Find hub page |  |
| PRD-042 | Show only library items matching active filters | important | full | §6 item 13 CollectionHome |  |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | §6 item 14 StatusSections |  |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | full | §6 items 11 and 15 |  |
| PRD-045 | Render poster, title, and My Data badges | important | full | §6 Phase 5 item 24 |  |
| PRD-046 | Provide empty-library and empty-filter states | detail | full | §6 item 16 Empty states |  |
| PRD-047 | Search by title or keywords | important | full | §6 item 29 Search |  |
| PRD-048 | Use poster grid with collection markers | important | full | §6 item 29 Search |  |
| PRD-049 | Auto-open Search when setting is enabled | detail | full | §6 item 29 Search |  |
| PRD-050 | Keep Search non-AI in tone | important | full | §5.4 Voice & Persona |  |
| PRD-051 | Preserve Show Detail narrative section order | important | full | §6 Phase 5 items 17-27 |  |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | full | §6 item 18 Header carousel |  |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | full | §6 item 19 Core facts |  |
| PRD-054 | Place status/interest controls in toolbar | important | full | §6 item 20 Status controls |  |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | §6 item 22 Tag controls |  |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | §6 item 21 Rating bar |  |
| PRD-057 | Show overview early for fast scanning | important | full | §6 item 23 Overview + Scoop |  |
| PRD-058 | Scoop shows correct states and progressive feedback | important | full | §5.3.2 AI Scoop |  |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | full | §6 item 31 Ask About Show; §5.3.1 Ask |  |
| PRD-060 | Include traditional recommendations strand | important | full | §6 item 25 Traditional recommendations |  |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | full | §6 item 26 Explore Similar |  |
| PRD-062 | Include streaming availability and person-linking credits | important | full | §6 item 27 Streaming and CastCrew |  |
| PRD-063 | Gate seasons to TV and financials to movies | important | full | §6 item 27 Seasons and BudgetRevenue |  |
| PRD-064 | Keep primary actions early and page not overwhelming | important | partial | §6 Phase 5 item order | The sequence clusters primary actions early, but the plan never translates “not overwhelming” into a concrete layout or acceptance criterion. |
| PRD-065 | Provide conversational Ask chat interface | important | full | §5.3.1 Ask |  |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | full | §5.2 Shared AI Rules; §5.3.1 Ask |  |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | §5.3.1 Mentioned shows strip |  |
| PRD-068 | Open Detail from mentions or Search fallback | important | full | §5.3.1 Search handoff |  |
| PRD-069 | Show six random starter prompts with refresh | important | full | §5.3.1 Starter prompts |  |
| PRD-070 | Summarize older turns while preserving voice | important | full | §5.3.1 summarize older turns |  |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | full | §5.3.1 Ask About a Show |  |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | full | §5.3.1 `commentary` + `showList` contract |  |
| PRD-073 | Retry malformed mention output once, then fallback | important | full | §5.3.1 retry once then fallback |  |
| PRD-074 | Redirect Ask back into TV/movie domain | important | full | §5.2 Shared AI Rules |  |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | full | §5.3.3 Get Concepts rules |  |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | full | §5.3.3 Get Concepts rules |  |
| PRD-077 | Order concepts by strongest aha and varied axes | important | full | §5.3.3 Get Concepts rules |  |
| PRD-078 | Require concept selection and guide ingredient picking | important | partial | §6 item 26; §6 item 32 | The plan requires concept selection, but it omits the guidance and empty-state cues that teach users to pick the ingredients they want more of. |
| PRD-079 | Return exactly five Explore Similar recommendations | important | full | §5.3.5 Explore Similar recommendations |  |
| PRD-080 | Support full Alchemy loop with chaining | important | full | §6 item 32 Alchemy; §5.3.6 Alchemy recs |  |
| PRD-081 | Clear downstream results when inputs change | important | missing | none | The plan never specifies clearing concepts or recommendation results when input shows or selected concepts change, which risks stale downstream state. |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | full | §5.3.4 Multi-show concepts |  |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | full | §5.3.5 Explore Similar recommendations |  |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | partial | §5.3.5 Explore Similar; §5.3.6 Alchemy | The plan targets taste-aware recommendations, but it does not encode the product bar for surprising yet defensible picks as an explicit requirement or test. |
| PRD-085 | Keep one consistent AI persona across surfaces | important | full | §5.4 Voice & Persona |  |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | full | §5.2 Shared AI Rules |  |
| PRD-087 | Make AI warm, joyful, and light in critique | important | full | §5.4 Voice & Persona |  |
| PRD-088 | Structure Scoop as personal taste mini-review | important | full | §5.3.2 AI Scoop |  |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | full | §5.3.1 Ask |  |
| PRD-090 | Feed AI the right surface-specific context inputs | important | full | §7.3 AI Routes — Context Assembly |  |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | partial | §10.3 Key Business Logic Tests; §5.3.5 and §5.3.6 | The plan covers some fallback cases, but it does not adopt the discovery rubric or a hard-fail validation gate for real-show integrity and taste quality. |
| PRD-092 | Show person gallery, name, and bio | important | full | §6 item 33 PersonShell |  |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | full | §6 item 33 PersonShell |  |
| PRD-094 | Group filmography by year | important | full | §6 item 33 PersonShell |  |
| PRD-095 | Open Show Detail from selected credit | important | full | §6 item 34 Credit links |  |
| PRD-096 | Include font size and Search-on-launch settings | important | full | §6 item 35 Settings page |  |
| PRD-097 | Support username, model, and API-key settings safely | important | full | §6 item 35; §11.1 Secrets |  |
| PRD-098 | Export saved shows and My Data as zip | critical | full | §6 item 36; §9.1 Export Format |  |
| PRD-099 | Encode export dates using ISO-8601 | important | full | §9.1 Export Format |  |

### 3. Coverage Scores

Overall score:

```
score = (88 × 1.0 + 9 × 0.5) / 99 × 100 = 93.43%
```

Score by severity tier:

```
Critical:  (28 × 1.0 + 1 × 0.5) / 30 × 100 = 95.00%  (28.5 of 30 critical requirements)
Important: (58 × 1.0 + 8 × 0.5) / 67 × 100 = 92.54%  (62.0 of 67 important requirements)
Detail:    (2 × 1.0 + 0 × 0.5) / 2 × 100 = 100.00%  (2.0 of 2 detail requirements)
Overall:   93.43% (99 total requirements)
```

### 4. Top Gaps

- PRD-026 | `critical` | Re-add preserves My Data and refreshes public data — Executing the removal flow as planned would wipe the user’s relationship history for a show, so re-adding it later would feel like data loss rather than a reversible library action.
- PRD-018 | `critical` | Overlay saved user data on every show appearance — If some surfaces render raw catalog objects while others render user-overlaid ones, the app will present contradictory statuses, ratings, and saved-state cues for the same show.
- PRD-081 | `important` | Clear downstream results when inputs change — Without explicit downstream invalidation, Alchemy and Explore Similar can show stale concepts or recommendations after the user changes inputs, which breaks trust in the flow.
- PRD-091 | `important` | Validate discovery with rubric and hard-fail integrity — The AI surfaces may ship with acceptable plumbing but no measurable bar for taste alignment or integrity, leaving QA unable to catch subtle but user-visible recommendation failures.
- PRD-033 | `important` | Sync libraries/settings consistently and merge duplicates — Cross-device usage will eventually create duplicate and conflict scenarios, and the plan does not yet define the merge behavior tightly enough to avoid inconsistent libraries or settings.

### 5. Coverage Narrative

#### Overall Posture

This is a strong plan with high structural coverage and a credible implementation sequence, but it is not fully execution-ready because a small set of product-behavior contracts remain underspecified. The biggest issues are not missing infrastructure; they are cross-surface data consistency, state invalidation, and one critical data-lifecycle requirement around re-adding shows.

#### Strength Clusters

The plan is strongest in Benchmark Runtime & Isolation, App Navigation & Discover Shell, Ask Chat, Show Detail & Relationship UX, and Settings & Export. Those areas have explicit architecture, concrete implementation phases, and specific behavioral contracts that map cleanly back to the PRD.

#### Weakness Clusters

The gaps cluster around cross-cutting behavioral fidelity rather than foundational scaffolding. Collection Data & Persistence has the most consequential misses, while Concepts, Explore Similar & Alchemy and AI Voice, Persona & Quality are mostly present structurally but under-specified at the edges where stale state, recommendation quality, and evaluation rigor matter.

#### Risk Assessment

If this plan were executed as-is, QA would most likely find that the app basically works but feels inconsistent in the places users notice quickly: a removed-and-re-added show loses history, some surfaces may not show the same saved-state overlay, and Alchemy-style flows can retain stale downstream results after inputs change. Stakeholders would also notice that the AI stack has delivery plumbing but no hard acceptance gate for recommendation quality or real-show integrity beyond partial checks.

#### Remediation Guidance

The plan needs tighter behavioral specification more than new architecture. The missing work is to define explicit cross-surface overlay contracts, spell out data-lifecycle rules for removal and re-add, add deterministic state-reset rules for concept-driven flows, and introduce measurable AI quality and integrity acceptance criteria that QA can enforce before release.
