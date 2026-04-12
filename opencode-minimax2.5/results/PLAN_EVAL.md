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
| PRD-001 | Use Next.js latest stable runtime | critical | full | `2. Tech Stack & Infrastructure > Runtime` |  |
| PRD-002 | Use Supabase official client libraries | critical | partial | `2. Tech Stack & Infrastructure > Persistence` | The plan commits to Supabase but never specifies using the official Supabase client SDKs. |
| PRD-003 | Ship `.env.example` with required variables | critical | full | `2. Tech Stack & Infrastructure > Environment Interface` |  |
| PRD-004 | Ignore `.env*` secrets except example | important | missing | none | The plan never calls for `.gitignore` rules excluding `.env*` secrets while preserving `.env.example`. |
| PRD-005 | Configure build through env without code edits | critical | partial | `2. Tech Stack & Infrastructure > Environment Interface` | It lists environment variables but does not explicitly require a zero-code-edit configuration path. |
| PRD-006 | Keep secrets out of repo and server-only | critical | partial | `2. Tech Stack & Infrastructure > Environment Interface` | It notes one server-only key but does not state that secrets must stay out of the repo and all elevated keys remain server-only. |
| PRD-007 | Provide app, test, reset command scripts | critical | full | `2. Tech Stack & Infrastructure > Scripts` |  |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | `8. Implementation Order > Phase 1` includes `Supabase schema + migrations` |  |
| PRD-009 | Use one stable namespace per build | critical | full | `3.3 Namespace & User Isolation` and `9. Critical Considerations` |  |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | `2. Tech Stack & Infrastructure > Persistence`, `2. Tech Stack & Infrastructure > Scripts`, and `9. Critical Considerations` |  |
| PRD-011 | Attach every user record to `user_id` | critical | full | `3.3 Namespace & User Isolation` |  |
| PRD-012 | Partition persisted data by namespace and user | critical | full | `3.3 Namespace & User Isolation` |  |
| PRD-013 | Support documented dev auth injection, prod-gated | important | partial | `3.3 Namespace & User Isolation` | It mentions `X-User-Id` / `DEFAULT_USER_ID` but does not document the mechanism or how it is gated off in production. |
| PRD-014 | Real OAuth later needs no schema redesign | important | partial | `3.3 Namespace & User Isolation` | Using `user_id` helps, but the plan never states that future OAuth can be added without schema redesign. |
| PRD-015 | Keep backend as persisted source of truth | critical | partial | `2. Tech Stack & Infrastructure > Persistence` and `8. Implementation Order > Phase 1` | A backend exists, but the plan does not explicitly declare server persistence as the sole source of truth. |
| PRD-016 | Make client cache safe to discard | critical | missing | none | The plan never defines cache/local-storage behavior or requires clearing client state to be lossless. |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | partial | `2. Tech Stack & Infrastructure > Persistence` | Allowing hosted Supabase suggests a non-Docker path, but the plan never states Docker is optional or unsupported for cloud agents. |
| PRD-018 | Overlay saved user data on every show appearance | critical | partial | `9. Critical Considerations` says `User always wins` | It states precedence in principle but does not plan how every list, search result, and recommendation surface uses the overlaid saved version. |
| PRD-019 | Support visible statuses plus hidden `Next` | important | missing | none | The plan omits the hidden `Next` state from the data model and feature plan. |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | partial | `5.1 Save Triggers` and `5.2 Default Values` | It covers interest chips and defaults but never explicitly models Interested/Excited as `Later` plus an interest level. |
| PRD-021 | Support free-form multi-tag personal tag library | important | partial | `3.1 Show Entity` and `4.1 Collection Home` | Tags are present, but the plan never specifies free-form entry or a reusable personal tag library. |
| PRD-022 | Define collection membership by assigned status | critical | partial | `5.1 Save Triggers` and `3.1 Show Entity` | Status-driven saves are planned, but the plan never defines collection membership strictly as presence of an assigned status. |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | full | `5.1 Save Triggers` |  |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | `5.2 Default Values` |  |
| PRD-025 | Removing status deletes show and all My Data | critical | partial | `5.3 Removing` | It clears My Data, but it does not explicitly say the show record itself is removed from storage. |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | partial | `5.4 Merge Rules` | Merge rules are noted, but the re-add flow does not explicitly preserve prior My Data while refreshing public metadata. |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | `3.1 Show Entity` |  |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | partial | `3.1 Show Entity` and `5.5 AI Scoop` | Timestamps are modeled and Scoop freshness uses them, but sort order and sync conflict usage are not planned. |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | full | `5.5 AI Scoop` |  |
| PRD-030 | Keep Ask and Alchemy state session-only | important | partial | `4.3 Ask (AI Chat)` and `4.4 Alchemy` | The plan keeps these features session-oriented, but it never states that chat/history/results are cleared when leaving or resetting. |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | partial | `6.5 Concept Recs` and `4.3 Ask (AI Chat)` | It requires valid IDs and selectable mentions, but it does not define the lookup/resolution flow that turns every AI recommendation into a real selectable show. |
| PRD-032 | Show collection and rating tile indicators | important | partial | `4.1 Collection Home` and `4.2 Search` | The plan covers in-collection and generic user badges, but it never explicitly calls for rating indicators on tiles. |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | missing | none | Cross-device sync behavior, duplicate detection, and merge transparency are not planned. |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | partial | `9. Critical Considerations` and `8. Implementation Order > Phase 1` | It names migration safety, but it does not describe upgrade handling that preserves existing libraries and My Data. |
| PRD-035 | Persist synced settings, local settings, UI state | important | partial | `3.2 CloudSettings Entity` and `4.8 Settings` | Synced settings are modeled, but local settings and persisted UI state such as last filter/removal confirmation are not planned. |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | partial | `3.1 Show Entity` | The plan persists provider data, but it does not distinguish provider IDs from transient detail-only fetches. |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | partial | `5.4 Merge Rules` and `3.1 Show Entity` | The merge policy is high level, but it omits details like non-empty overwrite safeguards and timestamp maintenance for merge lifecycle fields. |
| PRD-038 | Provide filters panel and main screen destinations | important | full | `4.1 Collection Home` and `7. Project Structure` |  |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | partial | `7. Project Structure` includes `/find` | The route exists, but the plan never specifies persistent primary navigation treatment. |
| PRD-040 | Keep Settings in persistent primary navigation | important | partial | `7. Project Structure` includes `/settings` | The route exists, but the plan never specifies persistent primary navigation treatment. |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | `4.2 Search`, `4.3 Ask (AI Chat)`, and `4.4 Alchemy` |  |
| PRD-042 | Show only library items matching active filters | important | full | `4.1 Collection Home` |  |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | `4.1 Collection Home` |  |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | full | `4.1 Collection Home` |  |
| PRD-045 | Render poster, title, and My Data badges | important | full | `4.1 Collection Home` |  |
| PRD-046 | Provide empty-library and empty-filter states | detail | missing | none | The plan does not specify empty-library or empty-filter states. |
| PRD-047 | Search by title or keywords | important | partial | `4.2 Search` | It plans text search, but does not explicitly support keyword-based matching beyond title lookup. |
| PRD-048 | Use poster grid with collection markers | important | full | `4.2 Search` |  |
| PRD-049 | Auto-open Search when setting is enabled | detail | partial | `4.8 Settings` includes `Search on launch` | The setting exists, but the plan never ties it to auto-opening the Search mode on app launch. |
| PRD-050 | Keep Search non-AI in tone | important | missing | none | The plan does not state that Search must remain a straightforward non-AI catalog experience. |
| PRD-051 | Preserve Show Detail narrative section order | important | partial | `4.6 Show Detail` | The plan defines an order, but it diverges from the required narrative hierarchy and omits the Ask CTA plus genres/languages placement. |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | partial | `4.6 Show Detail` item 1 | It names a header carousel, but not trailer-first behavior or graceful fallback when rich media is absent. |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | full | `4.6 Show Detail` item 2 |  |
| PRD-054 | Place status/interest controls in toolbar | important | partial | `4.6 Show Detail` item 3 | Status and interest controls are listed, but their required toolbar placement is not planned. |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | `5.1 Save Triggers` and `5.2 Default Values` |  |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | `5.2 Default Values` |  |
| PRD-057 | Show overview early for fast scanning | important | partial | `4.6 Show Detail` | Overview is included, but the plan does not explicitly keep it early enough to support the first-scan experience. |
| PRD-058 | Scoop shows correct states and progressive feedback | important | partial | `5.5 AI Scoop` and `6.3 Scoop` | The plan covers persistence and content shape, but not toggle states, progressive streaming feedback, or visible generating/error states. |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | missing | none | The plan does not include the `Ask about this show` entry point or seeded handoff behavior from Detail. |
| PRD-060 | Include traditional recommendations strand | important | full | `4.6 Show Detail` item 8 |  |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | full | `4.5 Explore Similar` |  |
| PRD-062 | Include streaming availability and person-linking credits | important | partial | `4.6 Show Detail` items 10-11 and `4.7 Person Detail` | Streaming and cast/crew are present, but the plan does not explicitly state that credits link into Person Detail from the show page. |
| PRD-063 | Gate seasons to TV and financials to movies | important | full | `4.6 Show Detail` items 12-13 |  |
| PRD-064 | Keep primary actions early and page not overwhelming | important | partial | `4.6 Show Detail` | The section list implies early actions, but the plan never addresses clutter management or the intended power-without-busyness balance. |
| PRD-065 | Provide conversational Ask chat interface | important | full | `4.3 Ask (AI Chat)` |  |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | partial | `4.3 Ask (AI Chat)` and `6.1 Voice Requirements` | Conversational and spoiler-safe behavior is noted, but the plan does not require direct first-response recommendations or confident recommendation formatting. |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | partial | `4.3 Ask (AI Chat)` | It includes a selectable strip, but never specifies the required horizontal mentioned-shows row. |
| PRD-068 | Open Detail from mentions or Search fallback | important | partial | `4.3 Ask (AI Chat)` | Show mentions are selectable, but the Detail-open path and Search fallback behavior are not fully specified. |
| PRD-069 | Show six random starter prompts with refresh | important | partial | `4.3 Ask (AI Chat)` says `80 starter prompts on welcome view` | The plan includes starter prompts, but it misses the required six-random-prompts with refresh behavior. |
| PRD-070 | Summarize older turns while preserving voice | important | partial | `4.3 Ask (AI Chat)` | It plans summarization after ~10 turns, but does not preserve persona/voice requirements for the summary. |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | missing | none | The plan does not cover Ask-about-show sessions being seeded with a show handoff. |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | partial | `6.2 Ask Chat` defines `{ commentary: string, showList: "Title::id::type;;..." }` | The plan sketches the structured object, but it does not commit to the exact external-ID/media-type contract the parser requires. |
| PRD-073 | Retry malformed mention output once, then fallback | important | missing | none | There is no retry-once and fallback plan for malformed mention output. |
| PRD-074 | Redirect Ask back into TV/movie domain | important | missing | none | The plan does not define how Ask redirects out-of-domain requests back to TV/movie discovery. |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | partial | `6.4 Concepts` | Concept formatting is covered, but the plan never states that concepts are taste ingredients rather than genres or plot labels. |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | full | `6.4 Concepts` |  |
| PRD-077 | Order concepts by strongest aha and varied axes | important | missing | none | The plan does not address ordering concepts by strongest insight or ensuring variety across structural, tonal, and emotional axes. |
| PRD-078 | Require concept selection and guide ingredient picking | important | partial | `4.4 Alchemy` and `4.5 Explore Similar` | Concept selection exists in the flows, but the plan omits selection guidance and ingredient-picking UX copy. |
| PRD-079 | Return exactly five Explore Similar recommendations | important | full | `4.5 Explore Similar` |  |
| PRD-080 | Support full Alchemy loop with chaining | important | full | `4.4 Alchemy` |  |
| PRD-081 | Clear downstream results when inputs change | important | missing | none | The plan never states that changing input shows or concepts clears downstream concepts/results. |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | missing | none | The plan does not require multi-show concept generation to return a larger shared option pool. |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | full | `6.5 Concept Recs` |  |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | missing | none | The plan never defines a quality bar for surprising yet defensible taste-aligned recommendations. |
| PRD-085 | Keep one consistent AI persona across surfaces | important | partial | `6.1 Voice Requirements` | A persona is described, but the plan never states that every AI surface must share that same persona consistently. |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | partial | `6.1 Voice Requirements` and `6.2-6.5` | Some guardrails are present, but the shared cross-surface contract omits domain redirect, real-show actionability, and other universal rules. |
| PRD-087 | Make AI warm, joyful, and light in critique | important | partial | `6.1 Voice Requirements` | Warmth and honesty are included, but the joy-forward tone and light-touch critique standard are not explicit. |
| PRD-088 | Structure Scoop as personal taste mini-review | important | full | `6.3 Scoop` |  |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | partial | `4.3 Ask (AI Chat)` and `6.1 Voice Requirements` | Ask is conversational, but the plan does not explicitly require brisk, dialogue-like default responses. |
| PRD-090 | Feed AI the right surface-specific context inputs | important | missing | none | The plan does not specify which surface-specific inputs each AI feature receives from library, show, concept, or conversation context. |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | missing | none | There is no evaluation rubric or hard-fail integrity gate for discovery quality. |
| PRD-092 | Show person gallery, name, and bio | important | full | `4.7 Person Detail` |  |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | partial | `4.7 Person Detail` | Analytics are planned, but the required ratings, genres, and projects-by-year breakdowns are not specified. |
| PRD-094 | Group filmography by year | important | full | `4.7 Person Detail` |  |
| PRD-095 | Open Show Detail from selected credit | important | full | `4.7 Person Detail` |  |
| PRD-096 | Include font size and Search-on-launch settings | important | full | `4.8 Settings` |  |
| PRD-097 | Support username, model, and API-key settings safely | important | partial | `4.8 Settings` and `2. Tech Stack & Infrastructure > Environment Interface` | The settings are listed, but safe handling for user-entered keys and synced sensitive values is not planned. |
| PRD-098 | Export saved shows and My Data as zip | critical | full | `4.8 Settings` |  |
| PRD-099 | Encode export dates using ISO-8601 | important | missing | none | The export plan does not specify ISO-8601 date encoding. |

## 3. Coverage Scores

Overall score:

`score = (36 x 1.0 + 46 x 0.5) / 99 x 100 = 59.60%`

Critical:  (15 x 1.0 + 14 x 0.5) / 30 x 100 = 73.33%  (22.0 of 30 critical requirements)
Important: (21 x 1.0 + 31 x 0.5) / 67 x 100 = 54.48%  (36.5 of 67 important requirements)
Detail:    (0 x 1.0 + 1 x 0.5) / 2 x 100 = 25.00%  (0.5 of 2 detail requirements)
Overall:   (36 x 1.0 + 46 x 0.5) / 99 x 100 = 59.60%  (99 total requirements)

## 4. Top Gaps

1. `PRD-016` | `critical` | Make client cache safe to discard. This gap matters because the plan never defines the backend/cache boundary, so a plausible implementation could accidentally rely on browser persistence and lose user data after clearing storage or reinstalling.
2. `PRD-031` | `critical` | Resolve AI recommendations to real selectable shows. This gap matters because the product promise is actionable discovery; without a concrete resolution/mapping flow, Ask, Explore Similar, and Alchemy can degrade into non-clickable text or broken handoffs.
3. `PRD-037` | `critical` | Merge catalog fields safely and maintain timestamps. This gap matters because shallow merge rules are where saved ratings, tags, Scoop freshness, and refreshed catalog data most often corrupt or overwrite one another.
4. `PRD-072` | `critical` | Emit `commentary` plus exact `showList` contract. This gap matters because the UI/parser contract is brittle; near-miss formatting is enough to break mentioned-show rendering even if the AI answer reads well to a human.
5. `PRD-006` | `critical` | Keep secrets out of repo and server-only. This gap matters because the plan names secrets but does not define repo hygiene and key-boundary rules tightly enough, which risks benchmark non-compliance and accidental credential exposure.

## 5. Coverage Narrative

#### Overall Posture

This is a structurally sound high-level plan, not a benchmark-ready one. It captures the major screens, core entities, and several important business rules, but it leaves too many behavioral contracts, persistence edge cases, and AI guardrails at the level of implication.

#### Strength Clusters

The plan is strongest in Collection Data & Persistence at the headline-rule level, Collection Home & Search, Person Detail, and the basic app shell. It also does a reasonable job of enumerating the major AI surfaces and the broad feature set for Show Detail, Alchemy, and Settings.

#### Weakness Clusters

The gaps cluster around three patterns: benchmark runtime hardening, data integrity details, and AI behavioral contracts. Most of the `partial` scores come from the plan naming a feature without specifying the exact parser contract, fallback behavior, merge rule, source-of-truth boundary, or UX nuance that the PRD treats as binding.

#### Risk Assessment

If this plan were executed as-is, the most likely outcome is a polished demo that looks correct in happy-path walkthroughs but fails benchmark review and QA on state correctness. The first problems a reviewer would notice are inconsistent data behavior across surfaces, underspecified Ask/AI integration contracts, and missing operational rules around secrets, cache disposal, sync, and migration safety.

#### Remediation Guidance

The plan needs another pass focused on exactness, not breadth. Add explicit acceptance criteria for persistence and isolation rules, tighten the data-lifecycle and merge semantics, define the full AI contract layer including fallbacks and quality gates, and refine screen-level UX specs where the PRD depends on specific ordering, states, and interaction behavior rather than just feature presence.
