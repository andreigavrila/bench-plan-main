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
| PRD-001 | Use Next.js latest stable runtime | critical | partial | `1. Architecture Overview > "Next.js 14+ (App Router)"` | The plan picks Next.js but does not commit to the latest stable release required by the rider. |
| PRD-002 | Use Supabase official client libraries | critical | partial | `1. Architecture Overview > "Persistence: Supabase"` and `3.2 Namespace Isolation > "src/lib/supabase.ts"` | It chooses Supabase but never explicitly calls for the official Supabase client libraries. |
| PRD-003 | Ship `.env.example` with required variables | critical | full | `8. Environment Configuration > Required Variables` |  |
| PRD-004 | Ignore `.env*` secrets except example | important | missing | none | `.gitignore` handling for `.env*` files is not planned. |
| PRD-005 | Configure build through env without code edits | critical | full | `8. Environment Configuration > Required Variables` and `14. Success Criteria Checklist` |  |
| PRD-006 | Keep secrets out of repo and server-only | critical | partial | `8. Environment Configuration > "SUPABASE_SERVICE_ROLE_KEY=... # Server only"` | Server-only handling is noted for the service key, but the plan does not explicitly prohibit committing secrets or define client/server boundaries for all credentials. |
| PRD-007 | Provide app, test, reset command scripts | critical | full | `8. Environment Configuration > Scripts` |  |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | `7. Implementation Phases > Phase 1` and `8. Environment Configuration > "db:migrate"` |  |
| PRD-009 | Use one stable namespace per build | critical | full | `3.2 Namespace Isolation > "NAMESPACE_ID environment variable (set per build/run)"` |  |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | `3.2 Namespace Isolation` and `4. API Routes > "POST /api/test/reset"` |  |
| PRD-011 | Attach every user record to `user_id` | critical | full | `2. Database Schema > shows.user_id` and `cloud_settings.user_id` |  |
| PRD-012 | Partition persisted data by namespace and user | critical | full | `3.2 Namespace Isolation > "Every query is scoped to (user_id, namespace_id)"` |  |
| PRD-013 | Support documented dev auth injection, prod-gated | important | partial | `3.1 Authentication & Identity` | The dev injection mechanism is planned, but the production gating or disablement of that path is not specified. |
| PRD-014 | Real OAuth later needs no schema redesign | important | full | `3.1 Authentication & Identity > Production Path` and `12. Migration Path > "No schema changes required"` |  |
| PRD-015 | Keep backend as persisted source of truth | critical | full | `2. Database Schema` and `4. API Routes` |  |
| PRD-016 | Make client cache safe to discard | critical | partial | `6. Data Flow & State Management > Server State` and `Client State` | The plan uses server state plus client caches, but it never explicitly states that clearing local client state is safe and non-destructive. |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | full | `11. Deployment & DevOps > Local Development` and `Cloud Agent (Benchmark)` |  |
| PRD-018 | Overlay saved user data on every show appearance | critical | partial | `2. Database Schema > shows` and `6. Data Flow & State Management > Merge Logic` | The data model preserves user fields, but the plan never makes the global display rule explicit for search, recommendations, mentions, and every other show surface. |
| PRD-019 | Support visible statuses plus hidden `Next` | important | partial | `2. Database Schema > shows.my_status` and `3.7 Status/Interest Controls` | Visible statuses are covered, but the hidden `Next` status is absent from the data model and plan. |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | partial | `2. Database Schema > shows.my_interest` and `14. Success Criteria Checklist > "Interest levels: Interested, Excited (for Later)"` | The plan defines interest values but never explicitly maps the Interested and Excited chips to `Later` plus an interest value. |
| PRD-021 | Support free-form multi-tag personal tag library | important | full | `2. Database Schema > shows.my_tags` and `3.3 Collection Home > Filter sidebar` |  |
| PRD-022 | Define collection membership by assigned status | critical | partial | `9. Key Business Rules Implementation > Auto-Save Triggers` and `Status Removal Flow` | Status drives save and remove behavior, but the plan does not explicitly define collection membership as "has a status." |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | partial | `9. Key Business Rules Implementation > Auto-Save Triggers` | Status, rating, and tagging saves are covered, but saving from interest-chip selection is not explicitly planned. |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | `9. Key Business Rules Implementation > Auto-Save Triggers` |  |
| PRD-025 | Removing status deletes show and all My Data | critical | full | `9. Key Business Rules Implementation > Status Removal Flow` |  |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | missing | none | The plan never specifies the re-add flow that preserves prior My Data while refreshing catalog fields. |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | `2. Database Schema > per-field *_updated_at columns` |  |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | partial | `2. Database Schema > per-field timestamps` and `6. Data Flow & State Management > Merge Logic` | Freshness and conflict resolution are covered, but timestamp-driven sorting behavior is not planned. |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | full | `3.7 Show Detail > AI Scoop` and `9. Key Business Rules Implementation > AI Scoop Freshness` |  |
| PRD-030 | Keep Ask and Alchemy state session-only | important | full | `3.5 Ask (AI Chat) > "Session-only history"` and `6. Data Flow & State Management > Client State` |  |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | full | `3.6 Alchemy > Recommendation contract`, `4. API Routes > /api/ai/explore-similar`, and `13. Risk Mitigation > "Resolve to real catalog items; fallback to Search"` |  |
| PRD-032 | Show collection and rating tile indicators | important | partial | `3.4 Search > "In-collection badges"` and `3.3 Collection Home > ShowTile` | The plan covers collection markers and generic badges, but it does not explicitly require rating indicators on tiles. |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | partial | `2. Database Schema > cloud_settings.version` and `6. Data Flow & State Management > Merge Logic` | It covers sync fields and timestamp merges, but duplicate detection and transparent merge behavior are not called out. |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | full | `12. Migration Path > Schema Evolution` |  |
| PRD-035 | Persist synced settings, local settings, UI state | important | partial | `2. Database Schema > cloud_settings`, `6. Data Flow & State Management > Client State`, and `3.9 Settings` | Synced settings and some local settings are planned, but persisted UI state like last filter and removal-confirmation preferences is missing. |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | partial | `2. Database Schema > provider_data` and `4. API Routes > "GET /api/shows/[id] - Get show with transient data"` | Provider IDs are persisted, but the boundary between persisted provider IDs and transient detail-only fields is not fully specified. |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | full | `6. Data Flow & State Management > Merge Logic` |  |
| PRD-038 | Provide filters panel and main screen destinations | important | full | `3.3 Collection Home > Filter sidebar` and routes in `3.3-3.9` |  |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | partial | `3.4 Search > Route /find` and `pages/Find/` | The Find surface exists, but the plan does not explicitly place it in persistent primary navigation. |
| PRD-040 | Keep Settings in persistent primary navigation | important | partial | `3.9 Settings > Route /settings` | The Settings screen exists, but persistent primary-navigation placement is not specified. |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | `3.4 Search`, `3.5 Ask`, and `3.6 Alchemy` |  |
| PRD-042 | Show only library items matching active filters | important | full | `3.3 Collection Home > Filter sidebar` |  |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | `3.3 Collection Home > "Status-grouped sections: Active -> Excited -> Interested -> Other"` |  |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | full | `3.3 Collection Home > "Filter sidebar (All Shows, tags, genres, decades, scores)"` and media-type toggle |  |
| PRD-045 | Render poster, title, and My Data badges | important | partial | `3.3 Collection Home > ShowTile` | The plan implies tiles, but it never explicitly says home tiles must show poster, title, and My Data badges together. |
| PRD-046 | Provide empty-library and empty-filter states | detail | full | `3.3 Collection Home > "Empty states with Search/Ask prompts"` |  |
| PRD-047 | Search by title or keywords | important | full | `3.4 Search > "Text search via catalog API"` |  |
| PRD-048 | Use poster grid with collection markers | important | full | `3.4 Search > "Poster grid results"` and `"In-collection badges"` |  |
| PRD-049 | Auto-open Search when setting is enabled | detail | full | `3.4 Search > "Search on Launch" setting` |  |
| PRD-050 | Keep Search non-AI in tone | important | missing | none | The plan never distinguishes Search as a deliberately non-AI-toned surface. |
| PRD-051 | Preserve Show Detail narrative section order | important | full | `3.7 Show Detail > Sections (top to bottom)` |  |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | partial | `3.7 Show Detail > "Header media carousel (backdrops/posters/logos/trailers)"` | The motion-rich header is planned, but graceful fallback behavior when motion or media is missing is not described. |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | full | `3.7 Show Detail > "Core facts (year, runtime/seasons) + community score"` |  |
| PRD-054 | Place status/interest controls in toolbar | important | full | `3.7 Show Detail > "Status/Interest Controls"` and `"Toolbar chips"` |  |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | `3.7 Show Detail > Auto-save rules` and `9. Key Business Rules Implementation > Auto-Save Triggers` |  |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | `3.7 Show Detail > Auto-save rules` and `9. Key Business Rules Implementation > Auto-Save Triggers` |  |
| PRD-057 | Show overview early for fast scanning | important | full | `3.7 Show Detail > "Overview + AI Scoop toggle/stream"` |  |
| PRD-058 | Scoop shows correct states and progressive feedback | important | partial | `3.7 Show Detail > AI Scoop` and `9. Key Business Rules Implementation > AI Scoop Freshness` | Streaming and caching are planned, but the state-specific UX copy and feedback contract are not fully spelled out. |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | full | `3.5 Ask > "Ask about this show" variant (seeded context from Detail)` and `3.7 Show Detail > CTA` |  |
| PRD-060 | Include traditional recommendations strand | important | full | `3.7 Show Detail > "Recommendations strand (similar shows)"` |  |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | partial | `3.7 Show Detail > "Explore Similar (concepts -> recs)"` | Explore Similar is present, but the CTA-first `Get Concepts -> select -> Explore Shows` interaction contract is only implied. |
| PRD-062 | Include streaming availability and person-linking credits | important | full | `3.7 Show Detail > "Streaming providers"` and `"Cast & Crew strands -> Person Detail"` |  |
| PRD-063 | Gate seasons to TV and financials to movies | important | full | `3.7 Show Detail > "Seasons (TV only)"` and `"Budget/Revenue (movies)"` |  |
| PRD-064 | Keep primary actions early and page not overwhelming | important | partial | `3.7 Show Detail > section ordering and early toolbar controls` | The section order suggests the right emphasis, but the plan never explicitly addresses the "powerful but not overwhelming" presentation constraint. |
| PRD-065 | Provide conversational Ask chat interface | important | full | `3.5 Ask (AI Chat) > "Chat UI with streaming responses"` |  |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | full | `3.5 Ask > Persona` and `10. Testing Strategy > AI Quality Tests` |  |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | `3.5 Ask > "Mentioned shows strip"` |  |
| PRD-068 | Open Detail from mentions or Search fallback | important | partial | `3.5 Ask > "Mentioned shows strip"` | The strip is planned, but opening Detail with a Search fallback on failed mapping is not explicitly covered for mentions. |
| PRD-069 | Show six random starter prompts with refresh | important | partial | `3.5 Ask > "Welcome view with 6 random starter prompts"` | The plan includes six random starters but does not specify the required refresh behavior. |
| PRD-070 | Summarize older turns while preserving voice | important | partial | `3.5 Ask > "summarized after ~10 messages"` | Summarization is planned, but preserving the existing voice and persona in the summary is not specified. |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | full | `3.5 Ask > "seeded context from Detail"` |  |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | full | `3.5 Ask > AI Contract` |  |
| PRD-073 | Retry malformed mention output once, then fallback | important | full | `13. Risk Mitigation > "Structured output parsing fails | Retry once with stricter format; fallback to unstructured"` |  |
| PRD-074 | Redirect Ask back into TV/movie domain | important | missing | none | The plan never states that off-domain Ask prompts should be redirected back into the TV/movie domain. |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | partial | `3.6 Alchemy > "Conceptualize Shows -> AI extracts shared concepts"` | The plan handles concepts mechanically, but it does not define them as taste ingredients rather than genres or plot labels. |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | partial | `3.6 Alchemy > AI Contract` and `10. Testing Strategy > "Concept validation (1-3 words, no generic)"` | It covers length and specificity, but not the bullet-only output contract. |
| PRD-077 | Order concepts by strongest aha and varied axes | important | missing | none | The plan does not require concept ordering by strongest "aha" or coverage across varied concept axes. |
| PRD-078 | Require concept selection and guide ingredient picking | important | partial | `3.6 Alchemy > Flow` and `ConceptChips` | Selection is required, but the user guidance around ingredient picking and empty-state nudging is not planned. |
| PRD-079 | Return exactly five Explore Similar recommendations | important | full | `14. Success Criteria Checklist > "Explore Similar: concepts -> 5 recommendations"` |  |
| PRD-080 | Support full Alchemy loop with chaining | important | full | `3.6 Alchemy > Flow` and `"Optional "More Alchemy!" chaining"` |  |
| PRD-081 | Clear downstream results when inputs change | important | missing | none | The plan never states that changing selected shows or concepts must clear downstream concept or recommendation results. |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | partial | `3.6 Alchemy > AI Contract` and `4. API Routes > /api/ai/concepts` | Shared multi-show concepts are planned, but the larger multi-show option pool is not. |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | full | `3.6 Alchemy > "6 recommendations with reasons"` and `10. Testing Strategy > "reasons cite concepts"` |  |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | partial | `5. AI Integration Architecture > Context Assembly` and `10. Testing Strategy > AI Quality Tests` | The plan aims for grounded recommendations, but it does not require the "surprising but defensible" taste-alignment bar from the quality spec. |
| PRD-085 | Keep one consistent AI persona across surfaces | important | partial | `3.5 Ask > Persona` and `5. AI Integration Architecture > Prompt Templates` | The plan defines an Ask persona and prompt files, but it never explicitly locks one consistent persona across Scoop, Ask, Alchemy, and Explore Similar. |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | partial | `5. AI Integration Architecture > Context Assembly` and `13. Risk Mitigation` | Some AI constraints appear, but the shared cross-surface guardrails from the prompting spec are not captured as a unified contract. |
| PRD-087 | Make AI warm, joyful, and light in critique | important | partial | `3.5 Ask > "Persona: fun, chatty, opinionated, spoiler-safe"` | The plan sketches tone, but it does not explicitly require the warm, joyful, light-in-critique voice pillars. |
| PRD-088 | Structure Scoop as personal taste mini-review | important | partial | `10. Testing Strategy > "Scoop: sections present, spoiler-safe, honest about mixed reviews"` | The quality tests touch Scoop shape, but the plan never defines Scoop itself as a personal taste mini-review. |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | partial | `3.5 Ask > Chat UI with streaming responses` and `10. Testing Strategy > AI Quality Tests` | The plan covers format and confidence, but not the default brisk, dialogue-like pacing contract. |
| PRD-090 | Feed AI the right surface-specific context inputs | important | full | `5. AI Integration Architecture > Context Assembly` |  |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | partial | `10. Testing Strategy > AI Quality Tests` | AI validation is planned, but the explicit rubric thresholds and hard-fail integrity rule are missing. |
| PRD-092 | Show person gallery, name, and bio | important | partial | `3.8 Person Detail > "Image gallery"` and `"Bio"` | The plan covers gallery and bio, but it does not explicitly call out the person's name in the page contract. |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | full | `3.8 Person Detail > "Analytics charts (avg ratings, top genres, projects-by-year)"` |  |
| PRD-094 | Group filmography by year | important | full | `3.8 Person Detail > "Filmography grouped by year"` |  |
| PRD-095 | Open Show Detail from selected credit | important | full | `3.8 Person Detail > "Tap credit -> Show Detail"` |  |
| PRD-096 | Include font size and Search-on-launch settings | important | full | `3.9 Settings > "App: Font size, Search on Launch"` |  |
| PRD-097 | Support username, model, and API-key settings safely | important | partial | `3.9 Settings`, `2. Database Schema > cloud_settings`, and `8. Environment Configuration > Required Variables` | The settings surface includes the right fields, but safe handling boundaries for user-entered API keys are not fully specified. |
| PRD-098 | Export saved shows and My Data as zip | critical | full | `3.9 Settings > "Data: Export My Data (.zip backup)"` and `4. API Routes > "POST /api/export"` |  |
| PRD-099 | Encode export dates using ISO-8601 | important | full | `14. Success Criteria Checklist > "Export: .zip with JSON backup, ISO-8601 dates"` |  |

## 3. Coverage Scores

Overall score:

```text
(55 x 1.0 + 38 x 0.5) / 99 x 100 = 74.75%
```

Score by severity tier:

```text
Critical:  (20 x 1.0 + 9 x 0.5) / 30 x 100 = 81.67%  (24.5 of 30 critical requirements)
Important: (33 x 1.0 + 29 x 0.5) / 67 x 100 = 70.90%  (47.5 of 67 important requirements)
Detail:    (2 x 1.0 + 0 x 0.5) / 2 x 100 = 100.00%  (2 of 2 detail requirements)
Overall:   74.75% (99 total requirements)
```

## 4. Top Gaps

- PRD-026 | `critical` | Re-add preserves My Data and refreshes public data. This matters because the plan leaves the library without a defined recovery path for previously saved shows, which risks either data loss or stale public metadata when a title comes back into the collection.
- PRD-018 | `critical` | Overlay saved user data on every show appearance. This matters because inconsistent overlays across Search, recommendations, and AI surfaces would make the collection feel unreliable and break the "your version of the show" product promise.
- PRD-020 | `critical` | Map Interested/Excited chips to Later interest. This matters because the visible chips are a core relationship control, and leaving the chip-to-data mapping implicit can break saving, filtering, and grouping behavior.
- PRD-023 | `critical` | Save shows from status, interest, rating, tagging. This matters because one of the primary entry paths into the collection, selecting an interest chip, is not fully planned, which creates inconsistent collection writes.
- PRD-086 | `critical` | Enforce shared AI guardrails across all surfaces. This matters because Ask, Scoop, Explore Similar, and Alchemy can drift in domain, spoiler behavior, and honesty even if the UI ships correctly.

## 5. Coverage Narrative

#### Overall Posture

This is a structurally sound implementation plan with meaningful holes. It covers the major screens, data model, API surface, and phased delivery well enough to build a working app, but it underspecifies several critical behavioral contracts around collection semantics and AI behavior.

#### Strength Clusters

The plan is strongest in Benchmark Runtime & Isolation, Collection Home & Search basics, Show Detail & Relationship UX fundamentals, and the broad skeleton of Settings & Export. It also does a solid job on the main discovery surface decomposition: Search, Ask, Alchemy, Person Detail, API routes, and migration scaffolding are all concretely named and phased.

#### Weakness Clusters

The gaps cluster in two places. First, Collection Data & Persistence has several semantic holes around overlay rules, hidden `Next`, interest-chip mapping, re-add behavior, and persisted UI state. Second, AI Voice, Persona & Quality and Concepts, Explore Similar & Alchemy are only partially specified at the behavioral-contract level: the plan has endpoints and components, but it does not fully capture the voice, guardrails, concept quality rules, and recommendation quality bar from the supporting docs.

#### Risk Assessment

If this plan were executed as-is, the first thing QA or stakeholders would notice is not missing pages but behavioral drift. The app would likely look complete while failing subtle but important expectations: Search may feel too AI-adjacent, Ask may lack domain guardrails, concept outputs may be mechanically correct but not "aha" quality, and collection state may appear inconsistent when the same show shows up across library, search, and AI-driven surfaces.

#### Remediation Guidance

The remaining work is primarily more detailed specification, not a wholesale rewrite of the plan. The plan needs explicit decision tables and acceptance criteria for collection lifecycle semantics, cross-surface overlay behavior, chip-to-data mappings, and re-add flows. It also needs a stronger AI contract layer that captures shared guardrails, consistent persona rules, concept-generation quality requirements, and objective validation thresholds for discovery integrity.
