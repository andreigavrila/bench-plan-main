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
| PRD-001 | Use Next.js latest stable runtime | critical | full | `0. Reading Summary`; `1.1 Stack`; `Phase 0` |  |
| PRD-002 | Use Supabase official client libraries | critical | full | `0. Reading Summary`; `1.1 Stack` says `@supabase/supabase-js` |  |
| PRD-003 | Ship `.env.example` with required variables | critical | full | `0. Reading Summary`; `Phase 0` includes `.env.example` |  |
| PRD-004 | Ignore `.env*` secrets except example | important | partial | `7. Settings, Secrets & Export` covers secret handling | The plan says secrets are server-only and not returned, but does not explicitly require `.gitignore` to exclude `.env*` except `.env.example`. |
| PRD-005 | Configure build through env without code edits | critical | full | `0. Reading Summary`; `3. Identity, Namespace & Auth`; `7. Settings, Secrets & Export` |  |
| PRD-006 | Keep secrets out of repo and server-only | critical | full | `1.1 Stack`; `7. Settings, Secrets & Export` |  |
| PRD-007 | Provide app, test, reset command scripts | critical | full | `0. Reading Summary`; `10. Testing & Quality Strategy`; `Phase 0` |  |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | `2.2 Migrations & Seed`; `Phase 0` |  |
| PRD-009 | Use one stable namespace per build | critical | full | `0. Reading Summary`; `3. Identity, Namespace & Auth` |  |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | `3. Identity, Namespace & Auth`; `4.6 Test/Dev Utilities`; `10. Testing & Quality Strategy` |  |
| PRD-011 | Attach every user record to `user_id` | critical | full | `0. Reading Summary`; `2.1 Tables`; `9. Cross-Cutting Rules` |  |
| PRD-012 | Partition persisted data by namespace and user | critical | full | `1.3 Key Architectural Decision`; `2.1 Tables`; `3. Identity, Namespace & Auth` |  |
| PRD-013 | Support documented dev auth injection, prod-gated | important | full | `3. Identity, Namespace & Auth` |  |
| PRD-014 | Real OAuth later needs no schema redesign | important | full | `3. Identity, Namespace & Auth`; `users` table note |  |
| PRD-015 | Keep backend as persisted source of truth | critical | full | `0. Reading Summary`; `6.5 Data Sync`; `9. Cross-Cutting Rules` |  |
| PRD-016 | Make client cache safe to discard | critical | full | `8.1 State/Data Fetching`; `9. Cross-Cutting Rules`; `Phase 9` |  |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | full | `0. Reading Summary` says no Docker dependency required |  |
| PRD-018 | Overlay saved user data on every show appearance | critical | full | `1.3 Key Architectural Decision`; `9. Cross-Cutting Rules` |  |
| PRD-019 | Support visible statuses plus hidden `Next` | important | full | `2.1 user_shows`; `11. Decisions on Open Questions` |  |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | full | `4.2 Collection Mutations`; `6.1 Save/Remove Triggers` |  |
| PRD-021 | Support free-form multi-tag personal tag library | important | full | `2.1 user_shows`; `4.2 GET /api/tags`; `8 Frontend Architecture` |  |
| PRD-022 | Define collection membership by assigned status | critical | full | `2.1 user_shows`; `6.1 Save/Remove Triggers` |  |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | full | `4.2 Collection Mutations`; `6.1 Save/Remove Triggers` |  |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | `6.1 Save/Remove Triggers` |  |
| PRD-025 | Removing status deletes show and all My Data | critical | full | `4.2 DELETE /api/shows/:id/collection`; `6.1 Save/Remove Triggers` |  |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | full | `2.4 Field Mapping & Merge Rules`; `6.2 Re-adding / Sync Merge` |  |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | `2.1 user_shows`; `6.3 Timestamps` |  |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | full | `6.3 Timestamps` |  |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | full | `4.3 AI Surfaces`; `5.3 Contracts Per Surface`; `7. Settings, Secrets & Export` |  |
| PRD-030 | Keep Ask and Alchemy state session-only | important | full | `8.1 State/Data Fetching`; `5.3 Contracts Per Surface` |  |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | full | `5.4 Real-Show Resolution`; `9. Cross-Cutting Rules` |  |
| PRD-032 | Show collection and rating tile indicators | important | full | `4.2 GET /api/collection`; `6.4 Tile Indicators` |  |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | partial | `6.5 Data Sync & Conflict Resolution`; `Phase 9` | Timestamp conflict resolution is covered, but duplicate detection/merge is only implicit through keys and not called out as a sync behavior. |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | full | `6.6 Data Continuity Across Versions`; `Phase 9` |  |
| PRD-035 | Persist synced settings, local settings, UI state | important | full | `2.1 cloud_settings`; local settings paragraph; `7. Settings, Secrets & Export` |  |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | full | `2.1 shows`; `2.4 Field Mapping & Merge Rules`; `4.1 GET /api/shows/:id` |  |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | full | `1.3 Key Architectural Decision`; `2.4 Field Mapping & Merge Rules` |  |
| PRD-038 | Provide filters panel and main screen destinations | important | full | `8. Frontend Architecture`; `Home/features/FiltersPanel` |  |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | full | `8. Frontend Architecture` says persistent nav |  |
| PRD-040 | Keep Settings in persistent primary navigation | important | full | `8. Frontend Architecture` says persistent nav |  |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | `Find.tsx mode switcher: Search | Ask | Alchemy` |  |
| PRD-042 | Show only library items matching active filters | important | full | `4.2 GET /api/collection`; `Phase 1` |  |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | `8. Frontend Architecture`; `Phase 1` |  |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | full | `4.2 GET /api/collection`; `8. Frontend Architecture`; `11. Decisions` |  |
| PRD-045 | Render poster, title, and My Data badges | important | full | `8. Frontend Architecture`; `Phase 1` |  |
| PRD-046 | Provide empty-library and empty-filter states | detail | full | `8. Frontend Architecture`; `Phase 1` |  |
| PRD-047 | Search by title or keywords | important | full | `4.1 Catalog & Search`; `Phase 1` |  |
| PRD-048 | Use poster grid with collection markers | important | full | `4.1 Catalog & Search`; `8. Frontend Architecture` |  |
| PRD-049 | Auto-open Search when setting is enabled | detail | full | `2.1 Local-only`; `7. Settings`; `Phase 8` |  |
| PRD-050 | Keep Search non-AI in tone | important | full | `5.2 Shared Persona Layer`; `9. Cross-Cutting Rules` |  |
| PRD-051 | Preserve Show Detail narrative section order | important | partial | `8. Frontend Architecture`; `10. Visual testing` | The plan includes the major sections and screenshot tests, but its listed order differs from the supporting doc hierarchy and omits an explicit genres/languages placement. |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | partial | `HeaderMedia` feature; `Phase 2` | The plan names trailers/backdrops/posters/logos but does not explicitly specify prioritizing motion or graceful fallback behavior when media is missing. |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | full | `CoreFactsRow`; `Phase 2` |  |
| PRD-054 | Place status/interest controls in toolbar | important | partial | `6.1 Save/Remove Triggers`; `MyRelationshipControls`; `Phase 2` | The plan includes status and interest controls, but does not explicitly place them in a toolbar. |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | `4.2 Collection Mutations`; `6.1 Save/Remove Triggers` |  |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | `4.2 Collection Mutations`; `6.1 Save/Remove Triggers` |  |
| PRD-057 | Show overview early for fast scanning | important | full | `OverviewAndScoop`; `Phase 2` |  |
| PRD-058 | Scoop shows correct states and progressive feedback | important | partial | `4.3 POST /api/ai/scoop`; `5.3 Contracts Per Surface`; `Phase 3` | Streaming/progressive feedback and cache freshness are covered, but the explicit no-scoop/cached/open copy states are not specified. |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | full | `4.3 POST /api/ai/ask`; `AskAboutShowCta`; `Phase 6` |  |
| PRD-060 | Include traditional recommendations strand | important | full | `RecommendationsStrand`; `Phase 2` |  |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | full | `ExploreSimilar`; `Phase 4` |  |
| PRD-062 | Include streaming availability and person-linking credits | important | full | `4.1 GET /api/shows/:id`; `StreamingAvailability`; `CastCrewStrands`; `Phase 2` |  |
| PRD-063 | Gate seasons to TV and financials to movies | important | full | `SeasonsStrand`; `BudgetRevenue`; `Phase 2` |  |
| PRD-064 | Keep primary actions early and page not overwhelming | important | partial | `Detail` feature order; `Phase 2` | The plan orders primary content early, but does not directly specify busyness/clutter management. |
| PRD-065 | Provide conversational Ask chat interface | important | full | `Ask/features/ChatThread, Composer`; `Phase 6` |  |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | partial | `5.2 Shared Persona Layer`; `5.3 Contracts Per Surface`; `9. Cross-Cutting Rules` | The plan covers confidence and spoiler safety, but does not explicitly preserve the quality-bar requirement to answer directly within the first few lines. |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | `MentionedShowsStrip`; `Phase 6` |  |
| PRD-068 | Open Detail from mentions or Search fallback | important | full | `5.4 Real-Show Resolution`; `Phase 6` |  |
| PRD-069 | Show six random starter prompts with refresh | important | full | `Phase 6` says starter prompts `6 of 80, refreshable` |  |
| PRD-070 | Summarize older turns while preserving voice | important | full | `5.6 Conversation Summarization`; `Phase 6` |  |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | full | `4.3 POST /api/ai/ask`; `Phase 6` |  |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | full | `5.3 Contracts Per Surface`; `5.5 Structured Output Parsing` |  |
| PRD-073 | Retry malformed mention output once, then fallback | important | full | `5.5 Structured Output Parsing & Fallback` |  |
| PRD-074 | Redirect Ask back into TV/movie domain | important | partial | `5.2 Shared Persona Layer`; `9. Cross-Cutting Rules` | The plan establishes the TV/movie product domain, but does not explicitly define Ask redirect behavior for off-domain prompts. |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | partial | `5.2 Shared Persona Layer`; `5.3 Contracts Per Surface` | The plan constrains concepts, but does not explicitly encode the taste-ingredient-not-genre/plot-label rule. |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | full | `5.3 Contracts Per Surface`; `5.7 Concept & Recommendation Quality Guardrails` |  |
| PRD-077 | Order concepts by strongest aha and varied axes | important | partial | `4.3 POST /api/ai/concepts`; `5.7 Concept & Recommendation Quality Guardrails` | The plan requires ordering by strength, but varied axes are not explicitly required or tested beyond a generic quality process. |
| PRD-078 | Require concept selection and guide ingredient picking | important | partial | `ExploreSimilar`; `Alchemy ConceptSelector`; `Phase 4`; `Phase 5` | Concept selection is covered, but ingredient-picking guidance and nudges are not fully specified. |
| PRD-079 | Return exactly five Explore Similar recommendations | important | full | `4.3 POST /api/ai/recommendations`; `5.3 Contracts Per Surface`; `Phase 4` |  |
| PRD-080 | Support full Alchemy loop with chaining | important | full | `Phase 5` |  |
| PRD-081 | Clear downstream results when inputs change | important | full | `Phase 5` says backtracking clears downstream state |  |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | full | `5.3 Contracts Per Surface`; `Phase 5` |  |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | full | `5.3 Contracts Per Surface`; `5.4 Real-Show Resolution` |  |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | full | `10. Testing & Quality Strategy`; quality checklist includes surprise and taste alignment |  |
| PRD-085 | Keep one consistent AI persona across surfaces | important | full | `5.2 Shared Persona Layer` |  |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | partial | `5.2 Shared Persona Layer`; `9. Cross-Cutting Rules` | The shared persona layer covers several guardrails, but does not fully include the all-surface TV/movie-domain redirect rule. |
| PRD-087 | Make AI warm, joyful, and light in critique | important | full | `5.2 Shared Persona Layer` |  |
| PRD-088 | Structure Scoop as personal taste mini-review | important | full | `5.3 Contracts Per Surface` |  |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | full | `5.3 Contracts Per Surface`; `5.6 Conversation Summarization` |  |
| PRD-090 | Feed AI the right surface-specific context inputs | important | full | `5.3 Contracts Per Surface`; `9. Cross-Cutting Rules` |  |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | full | `10. Testing & Quality Strategy` |  |
| PRD-092 | Show person gallery, name, and bio | important | full | `4.4 Person`; `Person/features/ImageGallery`; `Phase 7` |  |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | full | `2.3 Person`; `Phase 7` |  |
| PRD-094 | Group filmography by year | important | full | `4.4 Person`; `Person/features/FilmographyByYear`; `Phase 7` |  |
| PRD-095 | Open Show Detail from selected credit | important | full | `Phase 7` says credit to Detail navigation |  |
| PRD-096 | Include font size and Search-on-launch settings | important | full | `2.1 Local-only`; `7. Settings`; `Phase 8` |  |
| PRD-097 | Support username, model, and API-key settings safely | important | full | `2.1 cloud_settings`; `7. Settings, Secrets & Export`; `Phase 8` |  |
| PRD-098 | Export saved shows and My Data as zip | critical | full | `4.5 Settings & Data`; `7. Settings, Secrets & Export`; `Phase 8` |  |
| PRD-099 | Encode export dates using ISO-8601 | important | full | `7. Settings, Secrets & Export` |  |

### 3. Coverage Scores

Overall score:

```
score = (86 full × 1.0 + 13 partial × 0.5) / 99 total × 100 = 93.4%
```

Critical:  (29 full × 1.0 + 1 partial × 0.5) / 30 critical_total × 100 = 98.3%  (29.5 of 30 critical requirements)
Important: (55 full × 1.0 + 12 partial × 0.5) / 67 important_total × 100 = 91.0%  (61 of 67 important requirements)
Detail:    (2 full × 1.0 + 0 partial × 0.5) / 2 detail_total × 100 = 100.0%  (2 of 2 detail requirements)
Overall:   93.4% (99 total requirements)

### 4. Top Gaps

- PRD-086 | `critical` | Enforce shared AI guardrails across all surfaces: This matters because the shared persona layer is the control point for spoiler safety, domain boundaries, honesty, and specificity; without a complete shared guardrail contract, Ask, Scoop, Explore Similar, and Alchemy can drift inconsistently.
- PRD-051 | `important` | Preserve Show Detail narrative section order: This matters because the detail page is not just a data dump; the PRD treats its sequence as the intended first-15-seconds experience, and the plan's ordering could produce a page that is functionally complete but emotionally off.
- PRD-033 | `important` | Sync libraries/settings consistently and merge duplicates: This matters because duplicate handling is a user-trust issue in a cross-device library; timestamp conflict resolution alone does not guarantee users will not see duplicate saved shows or divergent settings.
- PRD-054 | `important` | Place status/interest controls in toolbar: This matters because relationship controls are core repeat actions; leaving toolbar placement implicit can produce a detail page that is functional but less scannable and less aligned with the specified interaction model.
- PRD-064 | `important` | Keep primary actions early and page not overwhelming: This matters because the detail page has many sections; without an explicit busyness/clutter constraint, long-tail content can crowd out the primary relationship and discovery actions.

### 5. Coverage Narrative

#### Overall Posture

This is a strong plan with minor but real specification gaps. It covers the infrastructure baseline, persistence model, namespace/user isolation, core collection lifecycle, AI contracts, and major app screens with enough architectural detail to guide implementation. The missing strength is not broad feature omission; it is that several experience-defining behaviors are left as broad intent rather than acceptance-level contracts.

#### Strength Clusters

The plan is strongest in Benchmark Runtime & Isolation, Collection Data & Persistence, App Navigation & Discover Shell, Collection Home & Search, Person Detail, and Settings & Export. It gives concrete table design, API boundaries, merge functions, RLS/namespace behavior, test/reset tooling, and phase sequencing, which means most correctness requirements are directly grounded in implementation tasks.

#### Weakness Clusters

The partials cluster around user-experience fidelity and AI output quality rather than basic functionality. Show Detail has the most visible risk because the plan lists all components but does not fully preserve the supporting document's narrative order, toolbar placement, busyness constraints, and header/Scoop state nuance. AI discovery has a smaller cluster where the plan relies on prompt intent or manual quality review instead of explicit response-shape and guardrail acceptance criteria.

#### Risk Assessment

If executed as-is, the most likely failure mode is a product that works correctly in data and navigation terms but feels slightly flatter than the PRD intends. QA would probably notice first on Show Detail and Ask: sections may appear in a reasonable but not prescribed order, primary controls may not land in the intended toolbar treatment, Scoop may lack precise cached/empty/open state behavior, and Ask may be on-brand without consistently answering immediately or redirecting off-domain prompts.

#### Remediation Guidance

The remaining planning work is mostly acceptance criteria tightening. Add explicit UI state contracts for Show Detail header media fallback and Scoop states, pin the exact detail-page section order including genres/languages, place relationship controls in the toolbar, state the Ask direct-answer and domain-redirect rules as prompt/test criteria, require concept diversity across axes and ingredient-picking guidance, and add a duplicate-detection/merge rule to the sync plan. These are refinements to existing sections, not new architecture.
