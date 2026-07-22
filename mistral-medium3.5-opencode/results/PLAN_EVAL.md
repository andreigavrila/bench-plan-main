# PLAN EVALUATION

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

## 2. Coverage Table

| PRD-ID | Requirement | Severity | Coverage | Evidence | Gap |
| ------ | ----------- | -------- | -------- | -------- | --- |
| PRD-001 | Use Next.js latest stable runtime | critical | full | 1.1 Technology Stack: "Next.js (latest stable)" |  |
| PRD-002 | Use Supabase official client libraries | critical | full | 1.1 Technology Stack: "Supabase...official client libraries" |  |
| PRD-003 | Ship `.env.example` with required variables | critical | full | 5.3 Environment Configuration lists `.env.example` variables |  |
| PRD-004 | Ignore `.env*` secrets except example | important | partial | 17. Files to Create lists `.gitignore`; 5.3 says secrets never committed | It does not explicitly require ignoring `.env*` while allowing `.env.example`. |
| PRD-005 | Configure build through env without code edits | critical | full | 5.3 Environment Configuration and 12.1 `cp .env.example .env` |  |
| PRD-006 | Keep secrets out of repo and server-only | critical | full | 5.3 Credential Rules: "Secrets NEVER committed" and "Service role key server-only" |  |
| PRD-007 | Provide app, test, reset command scripts | critical | full | 16. Delivery Checklist: `npm run dev`, `npm test`, `npm run test:reset` |  |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | 6.1 Supabase Setup: `supabase migration new init_schema` and migration up |  |
| PRD-009 | Use one stable namespace per build | critical | full | 5.1 Namespace Model: "single stable `namespace_id`" |  |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | 5.1 Namespace Model and 5.2 Destructive Testing |  |
| PRD-011 | Attach every user record to `user_id` | critical | partial | 5.1 says all user-owned records have `user_id`; 2.2 `cloud_settings` lacks `user_id` | The stated intent is contradicted by the concrete settings schema. |
| PRD-012 | Partition persisted data by namespace and user | critical | partial | 5.1 says partition is `(namespace_id, user_id)`; 2.2 settings use only `namespace_id` | The plan does not partition all persisted user settings by both namespace and user. |
| PRD-013 | Support documented dev auth injection, prod-gated | important | full | 5.1 Development Identity Injection: `X-User-Id`, selector, documented and gated |  |
| PRD-014 | Real OAuth later needs no schema redesign | important | full | 5.1 Migration to OAuth: "NOT a schema redesign" |  |
| PRD-015 | Keep backend as persisted source of truth | critical | full | 5.2 Source of Truth: "Server-side (Supabase)" |  |
| PRD-016 | Make client cache safe to discard | critical | full | 5.2 Cache Disposable: safe to clear local storage or reinstall |  |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | partial | 12.1 says local Supabase is optional; 12.3 uses hosted Supabase | It never explicitly states Docker must not be required for benchmark runs. |
| PRD-018 | Overlay saved user data on every show appearance | critical | partial | 15 checklist: "User's version takes precedence"; Search checks collection items | The plan lacks a concrete universal overlay rule for every list, recommendation, and AI output surface. |
| PRD-019 | Support visible statuses plus hidden `Next` | important | full | 2.1 `myStatus` includes `next`; 14 says Next hidden in data model, not surfaced |  |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | full | 7.1 Build Collection Journey: set Interested saves `status=Later, interest=Interested` |  |
| PRD-021 | Support free-form multi-tag personal tag library | important | full | 2.1 `myTags (String[])`; 4.1 TagFilters and tag filters |  |
| PRD-022 | Define collection membership by assigned status | critical | full | 2.4: "in collection" when non-nil `myStatus` |  |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | full | 2.4 Saving Triggers lists status, interest chip, rating, tag |  |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | 7.1 and 7.3 journeys show Later/Interested; 7.2 shows rating Done |  |
| PRD-025 | Removing status deletes show and all My Data | critical | full | 2.4 Removing from Collection clears status, interest, tags, rating, AI Scoop |  |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | full | 2.4 Re-adding Same Show preserves My Data and refreshes public metadata |  |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | 2.1 and 2.2 list per-field `my*UpdateDate` fields |  |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | full | 4.1 sorts by update date; 5.4 conflict resolution by timestamp; Scoop freshness |  |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | full | 4.5 and 4.8.1: cached ~4h, persists only if in collection |  |
| PRD-030 | Keep Ask and Alchemy state session-only | important | partial | 6.5 lists "AI sessions (Ask chat history, Alchemy state)"; 14 says Alchemy session only | Ask history and mentioned-show strip are not explicitly cleared/reset as session-only data. |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | full | 4.8.4 Mapping Strategy resolves by external ID and title match |  |
| PRD-032 | Show collection and rating tile indicators | important | full | 4.1: tiles display My Data badges including in-collection and rating |  |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | full | 5.4 Data Sync & Integrity: consistent library/settings, timestamp conflicts, duplicate merge |  |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | full | 5.4 Data Continuity: automatic migration and no data loss |  |
| PRD-035 | Persist synced settings, local settings, UI state | important | partial | 2.2 `cloud_settings`; 4.7 font size and Search on launch settings | It omits explicit persisted local settings and UI state keys such as confirmation suppression and last filter. |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | partial | 2.2 stores `providerData`; 6.4 fetches credits/recommendations/providers | Provider IDs are persisted, but transient-only handling for detail fetches is not specified. |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | full | 2.3 Data Merge Rules exactly covers non-empty catalog merge and timestamped My fields |  |
| PRD-038 | Provide filters panel and main screen destinations | important | full | 3.1 and 3.2 include FiltersPanel, Home, Find, Detail, Person, Settings |  |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | partial | 3.1 and 3.2 include the Find/Discover destination under `MainLayout` | The plan does not specify a persistent primary-navigation entry for Find/Discover. |
| PRD-040 | Keep Settings in persistent primary navigation | important | partial | 3.1 and 3.2 include `SettingsPage` under `MainLayout` | The Settings destination exists, but the plan does not specify it as a persistent primary-navigation entry. |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | 3.1 Find selector and sections 4.2, 4.3, 4.4 |  |
| PRD-042 | Show only library items matching active filters | important | full | 4.1: "Group by status and apply active filters" |  |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | 4.1 StatusGroups list Active, Excited, Interested, Other |  |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | full | 3.2 FiltersPanel lists tag, genre, decade, score; 4.1 media toggle |  |
| PRD-045 | Render poster, title, and My Data badges | important | full | 4.1: "Tiles display poster, title, and My Data badges" |  |
| PRD-046 | Provide empty-library and empty-filter states | detail | full | 4.1 empty collection and filter-none states |  |
| PRD-047 | Search by title or keywords | important | full | 4.2: "Text search by title/keywords" |  |
| PRD-048 | Use poster grid with collection markers | important | full | 4.2: "Results in poster grid" and in-collection badge |  |
| PRD-049 | Auto-open Search when setting is enabled | detail | full | 4.2: "Auto-open on launch if user enabled Search on Launch" |  |
| PRD-050 | Keep Search non-AI in tone | important | partial | 4.2 frames Search as external catalog text search | It does not explicitly state that Search has no AI voice or catalog-only tone. |
| PRD-051 | Preserve Show Detail narrative section order | important | full | 4.5 Sections in order match the required narrative hierarchy |  |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | partial | 4.5 header includes backdrops/posters/logos and trailers when available | The graceful fallback behavior for missing trailers/backdrops is not stated. |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | full | 4.5 section 2: "Core facts row (year/length) + community score" |  |
| PRD-054 | Place status/interest controls in toolbar | important | full | 4.5 Toolbar Controls list Interested, Excited, Active, Wait, Done, Quit |  |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | 4.5 behavior and 7.3 Tag-to-Save Journey |  |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | 4.5 behavior and 7.2 Rate-to-Save Journey |  |
| PRD-057 | Show overview early for fast scanning | important | full | 4.5 section 4: Overview + Scoop toggle/stream |  |
| PRD-058 | Scoop shows correct states and progressive feedback | important | full | 4.5 Scoop toggle copy and "Generating..." progressive state |  |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | full | 4.3 modes: Ask About a Show seeds conversation with show context |  |
| PRD-060 | Include traditional recommendations strand | important | full | 4.5 section 7: Traditional recommendations strand |  |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | full | 4.5 Explore Similar Flow: Get Concepts, select, Explore Shows |  |
| PRD-062 | Include streaming availability and person-linking credits | important | full | 4.5 sections 9 and 10: Streaming availability and Cast & Crew to Person Detail |  |
| PRD-063 | Gate seasons to TV and financials to movies | important | full | 4.5 sections: "Seasons (TV only)" and "Budget vs Revenue (movies where available)" |  |
| PRD-064 | Keep primary actions early and page not overwhelming | important | partial | 4.5 toolbar controls are always visible and early in the page | The plan does not address visual busyness or long-tail content de-emphasis beyond ordering. |
| PRD-065 | Provide conversational Ask chat interface | important | full | 4.3 AskChat with MessageList and Input |  |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | full | 4.8.2: direct answer in first 3-5 lines, confident picks; 4.3 spoiler-safe tone |  |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | 4.3 MentionedShowsStrip and horizontal strip behavior |  |
| PRD-068 | Open Detail from mentions or Search fallback | important | full | 4.3: tapping mentioned show opens Detail or Search fallback |  |
| PRD-069 | Show six random starter prompts with refresh | important | full | 4.3 StarterPrompts: "6 random, refreshable" |  |
| PRD-070 | Summarize older turns while preserving voice | important | full | 4.8.2 Summarization preserves persona/tone in 1-2 sentences |  |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | full | 4.3 Ask About a Show: "Seed conversation with show context" |  |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | full | 4.3 Structured Output Format has `commentary` and exact `showList` string |  |
| PRD-073 | Retry malformed mention output once, then fallback | important | full | 6.3 Response Parsing: retry stricter formatting, fallback unstructured + Search handoff |  |
| PRD-074 | Redirect Ask back into TV/movie domain | important | missing | none | No Ask or shared AI guardrail says to redirect off-domain requests back to TV/movies. |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | full | 4.4 and 4.8.3 call concepts vibes/ingredients and ingredient-like hooks |  |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | full | 4.8.3: bullet list only, 1-3 words, avoids generic concepts |  |
| PRD-077 | Order concepts by strongest aha and varied axes | important | full | 4.8.3: diversity across axes and order by strength |  |
| PRD-078 | Require concept selection and guide ingredient picking | important | full | 4.4 requires selecting 1-8 concepts and hints "pick the ingredients" |  |
| PRD-079 | Return exactly five Explore Similar recommendations | important | full | 4.5 Explore Similar displays 5 AI recommendations |  |
| PRD-080 | Support full Alchemy loop with chaining | important | full | 4.4 full flow includes "More Alchemy!" chaining |  |
| PRD-081 | Clear downstream results when inputs change | important | full | 4.4 UX Rules: changing shows clears concepts/results |  |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | partial | 4.4 and 4.8.3 require concepts shared across multiple input shows | Shared multi-show concepts are covered, but the plan uses the same default of 8 and does not specify a larger multi-show option pool. |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | full | 4.4 displays reasons tied to selected concepts; 4.8.4 reasons reflect concepts |  |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | partial | 4.8.4: bias recent but allow classics/hidden gems; reasons reflect concepts | It covers taste alignment but not explicit surprise-without-betrayal quality criteria. |
| PRD-085 | Keep one consistent AI persona across surfaces | important | full | 18 Summary: "One consistent AI persona across Scoop, Ask, Alchemy, and Explore Similar" |  |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | partial | 4.8.1 and 4.8.2 cover spoiler-safe, honest, structured AI behavior | Shared all-surface guardrails are incomplete because off-domain redirection is absent. |
| PRD-087 | Make AI warm, joyful, and light in critique | important | full | 4.8.1 Prompt Requirements: warm, playful, opinionated and honest about mixed reception |  |
| PRD-088 | Structure Scoop as personal taste mini-review | important | full | 4.8.1 mini blog-post with personal take, stack-up, centerpiece, fit, verdict |  |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | full | 4.8.2 responds like a friend, adapts depth, direct answer first |  |
| PRD-090 | Feed AI the right surface-specific context inputs | important | full | 4.3 builds conversation, library, and show context; 4.8.1 uses show details + user context |  |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | partial | 9 Testing Strategy covers AI parsing; 4.8.4 requires real catalog resolution | It lacks the discovery scoring rubric, threshold, and hard-fail integrity acceptance gate. |
| PRD-092 | Show person gallery, name, and bio | important | full | 4.6 components include ImageGallery and Name + Bio |  |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | full | 4.6 AnalyticsCharts: average ratings, top genres, projects-by-year |  |
| PRD-094 | Group filmography by year | important | full | 4.6 Filmography grouped and sorted by year |  |
| PRD-095 | Open Show Detail from selected credit | important | full | 4.6: selecting a credit opens Show Detail |  |
| PRD-096 | Include font size and Search-on-launch settings | important | full | 4.7 App Settings: font size/readability and Search on launch |  |
| PRD-097 | Support username, model, and API-key settings safely | important | full | 4.7 username, AI model, API keys; 5.3 and 11.1 credential safety |  |
| PRD-098 | Export saved shows and My Data as zip | critical | full | 4.7: Export My Data produces `.zip` JSON backup of saved shows and My Data |  |
| PRD-099 | Encode export dates using ISO-8601 | important | full | 4.7: "Dates encoded ISO-8601" |  |

## 3. Coverage Scores

Critical:  (26 full × 1.0 + 4 partial × 0.5) / 30 × 100 = 93.3%  (28 of 30 critical requirements)
Important: (53 full × 1.0 + 13 partial × 0.5) / 67 × 100 = 88.8%  (59.5 of 67 important requirements)
Detail:    (2 full × 1.0 + 0 partial × 0.5) / 2 × 100 = 100.0%  (2 of 2 detail requirements)
Overall:   90.4% (99 total requirements; 81 full, 17 partial, 1 missing)

## 4. Top Gaps

1. PRD-011 (`critical`) Attach every user record to `user_id`: The plan states the rule, but the concrete `cloud_settings` table is not user-scoped, so multi-user benchmark runs could leak or overwrite per-user settings.
2. PRD-012 (`critical`) Partition persisted data by namespace and user: The schema fully partitions shows but not all persisted settings, which weakens the core isolation contract.
3. PRD-018 (`critical`) Overlay saved user data on every show appearance: Without a universal overlay rule, Search, AI recommendations, and catalog-driven surfaces can show stale public-only versions instead of the user's saved relationship data.
4. PRD-086 (`critical`) Enforce shared AI guardrails across all surfaces: The plan covers tone and spoiler safety but misses the all-surface TV/movie domain boundary, allowing AI behavior to drift outside the product's scope.
5. PRD-074 (`important`) Redirect Ask back into TV/movie domain: Ask lacks an explicit off-domain redirect behavior, so a chat implementation could answer unrelated requests instead of preserving the entertainment-discovery surface.

## 5. Coverage Narrative

#### Overall Posture

This is a strong implementation plan with broad, concrete coverage across infrastructure, data modeling, core collection flows, discovery modes, detail pages, and export. It is not just a feature inventory; it includes schema sketches, API routes, data flows, and testing concerns. The main weaknesses are precision gaps where the PRD requires exact behavioral contracts.

#### Strength Clusters

Coverage is strongest in Benchmark Runtime & Isolation, Collection Home & Search, Ask Chat, Person Detail, and Settings & Export. The plan is especially concrete about Next.js/Supabase setup, namespace reset commands, status-driven collection membership, Ask structured output, Alchemy and Explore Similar flows, and export formatting.

#### Weakness Clusters

The partial and missing items cluster around cross-cutting guarantees and exact interaction contracts. Data isolation is weakened by settings schemas that do not consistently include `user_id`. AI quality is covered as tone and structure, but not as enforceable guardrails and rubric-based validation. Persistent Find/Discover and Settings navigation entries are implied by route placement rather than specified, and multi-show concepts lack the required larger option pool. A few storage details, such as session-only AI data and local/UI settings persistence, are also implied rather than specified.

#### Risk Assessment

If executed as-is, the most likely failure mode is a build that looks feature-complete but fails benchmark edge cases around isolation, AI guardrails, and persistence semantics. QA would probably notice settings shared across users in the same namespace, off-domain Ask responses, and inconsistent user overlays when catalog results or AI recommendations point at already-saved shows.

#### Remediation Guidance

The remaining planning work is mostly specification hardening. The plan needs tighter data ownership rules for every persisted table, explicit session lifecycle rules for Ask and Alchemy state, a universal "saved overlay wins" contract for every show rendering path, and AI acceptance criteria that include domain redirection plus the discovery quality rubric and real-show integrity gate.
