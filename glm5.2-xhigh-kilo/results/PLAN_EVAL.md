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
| PRD-001 | Use Next.js latest stable runtime | critical | full | 2. Technology Decisions & Rationale | |
| PRD-002 | Use Supabase official client libraries | critical | full | 2. Technology Decisions & Rationale | |
| PRD-003 | Ship `.env.example` with required variables | critical | full | 4.1 `.env.example` | |
| PRD-004 | Ignore `.env*` secrets except example | important | full | 4.2 `.gitignore` essentials | |
| PRD-005 | Configure build through env without code edits | critical | full | 4.1 `.env.example`; 17. Infra Rider Compliance Checklist | |
| PRD-006 | Keep secrets out of repo and server-only | critical | full | 4.3 One-command DX; 11. API / Server Route Surface | |
| PRD-007 | Provide app, test, reset command scripts | critical | full | 4.3 One-command DX | |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | 5.3 Migrations & seed | |
| PRD-009 | Use one stable namespace per build | critical | full | 6. Identity & Isolation Model | |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | 5.4 Data access layer; 6. Identity & Isolation Model; 14. Testing Strategy | |
| PRD-011 | Attach every user record to `user_id` | critical | full | 5.1 Tables; 6. Identity & Isolation Model | |
| PRD-012 | Partition persisted data by namespace and user | critical | full | 5.1 Tables; 6. Identity & Isolation Model | |
| PRD-013 | Support documented dev auth injection, prod-gated | important | full | 4.1 `.env.example`; 6. Identity & Isolation Model | |
| PRD-014 | Real OAuth later needs no schema redesign | important | full | 5.2 Row-Level Security & isolation; 6. Identity & Isolation Model | |
| PRD-015 | Keep backend as persisted source of truth | critical | full | 12. Client Architecture & State | |
| PRD-016 | Make client cache safe to discard | critical | full | 12. Client Architecture & State | |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | full | 2. Technology Decisions & Rationale; 4. Environment & Configuration | |
| PRD-018 | Overlay saved user data on every show appearance | critical | full | 9.1 The `Show` render model | |
| PRD-019 | Support visible statuses plus hidden `Next` | important | full | 5.1 Tables; 10.1 Collection Home; 10.5 Show Detail | |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | full | 9.3 Saving triggers; 10.5 Show Detail | |
| PRD-021 | Support free-form multi-tag personal tag library | important | full | 5.1 Tables; 10.1 Collection Home | |
| PRD-022 | Define collection membership by assigned status | critical | full | 9.2 Collection membership | |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | full | 9.3 Saving triggers | |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | 9.4 Defaults when saving | |
| PRD-025 | Removing status deletes show and all My Data | critical | full | 9.5 Removal | |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | full | 7.3 Catalog -> store merge; 9.6 Re-add | |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | 5.1 Tables; 9.7 Timestamps | |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | full | 9.7 Timestamps; 13. Cross-Cutting Concerns | |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | full | 8.1 Surfaces & contracts; 9.9 AI persistence matrix; 10.5 Show Detail | |
| PRD-030 | Keep Ask and Alchemy state session-only | important | full | 9.9 AI persistence matrix; 12. Client Architecture & State | |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | full | 7.1 Interface; 8.2 Structured output, parsing & fallbacks; 13. Cross-Cutting Concerns | |
| PRD-032 | Show collection and rating tile indicators | important | full | 9.8 Tile indicators; 10.1 Collection Home | |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | full | 7.3 Catalog -> store merge; 13. Cross-Cutting Concerns; 15. Phase 9 | |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | full | 5.3 Migrations & seed; 13. Cross-Cutting Concerns | |
| PRD-035 | Persist synced settings, local settings, UI state | important | full | 5.1 Tables; 10.7 Settings & Your Data; 12. Client Architecture & State | |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | full | 5.1 Tables; 7.1 Interface; 7.2 Decode -> `Show` mapping rules | |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | full | 7.3 Catalog -> store merge; 9.7 Timestamps | |
| PRD-038 | Provide filters panel and main screen destinations | important | full | 3. Repository & Directory Structure; 10.1 Collection Home | |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | partial | 3. Repository & Directory Structure; 10. Feature Implementation Plan | The plan defines the Find surface and its modes, but it never specifies a persistent primary-navigation entry that remains available across the app shell. |
| PRD-040 | Keep Settings in persistent primary navigation | important | partial | 3. Repository & Directory Structure; 10.7 Settings & Your Data | The plan includes a Settings page, but it does not explicitly commit to keeping Settings in persistent primary navigation. |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | 3. Repository & Directory Structure; 10.2 Search; 10.3 Ask; 10.4 Alchemy | |
| PRD-042 | Show only library items matching active filters | important | full | 10.1 Collection Home; 11. API / Server Route Surface | |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | 10.1 Collection Home | |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | full | 10.1 Collection Home | |
| PRD-045 | Render poster, title, and My Data badges | important | full | 10.1 Collection Home; 9.8 Tile indicators | |
| PRD-046 | Provide empty-library and empty-filter states | detail | full | 10.1 Collection Home | |
| PRD-047 | Search by title or keywords | important | full | 7.1 Interface; 10.2 Search | |
| PRD-048 | Use poster grid with collection markers | important | full | 10.2 Search | |
| PRD-049 | Auto-open Search when setting is enabled | detail | full | 10.2 Search; 10.7 Settings & Your Data | |
| PRD-050 | Keep Search non-AI in tone | important | full | 8. AI Provider & Prompt Architecture; 10.2 Search | |
| PRD-051 | Preserve Show Detail narrative section order | important | full | 10.5 Show Detail | |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | full | 10.5 Show Detail | |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | full | 10.5 Show Detail | |
| PRD-054 | Place status/interest controls in toolbar | important | full | 10.5 Show Detail | |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | 9.4 Defaults when saving; 10.5 Show Detail | |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | 9.4 Defaults when saving; 10.5 Show Detail | |
| PRD-057 | Show overview early for fast scanning | important | full | 10.5 Show Detail | |
| PRD-058 | Scoop shows correct states and progressive feedback | important | full | 8.1 Surfaces & contracts; 8.3 Streaming; 10.5 Show Detail | |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | full | 8.1 Surfaces & contracts; 10.3 Ask; 10.5 Show Detail; 11. API / Server Route Surface | |
| PRD-060 | Include traditional recommendations strand | important | full | 10.5 Show Detail | |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | full | 10.5 Show Detail | |
| PRD-062 | Include streaming availability and person-linking credits | important | full | 10.5 Show Detail | |
| PRD-063 | Gate seasons to TV and financials to movies | important | full | 10.5 Show Detail | |
| PRD-064 | Keep primary actions early and page not overwhelming | important | partial | 10.5 Show Detail | The plan preserves early action placement through section order, but it does not specify the anti-clutter rules that keep the page from feeling overwhelming. |
| PRD-065 | Provide conversational Ask chat interface | important | full | 10.3 Ask | |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | partial | 8.1 Surfaces & contracts; 10.3 Ask | The plan covers confidence, brevity, and spoiler safety, but it does not commit to the direct-answer-first bar from the quality spec. |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | 10.3 Ask | |
| PRD-068 | Open Detail from mentions or Search fallback | important | full | 8.2 Structured output, parsing & fallbacks; 10.3 Ask | |
| PRD-069 | Show six random starter prompts with refresh | important | full | 10.3 Ask | |
| PRD-070 | Summarize older turns while preserving voice | important | full | 8.1 Surfaces & contracts; 10.3 Ask | |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | full | 10.3 Ask; 10.5 Show Detail; 11. API / Server Route Surface | |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | full | 8.1 Surfaces & contracts; 8.2 Structured output, parsing & fallbacks; 11. API / Server Route Surface | |
| PRD-073 | Retry malformed mention output once, then fallback | important | full | 8.2 Structured output, parsing & fallbacks | |
| PRD-074 | Redirect Ask back into TV/movie domain | important | full | 8. AI Provider & Prompt Architecture | |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | partial | 8.1 Surfaces & contracts; 10.4 Alchemy | The plan uses ingredient-oriented UX language, but it never makes "not genres" an explicit generation rule or rejection criterion. |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | partial | 8. AI Provider & Prompt Architecture; 8.1 Surfaces & contracts | The plan specifies bullets and 1-3 word concepts, but it does not make non-genericity an explicit acceptance rule for concept output. |
| PRD-077 | Order concepts by strongest aha and varied axes | important | full | 8.1 Surfaces & contracts | |
| PRD-078 | Require concept selection and guide ingredient picking | important | full | 10.4 Alchemy; 10.5 Show Detail | |
| PRD-079 | Return exactly five Explore Similar recommendations | important | full | 8.1 Surfaces & contracts; 10.5 Show Detail; 11. API / Server Route Surface | |
| PRD-080 | Support full Alchemy loop with chaining | important | full | 10.4 Alchemy; 15. Phase 7 | |
| PRD-081 | Clear downstream results when inputs change | important | full | 10.4 Alchemy | |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | full | 8.1 Surfaces & contracts | |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | full | 8.1 Surfaces & contracts | |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | partial | 8.4 Quality bar; 10.4 Alchemy | The plan references surprise and taste alignment in evaluation, but it does not define a concrete recommendation strategy that would reliably produce that bar in generation. |
| PRD-085 | Keep one consistent AI persona across surfaces | important | full | 8. AI Provider & Prompt Architecture | |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | full | 8. AI Provider & Prompt Architecture; 13. Cross-Cutting Concerns | |
| PRD-087 | Make AI warm, joyful, and light in critique | important | full | 8. AI Provider & Prompt Architecture | |
| PRD-088 | Structure Scoop as personal taste mini-review | important | full | 8.1 Surfaces & contracts | |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | full | 8.1 Surfaces & contracts; 10.3 Ask | |
| PRD-090 | Feed AI the right surface-specific context inputs | important | full | 8. AI Provider & Prompt Architecture; 10.3 Ask; 10.4 Alchemy; 10.5 Show Detail | |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | partial | 8.4 Quality bar; 14. Testing Strategy | The rubric and integrity gate are described, but AI quality validation is treated as optional instead of a required release-blocking check. |
| PRD-092 | Show person gallery, name, and bio | important | full | 7.1 Interface; 10.6 Person Detail | |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | full | 10.6 Person Detail | |
| PRD-094 | Group filmography by year | important | full | 10.6 Person Detail | |
| PRD-095 | Open Show Detail from selected credit | important | full | 10.6 Person Detail | |
| PRD-096 | Include font size and Search-on-launch settings | important | full | 10.7 Settings & Your Data | |
| PRD-097 | Support username, model, and API-key settings safely | important | full | 4.1 `.env.example`; 10.7 Settings & Your Data; 11. API / Server Route Surface | |
| PRD-098 | Export saved shows and My Data as zip | critical | full | 10.7 Settings & Your Data; 11. API / Server Route Surface | |
| PRD-099 | Encode export dates using ISO-8601 | important | full | 10.7 Settings & Your Data | |

## 3. Coverage Scores

Overall score:

```text
score = (91 x 1.0 + 8 x 0.5) / 99 x 100 = 95.96%
```

Score by severity tier:

```text
Critical:  (30 x 1.0 + 0 x 0.5) / 30 x 100 = 100.00%  (30.0 of 30 critical requirements)
Important: (59 x 1.0 + 8 x 0.5) / 67 x 100 = 94.03%  (63.0 of 67 important requirements)
Detail:    (2 x 1.0 + 0 x 0.5) / 2 x 100 = 100.00%  (2.0 of 2 detail requirements)
Overall:   95.96% (99 total requirements)
```

## 4. Top Gaps

- PRD-091 | `important` | Validate discovery with rubric and hard-fail integrity. This matters because the plan names the discovery rubric but treats it as optional, which creates a path for AI regressions in taste alignment or real-show integrity to ship without a release-blocking check.
- PRD-039 | `important` | Keep Find/Discover in persistent primary navigation. This matters because Find/Discover is the main entry point for Search, Ask, and Alchemy, and leaving persistence unspecified risks an app shell that makes core discovery workflows harder to reach.
- PRD-040 | `important` | Keep Settings in persistent primary navigation. This matters because export, model selection, API-key handling, and Search-on-launch settings are first-class flows, and a non-persistent Settings entry would weaken those core controls.
- PRD-075 | `important` | Treat concepts as taste ingredients, not genres. This matters because if concept generation drifts toward genre labels, Explore Similar and Alchemy lose the product's differentiating "taste DNA" behavior and collapse into generic recommendation mechanics.
- PRD-084 | `important` | Deliver surprising but defensible taste-aligned recommendations. This matters because the discovery surfaces can look compliant on paper while still feeling bland or obvious in use, which undermines one of the product's main reasons to exist.

## 5. Coverage Narrative

#### Overall Posture

This is a strong plan with no critical coverage misses and very good structural alignment to the PRD. The gaps are not in persistence, isolation, or core business rules; they are mostly in app-shell navigation specificity and in the strictness of AI behavior and quality enforcement.

#### Strength Clusters

The plan is strongest in Benchmark Runtime & Isolation, Collection Data & Persistence, and Show Detail & Relationship UX. Those areas are translated into concrete schema choices, domain rules, route surfaces, and feature flows, and the plan is especially precise about namespace isolation, per-field timestamps, auto-save/removal behavior, and the Detail page's major sections.

#### Weakness Clusters

The partial items cluster in two places. One cluster is the global shell, where Find/Discover and Settings exist as pages but are not explicitly specified as persistent primary-navigation entries. The larger cluster is AI behavioral specificity: concept semantics, Ask response posture, surprise/taste quality, and rubric enforcement are described directionally but not always locked down as hard implementation or release criteria.

#### Risk Assessment

If this plan were executed as-is, the most likely failure mode is not a broken data model; it is a product that works mechanically while feeling slightly off-spec in the discovery experience. A QA reviewer would likely notice first that AI outputs can drift toward generic concepts or non-validated recommendation quality, and that the navigation shell does not explicitly guarantee the always-available Find/Discover and Settings entry points called for by the PRD.

#### Remediation Guidance

The remaining work is mostly tighter specification, not new architecture. The plan needs an explicit navigation-shell contract for persistent primary navigation, plus stronger acceptance criteria for AI surfaces: direct-answer behavior in Ask, explicit non-genre/non-generic concept rules, and a non-optional discovery quality gate that makes real-show integrity and taste alignment release-blocking rather than aspirational.
