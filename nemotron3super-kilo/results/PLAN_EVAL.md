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

### 2. Coverage Table

| PRD-ID | Requirement | Severity | Coverage | Evidence | Gap |
| ------ | ----------- | -------- | -------- | -------- | --- |
| PRD-001 | Use Next.js latest stable runtime | critical | full | Technical Stack: "Frontend: Next.js (latest stable), TypeScript" |  |
| PRD-002 | Use Supabase official client libraries | critical | partial | Technical Stack: "Backend: Supabase (PostgreSQL, Auth, Storage)" | The plan selects Supabase but does not state that official client libraries are required. |
| PRD-003 | Ship `.env.example` with required variables | critical | partial | Deployment & Infrastructure: "Benchmark compliance: .env.example, one-command experience, deterministic test data" | The plan mentions `.env.example` but does not define the required variables or the expected inline comments. |
| PRD-004 | Ignore `.env*` secrets except example | important | partial | Development Considerations: "Privacy & Security: RLS policies, anon key usage, secret management" | Secret handling is mentioned, but the plan never calls for `.gitignore` rules that exclude `.env*` except `.env.example`. |
| PRD-005 | Configure build through env without code edits | critical | partial | Deployment & Infrastructure: "Benchmark compliance: .env.example, one-command experience, deterministic test data" | Environment-based configuration is implied, but the plan does not explicitly require a no-code-edit setup path. |
| PRD-006 | Keep secrets out of repo and server-only | critical | partial | Development Considerations: "Privacy & Security: RLS policies, anon key usage, secret management" | The plan mentions secret management and anon keys, but it does not explicitly reserve elevated keys for server-only use. |
| PRD-007 | Provide app, test, reset command scripts | critical | full | Deployment & Infrastructure: "Development: npm run dev, npm test, npm run test:reset" |  |
| PRD-008 | Include repeatable schema evolution artifacts | critical | missing | none | The plan never calls for migrations or another repeatable schema-evolution mechanism to recreate a fresh database deterministically. |
| PRD-009 | Use one stable namespace per build | critical | full | Architecture Overview: "Namespace isolation for build/run separation" |  |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | Architecture Overview: "Namespace isolation for build/run separation" |  |
| PRD-011 | Attach every user record to `user_id` | critical | partial | Architecture Overview: "User-scoped data storage" | User scoping is named, but the plan does not specify that every user-owned persisted record must carry a `user_id`. |
| PRD-012 | Partition persisted data by namespace and user | critical | partial | Architecture Overview: "Namespace isolation for build/run separation" + "User-scoped data storage" | The plan mentions namespace isolation and user-scoped storage separately, but it does not define `(namespace_id, user_id)` as the effective partition. |
| PRD-013 | Support documented dev auth injection, prod-gated | important | missing | none | The plan does not describe a documented development identity-injection mechanism or how it is gated away from production. |
| PRD-014 | Real OAuth later needs no schema redesign | important | missing | none | The plan does not discuss how the auth design avoids a future schema redesign when real OAuth is introduced. |
| PRD-015 | Keep backend as persisted source of truth | critical | partial | Architecture Overview: "Client-server architecture with Next.js frontend and Supabase backend" | A backend exists in the architecture, but the plan never states that persisted backend data is the authoritative source of truth. |
| PRD-016 | Make client cache safe to discard | critical | missing | none | Caching is mentioned only as a performance concern, not as disposable state that can be cleared without losing user data. |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | missing | none | The plan never states that Docker must remain optional or unnecessary for benchmark execution. |
| PRD-018 | Overlay saved user data on every show appearance | critical | partial | Data Models: "Show entity with public catalog data and user overlay (My Data)" | The user overlay model is named, but the plan does not say that overlaid data must appear everywhere a show is rendered. |
| PRD-019 | Support visible statuses plus hidden `Next` | important | partial | Feature Implementation: "Collection Management (status, interest, tags, rating, auto-save rules)" | Statuses and interest are in scope, but the plan does not preserve the visible-status set plus hidden `Next` behavior. |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | partial | Feature Implementation: "Collection Management (status, interest, tags, rating, auto-save rules)" | The plan includes status and interest work, but it does not define the specific `Interested/Excited -> Later + interest` mapping. |
| PRD-021 | Support free-form multi-tag personal tag library | important | partial | Feature Implementation: "Collection Management (status, interest, tags, rating, auto-save rules)" | Tags are in scope, but the plan does not call out a reusable free-form personal tag library. |
| PRD-022 | Define collection membership by assigned status | critical | partial | Feature Implementation: "Collection Management (status, interest, tags, rating, auto-save rules)" | Collection management is planned, but the plan does not explicitly define collection membership as status assignment. |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | partial | Feature Implementation: "Collection Management (status, interest, tags, rating, auto-save rules)" | Auto-save rules are acknowledged, but the plan does not enumerate the save triggers from status, interest, rating, and tagging. |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | partial | Feature Implementation: "Collection Management (status, interest, tags, rating, auto-save rules)" | The plan references auto-save rules, but it does not specify the Later/Interested default or the rating-to-Done exception. |
| PRD-025 | Removing status deletes show and all My Data | critical | partial | Feature Implementation: "Collection Management (status, interest, tags, rating, auto-save rules)" | Status management is planned, but the removal rule does not explicitly delete the show and clear all My Data. |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | partial | Data Models: "Merge rules: non-my fields use selectFirstNonEmpty, my fields resolved by timestamp" | Merge rules are mentioned, but the plan does not explicitly cover re-add behavior that preserves My Data while refreshing public data. |
| PRD-027 | Track per-field My Data modification timestamps | critical | partial | Data Models: "Merge rules: non-my fields use selectFirstNonEmpty, my fields resolved by timestamp" | Timestamp-based merge behavior is named, but the plan does not require per-field modification timestamps for every My Data attribute. |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | partial | Development Considerations: "Data synchronization and merge rules per storage-schema.md" | The plan mentions sync/merge rules, but it does not specify timestamp-driven sorting, sync, and freshness behaviors. |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | partial | Feature Implementation: "Discovery Features (Search, Ask, Alchemy, Explore Similar, AI Scoop)" | AI Scoop is in scope, but the plan does not define the saved-only persistence rule or the four-hour freshness window. |
| PRD-030 | Keep Ask and Alchemy state session-only | important | missing | none | The plan does not say that Ask history and Alchemy state remain session-only and are cleared when those surfaces reset or close. |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | partial | Development Considerations: "AI integration with structured outputs and fallback strategies" | Structured AI integration is planned, but the plan does not explicitly require recommendation resolution into real selectable shows. |
| PRD-032 | Show collection and rating tile indicators | important | missing | none | The plan never mentions collection or rating indicators on show tiles. |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | partial | Development Considerations: "Data synchronization and merge rules per storage-schema.md" | Synchronization is acknowledged, but duplicate detection and transparent merging are not planned explicitly. |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | partial | Data Models: "Supporting entities: CloudSettings, AppMetadata, LocalSettings, UIState" | AppMetadata is mentioned, but the plan does not define a continuity strategy that preserves saved libraries across model upgrades. |
| PRD-035 | Persist synced settings, local settings, UI state | important | full | Data Models: "Supporting entities: CloudSettings, AppMetadata, LocalSettings, UIState" |  |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | missing | none | The plan does not distinguish persisted provider IDs from transient detail fetch data. |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | full | Data Models: "Merge rules: non-my fields use selectFirstNonEmpty, my fields resolved by timestamp" |  |
| PRD-038 | Provide filters panel and main screen destinations | important | missing | none | The plan does not describe the filters panel or the main screen destinations that make up the discover shell. |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | missing | none | The plan never states that Find/Discover remains in persistent primary navigation. |
| PRD-040 | Keep Settings in persistent primary navigation | important | missing | none | The plan never states that Settings remains in persistent primary navigation. |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | Feature Implementation: "Discovery Features (Search, Ask, Alchemy, Explore Similar, AI Scoop)" |  |
| PRD-042 | Show only library items matching active filters | important | missing | none | The plan does not say that Home displays only library items matching the active filters. |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | missing | none | The plan does not define the required Home grouping into Active, Excited, Interested, and Others. |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | missing | none | The plan never enumerates the All, tag, genre, decade, score, and media-type filter set. |
| PRD-045 | Render poster, title, and My Data badges | important | missing | none | The plan does not specify poster/title/badge rendering for collection tiles. |
| PRD-046 | Provide empty-library and empty-filter states | detail | missing | none | The plan does not mention empty-library or empty-filter states for Collection Home. |
| PRD-047 | Search by title or keywords | important | partial | Feature Implementation: "Discovery Features (Search, Ask, Alchemy, Explore Similar, AI Scoop)" | Search is in scope, but the plan does not explicitly define title-or-keyword query behavior. |
| PRD-048 | Use poster grid with collection markers | important | missing | none | The plan never specifies a poster-grid search layout with collection markers. |
| PRD-049 | Auto-open Search when setting is enabled | detail | missing | none | The plan includes Settings generally, but it does not connect Search-on-launch to automatically opening Search on app launch. |
| PRD-050 | Keep Search non-AI in tone | important | missing | none | The plan does not protect Search as a non-AI surface with straightforward catalog tone. |
| PRD-051 | Preserve Show Detail narrative section order | important | missing | none | The plan does not preserve the required Show Detail section order. |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | missing | none | The plan never mentions the motion-rich header or the graceful poster/backdrop fallback. |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | missing | none | The plan does not specify surfacing year, runtime/seasons, and community score early in Detail. |
| PRD-054 | Place status/interest controls in toolbar | important | missing | none | The plan never places status and interest controls in the Detail toolbar. |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | partial | Feature Implementation: "Collection Management (status, interest, tags, rating, auto-save rules)" | Auto-save rules are mentioned, but the tag-to-save behavior is not defined as `Later + Interested`. |
| PRD-056 | Auto-save unsaved rated show as Done | critical | partial | Feature Implementation: "Collection Management (status, interest, tags, rating, auto-save rules)" | Auto-save rules are mentioned, but the rating-to-save behavior is not defined as auto-saving unsaved shows as `Done`. |
| PRD-057 | Show overview early for fast scanning | important | missing | none | The plan does not say that the overview must appear early for quick scanning. |
| PRD-058 | Scoop shows correct states and progressive feedback | important | missing | none | The plan does not cover Scoop loading states, progressive feedback, or freshness-state UX. |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | missing | none | The plan does not include the Ask-about-this-show deep-link or its required context handoff. |
| PRD-060 | Include traditional recommendations strand | important | missing | none | The plan never calls for the traditional recommendation strand on Detail. |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | partial | Feature Implementation: "Discovery Features (Search, Ask, Alchemy, Explore Similar, AI Scoop)" | Explore Similar is in scope, but the plan does not describe the CTA-first concepts flow or its interaction steps. |
| PRD-062 | Include streaming availability and person-linking credits | important | missing | none | The plan does not include streaming availability or cast/crew person-linking behavior from Detail. |
| PRD-063 | Gate seasons to TV and financials to movies | important | missing | none | The plan does not gate seasons to TV and financials to movies. |
| PRD-064 | Keep primary actions early and page not overwhelming | important | missing | none | The plan does not address the early-action clustering and anti-overwhelm balance on Detail. |
| PRD-065 | Provide conversational Ask chat interface | important | partial | Feature Implementation: "Discovery Features (Search, Ask, Alchemy, Explore Similar, AI Scoop)" | Ask is in scope, but the plan does not explicitly call for a conversational chat interface. |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | missing | none | The plan does not specify direct, confident, spoiler-safe recommendation behavior for Ask. |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | missing | none | The plan does not include the horizontal mentioned-shows strip. |
| PRD-068 | Open Detail from mentions or Search fallback | important | partial | Development Considerations: "AI integration with structured outputs and fallback strategies" | Fallback strategies are mentioned, but the plan does not explicitly connect Ask mentions to Detail opens or Search fallback. |
| PRD-069 | Show six random starter prompts with refresh | important | missing | none | The plan does not mention six random starter prompts or refresh behavior for Ask. |
| PRD-070 | Summarize older turns while preserving voice | important | missing | none | The plan does not describe conversation summarization for older Ask turns. |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | missing | none | The plan does not include Ask-about-show sessions seeded by the current show. |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | partial | Development Considerations: "AI integration with structured outputs and fallback strategies" | Structured AI output is planned, but the exact `commentary` plus `showList` contract is not specified. |
| PRD-073 | Retry malformed mention output once, then fallback | important | partial | Development Considerations: "AI integration with structured outputs and fallback strategies" | Fallback strategies are mentioned, but the plan does not commit to a single retry before degrading gracefully. |
| PRD-074 | Redirect Ask back into TV/movie domain | important | missing | none | The plan does not require Ask to redirect users back into the TV/movie domain when they drift away. |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | missing | none | The plan never defines concepts as taste ingredients distinct from genres. |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | missing | none | The plan does not specify bullet-only, one-to-three-word, non-generic concept output. |
| PRD-077 | Order concepts by strongest aha and varied axes | important | missing | none | The plan does not require concept ordering by strongest aha or coverage across varied axes. |
| PRD-078 | Require concept selection and guide ingredient picking | important | missing | none | The plan does not describe concept-selection requirements or ingredient-picking guidance. |
| PRD-079 | Return exactly five Explore Similar recommendations | important | missing | none | The plan never fixes Explore Similar output at exactly five recommendations. |
| PRD-080 | Support full Alchemy loop with chaining | important | partial | Feature Implementation: "Discovery Features (Search, Ask, Alchemy, Explore Similar, AI Scoop)" | Alchemy is in scope, but the plan does not lay out the full stepwise loop or chaining behavior. |
| PRD-081 | Clear downstream results when inputs change | important | missing | none | The plan does not clear downstream concepts or recommendations when Alchemy inputs change. |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | missing | none | The plan does not require multi-show concepts to produce a larger shared option pool. |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | missing | none | The plan does not require recommendation reasons to cite the selected concepts directly. |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | missing | none | The plan does not define a quality bar for surprising but defensible taste-aligned recommendations. |
| PRD-085 | Keep one consistent AI persona across surfaces | important | missing | none | The plan does not define a single shared AI persona across Scoop, Ask, Alchemy, and Explore Similar. |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | missing | none | The plan does not establish shared AI guardrails for domain limits, spoiler safety, honesty, and specificity across all AI surfaces. |
| PRD-087 | Make AI warm, joyful, and light in critique | important | missing | none | The plan does not encode the warm, joyful, lightly critical voice requirements. |
| PRD-088 | Structure Scoop as personal taste mini-review | important | partial | Feature Implementation: "Discovery Features (Search, Ask, Alchemy, Explore Similar, AI Scoop)" | AI Scoop is in scope, but the plan does not define it as a structured personal taste mini-review. |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | partial | Feature Implementation: "Discovery Features (Search, Ask, Alchemy, Explore Similar, AI Scoop)" | Ask is in scope, but the plan does not specify brisk, dialogue-like default responses. |
| PRD-090 | Feed AI the right surface-specific context inputs | important | missing | none | The plan does not specify the surface-specific context that each AI feature must receive. |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | missing | none | The plan does not include the discovery quality rubric or a hard-fail integrity check for real-show resolution. |
| PRD-092 | Show person gallery, name, and bio | important | partial | Feature Implementation: "Supporting Features (Person Detail, Settings, Data Export/Import)" | Person Detail is in scope, but the plan does not specify the required gallery, name, and bio presentation. |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | partial | Feature Implementation: "Supporting Features (Person Detail, Settings, Data Export/Import)" | Person Detail is in scope, but ratings, genres, and projects-by-year analytics are not called out. |
| PRD-094 | Group filmography by year | important | partial | Feature Implementation: "Supporting Features (Person Detail, Settings, Data Export/Import)" | Person Detail is planned, but filmography grouping by year is not specified. |
| PRD-095 | Open Show Detail from selected credit | important | partial | Feature Implementation: "Supporting Features (Person Detail, Settings, Data Export/Import)" | Person Detail is planned, but the selected-credit handoff back into Show Detail is not specified. |
| PRD-096 | Include font size and Search-on-launch settings | important | partial | Feature Implementation: "Supporting Features (Person Detail, Settings, Data Export/Import)" | Settings are in scope, but the plan does not specify font-size and Search-on-launch controls. |
| PRD-097 | Support username, model, and API-key settings safely | important | partial | Feature Implementation: "Supporting Features (Person Detail, Settings, Data Export/Import)" | Settings and external services are planned, but the safe handling of username, model, and API-key settings is not detailed. |
| PRD-098 | Export saved shows and My Data as zip | critical | partial | Feature Implementation: "Supporting Features (Person Detail, Settings, Data Export/Import)" | Data export is in scope, but the plan does not specify a zip backup containing saved shows plus all My Data. |
| PRD-099 | Encode export dates using ISO-8601 | important | missing | none | The plan does not require export dates to be encoded in ISO-8601 format. |

### 3. Coverage Scores

Critical:  (5 x 1.0 + 22 x 0.5) / 30 x 100 = 53.3%  (16.0 of 30 critical requirements)
Important: (2 x 1.0 + 19 x 0.5) / 67 x 100 = 17.2%  (11.5 of 67 important requirements)
Detail:    (0 x 1.0 + 0 x 0.5) / 2 x 100 = 0.0%  (0.0 of 2 detail requirements)
Overall:   (7 x 1.0 + 41 x 0.5) / 99 x 100 = 27.8%  (27.5 of 99 total requirements)

### 4. Top Gaps

1. PRD-008 | `critical` | Include repeatable schema evolution artifacts
Without planned migrations or equivalent schema artifacts, the team cannot recreate or upgrade database state deterministically, which breaks benchmark repeatability and raises delivery risk immediately.
2. PRD-016 | `critical` | Make client cache safe to discard
If cache-disposal safety is not designed up front, users can lose the effective product state whenever local storage is cleared or a client is reinstalled, violating one of the rider's core data guarantees.
3. PRD-086 | `critical` | Enforce shared AI guardrails across all surfaces
Missing shared guardrails means each AI surface can drift on spoiler safety, domain boundaries, honesty, and specificity, producing inconsistent behavior that fails product identity and QA expectations.
4. PRD-072 | `critical` | Emit `commentary` plus exact `showList` contract
The Ask surface depends on an exact structured contract for rendering mentioned shows; without it, the UI integration is brittle and recommendation taps will fail or degrade unpredictably.
5. PRD-011 | `critical` | Attach every user record to `user_id`
User scoping is only gestured at, so the implementation could easily omit `user_id` on some records and fail the benchmark's minimum multi-user data ownership model.

### 5. Coverage Narrative

#### Overall Posture

This is a structurally weak plan for this benchmark. It establishes a few baseline technology and isolation choices, but at 27.8% weighted coverage it misses too many concrete behavioral requirements to guide a faithful rebuild of the product.

#### Strength Clusters

The strongest coverage is in Benchmark Runtime & Isolation basics and a narrow slice of Collection Data & Persistence. The plan explicitly commits to Next.js, Supabase, namespace isolation, reset scripts, core persisted entities, and the merge-rule pattern from the storage schema. It also at least names the major discovery surfaces: Search, Ask, Alchemy, Explore Similar, and AI Scoop.

#### Weakness Clusters

Gaps cluster heavily in UX-precise functional areas and in AI behavioral contracts. Collection Home, Show Detail, Ask, Concepts/Alchemy quality rules, AI persona/guardrails, and Settings/Export specifics are mostly missing, which indicates the plan treats the product as a stack-and-feature list rather than a behaviorally exact rebuild.

#### Risk Assessment

If executed as-is, the most likely outcome is an app that has the right headline technologies and some broad features, but fails parity on the first serious QA pass. Reviewers would notice missing home grouping/filter behavior, weak Detail-page relationship flows, absent Ask/mentioned-show contracts, and AI output that does not reliably match the product's voice or structured expectations.

#### Remediation Guidance

The plan needs deeper behavioral planning, not just more implementation bullets. The missing work is mainly: explicit data-contract decisions for auth/isolation/migrations, per-surface UX and state-transition planning for Home/Detail/Ask/Alchemy, and concrete AI-surface acceptance criteria covering persona, guardrails, structured outputs, resolution rules, and export/settings details.
