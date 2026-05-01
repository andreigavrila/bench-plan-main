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
| PRD-001 | Use Next.js latest stable runtime | critical | full | 1.1 Tech Stack: "Runtime: Next.js (latest stable) with App Router" | |
| PRD-002 | Use Supabase official client libraries | critical | full | 1.1 Tech Stack: "Persistence: Supabase (PostgreSQL + client libraries)" | |
| PRD-003 | Ship `.env.example` with required variables | critical | full | 1.2 Required Deliverables: ".env.example" with all required variables | |
| PRD-004 | Ignore `.env*` secrets except example | important | partial | 1.2 Required Deliverables: ".gitignore excluding .env* files" | The exception to keep `.env.example` committed is implied by the deliverables list but never stated in the ignore rule. |
| PRD-005 | Configure build through env without code edits | critical | partial | 1.2 Required Deliverables | The plan enumerates env files and configurable providers but never states that a build must be runnable solely by setting env vars with no source edits. |
| PRD-006 | Keep secrets out of repo and server-only | critical | partial | 1.2 Required Deliverables: "no secrets committed" | It does not define client-safe vs server-only secrets or keep elevated backend credentials off the browser. |
| PRD-007 | Provide app, test, reset command scripts | critical | full | 1.2 Required Deliverables: `npm run dev`, `npm test`, `npm run test:reset` | |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | 1.2 Required Deliverables: "Database migrations for repeatable schema setup" | |
| PRD-009 | Use one stable namespace per build | critical | partial | 1.3 Infrastructure Isolation: "All data scoped by namespace_id" | Isolation is described, but the plan does not operationalize one stable namespace per build lifetime. |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | 1.2 Required Deliverables: "reset test data for namespace" + 1.3 Infrastructure Isolation | |
| PRD-011 | Attach every user record to `user_id` | critical | full | 1.3 Infrastructure Isolation: "All user-owned records include user_id" | |
| PRD-012 | Partition persisted data by namespace and user | critical | full | 5.3 Supabase Backend: "All tables include `namespace_id` and `user_id` for isolation" | |
| PRD-013 | Support documented dev auth injection, prod-gated | important | partial | 1.3 Infrastructure Isolation: "`X-User-Id` header or equivalent for development" | The dev auth path is named but not documented as production-gated or explicitly disabled outside dev/test. |
| PRD-014 | Real OAuth later needs no schema redesign | important | full | 1.3 Infrastructure Isolation: "Auth mechanism swappable without schema redesign" | |
| PRD-015 | Keep backend as persisted source of truth | critical | full | 7. Cross-Cutting Concerns: "Backend as source of truth" | |
| PRD-016 | Make client cache safe to discard | critical | full | 7. Cross-Cutting Concerns: "Correctness not dependent on local persistence" | |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | missing | none | Docker optionality and cloud-agent compatibility are never addressed. |
| PRD-018 | Overlay saved user data on every show appearance | critical | full | 7. Cross-Cutting Concerns: "My Data always displays over refreshed public data" | |
| PRD-019 | Support visible statuses plus hidden `Next` | important | missing | none | The plan omits the hidden data-model-only `Next` status and even narrows the status enum to five visible states. |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | full | 4.2 Status System: "Selecting either sets `myStatus = later` + appropriate `myInterest`" | |
| PRD-021 | Support free-form multi-tag personal tag library | important | full | 2.1 Core Entities: `myTags` + 3.1 Navigation Layout tag filters | |
| PRD-022 | Define collection membership by assigned status | critical | partial | 4.1 Collection Management + 4.2 Status System | Status drives most behaviors, but the plan never states collection membership is defined solely by assigned status. |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | full | 4.1 Collection Management: Saving Triggers | |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | 4.1 Collection Management: Default Values on Save | |
| PRD-025 | Removing status deletes show and all My Data | critical | partial | 4.1 Collection Management: "Clears all My Data" | The removal flow clears overlay data but does not explicitly say the show record is deleted from collection storage. |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | missing | none | Re-adding a previously removed show and restoring prior My Data is not planned at all. |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | 2.1 Core Entities: per-field `my*UpdateDate` and `aiScoopUpdateDate` | |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | partial | 2.2 Merge Rules + 4.4 AI Scoop | Timestamps are used for merge and freshness, but the plan does not tie them to sorting behavior. |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | full | 4.4 AI Scoop: "Cached for 4 hours" and "Only persists if show is in collection" | |
| PRD-030 | Keep Ask and Alchemy state session-only | important | full | 4.5 Data Persistence Rules | |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | full | 4.3 Explore Similar: "Recommendations map to real catalog items" + 7. Cross-Cutting Concerns | |
| PRD-032 | Show collection and rating tile indicators | important | partial | 3.2 Collection Home + 4.3 Search | Collection and rating indicators are planned on some tiles, but not as a consistent tile rule across all result surfaces. |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | partial | 2.2 Merge Rules + 8. Phases: "Data sync (future-ready)" | Sync and duplicate-merge behavior is acknowledged but not specified concretely enough to execute. |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | partial | 2.1 AppMetadata + 1.2 Database migrations | The plan hints at versioning but never defines a continuity or migration path that preserves existing libraries through model upgrades. |
| PRD-035 | Persist synced settings, local settings, UI state | important | partial | 2.1 CloudSettings + 3.2 Settings | Some settings are covered, but local settings and UI-state persistence are not fully specified. |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | partial | 2.3 External Catalog Mapping | The plan covers transient detail fetches but never plans persisted provider-ID storage. |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | full | 2.2 Merge Rules | |
| PRD-038 | Provide filters panel and main screen destinations | important | full | 3.1 Navigation Layout | |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | partial | 3.1 Navigation Layout | Find/Discover exists in the layout, but the plan does not explicitly commit it to persistent primary navigation. |
| PRD-040 | Keep Settings in persistent primary navigation | important | partial | 3.1 Navigation Layout | Settings is listed as a destination, not explicitly as a persistent primary-nav entry. |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | 3.2 Find/Discover Hub: "Mode switcher: Search / Ask / Alchemy" | |
| PRD-042 | Show only library items matching active filters | important | partial | 3.1 Navigation Layout + 3.2 Collection Home | The plan defines filters and home sections, but not the explicit rule that Home only shows items matching the active filters. |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | 3.2 Collection Home | |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | full | 3.1 Navigation Layout | |
| PRD-045 | Render poster, title, and My Data badges | important | full | 3.2 Collection Home: "poster, title, status badges, user rating badge" | |
| PRD-046 | Provide empty-library and empty-filter states | detail | partial | 3.2 Collection Home: "Empty state: prompt to Search/Ask" | The empty-library state is planned, but the empty-filter state is not. |
| PRD-047 | Search by title or keywords | important | partial | 4.3 Search: "Live text search against external catalog" | Title search is clear, but keyword behavior is not explicitly planned. |
| PRD-048 | Use poster grid with collection markers | important | full | 4.3 Search: "Poster grid results" and "In-collection items marked" | |
| PRD-049 | Auto-open Search when setting is enabled | detail | partial | 3.2 Settings: "Search on launch toggle" | The setting exists, but the plan does not state that launch should automatically open Search when enabled. |
| PRD-050 | Keep Search non-AI in tone | important | missing | none | The plan never calls out Search as a deliberately non-AI, straight catalog experience. |
| PRD-051 | Preserve Show Detail narrative section order | important | partial | 3.2 Show Detail Page | The plan lists the major sections but changes the required narrative order, especially around tags, overview, and Ask placement. |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | partial | 3.2 Show Detail Page: "Header media carousel (backdrops/posters/logos/trailers)" | It prioritizes rich header media, but graceful fallback behavior is not planned. |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | full | 3.2 Show Detail Page: "Core facts row (year/length) + community score" | |
| PRD-054 | Place status/interest controls in toolbar | important | full | 3.2 Show Detail Page: "My Status + Interest chips (toolbar)" | |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | 4.1 Collection Management: "Adding tag to unsaved show → defaults to Later + Interested" | |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | 4.1 Collection Management: "Rating an unsaved show → defaults to Done" | |
| PRD-057 | Show overview early for fast scanning | important | partial | 3.2 Show Detail Page: "Overview text + Scoop toggle" | Overview is included, but not explicitly kept early enough to support fast scanning. |
| PRD-058 | Scoop shows correct states and progressive feedback | important | partial | 4.4 AI Scoop | Freshness and streaming are planned, but the detail-state UX copy and progressive status behavior are not. |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | full | 4.3 Ask: "Ask about this show variant: seeds conversation with show context" | |
| PRD-060 | Include traditional recommendations strand | important | full | 3.2 Show Detail Page: "Traditional recommendations strand" | |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | full | 3.2 Show Detail Page + 4.3 Explore Similar | |
| PRD-062 | Include streaming availability and person-linking credits | important | full | 3.2 Show Detail Page: "Streaming availability" and "Cast & Crew ... → Person Detail" | |
| PRD-063 | Gate seasons to TV and financials to movies | important | full | 3.2 Show Detail Page: "Seasons (TV only)" and "Budget/Revenue (movies)" | |
| PRD-064 | Keep primary actions early and page not overwhelming | important | partial | 3.2 Show Detail Page | The plan clusters many actions on the page but never addresses the anti-overwhelm principle or information-density control. |
| PRD-065 | Provide conversational Ask chat interface | important | full | 4.3 Ask: "Chat UI with user/assistant turns" | |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | partial | 4.3 Ask + 4.4 AI Voice Personality | The voice is described, but the plan does not explicitly require Ask to answer directly and confidently in its opening lines. |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | 4.3 Ask: "horizontal mentioned shows strip" | |
| PRD-068 | Open Detail from mentions or Search fallback | important | partial | 4.3 Ask: "Tapping mentioned show opens Detail" | Search handoff when mapping fails is missing from the interaction contract. |
| PRD-069 | Show six random starter prompts with refresh | important | partial | 4.3 Ask: "80 starter prompts (refreshable)" | The plan captures prompts and refresh, but not the required six random starters shown per welcome state. |
| PRD-070 | Summarize older turns while preserving voice | important | partial | 4.3 Ask: "older turns summarized after ~10 messages" | Summarization is planned, but not the requirement to preserve the same conversational voice in the summary. |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | full | 4.3 Ask: "Ask about this show variant: seeds conversation with show context" | |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | full | 4.3 Ask: "Structured output: `{ commentary: string, showList: ... }`" | |
| PRD-073 | Retry malformed mention output once, then fallback | important | missing | none | There is no malformed-output retry-once then fallback plan for Ask mentions parsing. |
| PRD-074 | Redirect Ask back into TV/movie domain | important | missing | none | The plan never defines how Ask should redirect out-of-domain requests back into TV/movie discovery. |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | partial | 4.4 Concept Generation | The plan describes concept axes, but not the core product framing that concepts are taste ingredients rather than genres. |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | full | 4.4 Concept Generation: "1-3 word evocative bullets" and "Specific over generic" | |
| PRD-077 | Order concepts by strongest aha and varied axes | important | full | 4.4 Concept Generation: "Ordered by strength/aha factor" + concept axes | |
| PRD-078 | Require concept selection and guide ingredient picking | important | partial | 4.3 Explore Similar + 4.3 Alchemy | Selection is required, but the plan omits the UX guidance that frames concept picking as choosing ingredients. |
| PRD-079 | Return exactly five Explore Similar recommendations | important | full | 4.3 Explore Similar: "5 AI recommendations" | |
| PRD-080 | Support full Alchemy loop with chaining | important | full | 4.3 Alchemy | |
| PRD-081 | Clear downstream results when inputs change | important | partial | 4.3 Alchemy: "changing shows clears concepts/results" | It only plans clearing on show changes, not the broader rule that downstream results clear whenever inputs change. |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | partial | 4.3 Alchemy: "AI extracts shared concepts" | Shared concepts are planned, but not the larger option pool expected for multi-show conceptualization. |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | full | 4.4 Concept-Based Recommendations: "Reasons cite specific concepts" | |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | partial | 4.4 Concept-Based Recommendations | The plan names concept-grounded recs, but not the quality bar of surprising yet defensible taste alignment. |
| PRD-085 | Keep one consistent AI persona across surfaces | important | full | 4.4 AI Voice Personality + 8. Phase 4: "AI voice consistency across surfaces" | |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | partial | 4.4 AI Voice Personality + 7. Cross-Cutting Concerns | Some shared rules appear, but the plan does not define a complete cross-surface guardrail contract with enforcement and fallback expectations. |
| PRD-087 | Make AI warm, joyful, and light in critique | important | partial | 4.4 AI Voice Personality: "Fun, chatty TV/movie nerd friend" | Warmth is present, but the plan does not explicitly preserve the joyful, light-in-critique behavior. |
| PRD-088 | Structure Scoop as personal taste mini-review | important | full | 4.4 AI Scoop: "personal take → honest stack-up → Scoop centerpiece → fit/warnings → verdict" | |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | partial | 4.3 Ask: "Conversational discovery" | Dialogue is planned, but not the default brisk pacing and concise response behavior. |
| PRD-090 | Feed AI the right surface-specific context inputs | important | missing | none | The plan never specifies the shared and surface-specific context inputs AI calls must receive. |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | partial | 7. Cross-Cutting Concerns: "All recommendations map to real catalog shows" | Integrity is emphasized, but there is no planned rubric or validation loop for voice, taste alignment, and hard-fail scoring. |
| PRD-092 | Show person gallery, name, and bio | important | full | 3.2 Person Detail Page: "Image gallery, name, bio" | |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | full | 3.2 Person Detail Page: "Analytics charts (ratings, genres, projects-by-year)" | |
| PRD-094 | Group filmography by year | important | full | 3.2 Person Detail Page: "Filmography grouped by year" | |
| PRD-095 | Open Show Detail from selected credit | important | full | 3.2 Person Detail Page: "Credits → Show Detail" | |
| PRD-096 | Include font size and Search-on-launch settings | important | full | 3.2 Settings: "Font size selector" and "Search on launch toggle" | |
| PRD-097 | Support username, model, and API-key settings safely | important | partial | 3.2 Settings | The plan includes username, model, and API-key settings, but it does not define the safe handling boundaries for stored keys. |
| PRD-098 | Export saved shows and My Data as zip | critical | full | 3.2 Settings: "Export My Data button (generates .zip with JSON backup)" | |
| PRD-099 | Encode export dates using ISO-8601 | important | missing | none | The export plan omits the ISO-8601 date-encoding requirement. |

## 3. Coverage Scores

Overall:

`score = (full_count × 1.0 + partial_count × 0.5) / total_count × 100`

Critical:  (22 × 1.0 + 7 × 0.5) / 30 × 100 = 85.0%  (25.5 of 30 critical requirements weighted coverage)
Important: (31 × 1.0 + 29 × 0.5) / 67 × 100 = 67.9%  (45.5 of 67 important requirements weighted coverage)
Detail:    (0 × 1.0 + 2 × 0.5) / 2 × 100 = 50.0%  (1.0 of 2 detail requirements weighted coverage)
Overall:   (53 × 1.0 + 38 × 0.5) / 99 × 100 = 72.7%  (72.0 of 99 requirements weighted coverage)

## 4. Top Gaps

1. PRD-026 | `critical` | Re-add preserves My Data and refreshes public data
Without this flow, a user can lose tags, ratings, status history, and Scoop metadata permanently after removing and later rediscovering the same show, which breaks the product's continuity promise.

2. PRD-086 | `critical` | Enforce shared AI guardrails across all surfaces
Without a unified guardrail contract, Ask, Scoop, Alchemy, and Explore Similar can drift on spoilers, domain limits, honesty, and output structure, creating visible behavioral inconsistency and benchmark failures.

3. PRD-025 | `critical` | Removing status deletes show and all My Data
If removal semantics are under-specified, the implementation can leave orphaned records or mismatched UI/backend state, which users and QA will notice as "removed" items still behaving as saved.

4. PRD-034 | `critical` | Preserve saved libraries across data-model upgrades
If upgrade continuity is not planned now, later schema changes can silently wipe or mis-map saved libraries, causing high-severity regression after an otherwise successful initial launch.

5. PRD-009 | `critical` | Use one stable namespace per build
If namespace lifetime is not nailed down, benchmark runs can collide or reset each other's data, undermining repeatability and making test failures hard to trust.

## 5. Coverage Narrative

#### Overall Posture

This is a structurally sound plan with concerning holes. It covers the product's main surfaces, data entities, and most benchmark scaffolding, but it under-specifies several high-severity behavioral contracts that the benchmark treats as non-negotiable.

#### Strength Clusters

The plan is strongest in Benchmark Runtime & Isolation fundamentals, core Collection Data & Persistence mechanics, the major App Navigation and Show Detail surfaces, Person Detail, and the baseline Settings and Export surface. The author clearly understands the major screens, the primary save triggers, the core data model, and the benchmark's namespace plus `user_id` framing.

#### Weakness Clusters

The gaps cluster in two patterns. First, AI behavioral contracts are repeatedly softened from explicit product rules into broad implementation intent, especially in Ask Chat, Concepts/Alchemy quality, and shared AI Voice and guardrail requirements. Second, data-lifecycle edge cases are weakly covered, especially re-add semantics, upgrade continuity, provider persistence, and the exact removal and filter behaviors that keep the collection model coherent.

#### Risk Assessment

If this plan were executed as-is, the app would likely look broadly complete but fail in the places the benchmark is strictest about exact behavior. QA would first notice that AI surfaces do not fully honor the required contracts for starter prompts, retry/fallback behavior, domain redirection, and shared context/guardrails, while product reviewers would also catch collection edge cases like removed shows not being truly deleted or prior My Data not surviving a re-add flow.

#### Remediation Guidance

The missing work is mostly not "more implementation detail" in the generic sense; it needs sharper behavioral planning. The plan should add explicit sections for lifecycle invariants and edge cases in collection persistence, a dedicated AI contract section that turns voice/guardrails/fallbacks into executable requirements, and a benchmark-operations section that specifies namespace lifecycle, Docker expectations, env-only configuration, and secure server/client secret boundaries. Those additions would convert many current partials into full coverage without changing the overall architecture.
