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
| PRD-001 | Use Next.js latest stable runtime | critical | full | Overview > Tech Stack | |
| PRD-002 | Use Supabase official client libraries | critical | partial | Overview > Tech Stack; Phase 1 > Project setup | The plan commits to Supabase, but it never explicitly says the implementation must use Supabase's official client libraries. |
| PRD-003 | Ship `.env.example` with required variables | critical | full | 2.1 Environment Configuration | |
| PRD-004 | Ignore `.env*` secrets except example | important | partial | Phase 1 > Project setup | The plan says to create `.gitignore`, but it does not spell out the required `.env*` ignore pattern with the `.env.example` exception. |
| PRD-005 | Configure build through env without code edits | critical | full | 2.1 Environment Configuration; 12. Success Criteria | |
| PRD-006 | Keep secrets out of repo and server-only | critical | partial | 2.1 Environment Configuration | The plan defines env vars, but it never states that secrets must never be committed and that elevated keys remain server-only. |
| PRD-007 | Provide app, test, reset command scripts | critical | full | 8. Scripts & Commands | |
| PRD-008 | Include repeatable schema evolution artifacts | critical | full | Phase 1 > Database migrations; 8. Scripts & Commands | |
| PRD-009 | Use one stable namespace per build | critical | full | 2.1 Environment Configuration; 2.2 Namespace Isolation Middleware | |
| PRD-010 | Isolate namespaces and scope destructive resets | critical | full | 2.2 Namespace Isolation Middleware; 7.3 Namespace Isolation Tests; 8. Scripts & Commands | |
| PRD-011 | Attach every user record to `user_id` | critical | full | 1.2 Supabase Schema; 11. Critical Reminders | |
| PRD-012 | Partition persisted data by namespace and user | critical | full | 1.2 Supabase Schema; 2.2 Namespace Isolation Middleware | |
| PRD-013 | Support documented dev auth injection, prod-gated | important | partial | 2.3 Dev Identity Injection | The plan covers a dev identity mechanism and production gating, but it does not include the required documentation work for that mechanism. |
| PRD-014 | Real OAuth later needs no schema redesign | important | full | 1.2 Supabase Schema; 12. Success Criteria | |
| PRD-015 | Keep backend as persisted source of truth | critical | full | 11. Critical Reminders | |
| PRD-016 | Make client cache safe to discard | critical | full | 11. Critical Reminders | |
| PRD-017 | Avoid Docker requirement for cloud-agent compatibility | important | missing | none | The plan never states that Docker must remain optional or that the hosted/cloud-agent path cannot depend on containers. |
| PRD-018 | Overlay saved user data on every show appearance | critical | full | 6.1 User's Version Precedence | |
| PRD-019 | Support visible statuses plus hidden `Next` | important | partial | 1.1 Core Entities; Phase 2 > Collection Home page | The plan carries `next` in the schema, but it does not explicitly define it as data-model-only while keeping the surfaced status set separate. |
| PRD-020 | Map Interested/Excited chips to Later interest | critical | full | Phase 2 > Collection Home page; 5.2 Saving Triggers; 5.3 Default Values on Save | |
| PRD-021 | Support free-form multi-tag personal tag library | important | full | Phase 2 > Show Detail page; Phase 3 > Sidebar/Filter panel | |
| PRD-022 | Define collection membership by assigned status | critical | full | 5.1 Collection Membership | |
| PRD-023 | Save shows from status, interest, rating, tagging | critical | full | 5.2 Saving Triggers; Phase 2 > Auto-save triggers | |
| PRD-024 | Default save to Later/Interested except rating-save Done | critical | full | 5.3 Default Values on Save; Phase 2 > Auto-save triggers | |
| PRD-025 | Removing status deletes show and all My Data | critical | full | 5.4 Remove from Collection | |
| PRD-026 | Re-add preserves My Data and refreshes public data | critical | full | 5.5 Re-add Same Show | |
| PRD-027 | Track per-field My Data modification timestamps | critical | full | 1.1 Core Entities; 1.2 Supabase Schema | |
| PRD-028 | Use timestamps for sorting, sync, freshness | important | partial | 1.3 Merge Rules; 5.5 Re-add Same Show; 6.2 Data Sync & Integrity; 5.1 AI Scoop | The plan uses timestamps for sync and Scoop freshness, but it does not turn sorting behavior into a concrete task or rule. |
| PRD-029 | Persist Scoop only for saved shows, 4h freshness | critical | full | 5.1 AI Scoop > Scoop generation | |
| PRD-030 | Keep Ask and Alchemy state session-only | important | partial | 1.1 Core Entities; 5.2 Ask; 5.5 Alchemy | The plan implies ephemeral AI sessions by omission from the persistence model, but it never explicitly states that Ask and Alchemy state must clear when leaving or resetting those flows. |
| PRD-031 | Resolve AI recommendations to real selectable shows | critical | full | 4.3 Real-Show Resolution; 11. Critical Reminders | |
| PRD-032 | Show collection and rating tile indicators | important | full | Phase 2 > Collection Home page; 5.6 Tile Indicators | |
| PRD-033 | Sync libraries/settings consistently and merge duplicates | important | full | 6.2 Data Sync & Integrity | |
| PRD-034 | Preserve saved libraries across data-model upgrades | critical | full | 6.3 Data Continuity Across Versions | |
| PRD-035 | Persist synced settings, local settings, UI state | important | partial | 1.1 CloudSettings Entity; Phase 7 > Settings page; 5.4 Remove from Collection | The plan covers synced settings and one UI preference, but it does not explicitly plan local settings/UI-state persistence such as last filter and persisted confirmation behavior. |
| PRD-036 | Keep provider IDs persisted and detail fetches transient | important | partial | 1.1 Core Entities; Phase 1 > Catalog API integration; Phase 2 > Show Detail page | The plan treats detail data as transient and persists provider data, but it never constrains provider persistence to IDs-only. |
| PRD-037 | Merge catalog fields safely and maintain timestamps | critical | full | 1.3 Merge Rules | |
| PRD-038 | Provide filters panel and main screen destinations | important | full | Phase 3 > Sidebar/Filter panel; Phase 3 > Navigation structure | |
| PRD-039 | Keep Find/Discover in persistent primary navigation | important | full | 3. App Navigation structure; 9. File Structure | |
| PRD-040 | Keep Settings in persistent primary navigation | important | full | Phase 3 > Navigation structure; 9. File Structure | |
| PRD-041 | Offer Search, Ask, Alchemy discover modes | important | full | Phase 3 > Navigation structure; Phase 4; Phase 5.2; Phase 5.5 | |
| PRD-042 | Show only library items matching active filters | important | full | Phase 2 > Collection Home page; Phase 3 > Sidebar/Filter panel | |
| PRD-043 | Group home into Active, Excited, Interested, Others | important | full | Phase 2 > Collection Home page | |
| PRD-044 | Support All, tag, genre, decade, score, media filters | important | full | Phase 3 > Sidebar/Filter panel | |
| PRD-045 | Render poster, title, and My Data badges | important | full | Phase 2 > Collection Home page | |
| PRD-046 | Provide empty-library and empty-filter states | detail | full | Phase 2 > Collection Home page | |
| PRD-047 | Search by title or keywords | important | full | Phase 4 > Search functionality | |
| PRD-048 | Use poster grid with collection markers | important | full | Phase 4 > Search functionality | |
| PRD-049 | Auto-open Search when setting is enabled | detail | full | Phase 4 > Search functionality; Phase 7 > Settings page | |
| PRD-050 | Keep Search non-AI in tone | important | missing | none | The plan defines Search behavior, but it never states that Search should remain a straightforward non-AI surface. |
| PRD-051 | Preserve Show Detail narrative section order | important | partial | Phase 2 > Show Detail page; Phase 5.4 Explore Similar; Phase 5.2 Ask About a Show | The plan covers most detail-page features, but it does not preserve or call out the exact narrative section order from the spec. |
| PRD-052 | Prioritize motion-rich header with graceful fallback | important | partial | Phase 2 > Show Detail page | The plan includes a media carousel, but it does not specify motion-first behavior with graceful poster/backdrop fallback. |
| PRD-053 | Surface year, runtime/seasons, and community score early | important | full | Phase 2 > Show Detail page | |
| PRD-054 | Place status/interest controls in toolbar | important | full | Phase 2 > Show Detail page | |
| PRD-055 | Auto-save unsaved tagged show as Later/Interested | critical | full | Phase 2 > Auto-save triggers | |
| PRD-056 | Auto-save unsaved rated show as Done | critical | full | Phase 2 > Auto-save triggers | |
| PRD-057 | Show overview early for fast scanning | important | partial | Phase 2 > Show Detail page | The plan includes an overview section, but it does not explicitly commit to keeping it early and optimized for fast scanning. |
| PRD-058 | Scoop shows correct states and progressive feedback | important | full | Phase 5.1 AI Scoop > Scoop generation | |
| PRD-059 | Ask-about-show deep-link seeds Ask context | important | full | Phase 5.2 > Ask About a Show | |
| PRD-060 | Include traditional recommendations strand | important | missing | none | The plan never adds the non-AI traditional recommendations strand to the detail page. |
| PRD-061 | Explore Similar uses CTA-first concept flow | important | partial | Phase 5.4 Explore Similar > Flow | The plan defines the Explore Similar sequence, but it does not capture the CTA-first/empty-state behavior from the detail-page experience spec. |
| PRD-062 | Include streaming availability and person-linking credits | important | full | Phase 2 > Show Detail page; Phase 6 > Person profile | |
| PRD-063 | Gate seasons to TV and financials to movies | important | full | Phase 2 > Show Detail page | |
| PRD-064 | Keep primary actions early and page not overwhelming | important | partial | Phase 2 > Show Detail page | The plan lists the main controls, but it does not turn the busyness-versus-power guidance into concrete layout or acceptance criteria. |
| PRD-065 | Provide conversational Ask chat interface | important | full | Phase 5.2 > Chat UI | |
| PRD-066 | Answer directly with confident, spoiler-safe recommendations | important | full | Phase 5.2 > Voice; 4.1 Prompt Design > Ask Prompt | |
| PRD-067 | Show horizontal mentioned-shows strip from chat | important | full | Phase 5.2 > Chat UI | |
| PRD-068 | Open Detail from mentions or Search fallback | important | full | Phase 5.2 > Chat UI; 4.3 Real-Show Resolution | |
| PRD-069 | Show six random starter prompts with refresh | important | full | Phase 5.2 > Chat UI | |
| PRD-070 | Summarize older turns while preserving voice | important | partial | Phase 5.2 > Chat UI | The plan includes summarization after older turns accumulate, but it does not require summaries to preserve the same persona/voice. |
| PRD-071 | Seed Ask-about-show sessions with show handoff | important | full | Phase 5.2 > Ask About a Show | |
| PRD-072 | Emit `commentary` plus exact `showList` contract | critical | full | Phase 5.2 > Structured output; 4.1 Prompt Design > Ask Prompt | |
| PRD-073 | Retry malformed mention output once, then fallback | important | missing | none | The plan defines the structured contract, but it never plans the required retry-then-fallback behavior for malformed output. |
| PRD-074 | Redirect Ask back into TV/movie domain | important | partial | 4.1 Prompt Design > Shared Rules | The plan keeps Ask in the TV/movie domain, but it does not specify the redirect/handoff behavior when a user asks for something outside that domain. |
| PRD-075 | Treat concepts as taste ingredients, not genres | important | partial | Phase 5.3 > Concept quality rules | The plan covers specificity and multiple concept axes, but it never explicitly frames concepts as taste ingredients rather than genre labels. |
| PRD-076 | Return bullet-only, 1-3 word, non-generic concepts | important | full | Phase 5.3 > Get Concepts; 4.1 Prompt Design > Concepts Prompt | |
| PRD-077 | Order concepts by strongest aha and varied axes | important | full | Phase 5.3 > Concept quality rules | |
| PRD-078 | Require concept selection and guide ingredient picking | important | partial | Phase 5.4 Explore Similar > Flow; Phase 5.5 Alchemy > Flow | The plan includes concept selection, but it does not add the UX guidance and explicit selection enforcement described in the concept spec. |
| PRD-079 | Return exactly five Explore Similar recommendations | important | full | Phase 5.4 Explore Similar > Flow | |
| PRD-080 | Support full Alchemy loop with chaining | important | full | Phase 5.5 Alchemy > Flow | |
| PRD-081 | Clear downstream results when inputs change | important | partial | Phase 5.5 Alchemy > UX | The plan allows backtracking, but it does not explicitly say that changed inputs clear concepts/results downstream. |
| PRD-082 | Generate shared multi-show concepts with larger option pool | important | partial | Phase 5.3 > Get Concepts | The plan requires shared multi-show concepts, but it does not preserve the spec's larger option pool for multi-show generation. |
| PRD-083 | Cite selected concepts in concise recommendation reasons | important | full | Phase 5.4 Explore Similar > Flow; 4.1 Prompt Design > Concept Recs Prompt | |
| PRD-084 | Deliver surprising but defensible taste-aligned recommendations | important | partial | 7.4 AI Quality Tests | The plan tests for surprise and taste alignment, but it does not convert that quality bar into concrete recommendation-generation requirements. |
| PRD-085 | Keep one consistent AI persona across surfaces | important | partial | 4.1 Prompt Design; Phase 5.1 > Voice implementation; Phase 5.2 > Voice | The plan defines shared AI rules and per-surface prompts, but it never explicitly commits to one consistent cross-surface persona contract. |
| PRD-086 | Enforce shared AI guardrails across all surfaces | critical | full | 4.1 Prompt Design > Shared Rules; 6.4 Spoiler Safety | |
| PRD-087 | Make AI warm, joyful, and light in critique | important | partial | Phase 5.1 > Voice implementation; Phase 5.2 > Voice | The plan captures warmth and opinionation, but it does not explicitly preserve the joy-forward and light-in-critique behavior from the voice spec. |
| PRD-088 | Structure Scoop as personal taste mini-review | important | full | Phase 5.1 AI Scoop > Scoop generation; 4.1 Prompt Design > Scoop Prompt | |
| PRD-089 | Keep Ask brisk and dialogue-like by default | important | full | 4.1 Prompt Design > Ask Prompt; Phase 5.2 > Chat UI | |
| PRD-090 | Feed AI the right surface-specific context inputs | important | full | 4.2 Context Injection | |
| PRD-091 | Validate discovery with rubric and hard-fail integrity | important | partial | 7.4 AI Quality Tests | The plan lists the rubric dimensions, but it does not define pass thresholds or an explicit hard-fail rule for real-show integrity. |
| PRD-092 | Show person gallery, name, and bio | important | full | Phase 6 > Person profile | |
| PRD-093 | Include ratings, genres, and projects-by-year analytics | important | full | Phase 6 > Person profile | |
| PRD-094 | Group filmography by year | important | full | Phase 6 > Person profile | |
| PRD-095 | Open Show Detail from selected credit | important | full | Phase 6 > Person profile | |
| PRD-096 | Include font size and Search-on-launch settings | important | full | Phase 7 > Settings page | |
| PRD-097 | Support username, model, and API-key settings safely | important | partial | Phase 7 > Settings page; 2.1 Environment Configuration | The plan includes the settings fields, but it does not define safe storage/handling rules for user-entered API keys. |
| PRD-098 | Export saved shows and My Data as zip | critical | full | Phase 7 > Export/Backup | |
| PRD-099 | Encode export dates using ISO-8601 | important | full | Phase 7 > Export/Backup | |

## 3. Coverage Scores

Overall score = (70 × 1.0 + 25 × 0.5) / 99 × 100 = 83.33%

Critical:  (28 × 1.0 + 2 × 0.5) / 30 × 100 = 96.67%  (29 of 30 critical requirements)
Important: (40 × 1.0 + 23 × 0.5) / 67 × 100 = 76.87%  (51.5 of 67 important requirements)
Detail:    (2 × 1.0 + 0 × 0.5) / 2 × 100 = 100.00%  (2 of 2 detail requirements)
Overall:   83.33% (99 total requirements)

## 4. Top Gaps

1. PRD-006 | `critical` | Keep secrets out of repo and server-only. This matters because the plan introduces both public and elevated credentials but never defines the repo hygiene and server-only boundary that prevent an unsafe implementation.
2. PRD-002 | `critical` | Use Supabase official client libraries. This matters because the infra rider freezes the integration path for the benchmark round, and leaving the client choice implicit creates avoidable implementation drift at the persistence boundary.
3. PRD-017 | `important` | Avoid Docker requirement for cloud-agent compatibility. This matters because a build that silently depends on Docker can fail the benchmark execution environment even if the app logic is otherwise correct.
4. PRD-073 | `important` | Retry malformed mention output once, then fallback. This matters because the Ask surface depends on structured AI output, and without the retry/fallback path a single malformed response can break mention rendering and navigation.
5. PRD-060 | `important` | Include traditional recommendations strand. This matters because it removes the non-AI discovery path from Show Detail, weakening one of the page's primary low-friction recommendation affordances.

## 5. Coverage Narrative

#### Overall Posture

This is a structurally strong plan with near-complete critical coverage and a solid implementation sequence, but it still has several important-tier holes in operational constraints, detail-page UX fidelity, and AI behavioral contracts. It is much closer to executable than to speculative, yet it would still miss benchmark-relevant polish and a few non-happy-path behaviors if implemented as written.

#### Strength Clusters

The plan is strongest in Benchmark Runtime & Isolation at the schema/partitioning level, Collection Data & Persistence, Collection Home & Search happy paths, Ask Chat core functionality, Person Detail, and Settings & Export. It also does a good job translating the PRD's data model, merge rules, save triggers, namespace scoping, and major AI feature surfaces into concrete implementation phases.

#### Weakness Clusters

The gaps cluster around important-tier behavioral detail rather than broad feature absence. The heaviest concentrations are in Show Detail & Relationship UX, Concepts/Alchemy UX nuance, and AI Voice/guardrail polish, with a smaller but high-impact operational cluster in benchmark runtime/security expectations. In other words, the plan covers what to build more consistently than it covers exact UX posture, fallback logic, and constraint handling.

#### Risk Assessment

If this plan were executed as-is, the most likely outcome is a functional app that passes happy-path demos but falls short under evaluator scrutiny and QA edge cases. The first issues a reviewer would notice are missing benchmark-runtime constraints like Docker optionality and secrets boundaries, plus AI-surface misses such as malformed-output fallback, non-AI Search tone, and the missing traditional recommendations strand on Show Detail.

#### Remediation Guidance

The remaining work is mostly specification tightening, not wholesale replanning. The plan needs explicit acceptance criteria for secrets handling, Docker/cloud-agent posture, AI output fallback, persona consistency, Search tone, and Detail-page section behavior; it also needs a few missing UX-state rules around session-only AI data, concept-selection guidance, and downstream-reset behavior when Alchemy inputs change.
