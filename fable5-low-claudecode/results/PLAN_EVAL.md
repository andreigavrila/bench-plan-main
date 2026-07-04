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
| PRD-001 | Use Next.js latest stable runtime | critical | full | `Scope Summary`: "Next.js (latest stable) + Supabase" |  |
| PRD-002 | Use Supabase official client libraries | critical | partial | `Scope Summary`: "Supabase"; `Architecture`: "Supabase ... persistence" | The plan commits to Supabase but does not explicitly require the official Supabase client libraries. |
| PRD-003 | Ship `.env.example` with required variables | critical | full | `Phase 0`: `.env.example` lists Supabase, namespace, user, catalog, and AI vars |  |
| PRD-004 | Ignore `.env*` secrets except example | important | full | `Phase 0`: ".gitignore for `.env*`"; `Compliance Checklist`: secrets never committed |  |
| PRD-005 | Configure build through env without code edits | critical | full | `Scope Summary`: keys via env var; `Compliance Checklist`: "config-only setup" |  |
| PRD-006 | Keep secrets out of repo and server-only | critical | full | `Architecture 2.1`: "All external API keys stay server-side"; `Compliance Checklist`: "elevated keys server-only" |  |
| PRD-007 | Provide app, test, reset command scripts | critical | full | `Phase 0`: scripts `dev` / `test` / `test:reset` |  |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | `Database schema`: "Migrations via Supabase SQL migration files" |  |
| PRD-009 | Use one stable namespace per build | critical | full | `Identity & isolation`: "`NAMESPACE_ID` env var: stable per build/run" |  |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | `Identity & isolation`: all queries filter by namespace; reset deletes only within it |  |
| PRD-011 | Attach every user record to `user_id` | critical | full | `Identity & isolation`: "`user_id`: opaque string"; `Compliance Checklist`: "All rows carry `namespace_id` + `user_id`" |  |
| PRD-012 | Partition persisted data by namespace and user | critical | full | `Identity & isolation`: "Effective partition everywhere: `(namespace_id, user_id)`" |  |
| PRD-013 | Support documented dev auth injection, prod-gated | important | full | `Identity & isolation`: `X-User-Id` dev/test only, gated by environment/flag |  |
| PRD-014 | Real OAuth later needs no schema redesign | important | full | `Identity & isolation`: real OAuth changes only how `user_id` is derived |  |
| PRD-015 | Keep backend as persisted source of truth | critical | full | `Scope Summary`: "backend is the source of truth"; `Compliance Checklist` repeats it |  |
| PRD-016 | Make client cache safe to discard | critical | full | `Architecture 2.1`: "React Query for client caching; safe to clear at any time" |  |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | full | `Database schema`: "Docker is not required"; `Compliance Checklist`: "hosted Supabase primary path" |  |
| PRD-018 | Overlay saved user data on every show appearance | critical | full | `Business-rules service`: "every list/search/AI result response is overlaid" |  |
| PRD-019 | Support visible statuses plus hidden `Next` | important | full | `Database schema`: `my_status` includes `next`; `Risks & Open Questions`: Next out of UI scope but schema supports it |  |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | partial | `Business-rules service`: interest chip save trigger; `Show Detail`: status/interest chips in toolbar | The plan includes interest chips and Later/Interested defaults, but does not explicitly state that Interested and Excited chips set `my_status = later` with the selected interest. |
| PRD-021 | Support free-form multi-tag personal tag library | important | full | `shows` schema: `my_tags text[]`; `Layout`: tag filters plus "No tags"; `Show Detail`: tag picker |  |
| PRD-022 | Define collection membership by assigned status | critical | full | `Database schema`: "`shows` - user-scoped saved shows (a row is collection membership)" |  |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | full | `Business-rules service`: save triggers list all four mutation paths |  |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | `Business-rules service`: defaults and rating exception are explicit |  |
| PRD-025 | Removing status deletes show and all My Data | critical | full | `Business-rules service`: "clearing status deletes the row (all My Data + scoop gone)" |  |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | full | `Business-rules service`: merge keeps newer My fields and refreshes catalog fields |  |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | `shows` schema lists five timestamps; `Business-rules service`: every My-field write stamps update date |  |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | partial | `Business-rules service`: timestamp merge; `API`: Scoop 4-hour freshness | The plan uses timestamps for sync/conflict handling and Scoop freshness, but does not specify timestamp-based sorting. |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | full | `API surface`: Scoop persisted only if in collection with 4-hour freshness check |  |
| PRD-030 | Keep Ask and Alchemy state session-only | important | full | `AI layer`: chat state session-only; `Find hub`: Alchemy results session-only |  |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | full | `API surface`: recs resolved to real catalog item; `AI layer`: real-show integrity non-negotiable |  |
| PRD-032 | Show collection and rating tile indicators | important | full | `Home`: tiles show in-collection and rating badges |  |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | partial | `settings` table per partition; `Business-rules service`: My-fields resolve by timestamp | The plan covers consistent persisted settings and timestamp conflict resolution but does not explicitly cover duplicate detection and transparent duplicate merging. |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | full | `app_metadata`: data model version for migration continuity |  |
| PRD-035 | Persist synced settings, local settings, UI state | important | full | `settings` and `ui_state` tables include synced settings, local settings, and UI state keys |  |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | full | `shows` schema stores `provider_data jsonb`; `Catalog integration` fetches detail-side credits/videos/images/providers |  |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | full | `Business-rules service`: `selectFirstNonEmpty`, timestamp My-field resolution, details timestamp |  |
| PRD-038 | Provide filters panel and main screen destinations | important | full | `Frontend structure`: persistent sidebar and top-level nav; UI routes listed |  |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | full | `Layout`: "top-level nav to Find and Settings" |  |
| PRD-040 | Keep Settings in persistent primary navigation | important | full | `Layout`: "top-level nav to Find and Settings" |  |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | `Find hub`: mode switcher Search / Ask / Alchemy |  |
| PRD-042 | Show only library items matching active filters | important | full | `API surface`: `/api/collection` with filter params; `Layout`: media toggle applies atop any filter |  |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | `Home`: status sections in required order with collapsed Other |  |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | full | `Layout`: All Shows, tag, genre, decade, community-score, media-type toggle |  |
| PRD-045 | Render poster, title, and My Data badges | important | full | `Home`: "tiles show poster/title + in-collection and rating badges" |  |
| PRD-046 | Provide empty-library and empty-filter states | detail | full | `Home`: "empty states per PRD"; `Phase 5`: empty states |  |
| PRD-047 | Search by title or keywords | important | partial | `API surface`: `GET /api/catalog/search?q=`; `Find hub`: Search mode | The plan defines catalog search but does not explicitly state title and keyword search behavior. |
| PRD-048 | Use poster grid with collection markers | important | full | `Find hub`: "Search: poster grid, in-collection marks" |  |
| PRD-049 | Auto-open Search when setting is enabled | detail | full | `Find hub`: optional auto-open on launch via `autoSearch` |  |
| PRD-050 | Keep Search non-AI in tone | important | partial | `Find hub`: Search is a catalog poster grid separate from AI Ask/Alchemy | The plan implies non-AI Search by architecture but does not explicitly preserve the straightforward, non-AI tone requirement. |
| PRD-051 | Preserve Show Detail narrative section order | important | full | `Show Detail`: section order copied from `detail_page_experience.md` |  |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | full | `Show Detail`: header media carousel with trailer/poster fallback |  |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | full | `Show Detail`: core facts + community score immediately after header |  |
| PRD-054 | Place status/interest controls in toolbar | important | full | `Show Detail`: "Status/interest chips in toolbar" |  |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | `Show Detail`: "tag picker auto-save-as-Later+Interested" |  |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | `Show Detail`: "rating slider auto-save-as-Done" |  |
| PRD-057 | Show overview early for fast scanning | important | full | `Show Detail`: overview appears before Ask, genres, recs, providers, credits |  |
| PRD-058 | Scoop shows correct states and progressive feedback | important | full | `Show Detail`: exact toggle labels plus streaming and 4-hour cache |  |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | full | `Show Detail`: "Ask about this show" seeds Ask with show context |  |
| PRD-060 | Include traditional recommendations strand | important | full | `Show Detail`: recommendations strand before Explore Similar |  |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | full | `Show Detail`: "Get Concepts -> chips -> Explore Shows" |  |
| PRD-062 | Include streaming availability and person-linking credits | important | full | `Show Detail`: streaming providers and cast/crew strands; `Person Detail` links back |  |
| PRD-063 | Gate seasons to TV and financials to movies | important | full | `Show Detail`: seasons (TV) and budget/revenue (movies) |  |
| PRD-064 | Keep primary actions early and page not overwhelming | important | partial | `Show Detail`: toolbar controls and Scoop/overview appear early | The plan places actions early but does not explicitly address the busyness constraint or layout treatment that keeps the page from becoming overwhelming. |
| PRD-065 | Provide conversational Ask chat interface | important | full | `Find hub`: "Ask: chat UI, mentioned-shows strip, starter prompts, streaming" |  |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | full | `AI layer`: Ask is a brisk friend, picks favorites, and shared persona is spoiler-safe |  |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | `Find hub`: mentioned-shows strip |  |
| PRD-068 | Open Detail from mentions or Search fallback | important | partial | `AI layer`: unresolved titles render non-interactive or hand off to Search | The fallback is covered, but the plan does not explicitly state that resolved mentioned-show items open Show Detail. |
| PRD-069 | Show six random starter prompts with refresh | important | full | `AI layer`: "6 random starter prompts ... with refresh" |  |
| PRD-070 | Summarize older turns while preserving voice | important | full | `AI layer`: older turns compressed to 1-2 sentences in-persona |  |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | full | `Show Detail`: Ask about this show seeds Ask with show context |  |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | full | `API surface` and `AI layer`: exact `{commentary, showList}` and `Title::externalId::mediaType;;...` contract |  |
| PRD-073 | Retry malformed mention output once, then fallback | important | full | `AI layer`: parse failure retry once, else unstructured commentary + Search handoff |  |
| PRD-074 | Redirect Ask back into TV/movie domain | important | full | `AI layer`: shared persona includes "TV/movies only" |  |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | partial | `AI layer`: Concepts are evocative, no generics, ordered by strength and diverse axes | The plan captures evocative concept quality but does not explicitly define concepts as taste ingredients rather than genres or plot categories. |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | full | `AI layer`: "bullet-only, 1-3 words, evocative, no generics" |  |
| PRD-077 | Order concepts by strongest aha and varied axes | important | full | `AI layer`: "ordered by strength, diverse axes" |  |
| PRD-078 | Require concept selection and guide ingredient picking | important | partial | `Find hub`: select up to 8 concept chips; `Show Detail`: chips before Explore Shows | The plan requires selection in the flow but does not include the ingredient-picking guidance copy or empty-state nudge. |
| PRD-079 | Return exactly five Explore Similar recommendations | important | full | `API surface`: 5 for Explore Similar; `Find hub`: Explore Similar 5 recs |  |
| PRD-080 | Support full Alchemy loop with chaining | important | full | `Find hub`: pick shows, conceptualize, select chips, alchemize, More Alchemy chaining |  |
| PRD-081 | Clear downstream results when inputs change | important | full | `Find hub`: changing shows/concepts clears downstream state |  |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | partial | `API surface`: concepts from 1..n show ids; shared commonality when multiple | The plan covers shared multi-show concepts but fixes concepts at 8 for 1..n inputs, so it misses the larger option pool for multi-show generation. |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | full | `AI layer`: concept rec reasons name matched concepts; `API`: each rec includes reason |  |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | partial | `Testing & quality bar`: manual AI check against quality rubric; `AI layer`: reasons name concepts | The plan validates taste alignment but does not explicitly plan for pleasantly unexpected yet defensible recommendations. |
| PRD-085 | Keep one consistent AI persona across surfaces | important | full | `AI layer`: shared persona system prompt across surfaces |  |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | full | `AI layer`: warm, opinionated, spoiler-safe, vibe-first, TV/movies only |  |
| PRD-087 | Make AI warm, joyful, and light in critique | important | full | `AI layer`: warm, opinionated, spoiler-safe; Scoop and concept modes inherit persona |  |
| PRD-088 | Structure Scoop as personal taste mini-review | important | full | `AI layer`: Scoop mini blog post with required sections and length target |  |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | full | `AI layer`: Ask as "brisk friend"; summarized in-persona |  |
| PRD-090 | Feed AI the right surface-specific context inputs | important | full | `AI layer`: library + My Data, current-show context, selected concepts |  |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | full | `Testing & quality bar`: rubric thresholds and real-show integrity = 2 |  |
| PRD-092 | Show person gallery, name, and bio | important | partial | `Person Detail`: "gallery, bio"; `API`: person details + credits | The plan covers gallery and bio, and implies person details, but does not explicitly name the person-name display requirement. |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | full | `Person Detail`: analytics charts for average ratings, top genres, projects-by-year |  |
| PRD-094 | Group filmography by year | important | full | `Person Detail`: filmography grouped by year |  |
| PRD-095 | Open Show Detail from selected credit | important | full | `Person Detail`: filmography links back to Detail |  |
| PRD-096 | Include font size and Search-on-launch settings | important | full | `Settings`: font size and search-on-launch |  |
| PRD-097 | Support username, model, and API-key settings safely | important | full | `Settings`: username, AI key/model, catalog key; API keys never seeded from repo |  |
| PRD-098 | Export saved shows and My Data as zip | critical | full | `API surface`: `/api/export` zip with JSON backup; `Settings`: Export My Data |  |
| PRD-099 | Encode export dates using ISO-8601 | important | full | `API surface`: "zip with JSON backup, ISO-8601 dates" |  |

### 3. Coverage Scores

Critical:  (28 full × 1.0 + 2 partial × 0.5) / 30 × 100 = 96.7%  (29 of 30 critical requirements)
Important: (56 full × 1.0 + 11 partial × 0.5) / 67 × 100 = 91.8%  (61.5 of 67 important requirements)
Detail:    (2 full × 1.0 + 0 partial × 0.5) / 2 × 100 = 100.0%  (2 of 2 detail requirements)
Overall:   93.4% (99 total requirements)

### 4. Top Gaps

- PRD-020 (`critical`) Map Interested/Excited chips to Later interest: Without the exact mapping, collection state can drift between status and interest and break home grouping for Later items.
- PRD-002 (`critical`) Use Supabase official client libraries: The plan commits to Supabase but not the official client libraries, leaving a compliance ambiguity around the benchmark's required integration path.
- PRD-033 (`important`) Sync libraries/settings consistently and merge duplicates: Without explicit duplicate detection and transparent merging, synced collections can drift or show duplicate saved items across devices or migrations.
- PRD-082 (`important`) Generate shared multi-show concepts with larger option pool: The plan's fixed 8-concept endpoint risks under-serving Alchemy, where users need a broader shared-concept pool before selecting ingredients.
- PRD-068 (`important`) Open Detail from mentions or Search fallback: If mentioned shows do not explicitly click through to Detail, Ask recommendations become less actionable even when they resolve correctly.

### 5. Coverage Narrative

#### Overall Posture

This is a strong implementation plan with high coverage across the core product and infrastructure contract. It is especially solid on persistence boundaries, namespace/user isolation, save/remove/default behavior, Detail page structure, and AI output contracts. The remaining gaps are mostly specificity gaps rather than absent product areas.

#### Strength Clusters

The plan is strongest in Benchmark Runtime & Isolation, Collection Data & Persistence, Show Detail & Relationship UX, Ask Chat, AI Voice/Persona/Quality, and Settings & Export. It repeatedly centralizes business rules server-side, names the required schema fields, and translates most PRD behavior into concrete route handlers, frontend flows, and tests.

#### Weakness Clusters

The partial items cluster around exact behavioral acceptance details at the edges of otherwise-covered features. Search is architecturally present but tone and title/keyword semantics are not spelled out. Concepts and Alchemy are present, but the "taste ingredient" framing, ingredient-picking guidance, larger multi-show concept pool, and surprise-quality target are under-specified. Data sync covers timestamp conflict resolution, but not duplicate merging.

#### Risk Assessment

If executed as-is, the most likely failure mode is a build that passes broad feature walkthroughs but loses some product-specific polish and evaluator-specific precision. QA would probably notice small gaps first: Ask mentions that do not clearly open Detail, Alchemy concept choices that feel too narrow, Search lacking a stated plain catalog tone, or duplicate library rows after sync/import-like scenarios.

#### Remediation Guidance

The plan needs targeted acceptance-detail additions, not a structural rewrite. Add explicit implementation notes for official Supabase client usage, duplicate detection and merge behavior, Search title/keyword and non-AI tone, mention click-through to Detail, concept ingredient framing with UI guidance, larger multi-show concept pools, and "surprising but defensible" recommendation checks in the AI quality rubric.
