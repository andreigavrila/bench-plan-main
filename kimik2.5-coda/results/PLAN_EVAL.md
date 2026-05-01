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
| PRD-001 | Use Next.js latest stable runtime | critical | full | 2.1 Tech Stack |  |
| PRD-002 | Use Supabase official client libraries | critical | partial | 2.1 Tech Stack; 2.2 Project Structure `lib/supabase/` | The plan names Supabase but never commits to using the official Supabase client packages. |
| PRD-003 | Ship `.env.example` with required variables | critical | full | 9.1 Environment Setup |  |
| PRD-004 | Ignore `.env*` secrets except example | important | partial | 10.1 Build Configuration | It bans committing secrets but omits the required `.gitignore` rule for `.env*` except `.env.example`. |
| PRD-005 | Configure build through env without code edits | critical | full | 9.1 Environment Setup; 10.1 Build Configuration |  |
| PRD-006 | Keep secrets out of repo and server-only | critical | full | 10.1 Build Configuration |  |
| PRD-007 | Provide app, test, reset command scripts | critical | full | 9.2 Scripts |  |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | 2.2 Project Structure `supabase/migrations/`; 10.2 Database Migrations |  |
| PRD-009 | Use one stable namespace per build | critical | partial | 2.3 Namespace & Identity Model; 9.1 `APP_NAMESPACE` | Namespace isolation is described, but there is no concrete plan for assigning and preserving one stable namespace across an entire build/run. |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | 2.3 Namespace & Identity Model; 9.2 `test:reset` |  |
| PRD-011 | Attach every user record to `user_id` | critical | full | 2.3 User Identity; 3.1 schema `user_id` columns |  |
| PRD-012 | Partition persisted data by namespace and user | critical | partial | 2.3 Composite partition `(namespace_id, user_id)` | The partition model is stated at a high level, but not all persisted tables are explicitly scoped or derived by `(namespace_id, user_id)`. |
| PRD-013 | Support documented dev auth injection, prod-gated | important | partial | 2.3 User Identity; 9.4 Dev Identity Injection | Dev identity injection is described, but production gating and operator-facing documentation are not planned. |
| PRD-014 | Real OAuth later needs no schema redesign | important | partial | 2.3 User Identity model | The schema hints at future auth, but the plan never states how OAuth can replace dev injection without redesigning storage. |
| PRD-015 | Keep backend as persisted source of truth | critical | partial | 2.1 Tech Stack; 3.1 Database Schema | The architecture implies server persistence, but it does not explicitly forbid correctness from depending on local state. |
| PRD-016 | Make client cache safe to discard | critical | missing | none | The plan never defines disposable client caching or any rule that clearing local storage must not lose user data. |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | missing | none | Cloud-agent compatibility is not addressed, and the plan never states that Docker is optional or unnecessary. |
| PRD-018 | Overlay saved user data on every show appearance | critical | partial | 4.2 Search collection markers; 4.3 merge stored data | Show overlay behavior is covered on Detail/Search, but not as a cross-surface rule for every list, recommendation, and AI result. |
| PRD-019 | Support visible statuses plus hidden `Next` | important | full | 3.1 `my_status` includes `next`; 12 Open Questions |  |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | full | 4.3 My Data Controls; 7.2 Saving Triggers |  |
| PRD-021 | Support free-form multi-tag personal tag library | important | full | 4.3 Tag input with autocomplete; 4.1 Filters Sidebar |  |
| PRD-022 | Define collection membership by assigned status | critical | full | 7.1 Collection Membership |  |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | full | 7.2 Saving Triggers |  |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | 7.3 Default Values |  |
| PRD-025 | Removing status deletes show and all My Data | critical | partial | 7.4 Removal | Removal behavior is ambiguous because it allows either deleting the row or merely nulling fields, which changes re-add semantics. |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | missing | none | There is no plan for preserving prior My Data after removal and restoring it when the same show is re-added. |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | 3.1 schema timestamp fields; 7.6 Timestamps |  |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | full | 7.6 Timestamps |  |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | full | 4.3 AI Scoop Section; 7.6 Timestamps |  |
| PRD-030 | Keep Ask and Alchemy state session-only | important | partial | 3.1 `chat_sessions`/`chat_messages`; 4.5 Alchemy | Ask chat is planned as persisted `chat_sessions`/`chat_messages`, and neither Ask nor Alchemy is defined to clear on leave/reset. |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | full | 5.2 Recommendations include external ID for catalog resolution |  |
| PRD-032 | Show collection and rating tile indicators | important | full | 8.2 Show Tile Requirements |  |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | partial | 3.1 `user_settings`; 7.5 Merge Policy; 4.7 Import/Restore | Timestamp-based merging is mentioned, but cross-device sync behavior and duplicate-item reconciliation are not concretely planned. |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | partial | 3.1 `app_metadata`; 10.2 Database Migrations | The plan includes `app_metadata`, but not an upgrade path that explicitly carries forward existing libraries/My Data. |
| PRD-035 | Persist synced settings, local settings, UI state | important | partial | 3.1 `user_settings`; 7.4 Removal confirmation | Synced settings are modeled, but local settings and UI-state persistence are only partially covered and not separated clearly. |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | partial | 3.1 `provider_data`; `credits` table | Provider data is persisted, but the plan also persists credits and does not define the full transient/detail-fetch boundary. |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | full | 7.5 Merge Policy |  |
| PRD-038 | Provide filters panel and main screen destinations | important | full | 2.2 Project Structure; 4.1 Filters Sidebar |  |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | full | 2.2 `layout.tsx` root layout with nav; `find/page.tsx` |  |
| PRD-040 | Keep Settings in persistent primary navigation | important | full | 2.2 `layout.tsx` root layout with nav; `settings/page.tsx` |  |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | 2.2 `find/page.tsx`; 4.2 Search; 4.4 Ask; 4.5 Alchemy |  |
| PRD-042 | Show only library items matching active filters | important | partial | 4.1 `getCollection(namespace_id, user_id, filter?)` | Filtering is mentioned, but the plan does not spell out combined filter application logic for the rendered library. |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | 4.1 Grouping Logic |  |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | full | 4.1 Filters Sidebar |  |
| PRD-045 | Render poster, title, and My Data badges | important | full | 8.2 Show Tile Requirements |  |
| PRD-046 | Provide empty-library and empty-filter states | detail | full | 4.1 Empty States |  |
| PRD-047 | Search by title or keywords | important | partial | 4.2 `searchCatalog(query: string, page?: number)` | A generic catalog query is planned, but the title/keyword search contract is not stated explicitly. |
| PRD-048 | Use poster grid with collection markers | important | full | 4.2 Search UI; 4.2 Collection Integration |  |
| PRD-049 | Auto-open Search when setting is enabled | detail | partial | 3.1 `search_on_launch`; 4.7 Settings Form | The setting exists, but the plan never describes launch behavior that auto-enters Search when enabled. |
| PRD-050 | Keep Search non-AI in tone | important | partial | 4.2 Search (catalog integration only) | Search is built as catalog UI, but the plan never explicitly protects it from inheriting AI voice or chatty copy. |
| PRD-051 | Preserve Show Detail narrative section order | important | partial | 4.3 Show Detail Page; 3.7 Additional Sections | The plan covers many sections, but the documented narrative order is not preserved and omits the Ask-about-show CTA in sequence. |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | partial | 4.3 Header Section | Rich header media is planned, but graceful fallback behavior when trailers/backdrops are absent is not. |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | partial | 4.3 Data Loading; 3.7 Additional Sections | Relevant facts are included somewhere on the page, but the plan does not commit to surfacing them early. |
| PRD-054 | Place status/interest controls in toolbar | important | partial | 4.3 My Data Controls | Status and interest controls are planned, but their required toolbar placement is not. |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | 4.3 My Data Controls |  |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | 4.3 My Data Controls |  |
| PRD-057 | Show overview early for fast scanning | important | partial | 4.3 Additional Sections includes Overview | Overview is present, but the plan does not position it early enough to satisfy the first-scan requirement. |
| PRD-058 | Scoop shows correct states and progressive feedback | important | full | 4.3 AI Scoop Section |  |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | full | 4.4 Ask About Show |  |
| PRD-060 | Include traditional recommendations strand | important | full | 4.3 Additional Sections |  |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | full | 4.3 Explore Similar |  |
| PRD-062 | Include streaming availability and person-linking credits | important | partial | 4.3 Additional Sections; 4.6 Person Detail Page | Streaming and credits are present, but the credits section is not explicitly planned as person-linked navigation from Detail. |
| PRD-063 | Gate seasons to TV and financials to movies | important | full | 4.3 Additional Sections |  |
| PRD-064 | Keep primary actions early and page not overwhelming | important | partial | 4.3 section ordering | The plan lists sections, but it does not explain how action density is managed so the page stays powerful without feeling busy. |
| PRD-065 | Provide conversational Ask chat interface | important | full | 4.4 Ask (AI Chat) |  |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | partial | 5.1 Base System Prompt; 4.4 Ask | The voice prompt is spoiler-safe, but the plan does not commit to direct-first Ask answers or confident recommendation formatting. |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | 4.4 UI Components |  |
| PRD-068 | Open Detail from mentions or Search fallback | important | partial | 4.4 UI Components; 5.2 Chat | Mentioned shows are parsed and displayed, but the handoff to Detail or Search fallback is not defined. |
| PRD-069 | Show six random starter prompts with refresh | important | full | 4.4 UI Components |  |
| PRD-070 | Summarize older turns while preserving voice | important | full | 4.4 Context Management |  |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | full | 4.4 Ask About Show |  |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | partial | 5.2 Chat mentioned shows format; 5.3 `chatAsk(...)` | It specifies the mention delimiter string, but not the exact `commentary` + `showList` response contract the UI/parser expects. |
| PRD-073 | Retry malformed mention output once, then fallback | important | missing | none | There is no retry-once/fallback plan for malformed structured mention output. |
| PRD-074 | Redirect Ask back into TV/movie domain | important | partial | 5.1 Base System Prompt | The persona is TV/movie themed, but the plan never defines explicit redirection for out-of-domain prompts. |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | partial | 4.3 Explore Similar; 4.5 Alchemy | Concept generation is included, but the plan does not explain the core product rule that concepts are ingredient-like taste DNA rather than genre tags. |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | full | 5.2 Concept Generation |  |
| PRD-077 | Order concepts by strongest aha and varied axes | important | missing | none | The plan never addresses ordering concepts by strongest aha or ensuring varied axes. |
| PRD-078 | Require concept selection and guide ingredient picking | important | partial | 4.3 Explore Similar; 4.5 Recommendation Flow | Concept selection exists, but the plan does not include guidance copy or UX nudges that teach users to pick ingredients. |
| PRD-079 | Return exactly five Explore Similar recommendations | important | full | 4.3 Explore Similar |  |
| PRD-080 | Support full Alchemy loop with chaining | important | full | 4.5 Alchemy |  |
| PRD-081 | Clear downstream results when inputs change | important | full | 4.5 State Management |  |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | partial | 4.5 Concept Generation | Shared multi-show concepts are planned, but there is no larger option pool than the single-show flow. |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | full | 4.5 Recommendation Flow; 5.2 Recommendations |  |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | partial | 5.2 Recommendations; 8.1 Taste-aware AI | Taste-aware reasoning is planned, but the surprise-without-betrayal quality bar is not. |
| PRD-085 | Keep one consistent AI persona across surfaces | important | full | 5.1 Base System Prompt |  |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | partial | 5.1 Base System Prompt; 5.2 prompts | Some shared rules appear in the base prompt, but the full cross-surface guardrail set is not codified as a reusable contract. |
| PRD-087 | Make AI warm, joyful, and light in critique | important | full | 5.1 Base System Prompt |  |
| PRD-088 | Structure Scoop as personal taste mini-review | important | full | 5.2 Scoop Generation |  |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | partial | 4.4 Ask (AI Chat); 5.1 Base System Prompt | Ask is conversational, but the plan does not explicitly keep responses brisk and dialogue-like by default. |
| PRD-090 | Feed AI the right surface-specific context inputs | important | full | 5.2 Surface-Specific Prompts |  |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | missing | none | No validation rubric, quality gate, or hard-fail integrity check is planned for discovery outputs. |
| PRD-092 | Show person gallery, name, and bio | important | full | 4.6 UI Layout |  |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | full | 4.6 Data Fetching; 4.6 UI Layout |  |
| PRD-094 | Group filmography by year | important | full | 4.6 Data Fetching; 4.6 UI Layout |  |
| PRD-095 | Open Show Detail from selected credit | important | full | 4.6 UI Layout |  |
| PRD-096 | Include font size and Search-on-launch settings | important | full | 4.7 Settings Form |  |
| PRD-097 | Support username, model, and API-key settings safely | important | partial | 4.7 Settings Form | Username, model, and API keys are partly covered, but the plan does not explicitly include the catalog-provider key path or full safe-handling rules. |
| PRD-098 | Export saved shows and My Data as zip | critical | full | 4.7 Export/Backup |  |
| PRD-099 | Encode export dates using ISO-8601 | important | full | 4.7 Export/Backup |  |

### 3. Coverage Scores

Overall score = (57 × 1.0 + 36 × 0.5) / 99 × 100 = 75.8%

Critical:  (19 × 1.0 + 9 × 0.5) / 30 × 100 = 78.3%  (23.5 of 30 critical requirements)
Important: (37 × 1.0 + 26 × 0.5) / 67 × 100 = 74.6%  (50 of 67 important requirements)
Detail:    (1 × 1.0 + 1 × 0.5) / 2 × 100 = 75.0%  (1.5 of 2 detail requirements)
Overall:   75.8% (99 total requirements)

### 4. Top Gaps

1. PRD-026 | `critical` | Re-add preserves My Data and refreshes public data
Without a re-add strategy, a user can lose the relationship data they curated the moment they remove and later re-save a title, which breaks continuity for ratings, tags, and Scoop history.

2. PRD-016 | `critical` | Make client cache safe to discard
If client-local state quietly becomes authoritative, clearing browser storage or reinstalling can erase user data even though the product and benchmark both require backend durability.

3. PRD-009 | `critical` | Use one stable namespace per build
Namespace support exists, but without a concrete per-build stability plan the benchmark can suffer cross-run collisions, unsafe resets, and nondeterministic test behavior.

4. PRD-072 | `critical` | Emit `commentary` plus exact `showList` contract
Ask may appear to work in prose while silently breaking the mentioned-shows strip and Detail handoff if the response shape drifts from the parser contract.

5. PRD-025 | `critical` | Removing status deletes show and all My Data
The delete-vs-nullify ambiguity changes collection semantics and directly conflicts with the separate requirement that re-adding a removed show can restore the user's prior relationship.

### 5. Coverage Narrative

#### Overall Posture

The plan is structurally sound and covers most major product surfaces, but it is not benchmark-ready as written. It reads like a solid implementation outline with several important and a handful of critical behavioral contracts left underspecified, especially around persistence semantics, isolation rigor, and AI output contracts.

#### Strength Clusters

Coverage is strongest in Collection Data & Persistence for first-save rules, timestamps, Scoop freshness, and merge policy; in App Navigation & Discover Shell plus Collection Home & Search for the visible surface map; and in Person Detail and Settings & Export, where the major user-facing capabilities are planned concretely. The Ask, Explore Similar, and Alchemy surfaces also have good baseline feature coverage when judged at the feature-list level.

#### Weakness Clusters

The biggest gaps cluster in benchmark-runtime semantics and exact behavioral contracts, not in headline feature presence. The plan regularly names a capability but stops short of the hard edge the PRD requires: stable per-build namespaces, disposable client cache, removal/re-add semantics, session-only AI state, exact Ask structured output, AI fallback rules, and discovery quality validation. A secondary weakness cluster is Show Detail craft, where section presence is decent but ordering and interaction placement are softer than the spec.

#### Risk Assessment

If this plan were executed as-is, the first thing QA would likely notice is that the app feels mostly complete but fails on benchmark-grade correctness. The most visible breakages would be Ask mention chips not reliably opening Detail, Search-on-launch and other persistence behaviors feeling inconsistent, data-reset or namespace collisions during test runs, and collection semantics that become confusing when a removed show is later encountered again.

#### Remediation Guidance

The plan needs a second pass focused on explicit contracts, not more broad feature enumeration. For the runtime/persistence cluster, add concrete data-lifecycle decisions, namespace ownership rules, cache-disposal guarantees, and removal/re-add behavior. For the AI cluster, define exact request/response schemas, fallback paths, and shared guardrails once and reuse them across surfaces. For Show Detail, tighten the narrative hierarchy and placement requirements so implementation decisions cannot drift away from the intended first-15-seconds experience.
