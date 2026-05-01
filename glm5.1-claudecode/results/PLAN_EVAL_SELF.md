# Plan Evaluation

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

---

## 2. Coverage Table

| PRD-ID | Requirement | Severity | Coverage | Evidence | Gap |
| ------ | ----------- | -------- | -------- | -------- | --- |
| PRD-001 | Use Next.js latest stable runtime | `critical` | full | Executive Summary: "Next.js (latest stable)"; Architecture §2.1: "Next.js (App Router)" | |
| PRD-002 | Use Supabase official client libraries | `critical` | full | Architecture §2.1: "Supabase (PostgreSQL)"; §2.2: `src/lib/supabase/client.ts`, `server.ts` | |
| PRD-003 | Ship `.env.example` with required variables | `critical` | full | Phase 1 step 3; §5.1 lists all env vars with comments | |
| PRD-004 | Ignore `.env*` secrets except example | `important` | partial | Phase 1 step 3 mentions `.gitignore` alongside `.env.example` | Does not explicitly state that `.gitignore` must exclude `.env*` except `.env.example` |
| PRD-005 | Configure build through env without code edits | `critical` | full | §5.1 env var interface; `src/config/env.ts`; all config via env | |
| PRD-006 | Keep secrets out of repo and server-only | `critical` | full | §5.1 `SUPABASE_SERVICE_ROLE_KEY` "Server-only"; §5.3 "All AI API keys stored server-only" | |
| PRD-007 | Provide app, test, reset command scripts | `critical` | full | Phase 1 step 9: `npm run dev`, `npm test`, `npm run test:reset` | |
| PRD-008 | Include repeatable schema evolution artifacts | `critical` | full | Phase 1 step 2: "run migrations for all tables"; §3.1 full SQL DDL | |
| PRD-009 | Use one stable namespace per build | `critical` | full | §5.1 `NAMESPACE_ID` env var; §3.1 `namespaces` table | |
| PRD-010 | Isolate namespaces and scope destructive resets | `critical` | full | §3.1 RLS policies keyed on `namespace_id`; Phase 5 step 6: "namespace-scoped destructive testing" | |
| PRD-011 | Attach every user record to `user_id` | `critical` | full | §3.1 all tables include `user_id` column; RLS enforces; Acceptance §5: "user_id on all records" | |
| PRD-012 | Partition persisted data by namespace and user | `critical` | full | §3.1 `UNIQUE(namespace_id, user_id, id)` constraints; RLS uses both dimensions | |
| PRD-013 | Support documented dev auth injection, prod-gated | `important` | full | §5.1: `X-User-Id` header in dev, dev-only login selector, production gate documented | |
| PRD-014 | Real OAuth later needs no schema redesign | `important` | full | §5.1: "Production: replace with real OAuth (Google) without schema changes" | |
| PRD-015 | Keep backend as persisted source of truth | `critical` | full | §9 key decisions: "Server is truth; cache is disposable" | |
| PRD-016 | Make client cache safe to discard | `critical` | full | §2.1: "SWR/React Query" with "Server is truth; cache is disposable; automatic revalidation" | |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | `important` | partial | Architecture is entirely hosted Supabase + Next.js with no Docker in the stack | Never explicitly acknowledges the Docker-independence constraint; relies on reader inferring it |
| PRD-018 | Overlay saved user data on every show appearance | `critical` | full | §4.2.1: "check if user has saved version → overlay My Data"; §2.2 user fields in `shows` table | |
| PRD-019 | Support visible statuses plus hidden `Next` | `important` | full | §3.1 schema: `my_status TEXT -- active | next | later | done | quit | wait`; §2.2 `constants.ts` | |
| PRD-020 | Map Interested/Excited chips to Later interest | `critical` | full | §4.3: "Interested/Excited map to Later + Interest"; §5.4: "Choosing interest chip → save (Later + Interested/Excited)" | |
| PRD-021 | Support free-form multi-tag personal tag library | `important` | full | §3.1 `my_tags TEXT[]`; §2.2 `TagPicker` component; §4.3 `TagManager` feature | |
| PRD-022 | Define collection membership by assigned status | `critical` | full | §4.1: "filtered by … where `my_status IS NOT NULL`" | |
| PRD-023 | Save shows from status, interest, rating, tagging | `critical` | full | §5.4 Saving triggers lists all four paths; Phase 2 step 4-6 | |
| PRD-024 | Default save to Later/Interested except rating-save Done | `critical` | full | §5.4: "No explicit status → Later + Interested"; "Rating first → Done (implies watched)" | |
| PRD-025 | Removing status deletes show and all My Data | `critical` | full | §4.3: "confirmation dialog → remove show + clear all My Data"; Phase 2 step 9 | |
| PRD-026 | Re-add preserves My Data and refreshes public data | `critical` | full | §5.4: "Preserve latest My Data, refresh public metadata"; "Merge by newest timestamp per field" | |
| PRD-027 | Track per-field My Data modification timestamps | `critical` | full | §3.1 schema: five `*_update_date` columns for status, interest, tags, score, scoop | |
| PRD-028 | Use timestamps for sorting, sync, freshness | `important` | full | §4.1: "Sort by `my_status_update_date` DESC"; §5.2: merge by newest timestamp | |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | `critical` | full | §4.3: "Only persists to DB if show is in collection"; "regenerates after 4 hours on demand" | |
| PRD-030 | Keep Ask and Alchemy state session-only | `important` | full | §5.3 persistence table: Ask and Alchemy marked "Session only"; §3.3 transient data list | |
| PRD-031 | Resolve AI recommendations to real selectable shows | `critical` | full | §4.2.2: "resolves via catalog lookup"; §4.2.3: "must map to real catalog item (title + external ID + media type)" | |
| PRD-032 | Show collection and rating tile indicators | `important` | full | §4.1: "in-collection badge, user rating badge" on tiles | |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | `important` | partial | Phase 4 step 10: "Implement cloud settings sync"; §3.1 `cloud_settings` table; §5.2 merge rules | No explicit strategy for cross-device library sync or transparent duplicate detection/merging |
| PRD-034 | Preserve saved libraries across data-model upgrades | `critical` | partial | §3.1 `app_metadata` table with `data_model_version` column exists | No migration strategy described; no plan for how schema evolution preserves existing user data during upgrades |
| PRD-035 | Persist synced settings, local settings, UI state | `important` | full | §3.1 `cloud_settings` table; §3.2 local settings (autoSearch, fontSize, filter state); `useSettings` hook | |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | `important` | full | §3.1 `provider_data JSONB`; §3.3: credits, seasons, images listed as transient | |
| PRD-037 | Merge catalog fields safely and maintain timestamps | `critical` | full | §5.2: `selectFirstNonEmpty(new, old)` for non-my fields; timestamp resolution for my fields; `detailsUpdateDate = now` | |
| PRD-038 | Provide filters panel and main screen destinations | `important` | full | §4.1 `FilterPanel` feature; §2.2 page routes: Home, Find, Detail, Person, Settings | |
| PRD-039 | Keep Find/Discover in persistent primary navigation | `important` | full | §2.2: `/find` route; §4.2 Find/Discover hub with mode switcher; root `layout.tsx` houses navigation | |
| PRD-040 | Keep Settings in persistent primary navigation | `important` | full | §2.2: `/settings` route; root `layout.tsx` houses navigation | |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | `important` | full | §4.2: "Mode switcher tabs: Search | Ask | Alchemy" | |
| PRD-042 | Show only library items matching active filters | `important` | full | §4.1: "Apply active filter configuration" on top of `my_status IS NOT NULL` query | |
| PRD-043 | Group home into Active, Excited, Interested, Others | `important` | full | §4.1 `StatusSections`: Active, Excited (Later+Excited), Interested (Later+Interested), Other (collapsed) | |
| PRD-044 | Support All, tag, genre, decade, score, media filters | `important` | full | §4.1: "All Shows, tag filters, genre/decade/score filters, media-type toggle" | |
| PRD-045 | Render poster, title, and My Data badges | `important` | full | §4.1: "poster, title, in-collection badge, user rating badge" | |
| PRD-046 | Provide empty-library and empty-filter states | `detail` | full | §4.1: "No collection → prompt to Search/Ask"; "Filter yields nothing → 'No results found'" | |
| PRD-047 | Search by title or keywords | `important` | full | §4.2.1: "Text input, live query against external catalog API"; API route `GET /api/catalog/search?q={query}` | |
| PRD-048 | Use poster grid with collection markers | `important` | full | §4.2.1: "Poster grid results, in-collection items marked" | |
| PRD-049 | Auto-open Search when setting is enabled | `detail` | full | §4.2.1: "Search on Launch auto-opens Search"; §3.2: `autoSearch: boolean` | |
| PRD-050 | Keep Search non-AI in tone | `important` | full | Search feature (§4.2.1) is a pure catalog proxy with no AI surface; AI persona section (§5.3) excludes Search | |
| PRD-051 | Preserve Show Detail narrative section order | `important` | partial | §4.3 lists 14 sections in explicit order; most sections match spec | Plan places StatusControls/RatingControl at positions 3-4 (before Overview), while spec places them in toolbar outside scroll body; Tags at 5 instead of 3; AskAboutShow at 7 instead of 5 |
| PRD-052 | Prioritize motion-rich header with graceful fallback | `important` | partial | §4.3: "backdrop/poster/logo carousel + trailers when available"; Phase 4 step 6 | Does not explicitly describe graceful fallback behavior when trailers are absent |
| PRD-053 | Surface year, runtime/seasons, and community score early | `important` | full | §4.3 CoreFacts at position 2: "year, runtime/seasons, community score bar" | |
| PRD-054 | Place status/interest controls in toolbar | `important` | partial | §4.3: "status chips in toolbar" text present | Controls also numbered as scroll-body sections 3-4, creating ambiguity about whether they are truly toolbar-only or duplicated in the scroll flow |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | `critical` | full | §4.3: "tagging unsaved show auto-saves as Later+Interested"; §5.4: explicit rule | |
| PRD-056 | Auto-save unsaved rated show as Done | `critical` | full | §4.3: "rating unsaved show auto-saves as Done"; §5.4: explicit rule | |
| PRD-057 | Show overview early for fast scanning | `important` | partial | OverviewAndScoop present at section 6 | Spec places overview at section 4 (before Ask CTA, genres, recs); plan positions it after StatusControls, RatingControl, and TagManager, pushing it below the fold relative to spec intent |
| PRD-058 | Scoop shows correct states and progressive feedback | `important` | full | §4.3: toggle states ("Give me the scoop!" → "Show the scoop" → "The Scoop"); "Generating… not a blank wait"; SSE streaming | |
| PRD-059 | Ask-about-show deep-link seeds Ask context | `important` | full | §4.3 AskAboutShow CTA; §4.2.2 "Ask about a show" variant; Phase 3 step 8 | |
| PRD-060 | Include traditional recommendations strand | `important` | full | §4.3 Recommendations at position 9; Phase 4 step 7 | |
| PRD-061 | Explore Similar uses CTA-first concept flow | `important` | full | §4.3: "Get Concepts → select concepts → Explore Shows"; Phase 3 step 6 | |
| PRD-062 | Include streaming availability and person-linking credits | `important` | full | §4.3: StreamingProviders section; CastCrew "horizontal strands → links to Person Detail" | |
| PRD-063 | Gate seasons to TV and financials to movies | `important` | full | §4.3: "Seasons (TV only)"; "BudgetRevenue (movies where available)" | |
| PRD-064 | Keep primary actions early and page not overwhelming | `important` | full | §4.3 clusters status/rating/tags/scoop in positions 3-6; long-tail info (streaming, cast, seasons, budget) near bottom | |
| PRD-065 | Provide conversational Ask chat interface | `important` | full | §4.2.2: ChatMessages, MentionedShows, StarterPrompts features; chat API route | |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | `important` | full | §5.3: "opinionated and honest"; "spoiler-safe by default"; "joy-forward, opinionated, specific" | |
| PRD-067 | Show horizontal mentioned-shows strip from chat | `important` | full | §4.2.2: "MentionedShows — horizontal strip of shows mentioned by AI" | |
| PRD-068 | Open Detail from mentions or Search fallback | `important` | partial | §4.2.2: "resolves via catalog lookup; failures become non-interactive text" | Does not mention Search fallback for Ask mentions; only non-interactive text for failures |
| PRD-069 | Show six random starter prompts with refresh | `important` | full | §4.2.2: "6 random prompts from a curated list of 80; refreshable"; Phase 3 step 4 | |
| PRD-070 | Summarize older turns while preserving voice | `important` | full | §4.2.2: "Summarize older turns into 1-2 sentences (same persona tone)" | |
| PRD-071 | Seed Ask-about-show sessions with show handoff | `important` | full | §4.2.2: "seed conversation with show context"; §4.3 AskAboutShow CTA; Phase 3 step 8 | |
| PRD-072 | Emit `commentary` plus exact `showList` contract | `critical` | full | §4.2.2: `{ commentary: string, showList: string }` format `Title::externalId::mediaType;;...` | |
| PRD-073 | Retry malformed mention output once, then fallback | `important` | partial | §5.3: "Structured output parsing with retry-on-failure fallback" | Does not specify "retry once" limit or the specific fallback behavior (unstructured commentary + Search handoff) |
| PRD-074 | Redirect Ask back into TV/movie domain | `important` | full | §5.3: "Guardrails: stay in TV/movie domain" | |
| PRD-075 | Treat concepts as taste ingredients, not genres | `important` | full | §5.3: "1-3 word evocative bullet list"; "avoids generic concepts ('good characters,' 'great story')" | |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | `important` | full | §5.3: "1-3 word evocative bullet list"; "no generic placeholders" | |
| PRD-077 | Order concepts by strongest aha and varied axes | `important` | partial | §5.3 describes concept format and quality but not ordering | No explicit requirement that concepts should be ordered by "aha" strength or cover varied axes (structure, vibe, emotion, craft) |
| PRD-078 | Require concept selection and guide ingredient picking | `important` | partial | §4.2.3: "user selects 1-8" concepts; §4.3: "select concepts" step required | Selection is enforced but no UI guidance copy (e.g., "pick the ingredients you want more of") is described |
| PRD-079 | Return exactly five Explore Similar recommendations | `important` | full | §4.3: "'Explore Shows' (5 AI recs)" | |
| PRD-080 | Support full Alchemy loop with chaining | `important` | full | §4.2.3: "'More Alchemy!' chains another round using results as new inputs"; Phase 3 step 7 | |
| PRD-081 | Clear downstream results when inputs change | `important` | full | §4.2.3: "Backtracking allowed (changing shows clears concepts/results)" | |
| PRD-082 | Generate shared multi-show concepts with larger option pool | `important` | partial | §5.3: multi-show concepts described as "Shared concept bullet list" | Does not specify that multi-show generation should return a larger pool of options than single-show generation |
| PRD-083 | Cite selected concepts in concise recommendation reasons | `important` | partial | §5.3: Concept Recs output is "5-6 shows with reasons" | Does not explicitly require that reasons must cite which selected concepts each recommendation aligns with |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | `important` | partial | §5.3 persona is "opinionated, specific"; "taste-aware" guardrail present | No explicit quality bar for "surprising but defensible" recommendations; no mention of the surprise-without-betrayal dimension |
| PRD-085 | Keep one consistent AI persona across surfaces | `important` | full | §5.3: "AI persona consistency" with shared tone sliders and behavior description | |
| PRD-086 | Enforce shared AI guardrails across all surfaces | `critical` | full | §5.3: "Guardrails: stay in TV/movie domain, spoiler-safe, taste-aware"; server-side enforcement | |
| PRD-087 | Make AI warm, joyful, and light in critique | `important` | full | §5.3: "Joy-forward, opinionated, specific"; "70% friend / 30% critic tone balance" | |
| PRD-088 | Structure Scoop as personal taste mini-review | `important` | partial | §5.3: "Structured 'mini blog post' text"; §4.3: streaming and toggle described | Does not detail the Scoop's required internal structure (personal take, honest stack-up, Scoop centerpiece, fit/warnings, verdict) |
| PRD-089 | Keep Ask brisk and dialogue-like by default | `important` | partial | §5.3 persona is "fun, chatty TV/movie nerd friend" | No explicit length target (e.g., 1-3 tight paragraphs) or brisk/dialogue-like behavioral contract for Ask specifically |
| PRD-090 | Feed AI the right surface-specific context inputs | `important` | full | §5.3 AI contracts table: each surface lists its specific inputs (library, show context, concepts, history) | |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | `important` | missing | none | Plan does not address discovery quality validation, scoring rubric, or hard-fail integrity checks for AI output |
| PRD-092 | Show person gallery, name, and bio | `important` | full | §4.4: "PersonGallery — image gallery + name + bio" | |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | `important` | full | §4.4: "AnalyticsCharts — average project ratings, top genres, projects-by-year" | |
| PRD-094 | Group filmography by year | `important` | full | §4.4: "Filmography — credits grouped by year" | |
| PRD-095 | Open Show Detail from selected credit | `important` | full | §4.4: "Each credit links to Show Detail" | |
| PRD-096 | Include font size and Search-on-launch settings | `important` | full | §4.5: "Font size, Search on Launch"; §3.2: `fontSize`, `autoSearch` | |
| PRD-097 | Support username, model, and API-key settings safely | `important` | full | §4.5: Username, AI provider key (env var, never committed), model selection, catalog API key | |
| PRD-098 | Export saved shows and My Data as zip | `critical` | full | §4.5: "'Export My Data' → produces `.zip` with JSON backup"; §2.2 `exportBackup.ts`; API route `GET /api/export` | |
| PRD-099 | Encode export dates using ISO-8601 | `important` | full | §4.5: "ISO-8601 dates"; §8 testing: "ISO-8601 dates" | |

---

## 3. Coverage Scores

```
Critical:  (28 × 1.0 + 1 × 0.5) / 30 × 100 = 96.7%  (28 of 30 critical requirements covered)
Important: (50 × 1.0 + 16 × 0.5) / 67 × 100 = 86.6%  (50 of 67 important requirements covered)
Detail:    (2 × 1.0 + 0 × 0.5) / 2 × 100 = 100.0%  (2 of 2 detail requirements covered)
Overall:   90.4% (99 total requirements)
```

---

## 4. Top Gaps

### 1. PRD-034 | `critical` | Preserve saved libraries across data-model upgrades

The plan includes an `app_metadata` table with a `data_model_version` column but provides no migration strategy. When the schema evolves between benchmark rounds or production updates, there is no specified mechanism to automatically migrate existing saved shows and My Data forward. Without this, users who built collections in a prior version could lose their data silently on upgrade, violating one of the product's core promises ("Your data is yours").

### 2. PRD-091 | `important` | Validate discovery with rubric and hard-fail integrity

The plan omits any mention of a discovery quality validation layer. The PRD defines a specific scoring rubric (voice, taste alignment, surprise, specificity, real-show integrity) with a passing threshold. Without incorporating this rubric into testing or runtime validation, the app could ship AI output that passes formatting checks but fails the qualitative bar that differentiates the product from generic chatbot responses.

### 3. PRD-033 | `important` | Sync libraries/settings consistently and merge duplicates

The plan describes cloud settings sync and per-field merge rules for catalog refreshes, but does not address how cross-device library sync works end-to-end. Duplicate detection and transparent merging across devices — required by the PRD — has no specified strategy. This could lead to duplicated collection entries or lost updates in multi-device scenarios.

### 4. PRD-051 | `important` | Preserve Show Detail narrative section order

The plan's section ordering deviates from the spec in material ways: status/rating controls appear in the scroll body (positions 3-4) rather than being toolbar-only; overview is pushed to position 6 (spec: position 4); AskAboutShow is at position 7 (spec: position 5). This changes the first-15-seconds experience that the detail page spec is designed around, potentially making the page feel cluttered at the top and pushing key content below the fold.

### 5. PRD-088 | `important` | Structure Scoop as personal taste mini-review

The plan describes Scoop as "structured 'mini blog post' text" and details the toggle states and streaming behavior, but does not specify the required internal structure (personal take, honest stack-up vs reviews, the Scoop centerpiece paragraph, fit/warnings, and "Worth it?" verdict). Without this structure encoded in the prompt design, Scoop output could drift toward generic summaries rather than the opinionated taste review that defines the feature's value.

---

## 5. Coverage Narrative

#### Overall Posture

This is a structurally sound plan with a strong infrastructure foundation and concerning holes in AI behavioral detail and data continuity. Critical infrastructure requirements (runtime, persistence, isolation, auth) are near-perfectly covered at 96.7%. The plan's architecture is well-reasoned, with clear phase ordering, specific technology choices, and detailed schema design. However, the plan treats AI quality specifications as an implementation detail to be handled by prompt templates rather than as specifiable behavioral surfaces — and it leaves data migration strategy as an implicit gap. The plan would produce a functional application but risks missing the product's "heart" in its AI interactions and could fail users during version upgrades.

#### Strength Clusters

**Benchmark Runtime & Isolation** is the strongest area — essentially complete with only one partial (PRD-017 Docker-independence not explicitly acknowledged). Every namespace, user identity, env configuration, and test isolation requirement is concretely addressed with schema, middleware, and scripts.

**Collection Data & Persistence** core mechanics are thorough: all saving triggers, default values, removal flows, merge rules, and timestamp tracking are explicitly specified with both schema columns and behavioral descriptions. The auto-save rules for status, rating, and tagging are each called out individually with correct defaults.

**Person Detail** and **Settings & Export** are fully covered — every requirement in both areas maps to a concrete feature, route, and acceptance criterion.

**App Navigation & Discover Shell** is complete with all four requirements addressed through the route structure and Find hub mode switcher.

#### Weakness Clusters

The gaps cluster around two distinct patterns:

1. **AI behavioral contracts** — The plan describes *what* each AI surface outputs (format, count, persistence) but not *how* it should behave qualitatively. This cluster spans AI Voice, Persona & Quality (PRD-088 Scoop structure, PRD-089 Ask briskness, PRD-091 quality rubric), Concepts (PRD-077 ordering, PRD-083 reason citing, PRD-084 surprise/defensibility), and Ask Chat (PRD-073 retry specificity). The plan treats AI behavior as a prompt-engineering task rather than a plan-level specification, which leaves the app's most differentiating feature underspecified.

2. **Show Detail section ordering** — A cluster of partials (PRD-051, PRD-052, PRD-054, PRD-057) all stem from the same root cause: the plan reorders the detail page narrative hierarchy, placing controls in the scroll body instead of the toolbar and pushing overview further down. This is a single architectural decision with cascading partial coverage.

#### Risk Assessment

If this plan were executed as-is, the most likely failure mode is **generic AI output that passes structural validation but fails the product's quality bar**. The plan specifies that Scoop should be a "mini blog post" and Ask should emit `commentary + showList`, but it does not encode the Scoop's five-part structure, the Ask's brisk dialogue target, or the discovery quality rubric. A QA reviewer would notice that AI responses feel like competent chatbot output rather than the opinionated, vibe-forward, specific taste commentary the product requires. This is the exact gap the `ai_voice_personality.md` and `discovery_quality_bar.md` companion documents exist to prevent.

A secondary risk is **data loss during schema upgrades**. The `app_metadata` table tracks the data model version but the plan provides no migration path, meaning any schema change between versions could orphan existing user collections.

#### Remediation Guidance

The plan needs three categories of additional specification:

1. **AI behavioral contracts per surface** — Not prompt text, but structural requirements: Scoop must contain [personal take, stack-up, centerpiece, fit/warnings, verdict]; Ask responses must target [1-3 tight paragraphs, then a list]; concept reasons must cite [which selected concepts they align with]. These belong in the plan's AI integration section (§5.3) as concrete acceptance criteria, not in deferred prompt templates.

2. **Data migration strategy** — A section describing how `app_metadata.data_model_version` drives migration logic: version detection, field mapping, default filling for new columns, and backward compatibility testing. This should be added to Phase 1 (schema) and Phase 5 (testing).

3. **Show Detail section order correction** — Reorder §4.3 to match the detail page spec: move status/rating controls to toolbar-only (not numbered sections), move Tags to position 3, Overview+Scoop to position 4, AskAboutShow to position 5. This single change resolves four partial items simultaneously.
