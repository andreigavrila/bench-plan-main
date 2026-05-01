### 1. Requirements Extraction

#### Pass 1: Identify Functional Areas

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

#### Pass 2: Extract Requirements Within Each Area

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
| PRD-001 | Use Next.js latest stable runtime | critical | full | Section 1.1 Tech Stack |  |
| PRD-002 | Use Supabase official client libraries | critical | full | Section 1.1 Tech Stack |  |
| PRD-003 | Ship `.env.example` with required variables | critical | full | Section 8.1 `.env.example` |  |
| PRD-004 | Ignore `.env*` secrets except example | important | full | Section 8.2 `.gitignore` |  |
| PRD-005 | Configure build through env without code edits | critical | full | Sections 8.1-8.3 Environment & Configuration |  |
| PRD-006 | Keep secrets out of repo and server-only | critical | full | Section 2.2 RLS Policies; Section 8.2 `.gitignore` |  |
| PRD-007 | Provide app, test, reset command scripts | critical | full | Section 8.3 Scripts |  |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | Section 9 Database Migrations |  |
| PRD-009 | Use one stable namespace per build | critical | full | Section 3.1 Namespace Isolation |  |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | Section 3.1 Namespace Isolation; Section 10.4 Destructive Testing |  |
| PRD-011 | Attach every user record to `user_id` | critical | full | Section 2.1 `shows`; Section 3.2 User Identity |  |
| PRD-012 | Partition persisted data by namespace and user | critical | full | Section 3.3 Effective Partition |  |
| PRD-013 | Support documented dev auth injection, prod-gated | important | full | Section 3.2 User Identity |  |
| PRD-014 | Real OAuth later needs no schema redesign | important | full | Section 3.2 "Schema designed for future OAuth migration without redesign" |  |
| PRD-015 | Keep backend as persisted source of truth | critical | full | Section 14.1 Key Design Decisions |  |
| PRD-016 | Make client cache safe to discard | critical | full | Section 14.1 Key Design Decisions |  |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | missing | none | The plan never states that Docker is optional or that hosted persistence is the primary cloud-agent path. |
| PRD-018 | Overlay saved user data on every show appearance | critical | full | Section 2.1 `shows`; Section 14.2 User's version takes precedence |  |
| PRD-019 | Support visible statuses plus hidden `Next` | important | full | Section 2.1 `my_status`; Section 13 Open Questions / Deferred |  |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | partial | Section 5.1 Collection Home grouping; Section 7.2 Default Values When Saving | The plan models Later plus interest, but it never explicitly states that choosing Interested or Excited in the status UI writes `Later` plus the paired interest value. |
| PRD-021 | Support free-form multi-tag personal tag library | important | full | Section 2.1 `my_tags`; Section 5.2 Filters |  |
| PRD-022 | Define collection membership by assigned status | critical | full | Section 7.1 Collection Membership |  |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | full | Section 5.6 Saving Triggers |  |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | Section 7.2 Default Values When Saving |  |
| PRD-025 | Removing status deletes show and all My Data | critical | full | Section 5.6 Removing from Collection |  |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | full | Section 7.3 Re-adding Same Show |  |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | Section 2.1 `shows` timestamp columns |  |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | partial | Section 7.3 Re-adding Same Show; Section 7.5 Data Sync & Integrity; Section 6.4 AI Data Persistence | The plan uses timestamps for conflict resolution and freshness, but it does not describe any sorting behavior that depends on them. |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | full | Section 5.6 AI Scoop; Section 6.4 AI Data Persistence |  |
| PRD-030 | Keep Ask and Alchemy state session-only | important | full | Section 6.4 AI Data Persistence |  |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | full | Section 5.5 Recommendations; Section 6.6 Guardrails |  |
| PRD-032 | Show collection and rating tile indicators | important | full | Section 7.4 Tile Indicators; Section 5.1 Collection Home |  |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | full | Section 7.5 Data Sync & Integrity |  |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | full | Section 7.6 Data Continuity Across Versions; Section 9.1 Migration Strategy |  |
| PRD-035 | Persist synced settings, local settings, UI state | important | full | Section 2.1 `cloud_settings`, `local_settings`, `ui_state` |  |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | partial | Section 2.1 `provider_data`; Section 4.2 Catalog -> Show Mapping | The plan preserves provider IDs, but it never explicitly states that credits, seasons, videos, recommendations, and other detail payloads remain transient rather than persisted. |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | full | Section 4.3 Merge Policy |  |
| PRD-038 | Provide filters panel and main screen destinations | important | full | Section 1.2 Project Structure; Section 5.2 Filters |  |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | partial | Section 1.2 Project Structure shows `find/` under `(main)` | The plan defines the route, but it never commits to Find/Discover being a persistent primary-navigation entry point. |
| PRD-040 | Keep Settings in persistent primary navigation | important | partial | Section 1.2 Project Structure shows `settings/` under `(main)` | The plan defines the route, but it never commits to Settings being a persistent primary-navigation entry point. |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | Section 1.2 `find/page.tsx` mode switcher; Sections 5.3-5.5 |  |
| PRD-042 | Show only library items matching active filters | important | full | Section 5.1 "Fetch shows filtered by `(namespace_id, user_id)` and active filter" |  |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | Section 5.1 Collection Home grouping |  |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | full | Section 5.2 Filters |  |
| PRD-045 | Render poster, title, and My Data badges | important | full | Section 5.1 "Tiles show: poster, title, My Data badges" |  |
| PRD-046 | Provide empty-library and empty-filter states | detail | full | Section 5.1 Empty states |  |
| PRD-047 | Search by title or keywords | important | full | Section 5.3 "Text input -> catalog API search" |  |
| PRD-048 | Use poster grid with collection markers | important | full | Section 5.3 "Results in poster grid"; "In-collection items marked with badge" |  |
| PRD-049 | Auto-open Search when setting is enabled | detail | full | Section 5.3 "Search on Launch"; Section 5.8 App settings |  |
| PRD-050 | Keep Search non-AI in tone | important | full | Section 5.3 Search uses catalog API search only |  |
| PRD-051 | Preserve Show Detail narrative section order | important | partial | Section 5.6 Show Detail section list | The plan covers most detail-page sections, but the order does not preserve the required narrative hierarchy and it omits the Ask-about-this-show CTA placement. |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | full | Section 5.6 "Header media: backdrops/posters/logos/carousel (trailers if available)" |  |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | full | Section 5.6 items 2-3 |  |
| PRD-054 | Place status/interest controls in toolbar | important | partial | Section 5.6 "My Status + Interest: status chips" | The plan defines the controls, but it never specifies the toolbar placement required by the detail-page UX spec. |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | Section 5.6 "adding tag to unsaved show -> auto-save as Later + Interested" |  |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | Section 5.6 "rating unsaved show -> auto-save as Done" |  |
| PRD-057 | Show overview early for fast scanning | important | partial | Section 5.6 puts Overview at item 6 | The overview is present, but the plan places it after rating, status, and tags instead of clearly in the first-scan portion of the page. |
| PRD-058 | Scoop shows correct states and progressive feedback | important | partial | Section 5.6 AI Scoop; Section 6.4 AI Data Persistence | The plan covers streaming and freshness, but it does not spell out the required no-scoop, cached-scoop, and open-state feedback contract. |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | full | Section 5.4 "Ask About a Show" variant |  |
| PRD-060 | Include traditional recommendations strand | important | full | Section 5.6 "Traditional recommendations" |  |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | full | Section 5.6 "Get Concepts -> select concepts -> Explore Shows" |  |
| PRD-062 | Include streaming availability and person-linking credits | important | full | Section 5.6 "Streaming availability"; "Cast & Crew -> Person Detail" |  |
| PRD-063 | Gate seasons to TV and financials to movies | important | full | Section 5.6 "Seasons (TV only)"; "Budget vs Revenue (movies when available)" |  |
| PRD-064 | Keep primary actions early and page not overwhelming | important | partial | Section 5.6 Show Detail section list | The plan enumerates the sections, but it never describes the anti-overwhelm strategy of clustering primary actions early and pushing long-tail information down-page. |
| PRD-065 | Provide conversational Ask chat interface | important | full | Section 5.4 Ask (AI Chat) |  |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | partial | Section 6.2 AI Personality; Section 6.3 Ask row | The plan defines tone and output length, but it does not capture the requirement that Ask answers get to the recommendation quickly and make confident picks early. |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | Section 5.4 "mentioned shows horizontal strip" |  |
| PRD-068 | Open Detail from mentions or Search fallback | important | full | Section 5.4 "Show Detail (or Search handoff if mapping fails)" |  |
| PRD-069 | Show six random starter prompts with refresh | important | full | Section 5.4 "Welcome view with 6 random starter prompts (refreshable)" |  |
| PRD-070 | Summarize older turns while preserving voice | important | full | Section 6.5 Conversation Summarization |  |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | full | Section 5.4 "seeds conversation with show context" |  |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | full | Section 5.4 structured output contract |  |
| PRD-073 | Retry malformed mention output once, then fallback | important | full | Section 6.6 Guardrails |  |
| PRD-074 | Redirect Ask back into TV/movie domain | important | partial | Section 6.2 AI Personality says "TV/movie nerd friend" | The plan implies domain focus, but it does not define the required Ask behavior for redirecting out-of-domain requests back to TV and movies. |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | partial | Section 5.5 "AI extracts shared concepts"; Section 6.3 Concepts row | The plan supports concept extraction, but it never explicitly frames concepts as taste ingredients distinct from genres. |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | partial | Section 5.5 "Concepts: bullet list, 1-3 words, evocative, no explanation" | The format is covered, but the plan never explicitly bans generic placeholder concepts. |
| PRD-077 | Order concepts by strongest aha and varied axes | important | missing | none | The plan never specifies concept ordering by strongest insight first or coverage across different axes such as structure, vibe, emotion, and craft. |
| PRD-078 | Require concept selection and guide ingredient picking | important | partial | Section 5.5 "User selects 1-8 concepts" | The selection step exists, but the plan omits the UX guidance that should frame concepts as ingredients the user wants more of. |
| PRD-079 | Return exactly five Explore Similar recommendations | important | full | Section 6.3 Recommendations count "5 (Explore) / 6 (Alchemy)" |  |
| PRD-080 | Support full Alchemy loop with chaining | important | full | Section 5.5 flow includes "More Alchemy!" |  |
| PRD-081 | Clear downstream results when inputs change | important | full | Section 5.5 "changing shows clears concepts/results" |  |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | missing | none | The plan supports multi-show concepts, but it never plans for a larger concept pool in Alchemy than in the single-show flow. |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | partial | Section 5.5 "AI returns 6 recommendations with reasons"; Section 11.1 Taste Alignment | The plan requires reasons, but it does not say those reasons must explicitly name the selected concepts they are grounded in. |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | full | Section 11.1 Surprise Without Betrayal; Taste Alignment |  |
| PRD-085 | Keep one consistent AI persona across surfaces | important | full | Section 6.2 "Consistent persona across all surfaces" |  |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | partial | Section 6.2 AI Personality; Section 6.6 Guardrails | The plan covers some AI rules, but it never consolidates the full shared guardrail set across all surfaces, especially domain redirection and shared honesty/specificity constraints. |
| PRD-087 | Make AI warm, joyful, and light in critique | important | full | Section 6.2 AI Personality |  |
| PRD-088 | Structure Scoop as personal taste mini-review | important | full | Section 6.3 Scoop output "Structured mini blog post" |  |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | full | Section 6.2 "Short by default"; Section 6.3 Ask output |  |
| PRD-090 | Feed AI the right surface-specific context inputs | important | partial | Section 14.3 Taste-aware AI; Section 5.4 Ask About a Show | The plan mentions key context inputs, but it does not define a clear surface-by-surface context contract for Scoop, Ask, Explore Similar, and Alchemy. |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | full | Section 11 Discovery Quality Bar |  |
| PRD-092 | Show person gallery, name, and bio | important | full | Section 5.7 Person Detail |  |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | full | Section 5.7 analytics charts |  |
| PRD-094 | Group filmography by year | important | full | Section 5.7 "Filmography grouped by year" |  |
| PRD-095 | Open Show Detail from selected credit | important | full | Section 5.7 "Selecting credit -> navigate to Show Detail" |  |
| PRD-096 | Include font size and Search-on-launch settings | important | full | Section 5.8 App settings |  |
| PRD-097 | Support username, model, and API-key settings safely | important | partial | Section 5.8 Settings; Section 2.1 `cloud_settings` | The plan includes the fields, but it does not explain how user-entered API keys are handled safely or optionally synced without leaking into the repo. |
| PRD-098 | Export saved shows and My Data as zip | critical | full | Section 5.8 "Export My Data -> `.zip` with JSON backup" |  |
| PRD-099 | Encode export dates using ISO-8601 | important | full | Section 5.8 "JSON backup (ISO-8601 dates)" |  |

### 3. Coverage Scores

Overall score:

`score = (77 x 1.0 + 19 x 0.5) / 99 x 100 = 87.37%`

Critical:  (28 x 1.0 + 2 x 0.5) / 30 x 100 = 96.67%  (29.0 of 30 critical requirements)
Important: (47 x 1.0 + 17 x 0.5) / 67 x 100 = 82.84%  (55.5 of 67 important requirements)
Detail:    (2 x 1.0 + 0 x 0.5) / 2 x 100 = 100.00%  (2.0 of 2 detail requirements)
Overall:   (77 x 1.0 + 19 x 0.5) / 99 x 100 = 87.37%  (86.5 of 99 total requirements)

### 4. Top Gaps

1. PRD-086 | `critical` | Enforce shared AI guardrails across all surfaces
Without an explicit cross-surface AI contract, the build can ship feature-complete AI surfaces that drift in domain boundaries, honesty, spoiler handling, and recommendation integrity.

2. PRD-020 | `critical` | Map Interested/Excited chips to Later interest
If this mapping is not made explicit, save semantics, home grouping, and filter behavior can diverge even though the UI appears to support the right chips.

3. PRD-017 | `important` | Avoid Docker requirement for cloud-agent compatibility
This is a benchmark execution constraint, not just an implementation preference; omitting it leaves a real risk that the plan produces a build path the benchmark runner cannot execute reliably.

4. PRD-051 | `important` | Preserve Show Detail narrative section order
The detail page is the product's core decision surface, so getting the section choreography wrong weakens orientation, delays discovery affordances, and changes how the app feels in first use.

5. PRD-077 | `important` | Order concepts by strongest aha and varied axes
Without explicit ordering and diversity rules, concept generation can become generic or repetitive, which directly degrades Explore Similar and Alchemy recommendation quality.

### 5. Coverage Narrative

#### Overall Posture

This is a strong, structurally sound plan with high coverage across the benchmark denominator, but it is not fully specification-tight. The architecture, persistence model, collection behaviors, and most feature flows are well covered; the remaining issues are concentrated in AI behavioral contracts, detail-page choreography, and one benchmark-runtime portability requirement.

#### Strength Clusters

The plan is strongest in Benchmark Runtime & Isolation, Collection Data & Persistence, Collection Home & Search, Person Detail, and Settings & Export. It gives concrete schema design, isolation rules, save/remove behaviors, export behavior, route structure, and testing coverage, and it translates most of the PRD's core collection and discovery flows into explicit implementation sections.

#### Weakness Clusters

The gaps are not random. They cluster around experience-shaping requirements that live between product behavior and implementation detail: persistent navigation commitments, the precise narrative order of Show Detail, and the AI quality layer. Within AI, the weaker spots are shared guardrails, surface-specific context contracts, and the concept-system quality rules that keep Explore Similar and Alchemy from collapsing into generic recommendation logic.

#### Risk Assessment

If this plan were executed as-is, the most likely outcome is a feature-rich app that works on the happy path but misses part of the intended product feel. QA would likely notice first that the Detail page does not read in the prescribed rhythm and that AI outputs are functionally present yet underspecified in ways that could produce off-domain, insufficiently constrained, or overly generic discovery behavior. In benchmark execution, a separate failure mode is that runtime assumptions around Docker/cloud-agent compatibility remain unstated.

#### Remediation Guidance

The remaining planning work is mostly about adding explicit behavioral contracts, not inventing new subsystems. The plan needs tighter acceptance criteria for runtime portability, persistent navigation, detail-page section placement, toolbar placement for relationship controls, and the AI contract matrix for Ask, Scoop, Explore Similar, and Alchemy. For the concept system specifically, it needs missing quality rules around ingredient framing, option-pool sizing, ordering, and reason-to-concept traceability so recommendation quality is specified rather than implied.
