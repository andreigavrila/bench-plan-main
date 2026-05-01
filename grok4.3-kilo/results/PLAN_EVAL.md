## 1. Requirements Extraction

### Benchmark Runtime & Isolation

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

### Collection Data & Persistence

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

### App Navigation & Discover Shell

- PRD-038 | `important` | Provide filters panel and main screen destinations | `product_prd.md > 6. App Structure & Navigation`
- PRD-039 | `important` | Keep Find/Discover in persistent primary navigation | `product_prd.md > 6. App Structure & Navigation`
- PRD-040 | `important` | Keep Settings in persistent primary navigation | `product_prd.md > 6. App Structure & Navigation`
- PRD-041 | `important` | Offer Search, Ask, Alchemy discover modes | `product_prd.md > 6. App Structure & Navigation`

### Collection Home & Search

- PRD-042 | `important` | Show only library items matching active filters | `product_prd.md > 7.1 Collection Home`
- PRD-043 | `important` | Group home into Active, Excited, Interested, Others | `product_prd.md > 7.1 Collection Home`
- PRD-044 | `important` | Support All, tag, genre, decade, score, media filters | `product_prd.md > 4.5 Filters (Ways to View the Collection)`
- PRD-045 | `important` | Render poster, title, and My Data badges | `product_prd.md > 7.1 Collection Home`
- PRD-046 | `detail` | Provide empty-library and empty-filter states | `product_prd.md > 7.1 Collection Home`
- PRD-047 | `important` | Search by title or keywords | `product_prd.md > 7.2 Search (Find → Search)`
- PRD-048 | `important` | Use poster grid with collection markers | `product_prd.md > 7.2 Search (Find → Search)`
- PRD-049 | `detail` | Auto-open Search when setting is enabled | `product_prd.md > 7.2 Search (Find → Search)`
- PRD-050 | `important` | Keep Search non-AI in tone | `supporting_docs/ai_voice_personality.md > 1. Persona Summary`

### Show Detail & Relationship UX

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

### Ask Chat

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

### Concepts, Explore Similar & Alchemy

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

### AI Voice, Persona & Quality

- PRD-085 | `important` | Keep one consistent AI persona across surfaces | `supporting_docs/ai_voice_personality.md > 1. Persona Summary`
- PRD-086 | `critical` | Enforce shared AI guardrails across all surfaces | `supporting_docs/ai_prompting_context.md > 1. Shared Rules (All AI Surfaces)`
- PRD-087 | `important` | Make AI warm, joyful, and light in critique | `supporting_docs/ai_voice_personality.md > 2. Non-Negotiable Voice Pillars`
- PRD-088 | `important` | Structure Scoop as personal taste mini-review | `supporting_docs/ai_voice_personality.md > 4.1 Scoop (Show Detail "The Scoop")`
- PRD-089 | `important` | Keep Ask brisk and dialogue-like by default | `supporting_docs/ai_voice_personality.md > 4.2 Ask (Find → Ask)`
- PRD-090 | `important` | Feed AI the right surface-specific context inputs | `supporting_docs/ai_prompting_context.md > 2. Shared Inputs (Typical)`
- PRD-091 | `important` | Validate discovery with rubric and hard-fail integrity | `supporting_docs/discovery_quality_bar.md > 4. Scoring Rubric (Quick)`

### Person Detail

- PRD-092 | `important` | Show person gallery, name, and bio | `product_prd.md > 7.6 Person Detail Page`
- PRD-093 | `important` | Include ratings, genres, and projects-by-year analytics | `product_prd.md > 7.6 Person Detail Page`
- PRD-094 | `important` | Group filmography by year | `product_prd.md > 7.6 Person Detail Page`
- PRD-095 | `important` | Open Show Detail from selected credit | `product_prd.md > 7.6 Person Detail Page`

### Settings & Export

- PRD-096 | `important` | Include font size and Search-on-launch settings | `product_prd.md > 7.7 Settings & Your Data`
- PRD-097 | `important` | Support username, model, and API-key settings safely | `product_prd.md > 7.7 Settings & Your Data`
- PRD-098 | `critical` | Export saved shows and My Data as zip | `product_prd.md > 7.7 Settings & Your Data`
- PRD-099 | `important` | Encode export dates using ISO-8601 | `product_prd.md > 7.7 Settings & Your Data`

Total: 99 requirements (30 critical, 67 important, 2 detail) across 10 functional areas

## 2. Coverage Table

| PRD-ID | Requirement | Severity | Coverage | Evidence | Gap |
| ------ | ----------- | -------- | -------- | -------- | --- |
| PRD-001 | Use Next.js latest stable runtime | critical | full | 1.1 Repository & Environment: initialize Next.js 15+ | |
| PRD-002 | Use Supabase official client libraries | critical | full | 1.1 Repository & Environment: add `@supabase/supabase-js` | |
| PRD-003 | Ship `.env.example` with required variables | critical | full | 1.1 Repository & Environment: create `.env.example` with required vars | |
| PRD-004 | Ignore `.env*` secrets except example | important | partial | 1.1 Repository & Environment: `.gitignore` excludes `.env*` | The plan does not explicitly preserve `.env.example` as the one allowed exception, so the repo-hygiene rule is only partially specified. |
| PRD-005 | Configure build through env without code edits | critical | full | 1.1 Repository & Environment; 10. Success Criteria: run after filling env vars | |
| PRD-006 | Keep secrets out of repo and server-only | critical | full | 1.1 Repository & Environment: service-role key server-only; never commit keys | |
| PRD-007 | Provide app, test, reset command scripts | critical | full | 1.1 Repository & Environment: `dev`, `test`, `test:reset`, `db:migrate` scripts | |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | 1.2 Database Foundation: `supabase/migrations/`, seed script, forward-only migrations | |
| PRD-009 | Use one stable namespace per build | critical | full | 1.1 Repository & Environment: stable `NAMESPACE_ID` | |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | 1.2 Database Foundation: partitioning rule and namespace-scoped `test:reset` | |
| PRD-011 | Attach every user record to `user_id` | critical | full | 1.2 Database Foundation: required `user_id` on user-owned rows | |
| PRD-012 | Partition persisted data by namespace and user | critical | full | 1.2 Database Foundation: every query/mutation filters `namespace_id` + `user_id` | |
| PRD-013 | Support documented dev auth injection, prod-gated | important | partial | 2.1 Dev Identity Injection: `X-User-Id` or env injection, dev-only switcher, prod gating | The mechanism and gating are planned, but the plan does not make the documentation deliverable for benchmark operators explicit. |
| PRD-014 | Real OAuth later needs no schema redesign | important | full | 2.1 Dev Identity Injection: auth abstraction with no schema impact | |
| PRD-015 | Keep backend as persisted source of truth | critical | full | 5.2 Settings & Metadata; 7. State Management: synced server data plus server mutations | |
| PRD-016 | Make client cache safe to discard | critical | partial | 7. State Management, Caching & Performance: React Query/SWR cache and transient re-fetches | The plan treats cache as ephemeral, but it never states a concrete local-clear/reinstall recovery contract or verification for saved user data. |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | full | 1.1 Repository & Environment: Docker optional, hosted Supabase primary path | |
| PRD-018 | Overlay saved user data on every show appearance | critical | partial | 5.1 Show Storage & Merge Logic: `getById` returns user-overlaid version | The plan covers overlay in storage reads and several surfaces, but it does not define a universal rendering rule for every list, recommendation, and AI mention surface. |
| PRD-019 | Support visible statuses plus hidden `Next` | important | full | 10. Open Questions Addressed: `Next` in data model but UI-hidden | |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | full | 6.4 Show Detail: Interested/Excited map to `Later + Interest` | |
| PRD-021 | Support free-form multi-tag personal tag library | important | full | 6.1 Navigation & Layout: per-tag filters; 6.4 Show Detail: tag chips + picker | |
| PRD-022 | Define collection membership by assigned status | critical | full | 5.1 Show Storage & Merge Logic: collection membership is `myStatus != null` | |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | full | 5.1 Show Storage & Merge Logic: auto-save triggers cover all four actions | |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | 5.1 Show Storage & Merge Logic: default `Later + Interested`, rating exception to `Done` | |
| PRD-025 | Removing status deletes show and all My Data | critical | full | 5.1 Show Storage & Merge Logic: `remove(showId)` deletes row and clears My Data | |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | full | 5.1 Show Storage & Merge Logic: merge policy preserves My Data and refreshes catalog fields | |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | 5.1 Show Storage & Merge Logic: per-field timestamps in merge logic | |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | full | 5.1 Show Storage & Merge Logic: recent-first sort, conflict resolution, freshness | |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | full | 4.2 Feature-Specific AI Contracts: Scoop cache 4h, persist only in collection | |
| PRD-030 | Keep Ask and Alchemy state session-only | important | full | 4.2 Feature-Specific AI Contracts: chat and Alchemy clear on leave/reset | |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | full | 4.2 Feature-Specific AI Contracts: extId/title resolution with Search fallback | |
| PRD-032 | Show collection and rating tile indicators | important | full | 6.2 Collection Home: tiles include in-collection and rating badges | |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | full | 5.1 Show Storage & Merge Logic; 5.2 Settings & Metadata: timestamp conflict handling and synced settings | |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | full | 1.2 Database Foundation; 8. Testing Strategy: upgrade path and data-continuity tests | |
| PRD-035 | Persist synced settings, local settings, UI state | important | full | 5.2 Settings & Metadata: cloud settings, local settings, UI state | |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | full | 1.2 Database Foundation: JSONB `providerData`; 3.1 Catalog integration transient detail fields | |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | full | 5.1 Show Storage & Merge Logic: `selectFirstNonEmpty`, timestamp-wins, `detailsUpdateDate` | |
| PRD-038 | Provide filters panel and main screen destinations | important | full | 6.1 Navigation & Layout: sidebar filters plus main content destinations | |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | full | 6.1 Navigation & Layout: persistent Find hub | |
| PRD-040 | Keep Settings in persistent primary navigation | important | full | 6.1 Navigation & Layout: persistent Settings entry | |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | 6.3 Find Hub: Search, Ask, Alchemy mode switcher | |
| PRD-042 | Show only library items matching active filters | important | full | 6.2 Collection Home: filtered sections with media toggle and filter chips | |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | 6.2 Collection Home: explicit four-way grouping | |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | full | 6.1 Navigation & Layout: all, tag, genre, decade, score, media filters | |
| PRD-045 | Render poster, title, and My Data badges | important | full | 6.2 Collection Home: poster, title, in-collection badge, rating badge | |
| PRD-046 | Provide empty-library and empty-filter states | detail | full | 6.2 Collection Home: empty library prompt and no-results state | |
| PRD-047 | Search by title or keywords | important | full | 6.3 Find Hub Search: input to live catalog results | |
| PRD-048 | Use poster grid with collection markers | important | full | 6.3 Find Hub Search: results grid with in-collection mark | |
| PRD-049 | Auto-open Search when setting is enabled | detail | full | 6.3 Find Hub Search and 6.6 Settings: Search-on-launch setting | |
| PRD-050 | Keep Search non-AI in tone | important | full | 6.3 Find Hub Search is planned as a straightforward catalog search surface distinct from Ask/Alchemy AI modes | |
| PRD-051 | Preserve Show Detail narrative section order | important | full | 6.4 Show Detail: preserved 12-step narrative hierarchy | |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | full | 6.4 Show Detail: trailers inline/playable with graceful fallback | |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | full | 6.4 Show Detail: core facts and community score bar near the top | |
| PRD-054 | Place status/interest controls in toolbar | important | full | 6.4 Show Detail: My Relationship toolbar with status chips | |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | 6.4 Show Detail: tags trigger auto-save | |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | 6.4 Show Detail: rating slider auto-saves unsaved show to `Done` | |
| PRD-057 | Show overview early for fast scanning | important | full | 6.4 Show Detail: overview appears before deeper metadata | |
| PRD-058 | Scoop shows correct states and progressive feedback | important | full | 4.2 Feature-Specific AI Contracts; 6.4 Show Detail: 4h freshness, stream while generating | |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | full | 6.4 Show Detail: Ask CTA hands off seeded show context | |
| PRD-060 | Include traditional recommendations strand | important | full | 6.4 Show Detail: traditional recs strand | |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | full | 6.4 Show Detail: Get Concepts, select chips, Explore Shows | |
| PRD-062 | Include streaming availability and person-linking credits | important | full | 6.4 Show Detail: Stream It providers and Cast/Crew links to Person Detail | |
| PRD-063 | Gate seasons to TV and financials to movies | important | full | 6.4 Show Detail: seasons for TV, Budget/Revenue for movies | |
| PRD-064 | Keep primary actions early and page not overwhelming | important | partial | 6.4 Show Detail: early toolbar/actions and ordered narrative hierarchy | The plan keeps key actions near the top, but it does not convert the busyness-vs-power requirement into concrete density or clutter-control acceptance criteria. |
| PRD-065 | Provide conversational Ask chat interface | important | full | 6.3 Find Hub Ask: chat UI with messages and input | |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | full | 4.1 Provider & Prompt Abstraction: Ask prompt plus shared guardrails | |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | 6.3 Find Hub Ask: horizontal strip of selectable show tiles | |
| PRD-068 | Open Detail from mentions or Search fallback | important | full | 6.3 Find Hub Ask: mention tap opens Detail or Search handoff | |
| PRD-069 | Show six random starter prompts with refresh | important | full | 6.3 Find Hub Ask: six random starter prompts, refreshable | |
| PRD-070 | Summarize older turns while preserving voice | important | full | 4.1 Provider & Prompt Abstraction; 6.3 Find Hub Ask: summarize history after ~10 turns | |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | full | 6.3 Find Hub Ask: Detail handoff seeds Ask context | |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | full | 4.1 Provider & Prompt Abstraction: exact `{commentary, showList}` structured contract | |
| PRD-073 | Retry malformed mention output once, then fallback | important | full | 4.1 Provider & Prompt Abstraction: retry on parse failure, then fallback | |
| PRD-074 | Redirect Ask back into TV/movie domain | important | full | 4.1 Provider & Prompt Abstraction: domain enforcement to TV/movies | |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | full | 4.1 Provider & Prompt Abstraction; 6.3 Alchemy UX: ingredient-oriented concept framing | |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | full | 4.1 Provider & Prompt Abstraction: bullet-only, 1-3 word, evocative concepts | |
| PRD-077 | Order concepts by strongest aha and varied axes | important | full | 4.1 Provider & Prompt Abstraction: diverse axes ordered by strength | |
| PRD-078 | Require concept selection and guide ingredient picking | important | full | 6.3 Alchemy UX: select 1-8 concept chips with ingredient-picking hints | |
| PRD-079 | Return exactly five Explore Similar recommendations | important | full | 4.2 Feature-Specific AI Contracts: Explore returns 5 recs | |
| PRD-080 | Support full Alchemy loop with chaining | important | full | 6.3 Find Hub Alchemy: select, conceptualize, alchemize, More Alchemy chain | |
| PRD-081 | Clear downstream results when inputs change | important | full | 6.3 Find Hub Alchemy: changing shows clears concepts/results | |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | partial | 4.2 Feature-Specific AI Contracts: multi-show concepts are shared for Alchemy | The plan covers shared concept generation, but it never specifies returning a larger option pool for multi-show inputs than for single-show Explore Similar. |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | full | 4.2 Feature-Specific AI Contracts: reasons name matching concepts | |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | full | 4.2 Feature-Specific AI Contracts; 8. Testing Strategy: surprise-without-betrayal quality bar | |
| PRD-085 | Keep one consistent AI persona across surfaces | important | full | 4.1 Provider & Prompt Abstraction: consistent system persona injection | |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | full | 4.1 Provider & Prompt Abstraction: shared domain, spoiler, honesty, specificity guardrails | |
| PRD-087 | Make AI warm, joyful, and light in critique | important | full | 4.1 Provider & Prompt Abstraction and 4.2 AI contracts inherit `ai_voice_personality.md` voice rules | |
| PRD-088 | Structure Scoop as personal taste mini-review | important | full | 4.1 Provider & Prompt Abstraction: Scoop prompt as structured mini-blog | |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | full | 4.1 Provider & Prompt Abstraction: Ask prompt in conversational friend mode | |
| PRD-090 | Feed AI the right surface-specific context inputs | important | full | 4.1 Provider & Prompt Abstraction: library, show context, concepts, session history | |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | full | 4.2 Feature-Specific AI Contracts; 8. Testing Strategy: quality rubric with real-show integrity as non-negotiable | |
| PRD-092 | Show person gallery, name, and bio | important | full | 6.5 Person Detail: image/gallery, name, bio | |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | full | 6.5 Person Detail: avg ratings, top genres, projects-by-year charts | |
| PRD-094 | Group filmography by year | important | full | 6.5 Person Detail: filmography grouped by year | |
| PRD-095 | Open Show Detail from selected credit | important | full | 6.5 Person Detail: clickable credits open Show Detail | |
| PRD-096 | Include font size and Search-on-launch settings | important | full | 6.6 Settings: font size and Search-on-launch controls | |
| PRD-097 | Support username, model, and API-key settings safely | important | full | 6.6 Settings: username, model selector, API key inputs with env fallback and key-safety notes | |
| PRD-098 | Export saved shows and My Data as zip | critical | full | 6.6 Settings: Export My Data produces `.zip` of shows and metadata | |
| PRD-099 | Encode export dates using ISO-8601 | important | full | 5.1 Show Storage & Merge Logic: ISO timestamps; 6.6 Settings export follows ISO-8601 | |

## 3. Coverage Scores

Overall score:

```text
score = (93 x 1.0 + 6 x 0.5) / 99 x 100 = 96.97%
```

Score by severity tier:

```text
Critical:  (28 x 1.0 + 2 x 0.5) / 30 x 100 = 96.67%  (29 of 30 critical requirements)
Important: (63 x 1.0 + 4 x 0.5) / 67 x 100 = 97.01%  (65 of 67 important requirements)
Detail:    (2 x 1.0 + 0 x 0.5) / 2 x 100 = 100.00%  (2 of 2 detail requirements)
Overall:   96.97% (99 total requirements)
```

## 4. Top Gaps

1. PRD-018 | `critical` | Overlay saved user data on every show appearance
Why it matters: the plan does not lock in a cross-surface overlay contract, so search results, AI mention strips, and recommendation rails could show inconsistent status/rating/tag state for the same show.

2. PRD-016 | `critical` | Make client cache safe to discard
Why it matters: without an explicit recovery contract and validation, the implementation can drift into relying on local cache for correctness, which would surface as apparent data loss after storage clears or reinstalls.

3. PRD-064 | `important` | Keep primary actions early and page not overwhelming
Why it matters: the plan preserves section order, but not the density-control rules that keep the Detail page usable; a rebuild could technically include every section while still feeling cluttered and fatiguing.

4. PRD-082 | `important` | Generate shared multi-show concepts with larger option pool
Why it matters: if Alchemy uses the same concept count/shape as single-show Explore Similar, multi-input discovery will feel shallow and produce fewer distinct steering options.

5. PRD-013 | `important` | Support documented dev auth injection, prod-gated
Why it matters: benchmark execution depends on operators knowing exactly how to inject identity safely; if that path is not explicitly documented, setup friction and production-gating mistakes become more likely.

## 5. Coverage Narrative

#### Overall Posture

This is a strong plan with minor but real specification gaps. It covers the architecture, persistence model, main UX surfaces, AI contracts, and benchmark isolation model in concrete terms, but it is slightly less precise on a few cross-surface consistency and experience-quality requirements than on the core feature buildout.

#### Strength Clusters

The plan is strongest in Benchmark Runtime & Isolation, Collection Data & Persistence, Ask Chat, and the broader discovery stack around Explore Similar and Alchemy. It also does a good job preserving the Show Detail information architecture, specifying the Supabase-backed data model, and translating the AI prompt/persona documents into implementation-facing contracts.

#### Weakness Clusters

The gaps are not random. They cluster around contract quality rather than feature absence: benchmark-operability details (`.env.example` exception handling and explicit dev-auth documentation), cross-surface consistency rules (user-overlay everywhere, disposable cache semantics), and a few nuanced UX requirements where the PRD asks for qualitative behavior rather than just feature presence (Detail page busyness control, larger multi-show concept pools).

#### Risk Assessment

If this plan were executed as-is, the first QA-visible issues would likely be inconsistency rather than missing screens. The most probable failure mode is a polished build that still shows uneven My Data overlays across recommendation/search/AI surfaces, coupled with a Detail page that includes the right sections but feels denser than intended. On the benchmark side, cache-clearing and dev-auth setup could also expose avoidable operational regressions.

#### Remediation Guidance

The remaining planning work is mostly about tightening contracts, not adding whole new modules. Add explicit acceptance criteria for universal user-overlay rendering, state what must survive local cache clears and how it is verified, make the dev-auth injection workflow a named documentation deliverable, and translate qualitative UX/AI notes such as Detail page busyness control and larger multi-show concept pools into concrete planning constraints.
