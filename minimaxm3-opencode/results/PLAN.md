# Implementation Plan — Personal TV + Movie Companion (Benchmark Build)

> **Scope of this document:** A complete, end-to-end implementation plan for a Next.js + Supabase rebuild of the personal TV/movie companion described in `docs/prd/product_prd.md`, with execution constraints from `docs/prd/infra_rider_prd.md` and behavior/voice contracts captured in `docs/prd/supporting_docs/`.
>
> This is a **plan**, not code. The build follows the **fractal architecture** from `INSTRUCTIONS.md` (Pages → Features → Sub-Features, humble components, co-location).
>
> **Deliverable target:** a single, coherent, immediately-executable plan a small team can pick up and ship in milestones.

---

## 0. Plan orientation

### 0.1 Product in one paragraph
A personal collection app for shows and movies where every saved item carries **My Status / My Interest / My Tags / My Rating / AI Scoop**. The collection powers three AI surfaces — **Ask** (chat), **Alchemy** (multi-show concept blending) and **Explore Similar** (single-show concepts) — all of which must resolve to real, selectable catalog items, and all of which share a single taste-aware, spoiler-safe, opinionated voice defined in `ai_voice_personality.md` and `ai_prompting_context.md`.

### 0.2 Tech baseline (locked by infra rider)
- **Next.js (App Router, latest stable)** — UI + server boundary, server routes for AI and catalog calls.
- **Supabase** — persistence layer (hosted preferred, local optional). No Docker required.
- **Identity:** dev-only `X-User-Id` injection (or local dev selector) — every user-owned record carries `user_id`; replacing it with real OAuth later must not require schema changes.
- **Isolation:** every persisted record carries `namespace_id` (a build-level primitive, not a user concept). Test data can be created/destroyed inside a namespace without global teardown.
- **Config:** `.env.example` + `.gitignore` (no committed secrets). Browser code uses **anon key only**; service role is server-only.
- **Repo scripts:** `npm run dev`, `npm test`, `npm run test:reset` (names illustrative).

### 0.3 Architecture pattern (locked by INSTRUCTIONS.md)
Fractal: **Pages → Features → Sub-Features**. Each feature owns its hooks/utils/child features. TSX is markup + binding only; logic lives in `useXxxLogic()` hooks. No magic numbers, no inline styles, no `index.tsx`. Styling through design tokens.

### 0.4 Build order (one-glance)
1. **Foundation** — repo scaffold, env, supabase client, namespace/user injection, migrations, design tokens, primitives, storage layer.
2. **Collection core** — Show model, merge logic, library home with filters, Show Detail skeleton, status/interest/tags/rating auto-save.
3. **External catalog integration** — provider client, search, detail hydration, recommendations/similar, providers, credits, seasons, budget/revenue.
4. **AI surfaces** — shared prompt engine + persona, Scoop, Ask (chat + mentioned shows), Concepts, Explore Similar, Alchemy.
5. **Person Detail + analytics** — bio, gallery, filmography by year, light charts.
6. **Settings + export** — username, font size, autoSearch, API keys, model selection, Export My Data (zip + JSON).
7. **Quality + benchmark gates** — tests, namespace reset, `.env.example`, scripts, smoke tests, evaluation criteria coverage.

---

## 1. Repository layout

```
.
├── .env.example
├── .gitignore
├── README.md
├── package.json
├── tsconfig.json
├── next.config.mjs
├── eslint.config.mjs
├── supabase/
│   ├── migrations/                # SQL migrations (timestamped)
│   └── seed.sql                   # Optional: a few canonical shows for smoke
├── scripts/
│   ├── dev-identity.mjs           # Dev-only "login as user" helper
│   ├── namespace-reset.mjs        # Drops all rows in (namespace_id) scope
│   └── export-data.mjs            # Builds the Export My Data .zip
├── src/
│   ├── app/                       # Next.js App Router
│   │   ├── layout.tsx
│   │   ├── page.tsx               # Library Home
│   │   ├── find/                  # Find/Discover hub
│   │   │   ├── page.tsx           # Mode switcher
│   │   │   ├── search/page.tsx
│   │   │   ├── ask/page.tsx
│   │   │   └── alchemy/page.tsx
│   │   ├── show/[id]/page.tsx
│   │   ├── person/[id]/page.tsx
│   │   ├── settings/page.tsx
│   │   └── api/
│   │       ├── catalog/...        # Catalog proxy/search/detail routes
│   │       ├── ai/...             # AI surface routes
│   │       ├── shows/...          # Library CRUD (server)
│   │       ├── settings/...       # Cloud settings
│   │       └── export/route.ts
│   ├── config/                    # Env, feature flags, constants
│   ├── theme/                     # Design tokens (colors, spacing, type)
│   ├── components/                # Cross-page primitives
│   ├── hooks/                     # Global hooks (useUser, useNamespace, …)
│   ├── utils/                     # Global pure utilities
│   ├── lib/
│   │   ├── supabase/              # Server + browser clients (anon only on client)
│   │   ├── auth/                  # Dev identity injection
│   │   ├── catalog/               # External catalog client
│   │   ├── ai/                    # AI engine (shared by all surfaces)
│   │   ├── storage/               # Show merge, export, import
│   │   └── domain/                # Types: Show, MyStatus, MyInterest, …
│   └── pages/                     # Logic-only "page logic" if needed by App Router boundaries
│       ├── LibraryHome/
│       ├── FindHub/
│       ├── ShowDetail/
│       ├── PersonDetail/
│       └── Settings/
│           └── features/…
└── tests/
    ├── unit/                      # Logic tests (merge, status, default-save, AI parsing)
    ├── integration/               # API routes + Supabase (against a test namespace)
    └── e2e/                       # Smoke: build collection, ask, alchemy, export
```

> Pages in the `src/pages/` tree are the **logic/feature packages** mounted by the thin `src/app/*/page.tsx` route files. This keeps App Router boundaries thin and feature code fractal.

---

## 2. Foundation layer

### 2.1 Environment, secrets, and scripts
- `.env.example` documents:
  - `NEXT_PUBLIC_SUPABASE_URL`
  - `NEXT_PUBLIC_SUPABASE_ANON_KEY` (browser-safe)
  - `SUPABASE_SERVICE_ROLE_KEY` (server-only; never imported by client)
  - `CATALOG_API_KEY` (content provider)
  - `CATALOG_API_BASE_URL`
  - `AI_API_KEY` (may be empty in benchmark; injected at runtime via Settings)
  - `AI_MODEL_DEFAULT`
  - `NAMESPACE_ID` (build isolation; auto-generated per run, persisted to `.env.local` for that dev session)
  - `DEV_USER_ID` (default user for dev/test; used by `X-User-Id` injection)
- `.gitignore` excludes `.env*` except `.env.example`.
- `package.json` scripts (names illustrative):
  - `dev` — `next dev`
  - `build` — `next build`
  - `start` — `next start`
  - `test` — `vitest run` (unit + integration with ephemeral namespace)
  - `test:reset` — runs `scripts/namespace-reset.mjs` for the current `NAMESPACE_ID`
  - `db:migrate` — applies `supabase/migrations/*.sql`
  - `export:debug` — runs an export for the current dev user

### 2.2 Namespace + identity injection
- `src/lib/auth/devIdentity.ts` reads `X-User-Id` and `X-Namespace-Id` headers (development/test only) and rejects them in production builds via env guard `process.env.NODE_ENV === 'production'`.
- Server-side helpers `getRequestContext(req)` return `{ userId, namespaceId }` for every server route and server component.
- **No real OAuth** required in this build. The data model is OAuth-ready: `user_id` is an opaque string and the only consumer is row-level partitioning.
- A local dev-only "login as user" page (gated behind `NODE_ENV !== 'production'`) lets the developer pick among locally-seeded user IDs to exercise multi-user behavior.

### 2.3 Database schema (Supabase migrations)
The schema is the contractual surface for the data model. Migrations are forward-only, deterministic, and replayable.

**Tables (one migration per table or grouped for atomicity):**

1. `app_metadata` (singleton)
   - `id` int PK (always 1)
   - `data_model_version` int not null default 3
   - `namespace_id` text not null

2. `users` (synthetic, but schema-real)
   - `id` uuid PK (default `gen_random_uuid()`)
   - `namespace_id` text not null
   - `user_name` text not null
   - `created_at` timestamptz default now()
   - Unique `(namespace_id, user_name)`

3. `shows`
   - `id` text PK (catalog id or app-generated stable id)
   - `namespace_id` text not null
   - `user_id` uuid not null references `users(id)` (the **owner** of the library entry; "in collection" lives here)
   - `external_ids` jsonb
   - `title` text not null
   - `show_type` text not null check in (`movie`,`tv`,`person`,`unknown`)
   - `overview`, `tagline`, `homepage` text
   - `genres` text[] not null default `{}`
   - `original_language` text
   - `spoken_languages` text[] not null default `{}`
   - `languages` text[] not null default `{}`
   - `poster_url`, `backdrop_url`, `logo_url` text
   - `network_logos` text[] not null default `{}`
   - `vote_average` double precision
   - `popularity` double precision
   - `vote_count` int
   - `last_air_date`, `first_air_date`, `release_date` date
   - `runtime` int, `budget` bigint, `revenue` bigint
   - `series_status` text
   - `number_of_episodes` int, `number_of_seasons` int
   - `episode_run_time` int[] not null default `{}`
   - `last_episode_run_time` int
   - `my_tags` text[] not null default `{}`
   - `my_tags_update_date` timestamptz
   - `my_score` double precision
   - `my_score_update_date` timestamptz
   - `my_status` text check in (`active`,`next`,`later`,`done`,`quit`,`wait`)
   - `my_status_update_date` timestamptz
   - `my_interest` text check in (`excited`,`interested`)
   - `my_interest_update_date` timestamptz
   - `ai_scoop` text
   - `ai_scoop_update_date` timestamptz
   - `provider_data` jsonb
   - `details_update_date` timestamptz
   - `creation_date` timestamptz default now()
   - `is_test` boolean not null default false
   - Unique composite: `(namespace_id, user_id, id)` — same show may be saved by multiple users; catalog facts are shared via merge.

   > **Design note:** The PRD's "in collection" rule is *user-scoped* (one user's saved set is independent of another's). A second `show_instances` table (or a column on `shows` enforcing `user_id`) carries My Data. Catalog meta may be shared across users via a denormalized read; for v1 we keep one row per `(namespace_id, user_id, id)` and merge catalog facts using the rules in §3.2. This is the simplest schema that satisfies "users may exist; identity is opaque; later OAuth requires no redesign."

4. `cloud_settings`
   - `id` text PK (always `"globalSettings"`)
   - `namespace_id` text not null
   - `user_id` uuid not null
   - `version` double precision not null (epoch seconds; conflict resolution)
   - `user_name` text
   - `catalog_api_key` text
   - `ai_api_key` text
   - `ai_model` text not null
   - Unique `(namespace_id, user_id)`

5. `chat_sessions` (session-only; cleared on reset)
   - `id` uuid PK
   - `namespace_id` text not null
   - `user_id` uuid not null
   - `mode` text check in (`ask`,`alchemy`)
   - `turns` jsonb not null default `'[]'`
   - `mentioned_shows` jsonb not null default `'[]'`
   - `summary` text
   - `created_at`, `updated_at` timestamptz

6. `ai_scoop_cache` (per-show, per-user; mirrors persistence rules)
   - Same effective fields as `shows.ai_scoop` + `_update_date`, but isolated so we can re-issue fresh scoops without touching user data.
   - This is **optional** in v1; if absent, scoop lives on the `shows` row. The PRD says scoop persists only if in collection, so the simpler path is to keep it on `shows` and gate writes by `my_status IS NOT NULL`.

**Row-level security (RLS):** the app uses the **service role key on the server only** and filters every query by `(namespace_id, user_id)`. RLS is on with a single permissive policy that **asserts** `namespace_id = current_setting('app.namespace_id')::text` and `user_id = current_setting('app.user_id')::uuid`, set at the top of each server transaction via `SET LOCAL`. This guarantees client-side anon-key requests cannot leak across namespaces or users even by accident.

**Indexes:** `(namespace_id, user_id, id)`, `(namespace_id, user_id, my_status)`, `(namespace_id, user_id, my_tags gin)`, `(namespace_id, user_id, last_air_date desc)`, `(namespace_id, user_id, popularity desc)`.

**Migrations + seed:**
- `001_init_schema.sql`
- `002_rls_policies.sql`
- `003_seed_dev_user.sql` (only seeds the dev `users` row; no show data)

### 2.4 Design tokens & primitives
- `src/theme/tokens.ts` exports color/space/typography scales including **font size scale** (XS…XXL) consumed by Settings.
- `src/components/` contains:
  - `Button`, `IconButton`, `Chip`, `Slider`, `TextField`, `TagPicker`, `Select`, `Toast`, `Dialog`, `Sheet`, `PosterTile`, `Backdrop`, `ScoreBar`, `EmptyState`, `Skeleton`, `ConfirmDialog`, `TabSwitcher`.

All primitives consume tokens — no hard-coded colors or pixel values in TSX.

### 2.5 Storage / domain layer (`src/lib/storage`)
- `types.ts` mirrors `Show`, `MyStatusType`, `MyInterestType`, `CloudSettings`, `FilterConfiguration`, `LocalSettings`, `UserDefaultsUIState` from `storage-schema.ts` (the file is reference; we re-derive and adapt names to snake_case for Supabase columns).
- `mergeShow(stored, incoming)`: implements the merge rules in `storage-schema.md`:
  - Non-`my*` fields use `selectFirstNonEmpty(new, old)`.
  - `my*` fields resolve by latest `*UpdateDate`; if only one side has a date, that side wins.
  - `detailsUpdateDate = now()`; `creationDate` preserved.
- `defaultSavePolicy(action)` returns `{ status, interest }` per §5.3 of the PRD: rating → `{ done, null }`; tag → `{ later, interested }`; status only → uses the chosen status; interest only → `{ later, chosenInterest }`.
- `isInCollection(show)`: `myStatus != null`.
- `ensureShowExists(user, catalogShow)`: upsert with merge.
- `exportSnapshot(user)` and `importSnapshot(user, json)` for the Export/Restore feature.

---

## 3. Collection core

### 3.1 Library Home page
**Route:** `/` (`src/app/page.tsx` → `<LibraryHome />`)

**Fractal package:** `src/pages/LibraryHome/LibraryHome.tsx` + features/

**Features:**
- `Sidebar` — Filter list: All Shows, tag filters (one per tag + "No tags"), data filters (genre / decade / community score range). Media-type toggle (All / Movies / TV) on top.
- `StatusSections` — Renders the four sections per PRD §7.1 (Active → Excited → Interested → Other collapsed). Active uses larger tiles.
- `PosterGrid` — Filtered, grouped, with empty states (no collection → Search/Ask CTA; filter yields none → "No results found").
- `EmptyLibrary` — Friendly first-run state with two CTAs (Search, Ask).

**Logic hook:** `useLibraryHome()` reads the selected filter + media type from `lastSelectedFilter` (UI state) and queries the server (`/api/shows?filter=…`). All server queries pass `namespace_id` and `user_id` from request context.

**Rules:**
- Items grouped by `myStatus` (with `later+excited` → "Excited" section, `later+interested` → "Interested").
- Within sections, sort by most recent `my*UpdateDate` desc.

### 3.2 Show Detail page (skeleton)
**Route:** `/show/[id]` (`src/app/show/[id]/page.tsx`)

**Fractal package:** `src/pages/ShowDetail/ShowDetail.tsx` + features/

This page is built incrementally; in the foundation stage we ship the **data shape + status/interest/tags/rating controls**. Catalog hydration, AI sections, and strands are added in §4 and §5.

**Initial features:**
- `HeaderMedia` (placeholder carousel — full implementation in §4)
- `CoreFactsRow` (year, runtime/seasons, community score)
- `MyStatusToolbar` — chips for Active, Interested, Excited, Done, Quit, Wait, plus "(no status)" toggle
- `MyRating` — score slider; clearing sets `myScore = null`
- `MyTags` — chip display + `TagPicker` for adding
- `AutoSaveStatus` (logic) — applies §5.2 saving triggers and §5.3 defaults

**Logic hook:** `useShowDetail(id)` returns:
- `show` (merged stored + live catalog), `isInCollection`
- handlers: `setStatus(s)`, `setInterest(i)`, `addTag(t)`, `removeTag(t)`, `setRating(score)`, `removeFromCollection()`.

**Auto-save semantics** (must be unit-tested):
| Action on unsaved show | Resulting `myStatus` | `myInterest` |
|---|---|---|
| set status (any explicit) | chosen | preserved if `later` |
| set interest (Interested/Excited) | `later` | chosen |
| set rating (any) | `done` | unchanged |
| add tag | `later` | `interested` |

**Removal:** `removeFromCollection()` shows a `ConfirmDialog`. The dialog can be suppressed after N removals (`statusRemovalCount` increments; on threshold, dialog offers a "don't ask again" toggle, persisted to `uiState`).

### 3.3 Filters & data views (`src/lib/storage/filters.ts`)
- `FilterConfiguration` discriminated union: `{type:'all'|'genre'|'myStatus'|'communityScore'|'decade'|'myTag', label, value}`.
- `applyFilters(shows, filter, mediaType)` returns filtered set. Sidebar subscribes to the current user's distinct tags (auto-derived) and renders a chip per tag + a "No tags" chip if any saved show has empty `myTags`.

### 3.4 Local settings / UI state
- `localSettings` (`autoSearch`, `fontSize`) and `uiState` (`hideStatusRemovalConfirmation`, `statusRemovalCountKey`, `lastSelectedFilter`) live in **client storage** (e.g., `localStorage`) per the PRD's "cache is disposable" rule. The backend is the source of truth for user-owned data.

---

## 4. External catalog integration

The catalog provider is an opaque client (`src/lib/catalog/client.ts`) with a stable interface. v1 supports a single provider (TMDB-shaped, namespaced) with stubs for the next.

### 4.1 Catalog client surface
```ts
interface CatalogClient {
  searchShows(query, opts): Promise<CatalogShow[]>;
  getShowById(id): Promise<CatalogShow>;
  getShowDetail(id): Promise<CatalogShowDetail>;   // includes credits, seasons, similar, recommended, images, videos, providers
  getPersonDetail(id): Promise<CatalogPersonDetail>;
}
```

All calls are server-side (`fetch` from `/api/catalog/*` route handlers), so the API key never reaches the browser.

### 4.2 Server routes (`src/app/api/catalog/...`)
- `GET /api/catalog/search?q=...&page=...` — proxy to provider, returns lightweight results.
- `GET /api/catalog/shows/[id]` — full detail, normalized to `CatalogShowDetail`.
- `GET /api/catalog/people/[id]` — Person detail.

### 4.3 Catalog → Show mapping
- `mapCatalogToShow(catalog)` returns a `Show` draft with **only catalog fields populated** (no `my*` fields).
- On save or refresh, `mergeShow(stored, mapped)` is invoked with the rules from §2.5.
- Field mapping rules per `storage-schema.md`:
  - `id` ← catalog id
  - `showType` ← catalog media type; fall back to name→tv, title→movie, else `unknown` (reject)
  - `overview` ← catalog overview
  - `genres` ← mapped from catalog genre ids to names
  - Dates parsed with multi-format tolerance
  - Movie fields: `runtime`, `budget`, `revenue`
  - TV fields: `seriesStatus`, `numberOfEpisodes`, `numberOfSeasons`, `episodeRunTime`
  - Images: `posterUrlString`, `backdropUrlString`, `logoUrlString` (best-rated English preferred)
  - Providers: stored as `ProviderData` (IDs only)
  - Transient: `cast`, `crew`, `seasons`, `videos`, `recommendations`, `similar` — fetched on demand and **not persisted**

### 4.4 Show Detail page (full build)
- `HeaderMedia` — Carousel: backdrops → posters → logo → videos (if any). Graceful fallback when only poster exists. Never blocks reading.
- `Overview` + `Scoop` — See §5.1.
- `AskAboutThisShow` — CTA: switches Find → Ask with show prefill (seed conversation with show context, then user prompt).
- `GenresLanguages` — Genre chips, language list.
- `Recommendations` — Strand of `similar` + `recommended` (catalog-native, no AI).
- `ExploreSimilar` — See §5.4.
- `Providers` — `Stream It` strip. Lookup `providerData.countries[userCountry]`; resolve provider IDs to names via a cached provider list.
- `CastCrew` — Horizontal strands → `PersonDetail`.
- `Seasons` (TV only) — Collapsible season list with episode counts.
- `BudgetRevenue` (movies, when present) — Bar chart (lightweight, design-token colors only).

### 4.5 Mentioned shows & AI → catalog resolution
- AI surfaces that mention shows (Ask, Alchemy results) emit `Title::externalId::mediaType;;...` per the contract in `ai_prompting_context.md` §3.2.
- Server resolves the list by:
  1. Looking up by `externalId` in the catalog.
  2. If absent, search the catalog by title and accept the first result whose title matches **case-insensitively**.
  3. If still absent, mark the title as non-interactive and offer a "Search for it" handoff.
- Resolved shows become real `Show` objects (transient) and can carry the AI "reason" as a transient field for tile tooltips. Saving them follows the auto-save rules.

### 4.6 Search (Find → Search)
**Route:** `/find/search`

**Features:**
- `SearchBar` (debounced, 250 ms)
- `PosterGrid` of results
- Tile shows **in-collection** indicator + **user rating** indicator
- Empty state: "Search for shows and movies"
- "Search on Launch" honored via `localSettings.autoSearch` (default off; the field is in the env example for future override)

---

## 5. AI surfaces (the heart)

All AI surfaces share a single engine in `src/lib/ai/`. The engine is provider-pluggable (the benchmark ships OpenAI-compatible and Anthropic-compatible adapters) and centralizes:
- the **persona** (`ai_voice_personality.md`),
- the **shared rules** (`ai_prompting_context.md` §1),
- the **structured output parser** for show lists,
- the **taste context builder** that pulls the user's library + relevant `my*` fields into a compact form,
- the **cache + freshness** layer (scoop 4 h, chat summary on/off, ephemeral session storage).

### 5.1 AI Scoop
- **Endpoint:** `POST /api/ai/scoop { showId, force? }`
- **Persistence:** stored on the `shows` row only if `my_status IS NOT NULL`. Otherwise returned ephemerally (not persisted).
- **Freshness:** regenerate after 4 h. `aiScoopUpdateDate` is the source of truth; if within window, return cached.
- **Structure (instructed, not parsed as JSON for v1):**
  1. **Personal Take** (one or two sentences; pick a side)
  2. **The Stack-Up** (one short paragraph vs critical/community reception)
  3. **The Scoop** (centerpiece, the most real estate)
  4. **Fit & Warnings** (who it's for, who'll bounce)
  5. **Worth It?** (one-line gut check)
- **Tone:** 70/30 friend/critic, 60/40 hype/measured; "gossipy, vivid, and useful"; ~150–350 words.
- **Streaming:** if the client supports SSE, stream tokens. While streaming, the UI shows a "Generating…" indicator and progressively reveals sections as they are detected (by header markers `**Personal Take**` etc., or by simple two-newline paragraph heuristics).
- **Scoop CTA copy:**
  - No cached scoop → "Give me the scoop!"
  - Cached scoop exists → "Show the scoop"
  - Open → title "The Scoop"
- **Tests:** unit tests for the freshness rule, the persistence gate (only persist when in collection), the streaming chunk parser, and a regression test for the required section headers (it must mention all five headings).

### 5.2 Ask (chat + mentioned shows)
- **Endpoint:** `POST /api/ai/ask { sessionId?, message, prefilledShowId? }`
- **Session storage:** ephemeral `chat_sessions` row keyed by `sessionId`. Cleared on `POST /api/ai/ask/reset`.
- **Welcome view:** 6 random starter prompts. `GET /api/ai/ask/starters` returns them; the user can refresh (re-roll).
- **Context window management:**
  - Always include: persona, shared rules, taste context (library digest + tags distribution + top 20 status-tagged titles).
  - Append recent turns verbatim.
  - When `turns.length > 10`, **summarize** older turns (1–2 sentences, same voice), prepend the summary, and keep the most recent 10 verbatim.
- **Structured output contract:** the model returns `{ commentary, showList }`. The server validates `showList` is well-formed (`Title::externalId::mediaType;;`); on parse failure, retry once with stricter formatting instructions, then fall back to unstructured commentary + Search handoff (per `ai_prompting_context.md` §5).
- **UI:**
  - `MessageList` with user/assistant bubbles
  - `MentionedShowsStrip` — horizontal row of resolved `Show` tiles, below the assistant message that mentioned them
  - `Composer` (textarea + send)
  - Ask About This Show: when launched from a Show Detail, server seeds the conversation with the show's catalog context, and the composer preloads a starter question.
- **Tone:** 1–3 tight paragraphs + bulleted lists for multi-recs; "low-friction, fast, and fun."

### 5.3 Concepts (shared)
- **Endpoint:** `POST /api/ai/concepts { showIds: string[] }` (1+ ids)
- **Output rules:**
  - Bullet list only, 1–3 words each
  - 8 concepts by default
  - For multi-show: must represent **shared** commonality across all inputs
  - Specificity over genericity ("hopeful absurdity" ✓, "good characters" ✗)
  - Diversity across axes (structure, vibe, emotion, craft)
  - Order by strength ("aha" concepts first)
- **Validation:** the server validates the bullet count is reasonable and the length constraint (1–3 words). If the model returns prose, retry once.
- **Provider for Explore Search Chat:** concepts are also returned via `ExploreSearchChatRequest` when a user asks about a single show inside Ask; same rules apply.

### 5.4 Explore Similar (single-show concepts)
**Route:** Section on Show Detail (no separate page).

**Flow:**
1. Tap **Get Concepts** → `POST /api/ai/concepts { showIds: [id] }`
2. Concepts render as `ConceptChip`s. User selects 1+ (cap matches Alchemy's 8-cap for consistency).
3. Tap **Explore Shows** → `POST /api/ai/recs { showId, concepts }`
4. Returns **5** recommendations with reasons that name which concepts align.
5. Resolved recommendations render as `PosterGrid`. Save actions follow auto-save rules.

**UX copy:** "pick the ingredients you want more of." Empty state nudges toward selecting at least one concept.

### 5.5 Alchemy (multi-show concept blending)
**Route:** `/find/alchemy`

**Fractal package:** `src/pages/FindHub/features/Alchemy/`

**Flow (must match PRD §7.4):**
1. **Pick 2+ shows** from library + global catalog (catalog search embedded). Chips display selected shows.
2. **Conceptualize Shows** → `POST /api/ai/concepts { showIds: [...] }`. Returns ~8 shared concepts.
3. **Select concepts** (cap 8). Toggling a concept clears downstream results.
4. **ALCHEMIZE!** → `POST /api/ai/recs { showIds, concepts }` → returns **6** recommendations with reasons.
5. **More Alchemy!** chains a new round using the results as new inputs (concept extraction may re-run; UI offers "Use these 6 as new starting shows").
6. Backtracking: changing shows clears concepts and results; changing concepts clears results only.

**Sessions:** ephemeral, like Ask. `chat_sessions.mode = 'alchemy'`. Stored turns include the concept list, selected concepts, and last results for handoff (but **never persisted past the session** per the PRD §5.7).

### 5.6 Persona & prompt loading
- `src/lib/ai/persona.ts` exports the **base system prompt** assembled from `ai_voice_personality.md` and `ai_prompting_context.md` (concatenated as immutable text blocks).
- `src/lib/ai/prompts/{scoop,ask,concepts,recs}.ts` export the surface-specific prefixes and structure instructions.
- All prompts include:
  - Persona block
  - Shared rules
  - Surface contract
  - Structured-output format spec (where applicable)
  - Taste context (library digest)
- **No prompts are editable from the UI.** Model selection is user-editable in Settings (next item).

---

## 6. Person Detail

**Route:** `/person/[id]`

**Fractal package:** `src/pages/PersonDetail/PersonDetail.tsx` + features/

**Features:**
- `PersonHeader` (image, name, bio)
- `ImageGallery` (catalog images, lazy-loaded)
- `PersonAnalytics` — three lightweight charts (no heavy chart lib): average project rating (line/bar), top genres (horizontal bar), projects-by-year (bar). All data computed from `getPersonDetail`'s filmography.
- `FilmographyByYear` — group by year, render project tiles grouped by year. Tapping a tile opens its `ShowDetail`.

---

## 7. Settings & Your Data

**Route:** `/settings`

**Fractal package:** `src/pages/Settings/Settings.tsx` + features/

**Features:**
- `App` group:
  - `FontSize` — slider bound to `localSettings.fontSize`; live preview on the page.
  - `AutoSearch` — toggle for `localSettings.autoSearch`.
- `User` group:
  - `UsernameField` — writes to `cloud_settings.user_name` (synced across devices if enabled).
- `AI` group:
  - `AiApiKey` — masked input; stored in `cloud_settings.ai_api_key` (synced; never committed).
  - `AiModelSelector` — list of models supported by the configured provider.
  - **Benchmark note:** keys may be injected via env (e.g., `AI_API_KEY`); user-entered keys are optional. Documented in Settings help text.
- `Integrations` group:
  - `CatalogApiKey` — same handling.
- `Your data` group:
  - `ExportMyData` — invokes `POST /api/export` → server-side zip of all `shows` + `cloud_settings` for `(namespace_id, user_id)`. Returns a downloadable `.zip` with a single `backup.json` (ISO-8601 dates, schema-versioned). Filename: `companion-export-{userName}-{YYYYMMDD}.zip`.
  - `ImportMyData` — *(explicitly noted as not implemented in v1 per PRD §7.7 Open Questions)*; we wire the route shell and return a "Coming soon" toast so the UI surface exists.

**Persistence boundary:** username, AI key, model, catalog key are **server-stored** (in `cloud_settings`). Font size and autoSearch are **client-only** (`localStorage`) — they are not user-owned "data" in the cross-device sense and would be annoying to sync. The PRD doesn't require syncing them, so we keep them local.

---

## 8. Cross-cutting concerns

### 8.1 Identity, namespaces, isolation
- All server handlers derive `{ userId, namespaceId }` via `getRequestContext(req)` (see §2.2). All Supabase queries pass both, and RLS enforces them via `SET LOCAL`.
- Production builds reject the `X-User-Id` / `X-Namespace-Id` injection; only real OAuth (future) or authenticated service calls pass.
- `scripts/namespace-reset.mjs` deletes all rows where `namespace_id = $NAMESPACE_ID` for the relevant tables, then re-seeds the dev user. This is the "destructive test reset" required by the rider — no global teardown.

### 8.2 Source of truth
- Server is the only writer. Client uses Supabase's anon client **read-only** (or with restrictive RLS) and refreshes from the server after writes.
- `mergeShow` runs **only on the server** when ingesting catalog data into a stored show.

### 8.3 Schema evolution
- `app_metadata.data_model_version` defaults to 3 (matches the reference schema).
- Migrations are forward-only and idempotent (`CREATE TABLE IF NOT EXISTS`, `ALTER TABLE … ADD COLUMN IF NOT EXISTS`).
- A migration test in `tests/integration/migrate.test.ts` applies the full migration set to a fresh database and asserts the schema matches `storage-schema.md` field-for-field.

### 8.4 Auto-save & implicit behaviors
- The single `useShowDetail()` hook centralizes all save paths and applies §5.2 / §5.3 rules. No screen other than the detail view mutates `my*` fields directly.
- All auto-saves round-trip through a single server endpoint (`POST /api/shows/[id]/mutate`) that validates state transitions and writes timestamps.

### 8.5 Tile indicators
- `PosterTile` shows: in-collection dot/badge when `myStatus != null`; user rating badge when `myScore != null`.

### 8.6 Search on Launch
- On first paint of `/`, if `localSettings.autoSearch === true`, redirect to `/find/search` with focus on the search field.

### 8.7 Backup export
- `POST /api/export` → `scripts/export-data.mjs` builds the zip in-memory (no FS write in serverless environments), then streams it. Contents:
  - `backup.json` — `{ version, exportedAt, user: {id, userName}, shows: Show[], cloudSettings }`
  - `README.txt` — short import-instructions stub
- The format is intentionally JSON-only in v1 (no CSV) because the schema includes nested arrays (tags, languages) and date precision that CSV would lose.

### 8.8 Error & empty states
- All features have an empty state component (no collection, no search results, no AI results, no concepts, no mentions, no chat, no provider data).
- All async surfaces distinguish loading, error, and empty; no "blank stare" UX.
- All destructive actions go through `ConfirmDialog` (status removal at minimum).

---

## 9. Quality plan

### 9.1 Test layers

**Unit (`tests/unit/`):**
- `mergeShow` matrix (every non-my field, every my field, tie-breakers, nil-handling)
- `defaultSavePolicy` table from §3.2
- AI Scoop freshness (`isFresh(scoopUpdateDate)`)
- Concept output validator (count, length, no-generics heuristic)
- Show-list parser (`Title::externalId::mediaType;;` round-trip)
- Filter `applyFilters` (all/genre/myStatus/communityScore/decade/myTag × mediaType)
- Export schema (version, dates in ISO-8601, round-trip)

**Integration (`tests/integration/`):**
- Namespace + identity round-trip: create a show as `userA` in `nsA`, assert `userB` in `nsA` and `userA` in `nsB` cannot see it.
- Destructive reset script: seed 50 shows, run `namespace-reset`, assert zero rows for that namespace, assert unrelated namespace untouched.
- Scoop endpoint: persist gate (in-collection saves; out-of-collection doesn't), 4-hour freshness (uses a clock abstraction), streaming chunk assembly.
- Ask endpoint: starter re-roll, mentioned-shows parsing, summary compaction at 11 turns, parse-failure retry.
- Alchemy endpoint: 2-show minimum, 8-concept cap, concept-change clears results, "More Alchemy" chain.
- Export endpoint: zip integrity, JSON schema, dates are ISO-8601.
- RLS assertions: queries with mismatched `namespace_id` or `user_id` setting return 0 rows.

**E2E / smoke (`tests/e2e/`):**
- Build collection: search → open → set status → tag → rating → see on home.
- Rate-to-save: open unsaved → adjust rating → assert `myStatus = done`.
- Tag-to-save: open unsaved → add tag → assert `myStatus = later`, `myInterest = interested`.
- Ask discovery: ask for vibe → see mentioned shows strip → tap → save.
- Explore Similar: detail → get concepts → select 2 → explore shows → see 5 recs.
- Alchemy: 2 shows → conceptualize → select 3 → alchemize → chain another round.
- Person deep-dive: detail → cast → person → filmography → credit → new detail.
- Backup export: settings → export → download zip → assert contains shows.

### 9.2 Lint, typecheck, build
- ESLint + Prettier, strict TypeScript.
- `tsc --noEmit` must pass with no errors.
- `next build` must succeed with no warnings (other than known framework ones).

### 9.3 Performance budgets
- Library Home first paint < 1.5 s on warm cache (200 shows).
- Search debounce 250 ms; request cancellation on new keystroke.
- Scoop stream first token < 1.5 s server-side.
- AI surface responses are streamed; the UI never shows a blank wait > 200 ms.

---

## 10. Milestones (build order)

> Each milestone is independently shippable behind a feature flag. M0–M3 produce a usable app; M4–M6 harden it.

| # | Milestone | Outcome | Key deliverables |
|---|---|---|---|
| M0 | **Scaffold** | App boots, env works, dev identity injects, namespace RLS verified. | `package.json`, `.env.example`, supabase clients, `getRequestContext`, RLS migrations, smoke test that RLS blocks cross-namespace reads. |
| M1 | **Collection core** | You can search (provider stub), open a show, set status/interest/tags/rating, see it on Home with filters. | `mergeShow`, `defaultSavePolicy`, Library Home + Sidebar + StatusSections, Show Detail skeleton (status toolbar, rating, tags), filter logic, local UI state. |
| M2 | **Catalog integration** | Real provider integration; full Show Detail (header, core facts, genres/langs, recommendations strand, cast, seasons, budget/revenue, providers). | Catalog client + routes, `mapCatalogToShow`, Header Media, Recommendations strand, Cast/Crew, Seasons, Budget/Revenue, Providers, Search page. |
| M3 | **AI engine + Scoop + Ask** | The heart. Taste-aware Scoop, Ask with mentioned shows, chat summarization. | `src/lib/ai/*` engine, Scoop endpoint + UI, Ask endpoint + UI + starters, persona, summary compaction, structured-output retry. |
| M4 | **Concepts + Explore Similar + Alchemy** | Full discovery suite. | Concepts endpoint + validators, Explore Similar section, Alchemy page with 5-step flow + chain. |
| M5 | **Person Detail + Settings + Export** | All remaining surfaces. | Person page + charts, Settings (font size, autoSearch, username, AI/catalog keys, model), Export My Data zip, Import shell. |
| M6 | **Quality gates** | The benchmark succeeds. | Full test suite, RLS coverage, namespace-reset script, README quickstart, `.env.example` complete, no warnings in `next build`. |

---

## 11. Risks & open questions handled

The PRD §10 lists open questions. This plan resolves or defers them as follows:

- **Next as a first-class status in UI:** *deferred.* Model supports it (`myStatus` enum includes `next`); UI does not surface a chip. The code path is one new chip and a section break in `StatusSections`.
- **Named custom lists beyond tags:** *out of scope for v1.* No data model change; revisit after M6.
- **Generating Scoop on unsaved show implicitly saves it:** *rejected.* Per PRD §4.9, scoop persists **only** if the show is already in the collection. Implementation honors this; the UI does not nudge save on scoop.
- **Unrated state vs nil:** *treated as nil.* `myScore = null` is "unrated." No explicit "Unrated" sentinel needed; UI shows the rating bar with no selected value.
- **Import/Restore:** *shell only.* Settings has the button and a "Coming soon" toast. The endpoint validates the zip format in a dry-run path but does not write. The export format is versioned to make later import non-breaking.
- **Saving/sharing Alchemy sessions:** *out of scope.*
- **Explicit myStatus sidebar filters:** *implemented as a sidebar category.* `FilterConfiguration.type = 'myStatus'` is in the union; Sidebar renders it as a top-level filter group with a sub-list (Active / Later+Excited / Later+Interested / Wait / Quit / Done).

---

## 12. Coverage map (PRD section → deliverable)

> Quick traceability. Every PRD section is mapped to the milestone that delivers it. A "—" means the PRD explicitly defers it.

| PRD § | Section | Delivered in |
|---|---|---|
| §1 Product Summary | Whole product | M1–M6 |
| §2 Goals & Success | Telemetry hooks | M3 (AI conversion events), M5 (export events) |
| §3 Non-Goals | Documented; nothing to do | M0 README |
| §4.1 Show | `Show` type, merge logic | M1 |
| §4.2 Status System | `MyStatusToolbar`, auto-save rules | M1 |
| §4.3 Interest Levels | `MyStatusToolbar` Interested/Excited chips | M1 |
| §4.4 Tags | `MyTags`, `TagPicker` | M1 |
| §4.5 Filters | Sidebar + `applyFilters` | M1 |
| §4.6 AI Chat | Ask | M3 |
| §4.7 Alchemy | Alchemy page | M4 |
| §4.8 Explore Similar | Show Detail section | M4 |
| §4.9 AI Scoop | Scoop | M3 |
| §4.10 Person | Person Detail | M5 |
| §5.1–§5.11 Data Behaviors | merge, defaults, timestamps, persistence rules | M1, M3 |
| §6 App Structure | Routes & nav | M0, M1 |
| §7.1 Collection Home | Library Home | M1 |
| §7.2 Search | Search page | M2 |
| §7.3 Ask | Ask page | M3 |
| §7.4 Alchemy | Alchemy page | M4 |
| §7.5 Show Detail | Full page | M1 (skeleton) + M2 (catalog) + M3 (scoop) + M4 (explore) |
| §7.6 Person Detail | Person page | M5 |
| §7.7 Settings & Your Data | Settings | M5 |
| §8 Cross-Cutting | Identity, namespace, source-of-truth | M0, M1, M3 |
| §9 Key User Journeys | 1–10 | End-to-end tests in M6 |
| §10 Open Questions | §11 above | M5–M6 |
| Infra rider §3 Repo | `.env.example`, scripts, migrations | M0 |
| Infra rider §4 Identity/Isolation | RLS, namespace reset | M0 |
| Infra rider §5 Auth | Dev identity injection | M0 |
| Infra rider §6 Source of truth | Server writes | M0–M1 |
| Infra rider §7 Destructive tests | `test:reset` script | M0, M6 |
| Infra rider §8 Cloud compatibility | No Docker required | M0 |
| Infra rider §9 Success criteria | All | M0, M6 |
| `ai_prompting_context.md` | Engine, parsers, validators | M3, M4 |
| `ai_voice_personality.md` | Persona, tone sliders, surface adaptations | M3, M4 |
| `concept_system.md` | Concepts endpoint, validators, selection UX | M4 |
| `detail_page_experience.md` | Show Detail hierarchy | M1–M4 |
| `discovery_quality_bar.md` | Test rubrics | M6 |
| `storage-schema.md` / `storage-schema.ts` | Migrations, `mergeShow`, types | M0–M1 |

---

## 13. Definition of Done (per milestone)

A milestone is "done" only when:

- All its deliverables are in the repo and pass `tsc --noEmit`, ESLint, and the relevant test layers.
- The dev workflow works: `npm run dev` boots against a real or hosted Supabase, `npm test` runs unit + integration in an isolated namespace, `npm run test:reset` returns it to a clean state.
- A short note in `results/` (or the PR) summarizes what changed, with screenshots for UI milestones.
- The PRD coverage map above has been updated to reflect any scope shifts.

When **M6** is complete, the build is **evaluation-ready**: `.env.example` complete, namespace isolation verified, RLS enforced, destructive resets scoped, OAuth-ready (replace `getRequestContext` with real session lookup, no schema change), export/import shell in place, and the discovery surfaces produce output that satisfies the `discovery_quality_bar.md` rubric in their tests.
