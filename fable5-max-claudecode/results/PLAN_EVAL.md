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
| PRD-001 | Use Next.js latest stable runtime | critical | full | Scope Summary: "Next.js (latest stable) as UI + server boundary" | |
| PRD-002 | Use Supabase official client libraries | critical | full | D1: "Supabase JS client"; Scope Summary: "Supabase ... via official client libraries" | |
| PRD-003 | Ship `.env.example` with required variables | critical | full | Section 13: "`.env.example` (names + comments)" | |
| PRD-004 | Ignore `.env*` secrets except example | important | full | Repository Layout: "`.gitignore` excludes `.env*` except `.env.example`" | |
| PRD-005 | Configure build through env without code edits | critical | full | Section 13: "runs with zero code edits" | |
| PRD-006 | Keep secrets out of repo and server-only | critical | full | D1 and Section 13: service role, catalog, and AI keys are server-only | |
| PRD-007 | Provide app, test, reset command scripts | critical | full | Section 13 scripts include `dev`, `test`, `test:reset`; Section 12 defines test scripts | |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | Sections 4 and 5.3: `supabase/migrations/`, `db:migrate`, deterministic fresh DB | |
| PRD-009 | Use one stable namespace per build | critical | full | D4: `namespace_id` from `NAMESPACE_ID` env, stamped on every row | |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | Section 5.3: reset deletes rows where `namespace_id = $NAMESPACE_ID`; integration tests prove isolation | |
| PRD-011 | Attach every user record to `user_id` | critical | full | Section 5.1: all user-owned tables share `user_id`; D4 opaque identity | |
| PRD-012 | Partition persisted data by namespace and user | critical | full | Section 5.1 primary keys use `(namespace_id, user_id, id)` | |
| PRD-013 | Support documented dev auth injection, prod-gated | important | full | D4 and Section 11: `X-User-Id` in dev/test, rejected in production | |
| PRD-014 | Real OAuth later needs no schema redesign | important | full | Section 5.2: OAuth policies can be added without schema change | |
| PRD-015 | Keep backend as persisted source of truth | critical | full | D1 and System Architecture: "Backend is the source of truth" | |
| PRD-016 | Make client cache safe to discard | critical | full | D5: TanStack Query in-memory only; no critical data in localStorage | |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | full | Section 5.3 and README plan: Docker optional, hosted Supabase primary path | |
| PRD-018 | Overlay saved user data on every show appearance | critical | full | Section 7.4: `overlayUserData` used by search, recs, mentions, Alchemy/Explore, person credits | |
| PRD-019 | Support visible statuses plus hidden `Next` | important | full | Section 5.1 DB includes `next`; D9 and StatusToolbar keep it data-model-only | |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | full | Section 7.1: interest chip creates `myStatus='later'`, `myInterest` chosen | |
| PRD-021 | Support free-form multi-tag personal tag library | important | full | Section 5.1 `my_tags text[]`; Section 7.5 distinct tags build filters | |
| PRD-022 | Define collection membership by assigned status | critical | full | Section 5.1 notes: "In collection == row exists with non-null `my_status`" | |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | full | Section 7.1 lists all four save triggers | |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | Section 7.1: generic default Later/Interested; rating sets Done | |
| PRD-025 | Removing status deletes show and all My Data | critical | full | Section 7.2: DELETE row clears status, interest, tags, rating, Scoop | |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | full | Section 7.3 merge engine preserves user edits; Section 5.4 upserts run merge engine | |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | Section 5.1 paired `*_update_date` fields; Section 7.1 stamps changed fields | |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | full | Sections 6, 5.4, and 8.5 use timestamps for ordering, conflict resolution, Scoop freshness | |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | full | Section 8.5: 4h cache, persist only if in collection, unsaved session-only | |
| PRD-030 | Keep Ask and Alchemy state session-only | important | full | D5 and Section 9.4: Zustand session stores, AI transient state not persisted | |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | full | Sections 8.4 and 8.7: resolver maps recs to real catalog items, unresolved handoff | |
| PRD-032 | Show collection and rating tile indicators | important | full | Section 7.4 emits `inCollection` and `hasRating` tile flags | |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | full | Section 5.4: backend source of truth, timestamp conflict resolution, PK prevents duplicates | |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | full | Section 5.5: migration registry transforms user rows in transaction | |
| PRD-035 | Persist synced settings, local settings, UI state | important | full | Section 5.1 `user_settings` includes cloud, local, and UI-state fields | |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | full | Section 5.1 provider IDs only; System Architecture says credits/seasons/videos/recs are never persisted | |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | full | Section 7.3: `selectFirstNonEmpty`, per-field timestamps, immutable creation date | |
| PRD-038 | Provide filters panel and main screen destinations | important | full | Repository Layout and Section 9.1 include Home, Find, Detail, Person, Settings, FiltersSidebar | |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | full | Scope Summary and Section 15 traceability: persistent Find hub | |
| PRD-040 | Keep Settings in persistent primary navigation | important | full | Scope Summary and Section 15 traceability: persistent Settings entry | |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | Section 9.1 Find mode switcher: Search, Ask, Alchemy | |
| PRD-042 | Show only library items matching active filters | important | full | Section 6 `/api/shows` filter/media params; Section 7.5 `applyFilter` | |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | Section 9.1 StatusSections with Active, Excited, Interested, Other | |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | full | Section 7.5 filter types and media-type layering | |
| PRD-045 | Render poster, title, and My Data badges | important | full | Scope Summary and Section 7.4 overlay/tile badges; Search/Home use ShowTile | |
| PRD-046 | Provide empty-library and empty-filter states | detail | full | Section 9.1 EmptyState: no collection prompts Search/Ask, filter says "No results found" | |
| PRD-047 | Search by title or keywords | important | full | Section 6 `/api/catalog/search`: `?q=` text search | |
| PRD-048 | Use poster grid with collection markers | important | full | Section 9.1 SearchMode: SearchBar, ResultsGrid with in-collection marks | |
| PRD-049 | Auto-open Search when setting is enabled | detail | full | Section 11 Behavior setting and Section 12 e2e includes search-on-launch | |
| PRD-050 | Keep Search non-AI in tone | important | full | Section 8.2: "Search has no AI voice" | |
| PRD-051 | Preserve Show Detail narrative section order | important | full | Section 9.1: ShowDetail section order is "load-bearing"; Section 15 traces detail order | |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | full | Section 9.1 HeaderMedia: carousel, inline trailers, graceful poster/logo fallback | |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | full | Section 9.1 CoreFacts and Section 9.2 first-15-seconds guarantees | |
| PRD-054 | Place status/interest controls in toolbar | important | full | Section 9.1 StatusToolbar: chips in toolbar, not scroll body | |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | Section 7.1 tag save trigger; Section 9.1 MyTags comment | |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | Section 7.1 rating trigger; Section 9.1 MyRating comment | |
| PRD-057 | Show overview early for fast scanning | important | full | Section 9.2: overview scannable early | |
| PRD-058 | Scoop shows correct states and progressive feedback | important | full | Section 8.5: toggle copy states, SSE streaming, Generating state | |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | full | Section 8.4 Ask about this show seeds handoff show; Section 9.1 AskAboutCta | |
| PRD-060 | Include traditional recommendations strand | important | full | Section 9.1 RecommendationsStrand: traditional similar/recommended, no AI steering | |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | full | Section 9.1 ExploreSimilar: Get Concepts to chips to Explore Shows | |
| PRD-062 | Include streaming availability and person-linking credits | important | full | Section 9.1 Providers and CastCrew; Section 6 detail payload includes watch providers and credits | |
| PRD-063 | Gate seasons to TV and financials to movies | important | full | Section 9.2 critical states and Section 9.1 Seasons/BudgetRevenue comments | |
| PRD-064 | Keep primary actions early and page not overwhelming | important | full | Section 9.2 Busyness vs power: primary actions clustered early | |
| PRD-065 | Provide conversational Ask chat interface | important | full | Section 9.1 AskMode includes ChatThread and Composer | |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | partial | Section 8.2 Ask mode: dialogue, confident favorites, spoiler-safe shared rules | The plan covers confidence and spoiler safety, but it does not explicitly require Ask to answer directly within the first 3-5 lines. |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | Section 9.1 MentionedShowsStrip; Section 8.4 structured mentions | |
| PRD-068 | Open Detail from mentions or Search fallback | important | full | Section 8.4: resolved selectable Show, unresolved "Search for this" handoff | |
| PRD-069 | Show six random starter prompts with refresh | important | full | Section 8.4: 6 random starter prompts, refreshable endpoint | |
| PRD-070 | Summarize older turns while preserving voice | important | full | Section 8.4 conversation summarization and Section 8.2 summarizer mode | |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | full | Section 8.4: handoff show with title, year, overview, My Data | |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | full | Section 8.4 exact `{ commentary, showList }` and delimiter format | |
| PRD-073 | Retry malformed mention output once, then fallback | important | full | Section 8.4 guardrails: retry once, then plain commentary plus Search handoff | |
| PRD-074 | Redirect Ask back into TV/movie domain | important | full | Section 8.2 shared hard rule: stay within TV/movies and redirect back | |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | full | Section 8.6: taxonomy includes genre-flavor-not-label and ingredient generator mode | |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | full | Section 8.6 output contract and genericity denylist | |
| PRD-077 | Order concepts by strongest aha and varied axes | important | full | Section 8.6: diversity across axes, ordered by strength | |
| PRD-078 | Require concept selection and guide ingredient picking | important | full | Section 9.1 ExploreSimilar and Alchemy require chip selection; concept explainer guides picking | |
| PRD-079 | Return exactly five Explore Similar recommendations | important | full | Section 8.7: Explore Similar = 5; Section 10 journey repeats 5 recs | |
| PRD-080 | Support full Alchemy loop with chaining | important | full | Section 9.1 AlchemyMode includes picker, concepts, results, ChainControl | |
| PRD-081 | Clear downstream results when inputs change | important | full | Section 9.4: changing shows clears concepts/results; changing concepts clears results | |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | full | Section 8.6: multi-show shared commonality, larger pool of 12 | |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | full | Section 8.7: reasons explicitly name selected concepts, 1-3 sentences | |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | full | Section 8.8 quality checklist includes taste alignment and surprise without betrayal | |
| PRD-085 | Keep one consistent AI persona across surfaces | important | full | Section 8.2: shared base system prompt, per-surface modes layered on it | |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | full | Section 8.2 hard rules for every surface: domain, spoiler safety, real items | |
| PRD-087 | Make AI warm, joyful, and light in critique | important | full | Section 8.2 persona encodes joy-forward, warm, opinionated honesty | |
| PRD-088 | Structure Scoop as personal taste mini-review | important | full | Section 8.5: personal take, stack-up, Scoop centerpiece, fit/warnings, gut check | |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | full | Section 8.2 Ask length target and friend-in-dialogue mode | |
| PRD-090 | Feed AI the right surface-specific context inputs | important | full | Section 8.3 prompt builders assemble library, My Data, show context, concepts, turns | |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | full | Section 8.8: rubric checklist and automated real-show integrity assertion | |
| PRD-092 | Show person gallery, name, and bio | important | full | Section 9.1 PersonDetail features include Gallery and Bio | |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | full | Section 9.1 AnalyticsCharts: RatingsChart, TopGenresChart, ProjectsByYearChart | |
| PRD-094 | Group filmography by year | important | full | Section 9.1 Filmography grouped by year; Section 6 person API groups credits | |
| PRD-095 | Open Show Detail from selected credit | important | full | Section 9.1 Filmography: credit to ShowDetail | |
| PRD-096 | Include font size and Search-on-launch settings | important | full | Section 5.1 and Section 11 include `font_size` and `auto_search` | |
| PRD-097 | Support username, model, and API-key settings safely | important | full | Section 11: username, model dropdown, masked key overrides server-side | |
| PRD-098 | Export saved shows and My Data as zip | critical | full | Section 11 `/api/export` builds zip with settings and shows; journey 10 validates | |
| PRD-099 | Encode export dates using ISO-8601 | important | full | Section 11: export dates ISO-8601; Section 6 `/api/export` says all dates ISO-8601 | |

### 3. Coverage Scores

Overall score:

score = (98 full × 1.0 + 1 partial × 0.5) / 99 total_count × 100 = 99.5%

Critical:  (30 full × 1.0 + 0 partial × 0.5) / 30 critical_total × 100 = 100%  (30 of 30 critical requirements)
Important: (66 full × 1.0 + 1 partial × 0.5) / 67 important_total × 100 = 99.3%  (66.5 of 67 important requirements)
Detail:    (2 full × 1.0 + 0 partial × 0.5) / 2 detail_total × 100 = 100%  (2 of 2 detail requirements)
Overall:   99.5% (99 total requirements)

### 4. Top Gaps

1. PRD-066 | important | Answer directly with confident, spoiler-safe recommendations

   This matters because Ask can satisfy broad persona and safety rules while still feeling evasive; users need the recommendation to appear directly within the first few lines.

### 5. Coverage Narrative

#### Overall Posture

This is a strong, implementation-ready plan with unusually complete requirement coverage and one narrow Ask acceptance-criteria gap. It does not merely name the major product surfaces; it specifies persistence shape, namespace/user isolation, save semantics, AI contracts, UI composition, export behavior, and verification strategy.

#### Strength Clusters

The strongest clusters are Benchmark Runtime & Isolation, Collection Data & Persistence, Ask Chat, Concepts/Alchemy, and AI Voice/Quality. These areas are backed by concrete server APIs, database fields, pure domain functions, parser contracts, state-persistence boundaries, and test coverage rather than high-level feature promises.

#### Weakness Clusters

The only partial item is in Ask response-shape quality. The plan specifies the right persona, confidence, and spoiler rules but omits the direct-answer-within-3-5-lines acceptance condition.

#### Risk Assessment

If executed as written, the most likely failure mode would not be omitted scope; it would be an Ask response that is safe and on-brand but takes too long to make its recommendation. A QA reviewer would notice this as slightly evasive chat behavior rather than a missing feature.

#### Remediation Guidance

No new architecture is required. Add a concrete Ask acceptance check requiring a direct answer within the first 3-5 lines, then carry it into prompt tests and the AI quality harness.
