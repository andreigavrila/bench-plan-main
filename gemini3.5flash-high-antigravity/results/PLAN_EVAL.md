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
| PRD-001 | Use Next.js latest stable runtime | critical | partial | `1.1 Benchmark Runtime & Isolation`: "Next.js App Router (v14/v15 stable)". | The plan names older/ambiguous major versions instead of pinning the current latest stable runtime target. |
| PRD-002 | Use Supabase official client libraries | critical | full | `1.1 Benchmark Runtime & Isolation`: `@supabase/supabase-js` and `@supabase/ssr`. |  |
| PRD-003 | Ship `.env.example` with required variables | critical | full | `1.1 Benchmark Runtime & Isolation` and `6.1 Environment Setup`: create comprehensive `.env.example`. |  |
| PRD-004 | Ignore `.env*` secrets except example | important | partial | `1.1 Benchmark Runtime & Isolation` and `6.1 Environment Setup`: configure environment-file ignores. | The concrete plan lists only `.env`, `.env.local`, and `.env.production`; it does not specify the required `.env*` wildcard with an `.env.example` exception. |
| PRD-005 | Configure build through env without code edits | critical | full | `1.1 Benchmark Runtime & Isolation` and `3. Directory Layout`: `env.ts` reads all config from `process.env`. |  |
| PRD-006 | Keep secrets out of repo and server-only | critical | full | `1.1 Benchmark Runtime & Isolation`: service-role style credentials restricted to Server Actions and API Routes. |  |
| PRD-007 | Provide app, test, reset command scripts | critical | full | `1.1 Benchmark Runtime & Isolation` and `6.1 Environment Setup`: `dev`, `test`, and `test:reset`. |  |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | `1.1 Benchmark Runtime & Isolation` and `2.1 Supabase Schema`: migrations under `/supabase/migrations`. |  |
| PRD-009 | Use one stable namespace per build | critical | full | `1.1 Benchmark Runtime & Isolation`: `NEXT_PUBLIC_NAMESPACE_ID` / `NEXT_PUBLIC_RUN_ID` scoped per build. |  |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | `1.1 Benchmark Runtime & Isolation`, `2.1 Supabase Schema`, and `7.1 Namespace Data Isolation Testing`. |  |
| PRD-011 | Attach every user record to `user_id` | critical | full | `1.1 Benchmark Runtime & Isolation` and `2.1 Supabase Schema`: `shows` and `cloud_settings` require `user_id`. |  |
| PRD-012 | Partition persisted data by namespace and user | critical | full | `1.1 Benchmark Runtime & Isolation` and `2.1 Supabase Schema`: compound keys on `(namespace_id, user_id, ...)`. |  |
| PRD-013 | Support documented dev auth injection, prod-gated | important | partial | `1.1 Benchmark Runtime & Isolation`: dev mode accepts `X-User-Id` or a dev cookie and blocks it in production. | The mechanism is described, but the plan does not add a documentation deliverable for how benchmark users inject identity. |
| PRD-014 | Real OAuth later needs no schema redesign | important | full | `1.1 Benchmark Runtime & Isolation`: standard opaque `user_id` keys for future auth wiring. |  |
| PRD-015 | Keep backend as persisted source of truth | critical | full | `1.1 Benchmark Runtime & Isolation`: "Always resolve mutations and reads against Supabase tables." |  |
| PRD-016 | Make client cache safe to discard | critical | full | `1.1 Benchmark Runtime & Isolation`: cache is in memory or disposable IndexedDB and re-pulls from server. |  |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | partial | `1.1 Benchmark Runtime & Isolation`: "Provide local sqlite fallback or remote hosted database connection mode." | The hosted path is compliant, but the sqlite fallback drifts from the benchmark's fixed Supabase baseline. |
| PRD-018 | Overlay saved user data on every show appearance | critical | full | `1.2 Collection Data & Persistence`: query the library and merge user metadata into public catalog shows dynamically. |  |
| PRD-019 | Support visible statuses plus hidden `Next` | important | full | `1.2 Collection Data & Persistence`: visible statuses plus hidden `next` in DB constraints. |  |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | full | `1.2 Collection Data & Persistence`: Interested/Excited set `myStatus = 'later'` plus interest value. |  |
| PRD-021 | Support free-form multi-tag personal tag library | important | full | `1.2 Collection Data & Persistence` and `2.1 Supabase Schema`: `my_tags` stored as `TEXT[]`. |  |
| PRD-022 | Define collection membership by assigned status | critical | full | `1.2 Collection Data & Persistence`: collection membership is `myStatus` not null. |  |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | full | `1.2 Collection Data & Persistence` and `4.1 Auto-Save Trigger Logic`: unified save handler covers all four triggers. |  |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | `4.1 Auto-Save Trigger Logic`: rating defaults to `done`; tags/interest default to `later` plus `interested`. |  |
| PRD-025 | Removing status deletes show and all My Data | critical | full | `1.2 Collection Data & Persistence` and `4.3 Show Removal and confirmation`: confirmed delete removes the row. |  |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | full | `1.2 Collection Data & Persistence`: retain existing `my_*` data and update only public fields. |  |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | `1.2 Collection Data & Persistence` and `2.1 Supabase Schema`: per-field `*_update_date` columns. |  |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | full | `1.2 Collection Data & Persistence`: timestamps drive home sorting, conflict resolution, and Scoop freshness. |  |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | full | `1.5 Show Detail & Relationship UX`: "Save only if saved to collection"; `5.3 AI Scoop Generation`: regenerate if older than 4 hours. |  |
| PRD-030 | Keep Ask and Alchemy state session-only | important | full | `1.2 Collection Data & Persistence`: chat history and Alchemy state stay in component state or session storage, never DB. |  |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | partial | `1.2 Collection Data & Persistence`: match AI-emitted details to catalog search and load full show details. | It omits the external-ID-first mapping contract and does not define the non-interactive/Search fallback for unresolved titles. |
| PRD-032 | Show collection and rating tile indicators | important | full | `1.2 Collection Data & Persistence` and `3. Directory Layout`: `ShowTile` renders in-collection and rating indicators. |  |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | partial | `1.2 Collection Data & Persistence`: timestamp conflict resolution for synced settings. | The plan covers newer-wins conflict handling, but it does not spell out transparent duplicate-library detection and merge behavior. |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | full | `1.2 Collection Data & Persistence` and `2.1 Supabase Schema`: forward-only upgrade scripts preserve rows. |  |
| PRD-035 | Persist synced settings, local settings, UI state | important | full | `1.2 Collection Data & Persistence` and `2.2 Local Storage Schema`: `cloud_settings`, local settings, and UI state keys. |  |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | full | `1.2 Collection Data & Persistence` and `2.1 Supabase Schema`: persist `provider_data`; fetch credits/trailers transiently. |  |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | partial | `4.2 Field Merge Policy` defines `selectFirstNonEmpty` and updates `detailsUpdateDate`. | The non-user merge is concrete, but the timestamp-based merge policy for `my*` fields is not fully specified. |
| PRD-038 | Provide filters panel and main screen destinations | important | full | `1.3 App Navigation & Discover Shell` and `6.3 Layout Shell & Navigation Panel`. |  |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | full | `1.3 App Navigation & Discover Shell`: persistent Find button in the sidebar. |  |
| PRD-040 | Keep Settings in persistent primary navigation | important | full | `1.3 App Navigation & Discover Shell`: Settings button pinned at the bottom of the sidebar. |  |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | `1.3 App Navigation & Discover Shell` and `3. Directory Layout`: mode switcher inside Discover workspace. |  |
| PRD-042 | Show only library items matching active filters | important | full | `1.4 Collection Home & Search`: filter local or persisted shows by the selected sidebar filter. |  |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | `1.4 Collection Home & Search` and `6.4 Collection Home Grid & Search Page`: four grouped sections. |  |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | full | `1.4 Collection Home & Search` and `6.3 Layout Shell & Navigation Panel`: all filter criteria plus media toggle. |  |
| PRD-045 | Render poster, title, and My Data badges | important | full | `1.4 Collection Home & Search` and `3. Directory Layout`: standard tiles show poster, title, and badges. |  |
| PRD-046 | Provide empty-library and empty-filter states | detail | full | `1.4 Collection Home & Search`: explicit empty-library and empty-filter UX states. |  |
| PRD-047 | Search by title or keywords | important | full | `1.4 Collection Home & Search` and `6.4 Collection Home Grid & Search Page`: debounced catalog search by title/keywords. |  |
| PRD-048 | Use poster grid with collection markers | important | full | `1.4 Collection Home & Search`: search results render as cards with overlay collection indicators. |  |
| PRD-049 | Auto-open Search when setting is enabled | detail | partial | `1.4 Collection Home & Search`: read `autoSearch` and route to Discover/Search "if true and library is empty/new." | The plan narrows the behavior to empty/new libraries, while the requirement is launch behavior whenever the setting is enabled. |
| PRD-050 | Keep Search non-AI in tone | important | full | `1.4 Collection Home & Search`: "Keep Search purely factual... No AI summaries here." |  |
| PRD-051 | Preserve Show Detail narrative section order | important | full | `1.5 Show Detail & Relationship UX` and `6.5 Show Detail View & Relationship Toolbar`: preserve the exact layout hierarchy. |  |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | full | `1.5 Show Detail & Relationship UX`: trailer-first header with poster/backdrop fallback. |  |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | full | `1.5 Show Detail & Relationship UX`: core stats shown prominently beneath the header. |  |
| PRD-054 | Place status/interest controls in toolbar | important | full | `1.5 Show Detail & Relationship UX` and `3. Directory Layout`: relationship toolbar owns status chips. |  |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | `1.5 Show Detail & Relationship UX` and `4.1 Auto-Save Trigger Logic`. |  |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | `1.5 Show Detail & Relationship UX` and `4.1 Auto-Save Trigger Logic`. |  |
| PRD-057 | Show overview early for fast scanning | important | full | `1.5 Show Detail & Relationship UX`: overview positioned immediately below top facts and tags. |  |
| PRD-058 | Scoop shows correct states and progressive feedback | important | partial | `1.5 Show Detail & Relationship UX`: stream chunk-by-chunk with spinner and "Generating..." feedback. | It covers generation feedback and persistence, but not the required no-scoop, cached-scoop, and open-state copy/state transitions. |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | full | `1.5 Show Detail & Relationship UX`: deep-link into Ask with a pre-filled show prompt. |  |
| PRD-060 | Include traditional recommendations strand | important | full | `1.5 Show Detail & Relationship UX`: horizontal slider from catalog recommendations. |  |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | full | `1.5 Show Detail & Relationship UX`: "Get Concepts" first, then chips, then unlock "Explore Shows". |  |
| PRD-062 | Include streaming availability and person-linking credits | important | full | `1.5 Show Detail & Relationship UX`: fetch providers and cast/crew with person links. |  |
| PRD-063 | Gate seasons to TV and financials to movies | important | full | `1.5 Show Detail & Relationship UX`: conditional rendering based on `showType`. |  |
| PRD-064 | Keep primary actions early and page not overwhelming | important | partial | `1.5 Show Detail & Relationship UX`: cluster interactive items in a top deck. | Early actions are covered, but the plan does not define the long-tail/full-bleed density treatment needed to keep the large Detail page from feeling overwhelming. |
| PRD-065 | Provide conversational Ask chat interface | important | full | `1.6 Ask Chat` and `6.6 Discover AI Services`: user/assistant bubbles plus text field. |  |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | partial | `1.6 Ask Chat` and `5.2 Ask Mode Contract`: friendly, opinionated, spoiler-safe guidance. | The traceability row says “direct,” but the concrete Ask prompt/acceptance contract does not require the answer within the first 3-5 lines. |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | `1.6 Ask Chat`: parse structured response into a poster carousel below the message. |  |
| PRD-068 | Open Detail from mentions or Search fallback | important | full | `1.6 Ask Chat`: click poster to open Detail or fall back to Search. |  |
| PRD-069 | Show six random starter prompts with refresh | important | full | `1.6 Ask Chat`: six prompts from a static pool of 80 plus refresh. |  |
| PRD-070 | Summarize older turns while preserving voice | important | full | `1.6 Ask Chat`: summarize turns beyond 10 using the same "critic friend" voice. |  |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | full | `1.6 Ask Chat`: prefill Ask with a context payload about the source show. |  |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | full | `5.2 Ask Mode Contract`: exact JSON shape and `Title::externalId::mediaType` string format. |  |
| PRD-073 | Retry malformed mention output once, then fallback | important | full | `5.2 Ask Mode Contract`: one retry on parse failure, then commentary-only fallback. |  |
| PRD-074 | Redirect Ask back into TV/movie domain | important | full | `1.6 Ask Chat` and `5.1 System Prompt Wrapper`: refuse out-of-domain requests and redirect. |  |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | full | `1.7 Concepts, Explore Similar & Alchemy`: prompt focuses on vibes, pacing, themes, and structure. |  |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | partial | `1.7 Concepts, Explore Similar & Alchemy`: strict bullet-only, 1-3 word prompt validation. | Format and length are specified, but the plan does not define concept-specific rejection of generic placeholders such as “good characters.” |
| PRD-077 | Order concepts by strongest aha and varied axes | important | full | `1.7 Concepts, Explore Similar & Alchemy`: order by evocative strength across varied axes. |  |
| PRD-078 | Require concept selection and guide ingredient picking | important | partial | `1.7 Concepts, Explore Similar & Alchemy`: require at least one selected concept before requesting recs. | It enforces selection, but does not plan the user guidance or empty-state copy around picking taste ingredients. |
| PRD-079 | Return exactly five Explore Similar recommendations | important | full | `1.7 Concepts, Explore Similar & Alchemy`: constrain Explore Similar to exactly five shows. |  |
| PRD-080 | Support full Alchemy loop with chaining | important | full | `1.7 Concepts, Explore Similar & Alchemy` and `6.6 Discover AI Services`: full loop plus chaining. |  |
| PRD-081 | Clear downstream results when inputs change | important | full | `1.7 Concepts, Explore Similar & Alchemy`: handlers wipe concept and recommendation arrays on input changes. |  |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | full | `1.7 Concepts, Explore Similar & Alchemy`: request 10-15 common concepts for multi-show mode. |  |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | full | `1.7 Concepts, Explore Similar & Alchemy`: reasons explicitly cite chosen concepts. |  |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | partial | `1.7 Concepts, Explore Similar & Alchemy`: prompts calibrate for diversity while defending the picks. | “Calibrate prompts” is not a concrete surprise-without-betrayal generation rule or acceptance check. |
| PRD-085 | Keep one consistent AI persona across surfaces | important | full | `1.8 AI Voice, Persona & Quality` and `5.1 System Prompt Wrapper`: central shared persona module. |  |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | full | `1.8 AI Voice, Persona & Quality`: TV/movie limits, spoiler safety, and honesty enforced centrally. |  |
| PRD-087 | Make AI warm, joyful, and light in critique | important | partial | `1.8 AI Voice, Persona & Quality` and `5.1 System Prompt Wrapper`: critic-friend tone. | The shared prompt covers enthusiasm and honesty, but it does not explicitly preserve joy-forward warmth and light, non-mean critique. |
| PRD-088 | Structure Scoop as personal taste mini-review | important | full | `1.8 AI Voice, Persona & Quality` and `5.3 AI Scoop Generation`: defined mini-review structure. |  |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | full | `1.8 AI Voice, Persona & Quality`: Ask kept under three paragraphs unless the user asks for depth. |  |
| PRD-090 | Feed AI the right surface-specific context inputs | important | full | `1.8 AI Voice, Persona & Quality`, `1.6 Ask Chat`, and `1.7 Concepts`: library, show, and concept context are passed per surface. |  |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | partial | `1.8 AI Voice, Persona & Quality`: assertions for format, count, and real catalog keys. | It checks structural integrity, but it does not operationalize rubric-based failures for voice and taste alignment. |
| PRD-092 | Show person gallery, name, and bio | important | partial | `1.9 Person Detail`: person page with profile image, biography, and facts. | The plan covers a profile image and biography, but not the requested person image gallery. |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | full | `1.9 Person Detail` and `3. Directory Layout`: analytics charts cover ratings, genres, and yearly project metrics. |  |
| PRD-094 | Group filmography by year | important | full | `1.9 Person Detail`: credits organized in descending order by year. |  |
| PRD-095 | Open Show Detail from selected credit | important | full | `1.9 Person Detail`: credit rows navigate back to the show detail screen. |  |
| PRD-096 | Include font size and Search-on-launch settings | important | full | `1.10 Settings & Export` and `2.2 Local Storage Schema`: both settings are persisted and exposed. |  |
| PRD-097 | Support username, model, and API-key settings safely | important | full | `1.10 Settings & Export`: safe settings persisted in `cloud_settings` without hardcoded keys. |  |
| PRD-098 | Export saved shows and My Data as zip | critical | full | `1.10 Settings & Export` and `6.7 Backup Export & Sync Systems`: zip export of DB snapshot and metadata. |  |
| PRD-099 | Encode export dates using ISO-8601 | important | full | `1.10 Settings & Export` and `7.3 Exporter Integrity Testing`: explicit ISO-8601 export validation. |  |

## 3. Coverage Scores

Overall score:

`(82 × 1.0 + 17 × 0.5) / 99 × 100 = 91.4%`

Score by severity tier:

`Critical:  (27 × 1.0 + 3 × 0.5) / 30 × 100 = 95.0%  (28.5 of 30 critical requirements)`
`Important: (54 × 1.0 + 13 × 0.5) / 67 × 100 = 90.3%  (60.5 of 67 important requirements)`
`Detail:    (1 × 1.0 + 1 × 0.5) / 2 × 100 = 75.0%  (1.5 of 2 detail requirements)`
`Overall:   91.4% (99 total requirements)`

## 4. Top Gaps

1. PRD-037 | `critical` | Merge catalog fields safely and maintain timestamps
The plan defines public-field merging but leaves the `my*` timestamp conflict policy underspecified, which risks losing or regressing user edits during sync and catalog refreshes.

2. PRD-031 | `critical` | Resolve AI recommendations to real selectable shows
If the mapping logic is not external-ID-first and failure-aware, AI results can become brittle, non-interactive, or mismatched to the wrong catalog entry.

3. PRD-001 | `critical` | Use Next.js latest stable runtime
The plan's stale or ambiguous v14/v15 target could put the build outside the benchmark baseline before implementation even starts.

4. PRD-091 | `important` | Validate discovery with rubric and hard-fail integrity
Format-only validation is not enough for this product; weak voice or shallow taste alignment would pass technical checks while still failing the core discovery promise.

5. PRD-033 | `important` | Sync libraries/settings consistently and merge duplicates
Conflict timestamps alone do not prevent duplicate or split library records, and that kind of integrity failure would directly erode trust in cross-device behavior.

## 5. Coverage Narrative

#### Overall Posture

This is a strong but materially over-credited plan. It tracks almost every benchmark requirement and gives concrete implementation direction across persistence, UI structure, and AI surfaces, but several rows rely on broad traceability claims where the PRD asks for narrower behavioral contracts. The recomputed score is lower because those narrowed or incomplete behaviors should be treated as partial, not full. Separately, the plan explicitly references the evaluator-only canonical catalog, so the run is benchmark-contaminated; the 91.4% coverage score does not apply an additional contamination penalty.

#### Strength Clusters

The plan is strongest in App Navigation & Discover Shell, Collection Home & Search, Ask Chat, and the core save/default portions of Show Detail & Relationship UX. Those areas are covered with both traceability rows and follow-through sections on layout, prompt contracts, schema, and testing. Collection Data & Persistence is also strong on core storage shape, implicit saves, and namespace/user partitioning.

#### Weakness Clusters

The gaps cluster around precision rather than missing screens. Infrastructure has a stale runtime target, incomplete environment-ignore coverage, and lacks explicit documentation work for dev identity injection. Data, Detail UX, and AI quality gaps center on edge-case contracts: external-ID-first recommendation resolution, timestamp-based `my*` merge semantics, duplicate handling, Scoop states, anti-clutter treatment, direct-first Ask responses, non-generic concepts, surprise-without-betrayal, voice pillars, concept-selection guidance, and rubric-based validation.

#### Risk Assessment

If this plan were executed as-is, the first visible failure would likely be subtle behavioral drift rather than a missing page. A QA reviewer would catch stale runtime assumptions, unreliable recommendation resolution, incomplete Scoop states, a crowded Detail page, or sync paths that blur catalog updates with user-owned edits. On the AI side, outputs might be formally structured but still feel evasive, generic, insufficiently surprising, or harsher and flatter than the intended persona.

#### Remediation Guidance

The missing work is mostly specification tightening, not wholesale replanning. The plan needs updated runtime/version language, the exact environment-ignore rule, explicit documentation tasks for benchmark auth injection, sharper duplicate/merge acceptance criteria, and fuller UI state and density specs. It also needs direct-first Ask, non-generic concept, surprise, warmth/light-critique, and rubric gates rather than treating formatting as the whole AI quality bar.
