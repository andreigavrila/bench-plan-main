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
| PRD-001 | Use Next.js latest stable runtime | critical | full | Phase 0.1: "Initialize Next.js project (latest stable)" |  |
| PRD-002 | Use Supabase official client libraries | critical | partial | Phase 1.2: "Supabase Client Layer" and client factories | The plan specifies Supabase clients but does not explicitly require the official Supabase client libraries. |
| PRD-003 | Ship `.env.example` with required variables | critical | full | Phase 0.2: "Create `.env.example` with all required variables" |  |
| PRD-004 | Ignore `.env*` secrets except example | important | full | Phase 0.2: "`.gitignore` excludes `.env*` except `.env.example`" |  |
| PRD-005 | Configure build through env without code edits | critical | full | Phase 0.2: typed environment access and env variable interface |  |
| PRD-006 | Keep secrets out of repo and server-only | critical | full | Phase 0.2: server-only keys gated behind server-side checks |  |
| PRD-007 | Provide app, test, reset command scripts | critical | full | Phase 0.5 scripts: `npm run dev`, `npm test`, `npm run test:reset` |  |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | Phase 0.3 migrations and Phase 0.5 `db:migrate` |  |
| PRD-009 | Use one stable namespace per build | critical | full | Phase 0.4: `NAMESPACE_ID` from env or generated per build |  |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | Phase 10.2: every query includes namespace and test reset is scoped |  |
| PRD-011 | Attach every user record to `user_id` | critical | full | Phase 0.3 tables include `user_id`; Phase 1.3 repositories scope by user |  |
| PRD-012 | Partition persisted data by namespace and user | critical | full | Phase 0.3 indexes/RLS and Phase 1.3 repository signatures |  |
| PRD-013 | Support documented dev auth injection, prod-gated | important | partial | Phase 0.4: dev mode reads `DEV_USER_ID` or `X-User-Id`, gated from production | The plan covers injection and production gating but does not include a documentation task for the dev auth mechanism. |
| PRD-014 | Real OAuth later needs no schema redesign | important | full | Phase 0.4: OAuth later requires auth wiring, not schema redesign |  |
| PRD-015 | Keep backend as persisted source of truth | critical | full | Executive Summary and Phase 1.3 Supabase repositories for persisted data |  |
| PRD-016 | Make client cache safe to discard | critical | full | Phase 10.4: "Client-side caching for catalog data (disposable, re-fetchable)" |  |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | full | Summary: "Benchmark-compliant infrastructure... no Docker requirement" |  |
| PRD-018 | Overlay saved user data on every show appearance | critical | full | Phase 10.1: saved data displayed everywhere shows appear |  |
| PRD-019 | Support visible statuses plus hidden `Next` | important | full | Phase 1.1 status types include `next`; Open Items defer first-class UI |  |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | full | Phase 1.5 auto-save matrix and Phase 6.2 MyRelationship |  |
| PRD-021 | Support free-form multi-tag personal tag library | important | full | Phase 2.2 `TagPicker` with autocomplete and Phase 4.1 tag filters |  |
| PRD-022 | Define collection membership by assigned status | critical | full | Phase 4.2: "In-collection indicator when `myStatus` exists" |  |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | full | Phase 1.5 saving trigger matrix |  |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | Phase 1.5 auto-save matrix |  |
| PRD-025 | Removing status deletes show and all My Data | critical | full | Phase 6.2: reselect status removes and clears all My Data |  |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | full | Phase 1.4 `mergeShow` preserves My fields and merges catalog fields |  |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | Phase 0.3 timestamp columns and Phase 10.1 timestamp tracking |  |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | full | Phase 10.1: timestamps used for sorting, conflict resolution, cache freshness |  |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | full | Phase 6.2 ScoopSection: 4-hour cache and saved-only persistence |  |
| PRD-030 | Keep Ask and Alchemy state session-only | important | partial | Phase 5.4: "Session-scoped: All Alchemy data cleared when leaving" | Alchemy is explicit, but Ask chat reset/leaving behavior is only implied by hook state and not specified as session-only. |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | full | Phase 9.3 catalog resolution flow |  |
| PRD-032 | Show collection and rating tile indicators | important | full | Phase 4.2: in-collection and user rating indicators |  |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | partial | Phase 1.4 merge logic and Phase 1.3 settings version conflict resolution | The plan covers conflict merging but does not specify duplicate item detection and transparent merge. |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | full | Phase 10.6: users never lose collection data due to updates |  |
| PRD-035 | Persist synced settings, local settings, UI state | important | full | Phase 1.1 types and Phase 8 settings/local UI persistence |  |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | full | Phase 0.3 `provider_data`; Phase 6.1 transient cast/crew/seasons/videos |  |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | full | Phase 1.4 `mergeShow` rules |  |
| PRD-038 | Provide filters panel and main screen destinations | important | full | Phase 3.2 main layout and Phase 3.3 navigation routes |  |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | full | Phase 3.2 top nav with Find/Discover entry |  |
| PRD-040 | Keep Settings in persistent primary navigation | important | full | Phase 3.2 top nav with Settings entry |  |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | Phase 5.1 FindHub mode switcher |  |
| PRD-042 | Show only library items matching active filters | important | full | Phase 4.1 `useCollection` applies active filter and media type |  |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | Phase 4.1 ordered status sections |  |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | full | Phase 1.6 filter system and Phase 4.1 FilterSidebar |  |
| PRD-045 | Render poster, title, and My Data badges | important | full | Phase 4.2 Show Tile Behavior |  |
| PRD-046 | Provide empty-library and empty-filter states | detail | full | Phase 4.1 CollectionEmptyState |  |
| PRD-047 | Search by title or keywords | important | full | Phase 5.2 debounced text search against catalog |  |
| PRD-048 | Use poster grid with collection markers | important | full | Phase 5.2 results grid with in-collection badge |  |
| PRD-049 | Auto-open Search when setting is enabled | detail | full | Phase 5.2 supports Search on Launch auto-open |  |
| PRD-050 | Keep Search non-AI in tone | important | partial | Phase 5.2 Search Mode uses catalog text search only | Search is separated from AI behavior, but the plan does not explicitly call out the non-AI tone requirement. |
| PRD-051 | Preserve Show Detail narrative section order | important | full | Phase 6.2: "Section Features (in narrative order)" |  |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | full | Phase 6.2 HeaderMedia with video playback and fallback |  |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | full | Phase 6.2 CoreFacts section |  |
| PRD-054 | Place status/interest controls in toolbar | important | partial | Phase 6.2 MyRelationship has status chips, rating, and tags | The plan includes the controls but places them in a MyRelationship section rather than explicitly in the toolbar. |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | Phase 6.2 tag add on unsaved auto-saves as later/interested |  |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | Phase 6.2 rating change on unsaved auto-saves as done |  |
| PRD-057 | Show overview early for fast scanning | important | full | Phase 6.2 OverviewSection follows early relationship controls |  |
| PRD-058 | Scoop shows correct states and progressive feedback | important | full | Phase 6.2 ScoopSection toggle states and streaming |  |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | full | Phase 6.2 AskAboutShow navigates with show context seeded |  |
| PRD-060 | Include traditional recommendations strand | important | full | Phase 6.2 RecommendationsStrand |  |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | full | Phase 6.2 ExploreSimilar three-step flow |  |
| PRD-062 | Include streaming availability and person-linking credits | important | full | Phase 6.2 StreamingProviders and CastCrew |  |
| PRD-063 | Gate seasons to TV and financials to movies | important | full | Phase 6.2 SeasonsSection and BudgetRevenue gating |  |
| PRD-064 | Keep primary actions early and page not overwhelming | important | full | Phase 6.2 narrative order clusters relationship, scoop, ask, and concepts before long-tail sections |  |
| PRD-065 | Provide conversational Ask chat interface | important | full | Phase 5.3 AskMode chat UI |  |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | full | Phase 9.1 Ask prompt: friendly dialogue, confident picks; shared rules spoiler-safe |  |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | Phase 5.3 Mentioned Shows strip |  |
| PRD-068 | Open Detail from mentions or Search fallback | important | full | Phase 5.3 resolved shows strip and unresolved fallback |  |
| PRD-069 | Show six random starter prompts with refresh | important | full | Phase 5.3 welcome view with 6 random starter prompts and refresh |  |
| PRD-070 | Summarize older turns while preserving voice | important | full | Phase 5.3 and Phase 9.4 conversation summarization |  |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | full | Phase 5.3 Ask About a Show variant |  |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | full | Phase 5.3 AI Contract with exact structured response |  |
| PRD-073 | Retry malformed mention output once, then fallback | important | full | Phase 9.2 `askParser.ts` parse failure handling |  |
| PRD-074 | Redirect Ask back into TV/movie domain | important | full | Phase 9.1 shared rules stay within TV/movies |  |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | partial | Phase 6.2 copy hints: "pick the ingredients you want more of" | The plan captures ingredient language but does not explicitly say concepts are not genres or plot categories. |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | full | Phase 9.1 `conceptPrompt.ts` output constraints |  |
| PRD-077 | Order concepts by strongest aha and varied axes | important | full | Phase 9.1 concept quality: diverse axes, ordered by strength |  |
| PRD-078 | Require concept selection and guide ingredient picking | important | full | Phase 5.4 and Phase 6.2 concept chip selection plus ingredient hint |  |
| PRD-079 | Return exactly five Explore Similar recommendations | important | full | Phase 6.2 Explore Similar generates 5 recommendations |  |
| PRD-080 | Support full Alchemy loop with chaining | important | full | Phase 5.4 step flow and "More Alchemy!" chaining |  |
| PRD-081 | Clear downstream results when inputs change | important | full | Phase 5.4 backtracking and concept-change clearing |  |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | full | Phase 9.1 multi-show variant returns shared concepts and larger pool |  |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | full | Phase 9.1 recommendation prompt references selected concepts |  |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | partial | Phase 9.1 recommendations use selected concepts, library, and reasons | The plan covers taste alignment but not the "surprising but defensible" quality bar. |
| PRD-085 | Keep one consistent AI persona across surfaces | important | full | Phase 9.1 "All prompts enforce shared rules" and Summary |  |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | full | Phase 9.1 shared rules: TV/movies, spoiler-safe, honest, specific |  |
| PRD-087 | Make AI warm, joyful, and light in critique | important | partial | Phase 9.1 prompt tones include friendly dialogue and gossipy/vivid Scoop | The plan gestures at friendly AI but does not explicitly encode warmth, joy-forward behavior, or light critique as non-negotiable voice pillars. |
| PRD-088 | Structure Scoop as personal taste mini-review | important | full | Phase 6.2 and Phase 9.1 Scoop contract |  |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | full | Phase 9.1 Ask tone: "friendly dialogue, not essay" |  |
| PRD-090 | Feed AI the right surface-specific context inputs | important | full | Phase 9.1 prompt inputs for Scoop, Ask, Ask About Show, concepts, recs |  |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | partial | Risk Mitigation: "AI personality drift" mitigated by golden set validation | The plan mentions validation but not the scoring rubric or non-negotiable real-show integrity hard fail. |
| PRD-092 | Show person gallery, name, and bio | important | full | Phase 7.1 PersonHeader |  |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | full | Phase 7.1 PersonAnalytics charts |  |
| PRD-094 | Group filmography by year | important | full | Phase 7.1 Filmography |  |
| PRD-095 | Open Show Detail from selected credit | important | full | Phase 7.1 credit click navigates to Show Detail |  |
| PRD-096 | Include font size and Search-on-launch settings | important | full | Phase 8.1 AppSettings |  |
| PRD-097 | Support username, model, and API-key settings safely | important | full | Phase 8.1 UserSettings, AISettings, IntegrationSettings |  |
| PRD-098 | Export saved shows and My Data as zip | critical | full | Phase 8.1 DataExport server action packages JSON into `.zip` |  |
| PRD-099 | Encode export dates using ISO-8601 | important | full | Phase 8.1 DataExport serializes JSON with ISO-8601 dates |  |

### 3. Coverage Scores

```
score = (full_count × 1.0 + partial_count × 0.5) / total_count × 100
```

Critical:  (29 × 1.0 + 1 × 0.5) / 30 × 100 = 98.3%  (29.5 of 30 critical requirements)
Important: (58 × 1.0 + 9 × 0.5) / 67 × 100 = 93.3%  (62.5 of 67 important requirements)
Detail:    (2 × 1.0 + 0 × 0.5) / 2 × 100 = 100.0%  (2.0 of 2 detail requirements)
Overall:   94.9% (99 total requirements)

### 4. Top Gaps

1. PRD-002 (`critical`) - Use Supabase official client libraries
   The plan is clearly Supabase-based, but omitting the official-library constraint leaves room for a custom or indirect integration that could miss benchmark expectations around supported clients and auth behavior.

2. PRD-013 (`important`) - Support documented dev auth injection, prod-gated
   The mechanism and production gate are planned, but lack of explicit documentation could make benchmark setup ambiguous for another agent or evaluator running the project.

3. PRD-033 (`important`) - Sync libraries/settings consistently and merge duplicates
   The plan covers timestamp/version conflict resolution but not duplicate detection and transparent merge, so sync could still produce repeated library entries or inconsistent saved shows.

4. PRD-054 (`important`) - Place status/interest controls in toolbar
   The controls exist, but if implemented as a normal body section instead of toolbar actions, the detail page loses the intended frictionless relationship-update behavior.

5. PRD-091 (`important`) - Validate discovery with rubric and hard-fail integrity
   The plan mentions golden set validation but does not bind implementation to the rubric or the real-show integrity hard fail, making AI quality regression harder to catch.

### 5. Coverage Narrative

#### Overall Posture

This is a strong, structurally complete plan with mostly minor-to-moderate gaps. It covers the main product flows, persistence model, benchmark isolation rules, AI surfaces, and user-facing pages in concrete implementation phases. The remaining issues are less about missing whole features and more about exact behavioral contracts that the PRD treats as important product safeguards.

#### Strength Clusters

The plan is strongest in Benchmark Runtime & Isolation, Collection Data & Persistence, Ask Chat, Person Detail, and Settings & Export. It gives concrete tables, repositories, routes, scripts, auto-save rules, timestamp fields, AI parsing contracts, and export behavior. Show Detail is also well covered, especially the narrative order, Scoop behavior, Explore Similar flow, and media/person-related sections.

#### Weakness Clusters

The partial items cluster around exactness rather than breadth. AI quality requirements are planned at a high level but sometimes miss the PRD's sharper wording around concepts as non-genre ingredients, surprise-without-betrayal, warm critique, and rubric-based validation. A smaller cluster appears in operational precision: official Supabase libraries, documented dev auth, duplicate merge handling, and toolbar placement.

#### Risk Assessment

If executed as-is, the most likely failure mode is a functionally complete app whose details drift from the benchmark's intended feel and repeatability. QA would probably notice that the core flows exist, but AI recommendations may not be consistently validated against the discovery quality bar, and a few UX or sync details could feel subtly off compared with the PRD.

#### Remediation Guidance

The plan needs targeted specification tightening, not a new architecture. Add explicit acceptance criteria for AI quality and concept semantics, document the benchmark identity-injection path, require official Supabase client libraries, define duplicate merge behavior, and pin status/interest controls to the detail toolbar. These additions would close the main gaps without changing the phase structure.
