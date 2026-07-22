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
| PRD-001 | Use Next.js latest stable runtime | critical | full | Section 1; Phase 1 |  |
| PRD-002 | Use Supabase official client libraries | critical | partial | Section 1 and Phase 1 specify Supabase client modules | Supabase is selected, but the plan never explicitly requires its official client libraries. |
| PRD-003 | Ship `.env.example` with required variables | critical | full | Section 2.3 |  |
| PRD-004 | Ignore `.env*` secrets except example | important | missing | none | The file tree names `.gitignore`, but no task specifies the required `.env*` exclusion with an `.env.example` exception. |
| PRD-005 | Configure build through env without code edits | critical | full | Section 2.3; Phase 1 |  |
| PRD-006 | Keep secrets out of repo and server-only | critical | partial | Section 2.3 separates public and service-role variables | The plan does not explicitly prohibit committed secrets or constrain elevated and provider keys to server-only code paths. |
| PRD-007 | Provide app, test, reset command scripts | critical | partial | Phase 7 names `npm run test:reset` | Reset is concrete, but start-app and test scripts are not specified as package commands. |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | Section 1.1 migration tree; Section 2.2; Phase 1 |  |
| PRD-009 | Use one stable namespace per build | critical | full | Section 2.1 Namespace Primitive |  |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | Section 2.1; Phase 7; Section 7.1 integration test |  |
| PRD-011 | Attach every user record to `user_id` | critical | full | Section 2.1; Section 2.2 schema |  |
| PRD-012 | Partition persisted data by namespace and user | critical | full | Section 2.1; composite constraints and indexes in Section 2.2 |  |
| PRD-013 | Support documented dev auth injection, prod-gated | important | full | Section 2.1 Dev Identity Injection |  |
| PRD-014 | Real OAuth later needs no schema redesign | important | full | Section 2.1 explicitly promises zero schema refactoring |  |
| PRD-015 | Keep backend as persisted source of truth | critical | partial | Sections 1 and 2 use Supabase persistence for shows/settings | Server persistence is planned, but the source-of-truth boundary and prohibition on correctness-critical local state are not explicit. |
| PRD-016 | Make client cache safe to discard | critical | missing | none | The plan never defines client caching as disposable or verifies recovery after clearing browser storage. |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | full | Section 2 opening paragraph |  |
| PRD-018 | Overlay saved user data on every show appearance | critical | partial | Section 3.2 merge policy; Section 4.2 catalog resolution | Merge behavior exists, but no universal overlay step is specified for Search, recommendations, Ask mentions, Alchemy, and all other show appearances. |
| PRD-019 | Support visible statuses plus hidden `Next` | important | full | Section 2.2 enum; Sections 3.1 and 5.2 visible chips |  |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | full | Section 3.1 |  |
| PRD-021 | Support free-form multi-tag personal tag library | important | full | Executive Summary; Sections 2.2, 3.1, and 5.2 |  |
| PRD-022 | Define collection membership by assigned status | critical | full | Section 3.1 Collection Definition |  |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | full | Section 3.1 Implicit Save Triggers |  |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | Section 3.1 |  |
| PRD-025 | Removing status deletes show and all My Data | critical | full | Section 3.1 Removal Semantics; Section 7.1 tests |  |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | partial | Section 3.2 Metadata Sync & Field Merge Policy | Catalog refresh and four My-field merges are planned, but re-add behavior and AI Scoop preservation are not stated explicitly. |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | Section 2.2 schema; Section 3.2 |  |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | partial | Sections 3.2 and 4.1 use timestamps for merge and Scoop freshness | Timestamp-based sorting is not planned, and the full set of intended timestamp uses is not verified. |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | full | Section 4.1 Scoop row; Phase 5 |  |
| PRD-030 | Keep Ask and Alchemy state session-only | important | partial | Section 4.1 gives Ask session turns; Section 5.3 defines an Alchemy wizard | The plan does not explicitly keep Alchemy results transient or clear Ask/Alchemy state when leaving or resetting the mode. |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | full | Sections 4.1 and 4.2 |  |
| PRD-032 | Show collection and rating tile indicators | important | partial | Section 5.1 Show Tile Indicators | Rating is explicit, but the plan describes an active-status chip rather than a general in-collection indicator on every tile surface. |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | partial | Section 2.2 unique constraints; Section 3.2 timestamp merge | Duplicate prevention and field merges exist, but cross-device consistency and transparent duplicate reconciliation are not fully planned. |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | missing | none | An initial migration is listed, but there is no upgrade/migration strategy or acceptance test proving existing libraries and My Data survive model changes. |
| PRD-035 | Persist synced settings, local settings, UI state | important | full | Section 2.2 `user_settings` schema |  |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | partial | Section 2.2 `provider_data`; Section 5.2 detail sections | The plan does not constrain provider persistence to IDs or enumerate detail-only cast, crew, season, media, and recommendation data as transient. |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | full | Section 3.2; Phase 2 and merge tests |  |
| PRD-038 | Provide filters panel and main screen destinations | important | full | Section 1.1 routes/components; Section 5.1 |  |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | partial | Section 1.1 includes `HeaderNav` and `/find` | The destination exists, but the plan does not explicitly place Find/Discover in persistent primary navigation. |
| PRD-040 | Keep Settings in persistent primary navigation | important | partial | Section 1.1 includes `HeaderNav` and `/settings` | The destination exists, but the plan does not explicitly place Settings in persistent primary navigation. |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | Section 5.3 |  |
| PRD-042 | Show only library items matching active filters | important | full | Section 5.1; Phase 4 sidebar filtering |  |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | Section 5.1 Status Sections |  |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | full | Section 5.1 Sidebar Navigation |  |
| PRD-045 | Render poster, title, and My Data badges | important | full | Section 5.1 poster tiles and Show Tile Indicators |  |
| PRD-046 | Provide empty-library and empty-filter states | detail | missing | none | Neither the no-library prompt nor the no-results filter state is planned. |
| PRD-047 | Search by title or keywords | important | partial | Section 5.3 Search Mode | A live search query is planned, but title/keyword semantics are not stated. |
| PRD-048 | Use poster grid with collection markers | important | partial | Section 5.3 specifies a catalog search grid; Section 5.1 defines tile indicators | The Search surface is not explicitly a poster grid and is not explicitly wired to universal collection markers. |
| PRD-049 | Auto-open Search when setting is enabled | detail | full | Sections 2.2 and 5.3 |  |
| PRD-050 | Keep Search non-AI in tone | important | missing | none | The plan does not define Search as a straightforward non-AI surface or provide a tone acceptance check. |
| PRD-051 | Preserve Show Detail narrative section order | important | partial | Section 5.2 | The plan claims the prescribed hierarchy but inserts toolbar controls into the numbered body and moves My Tags after them, so it does not reproduce the specified narrative order exactly. |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | partial | Section 5.2 Header Media | Trailer playback and rich media are planned, but poster/backdrop fallback behavior is not. |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | full | Section 5.2 Core Facts |  |
| PRD-054 | Place status/interest controls in toolbar | important | full | Section 5.2 Toolbar Controls |  |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | Section 3.1; Section 7.1 tests |  |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | Section 3.1; Section 7.1 tests |  |
| PRD-057 | Show overview early for fast scanning | important | full | Section 5.2 Overview & Scoop |  |
| PRD-058 | Scoop shows correct states and progressive feedback | important | partial | Sections 4.1 and 5.2; Phase 5 | Progressive streaming and a toggle are planned, but the no-scoop, cached, open, generating, and error-state copy/behavior is not fully specified. |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | full | Section 5.2 Ask About This Show CTA |  |
| PRD-060 | Include traditional recommendations strand | important | full | Section 5.2 Traditional Recommendations |  |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | full | Section 5.2 Explore Similar |  |
| PRD-062 | Include streaming availability and person-linking credits | important | full | Sections 5.2 and 5.4 |  |
| PRD-063 | Gate seasons to TV and financials to movies | important | full | Section 5.2 items 12-13 |  |
| PRD-064 | Keep primary actions early and page not overwhelming | important | partial | Section 5.2 puts relationship and Scoop actions early | Early placement is covered, but there is no explicit density treatment that pushes optional depth down-page and prevents the 13-section page from feeling crowded. |
| PRD-065 | Provide conversational Ask chat interface | important | full | Sections 5.3 and 4.1 |  |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | partial | Section 4 and Ask row specify confidence and spoiler safety | The plan omits the quality bar requiring a direct answer within the first 3-5 lines. |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | Section 5.3 Ask Mode |  |
| PRD-068 | Open Detail from mentions or Search fallback | important | full | Section 4.2 catalog resolution and Search fallback |  |
| PRD-069 | Show six random starter prompts with refresh | important | full | Section 5.3 Ask Mode |  |
| PRD-070 | Summarize older turns while preserving voice | important | partial | Section 4.1 Ask row | Summarization after ten turns is planned, but summaries are not required to preserve the conversational persona. |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | full | Section 5.2 Ask About This Show CTA |  |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | full | Sections 4.1 and 4.2; parser tests in Section 7.1 |  |
| PRD-073 | Retry malformed mention output once, then fallback | important | missing | none | Parser tests exist, but no one-retry strategy or unstructured-commentary fallback is planned for malformed AI output. |
| PRD-074 | Redirect Ask back into TV/movie domain | important | missing | none | The AI plan does not state the domain-redirect rule or test out-of-domain prompts. |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | full | Section 4 opening and Concepts row |  |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | full | Section 4.1 Concepts row |  |
| PRD-077 | Order concepts by strongest aha and varied axes | important | partial | Section 4.1 Concepts row covers varied format, tone, emotion, and craft axes | No ordering rule puts the strongest “aha” concepts first. |
| PRD-078 | Require concept selection and guide ingredient picking | important | partial | Sections 4.1, 5.2, and 5.3 require concept selection | Selection and caps are covered, but ingredient-picking helper copy and the no-selection empty state are absent. |
| PRD-079 | Return exactly five Explore Similar recommendations | important | full | Section 4.1 Concept Recommendations row |  |
| PRD-080 | Support full Alchemy loop with chaining | important | full | Section 5.3 Alchemy Mode; Phase 6 |  |
| PRD-081 | Clear downstream results when inputs change | important | missing | none | The plan does not define invalidation of concepts/results when source shows or selected concepts change. |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | missing | none | Shared commonality is covered, but the larger multi-show concept pool is never specified. |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | full | Section 4.1 Concept Recommendations row |  |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | missing | none | Taste alignment is tested, but the required “surprise without betrayal” criterion is not planned. |
| PRD-085 | Keep one consistent AI persona across surfaces | important | full | Section 4 unified persona; Phase 5 |  |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | partial | Section 4 persona constraints; Phase 5 voice guardrails | Spoiler safety and voice are present, but the plan does not enumerate or test domain restriction, honest criticism, specificity, and actionable real-title behavior across every AI surface. |
| PRD-087 | Make AI warm, joyful, and light in critique | important | full | Section 4 unified persona |  |
| PRD-088 | Structure Scoop as personal taste mini-review | important | full | Section 4.1 Scoop row |  |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | full | Section 4.1 Ask row |  |
| PRD-090 | Feed AI the right surface-specific context inputs | important | full | Section 4.1 input-context matrix |  |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | partial | Phase 7; Section 7.2 | The threshold and real-show hard fail are present, but the plan does not explicitly score every rubric dimension, notably specificity and surprise. |
| PRD-092 | Show person gallery, name, and bio | important | partial | Section 5.4 Person Detail header | Name and bio are covered, but only a single profile image is planned rather than an image gallery. |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | full | Section 5.4 Analytics Charts |  |
| PRD-094 | Group filmography by year | important | full | Section 5.4 Filmography |  |
| PRD-095 | Open Show Detail from selected credit | important | full | Section 5.4 Filmography |  |
| PRD-096 | Include font size and Search-on-launch settings | important | full | Section 2.2 settings schema; Sections 5.3 and 6 Phase 6 |  |
| PRD-097 | Support username, model, and API-key settings safely | important | partial | Sections 2.2 and 2.3; Phase 6 Settings | The data fields exist, but the plan does not define safe user-key storage, server-only use, redaction, or settings UX for these controls. |
| PRD-098 | Export saved shows and My Data as zip | critical | full | Section 3.3; Phase 6; Section 7.2 |  |
| PRD-099 | Encode export dates using ISO-8601 | important | full | Section 3.3 |  |

### 3. Coverage Scores

score = (62 full × 1.0 + 27 partial × 0.5) / 99 total_count × 100 = 76.3%

Critical:  (21 full × 1.0 + 7 partial × 0.5) / 30 critical_total × 100 = 81.7%  (24.5 of 30 critical requirements)
Important: (40 full × 1.0 + 20 partial × 0.5) / 67 important_total × 100 = 74.6%  (50 of 67 important requirements)
Detail:    (1 full × 1.0 + 0 partial × 0.5) / 2 detail_total × 100 = 50.0%  (1 of 2 detail requirements)
Overall:   76.3% (99 total requirements)

### 4. Top Gaps

1. PRD-016 | critical | Make client cache safe to discard

   This omission leaves a data-loss ambiguity: an implementation could accidentally treat browser storage as authoritative, causing cleared local state or a reinstall to lose user-owned data despite the Supabase schema.

2. PRD-034 | critical | Preserve saved libraries across data-model upgrades

   An initial migration does not establish continuity. Without an explicit upgrade strategy and regression fixture, later schema changes can silently drop statuses, tags, ratings, interest, or Scoop data.

3. PRD-006 | critical | Keep secrets out of repo and server-only

   The plan exposes the right environment variable categories but does not define trust boundaries. Provider keys or the Supabase service-role key could be bundled into client code, logged, or committed without explicit implementation and verification rules.

4. PRD-018 | critical | Overlay saved user data on every show appearance

   A generic merge utility is not enough to guarantee consistent UI. Without a universal overlay pipeline, the same show may lose collection badges or display stale My Data in Search, Ask mentions, Alchemy, or recommendation strands.

5. PRD-007 | critical | Provide app, test, reset command scripts

   The reset command is named, but missing start and test script deliverables weaken the benchmark’s one-command execution contract and can leave agents or reviewers unable to run the planned verification consistently.

### 5. Coverage Narrative

#### Overall Posture

The plan is structurally sound and implementation-oriented, but it is not yet comprehensive enough to execute without material interpretation. Its core schema, collection rules, page inventory, and principal AI flows are strong. The 76.3% score reflects a plan with a viable foundation and several important contract gaps rather than a plan missing the product’s central architecture.

#### Strength Clusters

Coverage is strongest in Collection Data & Persistence’s basic save/remove rules, the main Show Detail & Relationship UX flow, the core Ask Chat interface, Person Detail analytics and navigation, and Settings & Export. The plan is particularly concrete about namespace/user partitioning, the Supabase schema, status defaults, timestamp-based merge logic, structured Ask mentions, recommendation resolution, fixed recommendation counts, and zip export.

#### Weakness Clusters

The most consequential gaps cluster in Benchmark Runtime & Isolation and the deeper durability requirements of Collection Data & Persistence: disposable caches, secret boundaries, command scripts, universal overlays, and upgrade continuity are not fully specified. A second cluster concerns behavioral acceptance details across Collection Home & Search, Ask Chat, and Concepts/Alchemy—empty states, non-AI Search tone, parser fallback, domain redirection, state invalidation, multi-show concept pool sizing, and recommendation surprise.

#### Risk Assessment

If implemented as written, the app would likely demo its happy paths successfully while failing consistency, resilience, and edge-case review. QA would first notice saved shows presenting different My Data across surfaces, browser-state assumptions after storage is cleared, missing recovery behavior for malformed AI output, and Alchemy results that remain stale after users backtrack. Security review could also find provider or elevated keys without an explicit server-only handling contract.

#### Remediation Guidance

The plan needs targeted specification and acceptance-criteria work rather than a new architecture. Add explicit trust and source-of-truth boundaries, cache-clearing and migration-continuity tests, complete package-script deliverables, and one shared show-overlay path. Then tighten surface contracts with concrete empty/error states, AI retry/domain rules, Alchemy invalidation behavior, concept-pool sizing, Search tone, and complete quality-rubric checks.
