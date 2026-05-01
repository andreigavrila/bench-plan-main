# PLAN EVALUATION

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
| PRD-001 | Use Next.js latest stable runtime | critical | full | `§2.1 Tech Stack (Benchmark Baseline)` |  |
| PRD-002 | Use Supabase official client libraries | critical | partial | `§2.1 Tech Stack; Phase 1 Task 2 ("Configure Supabase client")` | The plan commits to Supabase but never explicitly says the implementation must use the official Supabase client libraries. |
| PRD-003 | Ship `.env.example` with required variables | critical | full | `§4.2 Environment Variables; Phase 1 Task 7` |  |
| PRD-004 | Ignore `.env*` secrets except example | important | partial | `Phase 1 Task 7; §9 Infrastructure Rider PRD` | It plans a `.gitignore`, but it does not explicitly state the `.env*` ignore pattern with a carve-out for `.env.example`. |
| PRD-005 | Configure build through env without code edits | critical | full | `§4.2 Environment Variables; §8 Build & Run Instructions` |  |
| PRD-006 | Keep secrets out of repo and server-only | critical | full | `§4.2 Environment Variables; Phase 1 Task 2; §6.2 AI Integration Pattern` |  |
| PRD-007 | Provide app, test, reset command scripts | critical | full | `Phase 1 Task 8; §8 Build & Run Instructions` |  |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | `§3.3 Migrations; Phase 1 Task 3` |  |
| PRD-009 | Use one stable namespace per build | critical | full | `§2.3 Isolation Model; Phase 1 Task 9` |  |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | `§2.3 Isolation Model; §3.2 RLS; Phase 11 Task 6` |  |
| PRD-011 | Attach every user record to `user_id` | critical | full | `§3.1 Tables > shows/cloud_settings; §2.3 Isolation Model` |  |
| PRD-012 | Partition persisted data by namespace and user | critical | full | `§2.3 Isolation Model; §3.2 RLS` |  |
| PRD-013 | Support documented dev auth injection, prod-gated | important | partial | `Phase 1 Task 5; §6.4 Namespace & User Scoping` | The gating behavior is planned, but the plan does not explicitly include documentation of the development identity injection path. |
| PRD-014 | Real OAuth later needs no schema redesign | important | full | `Phase 1 Task 5; §6.4 Namespace & User Scoping` |  |
| PRD-015 | Keep backend as persisted source of truth | critical | full | `§6.1 State Management; §6.4 Namespace & User Scoping` |  |
| PRD-016 | Make client cache safe to discard | critical | full | `§6.1 State Management ("Client cache is disposable")` |  |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | full | `§2.1 Tech Stack; §9 Infrastructure Rider PRD checklist` |  |
| PRD-018 | Overlay saved user data on every show appearance | critical | full | `Phase 10 Tasks 1 and 3` |  |
| PRD-019 | Support visible statuses plus hidden `Next` | important | full | `§3.1 Tables > shows.my_status; Phase 4 Task 4` |  |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | full | `Phase 4 Task 4 ("Interested/Excited set status=Later + interest")` |  |
| PRD-021 | Support free-form multi-tag personal tag library | important | full | `Phase 3 Task 2; Phase 4 Task 4 ("Free-form tag input")` |  |
| PRD-022 | Define collection membership by assigned status | critical | partial | `§3.1 Tables > shows.my_status; Phase 2 Task 5` | The plan implies status-based collection logic, but it never explicitly names assigned status as the authoritative collection-membership rule. |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | full | `Phase 4 Tasks 4-5; §9 Compliance Checklist` |  |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | `Phase 4 Task 5 ("default values per PRD §5.2-5.3")` |  |
| PRD-025 | Removing status deletes show and all My Data | critical | partial | `Phase 4 Task 4 ("Reselecting triggers removal confirmation"); Phase 2 Task 4` | The confirmation/remove flow is planned, but clearing every My Data field on removal is not spelled out. |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | partial | `Phase 2 Task 3; §6.3 Catalog Integration Pattern` | Merge-on-refresh is covered, but the plan does not define how removed shows retain and restore prior My Data when re-added. |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | `§3.1 Tables > my*_update_date columns; Phase 10 Task 4` |  |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | partial | `Phase 5 Task 3 (freshness); Phase 10 Task 5 (conflict resolution)` | Freshness and conflict resolution are explicit, but timestamp-driven sorting behavior is not planned concretely. |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | full | `Phase 5 Task 3 ("4-hour cache via aiScoopUpdateDate"; "Persist only if show is in collection")` |  |
| PRD-030 | Keep Ask and Alchemy state session-only | important | full | `Phase 6 Task 6; Phase 7 Task 2` |  |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | full | `Phase 6 Task 2; Phase 7 Tasks 1 and 4` |  |
| PRD-032 | Show collection and rating tile indicators | important | full | `Phase 3 Task 5; Phase 10 Task 2` |  |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | partial | `§3.1 cloud_settings; Phase 9 Task 2; Phase 10 Task 5` | Settings sync and merge policy are covered, but duplicate library reconciliation across devices is not described concretely. |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | partial | `Phase 10 Task 6 ("Implement migration system for future schema changes")` | It plans migrations, but not the carry-forward strategy that guarantees existing libraries survive model upgrades. |
| PRD-035 | Persist synced settings, local settings, UI state | important | full | `Phase 3 Task 2; Phase 9 Tasks 2-5` |  |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | full | `§3.1 shows.provider_data; §6.3 Catalog Integration Pattern` |  |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | full | `Phase 2 Tasks 2-3; §6.3 Catalog Integration Pattern` |  |
| PRD-038 | Provide filters panel and main screen destinations | important | full | `§4.1 Directory Layout; Phase 3 Task 1` |  |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | full | `§4.1 Directory Layout (find/ routes, TopNav)` |  |
| PRD-040 | Keep Settings in persistent primary navigation | important | full | `§4.1 Directory Layout (settings/ route, TopNav)` |  |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | `Phase 4 Task 1; components/find/ModeSwitcher.tsx` |  |
| PRD-042 | Show only library items matching active filters | important | full | `Phase 3 Task 4 ("Fetch filtered shows"); Phase 2 Task 5` |  |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | `Phase 3 Task 4` |  |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | full | `Phase 3 Tasks 2-3; Phase 2 Task 5` |  |
| PRD-045 | Render poster, title, and My Data badges | important | full | `Phase 3 Task 5` |  |
| PRD-046 | Provide empty-library and empty-filter states | detail | full | `Phase 3 Task 6` |  |
| PRD-047 | Search by title or keywords | important | full | `Phase 2 Task 1 ("Search by query"); Phase 4 Task 2` |  |
| PRD-048 | Use poster grid with collection markers | important | full | `Phase 4 Task 2 ("Results grid with in-collection indicators")` |  |
| PRD-049 | Auto-open Search when setting is enabled | detail | full | `Phase 4 Task 2 ("Auto-open on launch if autoSearch setting is enabled")` |  |
| PRD-050 | Keep Search non-AI in tone | important | partial | `Phase 4 Task 2; components/find/SearchResults.tsx` | The plan keeps Search structurally separate from AI flows, but it never explicitly calls out the non-AI tone requirement for Search UX or copy. |
| PRD-051 | Preserve Show Detail narrative section order | important | partial | `Phase 4 Task 3; Phase 5 Tasks 5-6; Phase 6 Task 5` | The relevant sections exist across phases, but the plan never restates the full required end-state order including Ask CTA and Explore Similar in one preserved hierarchy. |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | partial | `Phase 4 Task 3.1 ("Header media carousel...videos"); components/detail/HeaderMedia.tsx` | It prioritizes rich media, but the graceful poster/backdrop-only fallback is not explicitly planned. |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | full | `Phase 4 Task 3.2` |  |
| PRD-054 | Place status/interest controls in toolbar | important | full | `Phase 4 Task 4 ("Status/Interest chips in toolbar")` |  |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | `Phase 4 Task 4 (TagPicker auto-saves as Later + Interested)` |  |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | `Phase 4 Task 4 (Rating unsaved show auto-saves as Done)` |  |
| PRD-057 | Show overview early for fast scanning | important | full | `Phase 4 Task 3.4 ("Overview")` |  |
| PRD-058 | Scoop shows correct states and progressive feedback | important | full | `Phase 5 Tasks 3 and 5` |  |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | full | `Phase 6 Tasks 1 and 5` |  |
| PRD-060 | Include traditional recommendations strand | important | full | `Phase 4 Task 3.6` |  |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | full | `Phase 5 Task 6` |  |
| PRD-062 | Include streaming availability and person-linking credits | important | full | `Phase 4 Tasks 3.7-3.8; Phase 8 Task 3` |  |
| PRD-063 | Gate seasons to TV and financials to movies | important | full | `Phase 4 Tasks 3.9-3.10` |  |
| PRD-064 | Keep primary actions early and page not overwhelming | important | partial | `Phase 4 Task 3; Phase 10 Task 10` | The section list suggests early primary actions, but the plan does not explicitly design against detail-page overload or describe the intended information density. |
| PRD-065 | Provide conversational Ask chat interface | important | full | `Phase 6 Task 4` |  |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | partial | `Phase 6 Task 1; src/lib/ai/prompts/ask.ts deliverable` | The plan covers Ask mechanics, but it does not explicitly require the answer-first, confident-picks behavior from the quality bar. |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | `Phase 6 Task 4 ("Mentioned shows horizontal strip")` |  |
| PRD-068 | Open Detail from mentions or Search fallback | important | full | `Phase 6 Task 2` |  |
| PRD-069 | Show six random starter prompts with refresh | important | full | `Phase 6 Task 4 ("6 random starter prompts (refreshable)")` |  |
| PRD-070 | Summarize older turns while preserving voice | important | full | `Phase 6 Task 3` |  |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | full | `Phase 6 Tasks 1 and 5` |  |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | partial | `Phase 6 Task 2 ("Parse Title::externalId::mediaType;;... format")` | It plans the string parser, but it never explicitly preserves the outer `commentary` plus exact `showList` response contract. |
| PRD-073 | Retry malformed mention output once, then fallback | important | full | `Phase 6 Task 2 ("retry with stricter formatting, then unstructured + search handoff")` |  |
| PRD-074 | Redirect Ask back into TV/movie domain | important | full | `Phase 10 Task 8 ("Domain restriction (TV/movies only)")` |  |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | partial | `Phase 5 Task 2; Phase 5 Task 4` | Concept generation is specified, but the plan does not explicitly anchor concepts as taste ingredients rather than genre labels. |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | full | `Phase 5 Task 4 ("Return bullet list, 1-3 words each, no explanations")` |  |
| PRD-077 | Order concepts by strongest aha and varied axes | important | full | `Phase 5 Task 4 ("specific, diverse, ordered by strength")` |  |
| PRD-078 | Require concept selection and guide ingredient picking | important | partial | `Phase 5 Task 6; Phase 7 Tasks 2-3` | Selection mechanics are covered, but the guidance copy about "ingredients" and the requirement to nudge selection are not planned. |
| PRD-079 | Return exactly five Explore Similar recommendations | important | full | `Phase 7 Task 1 ("Return 6 recommendations (Alchemy) or 5 (Explore Similar)")` |  |
| PRD-080 | Support full Alchemy loop with chaining | important | full | `Phase 7 Task 2` |  |
| PRD-081 | Clear downstream results when inputs change | important | full | `Phase 7 Task 2 ("changing shows clears concepts/results")` |  |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | partial | `Phase 5 Task 4 ("Multi-show: shared concepts for Alchemy")` | Shared concept generation is planned, but the larger multi-show option pool called for by the spec is not. |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | full | `Phase 7 Task 1 ("Reasons explicitly reference selected concepts")` |  |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | partial | `Phase 7 Task 1; §7 Risk & Mitigation ("Golden set testing")` | The plan wants taste-aware reasons, but it does not define acceptance criteria that force surprising-but-defensible recommendation quality. |
| PRD-085 | Keep one consistent AI persona across surfaces | important | full | `§6.2 AI Integration Pattern ("share a common system prompt for persona consistency")` |  |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | partial | `Phase 10 Tasks 7-9; §6.2 AI Integration Pattern` | Spoiler safety, domain restriction, and fallbacks are planned, but the broader shared AI guardrail set is not fully enumerated across all surfaces. |
| PRD-087 | Make AI warm, joyful, and light in critique | important | partial | `Phase 5 Task 2; src/lib/ai/prompts/ask.ts and scoop.ts deliverables` | Persona consistency is planned, but the warm, joy-forward, lightly critical tone is not explicitly locked in as an acceptance criterion. |
| PRD-088 | Structure Scoop as personal taste mini-review | important | partial | `Phase 5 Task 2 ("Scoop prompt...structured sections"); Phase 5 Task 3` | The plan implies a structured Scoop, but it does not spell out the personal-taste mini-review shape from the spec. |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | partial | `Phase 6 Task 1; src/lib/ai/prompts/ask.ts deliverable` | Ask exists as chat, but the brisk, dialogue-first response style is not explicitly planned. |
| PRD-090 | Feed AI the right surface-specific context inputs | important | full | `Phase 5 Task 2; Phase 6 Task 1; Phase 7 Task 1` |  |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | partial | `§7 Risk & Mitigation ("Golden set testing"); Phase 11 Tasks 1-4` | There is test coverage around AI plumbing, but no concrete rubric-driven evaluation loop or hard-fail gate for recommendation integrity. |
| PRD-092 | Show person gallery, name, and bio | important | full | `Phase 8 Task 2` |  |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | full | `Phase 8 Task 2` |  |
| PRD-094 | Group filmography by year | important | full | `Phase 8 Task 2` |  |
| PRD-095 | Open Show Detail from selected credit | important | full | `Phase 8 Task 3` |  |
| PRD-096 | Include font size and Search-on-launch settings | important | full | `Phase 9 Tasks 1 and 3` |  |
| PRD-097 | Support username, model, and API-key settings safely | important | partial | `Phase 9 Tasks 1-2; §4.2 Environment Variables` | The settings are present, but the plan does not clearly define safe handling boundaries for user-entered API keys beyond keeping repo secrets out of source control. |
| PRD-098 | Export saved shows and My Data as zip | critical | full | `Phase 9 Task 4` |  |
| PRD-099 | Encode export dates using ISO-8601 | important | full | `Phase 9 Task 4 ("Dates encoded as ISO-8601")` |  |

### 3. Coverage Scores

Overall score:

`score = (74 × 1.0 + 25 × 0.5) / 99 × 100 = 87.37%`

Critical:  `(23 × 1.0 + 7 × 0.5) / 30 × 100 = 88.33%`  `(26.5 of 30 critical requirements)`
Important: `(49 × 1.0 + 18 × 0.5) / 67 × 100 = 86.57%` `(58 of 67 important requirements)`
Detail:    `(2 × 1.0 + 0 × 0.5) / 2 × 100 = 100.00%`  `(2 of 2 detail requirements)`
Overall:   `(74 × 1.0 + 25 × 0.5) / 99 × 100 = 87.37%` `(86.5 of 99 total requirements)`

### 4. Top Gaps

1. PRD-072 | `critical` | Emit `commentary` plus exact `showList` contract  
The Ask UI depends on deterministic structured output; without the exact response envelope, mentioned-show rendering can fail even when the prose answer looks correct.
2. PRD-086 | `critical` | Enforce shared AI guardrails across all surfaces  
Without a single cross-surface contract, Scoop, Ask, Explore Similar, and Alchemy can drift into spoilers, domain leakage, generic reasoning, or inconsistent fallback behavior.
3. PRD-026 | `critical` | Re-add preserves My Data and refreshes public data  
This is a trust-sensitive lifecycle rule: users will notice if previously entered ratings, tags, interest, or Scoop content disappear instead of being restored when a show returns to the collection.
4. PRD-034 | `critical` | Preserve saved libraries across data-model upgrades  
Schema migrations alone are not enough; without an explicit carry-forward plan, upgrades can silently drop or corrupt saved collections and fail a key durability expectation.
5. PRD-025 | `critical` | Removing status deletes show and all My Data  
If delete semantics are underspecified, implementations often leave stale tags, ratings, or Scoop fields behind, producing inconsistent collection state and confusing removal behavior.

### 5. Coverage Narrative

#### Overall Posture

This is a structurally sound plan with good surface coverage and solid benchmark-infrastructure thinking, but it still has meaningful fidelity gaps. It is not missing major screens or core platform choices; it is under-specifying several critical behavioral contracts that are easy to implement incorrectly.

#### Strength Clusters

The plan is strongest in Benchmark Runtime & Isolation, App Navigation & Discover Shell, Collection Home & Search, Person Detail, and Settings & Export. Those areas have concrete phases, identifiable components or tables, and explicit implementation tasks rather than vague intent.

#### Weakness Clusters

The gaps cluster in two places. First, Collection Data & Persistence has several lifecycle rules that are only implied, especially collection membership, delete/re-add semantics, sync duplication, and upgrade continuity. Second, AI Voice, Persona & Quality plus parts of Ask Chat and Concepts, Explore Similar & Alchemy are lighter on behavioral contracts than on plumbing, so the plan covers integration mechanics better than user-visible AI fidelity.

#### Risk Assessment

If executed as-is, the most likely failure mode is an app that looks complete and works on happy paths, but fails spec review on nuanced behavior. A QA reviewer would probably notice AI responses that parse or feel inconsistently across surfaces before noticing edge-case data lifecycle issues like incorrect delete/re-add behavior or weak continuity through schema upgrades.

#### Remediation Guidance

The next planning pass should add contract-level detail, not more architecture. It needs a dedicated data-lifecycle section for save/remove/re-add/upgrade semantics, an explicit AI behavior section with exact response schemas and per-surface quality bars, and a tighter Show Detail/Search UX section that locks narrative order, fallback behavior, and tone expectations into the plan itself.
