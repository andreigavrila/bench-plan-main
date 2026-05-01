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
| PRD-001 | Use Next.js latest stable runtime | critical | full | `§2.1 Technology Decisions`; `Phase 1.1` |  |
| PRD-002 | Use Supabase official client libraries | critical | full | `§2.1 Technology Decisions`; `§10 src/lib/supabase/` |  |
| PRD-003 | Ship `.env.example` with required variables | critical | full | `§5.1 Identity & Isolation` env block; `Phase 1.3` |  |
| PRD-004 | Ignore `.env*` secrets except example | important | partial | `Phase 1.3` "Create `.env.example`, `.gitignore`" | Plan never states the `.gitignore` rule must exclude `.env*` while preserving `.env.example`. |
| PRD-005 | Configure build through env without code edits | critical | full | `§5.1 Identity & Isolation`; `Acceptance Criteria 1` |  |
| PRD-006 | Keep secrets out of repo and server-only | critical | full | `§5.1` server-only comments; `§9` AI API keys server-only |  |
| PRD-007 | Provide app, test, reset command scripts | critical | full | `Phase 1.9`; `Acceptance Criteria 1` |  |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | `§3.1 Database Tables`; `Phase 1.2`; `Phase 1.10` |  |
| PRD-009 | Use one stable namespace per build | critical | full | `§5.1 Namespace isolation`; env `NAMESPACE_ID` |  |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | `§5.1 Namespace isolation`; `Phase 5.4`; `Phase 5.6` |  |
| PRD-011 | Attach every user record to `user_id` | critical | full | `§3.1 Database Tables` (`shows`, `cloud_settings`); `§5.1` |  |
| PRD-012 | Partition persisted data by namespace and user | critical | full | `§3.1` composite namespace/user schema; RLS policies |  |
| PRD-013 | Support documented dev auth injection, prod-gated | important | full | `§5.1 User identity (dev mode)`; `Acceptance Criteria 7` |  |
| PRD-014 | Real OAuth later needs no schema redesign | important | full | `§5.1` "replace with real OAuth ... without schema changes" |  |
| PRD-015 | Keep backend as persisted source of truth | critical | full | `§2.1 Technology Decisions` "server as truth"; `§9` SWR rationale |  |
| PRD-016 | Make client cache safe to discard | critical | full | `§2.1 State Management`; `§9` "cache is disposable" rationale |  |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | partial | `§2.1 Technology Decisions`; `Phase 1.2` | The plan picks hosted-friendly components but never explicitly commits to Docker remaining optional or unnecessary. |
| PRD-018 | Overlay saved user data on every show appearance | critical | partial | `§4.2.1 Search` "overlay My Data" | Overlay behavior is explicit for search but not for every appearance such as recommendations, mentions, and other list surfaces. |
| PRD-019 | Support visible statuses plus hidden `Next` | important | full | `§3.1 shows.my_status` includes `next`; `§4.3 StatusControls` omits it from visible chips |  |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | full | `§4.3 StatusControls`; `§5.4 Saving triggers` |  |
| PRD-021 | Support free-form multi-tag personal tag library | important | full | `§4.3 TagManager`; `§4.1 FilterPanel` tag filters |  |
| PRD-022 | Define collection membership by assigned status | critical | full | `§4.1 Data flow` `my_status IS NOT NULL` |  |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | full | `§5.4 Saving triggers` |  |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | `§5.4 Default values` |  |
| PRD-025 | Removing status deletes show and all My Data | critical | full | `§4.3 Auto-save behaviors`; `§5.4 Removal` |  |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | full | `§5.4 Re-adding` |  |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | `§3.1 shows` update-date columns |  |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | full | `§4.1` sorting; `§5.2` merge rules; `§4.3` Scoop freshness |  |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | full | `§4.3 Scoop behavior` |  |
| PRD-030 | Keep Ask and Alchemy state session-only | important | full | `§3.3 Transient Data`; `§4.2.2`/`§4.2.3` session language |  |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | full | `§4.2.2` mention resolution; `§4.2.3` "Each rec must map to real catalog item" |  |
| PRD-032 | Show collection and rating tile indicators | important | partial | `§4.1 Show tiles display`; `§4.2.1` in-collection markers | The plan clearly covers badges on home tiles but does not consistently specify both indicators across all poster-grid surfaces. |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | partial | `§3.1 cloud_settings`; `Phase 4.10`; `§5.4 Re-adding` | Settings sync is planned, but collection sync and duplicate-merge behavior are not explicitly designed. |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | partial | `§3.1 app_metadata`; `Phase 1.2` migrations | The plan tracks schema versioning, but it does not define upgrade-time migration behavior that guarantees preserving saved libraries and My Data. |
| PRD-035 | Persist synced settings, local settings, UI state | important | full | `§3.1 cloud_settings`; `§3.2 Local Settings` |  |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | partial | `§3.1 provider_data JSONB`; `§3.3 Transient Data` | Provider persistence exists and detail fetches are transient, but the plan never constrains persistence to provider IDs only. |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | full | `§5.2 Catalog Integration` merge rules |  |
| PRD-038 | Provide filters panel and main screen destinations | important | full | `§4.1 Collection Home`; `§4.2`/`§4.3`/`§4.4`/`§4.5` routes and pages |  |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | partial | `Phase 1.7` page shells; `§4.2 Find/Discover Hub` | The route exists, but the plan does not explicitly place Find/Discover in persistent primary navigation. |
| PRD-040 | Keep Settings in persistent primary navigation | important | partial | `Phase 1.7` page shells; `§4.5 Settings Page` | The plan defines the page but not its persistent primary-navigation placement. |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | `§4.2 Find/Discover Hub` mode switcher tabs |  |
| PRD-042 | Show only library items matching active filters | important | full | `§4.1 Behavior/Data flow` |  |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | `§4.1 StatusSections` |  |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | full | `§4.1 FilterPanel` |  |
| PRD-045 | Render poster, title, and My Data badges | important | full | `§4.1 Show tiles display` |  |
| PRD-046 | Provide empty-library and empty-filter states | detail | full | `§4.1 Empty states` |  |
| PRD-047 | Search by title or keywords | important | full | `§4.2.1 Search` |  |
| PRD-048 | Use poster grid with collection markers | important | full | `§4.2.1 Search` |  |
| PRD-049 | Auto-open Search when setting is enabled | detail | full | `§4.2.1 Search`; `§4.5 App settings` |  |
| PRD-050 | Keep Search non-AI in tone | important | partial | `§4.2.1 Search` catalog-search scope | The plan implements Search as a catalog feature but never explicitly preserves its non-AI tone/behavior contract. |
| PRD-051 | Preserve Show Detail narrative section order | important | partial | `§4.3 Sections (in order)` | The listed order diverges from the required narrative hierarchy by inserting status and rating ahead of tags and overview. |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | full | `§4.3 HeaderMedia`; `Phase 4.6` |  |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | full | `§4.3 CoreFacts` |  |
| PRD-054 | Place status/interest controls in toolbar | important | full | `§4.3 StatusControls` |  |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | `§4.3 TagManager` |  |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | `§4.3 RatingControl` |  |
| PRD-057 | Show overview early for fast scanning | important | full | `§4.3 OverviewAndScoop` |  |
| PRD-058 | Scoop shows correct states and progressive feedback | important | full | `§4.3 Scoop behavior`; `§9` streaming rationale |  |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | full | `§4.3 AskAboutShow`; `§4.2.2` variant |  |
| PRD-060 | Include traditional recommendations strand | important | full | `§4.3 Recommendations` |  |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | full | `§4.3 ExploreSimilar` |  |
| PRD-062 | Include streaming availability and person-linking credits | important | full | `§4.3 StreamingProviders`; `§4.3 CastCrew` |  |
| PRD-063 | Gate seasons to TV and financials to movies | important | full | `§4.3 Seasons`; `§4.3 BudgetRevenue` |  |
| PRD-064 | Keep primary actions early and page not overwhelming | important | partial | `§4.3 Sections (in order)` | The plan enumerates the sections, but it does not add layout or acceptance guidance that protects the page from becoming too busy. |
| PRD-065 | Provide conversational Ask chat interface | important | full | `§4.2.2 Ask (Chat)` |  |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | partial | `§4.2.2 Ask`; `§5.3 AI persona consistency` | Tone and safety are covered, but the plan does not explicitly require direct-answer-first, confident recommendation formatting. |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | `§4.2.2 MentionedShows` |  |
| PRD-068 | Open Detail from mentions or Search fallback | important | full | `§4.2.2` mention resolution and fallback |  |
| PRD-069 | Show six random starter prompts with refresh | important | full | `§4.2.2 StarterPrompts` |  |
| PRD-070 | Summarize older turns while preserving voice | important | full | `§4.2.2 Conversation management` |  |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | full | `§4.2.2` ask-about-show variant |  |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | full | `§4.2.2 Response` exact `{ commentary, showList }` format |  |
| PRD-073 | Retry malformed mention output once, then fallback | important | full | `§5.3` retry-on-failure fallback |  |
| PRD-074 | Redirect Ask back into TV/movie domain | important | full | `§5.3 Guardrails` |  |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | partial | `§4.2.3 ConceptChips`; `§5.3 Concepts (single)` | Concepts are implemented, but the plan never states the product rule that they are ingredient-like taste descriptors rather than genres. |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | partial | `§5.3 AI surfaces`; `Phase 5.2` concept parsing tests | The format is specified, but the non-generic quality constraint is not. |
| PRD-077 | Order concepts by strongest aha and varied axes | important | missing | none | The plan never defines ordering or diversity requirements for returned concepts. |
| PRD-078 | Require concept selection and guide ingredient picking | important | partial | `§4.2.3 ConceptChips`; `§4.3 ExploreSimilar` | Selection is planned, but the ingredient-picking guidance and explicit nudges for empty states are missing. |
| PRD-079 | Return exactly five Explore Similar recommendations | important | full | `§4.3 ExploreSimilar` "(5 AI recs)" |  |
| PRD-080 | Support full Alchemy loop with chaining | important | full | `§4.2.3 Alchemy`; `Phase 3.7` |  |
| PRD-081 | Clear downstream results when inputs change | important | missing | none | The plan never says changing shows or selected concepts clears previously generated concepts and results. |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | partial | `§4.2.3 ShowSelector` 2+ shows; concepts route | Multi-show concept generation is implied, but the shared-commonality rule and larger option pool are not specified. |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | partial | `§4.2.3 RecommendationResults` reasons | The plan asks for reasons, but not for explicit concept citation inside those reasons. |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | partial | `§5.3 Guardrails`; `Acceptance Criteria 8` | Taste-awareness is present, but the plan does not set the surprise-without-betrayal bar for discovery quality. |
| PRD-085 | Keep one consistent AI persona across surfaces | important | full | `§5.3 AI persona consistency` |  |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | full | `§5.3 Guardrails` |  |
| PRD-087 | Make AI warm, joyful, and light in critique | important | full | `§5.3 AI persona consistency` |  |
| PRD-088 | Structure Scoop as personal taste mini-review | important | partial | `§5.3 AI surfaces` structured "mini blog post" text | The plan identifies Scoop as a mini blog post, but it does not lock in the concrete personal-taste review structure behind that experience. |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | partial | `§4.2.2 Ask`; `§5.3 AI persona consistency` | The plan covers chat infrastructure and tone, but not the default short, dialogue-like response shape. |
| PRD-090 | Feed AI the right surface-specific context inputs | important | full | `§5.3 AI surfaces and their contracts`; `§4.2.2` request contents |  |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | partial | `Phase 5.2`; `Phase 5.7` | The plan tests parser integrity, but it does not adopt the discovery quality rubric or make real-show integrity a separate hard-fail validation gate. |
| PRD-092 | Show person gallery, name, and bio | important | full | `§4.4 Person Detail Page` |  |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | full | `§4.4 AnalyticsCharts` |  |
| PRD-094 | Group filmography by year | important | full | `§4.4 Filmography` |  |
| PRD-095 | Open Show Detail from selected credit | important | full | `§4.4` each credit links to Show Detail |  |
| PRD-096 | Include font size and Search-on-launch settings | important | full | `§4.5 App settings`; `§3.2 Local Settings` |  |
| PRD-097 | Support username, model, and API-key settings safely | important | full | `§4.5 User`; `§4.5 AI settings`; `§5.1` server-only env keys |  |
| PRD-098 | Export saved shows and My Data as zip | critical | full | `§4.5 Your Data`; `Phase 4.9`; `Acceptance Criteria 6` |  |
| PRD-099 | Encode export dates using ISO-8601 | important | full | `§4.5 Your Data`; `§5.5 Export/Backup` |  |

## 3. Coverage Scores

Overall score:

`score = (75 × 1.0 + 22 × 0.5) / 99 × 100 = 86.9%`

Critical:  `(28 × 1.0 + 2 × 0.5) / 30 × 100 = 96.7%`  (29 of 30 critical requirements)
Important: `(45 × 1.0 + 20 × 0.5) / 67 × 100 = 82.1%`  (55 of 67 important requirements)
Detail:    `(2 × 1.0 + 0 × 0.5) / 2 × 100 = 100.0%`  (2 of 2 detail requirements)
Overall:   `86.9%` (99 total requirements)

## 4. Top Gaps

- PRD-018 | `critical` | Overlay saved user data on every show appearance. This matters because the product promise is that the user's version of a show wins everywhere; if some surfaces show raw catalog data instead, state feels inconsistent and users lose trust in saves, tags, and ratings.
- PRD-034 | `critical` | Preserve saved libraries across data-model upgrades. This matters because schema evolution without an explicit continuity plan can silently strand or erase the core asset of the app: the user's library and My Data.
- PRD-051 | `important` | Preserve Show Detail narrative section order. This matters because Detail is the main decision surface, and changing the sequence weakens the intended "orient, relate, discover" flow that the supporting UX spec treats as essential.
- PRD-091 | `important` | Validate discovery with rubric and hard-fail integrity. This matters because AI discovery can appear to work while drifting into generic, low-trust, or unresolved recommendations unless quality checks are planned as first-class acceptance criteria.
- PRD-081 | `important` | Clear downstream results when inputs change. This matters because stale concepts or stale recommendation results make the Alchemy and Explore Similar flows feel broken and can surface recommendations that no longer match the user's current selections.

## 5. Coverage Narrative

#### Overall Posture

This is a structurally sound plan with strong infrastructure and data-model coverage, but it still has meaningful holes in behavioral fidelity. It would likely produce a working app, yet some of the most product-defining requirements around cross-surface consistency, Detail-page storytelling, and AI discovery quality are only partially specified.

#### Strength Clusters

The plan is strongest in Benchmark Runtime & Isolation and Collection Data & Persistence. It also covers the broad shape of Collection Home & Search, Person Detail, and Settings & Export well. The backend boundaries, schema, namespace and user partitioning, save/remove defaults, export path, and most surface routing are concrete enough to execute.

#### Weakness Clusters

The gaps cluster around important-tier experience requirements rather than base plumbing. App Navigation & Discover Shell, Show Detail & Relationship UX, Concepts/Explore Similar & Alchemy, and AI Voice, Persona & Quality all show the same pattern: the plan names the feature, but it underspecifies the qualitative contract, interaction constraints, or acceptance bar that makes the rebuilt product feel like the PRD instead of merely resembling it.

#### Risk Assessment

If this plan were executed as-is, the first thing a stakeholder or QA reviewer would notice is not missing infrastructure but a product that feels slightly off. Search and navigation could be functionally present without the intended shell behavior, the Detail page could land in the wrong narrative order, and the AI surfaces could return generic or stale-feeling concept/recommendation flows because the plan treats them more as endpoints to build than behaviors to preserve.

#### Remediation Guidance

The remaining planning work is mostly specification tightening, not wholesale re-architecture. The plan needs explicit acceptance criteria for cross-surface overlay behavior, persistent navigation placement, Detail-page ordering, concept quality rules, stale-state invalidation, and discovery QA. It also needs a concrete migration/data-continuity subsection so schema versioning is tied to preserving libraries rather than merely tracking versions.
