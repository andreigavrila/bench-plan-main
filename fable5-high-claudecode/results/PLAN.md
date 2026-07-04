# Implementation Plan — Personal TV + Movie Companion

**Sources:** `docs/prd/product_prd.md`, `docs/prd/infra_rider_prd.md`, all supporting docs (`ai_prompting_context.md`, `ai_voice_personality.md`, `concept_system.md`, `detail_page_experience.md`, `discovery_quality_bar.md`) and technical docs (`storage-schema.md`, `storage-schema.ts`). Architecture follows the fractal pattern in `INSTRUCTIONS.md`.

---

## 1. Executive Summary

We are building a personal TV/movie companion web app: users collect shows, overlay their own data (status, interest, tags, rating, AI Scoop), and get taste-aware discovery through four paths — Search, Ask (AI chat), Alchemy (multi-show concept blending), and per-show Explore Similar. The user's version of every show wins everywhere it appears.

**Benchmark baseline (mandated by the infra rider):**
- **Next.js (latest stable)** — App Router, UI + server boundary (API route handlers).
- **Supabase (hosted preferred; local optional, Docker never required)** — persistence via official `@supabase/supabase-js`.
- All persisted user data partitioned by `(namespace_id, user_id)`; dev identity injection instead of real OAuth, with a clean migration path to OAuth later.
- External integrations: a content catalog provider (TMDB-shaped API: search, details, credits, providers, images, videos, person data) and an AI provider (Anthropic API) — both configured via environment variables.

**Architectural stance:**
- **Backend is the source of truth.** All My Data mutations go through Next.js server routes into Supabase. The client caches (React Query) but clearing client storage loses nothing.
- **AI calls are server-side only** (keys never reach the browser), with structured-output contracts, one strict retry, and Search-handoff fallbacks.
- **Business rules live in one place** — a server-side domain layer implementing save triggers, defaults, removal semantics, per-field timestamp merge, and catalog merge policy — so every surface (Detail, Search tiles, Ask, Alchemy) behaves identically.

---

## 2. System Architecture

### 2.1 High-level component map

```
Browser (Next.js React client)
  │  React Query cache (disposable), UI state in localStorage (disposable)
  ▼
Next.js server boundary (route handlers under /api)
  ├── /api/collection/*      ← My Data CRUD, business rules, merge engine
  ├── /api/catalog/*         ← proxied catalog provider calls (search, details, person)
  ├── /api/ai/*              ← Ask chat, Scoop stream, concepts, concept recs
  ├── /api/settings/*        ← cloud settings (username, keys, model)
  ├── /api/export            ← zip backup of all saved shows + My Data
  └── /api/test/reset        ← namespace-scoped destructive reset (dev/test only)
  │
  ├──► Supabase (Postgres) — shows, settings, app_metadata; keyed by (namespace_id, user_id)
  ├──► Catalog provider API (server-side key)
  └──► AI provider API (server-side key; streaming for Scoop/Ask)
```

### 2.2 Why every AI/catalog call goes through the server

- Infra rider: elevated keys must be server-only; browser uses Supabase anon key only.
- The AI rec → real show resolution step (external ID lookup + case-insensitive title match) needs the catalog API and must be deterministic — one server implementation, reused by Ask, Alchemy, and Explore Similar.
- Identity injection (`X-User-Id` in dev/test) is enforced at the server boundary.

### 2.3 Identity & isolation model (infra rider §4–5)

- **`namespace_id`** — build-isolation primitive. Read from `NAMESPACE_ID` env var at server start; stable for the lifetime of the build. Every persisted row carries it. Two namespaces never see each other's data. Not a user concept, never shown in UI.
- **`user_id`** — opaque stable string on every user-owned record. Resolution order (server-side helper `resolveUserId(request)`):
  1. Production mode: session from the auth provider (future OAuth — see §12).
  2. Dev/test mode (`IDENTITY_MODE=dev`): `X-User-Id` header if present, else `DEFAULT_USER_ID` env var.
  - The dev mechanism is documented in README and hard-disabled when `IDENTITY_MODE=production`.
- Effective partition for all reads/writes: `(namespace_id, user_id)`. All repository functions take both; no query path can omit them (enforced by a single `scopedClient(namespaceId, userId)` accessor + composite indexes + RLS-style policies where applicable).

### 2.4 Data flow: the user-overlay rule

Every surface that renders a show tile or detail merges catalog data with the user's saved row:

1. Client asks server for catalog data (search results, recs, mentioned shows…).
2. Server (or a shared client hook `useOverlaidShows`) joins against the user's collection by show `id` in a single batched lookup (`POST /api/collection/lookup` with a list of ids).
3. Saved shows render with My Data badges (in-collection indicator, rating indicator) and user-overlaid fields. **User edits always win over refreshed public data.**

---

## 3. Data Model (Supabase)

Migrations live in `supabase/migrations/*.sql` and are applied with the Supabase CLI (works against hosted instance; local optional). Seed data in `supabase/seed.sql` + fixtures for tests.

### 3.1 Tables

**`shows`** — one row per (namespace, user, show). Mirrors `storage-schema.ts` `Show`, normalized for Postgres:

| Column group | Columns |
|---|---|
| Keys | `namespace_id text`, `user_id text`, `id text` (catalog id), **PK** `(namespace_id, user_id, id)` |
| Identity | `title text not null`, `show_type text check in ('movie','tv','person','unknown')`, `external_ids jsonb` |
| Catalog meta | `overview`, `genres text[] default '{}'`, `tagline`, `homepage`, `original_language`, `spoken_languages text[]`, `languages text[]` |
| Images | `poster_url`, `backdrop_url`, `logo_url`, `network_logos text[] default '{}'` (reserved) |
| Ratings/popularity | `vote_average double precision`, `vote_count int`, `popularity double precision` |
| Dates | `last_air_date`, `first_air_date`, `release_date` (timestamptz) |
| Movie | `runtime int`, `budget bigint`, `revenue bigint` |
| TV | `series_status text`, `number_of_episodes int`, `number_of_seasons int`, `episode_run_time int[]`, `last_episode_run_time int` (reserved) |
| My Data | `my_tags text[] default '{}'` + `my_tags_update_date`, `my_score double precision` + `my_score_update_date`, `my_status text check in ('active','next','later','done','quit','wait')` + `my_status_update_date`, `my_interest text check in ('excited','interested')` + `my_interest_update_date` |
| AI | `ai_scoop text`, `ai_scoop_update_date timestamptz` |
| Management | `details_update_date`, `creation_date`, `is_test boolean default false` |
| Providers | `provider_data jsonb` (IDs by country: `{countries: {US: {flatrate:[], rent:[], buy:[]}}}`) |

Indexes: PK; `(namespace_id, user_id, my_status)`; GIN on `my_tags`; `(namespace_id, user_id, is_test)`.

Collection-membership invariant: a row exists **iff** the show is in collection (`my_status` non-null). Removal = row delete. Transient data (cast, crew, seasons, videos, images, recommendations, similar) is **never persisted** — always re-fetched from catalog.

**`cloud_settings`** — synced settings per (namespace, user):
`namespace_id`, `user_id`, `id text default 'globalSettings'` (PK triple), `user_name text` (random friendly name on first launch), `version double precision` (epoch seconds, conflict resolution), `catalog_api_key text null`, `ai_api_key text null`, `ai_model text`. In benchmark mode API keys come from env vars; user-entered keys are optional overrides and never committed anywhere.

**`app_metadata`** — `namespace_id`, `user_id`, `data_model_version int default 3` (PK pair). Drives forward-migration of user data across model versions (§12 continuity).

### 3.2 Client-local storage (disposable cache only)

Per `storage-schema.md` key-value settings, stored in `localStorage` namespaced by `namespace_id:user_id`:
- `autoSearch: boolean` (Search on launch), `fontSize: "XS"|"S"|"M"|"L"|"XL"|"XXL"`
- `hideStatusRemovalConfirmation: boolean`, `statusRemovalCount: number`
- `lastSelectedFilter: {type: "all"|"genre"|"myStatus"|"communityScore"|"decade"|"myTag", label, value}`

These are UI conveniences; losing them loses no user-owned data. (Decision: `autoSearch`/`fontSize` stay local per the schema doc; username/keys/model are cloud-synced per the PRD settings section.)

### 3.3 Merge engines (core correctness logic — server-side, heavily unit-tested)

**A. Catalog merge (`mergeCatalogIntoStored(fresh, stored)`)** — applied whenever catalog details are fetched for an already-saved show:
- Non-my fields: `selectFirstNonEmpty(new, old)` — never overwrite non-empty string/array with empty, never overwrite non-nil with nil.
- My fields: untouched by catalog merges (catalog payloads carry no My Data).
- `details_update_date = now()`; `creation_date` set only on first insert.

**B. Sync/import merge (`mergeUserRows(a, b)`)** — applied on import/restore and any cross-device conflict:
- Per My-field group, compare update dates: both present → newer wins; one present → that side wins.
- Duplicates (same `(namespace, user, id)`) merge transparently, no user disruption.
- AI Scoop merges by `ai_scoop_update_date` the same way.

---

## 4. External Integrations

### 4.1 Catalog provider adapter (`src/server/catalog/`)

A single adapter module isolates the vendor (TMDB-shaped). Endpoints wrapped:
- `searchShows(query)` → multi search (movies + TV), mapped to `Show` DTOs.
- `getShowDetails(id, mediaType)` → details + `append_to_response` for credits, videos, images, watch providers, recommendations, similar, seasons.
- `getPerson(id)` → bio, images, combined credits.
- `resolveByExternalId(externalId, mediaType)` and `resolveByTitle(title, mediaType)` → used by AI rec resolution.

Mapping rules (from `storage-schema.md`): catalog id → `id`; prefer title (movie) / name (TV), reject if neither; media type from payload else infer (`name`→tv, `title`→movie, else unknown→reject); genre IDs → names; image paths → full URLs; pick one best logo deterministically (highest-rated, prefer English); providers stored as IDs by region; multiple accepted date formats.

### 4.2 AI provider adapter (`src/server/ai/`)

- Anthropic client, server-only key (`AI_API_KEY` env; user-entered override from cloud settings if set). Model from `AI_MODEL` / settings.
- Streaming support (SSE from route handlers) for Scoop and Ask.
- Structured-output helper: request → parse → on parse failure retry **once** with stricter formatting instructions → else fall back (unstructured commentary + Search handoff), per `ai_prompting_context.md` §5.

### 4.3 AI rec → real show resolution (`resolveRecommendation`)

Per PRD §5.8, for each AI-recommended `{title, externalId?, mediaType}`:
1. If `externalId` present: look up catalog by that ID; accept the first result whose title matches **case-insensitively**.
2. Else (or on miss): title search, accept first case-insensitive title match of the right media type.
3. Found → real selectable Show carrying the AI "reason" as transient text.
4. Not found → render non-interactive title with a "Search for this" handoff.

This function is the single gate for Ask mentions, Alchemy results, and Explore Similar results. **Real-show integrity is the non-negotiable quality bar** (`discovery_quality_bar.md` §4).

---

## 5. Server API Surface

All routes require identity resolution (§2.3); mutations are namespace+user scoped.

**Collection & My Data**
- `GET /api/collection` — user's full collection (supports filter params: status, tag, genre, decade, score range, media type).
- `POST /api/collection/lookup` — batch: given show ids, return saved rows (for overlay/badges).
- `PUT /api/collection/:id/status` — set status. Body includes full catalog snapshot on first save. Implements save triggers + defaults (§6.1).
- `DELETE /api/collection/:id` — remove from collection (clears **all** My Data by deleting the row).
- `PUT /api/collection/:id/interest` — set interest (implies status=later on unsaved).
- `PUT /api/collection/:id/rating` / `DELETE …/rating` — rate (auto-save as Done if unsaved) / clear rating.
- `PUT /api/collection/:id/tags` — replace tag list (auto-save as Later+Interested if unsaved).
- `GET /api/collection/tags` — distinct tag library + whether tagless shows exist (sidebar).

**Catalog proxy**
- `GET /api/catalog/search?q=`, `GET /api/catalog/show/:mediaType/:id`, `GET /api/catalog/person/:id`, `GET /api/catalog/providers` (provider ID → name/logo metadata).

**AI**
- `POST /api/ai/ask` — chat turn (streams). Input: recent turns + rolling summary + optional handoff show + taste profile. Output: structured `{commentary, showList}`; server resolves showList and returns resolved mentioned shows.
- `POST /api/ai/scoop/:id` — streams Scoop; server persists to `shows.ai_scoop` only if row exists (in collection); returns cached scoop if fresher than 4h.
- `POST /api/ai/concepts` — 1..n show inputs → concept list (single-show: Explore Similar; multi-show: Alchemy shared concepts).
- `POST /api/ai/concept-recs` — selected concepts + source shows + surface (`explore`→5 recs, `alchemy`→6 recs) → resolved recommendations with reasons.
- `POST /api/ai/summarize` — summarize older chat turns in-persona (invoked by ask route when turn count > ~10).
- `GET /api/ai/starter-prompts` — 6 random prompts from the 80-prompt pool (server holds the pool; refresh returns a new random 6).

**Settings & data**
- `GET/PUT /api/settings` — cloud settings (username, model, optional key overrides; `version` epoch-seconds newer-wins).
- `GET /api/export` — streams `.zip` containing `backup.json`: all saved shows + My Data + settings, dates ISO-8601, plus `dataModelVersion` and export timestamp (schema documented for future Import).

**Test support (gated: available only when `IDENTITY_MODE=dev` or `NODE_ENV=test`)**
- `POST /api/test/reset` — deletes all rows for the current namespace (optionally only `is_test=true` rows, or a specific test user). Never touches other namespaces; no global teardown.
- `POST /api/test/seed` — inserts fixture collection for the given user.

---

## 6. Business Rules (single domain module: `src/server/domain/collection-rules.ts`)

These rules are the heart of correctness; implemented once, used by all routes, exhaustively unit-tested.

### 6.1 Save triggers & defaults (PRD §5.2–5.3)

| Action on unsaved show | Resulting save |
|---|---|
| Set any status | that status |
| Choose interest chip (Interested/Excited) | `status=later`, `interest=` chosen |
| Rate | `status=done` (rating implies watched) |
| Add ≥1 tag | `status=later`, `interest=interested` |
| Any save without explicit status | `status=later`, `interest=interested` |

On every save: set the relevant `*_update_date` timestamps to now; `creation_date` on first insert; snapshot catalog fields into the row.

### 6.2 Status & interest semantics (PRD §4.2–4.3)

- Statuses: `active`, `later`, `wait`, `done`, `quit`; **`next` exists in the model/DB enum but is not surfaced in UI** (kept for forward compatibility).
- Interest (`interested`/`excited`) applies only when status is `later`; UI surfaces the two interest chips as primary status chips — selecting one sets `status=later` + that interest.
- When status moves away from `later`, interest is **retained in storage** (irrelevant until show returns to Later) — display logic ignores it for non-Later statuses.

### 6.3 Removal (PRD §5.4)

- Trigger: reselecting the currently-active status chip → confirmation dialog ("this clears your data") → on confirm, delete row (clears status, interest, tags, rating, Scoop).
- Confirmation counter: after repeated removals (increment `statusRemovalCount`), offer "stop asking"; if accepted set `hideStatusRemovalConfirmation` and skip future dialogs.

### 6.4 Re-add / refresh (PRD §5.5) — via merge engine §3.3.

### 6.5 Tile indicators (PRD §5.9)

Shared `ShowTile` component renders: in-collection badge when `my_status` exists; rating badge when `my_score` exists. Used identically in Home, Search, recs strands, mentioned-shows strip, Alchemy results, filmography.

---

## 7. Frontend Plan (fractal architecture per `INSTRUCTIONS.md`)

### 7.1 Directory skeleton

```
src/
├── config/                      # env access, constants (CONCEPT_MAX_SELECT=8,
│                                #   EXPLORE_REC_COUNT=5, ALCHEMY_REC_COUNT=6,
│                                #   SCOOP_TTL_HOURS=4, SUMMARIZE_AFTER_TURNS=10,
│                                #   STARTER_PROMPT_COUNT=6, MIN_ALCHEMY_SHOWS=2)
├── theme/                       # design tokens: colors, spacing, type scale,
│                                #   fontSize map XS–XXL (no hex/px in TSX)
├── components/                  # ShowTile, PosterGrid, Strand (horizontal rail),
│                                #   Chip, ConfirmDialog, RatingBar, ScoreBar,
│                                #   EmptyState, StreamingText, MediaTypeToggle
├── hooks/                       # useIdentity, useOverlaidShows, useLocalSetting,
│                                #   useCollection (React Query wrappers)
├── utils/                       # date/format helpers, showList parser (client mirror)
├── server/                      # (non-page code) domain/, catalog/, ai/, db/
└── app/                         # Next.js App Router routes → thin wrappers around:
    └── pages-src/
        ├── Home/                            # filtered library
        │   └── features/
        │       ├── FilterSidebar/           # All Shows, tag filters (+No tags),
        │       │                            #   genre/decade/score filters
        │       ├── StatusSections/          # Active(large tiles)/Excited/Interested
        │       │   └── features/OtherStatusesGroup/   # collapsed Wait/Quit/Done/
        │       │                                      #   Later-without-interest
        │       └── MediaTypeToggle/
        ├── Find/                            # hub with mode switcher
        │   └── features/
        │       ├── ModeSwitcher/            # Search | Ask | Alchemy
        │       ├── Search/                  # input, poster grid, in-collection marks
        │       ├── Ask/
        │       │   └── features/
        │       │       ├── WelcomeStarters/ # 6 random prompts + refresh
        │       │       ├── ChatThread/      # turns, streaming, summarization state
        │       │       └── MentionedShowsStrip/
        │       └── Alchemy/
        │           └── features/
        │               ├── ShowPicker/      # 2+ shows from library + catalog search
        │               ├── ConceptCatalysts/# chips, max 8 selected
        │               └── AlchemyResults/  # 6 recs + reasons + "More Alchemy!"
        ├── Detail/
        │   └── features/  (ordered per detail_page_experience.md §3)
        │       ├── HeaderMedia/             # backdrop/poster/logo carousel, inline trailer
        │       ├── CoreFacts/               # year, runtime|seasons/episodes, score bar
        │       ├── StatusToolbar/           # chips: Active/Interested/Excited/Done/Quit/Wait
        │       ├── TagChips/                # display + picker
        │       ├── OverviewScoop/           # overview + Scoop toggle/stream
        │       ├── AskAboutCta/
        │       ├── GenresLanguages/
        │       ├── RecommendationsStrand/   # traditional similar/recommended
        │       ├── ExploreSimilar/          # Get Concepts → chips → Explore Shows (5 recs)
        │       ├── StreamIt/                # providers by region
        │       ├── CastCrew/                # strands → Person
        │       ├── Seasons/                 # TV only
        │       └── BudgetRevenue/           # movies when available
        ├── Person/
        │   └── features/ ImageGalleryBio/, AnalyticsCharts/, FilmographyByYear/
        └── Settings/
            └── features/ AppearanceSettings/, UserSettings/, AiSettings/,
                          IntegrationSettings/, YourData/   # Export My Data (zip)
```

Rules honored throughout: no `index.tsx` (main file matches directory), humble components (all logic in `useXxxLogic` hooks), no magic numbers/inline styles (config + theme tokens), co-location of feature-specific hooks/utils, unit tests adjacent to source.

### 7.2 Key screen behaviors

**Home** — sections in fixed order: Active (larger tiles) → Excited (Later+excited) → Interested (Later+interested) → "Other" collapsed group (Wait, Quit, Done, Later w/o interest). Sidebar filters compose with media-type toggle on top. Recently-updated sorting inside sections (via `*_update_date`). Empty states: no collection → prompt to Search/Ask; filter empty → "No results found." Last selected filter persists locally.

**Search** — plain catalog search (no AI voice — `ai_voice_personality.md` §1), live queries (no pre-loading requirement), poster grid, in-collection marks, tile → Detail. If `autoSearch` setting on, app opens into Find→Search on launch.

**Ask** — welcome state with 6 refreshable starter prompts (from the 80-prompt pool). Chat: user/assistant turns; assistant output is `commentary` (never shows raw IDs); mentioned shows render as horizontal strip of real tiles (tap → Detail; unresolved → Search handoff). After ~10 messages, older turns are summarized in-persona and replace the raw turns in context. Session-only: history clears on reset/leave. **Ask About a Show**: entering from Detail seeds context with that show (handoff show injected into system context; open question on exact prefill noted in §14).

**Alchemy** — stepper cards: (1) pick 2+ shows (from library or catalog search); (2) **Conceptualize Shows** → shared-concept chips (larger pool than single-show); (3) select 1–8 catalysts (selection changes clear downstream results); (4) **ALCHEMIZE!** → 6 recs with concept-citing reasons; (5) **More Alchemy!** chains results as new inputs. Changing input shows clears concepts + results. All state session-only.

**Detail** — sections in the exact order of `detail_page_experience.md` §3 (header media → core facts/score → tags → overview+Scoop → Ask CTA → genres/languages → recs strand → Explore Similar → providers → cast/crew → seasons (TV) → budget/revenue (movies)). Status chips live in the **toolbar**, not the scroll body. Scoop toggle copy: "Give me the scoop!" (none) / "Show the scoop" (cached) / "The Scoop" title when open; streams progressively with "Generating…" state; 4-hour freshness; persists only when in collection. Explore Similar: "Get Concepts" CTA → chips (cap consistent with Alchemy's 8) → "Explore Shows" → 5 recs. Critical states handled: unsaved show (ephemeral scoop, auto-save triggers), no trailers/backdrops (premium poster/logo fallback), no concepts yet, TV vs movie field handling.

**Person** — image gallery + bio; analytics charts (average project ratings, top genres, projects-by-year — lightweight client-side charts from combined credits); filmography grouped by year; credit tap → Detail.

**Settings** — font size (XS–XXL applied via theme), Search-on-launch toggle, username (synced), AI key/model (synced; env fallback in benchmark mode), catalog key (synced; env fallback), **Export My Data** → downloads zip (JSON, ISO-8601 dates). Import/Restore: out of scope now (open question) but export format is versioned and documented to make it implementable without schema change.

---

## 8. AI Surface Implementation

### 8.1 Prompt architecture (`src/server/ai/prompts/`)

One **base persona** module (fun, chatty TV/movie nerd; joy-forward; opinionated honesty; vibe-first spoiler-safe; specific not generic; brisk by default) composed with per-surface modes, so all surfaces feel like one persona. Tone-slider defaults encoded as prompt guidance (70/30 friend-critic, 60/40 hype-measured, playfulness adaptive, concise-by-default). Shared rules injected everywhere: stay in TV/movies (redirect out-of-domain), spoiler-safe unless explicitly asked, honest about mixed reception, no generic filler.

Per-surface contracts:
- **Ask / Explore Search Chat**: friend-in-dialogue; direct answer in first 3–5 lines; bullets for multi-recs; confident picks; emotional chameleon (mirrors the show's tone); structured output `{commentary, showList}` with `Title::externalId::mediaType;;…` format — parser and format defined in one shared module with exhaustive tests (round-trip, empty list, delimiter edge cases). Taste context: compact library summary (statuses, interests, tags, ratings) + rolling conversation summary.
- **Scoop**: mini blog-post of taste, ~150–350 words; sections: personal take → honest stack-up vs reviews → "The Scoop" centerpiece paragraph (most real estate) → fit/warnings → "Worth it?" verdict. Streams via SSE.
- **Concepts**: bullet list only; **8 concepts by default**; 1–3 words; evocative, no explanations, no plot/spoilers; banned-generic list ("good characters," "great story," "funny," "action"); axes diversity (structure/vibe/emotion/relationships/craft/genre-flavor); ordered best-first; multi-show → concepts shared across **all** inputs, larger pool returned than single-show.
- **Concept recs**: 5 (Explore Similar) / 6 (Alchemy); each reason 1–3 sentences explicitly naming matched concept(s); recency bias without dogma; excited-friend tone.
- **Summarizer**: 1–2 sentence summaries of older turns, in-persona (no sterile system voice).

### 8.2 Quality bar & regression harness

Adopt `discovery_quality_bar.md` as acceptance criteria: voice adherence, taste alignment, surprise-without-betrayal, specificity, and **real-show integrity = 2/2 non-negotiable** (guaranteed structurally by the resolution gate — unresolved titles are never rendered as interactive recs). Ship a small eval script (`npm run eval:ai`, manual/optional) that runs golden prompts and prints outputs for human scoring per the 0–2 rubric; golden set left unpopulated per the doc, template checked in.

---

## 9. Infrastructure Deliverables (infra rider compliance)

### 9.1 Environment (`.env.example`, committed; `.gitignore` excludes `.env*` except `.env.example`)

```
# --- Isolation & identity ---
NAMESPACE_ID=            # stable per-build namespace; partitions all persisted data
IDENTITY_MODE=dev        # dev | production; dev enables X-User-Id header + default user
DEFAULT_USER_ID=         # opaque string used when no X-User-Id provided (dev/test)

# --- Supabase ---
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=   # browser-safe anon key only
SUPABASE_SERVICE_ROLE_KEY=       # server-only; never exposed to client bundles

# --- Providers ---
CATALOG_API_KEY=         # content catalog provider (server-side)
AI_API_KEY=              # AI provider (server-side)
AI_MODEL=                # default model id
```

Runs with env fill-in only — no source edits. Server code imports secrets solely via `src/config/server-env.ts` (never `NEXT_PUBLIC_`).

### 9.2 Scripts (`package.json`)

- `npm run dev` — start app.
- `npm test` — unit + integration tests (Vitest).
- `npm run test:e2e` — Playwright suite (uses `X-User-Id` test users; all rows `is_test=true`).
- `npm run test:reset` — namespace-scoped reset via `/api/test/reset` (or direct script) — deletes only current namespace's data; **no global teardown ever**.
- `npm run db:migrate` / `db:seed` — deterministic fresh schema + fixtures against hosted or local Supabase.
- `npm run eval:ai` — optional golden-set runner.

### 9.3 Compliance checklist mapping (rider §9)

| Rider criterion | Where satisfied |
|---|---|
| `.env.example`, config without code edits | §9.1 |
| Repeatable runs, no collisions | `namespace_id` on every row + scoped accessor (§2.3, §3.1) |
| All user records carry `user_id` | PKs include it; repository layer requires it (§3.1) |
| Destructive tests, no global teardown | `/api/test/reset` + `is_test` flag (§5, §9.2) |
| OAuth later without schema redesign | `user_id` opaque string; only `resolveUserId()` changes (§2.3, §12) |
| No Docker required | hosted Supabase primary path; local documented optional (§3) |

---

## 10. Testing Strategy

- **Unit (Vitest, adjacent to source):** priority on the domain layer — save triggers/defaults matrix (§6.1), removal semantics, interest retention, catalog merge `selectFirstNonEmpty`, per-field timestamp merge, showList parser round-trips, rec resolution (ID hit, ID miss + title fallback, unresolvable), scoop TTL, filter composition, date parsing.
- **Integration:** API routes against a test namespace in real Supabase (test users, `is_test=true`), verifying `(namespace_id, user_id)` scoping — including a test that two namespaces cannot see each other's rows.
- **E2E (Playwright):** the 10 key journeys from PRD §9 (build collection, rate-to-save, tag-to-save, maintain, tag filters, Ask discovery, Explore Similar, Alchemy chain, talent deep-dive, export). AI calls mocked with recorded structured outputs for determinism; one live smoke test optional.
- **Visual tests:** Playwright screenshots for ShowTile badge states, Home section grouping, Detail section order, empty states (per INSTRUCTIONS.md "visual testing highly preferred").
- **AI quality:** manual rubric via `eval:ai` (§8.2).

---

## 11. Implementation Phases

**Phase 0 — Foundation (scaffold + infra)**
Next.js app scaffold, theme/config/token setup, Supabase project + migrations + seed, env interface, identity resolution (`resolveUserId`, namespace plumbing), scoped repository layer, test reset/seed endpoints, CI-ready scripts. *Exit: `npm run dev` boots against hosted Supabase; isolation integration test passes.*

**Phase 1 — Catalog + Collection core**
Catalog adapter (search/details/person/providers), Show mapping + merge engines, collection CRUD routes with full business rules (§6), ShowTile + overlay hook. *Exit: domain unit-test matrix green; rate-to-save / tag-to-save / removal verified.*

**Phase 2 — Primary UI: Home, Search, Detail (non-AI)**
Home with status sections + sidebar filters + media toggle + empty states; Find hub + Search mode (+ auto-open setting); Detail page all non-AI sections in spec order incl. status toolbar, rating bar, tags, providers, cast/crew, seasons, budget/revenue; Person page. *Exit: journeys 1–5, 9 pass E2E.*

**Phase 3 — AI surfaces**
AI adapter + persona/prompt modules + structured-output pipeline + rec resolution gate; Scoop (streaming, TTL, conditional persistence); Ask (starters, chat, mentions strip, summarization, Ask-about-show seeding); Explore Similar; Alchemy full flow with chaining. *Exit: journeys 6–8 pass; real-show integrity tests green; quality rubric spot-check.*

**Phase 4 — Settings, export, continuity, polish**
Settings screens (font size theming, autoSearch, username, keys/model with env fallback), cloud-settings sync semantics (`version` newer-wins), Export zip, `data_model_version` migration hook (v3 baseline + forward-migration harness with a fixture test proving old-shaped data upgrades losslessly), removal-confirmation "stop asking" counter, empty/error/loading states audit, visual test pass, README (setup, identity injection docs, optional local Supabase, prod-gating of dev identity).

Dependencies are strictly forward; each phase is demoable. Estimated relative weight: P0 10%, P1 25%, P2 25%, P3 30%, P4 10%.

---

## 12. Forward-Compatibility Commitments

- **OAuth migration:** swap `resolveUserId()` to session-based lookup (e.g., Supabase Auth/Google); `user_id` stays opaque; zero schema change. Dev header path deleted or gated off.
- **Data continuity (PRD §5.11):** `app_metadata.data_model_version` checked on boot; ordered idempotent migration functions bring old rows forward automatically; export format carries version for the same reason.
- **Provider swaps:** catalog and AI vendors are isolated behind adapters; rider behavioral requirements are vendor-independent.
- **`next` status & myStatus sidebar filters:** already in enum/`FilterType` — UI-only work if promoted later.

## 13. Risks & Mitigations

| Risk | Mitigation |
|---|---|
| AI structured output drifts from `Title::externalId::mediaType;;` format | Single shared parser + strict-retry-once + fallback to commentary + Search handoff (spec'd behavior); parser fuzz tests |
| Hallucinated/mismatched recs break real-show integrity | Resolution gate before render; unresolved = non-interactive + Search handoff; integration tests with adversarial fixtures |
| Catalog rate limits during recs resolution (up to 6 lookups/round) | Server-side batching + short-lived LRU cache on catalog responses (cache is disposable, correctness unaffected) |
| Streaming (Scoop/Ask) on serverless timeouts | SSE route handlers with streaming-friendly runtime; chunked persistence of Scoop on completion only |
| Merge-rule regressions corrupting My Data | Merge engines pure + exhaustively unit-tested; per-field timestamps asserted in integration tests |
| Namespace leakage in ad-hoc queries | Only `scopedClient()` exposes DB access; lint rule/code review gate on raw client imports |

## 14. Open Questions (flagged, not blocking — defaults chosen)

From PRD §10 + docs, with our default stance:
- **Ask-about-show prefill** (TBD in PRD): default = inject show as system context + assistant greeting referencing it; no fake user message.
- Scoop on unsaved show implicitly saving: **no** (spec: ephemeral unless saved).
- Clearing rating → store nil (not explicit Unrated state).
- Import/Restore, named lists, Alchemy blends sharing, `next` status UI, myStatus sidebar filters: deferred; noted in §12 where schema already accommodates them.
- Companion docs `where_is_the_heart_opus.md` / `ai_personality_opus.md` / `philosophy_opus.md` are referenced by the PRD but not present in this repo; the voice/personality supporting docs provided are treated as the authoritative substitutes.
