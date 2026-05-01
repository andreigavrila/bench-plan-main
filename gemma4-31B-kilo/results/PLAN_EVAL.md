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
| PRD-001 | Use Next.js latest stable runtime | critical | full | 2. Architecture & Tech Stack: "Framework: Next.js (latest stable)" |  |
| PRD-002 | Use Supabase official client libraries | critical | partial | 2. Architecture & Tech Stack: "Persistence: Supabase (PostgreSQL)" | The plan names Supabase but never says the implementation must use the official Supabase client libraries. |
| PRD-003 | Ship `.env.example` with required variables | critical | full | 5. Infrastructure & DevEx: ".env.example for API keys and Supabase credentials" |  |
| PRD-004 | Ignore `.env*` secrets except example | important | missing | none | The plan does not mention .gitignore rules that exclude .env* secrets while preserving .env.example. |
| PRD-005 | Configure build through env without code edits | critical | partial | 5. Infrastructure & DevEx: ".env.example for API keys and Supabase credentials" | It introduces environment variables but does not explicitly require the build to run entirely through env configuration without source edits. |
| PRD-006 | Keep secrets out of repo and server-only | critical | missing | none | The plan never addresses secret-handling rules such as keeping elevated keys out of the repo and server-only. |
| PRD-007 | Provide app, test, reset command scripts | critical | full | 5. Infrastructure & DevEx: "npm run dev", "npm test", and "npm run test:reset" |  |
| PRD-008 | Include repeatable schema evolution artifacts | critical | partial | 6. Implementation Roadmap: "Setup Next.js + Supabase schema" | It mentions schema setup but not repeatable migrations or seed artifacts for deterministic database creation. |
| PRD-009 | Use one stable namespace per build | critical | full | 2. Architecture & Tech Stack: "namespace_id: Build-level isolation to prevent data collisions" |  |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | 2. Architecture & Tech Stack and 5. Infrastructure & DevEx: "Partitioning: (namespace_id, user_id)" and "test:reset (scoped to namespace_id)" |  |
| PRD-011 | Attach every user record to `user_id` | critical | full | 2. Architecture & Tech Stack: "user_id: User-level ownership for all records" |  |
| PRD-012 | Partition persisted data by namespace and user | critical | full | 2. Architecture & Tech Stack: "Partitioning: (namespace_id, user_id)" |  |
| PRD-013 | Support documented dev auth injection, prod-gated | important | partial | 2. Architecture & Tech Stack: "Development identity injection (e.g., X-User-Id header)" | The plan covers dev auth injection but does not say it will be documented and gated off in production. |
| PRD-014 | Real OAuth later needs no schema redesign | important | partial | 2. Architecture & Tech Stack: "a path to migrate to OAuth" | Migration intent is noted, but the plan does not explain how schema choices avoid an OAuth-driven redesign later. |
| PRD-015 | Keep backend as persisted source of truth | critical | partial | 2. Architecture & Tech Stack: "Persistence: Supabase (PostgreSQL)" | The plan chooses a backend but never states that persisted server data remains the authoritative source of truth over client state. |
| PRD-016 | Make client cache safe to discard | critical | missing | none | The plan does not say client caches or local storage can be discarded safely without losing user-owned data. |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | full | 5. Infrastructure & DevEx: "No Docker requirement for cloud agents" |  |
| PRD-018 | Overlay saved user data on every show appearance | critical | partial | 1. Overview: "taste profile" and 3. Data Model: "Stores catalog metadata + user overlay" | The plan recognizes the overlay model but does not commit to showing that overlaid user version everywhere a show appears. |
| PRD-019 | Support visible statuses plus hidden `Next` | important | partial | 4.1 Collection Home and 4.3 Show Detail Page | The visible status model is covered at a high level, but the hidden Next status is never acknowledged. |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | partial | 4.1 Collection Home: "Excited (Later + Excited)" and "Interested (Later + Interested)" | The plan implies the mapping in grouping, but it does not explicitly define the chips as setting Later plus an interest level. |
| PRD-021 | Support free-form multi-tag personal tag library | important | partial | 3. Data Model: "myTags" and 4.3 Show Detail Page: "Tag picker" | Tagging is present, but the plan never calls out a reusable free-form multi-tag library across the app. |
| PRD-022 | Define collection membership by assigned status | critical | partial | 4.1 Collection Home: "Grouping: Status-based sections" | Status-driven grouping implies collection membership, but the plan never defines membership as the presence of an assigned status. |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | full | 4.3 Show Detail Page: "Status chips in toolbar (Auto-save logic)" plus rating/tag auto-save bullets |  |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | 4.3 Show Detail Page: "Rating slider (Auto-saves as Done if unsaved)" and "Tag picker (Auto-saves as Later + Interested if unsaved)" |  |
| PRD-025 | Removing status deletes show and all My Data | critical | missing | none | The plan never specifies that clearing status removes the show from storage and clears all related My Data. |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | partial | 3. Data Model: "Catalog Refresh" and timestamp conflict resolution | Refresh and merge behavior is present, but re-adding the same show is not explicitly defined as preserving My Data while refreshing public fields. |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | 3. Data Model: "Conflict resolution via timestamps (myStatusUpdateDate, etc.)" |  |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | partial | 3. Data Model: "Conflict resolution via timestamps" | Timestamps are used for merge conflicts, but the plan does not cover sorting or AI freshness behaviors driven by those timestamps. |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | partial | 4.4 AI Services: "The Scoop: personality-driven, spoiler-safe review. Cached for 4 hours." | Freshness is specified, but the plan does not say Scoop only persists for shows already saved in the collection. |
| PRD-030 | Keep Ask and Alchemy state session-only | important | missing | none | The plan does not define Ask chat history, mentioned shows, and Alchemy results as session-only state. |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | full | 4.4 AI Services: "Recommendation Engine: Maps AI output to real catalog items via external IDs" |  |
| PRD-032 | Show collection and rating tile indicators | important | partial | 4.1 Collection Home and 4.2 Find & Discover Hub | The plan mentions in-collection marking, but it does not clearly require both collection and rating indicators on show tiles. |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | partial | 3. Data Model: timestamp conflict resolution and CloudSettings | It covers field-level merge rules and settings storage, but not duplicate detection or sync consistency across the full library. |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | partial | 3. Data Model: "AppMetadata: Versioning for migrations" | Versioning is noted, but the plan does not spell out a continuity strategy that safely carries saved libraries through model upgrades. |
| PRD-035 | Persist synced settings, local settings, UI state | important | full | 3. Data Model: "CloudSettings" and "LocalSettings/UIState" |  |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | missing | none | The plan omits persisted provider IDs and does not distinguish transient detail fetches from stored show fields. |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | full | 3. Data Model: "selectFirstNonEmpty" and timestamp-based conflict resolution |  |
| PRD-038 | Provide filters panel and main screen destinations | important | partial | 4.1 Collection Home and 4.2 Find & Discover Hub | The plan covers the destinations conceptually, but it does not explicitly define the filters panel plus main-content shell. |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | partial | 4.2 Find & Discover Hub | Find/Discover exists, but the plan does not say it remains a persistent primary-navigation destination. |
| PRD-040 | Keep Settings in persistent primary navigation | important | missing | none | Settings appears only late in the roadmap and is never called out as a persistent primary-navigation destination. |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | 4.2 Find & Discover Hub: "Search", "Ask", and "Alchemy" |  |
| PRD-042 | Show only library items matching active filters | important | full | 4.1 Collection Home: "Views: Filtered library" |  |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | 4.1 Collection Home: explicit Active / Excited / Interested / Other grouping |  |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | full | 4.1 Collection Home: "All, Tag, Genre, Decade, Community Score" plus "All / Movies / TV" |  |
| PRD-045 | Render poster, title, and My Data badges | important | missing | none | The plan does not specify tile composition on Home, including poster, title, and My Data badges. |
| PRD-046 | Provide empty-library and empty-filter states | detail | missing | none | The plan never mentions empty-library or empty-filter states. |
| PRD-047 | Search by title or keywords | important | partial | 4.2 Find & Discover Hub: "Search: External catalog search" | Search is planned, but the query modes are not explicitly defined as title-or-keyword search. |
| PRD-048 | Use poster grid with collection markers | important | partial | 4.2 Find & Discover Hub: "Items in collection are marked" | Collection markers are present, but the plan never commits to the poster-grid presentation. |
| PRD-049 | Auto-open Search when setting is enabled | detail | partial | 3. Data Model: "LocalSettings/UIState" includes autoSearch | The setting exists in the data model, but the plan never ties it to automatically opening Search on launch. |
| PRD-050 | Keep Search non-AI in tone | important | partial | 4.2 Find & Discover Hub: Search is separated from Ask and Alchemy | The plan keeps Search distinct from AI features, but it does not explicitly protect Search from adopting AI voice or behavior. |
| PRD-051 | Preserve Show Detail narrative section order | important | full | 4.3 Show Detail Page: "Narrative Hierarchy" |  |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | partial | 4.3 Show Detail Page: "Header Carousel" | The plan includes the header section but does not say trailers or motion are prioritized with a graceful static fallback. |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | full | 4.3 Show Detail Page: "Core Facts/Score" immediately after the header |  |
| PRD-054 | Place status/interest controls in toolbar | important | full | 4.3 Show Detail Page: "Status chips in toolbar" |  |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | 4.3 Show Detail Page: "Tag picker (Auto-saves as Later + Interested if unsaved)" |  |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | 4.3 Show Detail Page: "Rating slider (Auto-saves as Done if unsaved)" |  |
| PRD-057 | Show overview early for fast scanning | important | full | 4.3 Show Detail Page: Overview appears near the top of the narrative hierarchy |  |
| PRD-058 | Scoop shows correct states and progressive feedback | important | partial | 4.4 AI Services: "The Scoop ... Cached for 4 hours" | The plan covers Scoop generation and freshness, but not the user-facing states, toggle behavior, or progressive feedback. |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | missing | none | The plan includes an Ask entry on Detail but never says the session is seeded with the current show context. |
| PRD-060 | Include traditional recommendations strand | important | full | 4.3 Show Detail Page: "Recs" in the narrative hierarchy |  |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | full | 4.3 Show Detail Page: "Explore Similar: Get Concepts → Select → Explore Shows" |  |
| PRD-062 | Include streaming availability and person-linking credits | important | partial | 4.3 Show Detail Page: "Streaming" and "Cast/Crew" plus 4.5 Person Detail Page | The necessary sections exist, but the plan does not explicitly state that credits link through to Person Detail. |
| PRD-063 | Gate seasons to TV and financials to movies | important | partial | 4.3 Show Detail Page: "Seasons/Budget" | The plan lists both sections but does not state the media-type gating rules for TV-only seasons and movie-only financials. |
| PRD-064 | Keep primary actions early and page not overwhelming | important | partial | 4.3 Show Detail Page: primary actions are placed early in the hierarchy | The rough ordering is good, but the plan does not explicitly address the balance between early power features and avoiding overwhelm. |
| PRD-065 | Provide conversational Ask chat interface | important | full | 4.2 Find & Discover Hub: "Ask (AI Chat)" |  |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | partial | 4.2 Find & Discover Hub: "Persona: Fun, chatty TV/movie nerd friend" | The tone is named, but the plan does not explicitly require direct answers, confident picks, and spoiler-safe recommendation behavior. |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | 4.2 Find & Discover Hub: "mentioned shows strip" |  |
| PRD-068 | Open Detail from mentions or Search fallback | important | partial | 4.2 Find & Discover Hub and 4.4 AI Services: mentioned shows plus ID-based resolution | The plan implies actionable mentions, but it never states the Detail-open path and Search fallback when mapping fails. |
| PRD-069 | Show six random starter prompts with refresh | important | missing | none | The welcome state with six random starter prompts and refresh behavior is absent from the plan. |
| PRD-070 | Summarize older turns while preserving voice | important | partial | 4.2 Find & Discover Hub: "conversation summarization" | Summarization is included, but the plan does not require summaries to preserve the same persona and voice. |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | missing | none | The plan never defines the Ask-about-show variant or its seeded handoff behavior from Detail. |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | partial | 4.2 Find & Discover Hub: "mentioned shows strip (Title::externalId::mediaType)" | The string format is noted, but the exact structured output contract with both commentary and showList is underspecified. |
| PRD-073 | Retry malformed mention output once, then fallback | important | missing | none | The plan does not cover retrying malformed mention output once before falling back. |
| PRD-074 | Redirect Ask back into TV/movie domain | important | missing | none | The plan never states that Ask must redirect users back into the TV/movie domain when they go off-domain. |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | full | 4.4 AI Services: "Concept Engine ... evocative ingredients" |  |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | partial | 4.4 AI Services: "Generates 1-3 word evocative ingredients" | Length and tone are present, but the plan does not require bullet-only output or explicitly ban generic concepts. |
| PRD-077 | Order concepts by strongest aha and varied axes | important | missing | none | The plan never requires concept ordering by strongest aha first or coverage across varied axes. |
| PRD-078 | Require concept selection and guide ingredient picking | important | partial | 4.2 Find & Discover Hub: "Select 1-8 concepts" and 4.3 Explore Similar flow | Concept selection is present, but the plan omits UX guidance that teaches users to pick the ingredients they want more of. |
| PRD-079 | Return exactly five Explore Similar recommendations | important | missing | none | The plan does not specify that Explore Similar returns exactly five recommendations per round. |
| PRD-080 | Support full Alchemy loop with chaining | important | full | 4.2 Find & Discover Hub: Alchemy flow plus "Ability to chain results" |  |
| PRD-081 | Clear downstream results when inputs change | important | missing | none | The plan does not say changing shows or concept inputs clears downstream concepts or results. |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | partial | 4.2 Find & Discover Hub: "Conceptualize (shared concepts)" | Shared concept generation is covered, but the larger multi-show option pool is not. |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | missing | none | The plan never requires recommendation reasons to explicitly cite the selected concepts. |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | partial | 1. Overview: discovery grounded in a user taste profile | Taste-aware recommendations are an overall goal, but the plan does not require the surprising-yet-defensible quality bar from the PRD. |
| PRD-085 | Keep one consistent AI persona across surfaces | important | partial | 4.2 Ask persona and 4.4 AI Services across Scoop, Concepts, and Recommendations | The plan defines some AI behaviors, but it never says every AI surface must feel like one consistent persona. |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | missing | none | The plan does not state shared AI guardrails such as spoiler safety, domain limits, and honest opinionation across every surface. |
| PRD-087 | Make AI warm, joyful, and light in critique | important | partial | 4.2 Find & Discover Hub: "Fun, chatty TV/movie nerd friend" | A friendly voice is implied, but the warm, joyful, light-critique standard is not made explicit across surfaces. |
| PRD-088 | Structure Scoop as personal taste mini-review | important | partial | 4.4 AI Services: "personality-driven, spoiler-safe review" | The plan includes Scoop, but it does not define the mini-review structure with personal take, fit, and verdict. |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | partial | 4.2 Find & Discover Hub: "Ask (AI Chat)" and named persona | Conversational Ask is present, but the brisk dialogue-first response style is not specified. |
| PRD-090 | Feed AI the right surface-specific context inputs | important | partial | 2. Architecture & Tech Stack and 4.2/4.4 AI sections | The plan references context-aware AI, but it does not enumerate the surface-specific inputs each AI flow needs to receive. |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | partial | 6. Implementation Roadmap: "Test against Discovery Quality Bar and Infrastructure Rider requirements" | The plan names the rubric, but it does not translate that into explicit quality gates such as hard-failing real-show integrity. |
| PRD-092 | Show person gallery, name, and bio | important | partial | 4.5 Person Detail Page: "Bio, image gallery" | The plan covers most of the page, but it does not explicitly call out showing the person name. |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | full | 4.5 Person Detail Page: "Analytics charts for project ratings, genres, and projects-by-year" |  |
| PRD-094 | Group filmography by year | important | full | 4.5 Person Detail Page: "filmography grouped by year" |  |
| PRD-095 | Open Show Detail from selected credit | important | missing | none | The plan never states that selecting a credit on Person Detail opens the corresponding Show Detail page. |
| PRD-096 | Include font size and Search-on-launch settings | important | full | 3. Data Model: "LocalSettings/UIState" with font size and autoSearch |  |
| PRD-097 | Support username, model, and API-key settings safely | important | partial | 3. Data Model: "CloudSettings: User profile, API keys, and AI model selection" | The settings objects are present, but the plan does not explain the safe handling boundaries for user-entered keys and synced settings. |
| PRD-098 | Export saved shows and My Data as zip | critical | partial | 5. Infrastructure & DevEx: "JSON Export/Backup functionality" | Backup is included, but the plan does not commit to exporting saved shows and My Data as a zip bundle. |
| PRD-099 | Encode export dates using ISO-8601 | important | missing | none | The plan never mentions ISO-8601 date encoding in the export format. |

### 3. Coverage Scores

Critical:  (14 × 1.0 + 12 × 0.5) / 30 × 100 = 66.67%  (20 of 30 critical requirements)
Important: (19 × 1.0 + 32 × 0.5) / 67 × 100 = 52.24%  (35 of 67 important requirements)
Detail:    (0 × 1.0 + 1 × 0.5) / 2 × 100 = 25.00%  (0.5 of 2 detail requirements)
Overall:   (33 × 1.0 + 45 × 0.5) / 99 × 100 = 56.06%  (55.5 of 99 total requirements)

### 4. Top Gaps

- PRD-025 | critical | Removing status deletes show and all My Data: The plan never defines the destructive removal path, so a core collection action can leave stale tags, ratings, or Scoop data behind and immediately fail QA on library lifecycle semantics.
- PRD-072 | critical | Emit `commentary` plus exact `showList` contract: Ask may appear to work textually while still failing the UI handoff for actionable mentioned shows, which breaks one of the main discovery-to-detail flows.
- PRD-006 | critical | Keep secrets out of repo and server-only: The plan omits key security boundaries, creating direct benchmark-compliance risk and making it easy to leak elevated persistence credentials into client code or source control.
- PRD-016 | critical | Make client cache safe to discard: Without this rule, clearing storage or reinstalling can silently destroy user-owned state or create divergence between client and backend data.
- PRD-015 | critical | Keep backend as persisted source of truth: The plan does not anchor persistence semantics, so implementation can drift into client-authoritative behavior that undermines sync, reset, and multi-device correctness.

### 5. Coverage Narrative

#### Overall Posture

This is a structurally sound high-level plan, but it is not implementation-ready. It names most major surfaces and several foundational data concerns, yet too many behavioral contracts are left implicit for a benchmark that scores against exact product and infrastructure rules.

#### Strength Clusters

The strongest coverage is in Show Detail & Relationship UX, Collection Home & Search basics, and the benchmark runtime baseline. The plan also does a decent job naming the core data entities, namespace and user partitioning, merge rules, Alchemy flow, and Person Detail analytics.

#### Weakness Clusters

The gaps cluster around AI behavioral contracts, persistence edge cases, and benchmark compliance details. In practice that means the plan often names a feature surface but stops short of the exact I/O contract, destructive data rule, fallback behavior, or security boundary the PRD requires.

#### Risk Assessment

If executed as-is, the most likely result is a product that demos plausibly but fails benchmark QA on semantics rather than surface area. A reviewer would first notice undefined removal behavior, underspecified Ask mention parsing, missing session-only rules, and weak source-of-truth or secret-handling guidance even though the main screens exist on paper.

#### Remediation Guidance

The next planning pass needs tighter acceptance criteria, not just more phases. Add explicit sections for data lifecycle semantics, AI output contracts and guardrails, source-of-truth and cache-disposal rules, security boundaries for credentials, and the exact UX/state rules for Search, Ask, Explore Similar, Settings, and export behavior.