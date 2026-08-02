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
| PRD-001 | Use Next.js latest stable runtime | critical | full | Tech Stack: "Next.js (latest stable) with App Router" |  |
| PRD-002 | Use Supabase official client libraries | critical | full | Tech Stack and Phase 1.1 install `@supabase/supabase-js`, `@supabase/ssr` |  |
| PRD-003 | Ship `.env.example` with required variables | critical | full | Phase 1.1 lists `.env.example` keys |  |
| PRD-004 | Ignore `.env*` secrets except example | important | full | Phase 1.1: ".gitignore excludes `.env*` (except `.env.example`)" |  |
| PRD-005 | Configure build through env without code edits | critical | partial | Phase 1.1 lists env keys; Phase 9.1 says provider/base URL configurable via settings/env | The plan names environment variables but does not explicitly make the whole build/run path configurable without source edits. |
| PRD-006 | Keep secrets out of repo and server-only | critical | full | Phase 11.3: service role key never exposed; API keys never committed and stored server-side |  |
| PRD-007 | Provide app, test, reset command scripts | critical | full | Phase 1.4 defines `npm run dev`, `npm test`, and `npm run test:reset` |  |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | Phase 1.2: migration files in `supabase/migrations/` |  |
| PRD-009 | Use one stable namespace per build | critical | full | Phase 1.3 reads `x-namespace-id` or `process.env.NAMESPACE_ID` |  |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | Phase 1.3 scopes all queries; Phase 1.4 reset deletes current namespace |  |
| PRD-011 | Attach every user record to `user_id` | critical | full | Phase 1.2 adds `user_id` to `shows` and `cloud_settings`; Phase 1.3 injects it |  |
| PRD-012 | Partition persisted data by namespace and user | critical | full | Phase 1.2 RLS and keys scoped to `(namespace_id, user_id)` |  |
| PRD-013 | Support documented dev auth injection, prod-gated | important | full | Phase 1.3 reads `x-user-id` in dev/benchmark mode; Phase 11.3 gates behind production check |  |
| PRD-014 | Real OAuth later needs no schema redesign | important | partial | Phase 1.2 stores opaque `user_id`; Phase 11.3 gates dev auth | The plan does not explicitly state the OAuth migration path or that no schema redesign is needed. |
| PRD-015 | Keep backend as persisted source of truth | critical | full | Tech Stack uses Supabase persistence; Phase 2.1 centralizes CRUD in Show Service |  |
| PRD-016 | Make client cache safe to discard | critical | missing | none | The plan does not discuss client caches/local persistence being disposable or safe to clear without user-data loss. |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | partial | Tech Stack uses hosted-style Supabase and no Docker workflow is listed | Avoiding Docker is implied by omission, but the plan never documents Docker as unnecessary or optional. |
| PRD-018 | Overlay saved user data on every show appearance | critical | partial | Phase 6.2 marks in-collection search results; Phase 4.2 shows badges | The plan does not explicitly require user-overlaid saved data to replace public data everywhere a show appears, including recommendations and AI outputs. |
| PRD-019 | Support visible statuses plus hidden `Next` | important | full | Phase 1.2 uses all fields from `storage-schema.ts`; Phase 5.2 exposes visible status chips without `Next` |  |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | full | Phase 5.2: Interested/Excited set status Later plus interest level |  |
| PRD-021 | Support free-form multi-tag personal tag library | important | full | Phase 4.3: tag filters auto-generated from user's tag library; Phase 5.2 tag picker |  |
| PRD-022 | Define collection membership by assigned status | critical | full | Phase 2.1 default status on save and removal through status clearing establish status-based membership |  |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | full | Phase 5.2 covers status chips, Interested/Excited, rating auto-save, and tag auto-save |  |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | Phase 2.1: default Later/Interested except rating-save to Done |  |
| PRD-025 | Removing status deletes show and all My Data | critical | full | Phase 2.1: `removeShow` clears all `my*` fields; Phase 5.2 confirms removal |  |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | partial | Phase 2.1 merge logic uses timestamp comparison; Phase 3.2 maps catalog fields | The plan does not explicitly describe the re-add flow preserving latest My Data while refreshing public metadata. |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | Phase 1.2 includes all fields from `storage-schema.ts`, which carries per-field update dates |  |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | full | Phase 2.2 orders by update date; Phase 2.3 conflict resolution; Phase 5.3 4-hour Scoop freshness |  |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | full | Phase 5.3: 4-hour cache and only persists if show is in collection |  |
| PRD-030 | Keep Ask and Alchemy state session-only | important | full | Phase 6.3 reset/clear session; Phase 6.4 changing inputs clears concepts/results |  |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | full | Phase 9.3 resolves external IDs/title search and non-resolvable fallback |  |
| PRD-032 | Show collection and rating tile indicators | important | full | Phase 4.2: in-collection badge and rating badge |  |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | full | Phase 2.3 CloudSettings conflict resolution; Phase 2.1 timestamp merge logic |  |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | full | Phase 11.1 data continuity with versioned forward migrations |  |
| PRD-035 | Persist synced settings, local settings, UI state | important | partial | Phase 2.3 CloudSettings; Phase 8.1 settings; Phase 4.1 media toggle persisted as URL param | Synced settings are covered, but local settings/UI state such as confirmation suppression and last selected filter are not fully planned. |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | full | Phase 3.2 stores provider IDs only; Phase 3.3 fetches detail assets on demand, not persisted |  |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | full | Phase 2.1: catalog merge uses `selectFirstNonEmpty`; user fields use timestamp comparison |  |
| PRD-038 | Provide filters panel and main screen destinations | important | full | Phase 4.1 sidebar/nav panel and main content area |  |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | partial | Phase 6 defines Find/Discover hub and mode switcher | The plan does not explicitly place Find/Discover in persistent primary navigation. |
| PRD-040 | Keep Settings in persistent primary navigation | important | partial | Phase 8 defines Settings page | The plan does not explicitly place Settings in persistent primary navigation. |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | Phase 6.1: three tabs Search, Ask, Alchemy |  |
| PRD-042 | Show only library items matching active filters | important | full | Phase 4.1 filtered library; Phase 2.2 `listShows(filters)` |  |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | Phase 4.2 lists the required status sections |  |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | full | Phase 2.2 and Phase 4.3 list media type, tags, genre, decade, and score |  |
| PRD-045 | Render poster, title, and My Data badges | important | full | Phase 4.2: tiles include poster, title, in-collection badge, rating badge |  |
| PRD-046 | Provide empty-library and empty-filter states | detail | full | Phase 4.2: "No shows yet" and "No results found" |  |
| PRD-047 | Search by title or keywords | important | full | Phase 6.2: text input to debounced catalog search |  |
| PRD-048 | Use poster grid with collection markers | important | full | Phase 6.2: poster grid results with in-collection badge |  |
| PRD-049 | Auto-open Search when setting is enabled | detail | full | Phase 6.2: optional auto-open on launch setting |  |
| PRD-050 | Keep Search non-AI in tone | important | full | Phase 6.2 implements plain catalog search; AI surfaces are separated into Ask/Alchemy |  |
| PRD-051 | Preserve Show Detail narrative section order | important | full | Phase 5.1 lists the required 12-section order |  |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | full | Phase 5.1: header carousel with backdrops/posters/logos and trailer embed |  |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | full | Phase 5.1 item 2 core facts row |  |
| PRD-054 | Place status/interest controls in toolbar | important | full | Phase 5.2: My Relationship Controls in Toolbar |  |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | Phase 5.2: unsaved plus add tag auto-saves Later/Interested |  |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | Phase 5.2: unsaved plus rate auto-saves as Done |  |
| PRD-057 | Show overview early for fast scanning | important | full | Phase 5.1 places overview at item 4 before deeper sections |  |
| PRD-058 | Scoop shows correct states and progressive feedback | important | full | Phase 5.3 covers toggle states and progressive streaming |  |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | partial | Phase 5.1 includes an "Ask about this show" button; Phase 9.2 has surface-specific prompt templates | The plan includes the entry point but does not explicitly seed Ask with the current show context. |
| PRD-060 | Include traditional recommendations strand | important | full | Phase 5.1 item 7 recommendations strand |  |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | full | Phase 5.4: Get Concepts, select concepts, Explore Shows |  |
| PRD-062 | Include streaming availability and person-linking credits | important | full | Phase 5.1 providers plus Cast and Crew to Person Detail |  |
| PRD-063 | Gate seasons to TV and financials to movies | important | full | Phase 5.1: Seasons TV only and Budget/Revenue movies |  |
| PRD-064 | Keep primary actions early and page not overwhelming | important | full | Phase 5.1 places tags, Scoop, Ask, recommendations, and Explore Similar before long-tail sections |  |
| PRD-065 | Provide conversational Ask chat interface | important | full | Phase 6.3: chat UI with message bubbles, input, loading states |  |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | partial | Phase 9.2 base personality prompt and Phase 6.3 chat UI | The plan covers tone broadly but does not explicitly require direct answers in the first lines or confident spoiler-safe recommendation behavior. |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | Phase 6.3: mentioned shows horizontal strip below chat |  |
| PRD-068 | Open Detail from mentions or Search fallback | important | full | Phase 6.3: tap mentioned show opens Detail or Search fallback |  |
| PRD-069 | Show six random starter prompts with refresh | important | full | Phase 6.3: welcome view with 6 random starter prompts, refreshable |  |
| PRD-070 | Summarize older turns while preserving voice | important | full | Phase 6.3 older turns summarized; Phase 9.2 summarization preserves persona tone |  |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | partial | Phase 5.1 Ask-about-this-show button and Phase 9.2 surface-specific prompt templates | The handoff show is implied by the button but not specified as Ask session context. |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | partial | Phase 6.3 says commentary plus structured `showList`; Phase 9.1 parses `Title::id::type;;` | The plan contradicts itself by calling the format pipe-delimited and does not specify the exact `Title::externalId::mediaType;;` contract. |
| PRD-073 | Retry malformed mention output once, then fallback | important | full | Phase 9.1 retry once with stricter instructions, then fallback |  |
| PRD-074 | Redirect Ask back into TV/movie domain | important | missing | none | The plan does not specify out-of-domain Ask handling or redirect behavior. |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | partial | Phase 5.4 and Phase 6.4 use concept catalysts and concept-grounded reasons | The plan uses concepts but does not explicitly preserve the "taste ingredient, not genre" definition. |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | full | Phase 5.4: concepts rendered as 1-3 word evocative chips; Phase 9.2 concept templates |  |
| PRD-077 | Order concepts by strongest aha and varied axes | important | missing | none | The plan does not require concept ordering by strongest aha or coverage across varied axes. |
| PRD-078 | Require concept selection and guide ingredient picking | important | partial | Phase 5.4 and Phase 6.4 require selecting concepts before recommendations | Selection is covered, but the UI guidance to pick ingredients is not planned. |
| PRD-079 | Return exactly five Explore Similar recommendations | important | full | Phase 5.4: AI returns 5 recs |  |
| PRD-080 | Support full Alchemy loop with chaining | important | full | Phase 6.4 covers all Alchemy steps and "More Alchemy!" chaining |  |
| PRD-081 | Clear downstream results when inputs change | important | full | Phase 6.4: changing shows clears concepts/results |  |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | partial | Phase 6.4: AI generates shared concepts for selected shows | The larger multi-show option pool is not specified. |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | full | Phase 6.4 and Phase 9.3 concept-grounded reasons |  |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | partial | Phase 9.2 concept recommendation templates; Phase 6.4 concept-grounded reasons | Taste alignment is implied, but surprise-without-betrayal and defensibility are not acceptance criteria. |
| PRD-085 | Keep one consistent AI persona across surfaces | important | full | Phase 9.2 base personality prompt plus surface-specific prompt templates |  |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | partial | Phase 9.2 base prompt with voice pillars; Phase 11.2 AI fallback handling | The plan gestures at shared prompt management but does not explicitly enumerate or enforce the full guardrails across all AI surfaces. |
| PRD-087 | Make AI warm, joyful, and light in critique | important | full | Phase 9.2: "fun, chatty TV/movie nerd friend" with voice pillars |  |
| PRD-088 | Structure Scoop as personal taste mini-review | important | partial | Phase 5.3 streaming Scoop; Phase 9.2 Scoop prompt template | The plan does not list the required Scoop structure: personal take, stack-up, centerpiece, fit/warnings, and verdict. |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | full | Phase 9.2 Ask prompt template and persona; Phase 6.3 conversational chat UI |  |
| PRD-090 | Feed AI the right surface-specific context inputs | important | full | Phase 9.1 methods accept prompt/context; Phase 9.2 surface-specific prompt templates |  |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | missing | none | The plan has parser tests but no discovery quality rubric, golden checks, or hard-fail real-show integrity validation. |
| PRD-092 | Show person gallery, name, and bio | important | full | Phase 7.1: image gallery, name, bio |  |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | full | Phase 7.1 analytics charts for average rating, top genres, projects-by-year |  |
| PRD-094 | Group filmography by year | important | full | Phase 7.1: filmography grouped by year |  |
| PRD-095 | Open Show Detail from selected credit | important | full | Phase 7.1: each credit opens Show Detail |  |
| PRD-096 | Include font size and Search-on-launch settings | important | full | Phase 8.1 font size selector and Search on launch toggle |  |
| PRD-097 | Support username, model, and API-key settings safely | important | full | Phase 8.1 username, AI key, model, catalog key; Phase 11.3 secure handling |  |
| PRD-098 | Export saved shows and My Data as zip | critical | full | Phase 2.4 and Phase 8.2 export zip containing user shows/settings |  |
| PRD-099 | Encode export dates using ISO-8601 | important | full | Phase 2.4: ISO-8601 date encoding |  |

### 3. Coverage Scores

```
score = (full_count Ã— 1.0 + partial_count Ã— 0.5) / total_count Ã— 100
```

Critical:  (24 Ã— 1.0 + 5 Ã— 0.5) / 30 Ã— 100 = 88.3%  (26.5 of 30 critical requirements)
Important: (51 Ã— 1.0 + 13 Ã— 0.5) / 67 Ã— 100 = 85.8%  (57.5 of 67 important requirements)
Detail:    (2 Ã— 1.0 + 0 Ã— 0.5) / 2 Ã— 100 = 100.0%  (2 of 2 detail requirements)
Overall:   86.9% (99 total requirements)

### 4. Top Gaps

1. PRD-016 | critical | Make client cache safe to discard
   
   This matters because the benchmark explicitly requires backend persistence to survive clearing local storage or reinstalling; without that contract, an implementation might accidentally rely on browser cache for user-owned data.

2. PRD-018 | critical | Overlay saved user data on every show appearance
   
   This matters because the product's core promise is that the user's version of a show wins everywhere; if search, recommendations, or AI results show stale public-only cards, the app feels inconsistent and user trust drops.

3. PRD-086 | critical | Enforce shared AI guardrails across all surfaces
   
   This matters because guardrails are the consistency layer across Scoop, Ask, Explore Similar, and Alchemy; without explicit enforcement, the app can drift on spoilers, domain boundaries, honesty, and specificity.

4. PRD-072 | critical | Emit `commentary` plus exact `showList` contract
   
   This matters because Ask mentions drive selectable recommendation UI; a loose or contradictory format can break parsing, prevent catalog resolution, and degrade chat recommendations into plain text.

5. PRD-026 | critical | Re-add preserves My Data and refreshes public data
   
   This matters because users may remove and rediscover the same show; if re-add behavior is only implicit, user ratings, tags, or status history can be lost or public metadata can go stale.

### 5. Coverage Narrative

#### Overall Posture

This is a structurally sound and fairly complete plan. It covers the main product surfaces, Supabase-backed data model, namespace/user isolation, collection flows, Show Detail, Ask, Alchemy, Person Detail, Settings, and export. The remaining weaknesses are not about missing whole screens; they are mostly exact behavioral contracts that the PRD treats as product-critical.

#### Strength Clusters

The plan is strongest in Benchmark Runtime & Isolation, Show Detail & Relationship UX, Collection Home & Search, Person Detail, and Settings & Export. It gives concrete phases, service boundaries, schema artifacts, scripts, UI sections, and test categories for those areas. The Detail page is especially close to the PRD's required narrative order and auto-save rules.

#### Weakness Clusters

The gaps cluster around cross-surface invariants and AI quality contracts. The plan often names the right AI or data feature but misses exact behavioral details: disposable client cache, saved-user overlay everywhere, exact Ask `showList` formatting, concept ordering/variety, Scoop structure, and discovery quality rubric enforcement.

#### Risk Assessment

If executed as-is, the most likely failure mode is a product that looks feature-complete but behaves inconsistently at the edges. QA would first notice that some AI outputs or recommendation cards do not reliably resolve or carry user overlay state, and that AI quality is implemented through prompts but not protected by acceptance criteria.

#### Remediation Guidance

The plan needs tighter acceptance criteria rather than major architectural redesign. Add explicit cross-surface data-overlay rules, client-cache disposability constraints, exact AI output contracts, discovery quality tests/rubrics, and concept/Scoop prompt acceptance criteria. These should be written as implementation requirements and test targets, not just prompt-management intentions.
