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
| PRD-001 | Use Next.js latest stable runtime | critical | full | `3. Technical Baseline`: "Next.js latest stable, App Router, TypeScript." |  |
| PRD-002 | Use Supabase official client libraries | critical | full | `3. Technical Baseline`: "Supabase as persistence, accessed through official Supabase client libraries." |  |
| PRD-003 | Ship `.env.example` with required variables | critical | full | `4. Repository Deliverables` and `5. Environment and Identity Model` list `.env.example` and required variables. |  |
| PRD-004 | Ignore `.env*` secrets except example | important | full | `4. Repository Deliverables`: `.gitignore` "Excludes `.env*` secrets while allowing `.env.example`." |  |
| PRD-005 | Configure build through env without code edits | critical | full | `5. Environment and Identity Model`: defines the environment contract before feature work. |  |
| PRD-006 | Keep secrets out of repo and server-only | critical | full | `3. Technical Baseline` and `18. Security and Privacy Plan` require server-only elevated keys and no committed secrets. |  |
| PRD-007 | Provide app, test, reset command scripts | critical | full | `4. Repository Deliverables`: `npm run dev`, `npm test`, `npm run test:reset`, `npm run db:migrate`. |  |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | `4. Repository Deliverables`: `supabase/migrations/`; `20. Data Continuity and Migration Plan`. |  |
| PRD-009 | Use one stable namespace per build | critical | full | `5. Environment and Identity Model`: "`namespace_id` is stable for the lifetime of a run/build." |  |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | `15. Namespace Reset and Test Isolation`: reset deletes only `namespace_id = target`. |  |
| PRD-011 | Attach every user record to `user_id` | critical | full | `7.2 user_show_overlays` and `7.3 cloud_settings` include `user_id`; `23. Definition of Done` repeats this. |  |
| PRD-012 | Partition persisted data by namespace and user | critical | full | `1. Objective`: "User-owned persisted data is always scoped by `(namespace_id, user_id)`." |  |
| PRD-013 | Support documented dev auth injection, prod-gated | important | full | `5. Environment and Identity Model`: header/selector/default identity and production gating; `README.md` deliverable. |  |
| PRD-014 | Real OAuth later needs no schema redesign | important | full | `18. Security and Privacy Plan`: "Prepare schema for future OAuth by keeping `user_id` opaque." |  |
| PRD-015 | Keep backend as persisted source of truth | critical | full | `1. Objective`: "Supabase is the backend source of truth; browser/local storage is disposable." |  |
| PRD-016 | Make client cache safe to discard | critical | full | `17. E2E Journeys`: "Clear browser storage -> reload -> collection still present from Supabase." |  |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | full | `3. Technical Baseline`: "No Docker requirement. Hosted Supabase is the primary path." |  |
| PRD-018 | Overlay saved user data on every show appearance | critical | full | `1. Objective`: "Every surface that displays a saved show must display the user's overlaid version." |  |
| PRD-019 | Support visible statuses plus hidden `Next` | important | full | `7.2 user_show_overlays` includes `next`; `21. Key Product Decisions`: "`Next` remains in the data model but is not a first-class UI status." |  |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | full | `12.3 Show Detail Page`: Interested/Excited set `my_status = later` and corresponding `my_interest`. |  |
| PRD-021 | Support free-form multi-tag personal tag library | important | full | `12.1 Collection Home`: "Derive tag library from overlays"; `7.2` stores `my_tags text[]`. |  |
| PRD-022 | Define collection membership by assigned status | critical | full | `7.2 user_show_overlays`: "A show is in collection when `my_status is not null`." |  |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | full | `12.3 Show Detail Page`: setting status, rating, and tagging all save; interest chips map to save. |  |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | `12.3 Show Detail Page`: rating unsaved saves Done; tagging saves Later + Interested. |  |
| PRD-025 | Removing status deletes show and all My Data | critical | full | `12.3 Show Detail Page`: "Clearing status removes the show and clears My Data." |  |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | full | `8. Persistence and Merge Rules` and `16. Milestone 4 Acceptance`: "Refreshing details preserves user edits." |  |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | `7.2 user_show_overlays` lists update-date columns for status, interest, score, tags, and scoop. |  |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | full | `8. Persistence and Merge Rules`, `12.1`, and `20. Data Continuity` cover timestamp merge, sorting, and Scoop freshness. |  |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | full | `12.3 Show Detail Page`: "Cache for 4 hours" and "Persist only if the show is in collection." |  |
| PRD-030 | Keep Ask and Alchemy state session-only | important | full | `11. Application Shell and Routing` and `21. Key Product Decisions` keep Ask/Alchemy local/session-only. |  |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | full | `9. Catalog Provider Layer`: detailed AI recommendation resolution rule and unresolved fallback. |  |
| PRD-032 | Show collection and rating tile indicators | important | full | `12.1 Collection Home`: tile displays in-collection indicator and rating badge. |  |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | partial | `7.3 cloud_settings`, `8. Persistence and Merge Rules`, and namespace/user scoping cover sync consistency. | The plan does not explicitly require duplicate item detection and transparent duplicate merging. |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | full | `20. Data Continuity and Migration Plan`: preserve saved shows and My Data through schema changes. |  |
| PRD-035 | Persist synced settings, local settings, UI state | important | full | `11. Application Shell and Routing` and `12.8 Settings and Your Data` distinguish synced settings, local settings, and UI state. |  |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | partial | `7.1 catalog_shows` stores `provider_data`; `7.5 Optional Normalized Tables` says credits can remain transient. | It does not explicitly constrain persisted provider data to provider IDs only or list all transient detail fetches. |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | full | `8. Persistence and Merge Rules`: `selectFirstNonEmpty`, timestamp conflict resolution, `details_update_date`, `creation_date`. |  |
| PRD-038 | Provide filters panel and main screen destinations | important | full | `11. Application Shell and Routing`: navigation/filter panel and main routes. |  |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | full | `11. Application Shell and Routing`: "Persistent Find/Discover entry point." |  |
| PRD-040 | Keep Settings in persistent primary navigation | important | full | `11. Application Shell and Routing`: "Persistent Settings entry point." |  |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | `11. Application Shell and Routing`: `/find?mode=search|ask|alchemy`. |  |
| PRD-042 | Show only library items matching active filters | important | full | `12.1 Collection Home`: "Apply selected sidebar filter plus media type toggle." |  |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | `12.1 Collection Home`: lists Active, Excited, Interested, Other grouping rules. |  |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | full | `12.1 Collection Home`: lists All, tag, no-tag, genre, decade, score, media toggle. |  |
| PRD-045 | Render poster, title, and My Data badges | important | full | `12.1 Collection Home`: "Tile displays poster, title, in-collection indicator, and rating badge." |  |
| PRD-046 | Provide empty-library and empty-filter states | detail | full | `12.1 Collection Home`: no collection and filter-yields-none empty states. |  |
| PRD-047 | Search by title or keywords | important | full | `12.2 Search`: "Text search by title/keywords." |  |
| PRD-048 | Use poster grid with collection markers | important | full | `12.2 Search`: "Poster grid results" and "In-collection items marked." |  |
| PRD-049 | Auto-open Search when setting is enabled | detail | full | `12.2 Search`: "If user setting `autoSearch` is enabled, launch into Search on app load." |  |
| PRD-050 | Keep Search non-AI in tone | important | full | `13. AI System Plan`: "Search has no AI voice." |  |
| PRD-051 | Preserve Show Detail narrative section order | important | full | `12.3 Show Detail Page`: preserves the 12-section narrative hierarchy. |  |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | full | `12.3 Show Detail Page`: "Header media carousel with trailer/backdrop/poster/logo fallback." |  |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | full | `12.3 Show Detail Page`: second section is core facts row with year, runtime/seasons, community score. |  |
| PRD-054 | Place status/interest controls in toolbar | important | full | `12.3 Show Detail Page`: "Put status/interest chips in the toolbar." |  |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | `12.3 Show Detail Page`: "Adding a tag to an unsaved show auto-saves as Later + Interested." |  |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | `12.3 Show Detail Page`: "Rating an unsaved show auto-saves as Done." |  |
| PRD-057 | Show overview early for fast scanning | important | full | `12.3 Show Detail Page`: Overview appears as section 4 after header, facts, and tags. |  |
| PRD-058 | Scoop shows correct states and progressive feedback | important | full | `12.3 Show Detail Page`: toggle copy states, progressive stream, and generating/open/cached component tests. |  |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | full | `12.4 Ask`: "Ask About This Show enters Ask with show context seeded." |  |
| PRD-060 | Include traditional recommendations strand | important | full | `12.3 Show Detail Page`: "Traditional recommendations strand." |  |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | full | `12.6 Explore Similar`: Get Concepts, select concepts, Explore Shows. |  |
| PRD-062 | Include streaming availability and person-linking credits | important | full | `12.3 Show Detail Page`: streaming providers plus cast and crew; `12.7 Person Detail`. |  |
| PRD-063 | Gate seasons to TV and financials to movies | important | full | `12.3 Show Detail Page`: "TV/movie-specific facts render conditionally." |  |
| PRD-064 | Keep primary actions early and page not overwhelming | important | full | `22. Risks and Mitigations`: primary actions in toolbar and optional depth lower on page. |  |
| PRD-065 | Provide conversational Ask chat interface | important | full | `12.4 Ask`: "Chat UI with user and assistant turns." |  |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | full | `12.4 Ask`: spoiler-safe, direct answer, bullets, warm and opinionated. |  |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | `12.4 Ask`: "Mentioned shows render in a horizontal strip." |  |
| PRD-068 | Open Detail from mentions or Search fallback | important | full | `12.4 Ask`: tapping opens Detail if resolved or Search if unresolved. |  |
| PRD-069 | Show six random starter prompts with refresh | important | full | `12.4 Ask`: "Welcome view presents 6 random starter prompts and a refresh action." |  |
| PRD-070 | Summarize older turns while preserving voice | important | full | `13. AI System Plan`: summarize older turns into persona-consistent sentences after about 10 messages. |  |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | full | `12.4 Ask`: Ask About This Show handoff with show context seeded. |  |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | full | `12.4 Ask`: structured output with `commentary` and exact `showList` format. |  |
| PRD-073 | Retry malformed mention output once, then fallback | important | full | `12.4 Ask`: parser retry once with stricter formatting, then commentary/Search handoff. |  |
| PRD-074 | Redirect Ask back into TV/movie domain | important | full | `12.4 Ask`: "Stay in TV/movies"; `16. Milestone 6 Acceptance`. |  |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | partial | `12.6 Explore Similar`: UI copy should imply "pick the ingredients you want more of"; `13. AI System Plan` is vibe-first. | The plan does not explicitly prohibit genre labels or define concepts as non-genre taste DNA. |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | full | `12.5 Alchemy` and `13. AI System Plan`: bullet-only, 1 to 3 words, non-generic concepts. |  |
| PRD-077 | Order concepts by strongest aha and varied axes | important | missing | none | The plan lacks requirements for concept ordering by strongest "aha" and diversity across axes. |
| PRD-078 | Require concept selection and guide ingredient picking | important | full | `12.5 Alchemy` and `12.6 Explore Similar`: user selects concepts; copy implies picking ingredients. |  |
| PRD-079 | Return exactly five Explore Similar recommendations | important | full | `12.6 Explore Similar`: "AI returns 5 recommendations." |  |
| PRD-080 | Support full Alchemy loop with chaining | important | full | `12.5 Alchemy`: six-step flow plus "More Alchemy!" chaining. |  |
| PRD-081 | Clear downstream results when inputs change | important | full | `12.5 Alchemy`: changing input shows or concepts clears downstream results. |  |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | partial | `12.5 Alchemy`: "AI returns shared concept catalysts"; `16. Milestone 7` includes multi-show shared concepts. | The plan covers shared multi-show concepts but does not require a larger option pool than single-show concept generation. |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | full | `12.5 Alchemy`: "Reasons explicitly name selected concepts." |  |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | full | `13. AI System Plan` and `17. AI Quality Tests`: score "Surprise without betrayal" and taste alignment. |  |
| PRD-085 | Keep one consistent AI persona across surfaces | important | full | `13. AI System Plan`: shared persona requirements across surfaces. |  |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | full | `13. AI System Plan`: shared guardrails; `12.4 Ask` and `18. Security and Privacy Plan`. |  |
| PRD-087 | Make AI warm, joyful, and light in critique | important | full | `13. AI System Plan`: "Joy-forward and warm" and "Opinionated honesty." |  |
| PRD-088 | Structure Scoop as personal taste mini-review | important | full | `13. AI System Plan`: Scoop is a 150 to 350 word mini taste review with required parts. |  |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | full | `13. AI System Plan`: "Ask is conversational, direct, and low-friction." |  |
| PRD-090 | Feed AI the right surface-specific context inputs | important | full | `13. AI System Plan`: library/My Data, show context, selected concepts, recent turns. |  |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | full | `17. AI Quality Tests`: voice, taste alignment, real-show integrity = 2, total >= 7/10. |  |
| PRD-092 | Show person gallery, name, and bio | important | full | `12.7 Person Detail`: displays image gallery, name, and bio. |  |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | full | `12.7 Person Detail`: average project ratings, top genres, projects by year. |  |
| PRD-094 | Group filmography by year | important | full | `12.7 Person Detail`: "Shows filmography/credits grouped by year." |  |
| PRD-095 | Open Show Detail from selected credit | important | full | `12.7 Person Detail`: selecting a credit opens Show Detail. |  |
| PRD-096 | Include font size and Search-on-launch settings | important | full | `12.8 Settings and Your Data`: font size/readability and Search on Launch toggle. |  |
| PRD-097 | Support username, model, and API-key settings safely | important | full | `12.8 Settings and Your Data` and `18. Security and Privacy Plan`: username, AI model, API keys, safe handling. |  |
| PRD-098 | Export saved shows and My Data as zip | critical | full | `12.8 Settings and Your Data`: "Produces a `.zip`" with saved shows and My Data. |  |
| PRD-099 | Encode export dates using ISO-8601 | important | full | `12.8 Settings and Your Data`: "Dates encoded ISO-8601"; `17. Unit Tests` covers date serialization. |  |

### 3. Coverage Scores

```
score = (full_count × 1.0 + partial_count × 0.5) / total_count × 100
```

Critical:  (30 × 1.0 + 0 × 0.5) / 30 × 100 = 100.00%  (30.0 of 30 critical requirements)
Important: (62 × 1.0 + 4 × 0.5) / 67 × 100 = 95.52%  (64.0 of 67 important requirements)
Detail:    (2 × 1.0 + 0 × 0.5) / 2 × 100 = 100.00%  (2.0 of 2 detail requirements)
Overall:   96.97% (99 total requirements)

### 4. Top Gaps

1. PRD-077 (`important`) - Order concepts by strongest aha and varied axes.
   This matters because concept quality is a core differentiator of Explore Similar and Alchemy; without ordering and axis diversity, the AI can return a flat list of repetitive or weak ingredients that still passes basic formatting checks.

2. PRD-082 (`important`) - Generate shared multi-show concepts with larger option pool.
   This matters because Alchemy needs enough shared concept candidates for users to steer the blend; using the same small pool as single-show concepts can make multi-show discovery feel constrained.

3. PRD-033 (`important`) - Sync libraries/settings consistently and merge duplicates.
   This matters because duplicate saved items or duplicate settings records can undermine trust in collection integrity, especially across devices or repeated catalog refreshes.

4. PRD-036 (`important`) - Keep provider IDs persisted and detail fetches transient.
   This matters because over-persisting provider/detail payloads can make stale third-party data harder to refresh and blur the boundary between durable user data and re-fetchable catalog detail.

5. PRD-075 (`important`) - Treat concepts as taste ingredients, not genres.
   This matters because genre-like concepts collapse the product's "taste DNA" promise into ordinary filtering, making Explore Similar and Alchemy less distinctive.

### 5. Coverage Narrative

#### Overall Posture

This is a strong implementation plan with high coverage of the PRD and no critical omissions. It is especially strong on infrastructure, persistence boundaries, user overlay behavior, and the main product journeys. The remaining gaps are real but narrow: they mostly concern exact concept-generation quality rules and a couple of lower-level persistence constraints.

#### Strength Clusters

The strongest areas are Benchmark Runtime & Isolation, App Navigation & Discover Shell, Show Detail & Relationship UX, Ask Chat, AI Voice, Person Detail, and Settings & Export. The plan repeatedly translates PRD behavior into schema, API, feature milestones, tests, and acceptance criteria, which makes most requirements actionable rather than aspirational.

#### Weakness Clusters

The partial and missing coverage clusters around Concepts, Explore Similar & Alchemy, with smaller persistence gaps in Collection Data & Persistence. The pattern is not missing feature screens; it is missing precision in behavioral contracts: concept ordering, concept diversity, larger multi-show concept pools, duplicate merge semantics, and provider-data persistence boundaries.

#### Risk Assessment

If executed as-is, the app would likely satisfy the benchmark's major user flows, but Alchemy and Explore Similar could feel less sharp than specified. A QA reviewer would probably notice that concepts are formatted correctly yet repetitive, genre-like, or not ordered by usefulness. Separately, sync edge cases could leave duplicate collection records insufficiently specified.

#### Remediation Guidance

The plan needs targeted acceptance criteria rather than a broad rewrite. Add explicit concept-generation rules for non-genre taste ingredients, strongest-first ordering, varied concept axes, and a larger multi-show option pool. For persistence, add duplicate-detection/merge behavior and explicitly state that provider persistence stores provider IDs only while rich details remain transient and refreshable.
