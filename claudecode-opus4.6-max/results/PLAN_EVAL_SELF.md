# Plan Evaluation

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
| PRD-001 | Use Next.js latest stable runtime | critical | full | §1.1 "Initialize a Next.js project (App Router, TypeScript, Tailwind CSS)"; §0 "Next.js (latest stable)" | |
| PRD-002 | Use Supabase official client libraries | critical | full | §1.2 "Both clients are thin wrappers around the official `@supabase/supabase-js` SDK" | |
| PRD-003 | Ship `.env.example` with required variables | critical | full | §1.1 lists full `.env.example` with all variables and comments | |
| PRD-004 | Ignore `.env*` secrets except example | important | full | §1.1 "`.gitignore` excludes `.env*` (except `.env.example`)" | |
| PRD-005 | Configure build through env without code edits | critical | full | §1.1 env-based config; Phase 7 task 8 "App runs by filling env vars only (no code edits)" | |
| PRD-006 | Keep secrets out of repo and server-only | critical | full | §1.1 marks service role key, TMDB key, AI key as "server-only"; §1.2 browser client uses only anon key | |
| PRD-007 | Provide app, test, reset command scripts | critical | full | §1.1 npm scripts: `dev`, `build`/`start`, `test`, `test:reset`, `db:migrate` | |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | §2.2 "All migrations live in `supabase/migrations/`"; initial migration creates all tables deterministically | |
| PRD-009 | Use one stable namespace per build | critical | full | §1.3 "Read `NAMESPACE_ID` from environment. Every database query... includes a `namespace_id` predicate" | |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | §1.4 RLS policies restrict by namespace_id; §2.3 test reset scoped via `WHERE namespace_id = :namespace` | |
| PRD-011 | Attach every user record to `user_id` | critical | full | §2.1 `user_id` is PK component on shows, cloud_settings, user_preferences tables | |
| PRD-012 | Partition persisted data by namespace and user | critical | full | §2.1 PK `(namespace_id, user_id, id)`; §1.4 RLS policies enforce both dimensions | |
| PRD-013 | Support documented dev auth injection, prod-gated | important | full | §1.3 "In dev/test mode: accept `X-User-Id` header... In production mode: the dev injection path is disabled" | |
| PRD-014 | Real OAuth later needs no schema redesign | important | full | §1.3 "replacing the identity resolution function — no schema changes needed"; §8.4 opaque user_id | |
| PRD-015 | Keep backend as persisted source of truth | critical | full | §8.1 "all user data lives in Supabase. Client-side state is ephemeral" | |
| PRD-016 | Make client cache safe to discard | critical | full | §8.1 "Clearing browser storage loses nothing" | |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | full | Plan uses env vars for Supabase connection and npm for Next.js; no Docker dependency anywhere in the plan | |
| PRD-018 | Overlay saved user data on every show appearance | critical | full | §6.2 ShowTile includes badges; Phase 6 task 4 "Ensure all show tiles everywhere display user overlay per PRD §4.1" | |
| PRD-019 | Support visible statuses plus hidden `Next` | important | full | §2.1 my_status includes `'next'`; §6.2 StatusChips lists Active/Interested/Excited/Wait/Done/Quit (Next excluded from UI) | |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | full | §4.2 "Choosing Interested/Excited → save with `my_status = 'later'`, `my_interest = 'interested'\|'excited'" | |
| PRD-021 | Support free-form multi-tag personal tag library | important | full | §2.1 `my_tags text[]`; §4.1 tags PATCH and list APIs; §6.2 TagPicker component | |
| PRD-022 | Define collection membership by assigned status | critical | full | §4.2 "Setting status → save"; §4.3 collection queries filter by my_status | |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | full | §4.2 explicitly lists all four save triggers from PRD §5.2 | |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | §4.2 "No explicit status on save → later/interested"; "First save via rating → done" | |
| PRD-025 | Removing status deletes show and all My Data | critical | full | §4.2 "DELETE removes the row entirely, clearing all user data"; §6.2 RemovalConfirmation with "don't ask again" | |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | full | §4.2 "PUT upsert preserves existing user data and merges catalog fields using the merge logic" | |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | §2.1 all *_update_date columns present; §4.2 "Every PATCH sets the corresponding *_update_date = now()" | |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | partial | §3.4 merge uses timestamps for conflict resolution; §5.5 uses ai_scoop_update_date for 4h freshness | Plan does not specify timestamp-based sorting within collection groups (e.g., recently updated shows first) |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | full | §5.5 "in collection: persist; not in collection: do not persist"; "older than 4 hours → regenerate" | |
| PRD-030 | Keep Ask and Alchemy state session-only | important | full | §6.4.2 "Conversation state: held in client-side React state"; §6.4.3 "Session-only: all Alchemy state is client-side" | |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | full | §5.4 full resolution pipeline: external ID lookup → title search → interactive tile or non-interactive fallback | |
| PRD-032 | Show collection and rating tile indicators | important | full | §6.2 ShowTile "Poster + title + in-collection badge + rating badge" | |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | full | §8.1 server-side source of truth inherently syncs library; Phase 6 task 1 settings sync; §3.4 merge logic + PK dedup | |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | full | §2.2 sequential migrations + data_model_version tracking; §9 "migrations are additive; PRD §5.11 requires data continuity" | |
| PRD-035 | Persist synced settings, local settings, UI state | important | full | §2.1 cloud_settings (synced) and user_preferences (local + UI state) tables with all required fields | |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | full | §2.1 `provider_data jsonb`; §3.3 "Transient fields... returned in API response but not stored" | |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | full | §3.4 selectFirstNonEmpty for non-user fields; timestamp-based for user fields; creation_date never overwritten | |
| PRD-038 | Provide filters panel and main screen destinations | important | full | §6.1 "Sidebar (filters/navigation panel) + main content area" with filter links | |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | full | §6.1 "Persistent Find/Discover button" in top bar/nav | |
| PRD-040 | Keep Settings in persistent primary navigation | important | full | §6.1 "Persistent Settings button" in top bar/nav | |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | §6.4 "mode switcher: Search \| Ask \| Alchemy" | |
| PRD-042 | Show only library items matching active filters | important | full | §4.3 "Filters narrow the result set"; §6.3 fetches collection with current filter | |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | §4.3 groups: Active, Excited (Later+Excited), Interested (Later+Interested), Other (Wait/Quit/Done) | |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | full | §4.3 tag, genre, decade, community score filters; §6.1 "All Shows" link; media type toggle | |
| PRD-045 | Render poster, title, and My Data badges | important | full | §6.2 ShowTile: "Poster + title + in-collection badge + rating badge"; §6.3 "grid of ShowTile components" | |
| PRD-046 | Provide empty-library and empty-filter states | detail | full | §6.3 "no collection → prompt to Search/Ask. Filter yields nothing → 'No results found.'" | |
| PRD-047 | Search by title or keywords | important | full | §6.4.1 "Text input with live or submit-based search" | |
| PRD-048 | Use poster grid with collection markers | important | full | §6.4.1 "Results displayed as ShowGrid. In-collection items are marked with a badge" | |
| PRD-049 | Auto-open Search when setting is enabled | detail | full | §6.4.1 "Auto-opens on launch if `auto_search` setting is true" | |
| PRD-050 | Keep Search non-AI in tone | important | full | §6.4.1 Search page is purely TMDB catalog queries with no AI involvement | |
| PRD-051 | Preserve Show Detail narrative section order | important | full | §6.5 lists 15 sections following the detail_page_experience.md narrative hierarchy | |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | full | §6.5 item 1 "Trailers inline when available. Graceful fallback to poster-only" | |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | full | §6.5 item 2 "Year, runtime (movies) or seasons/episodes (TV), community score bar" | |
| PRD-054 | Place status/interest controls in toolbar | important | full | §6.5 item 4 "StatusChips in a sticky toolbar (not in scroll body)" | |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | §6.5 item 5 "Adding tag to unsaved show triggers auto-save as Later + Interested"; §4.2 confirms rule | |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | §6.5 item 3 "Rating unsaved show triggers auto-save as Done"; §4.2 confirms rule | |
| PRD-057 | Show overview early for fast scanning | important | full | §6.5 item 6: Overview appears at position 6 in the hierarchy, before AI features and long-tail content | |
| PRD-058 | Scoop shows correct states and progressive feedback | important | full | §6.5 item 7 toggle states ("Give me the scoop!" / "Show the scoop" / "The Scoop"); streams progressively with "Generating..." | |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | full | §6.5 item 8 "navigates to Ask page with show context seeded"; §5.2 ask.ts show-seeded variant | |
| PRD-060 | Include traditional recommendations strand | important | full | §6.5 item 10 "Traditional recommendations strand: ShowStrand from TMDB similar/recommended" | |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | full | §6.5 item 11 "Get Concepts → select → Explore Shows → 5 recommendation tiles" | |
| PRD-062 | Include streaming availability and person-linking credits | important | full | §6.5 item 12 streaming providers; item 13 "Cast & Crew... Tapping opens Person Detail" | |
| PRD-063 | Gate seasons to TV and financials to movies | important | full | §6.5 item 14 "Seasons (TV only)"; item 15 "Budget vs Revenue (movies, when available)" | |
| PRD-064 | Keep primary actions early and page not overwhelming | important | full | §6.5 clusters status/rating/scoop/concepts in items 1–11; long-tail info in items 12–15 | |
| PRD-065 | Provide conversational Ask chat interface | important | full | §6.4.2 "Chat UI: scrollable message list with user/assistant turns" | |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | full | §5.2 ask.ts "spoiler-safe default, opinionated honesty"; references discovery quality bar contracts | |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | §6.4.2 "Mentioned shows appear in a ShowStrand below the latest assistant message" | |
| PRD-068 | Open Detail from mentions or Search fallback | important | full | §6.4.2 "Tapping a mentioned show navigates to Show Detail (or Search if resolution fails)" | |
| PRD-069 | Show six random starter prompts with refresh | important | full | §6.4.2 "6 random starter prompts (from a pool of ~80 curated prompts) with a refresh button" | |
| PRD-070 | Summarize older turns while preserving voice | important | full | §5.2 summarize.ts "preserving the persona's tone. Applied after ~10 messages" | |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | full | §5.2 ask.ts "system prompt includes that show's metadata as seed context"; §6.4.2 confirms flow | |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | full | §5.2 ask.ts "commentary + showList dual format (Title::externalId::mediaType;;...)" | |
| PRD-073 | Retry malformed mention output once, then fallback | important | full | §9 "Retry once with stricter formatting instructions. Fall back to unstructured commentary + Search handoff" | |
| PRD-074 | Redirect Ask back into TV/movie domain | important | full | §5.2 "constructs the system prompt... according to the contracts in ai_prompting_context.md" which specifies domain redirection | |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | full | §5.2 concepts.ts "evocative, no plot, no generics. Focus axes: Structure, tone/vibe, emotional palette, craft, genre-flavor" | |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | full | §5.2 concepts.ts "Bullet list only, 1–3 words each, evocative, no plot, no generics" | |
| PRD-077 | Order concepts by strongest aha and varied axes | important | partial | §5.2 concepts.ts lists focus axes but not ordering rules | Plan specifies concept format and axes but omits the ordering requirement (strongest "aha" first) and explicit diversity constraint across axes |
| PRD-078 | Require concept selection and guide ingredient picking | important | partial | §6.2 ConceptChips "Selectable concept chips (max 8 selection)"; §6.4.3 and §6.5 describe selection flows | Plan covers selection mechanics but doesn't specify the "pick the ingredients you want more of" guidance copy or empty-state nudge |
| PRD-079 | Return exactly five Explore Similar recommendations | important | full | §5.2 recommendations.ts "5 for Explore Similar"; §6.5 item 11 "5 recommendation tiles" | |
| PRD-080 | Support full Alchemy loop with chaining | important | full | §6.4.3 full multi-step flow with "More Alchemy! button: chain another round using result shows as new inputs" | |
| PRD-081 | Clear downstream results when inputs change | important | full | §6.4.3 "Backtracking: changing the input shows clears concepts and results" | |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | partial | §5.2 concepts.ts "Multi-show (Alchemy): Extract concepts shared across all input shows" | Plan addresses shared concepts for multi-show but doesn't specify that the pool should be larger than single-show generation |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | full | §5.2 recommendations.ts "per-show reasons explicitly referencing concepts" | |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | full | §5.2 recommendations.ts includes library context; Phase 6 task 6 reviews against discovery quality bar including surprise | |
| PRD-085 | Keep one consistent AI persona across surfaces | important | full | §5.2 "Each AI surface has a dedicated prompt builder... according to the contracts in ai_voice_personality.md" | |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | partial | §5.2 "constructs the system prompt... according to the contracts in ai_prompting_context.md"; §9 "Prompt modules encode the voice pillars and guardrails" | Plan delegates guardrails to per-surface prompt modules referencing the spec; does not enumerate the shared guardrails (especially domain restriction) or describe a unified enforcement mechanism |
| PRD-087 | Make AI warm, joyful, and light in critique | important | full | §5.2 ask.ts "fun, chatty TV/movie nerd friend"; Phase 6 task 6 reviews voice adherence | |
| PRD-088 | Structure Scoop as personal taste mini-review | important | full | §5.2 scoop.ts "personal take, honest stack-up, The Scoop (emotional centerpiece), fit/warnings, verdict" | |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | full | §5.2 ask.ts describes persona; references ai_voice_personality.md contracts for tone | |
| PRD-090 | Feed AI the right surface-specific context inputs | important | full | §5.2 details context per surface; §5.3 "Include the user's library context... when the surface requires taste-awareness" | |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | full | Phase 6 task 6 "Review all AI surfaces against the discovery quality bar (voice, taste, integrity, specificity, surprise)" | |
| PRD-092 | Show person gallery, name, and bio | important | full | §6.6 "Image gallery, name, bio" | |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | full | §6.6 "Average project ratings, Top genres, Projects by year" with chart types specified | |
| PRD-094 | Group filmography by year | important | full | §6.6 "Filmography: credits grouped by year" | |
| PRD-095 | Open Show Detail from selected credit | important | full | §6.6 "each credit is a ShowTile that links to Show Detail" | |
| PRD-096 | Include font size and Search-on-launch settings | important | full | §6.7 "Font size selector (XS–XXL), 'Search on Launch' toggle" | |
| PRD-097 | Support username, model, and API-key settings safely | important | full | §6.7 "Username input... API key input, model selector. Key stored in cloud_settings... never committed to repo" | |
| PRD-098 | Export saved shows and My Data as zip | critical | full | §4.4 "GET /api/collection/export produces a ZIP file containing: shows.json... settings.json" | |
| PRD-099 | Encode export dates using ISO-8601 | important | full | §4.4 "Dates encoded ISO-8601" | |

## 3. Coverage Scores

**Score by severity tier:**

```
Critical:  (29 × 1.0 + 1 × 0.5) / 30 × 100 = 98.3%  (29.5 of 30 critical requirements)
Important: (63 × 1.0 + 4 × 0.5) / 67 × 100 = 97.0%  (65 of 67 important requirements)
Detail:    (2 × 1.0 + 0 × 0.5) / 2 × 100 = 100.0%  (2 of 2 detail requirements)
Overall:   (94 × 1.0 + 5 × 0.5) / 99 × 100 = 97.0% (99 total requirements)
```

## 4. Top Gaps

1. **PRD-086 | `critical` | Enforce shared AI guardrails across all surfaces**
   The plan delegates AI guardrails to individual prompt modules that reference the spec documents, but does not explicitly enumerate the shared rules (domain restriction to TV/movies, spoiler safety, opinionated honesty, actionable outputs) as a unified cross-cutting contract. Without this, an implementer could build each surface in isolation and inadvertently omit a guardrail — particularly the domain-redirection behavior — in one surface while including it in another. This is the only critical-tier gap.

2. **PRD-028 | `important` | Use timestamps for sorting, sync, freshness**
   The plan uses timestamps for merge conflict resolution and AI Scoop freshness, but does not specify timestamp-based sorting within collection views (e.g., "recently updated shows first where applicable"). The collection home groups by status with no stated sort order within groups, which means the most recently interacted-with shows may not surface naturally.

3. **PRD-077 | `important` | Order concepts by strongest aha and varied axes**
   The plan specifies concept format (bullet list, 1-3 words, evocative) and focus axes, but omits the ordering rule that strongest "aha" concepts should appear first and that the list should cover varied axes rather than clustering on one dimension. Without this, the concept system could return a correctly formatted but poorly prioritized list.

4. **PRD-078 | `important` | Require concept selection and guide ingredient picking**
   Concept selection mechanics are fully planned (ConceptChips, max 8, selection/deselection), but the plan does not specify the guidance copy ("pick the ingredients you want more of") or the empty-state nudge that should encourage at least one selection. Without these micro-copy cues, the concept step risks feeling opaque to first-time users.

5. **PRD-082 | `important` | Generate shared multi-show concepts with larger option pool**
   The plan covers multi-show concept generation (shared across all input shows) but does not specify that multi-show generation should return a larger pool than single-show generation. This distinction matters because Alchemy's value depends on having enough combinatorial breadth for the user to compose surprising ingredient blends.

## 5. Coverage Narrative

### Overall Posture

This is a strong, comprehensive plan with only minor gaps. It covers 94 of 99 requirements fully and the remaining 5 partially — no requirement is missing entirely. The plan demonstrates deep engagement with both the product PRD and the infrastructure rider, translating behavioral requirements into concrete schema designs, API routes, component specifications, and phased delivery. A team executing this plan would build a recognizable, functional version of the product with high fidelity to the specification.

### Strength Clusters

The plan is strongest in **Benchmark Runtime & Isolation** (all 17 requirements fully covered) and **Collection Data & Persistence** (19 of 20 fully covered). The infrastructure design — namespace partitioning via composite primary keys, RLS enforcement, opaque user_id, env-driven configuration, and migration artifacts — is thorough and architecturally sound. The collection management layer is equally robust: all save triggers, default values, removal semantics, re-add behavior, and merge logic are specified with concrete API routes and SQL-level detail. **Show Detail & Relationship UX** is another standout area (all 14 requirements fully covered), with the plan faithfully reproducing the detail page narrative hierarchy and wiring each interactive control to its corresponding business rule. **Ask Chat** (all 10 fully covered) and **Settings & Export** (all 4 fully covered) are also comprehensively addressed.

### Weakness Clusters

The partial items cluster around two specific themes rather than a single functional area. First, **AI behavioral contracts at the prompt-engineering level**: the plan specifies what each AI surface should produce but occasionally omits the finer-grained generation rules from the concept system and shared guardrails specs (PRD-077, PRD-082, PRD-086). These are not structural omissions — the architecture is sound — but they represent under-specification of the AI's behavioral contract, which could lead to quality drift during implementation. Second, **micro-UX copy and sorting polish** (PRD-028, PRD-078): timestamp-based sorting within collection groups and concept-selection guidance copy are small but user-facing details that the plan defers without explicitly planning for them.

### Risk Assessment

If executed as-is, the most likely failure mode is **inconsistent AI behavior across surfaces**. The plan's AI architecture correctly separates prompt modules, streams responses, resolves shows, and handles failures — but because the shared guardrails are not enumerated as a cross-cutting specification (PRD-086), a developer building the Scoop surface might omit the domain-redirection rule, while the developer building Ask might include it. A QA reviewer would notice this as: "the Scoop sometimes responds to non-TV/movie queries when the user's show context drifts, while Ask correctly redirects." The concept ordering gap (PRD-077) would manifest more subtly — users might see repetitive or poorly prioritized concept lists in Explore Similar without understanding why the feature feels flat.

### Remediation Guidance

The gaps fall into two categories of remaining work. The **AI guardrail and generation-rule gaps** (PRD-077, PRD-082, PRD-086) need a short specification addendum — a single "Shared AI Contract" section in the plan that enumerates the cross-surface guardrails as an explicit checklist and specifies concept ordering/pool-size rules. This is specification work, not architectural work; the underlying AI module structure is already correct. The **UX copy and sorting gaps** (PRD-028, PRD-078) need minor additions to existing plan sections — a sort-order clause in the collection home specification and a copy/guidance note in the concept selection component spec. These are detail-level refinements that could be addressed in a single pass over the existing plan text without requiring new architectural decisions.
