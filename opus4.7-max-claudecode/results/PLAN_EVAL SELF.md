# Plan Evaluation — Personal TV/Movie Companion

Evaluated against the canonical requirements catalog at `evaluator/requirements_catalog_v1.md`, using the PRD files in `docs/prd/` as the semantic source of truth, and the implementation plan at `results/PLAN.md`.

---

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
| PRD-001 | Use Next.js latest stable runtime | critical | full | §1 Technology Choices: "Next.js (latest stable), App Router, TypeScript" | |
| PRD-002 | Use Supabase official client libraries | critical | full | §1: "@supabase/supabase-js (browser, anon key) + @supabase/ssr for Next.js server actions/route handlers" | |
| PRD-003 | Ship `.env.example` with required variables | critical | full | §3 Environment Variables enumerates full `.env.example` block | |
| PRD-004 | Ignore `.env*` secrets except example | important | full | §3: "`.gitignore` excludes `.env*` except `.env.example`" | |
| PRD-005 | Configure build through env without code edits | critical | full | §3: "the build must run purely by filling env vars; no secrets are committed" | |
| PRD-006 | Keep secrets out of repo and server-only | critical | full | §1, §3, §13: anon key in browser, service-role key server-only, `.gitignore` excludes secrets | |
| PRD-007 | Provide app, test, reset command scripts | critical | full | §11 Scripts & One-Command DX: dev / test / test:reset / db:migrate / db:seed | |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | §11 db:migrate; §2 `supabase/migrations/*.sql` and `seed.sql` | |
| PRD-009 | Use one stable namespace per build | critical | full | §4.1: "`NAMESPACE_ID` env var resolves at server startup… every persisted row carries a `namespace_id` column" | |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | §4.1 RLS gating + §11: "`test:reset` never touches rows outside the current namespace" | |
| PRD-011 | Attach every user record to `user_id` | critical | full | §4.2 + §5.4–§5.7: every user-scoped table keyed by `user_id` | |
| PRD-012 | Partition persisted data by namespace and user | critical | full | §4.2: "Effective partition: `(namespace_id, user_id)`. RLS combines both" | |
| PRD-013 | Support documented dev auth injection, prod-gated | important | full | §4.2 X-User-Id / DEV_DEFAULT_USER_ID; "compiled out when APP_ENV=production" | |
| PRD-014 | Real OAuth later needs no schema redesign | important | full | §4.3: `users` table already includes `auth_provider`/`provider_user_id`; "no schema redesign" | |
| PRD-015 | Keep backend as persisted source of truth | critical | full | §0.3: "Backend is source of truth. Clients may cache but must tolerate full cache wipes" | |
| PRD-016 | Make client cache safe to discard | critical | full | §0.3: "tolerate full cache wipes. No offline-first requirement." | |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | full | §1: "Containers — None required; Docker is strictly optional" | |
| PRD-018 | Overlay saved user data on every show appearance | critical | full | §0.1: "User overlay wins everywhere. Wherever a show appears, the saved my* data is authoritative" | |
| PRD-019 | Support visible statuses plus hidden `Next` | important | full | §5.4 `my_status` check includes `'next'` alongside the visible statuses | |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | full | §6.1 `onSelectInterest` returns `{my_status:'later', my_interest, saved}` | |
| PRD-021 | Support free-form multi-tag personal tag library | important | full | §5.4 `my_tags text[]` + §9.6 tag chips + TagPicker component | |
| PRD-022 | Define collection membership by assigned status | critical | full | §0.2 + §5.4: "Collection membership = my_status is not null" | |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | full | §6.1 enumerates all four implicit save handlers | |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | §0.2 + §6.1: rating defaults to Done; tagging/interest default to Later+Interested | |
| PRD-025 | Removing status deletes show and all My Data | critical | full | §6.1 `onClearStatus` + §10 `DELETE /api/collection/[showId]`; remove-confirmation in §9.3 | |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | full | §6.2 merge logic: timestamp-LWW preserves my_*; selectFirstNonEmpty refreshes public fields | |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | §5.4 lists `my_status_update`, `my_interest_update`, `my_tags_update`, `my_score_update`, `ai_scoop_update` | |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | partial | §6.2 timestamp-LWW for sync; §8.5 4h freshness for Scoop | Sorting use case (recently-updated-first) is not explicitly addressed in Home or any view |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | full | §8.5 + §10: "persisted iff my_status not null; respects 4-hour freshness" | |
| PRD-030 | Keep Ask and Alchemy state session-only | important | full | §8.5 table marks both Alchemy and Ask as "session only" | |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | full | §0.6 + §8.3 parser resolves via `CatalogProvider.getShow`, falls back to title match, then non-interactive | |
| PRD-032 | Show collection and rating tile indicators | important | full | §9.9 `<ShowTile>` renders `my_status` badge + `my_score` badge | |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | partial | §6.2 timestamp-LWW; §5.5 `cloud_settings` table | Cross-device sync mechanism is not described; duplicate detection / transparent merge of duplicates not addressed |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | partial | §5.8 `app_metadata.data_model_version` placeholder exists | No migration upgrade path or data-preservation strategy is described; only a version column is added |
| PRD-035 | Persist synced settings, local settings, UI state | important | full | §5.5 cloud_settings, §5.6 local_settings, §5.7 ui_state all defined | |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | full | §5.3 `provider_data jsonb`; §7.2 lists transient fetches (cast/crew/seasons/etc.) | |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | full | §6.2: selectFirstNonEmpty + timestamp-LWW + details_update_date set to now; creation_date preserved | |
| PRD-038 | Provide filters panel and main screen destinations | important | full | §9.1: "App Router layout with Filters sidebar + main area" + Home/Detail/Find/Person/Settings routes in §2 | |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | full | §9.1: "Persistent entry points: Find (Search/Ask/Alchemy switcher) and Settings" | |
| PRD-040 | Keep Settings in persistent primary navigation | important | full | §9.1 same persistent-entry-points statement | |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | §2 routes `/find/search`, `/find/ask`, `/find/alchemy`; §9.1 mode switcher | |
| PRD-042 | Show only library items matching active filters | important | full | §6.3 + §9.2 grouping pipes through filter evaluation | |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | §6.4 explicit ordering: Active → Excited → Interested → Other (Wait/Quit/Done/Later-no-interest) | |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | full | §6.3 enumerates `all`, `genre`, `myStatus`, `communityScore`, `decade`, `myTag` + media-type toggle | |
| PRD-045 | Render poster, title, and My Data badges | important | full | §9.2 + §9.9 `<ShowTile>` | |
| PRD-046 | Provide empty-library and empty-filter states | detail | full | §6.4 + §9.2: "Empty states per §7.1" | |
| PRD-047 | Search by title or keywords | important | full | §9.3: "Text input → calls /api/catalog/search" | |
| PRD-048 | Use poster grid with collection markers | important | full | §9.3: "Poster grid with in-collection badges (join with show_user_data server-side)" | |
| PRD-049 | Auto-open Search when setting is enabled | detail | full | §9.3: "autoSearch local setting auto-focuses search on launch if true" | |
| PRD-050 | Keep Search non-AI in tone | important | full | §0.5: "Search has no AI voice" | |
| PRD-051 | Preserve Show Detail narrative section order | important | full | §9.6 lists 12 sections in the spec's exact order | |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | full | §9.6: "Header media carousel (trailer-priority, poster fallback)" | |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | full | §9.6 step 2: "Core facts + community score" | |
| PRD-054 | Place status/interest controls in toolbar | important | full | §9.6: "Toolbar hosts status chips + rating" | |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | §6.1 `onAddTagUnsaved` defaults to `later` + `interested` | |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | §6.1 `onRateUnsaved` defaults `my_status:'done'` if not previously saved | |
| PRD-057 | Show overview early for fast scanning | important | full | §9.6 step 4 places Overview before downstream sections | |
| PRD-058 | Scoop shows correct states and progressive feedback | important | partial | §8.5 streaming + 4h freshness; §9.6 includes Scoop toggle/stream | The three labelled UX states ("Give me the scoop!" / "Show the scoop" / "The Scoop"), and the explicit "Generating…" state, are not specified |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | full | §8.2 + §9.4: Ask-about-this-show "seeded with current show context (title, genres, overview, user's rating/status if saved)" | |
| PRD-060 | Include traditional recommendations strand | important | full | §9.6 step 7: "Recommendations strand" | |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | full | §9.6 step 8: "Get Concepts → select → Explore Shows" | |
| PRD-062 | Include streaming availability and person-linking credits | important | full | §9.6 steps 9 + 10 cover streaming providers and Cast/Crew strands → Person Detail | |
| PRD-063 | Gate seasons to TV and financials to movies | important | full | §9.6 steps 11–12: "Seasons (TV only). Budget/Revenue (movies)" | |
| PRD-064 | Keep primary actions early and page not overwhelming | important | partial | §9.6 puts status/rating/scoop early via the prescribed section order | "Busyness vs power" trade-off (long-tail info down-page, full-bleed to reduce clutter) is not explicitly addressed as a design rule |
| PRD-065 | Provide conversational Ask chat interface | important | full | §9.4: "Chat UI, user/assistant turns, streaming" | |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | full | §0.5 + §8.2 base persona: "warm, opinionated, vibe-first, spoiler-safe" | |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | §9.4: "Mentioned-shows strip derived from latest assistant turn's showList" | |
| PRD-068 | Open Detail from mentions or Search fallback | important | full | §8.3: "Unresolved titles: returned as non-interactive items with a Search handoff affordance" | |
| PRD-069 | Show six random starter prompts with refresh | important | full | §9.4: "6 random starter prompts; refresh button" | |
| PRD-070 | Summarize older turns while preserving voice | important | full | §8.4: "After ~10 Ask turns, oldest turns condensed to 1–2 sentences keeping the same persona's voice" | |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | full | §9.4: "Ask-about-a-show (from Detail) — the latter seeds with the show context before the first user message" | |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | full | §8.2: "returns structured `{commentary, showList}`… `Title::externalId::mediaType;;...`" | |
| PRD-073 | Retry malformed mention output once, then fallback | important | full | §8.6: "Structured-output parse failure: one retry with tighter instructions; otherwise fall back to unstructured commentary + Search handoff" | |
| PRD-074 | Redirect Ask back into TV/movie domain | important | full | §0.5 + §8.2 base persona: "TV/movies only" | |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | full | §8.2: "vibe/structure/emotion axes, no generic concepts" matches taste-ingredient framing | |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | full | §8.2 + §8.6: "8 bullets, 1–3 words each… rejects items in a small blocklist" | |
| PRD-077 | Order concepts by strongest aha and varied axes | important | partial | §8.2 mentions "vibe/structure/emotion axes" for variety | "Order by strongest aha" / "best concepts first" is not addressed; no explicit ordering rule |
| PRD-078 | Require concept selection and guide ingredient picking | important | partial | §9.5 step 3 caps selection at 8 | Required minimum-selection (≥1) and the "pick the ingredients you want more of" guidance copy are not specified |
| PRD-079 | Return exactly five Explore Similar recommendations | important | full | §8.2: "5 recs for Explore Similar, 6 recs for Alchemy" | |
| PRD-080 | Support full Alchemy loop with chaining | important | full | §9.5 explicit five-step flow with "More Alchemy! chains, using current results as new inputs" | |
| PRD-081 | Clear downstream results when inputs change | important | full | §9.5: "Changing inputs clears downstream state" | |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | full | §8.2: "concepts must be shared across inputs; return a larger pool than single-show" | |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | full | §8.2: "1–3 sentence reason that names which concept(s) match" | |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | partial | §12.3 quality harness scores along Surprise + Taste dimensions | The runtime/prompt-level requirement to actually steer toward "surprising but defensible" recs is not encoded into the prompt builders or output validation |
| PRD-085 | Keep one consistent AI persona across surfaces | important | full | §8.2: "Base persona injected into every call… Lives in one file so voice is shared" | |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | full | §0.5 + §8.2 shared guardrails: spoiler-safe, in-domain only, opinionated honesty | |
| PRD-087 | Make AI warm, joyful, and light in critique | important | partial | §0.5 + §8.2 persona: "warm, opinionated, vibe-first, spoiler-safe" | "Joyful" and the "even critique is friendly, never mean or snobby" tonal pillar aren't called out; no Joy↔Hype tone-slider concept |
| PRD-088 | Structure Scoop as personal taste mini-review | important | full | §8.2: "structured multi-section (personal take, honest stack-up, Scoop centerpiece, fit/warnings, verdict); 150–350 words" | |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | full | §8.2 Ask: "conversational, short by default" | |
| PRD-090 | Feed AI the right surface-specific context inputs | important | full | §8.2 lists per-surface inputs (recent turns, show context, library, selected concepts) | |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | full | §8.6 + §12.3: real-show integrity is non-negotiable; quality harness scores rubric dimensions | |
| PRD-092 | Show person gallery, name, and bio | important | full | §9.7: "Image gallery, bio, filmography grouped by year" | |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | full | §9.7: "Analytics: avg project rating, top genres, projects-by-year" | |
| PRD-094 | Group filmography by year | important | full | §9.7: "filmography grouped by year" | |
| PRD-095 | Open Show Detail from selected credit | important | full | §9.7: "Credit click → /detail/[showId]" | |
| PRD-096 | Include font size and Search-on-launch settings | important | full | §9.8 App: "font size, search-on-launch" | |
| PRD-097 | Support username, model, and API-key settings safely | important | full | §9.8: "User: username; AI: provider API key (env always wins), model name; Integrations: catalog API key" | |
| PRD-098 | Export saved shows and My Data as zip | critical | full | §9.8 + §10: "/api/export → streams a .zip containing a JSON backup of all saved shows + my data" | |
| PRD-099 | Encode export dates using ISO-8601 | important | full | §9.8: "dates ISO-8601" | |

---

## 3. Coverage Scores

Counts:
- `full`: 90 (29 critical, 59 important, 2 detail)
- `partial`: 9 (1 critical, 8 important, 0 detail)
- `missing`: 0

**Score by severity tier:**

```
Critical:  (29 × 1.0 + 1 × 0.5) / 30 × 100 = 98.33%  (30 critical requirements)
Important: (59 × 1.0 + 8 × 0.5) / 67 × 100 = 94.03%  (67 important requirements)
Detail:    (2 × 1.0 + 0 × 0.5) / 2 × 100 = 100.00%   (2 detail requirements)
Overall:   (90 × 1.0 + 9 × 0.5) / 99 × 100 = 95.45%  (99 total requirements)
```

---

## 4. Top Gaps

1. **PRD-034 | critical | Preserve saved libraries across data-model upgrades.** The plan adds an `app_metadata.data_model_version` column but does not describe a migration upgrade strategy that brings forward existing `my_*` rows when the schema changes. Without this, a real schema evolution after launch could silently strand or drop user libraries — exactly the failure mode this requirement guards against.
2. **PRD-028 | important | Use timestamps for sorting, sync, freshness.** Timestamp-LWW for sync and 4h Scoop freshness are covered, but the "recently updated first" sort use-case is not addressed in Home, Other, or any other view. Users won't see their most recently maintained shows surfaced naturally without it.
3. **PRD-033 | important | Sync libraries/settings consistently and merge duplicates.** Cross-device sync is implied by `cloud_settings` and timestamp-LWW, but transparent duplicate detection/merge is missing. If two devices add the same show concurrently, the plan as written has no rule for collapsing duplicates.
4. **PRD-058 | important | Scoop shows correct states and progressive feedback.** Streaming is covered, but the three labelled toggle states ("Give me the scoop!" / "Show the scoop" / "The Scoop") and the explicit "Generating…" affordance aren't specified. Users will see a less considered Scoop entry-point than the spec describes.
5. **PRD-064 | important | Keep primary actions early and page not overwhelming.** Section ordering is preserved, but the underlying "busyness vs power" rule (down-page long-tail info, full-bleed to reduce clutter) is not encoded. The Detail page risks becoming a dense scroll without the explicit clutter-reduction guidance.

---

## 5. Coverage Narrative

#### Overall Posture

This is a **strong, structurally complete plan with minor specification gaps**. Every one of the 99 catalog requirements is at least addressed; nothing is wholly missing. Critical infrastructure requirements (Next.js + Supabase, namespace/user partitioning, RLS, env-var config, secret hygiene, save-rules, merge semantics, AI structured-output contract, export) are concretely covered with named tables, files, and route handlers. The plan reads like one a competent engineer could hand to another team and have them ship a behaviorally faithful first version. The one critical-tier soft spot is data-continuity-across-versions (PRD-034) — listed but not designed.

#### Strength Clusters

The plan is strongest in **Benchmark Runtime & Isolation** (17/17 full), **Ask Chat** (10/10 full), **Person Detail** (4/4 full), and **Settings & Export** (4/4 full). The infrastructure section in particular goes beyond restatement: it specifies the `(namespace_id, user_id)` partition, RLS via `current_setting`, dev identity injection that compiles out in production, OAuth-ready user-table columns, and a namespace-scoped `test:reset` — each tied to a Rider success criterion. The Ask surface is similarly concrete: the `Title::externalId::mediaType;;...` contract, parser fallback, summarization-with-voice, starter-prompt refresh, and Ask-about-this-show seeding are all called out by name.

#### Weakness Clusters

The partials cluster around two patterns. First, **AI behavioral subtlety** — concept ordering (PRD-077), selection guidance copy (PRD-078), surprise-without-betrayal (PRD-084), and the joyful/light-in-critique tonal pillar (PRD-087). The plan treats AI as a structural pipeline (prompts, parsers, validators) and under-specifies the *taste/voice* qualities that the supporting docs spend the most ink on. Second, **data-lifecycle edge cases** — schema upgrades (PRD-034), cross-device duplicate merging (PRD-033), and recency-driven sorting (PRD-028). The schema is sound for steady-state operations but doesn't specify what happens at the seams (upgrade, conflict, cross-device add). The Detail-page partials (PRD-058, PRD-064) reflect a related blind spot: the plan honors structural rules (section order) but not experiential rules (toggle copy, clutter management).

#### Risk Assessment

If executed as-is, the most likely failure mode would surface in **first user-perceived AI quality** rather than breakage. Concepts may come out in reasonable but not "aha"-ordered shape; recs may be safe rather than surprising; the Scoop entry-point may feel undesigned (no labelled state transitions, no "Generating…"). A QA reviewer reading the discovery_quality_bar rubric would notice the Surprise and Specificity dimensions sliding toward 1/2 rather than 2/2. A second, slower-burning risk: the data-continuity gap (PRD-034) is invisible until the second deploy with a schema change — at which point existing collections may not migrate cleanly. Stakeholders won't notice this on day one but will notice it badly when it happens.

#### Remediation Guidance

The AI partials need **prompt-builder specification work**, not new architecture: the existing `prompts/concepts.ts` and `prompts/recs.ts` need explicit ordering directives, selection-UX copy, surprise-target language, and the missing voice pillars woven into the base persona. This is detailed specification, not a new section. The data-lifecycle partials need a **dedicated short subsection** ("Data evolution & sync semantics") covering: (a) the migration playbook when `data_model_version` increases — what happens to existing `show_user_data` rows; (b) duplicate-detection rules when the same `show_id` arrives concurrently; (c) explicit sort-by-recency on Home and Other groups. The Detail partials need **acceptance-criteria rather than new sections**: enumerate Scoop button states, and add a "long-tail content is full-bleed and collapsed by default" rule in §9.6. None of these require architectural rework — they are gaps in *what the plan tells the implementer to build*, not in the plan's structure.
