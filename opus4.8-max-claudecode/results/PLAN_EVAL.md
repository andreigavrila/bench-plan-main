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
| PRD-001 | Use Next.js latest stable runtime | critical | full | §3 Technology Stack: "Next.js (latest stable), App Router, TypeScript" | |
| PRD-002 | Use Supabase official client libraries | critical | full | §3 Technology Stack: "Supabase (Postgres) via official `@supabase/supabase-js`" | |
| PRD-003 | Ship `.env.example` with required variables | critical | full | §14 Environment & Developer Experience lists `.env.example` variables and comments | |
| PRD-004 | Ignore `.env*` secrets except example | important | full | §14: "`.gitignore` excludes `.env*` except `.env.example`" | |
| PRD-005 | Configure build through env without code edits | critical | full | §14: "Runs by filling env only — no source edits" | |
| PRD-006 | Keep secrets out of repo and server-only | critical | full | §15 Security & Secrets: browser anon only, service/catalog/AI keys server-only | |
| PRD-007 | Provide app, test, reset command scripts | critical | full | §14 scripts: `npm run dev`, `npm test`, `npm run test:reset` | |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | §6.6: `supabase/migrations/*.sql`, optional seed, deterministic fresh DB | |
| PRD-009 | Use one stable namespace per build | critical | full | §7: "`NAMESPACE_ID` env var — one stable value per build" | |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | §7 destructive reset deletes rows where `namespace_id = $NAMESPACE_ID` | |
| PRD-011 | Attach every user record to `user_id` | critical | full | §6.2: all user-owned tables carry `namespace_id` + `user_id` | |
| PRD-012 | Partition persisted data by namespace and user | critical | full | §7: "Effective partition = `(namespace_id, user_id)` everywhere" | |
| PRD-013 | Support documented dev auth injection, prod-gated | important | full | §7 dev/test accepts `X-User-Id` or selector, gated by `APP_MODE` | |
| PRD-014 | Real OAuth later needs no schema redesign | important | full | §7 production auth wiring uses existing `user_id`; no schema redesign | |
| PRD-015 | Keep backend as persisted source of truth | critical | full | §2 principle 2 and §6.2 server-side settings mirror | |
| PRD-016 | Make client cache safe to discard | critical | full | §4 browser cache marked disposable; §20 clearing client cache loses nothing | |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | full | §3 and §6.6 state hosted path and no Docker needed | |
| PRD-018 | Overlay saved user data on every show appearance | critical | full | §2 principle 1 and §10 `applyOverlay(show)` used by tiles, search, AI recs, detail | |
| PRD-019 | Support visible statuses plus hidden `Next` | important | full | §11.2 folds hidden `Next` into Others; §18 keeps `Next` in model hidden in UI | |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | full | §10: Interested/Excited chips set `my_status=Later` and `my_interest` | |
| PRD-021 | Support free-form multi-tag personal tag library | important | full | §6.2 `my_tags text[]`; §11.1 one tag filter per tag; §11.4 tag chips + picker | |
| PRD-022 | Define collection membership by assigned status | critical | full | §10: "Collection membership = row exists with non-nil `my_status`" | |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | full | §10 `applySaveTriggers` lists status, Interested/Excited, rating, tag | |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | §10 defaults Later/Interested with rating exception to Done | |
| PRD-025 | Removing status deletes show and all My Data | critical | full | §10 removal deletes row and clears status, interest, tags, rating, Scoop | |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | full | §6.4: re-add preserves My Data + Scoop and refreshes public metadata | |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | §6.2 `*_update_date` per My Data field; §10 stamps every write | |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | full | §10 timestamps used for recency sorting, sync conflict resolution, Scoop freshness | |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | full | §9.1 Scoop persists only if in collection; 4h freshness | |
| PRD-030 | Keep Ask and Alchemy state session-only | important | full | §11.5 Ask session-only; §11.6 Alchemy session-only | |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | full | §8 recommendation resolver maps title/externalId/mediaType to real selectable Show | |
| PRD-032 | Show collection and rating tile indicators | important | full | §10 tile indicators and §11.2 tiles show My Data badges | |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | partial | §6.4 timestamp sync conflict resolution; §6.2 synced settings tables | The plan covers sync consistency and conflict resolution but does not specify duplicate detection or transparent duplicate merging. |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | full | §6.5 migration chain carries statuses, interest, tags, rating, and Scoop forward | |
| PRD-035 | Persist synced settings, local settings, UI state | important | full | §6.2 `cloud_settings` and `user_settings` include synced, local, and UI state fields | |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | full | §6.1 transient details never persisted; §8 provider IDs by region only | |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | full | §6.4 implements `selectFirstNonEmpty`, My field timestamp resolution, update dates | |
| PRD-038 | Provide filters panel and main screen destinations | important | full | §11.1 filters/navigation panel and Home, Detail, Find, Person, Settings destinations | |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | full | §11.1 persistent Find/Discover entry point | |
| PRD-040 | Keep Settings in persistent primary navigation | important | full | §11.1 persistent Settings entry point | |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | §5 `find/page.tsx` as Search/Ask/Alchemy; §11.3, §11.5, §11.6 | |
| PRD-042 | Show only library items matching active filters | important | full | §11.2 media toggle applied on top of filters; §11.1 filter panel | |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | §11.2 grouping order Active, Excited, Interested, Others | |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | full | §11.1 All, tag, genre, decade, community-score; §11.2 media toggle | |
| PRD-045 | Render poster, title, and My Data badges | important | full | §11.2 tiles: poster, title, My Data badges | |
| PRD-046 | Provide empty-library and empty-filter states | detail | full | §11.2 empty library and no-results filter states | |
| PRD-047 | Search by title or keywords | important | full | §11.3: "Text search by title/keywords" | |
| PRD-048 | Use poster grid with collection markers | important | full | §11.3: poster grid with in-collection items marked | |
| PRD-049 | Auto-open Search when setting is enabled | detail | full | §11.3 auto-open on launch when `auto_search` enabled | |
| PRD-050 | Keep Search non-AI in tone | important | full | §11.3: "No AI voice"; §9.2 Search has no AI voice | |
| PRD-051 | Preserve Show Detail narrative section order | important | full | §11.4 lists the required section order explicitly | |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | full | §11.4 header media carousel prioritizes motion with poster/logo fallback | |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | full | §11.4 item 2 core facts: year, runtime or seasons/episodes, community score | |
| PRD-054 | Place status/interest controls in toolbar | important | full | §11.4 Toolbar: Status/Interest chips not in scroll body | |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | §11.4 My Tags chips + picker auto-save Later+Interested | |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | §11.4 Toolbar My Rating auto-saves unsaved show as Done | |
| PRD-057 | Show overview early for fast scanning | important | full | §11.4 overview is item 4 before downstream recs and long-tail info | |
| PRD-058 | Scoop shows correct states and progressive feedback | important | full | §11.4 Scoop states and streaming; §9.1 "Generating...", never blank | |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | full | §11.4 Ask CTA enters Ask seeded with show context | |
| PRD-060 | Include traditional recommendations strand | important | full | §11.4 item 7 traditional recommendations strand | |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | full | §11.4 Explore Similar: Get Concepts -> select -> Explore Shows | |
| PRD-062 | Include streaming availability and person-linking credits | important | full | §11.4 items 9 and 10: Stream It and Cast & Crew to Person Detail | |
| PRD-063 | Gate seasons to TV and financials to movies | important | full | §11.4 items 11-12 and critical states gate seasons/financials | |
| PRD-064 | Keep primary actions early and page not overwhelming | important | full | §11.4 primary actions clustered early; long-tail info down-page/full-bleed | |
| PRD-065 | Provide conversational Ask chat interface | important | full | §11.5 Chat UI with user/assistant turns | |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | full | §9.1 Ask friend-in-dialogue with confident picks; §9 shared spoiler-safe guardrails | |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | §11.5 mentioned-shows strip parses `showList` into horizontal strip | |
| PRD-068 | Open Detail from mentions or Search fallback | important | full | §11.5 tap mention opens Detail or Search handoff if mapping fails | |
| PRD-069 | Show six random starter prompts with refresh | important | full | §11.5 welcome: 6 random starter prompts with refresh | |
| PRD-070 | Summarize older turns while preserving voice | important | full | §9.1 Summarize route preserves persona/tone after ~10 messages | |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | full | §11.5 Ask-about-a-show variant seeded with handoff show context | |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | full | §9.1 Ask structured `{ commentary, showList }` and exact `Title::externalId::mediaType;;...` format | |
| PRD-073 | Retry malformed mention output once, then fallback | important | full | §9.3 parse fails -> retry once -> fallback to commentary + Search handoff | |
| PRD-074 | Redirect Ask back into TV/movie domain | important | full | §9 shared guardrails redirect out-of-domain requests | |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | full | §1.1 "Vibes over genres"; §9.1 concepts are evocative ingredients | |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | full | §9.1 Concepts output contract: bullet list only, 1-3 words, reject generic | |
| PRD-077 | Order concepts by strongest aha and varied axes | important | full | §9.1 Concepts: diverse axes and ordered by strongest "aha" | |
| PRD-078 | Require concept selection and guide ingredient picking | important | full | §11.4 and §11.6 require selection; §11.4 copy implies picking ingredients | |
| PRD-079 | Return exactly five Explore Similar recommendations | important | full | §9.1 Concept recs: Explore Similar = 5 recs | |
| PRD-080 | Support full Alchemy loop with chaining | important | full | §11.6 full flow through More Alchemy chaining | |
| PRD-081 | Clear downstream results when inputs change | important | full | §11.6 backtracking clears downstream results | |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | full | §11.6 shared multi-show concepts, larger pool; §9.1 multi-show shared across inputs | |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | full | §9.1 concept recs name which concepts align | |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | full | §9.3 discovery rubric harness; §9.1 allows classics/hidden gems with concept-grounded reasons | |
| PRD-085 | Keep one consistent AI persona across surfaces | important | full | §9 states one consistent persona with surface modes | |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | full | §9 shared guardrails for every surface | |
| PRD-087 | Make AI warm, joyful, and light in critique | important | full | §9.2 warm, joy-forward, opinionated, spoiler-safe tone sliders | |
| PRD-088 | Structure Scoop as personal taste mini-review | important | full | §9.1 Scoop mini blog-post with personal take, stack-up, Scoop, warnings, verdict | |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | full | §9.1 Ask: friend-in-dialogue, 1-3 tight paragraphs | |
| PRD-090 | Feed AI the right surface-specific context inputs | important | full | §9 shared context inputs: library/My Data, current show, selected concepts, turns | |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | full | §9.3 quality check encodes rubric and real-show integrity hard-fail | |
| PRD-092 | Show person gallery, name, and bio | important | full | §11.8 image gallery, name, bio | |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | full | §11.8 analytics charts: average ratings, top genres, projects-by-year | |
| PRD-094 | Group filmography by year | important | full | §11.8 filmography grouped by year | |
| PRD-095 | Open Show Detail from selected credit | important | full | §11.8 select a credit -> Show Detail | |
| PRD-096 | Include font size and Search-on-launch settings | important | full | §11.9 App settings: font size and Search-on-launch | |
| PRD-097 | Support username, model, and API-key settings safely | important | full | §11.9 username, AI provider key, model, catalog key; §15 masked/server-only key handling | |
| PRD-098 | Export saved shows and My Data as zip | critical | full | §11.9 Export My Data -> `.zip` containing JSON of saved shows + My Data | |
| PRD-099 | Encode export dates using ISO-8601 | important | full | §11.9 dates ISO-8601; §13 export zip shape + ISO dates test | |

### 3. Coverage Scores

Overall score:

```
score = (98 × 1.0 + 1 × 0.5) / 99 × 100 = 99.5%
```

Critical:  (30 × 1.0 + 0 × 0.5) / 30 × 100 = 100.0%  (30 of 30 critical requirements)
Important: (66 × 1.0 + 1 × 0.5) / 67 × 100 = 99.3%  (66.5 of 67 important requirements)
Detail:    (2 × 1.0 + 0 × 0.5) / 2 × 100 = 100.0%  (2 of 2 detail requirements)
Overall:   99.5% (99 total requirements)

### 4. Top Gaps

1. PRD-033 | important | Sync libraries/settings consistently and merge duplicates

The plan defines timestamp-based sync conflict handling and settings persistence, but it does not explicitly plan duplicate item detection and transparent duplicate merging. Without that, cross-device or migration flows could leave duplicate saved shows in the library, making filters, collection counts, and user edits inconsistent.

### 5. Coverage Narrative

#### Overall Posture

This is a very strong implementation plan with one narrow but real planning gap. It covers the benchmark runtime, identity isolation, data model, collection behaviors, AI contracts, detail-page UX, and export path with concrete mechanisms rather than generic promises.

#### Strength Clusters

Coverage is strongest in Benchmark Runtime & Isolation, Collection Data & Persistence, Show Detail & Relationship UX, Ask Chat, and Concepts/Alchemy. The plan repeatedly turns PRD semantics into named modules, routes, tables, constants, and tests, which makes the implementation path clear.

#### Weakness Clusters

The only weakness cluster is sync integrity at the edge of Collection Data & Persistence. The plan handles per-field timestamp conflict resolution, but it treats duplicate library rows as an implied consequence of merge logic instead of naming duplicate detection and transparent merge as a required behavior.

#### Risk Assessment

If executed as-is, the most likely visible failure would appear in synced or upgraded libraries: the same show could appear more than once or carry split My Data across duplicate records. QA would likely catch this through cross-device sync, re-add, or migration scenarios rather than through ordinary single-session use.

#### Remediation Guidance

The plan needs a small additional data-integrity planning section, not a broad redesign. It should specify canonical duplicate keys, when duplicate detection runs, how My Data conflicts are merged by timestamp, and tests that prove duplicate records collapse without losing status, interest, tags, rating, or Scoop.
