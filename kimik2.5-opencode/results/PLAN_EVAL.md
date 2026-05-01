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
| PRD-001 | Use Next.js latest stable runtime | critical | full | `Executive Summary` ("Core Stack: Next.js..."); `1.1 Repository Setup` | |
| PRD-002 | Use Supabase official client libraries | critical | full | `Executive Summary`; `2.3 Supabase Clients` | |
| PRD-003 | Ship `.env.example` with required variables | critical | full | `1.1 Repository Setup` ("Files to Create"; "Required Environment Variables") | |
| PRD-004 | Ignore `.env*` secrets except example | important | full | `1.1 Repository Setup` (".gitignore - Exclude .env* files (except .env.example)") | |
| PRD-005 | Configure build through env without code edits | critical | full | `1.1 Repository Setup` ("Required Environment Variables"); env-driven clients in `2.3 Supabase Clients` | |
| PRD-006 | Keep secrets out of repo and server-only | critical | full | `1.1 Repository Setup` ("Service role key (server-only)"); `9.6 Security Considerations` | |
| PRD-007 | Provide app, test, reset command scripts | critical | full | `1.1 Repository Setup` ("Scripts Required") | |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | `1.2 Database Schema (Supabase)` ("Migration Files"); `10. Deliverables Checklist` | |
| PRD-009 | Use one stable namespace per build | critical | full | `1.1 Repository Setup` ("NAMESPACE_ID"); `2.4 Identity & Namespace Context` | |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | `1.2 Database Schema (Supabase)` (RLS policies); `9.2 Namespace Isolation` | |
| PRD-011 | Attach every user record to `user_id` | critical | full | `1.2 Database Schema (Supabase)` (`shows`/`cloud_settings` include `user_id`); `9.1 User Identity in Benchmark Mode` | |
| PRD-012 | Partition persisted data by namespace and user | critical | full | `1.2 Database Schema (Supabase)` (`unique_user_show`, `unique_user_settings`); `9.2 Namespace Isolation` | |
| PRD-013 | Support documented dev auth injection, prod-gated | important | partial | `9.1 User Identity in Benchmark Mode` ("Use DEFAULT_USER_ID environment variable for dev/test") | The plan names a dev identity path, but it does not document the mechanism or specify how production mode disables or gates it. |
| PRD-014 | Real OAuth later needs no schema redesign | important | partial | `1.2 Database Schema (Supabase)`; `9.1 User Identity in Benchmark Mode` | The schema shape implies future auth wiring, but the plan never states the explicit no-schema-redesign migration strategy. |
| PRD-015 | Keep backend as persisted source of truth | critical | full | `3.1 Show Repository`; `9.4 Data Freshness` ("User data: Always current from database") | |
| PRD-016 | Make client cache safe to discard | critical | partial | `3.1 Show Repository`; `9.4 Data Freshness` | The plan reads from Supabase, but it never explicitly states that clearing local storage or reinstalling is safe. |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | missing | none | The plan never addresses Docker avoidance, optional local containers, or the hosted-first cloud-agent path. |
| PRD-018 | Overlay saved user data on every show appearance | critical | partial | `4.6 Show Detail Page` (merge stored + catalog show); `3.2 Show Merge Logic` | Overlay behavior is planned on Detail, but not across search results, recommendation tiles, and AI-derived show surfaces everywhere the show appears. |
| PRD-019 | Support visible statuses plus hidden `Next` | important | partial | `2.1 Types Definition` (includes `next`); `2.2 Configuration Constants` | The data model supports `next`, but the plan does not preserve the requirement that `Next` remain hidden/non-primary in the UI. |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | full | `4.6 Show Detail Page` (`handleInterestChange` sets `status: 'later'`); `9.5 Auto-Save Behaviors` | |
| PRD-021 | Support free-form multi-tag personal tag library | important | full | `2.1 Types Definition` (`myTags: string[]`); `4.6 Show Detail Page` (`TagPicker`); `4.1 Collection Home Page` (`availableTags`) | |
| PRD-022 | Define collection membership by assigned status | critical | full | `3.1 Show Repository` (`getCollection()` filters `my_status` not null) | |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | full | `4.6 Show Detail Page` (status/rating/tags handlers); `9.5 Auto-Save Behaviors` | |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | `9.5 Auto-Save Behaviors`; `4.6 Show Detail Page` (`handleRatingChange`, `handleTagsChange`) | |
| PRD-025 | Removing status deletes show and all My Data | critical | partial | `3.1 Show Repository` (`status === null` clears My Data); `4.6 Show Detail Page` (`RemovalConfirmationModal`) | The plan clears fields on status removal, but it does not actually delete the stored show record as the PRD requires. |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | partial | `4.6 Show Detail Page` (merge stored + catalog show); `3.2 Show Merge Logic` | The plan refreshes catalog data, but it does not specify how removed shows preserve My Data for later re-add. |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | `1.2 Database Schema (Supabase)` (per-field `*_update_date` columns); `3.1 Show Repository` update methods | |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | full | `3.1 Show Repository` (`order('my_status_update_date')`); `3.2 Show Merge Logic`; `9.4 Data Freshness` | |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | full | `5.3 AI API Routes` (4-hour cache; persist only if `show?.myStatus`); `2.2 Configuration Constants` | |
| PRD-030 | Keep Ask and Alchemy state session-only | important | full | `4.4 Ask Mode (AI Chat)` (local session hook/state); `4.5 Alchemy Mode` (`useState` flow only) | |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | partial | `4.5 Alchemy Mode` (`AIRecommendation` with `externalId`); `9.3 AI Response Parsing` ("search handoff") | The plan carries IDs and a fallback, but it never defines the deterministic lookup/mapping step that turns AI recs into selectable show objects. |
| PRD-032 | Show collection and rating tile indicators | important | partial | `4.1 Collection Home Page`; `8. Implementation Phases` (Phase 3 item 4: "Show tiles with indicators") | The plan mentions indicators, but it does not specify collection and rating badges consistently across all tile surfaces. |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | partial | `1.2 Database Schema (Supabase)` (`cloud_settings.version`); `3.2 Show Merge Logic` | The plan sketches versioning and merge logic, but it does not define a concrete library/settings sync path or duplicate merge handling. |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | partial | `1.2 Database Schema (Supabase)` (`app_metadata`); migration files in `1.2` | The plan includes migrations and metadata, but it does not describe the upgrade flow that preserves existing saved libraries and My Data. |
| PRD-035 | Persist synced settings, local settings, UI state | important | partial | `2.1 Types Definition` (`CloudSettings`, `LocalSettings`); `4.8 Settings Page` | The plan defines some settings types, but it omits a concrete persistence strategy for local settings and UI-state keys. |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | full | `1.2 Database Schema (Supabase)` (`provider_data jsonb`); `6.1 Catalog Client` (`watch/providers` mapped to provider IDs) | |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | partial | `3.2 Show Merge Logic` | The merge section gestures at timestamp-safe behavior, but it does not implement or specify the full per-field overwrite policy and maintenance timestamps required by the PRD. |
| PRD-038 | Provide filters panel and main screen destinations | important | full | `4.1 Collection Home Page` (`FilterSidebar`); `4.2 Find/Discover Hub` | |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | partial | `4.2 Find/Discover Hub` (`/find` route and mode switcher) | The plan provides a Find route, but it does not define a persistent primary-navigation shell that keeps Discover always available. |
| PRD-040 | Keep Settings in persistent primary navigation | important | partial | `4.8 Settings Page` | Settings exists as a page, but the plan does not place it in persistent primary navigation. |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | `4.2 Find/Discover Hub` (`Search`, `Ask`, `Alchemy` mode switcher) | |
| PRD-042 | Show only library items matching active filters | important | full | `4.1 Collection Home Page` (`useCollectionFilters` -> `filteredShows`) | |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | `4.1 Collection Home Page` (grouped `active`, `excited`, `interested`, `other`) | |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | partial | `2.1 Types Definition` (`FilterType` includes `genre`, `decade`, `communityScore`, `myTag`); `4.1 Collection Home Page` | The data types imply the filter set, but the plan does not concretely define the full sidebar/filter behavior for all of those views. |
| PRD-045 | Render poster, title, and My Data badges | important | full | `4.1 Collection Home Page`; `8. Implementation Phases` (Phase 3 item 4: "Show tiles with indicators") | |
| PRD-046 | Provide empty-library and empty-filter states | detail | partial | `4.1 Collection Home Page` (`EmptyState`) | The plan includes an empty state, but it does not distinguish between an empty library and a filter-specific empty result state. |
| PRD-047 | Search by title or keywords | important | full | `4.3 Search Mode`; `6.1 Catalog Client.search(query)` | |
| PRD-048 | Use poster grid with collection markers | important | partial | `4.3 Search Mode` (`ShowGrid` results) | The plan uses a grid layout, but it never explicitly adds the in-collection markers required on search results. |
| PRD-049 | Auto-open Search when setting is enabled | detail | partial | `2.1 Types Definition` (`autoSearch`); `8. Implementation Phases` (Phase 4 item 4: "Search on launch setting") | The setting exists in types and phases, but the actual auto-open behavior is not specified. |
| PRD-050 | Keep Search non-AI in tone | important | full | `4.3 Search Mode` (plain search UI with no AI persona surface) | |
| PRD-051 | Preserve Show Detail narrative section order | important | partial | `4.6 Show Detail Page` (numbered section comments) | The plan keeps a high-level sequence, but it changes the prescribed hierarchy by bundling relationship controls into the body and not preserving the exact narrative order. |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | full | `4.6 Show Detail Page` (`HeaderMedia` with `backdropUrl`, `posterUrl`, `logoUrl`, `videos`) | |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | full | `4.6 Show Detail Page` (`CoreFacts` near top) | |
| PRD-054 | Place status/interest controls in toolbar | important | partial | `4.6 Show Detail Page` (`MyRelationship` section) | The plan includes the controls, but it places them in the scroll body instead of explicitly in a toolbar. |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | `4.6 Show Detail Page` (`handleTagsChange` comment); `9.5 Auto-Save Behaviors` | |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | `4.6 Show Detail Page` (`handleRatingChange` comment); `9.5 Auto-Save Behaviors` | |
| PRD-057 | Show overview early for fast scanning | important | full | `4.6 Show Detail Page` (`OverviewScoop` placed near top) | |
| PRD-058 | Scoop shows correct states and progressive feedback | important | partial | `5.3 AI API Routes` (cached vs fresh scoop); `8. Implementation Phases` (Phase 6 item 4: "Progressive streaming UI") | The plan covers caching and streaming in broad strokes, but it does not define the detailed scoop state model and progressive feedback behavior from the PRD. |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | partial | `4.6 Show Detail Page` (`AskAboutShow` component) | The plan adds an Ask-about-show entry point, but it never specifies how show context is handed off into Ask. |
| PRD-060 | Include traditional recommendations strand | important | full | `4.6 Show Detail Page` (`Recommendations` strand) | |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | partial | `4.6 Show Detail Page` (`ExploreSimilar`); `8. Implementation Phases` (Phase 8) | The feature exists, but the plan does not spell out the CTA-first single-show flow from "Get Concepts" through concept selection to "Explore Shows." |
| PRD-062 | Include streaming availability and person-linking credits | important | partial | `4.6 Show Detail Page` (`StreamingProviders`, `CastCrew`); `4.7 Person Detail Page` | The plan includes providers and credits, but it does not explicitly define the cast/crew links that open Person Detail. |
| PRD-063 | Gate seasons to TV and financials to movies | important | full | `4.6 Show Detail Page` (`show.showType === 'tv'` / `show.showType === 'movie'`) | |
| PRD-064 | Keep primary actions early and page not overwhelming | important | partial | `4.6 Show Detail Page` | The plan places primary actions early, but it does not articulate the anti-busyness constraints or layout principles from the spec. |
| PRD-065 | Provide conversational Ask chat interface | important | full | `4.4 Ask Mode (AI Chat)` | |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | partial | `4.4 Ask Mode (AI Chat)` | The plan defines the chat UI, but it does not provide an Ask-specific response contract for direct, confident, spoiler-safe answers. |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | `4.4 Ask Mode (AI Chat)` (`MentionedShows` component) | |
| PRD-068 | Open Detail from mentions or Search fallback | important | partial | `4.4 Ask Mode (AI Chat)` (`MentionedShows`); `9.3 AI Response Parsing` ("search handoff") | The fallback is mentioned, but the plan does not explicitly specify opening Show Detail from valid mention hits. |
| PRD-069 | Show six random starter prompts with refresh | important | partial | `4.4 Ask Mode (AI Chat)` (`StarterPrompts`) | The plan includes six prompts, but they are fixed and there is no refresh/randomization behavior. |
| PRD-070 | Summarize older turns while preserving voice | important | partial | `8. Implementation Phases` (Phase 7 item 4: "Conversation summarization") | The plan includes summarization as work, but it does not preserve the voice/persona contract from the PRD. |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | partial | `4.6 Show Detail Page` (`AskAboutShow` component) | The plan creates the entry point, but it never defines the show-handoff payload or initialization flow. |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | partial | `8. Implementation Phases` (Phase 7 item 3: "Mentioned shows parsing"); `9.3 AI Response Parsing` | The plan intends to parse mentions, but it omits the exact `commentary`/`showList` shape and delimiter contract required by the PRD. |
| PRD-073 | Retry malformed mention output once, then fallback | important | partial | `9.3 AI Response Parsing` ("Implement retry logic... Fall back...") | The plan includes retry plus fallback, but it does not commit to the exact one-retry rule. |
| PRD-074 | Redirect Ask back into TV/movie domain | important | partial | `5.2 AI Prompts` (`scoop.ts` says "Stay in TV/movie domain") | The domain rule appears in the Scoop prompt, but the plan does not define it as a shared Ask surface guardrail. |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | full | `5.2 AI Prompts` (`concepts.ts`: "concept ingredients" for feeling/vibe/structure/emotional DNA) | |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | full | `5.2 AI Prompts` (`concepts.ts`: "Bullet list only"; "1-3 words"; "Avoid generic concepts") | |
| PRD-077 | Order concepts by strongest aha and varied axes | important | partial | `5.2 AI Prompts` (`concepts.ts` lists multiple concept axes) | The prompt names several axes, but it does not require strongest-first ordering or explicit diversity across axes. |
| PRD-078 | Require concept selection and guide ingredient picking | important | partial | `4.5 Alchemy Mode` (`selectedConcepts.length === 0`; `maxSelection={8}`) | The plan requires concept selection, but it does not include the UX guidance that tells users to pick the ingredients they want more of. |
| PRD-079 | Return exactly five Explore Similar recommendations | important | partial | `2.2 Configuration Constants` (`exploreSimilarRecs: 5`); `4.6 Show Detail Page` (`ExploreSimilar`) | The count exists in configuration, but the Explore Similar recommendation contract itself is not described concretely. |
| PRD-080 | Support full Alchemy loop with chaining | important | full | `4.5 Alchemy Mode` (multi-step flow and `handleChainAlchemy`) | |
| PRD-081 | Clear downstream results when inputs change | important | partial | `4.5 Alchemy Mode` | The plan resets state during chaining, but it does not explicitly clear downstream results whenever upstream show/concept inputs change. |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | partial | `5.2 AI Prompts` (`concepts.ts`: "Extract shared concepts from these shows") | The shared-concept behavior is present, but the larger multi-show option pool is not specified. |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | partial | `4.5 Alchemy Mode` (`Recommendations` receives `selectedConcepts`) | The plan passes selected concepts into the results component, but it never requires the recommendation reasons to explicitly cite them. |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | partial | `4.5 Alchemy Mode`; `Executive Summary` | The plan includes AI recommendations, but it does not define the quality bar for surprising yet defensible taste alignment. |
| PRD-085 | Keep one consistent AI persona across surfaces | important | partial | `5.2 AI Prompts` (`scoop.ts` persona definition) | The plan defines a Scoop persona, but it does not show a shared persona contract spanning Ask, Alchemy, and Explore Similar. |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | partial | `5.2 AI Prompts` (`scoop.ts`); `9.3 AI Response Parsing` | Some guardrails appear in one prompt and parsing notes, but the plan does not centralize or enforce them across all AI surfaces. |
| PRD-087 | Make AI warm, joyful, and light in critique | important | partial | `5.2 AI Prompts` (`scoop.ts`: "warm, opinionated") | The plan captures part of the voice for Scoop, but it does not define the warm/joyful/light-critique behavior across the broader AI system. |
| PRD-088 | Structure Scoop as personal taste mini-review | important | full | `5.2 AI Prompts` (`scoop.ts` sections: Personal Take / Stack-Up / The Scoop / Fit/Warnings / Worth It?) | |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | partial | `4.4 Ask Mode (AI Chat)` | The chat UI exists, but the plan does not specify the Ask response style as brisk, dialogue-first output. |
| PRD-090 | Feed AI the right surface-specific context inputs | important | partial | `5.2 AI Prompts` (`scoop.ts`, `concepts.ts`) | The plan sketches some prompt inputs, but it does not define the full context package for Ask, Explore Similar, and Alchemy. |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | missing | none | The plan includes testing, but it never adds the discovery-quality rubric or the hard-fail real-show integrity gate from the PRD. |
| PRD-092 | Show person gallery, name, and bio | important | partial | `4.7 Person Detail Page` (`PersonDetail person={person}`) | The route exists, but the gallery/name/bio presentation is not described. |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | partial | `8. Implementation Phases` (Phase 9 item 3: "Analytics charts") | The plan includes analytics work, but it never specifies the required ratings, genres, and projects-by-year views. |
| PRD-094 | Group filmography by year | important | partial | `8. Implementation Phases` (Phase 9 item 2: "Filmography display") | The plan includes filmography, but not the required grouping-by-year behavior. |
| PRD-095 | Open Show Detail from selected credit | important | partial | `4.7 Person Detail Page` | The person route exists, but the plan does not define navigation from a selected credit into Show Detail. |
| PRD-096 | Include font size and Search-on-launch settings | important | full | `2.1 Types Definition` (`fontSize`, `autoSearch`); `8. Implementation Phases` (Phase 4 item 4; Phase 10 item 3) | |
| PRD-097 | Support username, model, and API-key settings safely | important | partial | `2.1 Types Definition` (`userName`, `aiModel`, `aiApiKey`, `catalogApiKey`); `4.8 Settings Page`; `9.6 Security Considerations` | The plan names the settings fields and generic security notes, but it does not define the safe UX/handling rules for user-entered secrets. |
| PRD-098 | Export saved shows and My Data as zip | critical | partial | `1.3 Project Structure` (`api/export/route.ts`); `8. Implementation Phases` (Phase 10 item 2: "Data export (JSON backup)") | The plan includes export work, but it does not explicitly require a zip containing all saved shows and My Data. |
| PRD-099 | Encode export dates using ISO-8601 | important | missing | none | The export format is not specified to use ISO-8601 dates. |

## 3. Coverage Scores

score = (full_count × 1.0 + partial_count × 0.5) / total_count × 100

Critical:  (20 × 1.0 + 10 × 0.5) / 30 × 100 = 83.33%  (25.0 of 30 critical requirements)
Important: (24 × 1.0 + 40 × 0.5) / 67 × 100 = 65.67%  (44.0 of 67 important requirements)
Detail:    (0 × 1.0 + 2 × 0.5) / 2 × 100 = 50.00%  (1.0 of 2 detail requirements)
Overall:   (44 × 1.0 + 52 × 0.5) / 99 × 100 = 70.71%  (70.0 of 99 total requirements)

## 4. Top Gaps

1. PRD-037 | `critical` | Merge catalog fields safely and maintain timestamps
The plan acknowledges merge logic, but it does not specify the full timestamp-based overwrite policy that protects user-edited fields during refreshes and sync. Without that, normal catalog refreshes can silently clobber saved ratings, tags, status, or freshness metadata.

2. PRD-072 | `critical` | Emit `commentary` plus exact `showList` contract
Ask mentions are central to turning chat output into tappable show rows, and the PRD requires an exact machine-readable contract. Without the precise `commentary`/`showList` format, the mentioned-shows UI becomes fragile and likely breaks on routine model variation.

3. PRD-025 | `critical` | Removing status deletes show and all My Data
The plan clears fields but keeps the record, which diverges from the collection-removal contract. That creates ambiguous collection state, complicates re-add behavior, and risks stale data hanging around after users believe they removed a show.

4. PRD-026 | `critical` | Re-add preserves My Data and refreshes public data
The PRD expects removal and re-add to feel safe and forgiving, but the plan never defines how prior My Data survives that round trip. Executed as written, users are likely to lose tags, ratings, and scoop history when they briefly remove and later re-save a show.

5. PRD-031 | `critical` | Resolve AI recommendations to real selectable shows
The plan carries external IDs through recommendation flows, but it stops short of defining the real-item resolution contract. That undermines the core product rule that AI discovery must stay actionable, with recommendations that open into actual detail pages instead of dead text.

## 5. Coverage Narrative

### Overall Posture

This is a structurally sound plan with meaningful coverage of the app shell, persistence baseline, and major feature surfaces, but it is not yet a parity-ready plan. It reads strongest as an implementation scaffold and weakest where the PRD depends on hidden behavioral contracts, especially data continuity rules and AI output strictness.

### Strength Clusters

The plan is strongest in Benchmark Runtime & Isolation, Collection Home & Search, and the broad Show Detail page shell. It also covers the Scoop feature more concretely than the other AI surfaces, with explicit caching, persistence gating, and a shaped output prompt.

### Weakness Clusters

The gaps cluster around two patterns. First, the plan is thin on Collection Data & Persistence edge cases: removal semantics, re-add continuity, sync behavior, upgrade continuity, and precise merge policy. Second, AI coverage is broad but shallow across Ask Chat, Concepts/Alchemy, and AI Voice/Quality: the UI exists, but the exact contracts, guardrails, and quality bars are frequently left implied instead of specified.

### Risk Assessment

If this plan were executed as-is, the most likely result is an app that looks complete at the page level but fails parity in the invisible behaviors that make the product trustworthy. QA would likely notice first that AI chat mentions are unreliable to parse, recommendations are not consistently actionable, and user data integrity breaks around refresh/remove/re-add flows.

### Remediation Guidance

The remaining work is less about adding more pages and more about tightening behavioral specification. The plan needs explicit acceptance criteria for persistence edge cases, a concrete merge/removal/re-add model, exact AI input/output contracts shared across surfaces, and a more detailed settings/export/person-detail specification so implementation teams are not forced to invent product semantics mid-build.
