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
| PRD-001 | Use Next.js latest stable runtime | critical | full | 2. Scope Summary; 3.1 Runtime and routing | |
| PRD-002 | Use Supabase official client libraries | critical | full | 2. Scope Summary; 4.2 Server layers > server/supabase | |
| PRD-003 | Ship `.env.example` with required variables | critical | full | 10. Delivery Phases > Phase 0: Foundations; 12. Required Repo Deliverables | |
| PRD-004 | Ignore `.env*` secrets except example | important | full | 12. Required Repo Deliverables > `.gitignore` excluding secrets | |
| PRD-005 | Configure build through env without code edits | critical | full | 10. Delivery Phases > Phase 0 > "App boots from env configuration only"; 12. Required Repo Deliverables | |
| PRD-006 | Keep secrets out of repo and server-only | critical | full | 3.1 Runtime and routing; 4.2 Server layers > server/supabase; 12. Required Repo Deliverables | |
| PRD-007 | Provide app, test, reset command scripts | critical | full | 12. Required Repo Deliverables > Scripts for starting the app, running tests, resetting namespace-scoped test data | |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | 10. Delivery Phases > Phase 0 > Create Supabase migration structure; 12. Required Repo Deliverables > repeatable migrations | |
| PRD-009 | Use one stable namespace per build | critical | full | 3.3 Isolation and identity; 6.2 Namespace resolution | |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | 3.3 Isolation and identity; 6.2 Namespace resolution; 10. Delivery Phases > Phase 6 > benchmark reset tooling | |
| PRD-011 | Attach every user record to `user_id` | critical | full | 3.3 Isolation and identity; 5.1 Durable tables > saved_shows and cloud_settings keys | |
| PRD-012 | Partition persisted data by namespace and user | critical | full | 3.3 Isolation and identity; 5.1 Durable tables > `(namespace_id, user_id, show_id)` | |
| PRD-013 | Support documented dev auth injection, prod-gated | important | full | 3.3 Isolation and identity; 6.1 Identity resolution; 12. Required Repo Deliverables > benchmark identity injection docs | |
| PRD-014 | Real OAuth later needs no schema redesign | important | full | 3.3 Isolation and identity; 6.3 Supabase access policy | |
| PRD-015 | Keep backend as persisted source of truth | critical | full | 3.2 Data ownership | |
| PRD-016 | Make client cache safe to discard | critical | full | 3.2 Data ownership; 5.2 Local-only UI settings | |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | partial | 2. Scope Summary > Supabase-backed persistence using official client libraries | The plan never explicitly states Docker is optional or unsupported, so cloud-agent compatibility remains implied rather than planned. |
| PRD-018 | Overlay saved user data on every show appearance | critical | full | 5.4 Overlay behavior | |
| PRD-019 | Support visible statuses plus hidden `Next` | important | partial | 2. Explicitly out of initial implementation scope > "First-class `Next` UI status" | The plan calls out the visible UI omission but never reserves hidden `Next` support in the data model or business rules. |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | full | 5.3 Merge and save rules > rule 3; 8.3 Show Detail > status chips | |
| PRD-021 | Support free-form multi-tag personal tag library | important | full | 2. Scope Summary; 8.1 Collection Home > tag-derived filters | |
| PRD-022 | Define collection membership by assigned status | critical | full | 5.3 Merge and save rules > rule 1 | |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | full | 5.3 Merge and save rules > rules 2-5 | |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | 5.3 Merge and save rules > rules 3-5 | |
| PRD-025 | Removing status deletes show and all My Data | critical | full | 5.3 Merge and save rules > rule 6; 8.3 Show Detail > reselecting an active status | |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | full | 5.3 Merge and save rules > rules 7-10; 5.4 Overlay behavior | |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | 5.1 Durable tables > `my_*_update_date` columns; 5.3 Merge and save rules | |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | full | 5.1 Durable tables; 5.3 Merge and save rules > user fields merge by timestamps; 8.1 Collection Home > recent-update timestamps | |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | full | 3.4 Persistence strategy; 8.3 Show Detail > persisted only if the show is in the collection; 10. Delivery Phases > Phase 4 | |
| PRD-030 | Keep Ask and Alchemy state session-only | important | full | 2. Explicitly out of initial implementation scope; 8.4 Ask > ephemeral; 8.5 Alchemy > session-only | |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | full | 3.5 AI architecture; 9.3 Recommendation mapping pipeline | |
| PRD-032 | Show collection and rating tile indicators | important | full | 8.1 Collection Home > tile badges; 8.2 Search > overlay badges | |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | partial | 5.1 Durable tables > `cloud_settings.version`; 5.3 Merge and save rules > timestamp merges | The plan covers timestamp-based conflict handling but does not explicitly plan duplicate detection and transparent merge behavior for synced libraries. |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | partial | 5.1 Durable tables > `app_metadata`; 10. Delivery Phases > Phase 0 > migration structure | Migrations and version tracking are planned, but there is no explicit upgrade path or acceptance gate proving existing libraries survive model changes intact. |
| PRD-035 | Persist synced settings, local settings, UI state | important | full | 5.1 Durable tables > `cloud_settings`; 5.2 Local-only UI settings | |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | full | 5.1 Durable tables > `provider_data` JSONB; 7.1 Catalog integration > transient fields fetched on demand | |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | full | 5.3 Merge and save rules > rules 7-10; 7.1 Catalog integration > transient mapping | |
| PRD-038 | Provide filters panel and main screen destinations | important | full | 8.1 Collection Home > filter/navigation panel; 4.1 Frontend structure | |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | partial | 4.1 Frontend structure > `find/page.tsx`; 8.2 Search > Find hub | The plan includes the Find route and modes but never explicitly commits to a persistent primary-nav entry. |
| PRD-040 | Keep Settings in persistent primary navigation | important | partial | 4.1 Frontend structure > `settings/page.tsx`; 8.8 Settings and Your Data | The settings surface is planned, but the app shell does not explicitly reserve it as a persistent primary-nav destination. |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | 4.1 Frontend structure > `FindModeSwitcher`, `SearchMode`, `AskMode`, `AlchemyMode`; 8.2-8.5 | |
| PRD-042 | Show only library items matching active filters | important | full | 8.1 Collection Home > "Shows matching the selected filter(s) are displayed" | |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | 8.1 Collection Home > grouped sections | |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | full | 8.1 Collection Home > All Shows, tag-derived filters, data filters, media-type toggle | |
| PRD-045 | Render poster, title, and My Data badges | important | full | 8.1 Collection Home > tiles/badges; 8.2 Search > poster grid with overlay badges | |
| PRD-046 | Provide empty-library and empty-filter states | detail | full | 8.1 Collection Home > Empty states | |
| PRD-047 | Search by title or keywords | important | full | 8.2 Search > live text search against external catalog | |
| PRD-048 | Use poster grid with collection markers | important | full | 8.2 Search > poster grid results with overlay badges | |
| PRD-049 | Auto-open Search when setting is enabled | detail | full | 8.2 Search > respecting the local `autoSearch` preference | |
| PRD-050 | Keep Search non-AI in tone | important | partial | 8.2 Search > live text search against external catalog | The plan treats Search as catalog-driven, but it never explicitly states that Search must stay free of AI voice or AI-generated tone. |
| PRD-051 | Preserve Show Detail narrative section order | important | full | 8.3 Show Detail > "Preserve the documented narrative order" | |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | partial | 8.3 Show Detail > header media carousel | The plan names the header section but does not specify trailer-first motion handling or graceful visual fallback behavior. |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | full | 8.3 Show Detail > core facts and community score | |
| PRD-054 | Place status/interest controls in toolbar | important | partial | 4.1 Frontend structure > `RatingAndStatusBar`; 8.3 Show Detail > status chips | The plan places relationship controls early, but it does not explicitly preserve the toolbar placement required by the detail-page spec. |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | 5.3 Merge and save rules > rule 4; 8.3 Show Detail > tagging auto-saves | |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | 5.3 Merge and save rules > rule 5; 8.3 Show Detail > rating auto-saves | |
| PRD-057 | Show overview early for fast scanning | important | full | 8.3 Show Detail > section order places Overview fourth | |
| PRD-058 | Scoop shows correct states and progressive feedback | important | partial | 8.3 Show Detail > Scoop is generated on demand; 7.2 AI provider integration > progressive streaming if feasible | The plan covers on-demand Scoop generation, but not the required toggle-state UX and guaranteed progressive feedback behavior. |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | full | 8.3 Show Detail > Ask about this show CTA; 8.4 Ask > handoff from Detail page | |
| PRD-060 | Include traditional recommendations strand | important | full | 8.3 Show Detail > Traditional recommendations | |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | partial | 8.3 Show Detail > Explore Similar; 8.6 Explore Similar > Get Concepts -> chips -> Explore Shows | The flow is present, but the plan does not explicitly preserve the CTA-first state where only Get Concepts appears before concepts are loaded. |
| PRD-062 | Include streaming availability and person-linking credits | important | full | 8.3 Show Detail > streaming availability and Cast/Crew; 8.7 Person Detail | |
| PRD-063 | Gate seasons to TV and financials to movies | important | full | 8.3 Show Detail > "Seasons for TV" and "Budget/Revenue for movies" | |
| PRD-064 | Keep primary actions early and page not overwhelming | important | partial | 8.3 Show Detail > section order; 4.1 Frontend structure | The plan preserves the sections, but it does not state how the layout will keep early actions prominent without making the page feel overloaded. |
| PRD-065 | Provide conversational Ask chat interface | important | full | 8.4 Ask > Chat UI inside Find | |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | full | 9.1 Shared AI behavior; 9.2 Surface-specific contracts > Ask | |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | 8.4 Ask > mentioned-show strip derived from structured AI output | |
| PRD-068 | Open Detail from mentions or Search fallback | important | full | 8.4 Ask > tapping a mentioned show opens Detail or Search handoff | |
| PRD-069 | Show six random starter prompts with refresh | important | full | 8.4 Ask > welcome state with 6 random starter prompts and refresh | |
| PRD-070 | Summarize older turns while preserving voice | important | partial | 8.4 Ask > session context retention with summarization; 9.1 Shared AI behavior | The plan includes summarization, but it never explicitly preserves the same voice/persona in the summarized turns. |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | full | 8.4 Ask > Ask-about-a-show handoff from Detail page | |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | partial | 8.4 Ask > "Structure output as `commentary` plus `showList`" | The plan omits the exact `Title::externalId::mediaType;;...` string contract, so parser compatibility is not fully specified. |
| PRD-073 | Retry malformed mention output once, then fallback | important | full | 8.4 Ask > retry once on parser failure, then fall back | |
| PRD-074 | Redirect Ask back into TV/movie domain | important | full | 9.1 Shared AI behavior > stay in the TV/movie domain | |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | partial | 8.5 Alchemy > concept-aware reasons; 8.6 Explore Similar > evocative concepts | The plan treats concepts as structured AI output, but it never explicitly frames them as taste ingredients rather than genres. |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | full | 8.6 Explore Similar > 1-3 words, evocative, spoiler-safe, and not generic; 9.2 Concepts | |
| PRD-077 | Order concepts by strongest aha and varied axes | important | partial | 8.6 Explore Similar > evocative concepts; 9.4 Quality bar enforcement | The plan does not specify ordering concepts by strongest aha first or ensuring deliberate variety across structural, emotional, and craft axes. |
| PRD-078 | Require concept selection and guide ingredient picking | important | partial | 8.5 Alchemy > concept selection with a max of 8; 8.6 Explore Similar > select 1+ concepts | Selection is planned, but the UX guidance that teaches users to pick ingredients they want more of is absent. |
| PRD-079 | Return exactly five Explore Similar recommendations | important | full | 8.6 Explore Similar > 5 mapped recommendations; 9.2 Surface-specific contracts | |
| PRD-080 | Support full Alchemy loop with chaining | important | full | 8.5 Alchemy > full numbered loop; "More Alchemy!" | |
| PRD-081 | Clear downstream results when inputs change | important | full | 8.5 Alchemy > changing the input selection clears concepts and downstream results | |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | partial | 8.5 Alchemy > concept generation across all selected titles | The multi-show flow is covered, but the plan never commits to returning a larger concept option pool than single-show generation. |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | full | 8.5 Alchemy > concept-aware reasons; 9.2 Surface-specific contracts | |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | full | 9.4 Quality bar enforcement > Surprise without betrayal; Taste alignment | |
| PRD-085 | Keep one consistent AI persona across surfaces | important | full | 3.5 AI architecture; 9.1 Shared AI behavior | |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | full | 9.1 Shared AI behavior; 7.2 AI provider integration | |
| PRD-087 | Make AI warm, joyful, and light in critique | important | partial | 9.1 Shared AI behavior > opinionated and honest; 3.5 AI architecture > preserve shared personality | Persona consistency is planned, but the warmth/joy/light-critique voice pillars are not explicitly translated into delivery requirements. |
| PRD-088 | Structure Scoop as personal taste mini-review | important | full | 9.2 Surface-specific contracts > Scoop | |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | full | 9.2 Surface-specific contracts > Ask | |
| PRD-090 | Feed AI the right surface-specific context inputs | important | partial | 3.5 AI architecture; 8.4 Ask > handoff from Detail; 8.5/8.6 concept inputs | The plan references contextual grounding, but it never enumerates the required per-surface inputs such as library/My Data, current show context, selected concepts, and summarized recent turns. |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | full | 9.4 Quality bar enforcement; 11.4 Manual AI review | |
| PRD-092 | Show person gallery, name, and bio | important | full | 8.7 Person Detail > hero area with image gallery, name, and bio | |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | full | 8.7 Person Detail > average project ratings, top genres, projects by year | |
| PRD-094 | Group filmography by year | important | full | 8.7 Person Detail > filmography grouped by year | |
| PRD-095 | Open Show Detail from selected credit | important | full | 8.7 Person Detail > credit selection opens Show Detail | |
| PRD-096 | Include font size and Search-on-launch settings | important | full | 8.8 Settings and Your Data > font size/readability controls; Search-on-launch toggle | |
| PRD-097 | Support username, model, and API-key settings safely | important | full | 8.8 Settings and Your Data > Username, AI provider key, AI model, Catalog provider API key | |
| PRD-098 | Export saved shows and My Data as zip | critical | full | 8.8 Settings and Your Data > Export My Data to a zip containing JSON | |
| PRD-099 | Encode export dates using ISO-8601 | important | full | 8.8 Settings and Your Data > ISO-8601 dates | |

## 3. Coverage Scores

score = (full_count × 1.0 + partial_count × 0.5) / total_count × 100

Critical:  (28 × 1.0 + 2 × 0.5) / 30 × 100 = 96.7%  (29.0 of 30 critical requirements)
Important: (49 × 1.0 + 18 × 0.5) / 67 × 100 = 86.6%  (58.0 of 67 important requirements)
Detail:    (2 × 1.0 + 0 × 0.5) / 2 × 100 = 100.0%  (2.0 of 2 detail requirements)
Overall:   89.9% (89.0 of 99 total requirements)

## 4. Top Gaps

1. PRD-072 | `critical` | Emit `commentary` plus exact `showList` contract
Without the exact Ask wire format, the mentioned-shows strip can break or silently drop recommendations, which directly weakens a benchmark-visible discovery surface.

2. PRD-034 | `critical` | Preserve saved libraries across data-model upgrades
Without an explicit migration continuity plan and verification gate, future schema changes can strand or lose user collections, which is a direct durability failure.

3. PRD-033 | `important` | Sync libraries/settings consistently and merge duplicates
Without duplicate detection and transparent merge rules, cross-device sync can produce conflicting or duplicated library state that users cannot easily untangle.

4. PRD-019 | `important` | Support visible statuses plus hidden `Next`
If hidden `Next` support is omitted from the model now, a later product decision to surface it will force avoidable schema/API churn and reduce spec compatibility.

5. PRD-058 | `important` | Scoop shows correct states and progressive feedback
If Scoop state transitions and progressive feedback are not specified, one of the product's signature delight moments will feel brittle or unfinished in QA.

## 5. Coverage Narrative

#### Overall Posture

This is a strong, structurally sound plan with high critical coverage and no outright missing requirements, but it still leaves a meaningful set of benchmark-sensitive behaviors underdefined. The architecture, data model, and phased delivery are solid; the remaining shortfall is mostly precision around exact UX and AI contracts rather than wholesale feature absence.

#### Strength Clusters

The plan is strongest in Benchmark Runtime & Isolation, Collection Data & Persistence, Collection Home & Search, and Settings & Export. It is explicit about Next.js/Supabase, env-driven configuration, namespace and user scoping, durable save and merge rules, overlay behavior, export, and the major delivery phases required to ship the collection, detail, person, and settings surfaces end to end.

#### Weakness Clusters

The partials cluster in three patterns. First, AI behavioral precision is weaker than the rest of the plan: Ask's exact structured output, per-surface context payloads, concept philosophy, and a few voice-specific requirements are not locked down tightly enough. Second, the Detail experience loses some fidelity from the supporting docs, especially toolbar placement, motion/fallback behavior, CTA-first concept flow, and Scoop state handling. Third, a smaller set of lifecycle/app-shell nuances remain soft, notably Docker-free cloud-agent assumptions, persistent primary navigation, hidden `Next` support, duplicate merge behavior, and upgrade continuity.

#### Risk Assessment

If this plan were executed as-is, the most likely result is an app that looks broadly correct and covers the core journeys, but misses benchmark-visible details that stakeholders and QA would notice quickly. Ask mentions are the sharpest risk because the exact `showList` contract is underspecified; after that, the most visible failures would be a slightly off-spec Detail page experience and unresolved migration/sync edge cases that threaten long-term trust in saved data.

#### Remediation Guidance

The remaining work is mostly plan refinement, not a re-plan. Add explicit acceptance criteria for schema upgrades and duplicate merge behavior; specify the exact Ask output contract and required context inputs per AI surface; and tighten the UX planning for the app shell and Detail page microflows, especially toolbar placement, CTA-first concepts, and Scoop state transitions/progressive feedback.
