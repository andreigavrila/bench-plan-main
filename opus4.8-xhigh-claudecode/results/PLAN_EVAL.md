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
| PRD-001 | Use Next.js latest stable runtime | critical | full | `§2 Technology decisions`: "Next.js (latest stable), App Router, TypeScript" |  |
| PRD-002 | Use Supabase official client libraries | critical | full | `§2 Technology decisions`: `@supabase/supabase-js` |  |
| PRD-003 | Ship `.env.example` with required variables | critical | full | `§10 Repo deliverables`: `.env.example` variable list |  |
| PRD-004 | Ignore `.env*` secrets except example | important | full | `§10 Repo deliverables`: `.gitignore` excludes `.env*` except `.env.example` |  |
| PRD-005 | Configure build through env without code edits | critical | full | `§10 Repo deliverables`: "Build runs by filling env -- no source edits" |  |
| PRD-006 | Keep secrets out of repo and server-only | critical | full | `§3.5 Key handling`; `§10 Repo deliverables` |  |
| PRD-007 | Provide app, test, reset command scripts | critical | full | `§10 Repo deliverables`: `npm run dev`, `npm test`, `npm run test:reset` |  |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | `§4.5 Migrations & data continuity`; `§10 Repo deliverables` |  |
| PRD-009 | Use one stable namespace per build | critical | full | `§3.1 Namespace`: `NAMESPACE_ID` read from env at boot |  |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | `§3.1 Namespace`; `§5.4 Settings, export, test-reset` |  |
| PRD-011 | Attach every user record to `user_id` | critical | full | `§3.2 User identity`; `§4.1 shows table` |  |
| PRD-012 | Partition persisted data by namespace and user | critical | full | `§3.2`: effective partition key `(namespace_id, user_id)` |  |
| PRD-013 | Support documented dev auth injection, prod-gated | important | full | `§3.3 Dev identity injection`; `§10 README documents` |  |
| PRD-014 | Real OAuth later needs no schema redesign | important | full | `§3.3`: OAuth requires config and auth wiring only |  |
| PRD-015 | Keep backend as persisted source of truth | critical | full | `§3.4 Backend is the source of truth` |  |
| PRD-016 | Make client cache safe to discard | critical | full | `§2`: TanStack Query as disposable cache; `§3.4` |  |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | full | `§10 Repo deliverables`: "No Docker required" |  |
| PRD-018 | Overlay saved user data on every show appearance | critical | full | `§1 Product understanding`: user's version always wins everywhere |  |
| PRD-019 | Support visible statuses plus hidden `Next` | important | full | `§7.1 Status, Interest`: visible statuses plus hidden `next` |  |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | full | `§7.1`: selecting Interested/Excited sets `later` plus interest |  |
| PRD-021 | Support free-form multi-tag personal tag library | important | full | `§7.5 Filters`: tag filters from tags; `§7.2` tag save trigger |  |
| PRD-022 | Define collection membership by assigned status | critical | full | `§7.1`: in collection iff non-nil `my_status` |  |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | full | `§7.2 Saving triggers & defaults` |  |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | `§7.2`: default later/interested; rating saves as done |  |
| PRD-025 | Removing status deletes show and all My Data | critical | full | `§7.3 Removal semantics` |  |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | full | `§4.4 Merge / overwrite engine` |  |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | `§4.1 shows table`: per-field timestamps listed |  |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | full | `§4.4` timestamp merge; `§4.6` sync; `§8.3` freshness |  |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | full | `§8.3 Scoop`: 4h freshness, persist only if in collection |  |
| PRD-030 | Keep Ask and Alchemy state session-only | important | full | `§2`: React Context/useReducer session state; `§8.4`, `§8.5` |  |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | full | `§8.5 AI-to-real-show resolution` |  |
| PRD-032 | Show collection and rating tile indicators | important | full | `§7.4 Collection Home`: My Data badges, in-collection + rating |  |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | full | `§4.6 Sync & conflict resolution` |  |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | full | `§4.5 Migrations & data continuity` |  |
| PRD-035 | Persist synced settings, local settings, UI state | important | full | `§4.2 Supporting tables`; `§4.3 Client-only settings` |  |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | full | `§4.1` provider IDs and transient list; `§9 Catalog provider` |  |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | full | `§4.4 Merge / overwrite engine` |  |
| PRD-038 | Provide filters panel and main screen destinations | important | full | `§6 Frontend architecture`: global layout and page tree |  |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | full | `§6`: persistent Find/Discover entry point |  |
| PRD-040 | Keep Settings in persistent primary navigation | important | full | `§6`: persistent Settings entry point |  |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | `§1 Product understanding`; `§6 Find features` |  |
| PRD-042 | Show only library items matching active filters | important | full | `§7.4 Collection Home`: shows matching active filters |  |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | `§7.4 Collection Home`: exact four groups |  |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | full | `§7.5 Filters`: All, tag, genre, decade, score, media toggle |  |
| PRD-045 | Render poster, title, and My Data badges | important | full | `§7.4 Collection Home`: tiles show poster, title, My Data badges |  |
| PRD-046 | Provide empty-library and empty-filter states | detail | full | `§7.4 Collection Home`: no collection and filter empty states |  |
| PRD-047 | Search by title or keywords | important | full | `§7.6 Search`: text search by title/keyword |  |
| PRD-048 | Use poster grid with collection markers | important | full | `§7.6 Search`: poster grid; in-collection items marked |  |
| PRD-049 | Auto-open Search when setting is enabled | detail | full | `§7.6 Search`: auto-open on launch when `autoSearch` enabled |  |
| PRD-050 | Keep Search non-AI in tone | important | full | `§7.6 Search`: "No AI voice" |  |
| PRD-051 | Preserve Show Detail narrative section order | important | full | `§7.7 Show Detail`: numbered order matches spec |  |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | full | `§7.7`: carousel with trailers and graceful poster/logo fallback |  |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | full | `§7.7` item 2: core facts and score |  |
| PRD-054 | Place status/interest controls in toolbar | important | full | `§7.7`: relationship controls in toolbar |  |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | `§7.2`: adding tag saves as `later` + `interested` |  |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | `§7.2`: rating unsaved show saves as `done` |  |
| PRD-057 | Show overview early for fast scanning | important | full | `§7.7` item 4: Overview + Scoop after tags/core facts |  |
| PRD-058 | Scoop shows correct states and progressive feedback | important | full | `§8.3 Scoop`: toggle copy states and streaming "Generating..." |  |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | full | `§8.4 Ask`: launched from Detail seeds show context |  |
| PRD-060 | Include traditional recommendations strand | important | full | `§7.7` item 7: Recommendations strand |  |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | full | `§7.7` item 8; `§8.5` Get Concepts to Explore Shows |  |
| PRD-062 | Include streaming availability and person-linking credits | important | full | `§7.7` Providers and Cast/Crew; `§8.8 Person Detail` |  |
| PRD-063 | Gate seasons to TV and financials to movies | important | full | `§7.7`: TV-vs-movie gating |  |
| PRD-064 | Keep primary actions early and page not overwhelming | important | full | `§7.7`: toolbar controls and long-tail info down-page |  |
| PRD-065 | Provide conversational Ask chat interface | important | full | `§8.4 Ask`: chat UI and dialogue tone |  |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | full | `§8.4 Ask`: direct answer, confident picks; `§8.2` spoiler-safe |  |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | `§8.4`: Mentioned-shows strip |  |
| PRD-068 | Open Detail from mentions or Search fallback | important | full | `§8.4`: tapping opens Detail or Search handoff |  |
| PRD-069 | Show six random starter prompts with refresh | important | full | `§8.4`: welcome view with 6 random starter prompts and refresh |  |
| PRD-070 | Summarize older turns while preserving voice | important | full | `§8.4`: summaries in same persona/tone |  |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | full | `§8.4`: handoff show context |  |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | full | `§8.4`: exact `{ commentary, showList }` and string format |  |
| PRD-073 | Retry malformed mention output once, then fallback | important | full | `§8.4`: retry once then unstructured/Search handoff |  |
| PRD-074 | Redirect Ask back into TV/movie domain | important | full | `§8.2 Shared rules`: stay in TV/movies, redirect if asked to leave |  |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | full | `§8.5 Concepts`: "taste ingredients"; not genres |  |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | full | `§8.5`: bullet list only, 1-3 words, avoid generic |  |
| PRD-077 | Order concepts by strongest aha and varied axes | important | full | `§8.5`: ordered by strongest aha and varied axes |  |
| PRD-078 | Require concept selection and guide ingredient picking | important | full | `§8.5`: require >=1 concept and ingredient guidance |  |
| PRD-079 | Return exactly five Explore Similar recommendations | important | full | `§8.5`: Explore Similar = 5 recs |  |
| PRD-080 | Support full Alchemy loop with chaining | important | full | `§8.5`: Alchemy flow through More Alchemy chaining |  |
| PRD-081 | Clear downstream results when inputs change | important | full | `§8.5`: changing inputs/selection clears downstream results |  |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | full | `§8.5`: shared across inputs and larger option pool |  |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | full | `§8.5`: reasons name matching concepts, 1-3 sentences |  |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | partial | `§8.6 Quality bar`: bake rubric into fixtures; `§8.5`: classics/hidden gems allowed | The plan implies the quality bar but does not explicitly plan for the "surprise without betrayal" acceptance criterion or 1-2 pleasantly unexpected recommendations. |
| PRD-085 | Keep one consistent AI persona across surfaces | important | full | `§8`: all surfaces share one persona |  |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | full | `§8.2 Shared rules & inputs` |  |
| PRD-087 | Make AI warm, joyful, and light in critique | important | full | `§8`: warm, opinionated, spoiler-safe friend persona |  |
| PRD-088 | Structure Scoop as personal taste mini-review | important | full | `§8.3 Scoop`: personal take, stack-up, centerpiece, warnings, verdict |  |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | full | `§8.4 Ask`: friend-in-dialogue, tight paragraphs |  |
| PRD-090 | Feed AI the right surface-specific context inputs | important | full | `§8.2`: library, My Data, show context, concepts, turns |  |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | full | `§8.6 Quality bar`: fixtures and real-show integrity hard gate |  |
| PRD-092 | Show person gallery, name, and bio | important | full | `§7.8 Person Detail`: image gallery, name, bio |  |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | full | `§7.8 Person Detail`: analytics charts listed |  |
| PRD-094 | Group filmography by year | important | full | `§7.8 Person Detail`: filmography grouped by year |  |
| PRD-095 | Open Show Detail from selected credit | important | full | `§7.8 Person Detail`: selecting credit opens Show Detail |  |
| PRD-096 | Include font size and Search-on-launch settings | important | full | `§7.9 Settings`: font size and search on launch |  |
| PRD-097 | Support username, model, and API-key settings safely | important | full | `§7.9 Settings`: username, model selection, API keys; env and never committed |  |
| PRD-098 | Export saved shows and My Data as zip | critical | full | `§5.4` and `§7.9`: `.zip` of saved shows + My Data |  |
| PRD-099 | Encode export dates using ISO-8601 | important | full | `§7.9`: ISO-8601 dates; `§11` export encoding tests |  |

### 3. Coverage Scores

Critical:  (30 full x 1.0 + 0 partial x 0.5) / 30 x 100 = 100.0%  (30.0 of 30 critical requirements)
Important: (66 full x 1.0 + 1 partial x 0.5) / 67 x 100 = 99.3%  (66.5 of 67 important requirements)
Detail:    (2 full x 1.0 + 0 partial x 0.5) / 2 x 100 = 100.0%  (2.0 of 2 detail requirements)
Overall:   99.5% (98.5 of 99 total requirements)

score = (98 full x 1.0 + 1 partial x 0.5) / 99 total x 100 = 99.5%

### 4. Top Gaps

1. PRD-084 | important | Deliver surprising but defensible taste-aligned recommendations

The plan commits to taste alignment, concept-cited reasons, real-show integrity, and quality fixtures, but it does not explicitly preserve the "surprise without betrayal" dimension from the discovery quality bar. Without that criterion, an implementation could pass with safe obvious recommendations that are technically aligned but feel less distinctive and less magical to users.

### 5. Coverage Narrative

#### Overall Posture

This is a very strong plan with one narrow quality-spec gap rather than a structural hole. The critical infrastructure, persistence, identity, source-of-truth, collection behavior, AI contract, and export requirements are all covered with concrete sections, schema choices, APIs, and test strategy.

#### Strength Clusters

The strongest coverage clusters are Benchmark Runtime & Isolation, Collection Data & Persistence, Show Detail & Relationship UX, Ask Chat, and Settings & Export. These areas are not just mentioned; they are tied to data model choices, route handlers, merge logic, UI placement, session lifetime, and validation/testing hooks.

#### Weakness Clusters

The only weakness cluster is in Concepts, Explore Similar & Alchemy, specifically the recommendation-quality nuance around surprise. The plan treats real-show resolution, selected-concept reasoning, counts, and tone as hard contracts, but the "pleasantly unexpected yet defensible" standard is left implicit through the broader quality rubric rather than named as its own acceptance condition.

#### Risk Assessment

If executed as-is, the most likely failure mode is not data loss or missing screens; it is discovery recommendations that are correct but too conservative. A QA reviewer comparing outputs to the discovery quality bar might notice that Explore Similar or Alchemy returns obvious adjacent titles without ensuring at least a small amount of defensible surprise.

#### Remediation Guidance

The remaining planning work is an acceptance-criteria refinement, not a new architecture section. The AI quality plan should explicitly add "surprise without betrayal" to the recommendation rubric and golden-set checks, including a target that at least 1-2 recommendations per Explore Similar or Alchemy round are unexpected but clearly justified by selected concepts and user taste.
