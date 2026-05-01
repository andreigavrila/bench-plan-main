# Implementation Plan: Personal Entertainment Companion Application

**Generated from:** Full review of `docs/prd/product_prd.md`, `infra_rider_prd.md`, and all supporting documents (`discovery_quality_bar.md`, `detail_page_experience.md`, `concept_system.md`, `ai_voice_personality.md`, `ai_prompting_context.md`, `storage-schema.md`, `storage-schema.ts`).

**Scope:** This plan covers a complete, production-ready implementation of the specified application using the benchmark baseline (Next.js + Supabase). It does not include code; it defines architecture, components, data flows, AI contracts, and delivery phases to ensure full fidelity to the PRD, quality bars, voice/personality, and infrastructure rider.

**Key Constraints Adhered To:**
- Name-, platform-, technology-agnostic PRD translated to concrete Next.js/Supabase implementation.
- Infra rider: namespace isolation, user_id scoping, dev auth injection, destructive test support, .env.example, one-command scripts, Supabase migrations.
- All data rules, auto-save behaviors, merge policies, AI persistence, and discovery quality dimensions.
- AI voice/persona consistency across surfaces.
- No implementation performed.

---

## 1. Project Initialization & Baseline Setup

### 1.1 Repository & Environment
- Initialize Next.js 15+ (App Router, TypeScript, ESLint, Tailwind, shadcn/ui or equivalent component library for rapid UI).
- Add Supabase JS client (`@supabase/supabase-js`).
- Create `.env.example` with:
  - `NEXT_PUBLIC_SUPABASE_URL`
  - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
  - `SUPABASE_SERVICE_ROLE_KEY` (server-only)
  - `TMDB_API_KEY` (or chosen catalog provider; e.g., TheMovieDB for external catalog)
  - `OPENAI_API_KEY` (or configurable AI provider; benchmark allows env injection)
  - `NAMESPACE_ID` (stable build identifier, e.g., `bench-run-2026-05`)
  - `DEFAULT_USER_ID` (for dev identity injection)
  - AI model selection vars.
- `.gitignore`: exclude `.env*`, `node_modules`, `.next`, Supabase local volumes if used.
- Package scripts (per rider):
  - `npm run dev`: starts Next.js dev server with hot reload.
  - `npm run build`: production build.
  - `npm test`: runs unit/integration/E2E tests.
  - `npm run test:reset`: clears test data for the active `NAMESPACE_ID` only (via Supabase RPC or admin delete scoped to namespace).
  - `npm run db:migrate`: applies Supabase migrations.
  - `npm run db:seed`: optional fixture loader scoped to namespace/user.
- Docker optional only (for local Supabase if chosen); primary path uses hosted Supabase or env-configured instance. Document both.
- Root layout: providers for Supabase client (browser + server), theme, toast notifications.

### 1.2 Database Foundation (Supabase)
- Create Supabase project (hosted preferred for benchmark agents).
- Migrations (in `supabase/migrations/`):
  - `0001_initial_schema.sql`: tables for `shows`, `cloud_settings`, `app_metadata` with RLS policies.
  - Columns exactly matching `storage-schema.ts` + additional `namespace_id` (text, indexed, part of composite keys/queries), `user_id` (text/uuid, required on all user-owned rows).
  - Enums: `show_type`, `my_status_type`, `my_interest_type`.
  - Indexes: on `(namespace_id, user_id, id)`, `(namespace_id, user_id, my_status)`, genres, dates for filters/sorting.
  - RLS: `namespace_id = current_setting('app.namespace_id')::text AND user_id = current_setting('app.user_id')::text` (set via server-side `SET` or JWT claims in dev/prod).
  - `shows` table: primary key `(namespace_id, user_id, id)` or surrogate + unique constraint. JSONB for `providerData` and `externalIds`.
  - Separate tables if needed: `user_settings` (1:1 with user), `ai_cache` (ephemeral or keyed by show+namespace).
- `AppMetadata` row: track `dataModelVersion` (start at 3, increment on changes).
- Seed script: creates default user + namespace test data without affecting other namespaces.
- Migration path: forward-only, idempotent; supports model upgrades without data loss (per PRD 5.11).

**Partitioning Rule:** Every query and mutation explicitly filters by `namespace_id` + `user_id`. Destructive ops (`test:reset`) target only current namespace.

---

## 2. Identity, Authentication & Isolation

### 2.1 Dev Identity Injection (Benchmark Mode)
- Middleware or server context: read `X-User-Id` header or env `DEFAULT_USER_ID` / `NAMESPACE_ID`.
- Provide a dev-only "Switch User" UI toggle (gated behind `NODE_ENV=development` or feature flag; disabled in prod builds).
- All Supabase clients (server actions, API routes, client components) inject `namespace_id` and `user_id` via:
  - Supabase `rpc` helpers or Postgres `SET app.namespace_id = '...'; SET app.user_id = '...';`.
  - Or pass as query params/JWT custom claims.
- Design: Replaceable by real OAuth (Google, etc.) later: auth layer abstraction (`getCurrentUser()`, `getNamespace()`) with no schema impact. OAuth flow adds `auth.users` integration + RLS using `auth.uid()`.

### 2.2 Multi-User Readiness
- Schema supports multiple `user_id` per namespace.
- UI initially single-user (default user), but code paths treat `user_id` as first-class.

---

## 3. External Catalog Integration Layer

### 3.1 Provider Abstraction
- Service: `CatalogService` (or `TMDBCatalogAdapter`).
- Methods:
  - `search(query: string, type?: 'movie'|'tv'): Promise<Show[]>`
  - `getDetails(id: string, type: ShowType): Promise<Show>` (full metadata + transient fields: cast, crew, videos, recommendations, similar, seasons, providers).
  - `getProviders(id, type, region='US')`: returns `ProviderData`.
  - `getPerson(id)`: for Person Detail.
- Mapping: Decode to internal `Show` shape per `storage-schema.md` merge rules (selectFirstNonEmpty for non-my fields).
- Caching: In-memory or Redis for hot details (24h); always re-merge on refresh. `detailsUpdateDate` updated.
- Fallback: If provider fails, graceful degradation (cached or error UI).

**Note:** PRD is provider-agnostic; choose TMDB (or equivalent) but abstract interface for future swaps.

---

## 4. AI Services Layer (Core "Heart")

### 4.1 Provider & Prompt Abstraction
- Configurable AI provider (OpenAI default, extensible to Anthropic/Groq).
- Central `AIService` with:
  - Model selection from `CloudSettings.aiModel`.
  - API key from `CloudSettings.aiApiKey` or env (never commit keys).
  - Consistent system persona injection (from `ai_voice_personality.md` and `ai_prompting_context.md`).
- Prompt templates (versioned, in `lib/prompts/`):
  - `scoop.prompt.ts`: structured mini-blog (personal take, stack-up, "The Scoop", fit/warnings, verdict). ~150-350 words. Spoiler-safe.
  - `ask.prompt.ts`: conversational, friend mode. Supports summarization of history (>10 turns).
  - `askWithMentions.prompt.ts`: structured output `{commentary, showList: "Title::extId::type;;..."}` for "mentioned shows" strip.
  - `concepts.prompt.ts`: 1-3 word evocative bullets (8 default), shared for Alchemy. Axes: structure, vibe, emotion, relationships, craft.
  - `recommendations.prompt.ts`: 5-6 real recs with concept-tied reasons. Real-show integrity enforced (title + extId + type).
- Guardrails: Domain enforcement (TV/movies only), opinionated honesty, vibe-first, specific not generic. Retry on parse failure for structured outputs.
- Context inputs: user library snapshot (My Data), current show, selected concepts, session history.

### 4.2 Feature-Specific AI Contracts
- **Scoop ("The Scoop")**: On-demand from Detail. Cache 4h (`aiScoopUpdateDate`). Persist only if show in collection. Progressive streaming UI ("Generating...").
- **Ask / Chat**: Session context (short-term memory + summary). Mentioned shows row (parse `showList`, resolve via Catalog or handoff to Search). Starter prompts (80 from opus, welcome view).
- **Concepts (Explore Similar / Alchemy)**: Single-show or multi-show (shared). 1-3 words, no explanations, diverse axes, ordered by strength. Selection chips (max 8 for Alchemy).
- **Recommendations (Explore/Alchemy)**: Grounded to concepts. Real catalog resolution (lookup by extId or fuzzy title match). Reasons name matching concepts. Counts: 5 for Explore, 6 for Alchemy. Recent bias + hidden gems.
- Quality bar enforcement (per `discovery_quality_bar.md`): Voice adherence, taste alignment, surprise without betrayal, specificity, real-show integrity (must pass =2). Use golden-set style regression in tests later.

**Persistence:** AI Scoop yes (if collected); chat/Alchemy results session-only (clear on leave/reset).

---

## 5. Data Layer & Business Rules Implementation

### 5.1 Show Storage & Merge Logic
- Supabase table `shows` mirrors `Show` interface + `namespace_id`, `user_id`.
- `ShowRepository`:
  - `saveOrMerge(show: Partial<Show>, source: 'catalog' | 'user')`: implements merge policy (5.5, storage-schema.md):
    - Non-my fields: `selectFirstNonEmpty(new, old)`.
    - My fields: timestamp newer wins (`my*UpdateDate`).
    - `detailsUpdateDate` = now; `creationDate` immutable.
  - `getById(id, userId, namespace)`: always returns user-overlaid version.
  - `remove(showId)`: delete row + clear all My Data (with confirmation warning, optional `hideStatusRemovalConfirmation`).
- Auto-save triggers (5.2): Any status set, interest chip, rating unsaved show → Done, tag on unsaved → Later+Interested. Default: Later+Interested (except rating → Done).
- Collection membership: `myStatus != null`.
- Timestamps: ISO strings, used for sort (recent first), conflict resolution.
- Export: Settings → JSON zip of all shows + My Data (ISO dates) for current user/namespace.

### 5.2 Settings & Metadata
- `cloud_settings` table (synced): username, api keys (optional), aiModel, version (for conflicts).
- Local (per-device, non-synced): `autoSearch`, `fontSize`, UI state (`lastSelectedFilter`, hide confirmation).
- `app_metadata`: version for migrations.

---

## 6. Core Feature Breakdown & UI Components

### 6.1 Navigation & Layout (Next.js App Router)
- Root: Sidebar (Filters) + Main content + Bottom/Top nav for Find/Settings.
- Persistent: Find (hub), Settings.
- Filters panel (left):
  - All Shows.
  - Per-tag filters + "No tags".
  - Data filters: genre, decade, communityScore ranges.
  - Media toggle: All/Movies/TV.
  - Status filters (optional extension).
- State: `FilterConfiguration` persisted in local/UI state. React context or Zustand for global filter + selected show.

### 6.2 Collection Home (/)
- Grouped sections:
  1. Active (prominent tiles).
  2. Excited (Later+Excited).
  3. Interested (Later+Interested).
  4. Other (collapsed: Wait, Quit, Done, unclassified Later).
- Media toggle + filter chips.
- Tiles: poster, title, in-collection badge, rating badge. Click → Detail.
- Empty: prompt to Find/Ask.
- Infinite scroll or pagination if large library.

### 6.3 Find Hub (/find)
- Mode switcher: Search | Ask | Alchemy (tabs or segmented control).
- **Search**: Input → live catalog results grid (tiles with in-collection mark). Select → Detail. "Search on launch" setting.
- **Ask**: Chat UI (messages list + input). Welcome: 6 random starter prompts (refreshable). Inline mentions → horizontal strip of selectable Show tiles (resolve or Search handoff). Context: seed from Detail "Ask about…". History summarization after ~10 turns.
- **Alchemy**:
  1. Select 2+ shows (library + catalog search picker).
  2. "Conceptualize Shows" → fetch concepts.
  3. Select 1-8 concept chips (clear results on change).
  4. "ALCHEMIZE!" → 6 recs with reasons (concept-grounded).
  5. "More Alchemy!" chain (use results as new inputs).
  - UX: step cards, backtracking allowed, "pick ingredients you want more of" hints.

### 6.4 Show Detail (/shows/[id])
- Narrative hierarchy (preserve order):
  1. Header media carousel (backdrops > posters > logos; trailers inline/playable, graceful fallback).
  2. Core facts (year, runtime/seasons/episodes) + community score bar.
  3. My Tags chips + picker (add triggers auto-save).
  4. Overview + "Give me the scoop!" / "Show the scoop" toggle (streams "The Scoop", 4h freshness).
  5. "Ask about this show" CTA (handoff to Ask with seed).
  6. Genres/languages.
  7. Traditional recs strand.
  8. Explore Similar: "Get Concepts" → chips → "Explore Shows" → 5 recs.
  9. "Stream It" providers (by region).
  10. Cast & Crew horizontal (→ Person Detail).
  11. Seasons (TV).
  12. Budget/Revenue (movies).
- My Relationship toolbar (sticky or prominent): Status chips (Interested/Excited map to Later+Interest), Rating slider (unsaved → auto Done), Status reselect → removal confirmation (with "don't ask again" option).
- Unsaved show: Scoop ephemeral (persist only on save). All actions follow auto-save rules.
- TV vs Movie: conditional strands.

### 6.5 Person Detail (/people/[id])
- Header: image + name + bio.
- Analytics: charts (avg ratings, top genres, projects-by-year) – use Recharts or Chart.js.
- Filmography: grouped by year, clickable credits → Show Detail.
- Gallery: images.

### 6.6 Settings (/settings)
- App: font size (XS–XXL, affects readability), "Search on launch".
- User: editable username (synced).
- AI: provider key input (optional, env fallback), model selector (synced).
- Integrations: catalog API key (synced).
- Your Data: "Export My Data" → .zip (JSON of shows + metadata, scoped to user/namespace). Import noted as future (open question).
- Danger: Reset namespace data (dev only).

---

## 7. State Management, Caching & Performance

- Client: React Context + custom hooks (`useShows`, `useFilters`, `useAI`) or lightweight Zustand for global.
- Server: Next.js Server Components for initial data, Server Actions for mutations (Supabase calls).
- Caching: React Query / SWR for catalog/AI fetches. 4h for Scoop. Transient fields re-fetched on demand.
- Optimistic updates: status/rating/tag changes (rollback on error).
- Media: Next Image optimization, lazy posters, responsive.
- Accessibility: ARIA, keyboard nav, high-contrast font scaling.

---

## 8. Testing Strategy (Per Rider & Quality Bar)

- Unit: Repositories, merge logic, prompt builders, catalog mappers. (Jest/Vitest).
- Integration: Supabase queries with namespace scoping. AI service contracts (mock providers).
- E2E: Playwright – key journeys (build collection, Ask discovery, Alchemy chain, Detail maintenance, Export).
- Destructive: `test:reset` clears only namespace; tests create isolated data.
- AI Quality: Snapshot tests for voice (prompt outputs), manual golden-set scoring (voice ≥1, taste ≥1, real-show=2, total ≥7/10). Regression on model changes.
- Data continuity: Upgrade simulation tests (model v3 → v4 preserves My Data).
- Coverage: 80%+ on core logic; benchmark runs must pass without data collisions across parallel namespaces.

---

## 9. Phased Implementation Roadmap

**Phase 0: Foundation (1-2 days)**
- Next.js + Supabase project, env, migrations, namespace/user injection, basic auth dev gate.
- CatalogService skeleton + TMDB adapter (search/details).
- Basic layout + routing (Home, Find, Detail stubs).

**Phase 1: Core Collection & Persistence (3-4 days)**
- Show model, repository with merge/auto-save rules.
- Home: filters, status grouping, tiles, CRUD via Detail.
- Detail: header, facts, status/rating/tags, overview, traditional recs, providers.
- Settings + Export.
- Tests for business rules.

**Phase 2: Discovery Surfaces (4-5 days)**
- Search integration.
- Ask chat (basic + mentions strip + starters).
- Explore Similar (concepts + recs).
- Person Detail.
- Quality bar validation on AI outputs.

**Phase 3: Alchemy & Advanced AI (3-4 days)**
- Alchemy flow end-to-end (select, conceptualize, alchemize, chain).
- Full prompt suite + persona consistency.
- Scoop generation + caching.
- Session management, summarization.

**Phase 4: Polish, Settings, Polish & Benchmark Hardening (2-3 days)**
- Settings sync, font scaling, import notes.
- Performance, accessibility, empty states, error handling.
- Destructive test scripts, namespace isolation verification.
- Full E2E suite + manual quality scoring.
- Docs: README with run/reset instructions, .env setup.

**Total Estimate:** 12-18 developer-days for MVP parity. Incremental commits with tests at each phase.

---

## 10. Open Questions Addressed in Plan (from PRD)
- Next status: Data model includes but UI-hidden (future surface as first-class).
- Custom lists: Use tags (current); named lists future.
- Scoop on unsaved: Ephemeral (per spec); persist only on save.
- Unrated state: Explicit nil vs "unrated" – treat as optional `myScore=null`.
- Import: Documented as open (UI stub + future task).
- Alchemy session save: Future (current session-only).
- myStatus filters: Supported in data, optional sidebar addition.

**Risks & Mitigations:**
- AI hallucination / non-real recs: Strict ID+title resolution + fallback to Search; quality rubric in CI.
- Catalog rate limits: Caching + backoff.
- Supabase RLS complexity: Server-only privileged ops; thorough test scoping.
- Voice drift: Centralized prompt lib + example-based tests.

**Success Criteria (from rider + PRD):**
- One-command run after `cp .env.example .env` + key fill.
- Namespace-isolated repeatable builds/tests.
- All user records scoped to `(namespace_id, user_id)`.
- Full feature parity: collection maintenance, taste-aware discovery (Ask/Alchemy/Explore), actionable recs, data export.
- AI outputs pass quality dimensions consistently.
- Ready for OAuth migration (no schema change).

This plan ensures the rebuilt application captures both the functional scope and the "heart" (voice, concepts, emotional design) defined across all PRD documents.

**Deliverable complete.** `results/PLAN.md` written. No source code or modifications to application files were made.
