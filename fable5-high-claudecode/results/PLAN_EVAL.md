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
| PRD-001 | Use Next.js latest stable runtime | critical | full | Executive Summary: "Next.js (latest stable)" | |
| PRD-002 | Use Supabase official client libraries | critical | full | Executive Summary: "official `@supabase/supabase-js`" | |
| PRD-003 | Ship `.env.example` with required variables | critical | full | Section 9.1 Environment includes committed `.env.example` variables | |
| PRD-004 | Ignore `.env*` secrets except example | important | full | Section 9.1: "`.gitignore` excludes `.env*` except `.env.example`" | |
| PRD-005 | Configure build through env without code edits | critical | full | Section 9.1: "Runs with env fill-in only - no source edits" | |
| PRD-006 | Keep secrets out of repo and server-only | critical | full | Sections 2.2 and 9.1: server-only keys, browser anon key only | |
| PRD-007 | Provide app, test, reset command scripts | critical | full | Section 9.2 lists `dev`, `test`, `test:reset`, e2e, migrate scripts | |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | Section 3: `supabase/migrations/*.sql`, seed, fixtures | |
| PRD-009 | Use one stable namespace per build | critical | full | Section 2.3: `NAMESPACE_ID` stable for build lifetime | |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | Sections 2.3 and 5: scoped partition plus `/api/test/reset` | |
| PRD-011 | Attach every user record to `user_id` | critical | full | Sections 2.3 and 3.1: PKs include `user_id` | |
| PRD-012 | Partition persisted data by namespace and user | critical | full | Section 2.3: effective partition `(namespace_id, user_id)` | |
| PRD-013 | Support documented dev auth injection, prod-gated | important | full | Section 2.3: `IDENTITY_MODE=dev`, `X-User-Id`, production disabled | |
| PRD-014 | Real OAuth later needs no schema redesign | important | full | Sections 2.3 and 12: opaque `user_id`, only resolver changes | |
| PRD-015 | Keep backend as persisted source of truth | critical | full | Executive Summary: "Backend is the source of truth" | |
| PRD-016 | Make client cache safe to discard | critical | full | Sections 2.1 and 3.2: React Query/local storage disposable | |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | full | Executive Summary and 9.3: hosted Supabase, Docker never required | |
| PRD-018 | Overlay saved user data on every show appearance | critical | full | Section 2.4: "Every surface... merges catalog data with user's saved row" | |
| PRD-019 | Support visible statuses plus hidden `Next` | important | full | Section 6.2: statuses listed, `next` in enum but not UI | |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | full | Section 6.2: selecting chips sets `status=later` plus interest | |
| PRD-021 | Support free-form multi-tag personal tag library | important | full | Sections 3.1 and 5: `my_tags text[]`, `/api/collection/tags` | |
| PRD-022 | Define collection membership by assigned status | critical | full | Section 3.1: row exists iff `my_status` non-null | |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | full | Section 6.1 save triggers matrix | |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | Section 6.1 save defaults matrix | |
| PRD-025 | Removing status deletes show and all My Data | critical | full | Section 6.3: confirm then delete row clearing data | |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | full | Sections 3.3 and 6.4: merge engine for re-add/refresh | |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | Sections 3.1 and 6.1: each My Data field has update date | |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | full | Sections 3.3 and 7.2: timestamp merge, sorting, Scoop TTL | |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | full | Sections 5 and 7.2: persists only if row exists, 4-hour freshness | |
| PRD-030 | Keep Ask and Alchemy state session-only | important | full | Section 7.2: Ask history clears; Alchemy state session-only | |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | full | Section 4.3: resolution gate to real selectable Show | |
| PRD-032 | Show collection and rating tile indicators | important | full | Section 6.5: in-collection and rating badge in ShowTile | |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | full | Section 3.3: `mergeUserRows`; Section 7.2 settings sync | |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | full | Sections 11 Phase 4 and 12: migration hook and lossless fixture test | |
| PRD-035 | Persist synced settings, local settings, UI state | important | full | Sections 3.1 and 3.2: cloud settings plus local UI state keys | |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | full | Sections 3.1 and 4.1: provider IDs stored; transient data never persisted | |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | full | Section 3.3: `selectFirstNonEmpty`, dates, creation rules | |
| PRD-038 | Provide filters panel and main screen destinations | important | full | Section 7.1 skeleton: Home filters, Find, Detail, Person, Settings | |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | partial | Section 7.1 defines a `Find` hub with Search/Ask/Alchemy | The plan includes a Find hub, but does not explicitly specify persistent primary navigation placement or behavior. |
| PRD-040 | Keep Settings in persistent primary navigation | important | partial | Section 7.1 defines a `Settings` screen | The plan includes Settings as a destination, but does not explicitly require it to remain in persistent primary navigation. |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | Sections 7.1 and 7.2: ModeSwitcher Search/Ask/Alchemy | |
| PRD-042 | Show only library items matching active filters | important | full | Section 7.2 Home: filters compose with media-type toggle | |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | Section 7.2 Home fixed section order | |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | full | Section 7.1 FilterSidebar and Section 5 filter params | |
| PRD-045 | Render poster, title, and My Data badges | important | full | Sections 6.5 and 7.1: shared ShowTile, PosterGrid, badges | |
| PRD-046 | Provide empty-library and empty-filter states | detail | full | Section 7.2 Home empty states | |
| PRD-047 | Search by title or keywords | important | full | Section 5: `GET /api/catalog/search?q=`; Section 7.2 Search | |
| PRD-048 | Use poster grid with collection markers | important | full | Section 7.2 Search: poster grid and in-collection marks | |
| PRD-049 | Auto-open Search when setting is enabled | detail | full | Section 7.2 Search: `autoSearch` opens Find -> Search on launch | |
| PRD-050 | Keep Search non-AI in tone | important | full | Section 7.2 Search: "plain catalog search (no AI voice)" | |
| PRD-051 | Preserve Show Detail narrative section order | important | full | Section 7.2 Detail: exact order from detail spec | |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | full | Section 7.2 Detail: header carousel, trailer, poster/logo fallback | |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | full | Section 7.1 `CoreFacts`; Section 7.2 Detail order | |
| PRD-054 | Place status/interest controls in toolbar | important | full | Section 7.2 Detail: status chips live in toolbar | |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | Sections 6.1 and 7.2 Detail critical states | |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | Sections 6.1 and 7.2 Detail critical states | |
| PRD-057 | Show overview early for fast scanning | important | full | Section 7.2 Detail: overview immediately after tags | |
| PRD-058 | Scoop shows correct states and progressive feedback | important | full | Section 7.2 Detail: toggle copy, streaming, generating state | |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | full | Section 7.2 Ask and Detail: handoff show injected | |
| PRD-060 | Include traditional recommendations strand | important | full | Section 7.1 `RecommendationsStrand`; Section 7.2 Detail | |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | full | Section 7.2 Detail: Get Concepts -> chips -> Explore Shows | |
| PRD-062 | Include streaming availability and person-linking credits | important | full | Section 7.1 `StreamIt` and `CastCrew`; Section 4.1 catalog details | |
| PRD-063 | Gate seasons to TV and financials to movies | important | full | Section 7.2 Detail: TV vs movie field handling | |
| PRD-064 | Keep primary actions early and page not overwhelming | important | full | Section 7.2 Detail clusters status, tags, Scoop, Ask, Explore early | |
| PRD-065 | Provide conversational Ask chat interface | important | full | Section 7.2 Ask: user/assistant turns and streaming | |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | full | Section 8.1 Ask: direct first lines, confident picks, spoiler-safe | |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | Section 7.2 Ask: mentioned shows horizontal strip | |
| PRD-068 | Open Detail from mentions or Search fallback | important | full | Section 7.2 Ask: tap to Detail; unresolved Search handoff | |
| PRD-069 | Show six random starter prompts with refresh | important | full | Sections 5 and 7.2 Ask: 6 starter prompts with refresh | |
| PRD-070 | Summarize older turns while preserving voice | important | full | Sections 5 and 8.1: in-persona summarizer after ~10 turns | |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | full | Section 7.2 Ask About a Show; Section 14 default stance | |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | full | Sections 5 and 8.1: `{commentary, showList}` and delimiter format | |
| PRD-073 | Retry malformed mention output once, then fallback | important | full | Section 4.2: parse failure retry once, then fallback | |
| PRD-074 | Redirect Ask back into TV/movie domain | important | full | Section 8.1 shared rules: stay in TV/movies, redirect out-of-domain | |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | full | Section 8.1 Concepts: ingredient-like axes and no generic genre labels | |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | full | Section 8.1 Concepts: bullet list only, 1-3 words, banned generic list | |
| PRD-077 | Order concepts by strongest aha and varied axes | important | full | Section 8.1 Concepts: axes diversity and ordered best-first | |
| PRD-078 | Require concept selection and guide ingredient picking | important | full | Sections 7.2 Alchemy and Detail: select catalysts/concepts before recs | |
| PRD-079 | Return exactly five Explore Similar recommendations | important | full | Sections 5, 7.2, and 8.1: explore -> 5 recs | |
| PRD-080 | Support full Alchemy loop with chaining | important | full | Section 7.2 Alchemy: pick shows, concepts, alchemize, More Alchemy | |
| PRD-081 | Clear downstream results when inputs change | important | full | Section 7.2 Alchemy: changing inputs clears concepts/results | |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | full | Section 8.1 Concepts: multi-show shared across all, larger pool | |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | full | Section 8.1 Concept recs: reasons name matched concepts | |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | full | Section 8.2 adopts quality bar including surprise-without-betrayal | |
| PRD-085 | Keep one consistent AI persona across surfaces | important | full | Section 8.1: one base persona composed with per-surface modes | |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | full | Section 8.1 shared rules injected everywhere | |
| PRD-087 | Make AI warm, joyful, and light in critique | important | full | Section 8.1 base persona: joy-forward, opinionated honesty | |
| PRD-088 | Structure Scoop as personal taste mini-review | important | full | Section 8.1 Scoop: personal take, stack-up, Scoop, fit, verdict | |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | full | Section 8.1 Ask: friend-in-dialogue, direct, bullets | |
| PRD-090 | Feed AI the right surface-specific context inputs | important | full | Section 8.1: taste context, handoff show, selected concepts, turns | |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | full | Section 8.2: scoring rubric and real-show integrity non-negotiable | |
| PRD-092 | Show person gallery, name, and bio | important | full | Section 7.2 Person: image gallery + bio | |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | full | Section 7.2 Person: average ratings, top genres, projects-by-year | |
| PRD-094 | Group filmography by year | important | full | Section 7.2 Person: filmography grouped by year | |
| PRD-095 | Open Show Detail from selected credit | important | full | Section 7.2 Person: credit tap -> Detail | |
| PRD-096 | Include font size and Search-on-launch settings | important | full | Section 7.2 Settings: font size and Search-on-launch toggle | |
| PRD-097 | Support username, model, and API-key settings safely | important | full | Sections 3.1, 7.2, and 9.1: synced username/model/keys, env fallback | |
| PRD-098 | Export saved shows and My Data as zip | critical | full | Sections 5 and 7.2 Settings: Export My Data zip | |
| PRD-099 | Encode export dates using ISO-8601 | important | full | Section 5 export route and Section 7.2 Settings: ISO-8601 dates | |

### 3. Coverage Scores

Overall score:

```
score = (97 x 1.0 + 2 x 0.5) / 99 x 100 = 99.0%
```

Critical:  (30 x 1.0 + 0 x 0.5) / 30 x 100 = 100.0%  (30 of 30 critical requirements)
Important: (65 x 1.0 + 2 x 0.5) / 67 x 100 = 98.5%  (66 of 67 important requirements)
Detail:    (2 x 1.0 + 0 x 0.5) / 2 x 100 = 100.0%  (2 of 2 detail requirements)
Overall:   99.0% (99 total requirements)

### 4. Top Gaps

1. PRD-039 (`important`) - Keep Find/Discover in persistent primary navigation

The plan defines the Find hub and its modes well, but does not explicitly commit to a persistent primary navigation entry. If implemented literally, Discover could become reachable only through routing or page flow rather than a durable global entry point.

2. PRD-040 (`important`) - Keep Settings in persistent primary navigation

The plan includes a Settings screen and settings features, but does not specify persistent primary navigation placement. This could make user data export, font sizing, and provider/model controls less discoverable than the PRD intends.

### 5. Coverage Narrative

#### Overall Posture

This is a very strong implementation plan with only minor navigation-specification gaps. It directly covers the critical infrastructure, persistence, AI contract, and user-data rules, and it usually names the concrete module, route, component, or test strategy that would enforce each requirement.

#### Strength Clusters

Coverage is strongest in Benchmark Runtime & Isolation, Collection Data & Persistence, Ask Chat, Concepts/Explore Similar/Alchemy, and AI Voice/Persona/Quality. The plan is especially concrete where correctness matters: namespace and user scoping, Supabase schema design, server-only AI/catalog access, save triggers, merge rules, structured Ask output, recommendation resolution, and testing.

#### Weakness Clusters

The only meaningful weakness cluster is App Navigation & Discover Shell. The plan describes the destination screens and Discover modes, but it treats primary navigation as an app shell detail rather than an explicit requirement with persistent Find/Discover and Settings entries.

#### Risk Assessment

If executed exactly as written, the most likely QA finding would not be data loss or AI contract failure; it would be a navigation compliance issue. A reviewer could find fully implemented Find and Settings screens but no guaranteed persistent global way to reach them, which would violate the PRD's app-structure expectations.

#### Remediation Guidance

The remaining work is specification detail, not new architecture. The plan should add a small app-shell/navigation section that explicitly defines persistent primary navigation entries for Collection/Home, Find/Discover, and Settings, including behavior across Home, Detail, Person, and Discover submodes.
