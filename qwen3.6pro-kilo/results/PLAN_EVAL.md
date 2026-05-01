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
| PRD-001 | Use Next.js latest stable runtime | critical | full | `Architecture Summary` | |
| PRD-002 | Use Supabase official client libraries | critical | full | `Architecture Summary`; `2.1 Supabase Client` | |
| PRD-003 | Ship `.env.example` with required variables | critical | full | `1.2 Environment Variables` | |
| PRD-004 | Ignore `.env*` secrets except example | important | partial | `1.1 Repository Structure`; `1.2 Environment Variables` | The plan includes `.gitignore` and `.env.example` but never states the required `.env*` ignore rule or the `.env.example` exception. |
| PRD-005 | Configure build through env without code edits | critical | full | `1.2 Environment Variables`; `Architecture Summary` | |
| PRD-006 | Keep secrets out of repo and server-only | critical | partial | `1.2 Environment Variables` marks `SUPABASE_SERVICE_ROLE_KEY` as server-only | The plan does not explicitly cover repo secret hygiene and safe handling boundaries for all sensitive keys. |
| PRD-007 | Provide app, test, reset command scripts | critical | full | `1.4 Scripts` | |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | `1.1 Repository Structure` shows `supabase/migrations/` and `seed.sql` | |
| PRD-009 | Use one stable namespace per build | critical | full | `1.2 Environment Variables` (`NAMESPACE_ID`); `6.1 Namespace Isolation` | |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | `1.4 Scripts` (`npm run test:reset`); `6.1 Namespace Isolation` | |
| PRD-011 | Attach every user record to `user_id` | critical | full | `1.3 Database Schema` for `shows` and `cloud_settings`; `2.2 Identity Management` | |
| PRD-012 | Partition persisted data by namespace and user | critical | full | `1.3 Database Schema` indexes/RLS; `2.2 Identity Management` | |
| PRD-013 | Support documented dev auth injection, prod-gated | important | partial | `2.2 Identity Management` | The plan includes dev-only identity injection paths, but it does not explicitly plan the documentation of that mechanism. |
| PRD-014 | Real OAuth later needs no schema redesign | important | partial | `Architecture Summary` says auth is designed for future OAuth | The plan states intent but does not explain the schema and abstraction choices that keep OAuth migration free of redesign. |
| PRD-015 | Keep backend as persisted source of truth | critical | full | `6.3 Backend as Source of Truth` | |
| PRD-016 | Make client cache safe to discard | critical | full | `6.3 Backend as Source of Truth` | |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | partial | `Architecture Summary` uses hosted or local Supabase | The plan never explicitly states that Docker is optional or unnecessary for the supported benchmark path. |
| PRD-018 | Overlay saved user data on every show appearance | critical | full | `4.5 Display Rule` | |
| PRD-019 | Support visible statuses plus hidden `Next` | important | full | `1.3 Database Schema` includes `next`; `8. Open Questions / Deferred` | |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | full | `3.3 Show Detail > features/MyStatus` | |
| PRD-021 | Support free-form multi-tag personal tag library | important | full | `3.3 Show Detail > features/MyTags`; `3.1 FilterSidebar` | |
| PRD-022 | Define collection membership by assigned status | critical | full | `3.1 ShowLibrary` status-grouped library; `4.3 Removal` clears status to remove from collection | |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | full | `4.1 Saving Triggers` | |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | `4.2 Default Values` | |
| PRD-025 | Removing status deletes show and all My Data | critical | full | `4.3 Removal` | |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | full | `4.4 Re-adding` | |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | `1.3 Database Schema` timestamp columns; `4.4 Re-adding` | |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | partial | `4.4 Re-adding`; `4.7 AI Data Persistence` | The plan uses timestamps for conflict resolution and Scoop freshness but does not explicitly tie them to sorting behavior. |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | full | `3.3 Show Detail > features/AIScoop`; `4.7 AI Data Persistence` | |
| PRD-030 | Keep Ask and Alchemy state session-only | important | full | `4.7 AI Data Persistence` | |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | full | `4.8 AI Recommendations → Real Shows` | |
| PRD-032 | Show collection and rating tile indicators | important | full | `3.1 ShowLibrary > features/ShowTile` | |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | partial | `1.3 cloud_settings`; `4.4 Re-adding`; `6.2 Data Continuity` | Cross-device sync and duplicate detection and merge behavior are acknowledged only indirectly, not as a concrete implementation slice. |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | full | `6.2 Data Continuity` | |
| PRD-035 | Persist synced settings, local settings, UI state | important | full | `1.3 cloud_settings`; `6.4 Local Settings` | |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | partial | `2.3 External Catalog Integration`; `1.3 Database Schema` (`provider_data`) | The plan persists provider data, but it does not explicitly call out the transient-only treatment of credits, seasons, videos, and similar detail fetches. |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | full | `4.6 Merge Policy` | |
| PRD-038 | Provide filters panel and main screen destinations | important | full | `3.1 Collection Home Page`; `3.2 Find/Discover Hub Page`; `3.5 Settings Page` | |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | partial | `3.2 Find/Discover Hub Page` | The plan defines the Find surface itself but never plans a persistent primary-navigation shell that keeps it globally accessible. |
| PRD-040 | Keep Settings in persistent primary navigation | important | partial | `3.5 Settings Page` | The Settings page exists in the plan, but the persistent primary-navigation placement is not specified. |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | `3.2 Find/Discover Hub Page > features/ModeSwitcher` | |
| PRD-042 | Show only library items matching active filters | important | full | `3.1 ShowLibrary`; `hooks/useLibraryQuery.ts` | |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | `3.1 ShowLibrary` | |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | full | `3.1 FilterSidebar` | |
| PRD-045 | Render poster, title, and My Data badges | important | full | `3.1 ShowLibrary > features/ShowTile` | |
| PRD-046 | Provide empty-library and empty-filter states | detail | full | `3.1 ShowLibrary` empty states | |
| PRD-047 | Search by title or keywords | important | full | `3.2 SearchMode` | |
| PRD-048 | Use poster grid with collection markers | important | full | `3.2 SearchMode` | |
| PRD-049 | Auto-open Search when setting is enabled | detail | full | `3.2 SearchMode`; `6.4 Local Settings` (`autoSearch`) | |
| PRD-050 | Keep Search non-AI in tone | important | missing | none | The plan never calls out Search as a deliberately non-AI, straightforward catalog experience. |
| PRD-051 | Preserve Show Detail narrative section order | important | partial | `3.3 Show Detail Page` section list | The plan includes a section list, but its ordering diverges from the required narrative hierarchy for tags, overview and Scoop, Ask, and genres and languages. |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | full | `3.3 Show Detail > features/HeaderMedia` | |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | full | `3.3 Show Detail > features/CoreFacts` | |
| PRD-054 | Place status/interest controls in toolbar | important | partial | `3.3 Show Detail > features/MyStatus` | The plan names the controls but does not explicitly keep them in the toolbar rather than the scroll body. |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | `3.3 Show Detail > features/MyTags` | |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | `3.3 Show Detail > features/MyRating` | |
| PRD-057 | Show overview early for fast scanning | important | full | `3.3 Show Detail > features/Overview` | |
| PRD-058 | Scoop shows correct states and progressive feedback | important | full | `3.3 Show Detail > features/AIScoop` | |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | full | `3.3 Show Detail > features/AskAboutShow` | |
| PRD-060 | Include traditional recommendations strand | important | full | `3.3 Show Detail > features/TraditionalRecs` | |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | full | `3.3 Show Detail > features/ExploreSimilar` | |
| PRD-062 | Include streaming availability and person-linking credits | important | full | `3.3 Show Detail > features/StreamingAvailability`; `features/CastCrew` | |
| PRD-063 | Gate seasons to TV and financials to movies | important | full | `3.3 Show Detail > features/Seasons`; `features/BudgetRevenue` | |
| PRD-064 | Keep primary actions early and page not overwhelming | important | partial | `3.3 Show Detail Page` clusters key actions near the top | The plan does not explicitly address the anti-busyness principle or how the page avoids feeling overloaded. |
| PRD-065 | Provide conversational Ask chat interface | important | full | `3.2 AskMode > features/ChatInterface` | |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | partial | `5.1 Shared Rules`; `5.3 Ask` | The plan covers tone and spoiler safety, but it does not capture the "direct answer in the first few lines" quality bar. |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | `3.2 AskMode > features/MentionedShowsStrip` | |
| PRD-068 | Open Detail from mentions or Search fallback | important | partial | `3.2 AskMode`; `4.8 AI Recommendations → Real Shows` | Mention resolution exists conceptually, but the tap behavior from the mentioned-shows strip to Detail or Search fallback is not explicitly planned. |
| PRD-069 | Show six random starter prompts with refresh | important | full | `3.2 AskMode > features/StarterPrompts` | |
| PRD-070 | Summarize older turns while preserving voice | important | full | `2.4 AI Service Layer`; `5.6 Conversation Summarization` | |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | full | `3.2 AskMode` ("Ask About a Show" variant) | |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | partial | `3.2 AskMode > hooks/useMentionedShowsParser.ts`; `5.3 Ask` | The plan captures the `showList` string format but never specifies the required top-level `commentary` plus `showList` response object contract. |
| PRD-073 | Retry malformed mention output once, then fallback | important | full | `2.4 AI Service Layer`; `5.7 Guardrails & Fallbacks` | |
| PRD-074 | Redirect Ask back into TV/movie domain | important | full | `5.1 Shared Rules` | |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | partial | `3.2 AlchemyMode > features/ConceptCatalysts`; `3.3 Show Detail > features/ExploreSimilar` | The plan treats concepts as selectable AI outputs, but it never explicitly frames them as taste ingredients rather than genres. |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | full | `5.4 Concepts` | |
| PRD-077 | Order concepts by strongest aha and varied axes | important | partial | `5.4 Concepts` | The plan calls for diversity across axes, but it omits the strongest-first ordering rule. |
| PRD-078 | Require concept selection and guide ingredient picking | important | partial | `3.2 ConceptCatalysts`; `3.3 ExploreSimilar` | Selection is present, but the user guidance and empty-state nudges about choosing ingredients are missing. |
| PRD-079 | Return exactly five Explore Similar recommendations | important | full | `3.3 Show Detail > features/ExploreSimilar` | |
| PRD-080 | Support full Alchemy loop with chaining | important | full | `3.2 AlchemyMode`; `features/AlchemyChain` | |
| PRD-081 | Clear downstream results when inputs change | important | full | `3.2 AlchemyMode` backtracking rule; `hooks/useAlchemySession.ts` | |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | missing | none | The plan never distinguishes Alchemy's multi-show concept generation as requiring a larger option pool than single-show concept generation. |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | full | `5.5 Concept-Based Recommendations` | |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | partial | `Phase 5: Discovery quality validation` | The plan validates taste alignment generally, but it does not make "surprise without betrayal" an explicit recommendation quality target. |
| PRD-085 | Keep one consistent AI persona across surfaces | important | full | `5.1-5.5 AI Surface Contracts`; `9. Key Risk Areas` | |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | full | `5.1 Shared Rules` | |
| PRD-087 | Make AI warm, joyful, and light in critique | important | partial | `5.2 Scoop`; `5.3 Ask` | The plan implies a friendly voice, but it does not explicitly preserve the joy-forward and light-in-critique requirements as shared acceptance criteria. |
| PRD-088 | Structure Scoop as personal taste mini-review | important | full | `5.2 Scoop` | |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | full | `5.3 Ask` | |
| PRD-090 | Feed AI the right surface-specific context inputs | important | partial | `2.4 AI Service Layer`; `3.2 AskMode`; `3.3 AskAboutShow`; `3.3 ExploreSimilar` | The plan sets up the AI surfaces, but it never spells out the exact context bundle each prompt receives from library, My Data, show context, concepts, and chat history. |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | partial | `Phase 5: Discovery quality validation` | The plan mentions validation themes, but it does not adopt the scoring rubric thresholds or the non-negotiable integrity gate. |
| PRD-092 | Show person gallery, name, and bio | important | full | `3.4 Person Detail Page > features/PersonHeader` | |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | full | `3.4 Person Detail Page > features/PersonAnalytics` | |
| PRD-094 | Group filmography by year | important | full | `3.4 Person Detail Page > features/Filmography` | |
| PRD-095 | Open Show Detail from selected credit | important | full | `3.4 Person Detail Page > features/Filmography` | |
| PRD-096 | Include font size and Search-on-launch settings | important | full | `3.5 Settings Page > features/AppSettings` | |
| PRD-097 | Support username, model, and API-key settings safely | important | partial | `3.5 Settings Page > features/UserSettings`; `features/AISettings`; `features/IntegrationSettings` | The plan includes the settings surfaces, but it does not define safe storage and exposure boundaries for user-entered API keys. |
| PRD-098 | Export saved shows and My Data as zip | critical | full | `3.5 Settings Page > features/YourData`; `hooks/useDataExport.ts` | |
| PRD-099 | Encode export dates using ISO-8601 | important | full | `3.5 Settings Page > features/YourData` | |

## 3. Coverage Scores

score = (73 × 1.0 + 24 × 0.5) / 99 × 100 = 85.9%

Critical:  (28 × 1.0 + 2 × 0.5) / 30 × 100 = 96.7%  (29 of 30 critical requirements)
Important: (43 × 1.0 + 22 × 0.5) / 67 × 100 = 80.6%  (54 of 67 important requirements)
Detail:    (2 × 1.0 + 0 × 0.5) / 2 × 100 = 100.0%  (2 of 2 detail requirements)
Overall:   85.9% (99 total requirements)

## 4. Top Gaps

1. PRD-072 | `critical` | Emit `commentary` plus exact `showList` contract
The plan only captures the delimited `showList` string, so the Ask surface could ship with an incompatible response envelope and break the mentioned-shows UI contract.

2. PRD-006 | `critical` | Keep secrets out of repo and server-only
The plan names some secrets and one server-only key, but without explicit secret-handling rules it leaves room for unsafe key storage or accidental client exposure.

3. PRD-051 | `important` | Preserve Show Detail narrative section order
The detail page is one of the product-defining experiences, and reordering its sections changes how quickly users orient, save, and discover from a show.

4. PRD-082 | `important` | Generate shared multi-show concepts with larger option pool
Without a larger concept pool for Alchemy, multi-show blending is likely to feel shallow and repetitive, which weakens one of the product's signature discovery paths.

5. PRD-091 | `important` | Validate discovery with rubric and hard-fail integrity
If the plan lacks the explicit scoring gate, AI discovery quality can regress while still appearing "implemented," especially around hallucinated or weakly justified recommendations.

## 5. Coverage Narrative

#### Overall Posture

This is a structurally strong plan that covers most of the benchmark's critical mechanics and almost all of the major product surfaces. The shortfall is not missing whole features so much as missing some of the product-shaping behavioral contracts and acceptance bars that distinguish a faithful rebuild from a merely complete-looking implementation.

#### Strength Clusters

The plan is strongest in Benchmark Runtime & Isolation, Collection Data & Persistence, and the core page inventory across Collection Home, Ask, Person Detail, and Settings & Export. It also does a good job translating the major flows for Show Detail, Explore Similar, and Alchemy into concrete feature slices, hooks, and data responsibilities.

#### Weakness Clusters

The weaker coverage clusters around important-tier UX semantics and AI behavioral precision. The biggest concentration is in navigation shell details, the exact Show Detail narrative choreography, Search's non-AI positioning, concept-system nuance, and AI surface contracts and quality enforcement where the plan captures the existence of a feature but not the exact bar it must meet.

#### Risk Assessment

If this plan were executed as-is, the app would probably look broadly correct and satisfy many benchmark mechanics, but QA and stakeholders would start noticing that some signature experiences feel off. The first visible failures would likely be a Detail page that is functionally complete but sequenced differently than intended, Ask integrations that are brittle around the mentioned-shows contract, and AI discovery that works but is not consistently governed by the product's exact quality and persona rules.

#### Remediation Guidance

What remains is mostly planning precision, not a wholesale rewrite. The plan needs tighter behavioral specifications for AI response contracts, recommendation quality gates, Search's non-AI posture, shell and navigation persistence, and the Detail page's narrative layout. In other words, the remaining work is primarily missing acceptance criteria and product-level architectural decisions, with only a small amount of genuinely missing feature scope.
