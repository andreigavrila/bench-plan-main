# Implementation Plan — Personal TV & Movie Companion

**Sources:** `docs/prd/product_prd.md` (functional spec), `docs/prd/infra_rider_prd.md` (execution/infra constraints), and all supporting docs: `ai_prompting_context.md`, `ai_voice_personality.md`, `concept_system.md`, `detail_page_experience.md`, `discovery_quality_bar.md`, `technical_docs/storage-schema.md` + `storage-schema.ts`. Architectural standards from repo `INSTRUCTIONS.md` (fractal architecture, humble components, co-location).

**Note on companion docs:** Product PRD §12 references `where_is_the_heart_opus.md`, `ai_personality_opus.md`, and `philosophy_opus.md`. These files are not present in `docs/prd/`. Their content areas (persona, prompts, starter-prompt pool, emotional design) are covered by the supporting docs above; where the missing docs contained concrete assets (e.g., the 80 starter prompts, verbatim prompt text), this plan schedules them as content-authoring tasks constrained by `ai_voice_personality.md` + `ai_prompting_context.md`.

---

## 1. What We Are Building (Scope Summary)

A personal TV + movie companion web app. Users build *their version* of each show — status, interest, tags, rating, notes/AI Scoop — and the app uses that taste profile to power four discovery paths:

1. **Search** — straightforward external-catalog search (no AI voice).
2. **Ask** — conversational AI discovery with a "mentioned shows" strip.
3. **Alchemy** — blend 2+ shows → shared concept catalysts → 6 grounded recommendations → chainable.
4. **Explore Similar** — per-show concepts → 5 grounded recommendations (on Show Detail).

Plus: a status/interest/tag-organized Collection Home with filters, a rich Show Detail page (the "single source of truth" for a show), Person Detail with filmography + analytics charts, Settings (appearance, behavior, user, AI, integrations), and first-class data export.

**Benchmark baseline (mandatory):** Next.js (latest stable) as UI + server boundary; Supabase (hosted preferred) as persistence via official client libraries; no Docker required; namespace-isolated, user-scoped data; dev identity injection instead of real OAuth; backend is the source of truth.

---

## 2. Guiding Decisions (made up front, with rationale)

| # | Decision | Rationale |
|---|----------|-----------|
| D1 | **All persistence goes through Next.js server code** (route handlers + server modules) using the Supabase JS client with the service-role key, server-only. The browser never talks to Supabase directly and holds no Supabase key. | Satisfies rider §3.1 credential rules by construction (elevated key server-only; nothing sensitive in client). Centralizes namespace/user scoping and business rules server-side (rider §6.1, PRD §8.9). RLS is enabled with deny-all anon policies as defense-in-depth. |
| D2 | **Catalog provider = TMDB behind a `CatalogProvider` adapter interface.** | The storage schema (voteAverage, popularity, flatrate/rent/buy provider IDs, posters/backdrops/logos, seasons) is TMDB-shaped. PRD is provider-agnostic, so all TMDB specifics live in one adapter module; `Show.externalIds` stays an opaque map (`{ tmdb: "603" }`). |
| D3 | **AI provider = Anthropic Claude behind an `AiProvider` adapter interface.** Official `@anthropic-ai/sdk`. Default model `claude-opus-4-8`; user-selectable model list in Settings (PRD §7.7). Key from env in benchmark mode (`AI_API_KEY`); optional user-entered key stored server-side, never committed. | PRD requires AI provider key + model selection as settings; adapter keeps the app provider-swappable. Streaming for Scoop, structured output for Ask-with-mentions (see §8). |
| D4 | **Identity:** `user_id` is an opaque string resolved per-request by a single `resolveIdentity()` helper — dev/test: `X-User-Id` header override, else `DEFAULT_USER_ID` env; production mode: requires a real session (future OAuth) and rejects header injection. `namespace_id` comes from `NAMESPACE_ID` env, stamped on every row. | Rider §4–5 verbatim. Replacing dev injection with OAuth is a resolver swap, not a schema change. |
| D5 | **Client caching = TanStack Query (in-memory) only; session-only AI state in a lightweight store (Zustand).** No critical data in localStorage; clearing client storage loses nothing. | Rider §6.2 (cache is disposable), PRD §5.7 (Alchemy/Ask state is session-only by *requirement* — deliberately not persisted). |
| D6 | **Fractal front-end architecture per `INSTRUCTIONS.md`**, with one documented adaptation: the page tree lives at `src/screens/` instead of `src/pages/`, because Next.js reserves any `pages/`/`src/pages/` directory for its legacy Pages Router — component files there would register as junk routes. Everything else follows INSTRUCTIONS.md exactly: `ScreenName/ScreenName.tsx`, nested `features/`, co-located `hooks/`/`utils/`, no `index.tsx`, humble components, no magic numbers/inline styles, theme tokens only. `src/app/` contains only thin route shells that import screen components. | Preserves the pattern's intent (testability, change isolation) without fighting the framework. |
| D7 | **User settings are server-persisted** (one row per namespace+user), including "local" preferences (font size, search-on-launch, removal-confirmation suppression, last filter). Client caches them via Query for snappiness. | PRD §8.9 "clearing client storage must not lose user data"; PRD §7.7 says username/AI key/model/catalog key sync across devices — one settings row gives us that for free since the backend is shared. Storage-schema's "local settings" distinction reflects the legacy on-device app; the rider supersedes it. |
| D8 | **Styling = CSS Modules + design tokens as CSS custom properties** generated from `src/theme/`. No Tailwind-style utility classes in markup. | INSTRUCTIONS.md: "styling concerns live in the style system, not in markup"; "no hex codes, colors, or pixel values in TSX." |
| D9 | **Open questions from PRD §10 resolved for v1** (documented in §16): `next` status stays data-model-only; no named custom lists; Scoop on unsaved show does *not* implicitly save; clearing rating = `null` (no explicit Unrated state); Import/Restore deferred but export format designed to be re-importable; no saved Alchemy blends; no sidebar myStatus filters (model supports them). | PRD marks all of these optional; v1 ships the required behavior and keeps the extensions cheap. |

---

## 3. System Architecture

```
┌────────────────────────────── Browser ──────────────────────────────┐
│  Next.js React app (App Router client components)                   │
│  • src/screens/* fractal UI (humble components + hooks)             │
│  • TanStack Query cache (disposable)  • Zustand session stores      │
│  • SSE/stream consumption for Scoop & Ask                           │
└──────────────┬───────────────────────────────────────────────────────┘
               │ fetch /api/* (JSON + SSE)   [X-User-Id in dev/test]
┌──────────────▼───────────────────────────────────────────────────────┐
│  Next.js server (route handlers, src/server/*)                       │
│  • identity.ts  → (namespace_id, user_id) on every request           │
│  • domain/      → business rules: save triggers, defaults, removal,  │
│                   merge engine, timestamps, tile badge derivation     │
│  • repo/        → Supabase data access (service-role, server-only)   │
│  • catalog/     → CatalogProvider interface + TmdbProvider           │
│  • ai/          → AiProvider (Anthropic) + per-surface prompt        │
│                   builders, parsers, summarizer, resolver, guardrails │
│  • export/      → zip builder (JSON backup, ISO-8601 dates)          │
└─────┬───────────────────────┬────────────────────────┬───────────────┘
      │                       │                        │
┌─────▼──────┐        ┌───────▼────────┐       ┌───────▼────────┐
│  Supabase  │        │  TMDB API      │       │  Anthropic API │
│  Postgres  │        │  (catalog)     │       │  (AI)          │
│  (hosted)  │        └────────────────┘       └────────────────┘
│  rows keyed by (namespace_id, user_id)                          │
└─────────────────────────────────────────────────────────────────┘
```

Key properties:

- **Backend is the source of truth** (PRD §8.9 / rider §6). Every user-owned record carries `(namespace_id, user_id)`.
- **Catalog data is two-tier:** live TMDB fetches for transient data (credits, seasons, videos, recommendations, similar, images) that is *never persisted* (storage schema "Not stored" list); a snapshot of persistable fields is stored on the user's `shows` row when a show is saved, merged under the rules in §7.3.
- **Display rule** (PRD §4.1): every list/strip/grid that renders shows passes catalog results through a server-side (or hook-level) overlay step that merges the user's saved version on top — user fields always win.

---

## 4. Repository Layout

```
.
├── .env.example                # all vars, commented (rider §3.1)
├── .gitignore                  # excludes .env* except .env.example
├── package.json                # scripts: dev/build/start/test/test:reset/db:*
├── next.config.ts
├── supabase/
│   ├── migrations/             # 0001_init.sql, ... (deterministic fresh DB)
│   └── seed/                   # optional fixtures (test data, is_test=true)
├── scripts/
│   ├── db-migrate.ts           # applies migrations via DATABASE_URL (no Docker)
│   ├── db-seed.ts
│   └── test-reset.ts           # deletes all rows for NAMESPACE_ID (rider §7)
├── src/
│   ├── app/                    # Next.js App Router — thin shells only
│   │   ├── layout.tsx, page.tsx            → HomeScreen
│   │   ├── find/page.tsx                   → FindScreen (?mode=search|ask|alchemy)
│   │   ├── show/[id]/page.tsx              → ShowDetailScreen
│   │   ├── person/[id]/page.tsx            → PersonDetailScreen
│   │   ├── settings/page.tsx               → SettingsScreen
│   │   └── api/…                           → route handlers (see §6)
│   ├── screens/                # fractal tree (see §9) — INSTRUCTIONS.md pattern
│   ├── components/             # shared primitives (ShowTile, Chip, PosterGrid…)
│   ├── hooks/                  # global hooks (useIdentityHeaders, useSettings…)
│   ├── utils/                  # global pure functions
│   ├── config/                 # constants: counts, cache TTLs, buckets, env access
│   ├── theme/                  # tokens → CSS custom properties, font scale
│   └── server/                 # server-only modules
│       ├── identity.ts
│       ├── domain/             # myShow rules, merge engine, filters
│       ├── repo/               # showsRepo, settingsRepo, metadataRepo
│       ├── catalog/            # CatalogProvider, TmdbProvider, mapping
│       ├── ai/                 # AiProvider, prompts/, parse/, resolve/, summarize/
│       └── export/
├── e2e/                        # Playwright journeys + visual snapshots
└── README.md                   # setup, env, identity injection, reset, no-Docker note
```

---

## 5. Data Model & Persistence (Supabase)

### 5.1 Tables

All user-owned tables share the isolation columns:

```sql
namespace_id text not null,     -- build/run isolation (rider §4.1)
user_id      text not null,     -- opaque stable string (rider §4.2)
```

**`shows`** — the user's saved show (public snapshot + My Data), mirroring `storage-schema.ts` `Show`:

```sql
create table shows (
  namespace_id text not null,
  user_id      text not null,
  id           text not null,            -- catalog id (e.g. TMDB id as string)
  title        text not null,
  show_type    text not null check (show_type in ('movie','tv','person','unknown')),
  external_ids jsonb,
  overview     text,
  genres       text[] not null default '{}',   -- names, not ids
  tagline      text, homepage text, original_language text,
  spoken_languages text[] not null default '{}',
  languages    text[] not null default '{}',
  poster_url   text, backdrop_url text, logo_url text,
  network_logos text[] not null default '{}',  -- reserved
  vote_average double precision, vote_count integer, popularity double precision,
  last_air_date timestamptz, first_air_date timestamptz, release_date timestamptz,
  runtime integer, budget bigint, revenue bigint,
  series_status text, number_of_episodes integer, number_of_seasons integer,
  episode_run_time integer[] not null default '{}',
  last_episode_run_time integer,               -- reserved
  my_tags text[] not null default '{}',        my_tags_update_date timestamptz,
  my_score double precision,                   my_score_update_date timestamptz,
  my_status text check (my_status in ('active','next','later','done','quit','wait')),
  my_status_update_date timestamptz,
  my_interest text check (my_interest in ('excited','interested')),
  my_interest_update_date timestamptz,
  ai_scoop text,                               ai_scoop_update_date timestamptz,
  details_update_date timestamptz,
  creation_date timestamptz not null default now(),
  is_test boolean not null default false,
  provider_data jsonb,                         -- { countries: { US: { flatrate:[…], rent:[…], buy:[…] } } } — IDs only
  primary key (namespace_id, user_id, id)
);
create index shows_status_idx on shows (namespace_id, user_id, my_status);
```

Notes:
- **"In collection" ≡ row exists** with non-null `my_status` (PRD §5.1). Because removal deletes the row (PRD §5.4), in practice every row has a status; the invariant is enforced in the domain layer (a row is only ever written with a status).
- Every `my*` field pairs with its `*_update_date` (PRD §5.6) — used for sorting, conflict resolution, and cache freshness.
- Transient catalog data (cast, crew, seasons, videos, images sets, recommendations, similar) is **not** stored (storage-schema "Not stored" list) — always re-fetched.

**`user_settings`** — one row per (namespace, user); supersedes CloudSettings/LocalSettings/UI-state keys from the reference schema (Decision D7):

```sql
create table user_settings (
  namespace_id text not null,
  user_id      text not null,
  id           text not null default 'globalSettings',
  user_name    text not null,                  -- random on first touch
  version      double precision not null,      -- epoch seconds, conflict resolution
  catalog_api_key text,                        -- optional user override (server-held)
  ai_api_key      text,                        -- optional user override (server-held)
  ai_model     text not null default 'claude-opus-4-8',
  auto_search  boolean not null default false, -- "Search on launch"
  font_size    text not null default 'M' check (font_size in ('XS','S','M','L','XL','XXL')),
  hide_status_removal_confirmation boolean not null default false,
  status_removal_count integer not null default 0,
  last_selected_filter jsonb,                  -- FilterConfiguration {type,label,value}
  primary key (namespace_id, user_id, id)
);
```

**`app_metadata`** — data-model versioning for continuity (PRD §5.11):

```sql
create table app_metadata (
  namespace_id text not null,
  user_id      text not null,
  data_model_version integer not null default 3,
  primary key (namespace_id, user_id)
);
```

### 5.2 Row-level security

RLS enabled on all tables with **no policies for `anon`/`authenticated`** (deny-all): the only access path is the server's service-role client. When real OAuth arrives, per-user policies (`user_id = auth.uid()::text`) can be added without schema change — `user_id` is already an opaque string (rider §5.2).

### 5.3 Migrations, seed, reset (rider §3.2–3.3, §7, §8)

- **Migrations:** plain SQL files in `supabase/migrations/`, applied by either `supabase db push` (hosted project — no Docker) or the bundled `npm run db:migrate` (node-postgres against `DATABASE_URL`). Fresh DB state is deterministic from the migration chain.
- **Seed:** `npm run db:seed` inserts optional fixtures with `is_test = true` under the current namespace.
- **Reset:** `npm run test:reset` deletes **all rows where `namespace_id = $NAMESPACE_ID`** across all tables. Destructive testing never requires global teardown; two namespaces can run tests concurrently without collisions.
- **Local Supabase via Docker:** documented as *optional* in README; the primary path is a provided hosted instance.

### 5.4 Sync, conflicts, duplicates (PRD §5.10)

With a single backend as source of truth, cross-device consistency is inherent. Residual conflict cases (two devices editing the same show while one request is in flight) resolve in the domain layer's merge engine: **per-field, newest `*_update_date` wins**; settings use the `version` (epoch seconds) field, newest wins. Duplicates are structurally impossible (`PK (namespace_id, user_id, id)`); saves are upserts that run the merge engine, which is exactly the PRD §5.5 re-add behavior.

### 5.5 Data continuity across versions (PRD §5.11)

- `app_metadata.data_model_version` starts at 3 (matching the reference schema).
- A server-side migration registry (`src/server/domain/dataMigrations.ts`) maps `version N → N+1` transforms over user rows. On first request for a user whose stored version < current, transforms run transparently inside a transaction, then the version is bumped. Users never lose statuses/tags/ratings/interest/Scoop on upgrade.
- Schema (SQL) migrations remain additive wherever possible; destructive column changes require a paired data migration.

---

## 6. Server API Design

All handlers: resolve `(namespace_id, user_id)` first; JSON errors with stable codes; input validation with zod.

### Collection & shows

| Route | Method | Behavior |
|---|---|---|
| `/api/shows` | GET | User's collection. Query params: `filter` (FilterConfiguration), `mediaType` (`all\|movie\|tv`). Returns shows grouped/sortable client-side; recently-updated ordering uses `my*_update_date` maxima. |
| `/api/shows/[id]` | GET | Stored user version of one show (or 404 → not in collection). |
| `/api/shows/[id]` | PUT | **The single write endpoint for My Data.** Body: any of `{ myStatus, myInterest, myTags, myScore, aiScoop }` + a catalog snapshot of the show (from the client's current detail payload). Server applies save-trigger/default/merge rules (§7). Returns the merged row. |
| `/api/shows/[id]` | DELETE | Removal (PRD §5.4): deletes the row → clears **all** My Data incl. Scoop. |
| `/api/filters` | GET | Sidebar filter model: All Shows; one filter per distinct tag (+ “No tags” if any saved show has no tags); data filters — genres present in the library, decades derived from release/first-air dates, community-score buckets (`9+`, `8–8.9`, `7–7.9`, `6–6.9`, `<6` — implementation-defined per PRD §4.5). |

### Catalog proxy (keys stay server-side)

| Route | Method | Behavior |
|---|---|---|
| `/api/catalog/search` | GET | `?q=` text search → poster-grid payload, each item overlaid with user data (`inCollection`, `myScore` badges — PRD §5.9). Live queries; no pre-loading (PRD §3). |
| `/api/catalog/shows/[type]/[id]` | GET | Full detail payload: persistable snapshot fields + transient blocks (images/videos, credits, seasons for TV, similar/recommended, watch providers with region, budget/revenue for movies). Overlaid with the stored user version if present (user fields win — PRD §4.1). Sets nothing in DB. |
| `/api/catalog/people/[id]` | GET | Person profile: images, bio, combined credits grouped by year; credits overlaid with in-collection badges. |

### AI surfaces (details in §8)

| Route | Method | Behavior |
|---|---|---|
| `/api/ai/ask` | POST | `{ turns, summary?, aboutShowId? }` → structured `{ commentary, mentionedShows[], updatedSummary? }`. Mentioned shows already resolved to real catalog items (or flagged unresolved). |
| `/api/ai/scoop` | POST (SSE) | `{ showId }` → streams Scoop text. Server enforces the 4-hour freshness rule and the persist-only-if-in-collection rule. |
| `/api/ai/concepts` | POST | `{ showIds: string[] }` (1 = Explore Similar, ≥2 = Alchemy) → ordered concept list. |
| `/api/ai/recommendations` | POST | `{ showIds, concepts, mode: 'explore'\|'alchemy' }` → 5 or 6 recommendations, each `{ show, reason }` resolved to real catalog items; unresolved ones returned as `{ title, reason, unresolved: true }`. |
| `/api/ai/starter-prompts` | GET | 6 random prompts from the authored pool (refreshable). |

### Settings, export, admin

| Route | Method | Behavior |
|---|---|---|
| `/api/settings` | GET/PUT | Read/update the `user_settings` row (version-checked write: newest wins). |
| `/api/export` | GET | Streams `export-YYYYMMDD.zip` containing `backup.json`: all saved shows + My Data + settings, **all dates ISO-8601** (PRD §7.7). Format documented and versioned so Import/Restore (deferred) can consume it. |
| `/api/dev/reset` | POST | Dev/test-mode-only mirror of `test:reset` (gated off in production mode). |

---

## 7. Business Rules Engine (`src/server/domain/`)

The heart of the app. Implemented as pure functions with exhaustive unit tests, called by the `/api/shows/[id]` PUT/DELETE handlers.

### 7.1 Save triggers & defaults (PRD §5.2–5.3)

`applyMyDataChange(existing: ShowRow | null, change, catalogSnapshot, now)`:

- Any of the following on an **unsaved** show creates the row ("saving triggers"):
  - setting any status → status as given;
  - choosing an interest chip → `myStatus='later'`, `myInterest` as chosen (PRD §4.2 nuance: *Interested*/*Excited* chips set Later + interest);
  - rating → **`myStatus='done'`** (rating implies watched), `myScore` as given;
  - adding ≥1 tag → defaults `myStatus='later'`, `myInterest='interested'`.
- Generic default when saving without explicit status: `later` + `interested`.
- Every changed `my*` field stamps its `*_update_date = now`. `creation_date` set only on insert. `details_update_date = now` whenever the catalog snapshot is merged.
- Interest is only *meaningful* while status is Later, but is **retained** when status moves away, so it's restored if the show returns to Later (PRD §4.3).

### 7.2 Removal (PRD §5.4, detail spec §3.3)

- Trigger: user **reselects the currently active status chip** → client shows a destructive confirmation.
- Confirmation policy: server increments `status_removal_count` per confirmation shown; once the user has confirmed ≥3 times the dialog offers **"Stop asking"**; selecting it sets `hide_status_removal_confirmation=true` and future removals skip the dialog.
- Effect: `DELETE` the row → status, interest, tags, rating, and AI Scoop are all gone. Re-adding later starts fresh (subject to §7.3 if a stale client re-sends old fields — timestamps protect the newest intent).

### 7.3 Merge engine (storage-schema "Merge / overwrite policy", PRD §5.5)

`mergeShow(stored, incoming)`:

- **Non-my fields:** `selectFirstNonEmpty(newValue, oldValue)` — never overwrite non-empty strings/arrays with empty ones, never overwrite non-null with null. Catalog refreshes update public data without erasing anything.
- **My fields (tags, score, status, interest, scoop):** per-field timestamp comparison — if both sides have update dates, newer wins; if only one side has a date, that side wins. Preserves user edits across re-adds, refreshes, and multi-device races.
- `details_update_date = now` after merge; `creation_date` immutable.

### 7.4 Display overlay & tile badges (PRD §4.1, §5.9)

`overlayUserData(catalogItems, storedRows)` — used by search results, recommendation strands, AI-mentioned shows, Alchemy/Explore results, and person credits. Emits per-tile flags: `inCollection` (status exists) and `hasRating` (myScore exists). User's version always wins over refreshed public data.

### 7.5 Filters (PRD §4.5, schema `FilterConfiguration`)

`applyFilter(rows, filter, mediaType)` with `filter.type ∈ all | myTag | genre | decade | communityScore | myStatus` (myStatus supported in the model; not surfaced in v1 sidebar). Media-type toggle applies **on top of** any filter. "No tags" is a `myTag` filter with a sentinel value. `last_selected_filter` persists the selection across sessions.

---

## 8. AI Subsystem (`src/server/ai/`)

### 8.1 Provider adapter

```ts
interface AiProvider {
  complete(req: { system: string; messages: Turn[]; maxTokens: number }): Promise<string>;
  completeStructured<T>(req: { system, messages, schema: ZodSchema<T> }): Promise<T>;
  stream(req: { system, messages, maxTokens }): AsyncIterable<string>;
}
```

`AnthropicProvider` implements it with `@anthropic-ai/sdk`: `client.messages.stream()` for Scoop (SSE to the browser), `client.messages.parse()` with `zodOutputFormat` (structured outputs) for Ask-with-mentions and recommendation calls. Model comes from `user_settings.ai_model` (default `claude-opus-4-8`); key precedence: user-entered key (if set) → `AI_API_KEY` env (benchmark mode). Keys never reach the client or the repo.

### 8.2 One persona, per-surface modes (ai_voice_personality.md)

A shared base system prompt encodes the persona: fun, chatty TV/movie nerd; joy-forward and warm; opinionated honesty (acknowledge mixed reception, never gush undeservedly); vibe-first and spoiler-safe by default; specific over generic; brisk by default, lush when earned. Tone sliders: ~70/30 friend/critic, ~60/40 hype/measured, playfulness adaptive to the show. Language patterns: contractions, vivid vibe adjectives ("hopeful absurdity"), quick contrasts ("cozy but sharp"), fit framing ("perfect if you like…"). Hard rules for **every** surface (ai_prompting_context §1): stay within TV/movies and redirect back if pulled away; spoiler-safe unless the user explicitly asks; recommendations must resolve to real catalog items. **Search has no AI voice.**

Surface modes layered on the base prompt:

| Surface | Mode | Length target |
|---|---|---|
| Ask (general) | friend in dialogue, confident favorites, bullets for multi-rec | 1–3 tight paragraphs + list |
| Ask about a show | "showman" — mirrors the show's emotional color, insider context (cancellations, reception) | scannable in one screen |
| Scoop | mini blog post of taste | ~150–350 words |
| Concepts | ingredient generator | bullets only |
| Concept recs | thrilled friend sharing gold | 1–3 sentence reasons |
| Summarizer | same persona, never sterile | 1–2 sentences per summarized span |

### 8.3 Taste-aware context (ai_prompting_context §2)

Prompt builders assemble, per surface: the user's library + My Data (statuses, interests, tags, ratings — compactly serialized, capped), current show context (Ask-about / Scoop / Explore Similar), selected concepts (Explore/Alchemy), and recent turns + rolling summary (chat). The product goal: outputs feel grounded in what the user saves and how they label it.

### 8.4 Ask + mentioned shows (contract from ai_prompting_context §3.2)

- Structured output: `{ commentary: string, showList: string }` where `showList` = `Title::externalId::mediaType;;Title2::externalId::mediaType;;…`. No external IDs inside `commentary`.
- The **parser exactly matches the format** (single shared module + fixture tests): split on `;;`, then `::`; tolerate empty externalId; reject malformed entries individually.
- Resolution (PRD §5.8): if `externalId` present → direct TMDB lookup by id+mediaType, accept when title matches case-insensitively; else title search, accept the **first result whose title matches case-insensitively**. Resolved → selectable real Show (with transient AI "reason"/context); unresolved → non-interactive chip with a "Search for this" handoff.
- **Guardrails (ai_prompting_context §5):** if structured parsing fails, retry **once** with stricter formatting instructions; on second failure, fall back to plain commentary + Search handoff. Same policy for concept/recommendation calls.
- **Conversation summarization:** session keeps full turns client-side (session-only, PRD §5.7); once turns exceed ~10 messages, the server folds the oldest turns into `updatedSummary` (1–2 sentences per span, persona-toned) returned to the client, which sends `summary + recent turns` thereafter.
- **Welcome state:** 6 random starter prompts, refreshable (`/api/ai/starter-prompts`). Content task: author a pool of ~80 on-brand starter prompts per the voice spec (the original 80 live in the missing companion doc).
- **Ask about this show:** entering from Detail seeds the conversation server-side with the handoff show (title, year, overview, the user's My Data) and switches Ask into showman mode. No fake visible user message; the UI shows a small "about *Show*" context chip. (PRD flags exact prefill behavior as TBD — this is our documented resolution.)

### 8.5 Scoop (detail spec §3.4, ai_voice §4.1, quality bar §2.1)

- Structure enforced by prompt: personal take (make a stand) → honest stack-up vs reviews → **"The Scoop" paragraph as the emotional centerpiece** → practical fit/warnings → "Worth it?" gut check. ~150–350 words, spoiler-safe.
- **Streaming:** SSE from `/api/ai/scoop`; UI shows progressive text with a "Generating…" state — never a blank wait.
- **Caching/persistence (PRD §4.9, §5.7):** if the show is in the collection and `ai_scoop_update_date` is < 4h old → return cached scoop (no model call). If stale or absent → generate; **persist only if the show is in the collection** (`ai_scoop` + timestamp on the row); for unsaved shows the scoop lives only in the client session. Generating a scoop does **not** save the show (D9). Toggle copy: "Give me the scoop!" (none) / "Show the scoop" (cached) / open panel titled "The Scoop".

### 8.6 Concepts (concept_system.md)

- Single show (Explore Similar) and multi-show (Alchemy) share one endpoint; multi-show concepts must represent **shared commonality across all inputs**.
- Output contract: bullet list only; each concept 1–3 words; evocative; no explanations, no plot/spoilers. Prompt steers across the taxonomy axes: structure (procedural vs serialized, episodic flow), tone/vibe, emotional palette, relationship dynamics (found family…), craft (writing intelligence, music/cinematography), genre-flavor-not-label.
- Quality constraints enforced by prompt + post-validation: specificity (reject generic outputs like "good characters" via a denylist heuristic and re-ask once), diversity across axes, **ordered by strength** (best "aha" first).
- Counts: single-show returns **8** (quality bar §2.3); multi-show returns a **larger pool (12)** per concept_system §8, selection capped at **8** in the UI for both surfaces (§5).

### 8.7 Concept-based recommendations (concept_system §6, quality bar §2.4)

- Counts: **Explore Similar = 5**, **Alchemy = 6** per round.
- Structured output per rec: title, externalId (when known), mediaType, reason. Reasons must **explicitly name which selected concept(s) they match** and stay 1–3 sentences — taste-aware, not synopses. Recent bias but classics/hidden gems allowed.
- Every rec passes through the resolver (§8.4); results carry the transient reason text (never persisted — PRD §5.7).

### 8.8 AI quality bar (discovery_quality_bar.md)

- The five dimensions (voice adherence, taste alignment, surprise without betrayal, specificity of reasoning, real-show integrity) become a **manual QA checklist** in the repo plus an optional scripted harness (`npm run quality:check`, env-gated, live-key) that runs canned scenarios and prints outputs against the rubric (0–2 per dimension; real-show integrity must be 2 — enforced automatically by asserting every rec resolved).
- Hard automated gates in tests: concept count/length/genericity, rec counts (5/6), showList parseability, resolution integrity.

---

## 9. Frontend Architecture

### 9.1 Fractal screen tree (INSTRUCTIONS.md; adaptation D6)

```
src/screens/
├── Home/
│   ├── Home.tsx                       # humble: layout + bindings
│   ├── hooks/useHomeLogic.ts          # filter state, grouped sections, queries
│   └── features/
│       ├── FiltersSidebar/            # All Shows, tag filters (+ No tags), data filters
│       │   ├── FiltersSidebar.tsx
│       │   ├── hooks/useFilters.ts    # persists lastSelectedFilter
│       │   └── features/ TagFilters/ · DataFilters/ (genre, decade, score buckets)
│       ├── MediaTypeToggle/           # All / Movies / TV — applies on top of filter
│       ├── StatusSections/            # grouping engine
│       │   ├── StatusSections.tsx
│       │   └── features/
│       │       ├── ActiveSection/     # prominent, larger tiles
│       │       ├── ExcitedSection/    # Later + Excited
│       │       ├── InterestedSection/ # Later + Interested
│       │       └── OtherSection/      # collapsed: Wait, Quit, Done, Later w/o interest
│       └── EmptyState/                # no collection → prompt Search/Ask; filter → "No results found."
├── Find/
│   ├── Find.tsx                       # mode switcher: Search | Ask | Alchemy (deep-linkable)
│   └── features/
│       ├── SearchMode/                # SearchBar, ResultsGrid (in-collection marks), auto-focus
│       ├── AskMode/
│       │   ├── AskMode.tsx
│       │   ├── hooks/useAskSession.ts # turns, summary, mentioned shows (session-only)
│       │   └── features/ WelcomePrompts/ (6 random, refresh) · ChatThread/ ·
│       │                 MentionedShowsStrip/ · Composer/
│       └── AlchemyMode/
│           ├── AlchemyMode.tsx
│           ├── hooks/useAlchemySession.ts   # step state; backtracking clears downstream
│           └── features/ ShowPicker/ (library + global search, ≥2)
│                         ConceptCatalysts/ ("Conceptualize Shows", chips, max 8)
│                         AlchemyResults/ ("ALCHEMIZE!", 6 recs w/ reasons)
│                         ChainControl/ ("More Alchemy!" — results feed a new round)
├── ShowDetail/
│   ├── ShowDetail.tsx                 # section order below is load-bearing (detail spec §3)
│   ├── hooks/useShowDetail.ts · useMyDataActions.ts
│   └── features/
│       ├── StatusToolbar/             # chips in toolbar, not scroll body:
│       │                              # Active·Interested·Excited·Done·Quit·Wait;
│       │                              # reselect → removal confirmation flow
│       ├── HeaderMedia/               # backdrops/posters/logos carousel, inline trailers,
│       │                              # graceful poster/logo fallback
│       ├── CoreFacts/                 # year, runtime | seasons/episodes + community score bar
│       ├── MyRating/                  # slider; unrated = null; rating unsaved → auto-save Done
│       ├── MyTags/                    # chips + picker; tagging unsaved → Later+Interested
│       ├── OverviewScoop/             # overview text + Scoop toggle/stream states
│       ├── AskAboutCta/               # "Ask about …" → Find/Ask with handoff show
│       ├── GenresLanguages/
│       ├── RecommendationsStrand/     # traditional similar/recommended (no AI steering)
│       ├── ExploreSimilar/            # Get Concepts → chips (+ 1-line "why concepts
│       │                              #  matter" explainer) → Explore Shows (5 recs)
│       ├── Providers/                 # "Stream It" — availability by region
│       ├── CastCrew/                  # horizontal strands → Person Detail
│       ├── Seasons/                   # TV only
│       └── BudgetRevenue/             # movies, when available
├── PersonDetail/
│   ├── PersonDetail.tsx
│   └── features/ Gallery/ · Bio/ ·
│       AnalyticsCharts/ (features/: RatingsChart, TopGenresChart, ProjectsByYearChart)
│       Filmography/                   # grouped by year; credit → ShowDetail
└── Settings/
    ├── Settings.tsx
    └── features/ Appearance/ (font size XS–XXL) · Behavior/ (search on launch) ·
                  User/ (username) · Ai/ (provider key, model select) ·
                  Integrations/ (catalog key) · YourData/ (Export My Data → zip;
                  Import listed as "coming soon", per D9)
```

Standards applied throughout: main file matches directory name; no `index.tsx`; TSX = markup + binding only, logic in hooks (`const { data, handlers } = useFeatureLogic()`); feature-specific hooks/utils co-located; sub-features used by one parent live under that parent; constants in `src/config/` or local `constants.ts`; all colors/sizes from theme tokens; lint-clean; unit tests adjacent to source.

### 9.2 Detail page experience guarantees (detail spec §2, §4, §5)

- **First 15 seconds:** header media sets mood; year/length + community score + your status/rating visible without hunting; status chips invite an instant save; overview scannable early; Scoop is an affordance for delight, not a requirement.
- **Busyness vs power:** primary actions (status, rating, scoop, concepts) clustered early; long-tail info down-page and full-bleed.
- **Critical states:** unsaved show (auto-save rules live; scoop ephemeral), no trailers/backdrops (premium poster/logo layout), no concepts yet (only "Get Concepts" CTA), TV vs movie (seasons vs runtime/budget handled gracefully).
- **Open TODOs honored:** Alchemy entry stays hidden on Detail; trailers play inline; concepts explainer line included.

### 9.3 Theme & readability

`src/theme/` defines token scales (color, spacing, radius, type). Font-size setting maps XS–XXL to a root `data-font-size` attribute scaling a CSS custom-property type ramp — every component inherits it. No pixel values or hex codes in TSX.

### 9.4 Client data layer

- TanStack Query for all `/api/*` reads; mutations invalidate collection/detail/filters queries so **status/tag/rating changes propagate everywhere a show appears** (PRD §2 "consistent and durable everywhere").
- Optimistic updates for My Data actions (quick, playful — "no modal walls unless destructive").
- Session stores (Zustand): Ask session (turns, summary, mentioned shows), Alchemy session (inputs, concepts, results — cleared on leave; changing shows clears concepts/results; changing concept selection clears results). Nothing AI-transient is persisted (PRD §5.7).
- Identity: a tiny fetch wrapper adds `X-User-Id` in dev/test (value from a dev-only user switcher, default from env-exposed default user).

---

## 10. Key User Journeys → acceptance walkthroughs (PRD §9)

Each ships as a Playwright e2e spec:

1. **Build collection:** Find → Search → open show → set Interested/Excited/Active → tag/rate → appears in Home under the right section.
2. **Rate-to-save:** rating an unsaved show from Detail auto-saves as Done (badge appears, Home "Other" group contains it).
3. **Tag-to-save:** tagging an unsaved show auto-saves Later+Interested; sidebar gains the tag filter.
4. **Maintain:** Home → browse by status → update My Data from Detail → sections re-group.
5. **Tag-driven organization:** tag filter selected → Home shows matching items grouped by status; "No tags" appears only when applicable.
6. **Ask discovery:** starter prompt → recommendation mentioned → strip renders → tap → Detail → save.
7. **Explore Similar:** Get Concepts → select → Explore Shows → 5 recs with concept-citing reasons → save one.
8. **Alchemy:** pick 3 → Conceptualize → select catalysts (≤8) → ALCHEMIZE! → 6 recs → More Alchemy! chains with results as inputs.
9. **Talent deep-dive:** Detail → cast member → Person Detail (charts + filmography) → credit → new Detail.
10. **Backup:** Settings → Export My Data → zip downloads; JSON contains all saved shows + My Data, ISO-8601 dates.

---

## 11. Settings, Export & Modes

- **Settings persistence:** single `user_settings` row; PUT is last-write-wins by `version` (epoch seconds). Username defaults to a generated random name on first touch.
- **AI settings:** model dropdown (curated list of current Claude models, default `claude-opus-4-8`); optional API-key override field (stored server-side, masked in UI, never returned in full, never committed — benchmark mode works with env keys alone).
- **Integrations:** optional catalog (TMDB) key override, same handling.
- **Export:** server builds zip in-memory (`archiver`): `backup.json` `{ formatVersion, exportedAt, settings, shows: [...] }`, dates ISO-8601. First-class per PRD §8.6.
- **Modes:** `APP_MODE=benchmark|production`. Benchmark/dev: identity injection on, `/api/dev/reset` on, verbose errors. Production: injection rejected, dev routes 404 — the documented gating the rider requires.

---

## 12. Testing Strategy

| Layer | Tooling | Coverage |
|---|---|---|
| Domain unit tests (adjacent to source) | Vitest | Save triggers incl. all four trigger paths + defaults + rate→Done exception; removal semantics; merge engine (`selectFirstNonEmpty`, per-field timestamps, creation-date immutability); filter engine incl. "No tags" and media-type layering; timestamp stamping. |
| AI contract tests | Vitest + stub `AiProvider` | showList format parser (round-trip + malformed fixtures); retry-once-then-fallback; concept validation (count, 1–3 words, genericity denylist, multi-show pool size); rec counts 5/6; resolver (id-hit, title-mismatch → search, case-insensitive first match, unresolved → handoff). |
| Repo/integration | Vitest against hosted Supabase | CRUD under a **test namespace** (`$NAMESPACE_ID-test-$RUN`), created and reset by the suite via the same reset path — proves rider §7 (destructive tests, no global teardown) and cross-namespace isolation (write in A, assert invisible in B). |
| API route tests | Vitest + fetch against dev server | Identity resolution (header in dev, rejected in prod mode), scoping of every query, Scoop cache freshness (4h boundary), scoop persist-only-if-saved. |
| E2E | Playwright (catalog/AI mocked at the network edge; optional live mode) | The 10 journeys in §10 + empty states + removal confirmation/"stop asking" flow + search-on-launch. |
| Visual | Playwright snapshots | Home (all sections), Detail (movie + TV), Person, Find modes — per INSTRUCTIONS.md "visual testing highly preferred". |
| AI quality (manual/optional) | `npm run quality:check` | Discovery quality bar rubric outputs for human scoring (§8.8). |

`npm test` runs unit + contract + route suites; `npm run test:integration` and `npm run test:e2e` opt in; `npm run test:reset` clears the namespace (rider §3.2).

---

## 13. Environment & DX Deliverables

`.env.example` (names + comments; runs with zero code edits — rider §3.1):

```
# --- Persistence (Supabase, hosted preferred; local via Docker is OPTIONAL) ---
SUPABASE_URL=
SUPABASE_SERVICE_ROLE_KEY=        # server-only; never exposed to the browser
SUPABASE_ANON_KEY=                # unused by app code today (RLS deny-all); reserved for future client auth
DATABASE_URL=                     # optional: direct Postgres for db:migrate/reset

# --- Isolation & identity (rider §4–5) ---
NAMESPACE_ID=                     # stable per build/run; partitions ALL persisted data
DEFAULT_USER_ID=default-user      # dev/test fallback identity
APP_MODE=benchmark                # benchmark | production (gates X-User-Id & dev routes)

# --- Integrations ---
CATALOG_API_KEY=                  # TMDB API key (server-only)
AI_API_KEY=                       # Anthropic API key (server-only, benchmark mode)
AI_MODEL=claude-opus-4-8          # default model; user-overridable in Settings
```

Scripts: `dev`, `build`, `start`, `lint`, `typecheck`, `test`, `test:integration`, `test:e2e`, `test:reset`, `db:migrate`, `db:seed`, `quality:check`.

README covers: setup in 3 steps (fill env → `npm run db:migrate` → `npm run dev`); identity injection usage and its production gating; namespace semantics + how to run two builds side-by-side; reset semantics; hosted-vs-local Supabase (Docker optional); export format.

---

## 14. Delivery Milestones

Each milestone is independently verifiable; later ones only depend on earlier ones.

**M0 — Skeleton & rails.** Next.js scaffold, theme tokens, config, `.env.example`, `.gitignore`, identity resolver, Supabase repos, migration 0001 + migrate/seed/reset scripts, CI (lint, typecheck, unit). *Exit:* fresh DB deterministic; two namespaces provably isolated; `npm run dev` serves a shell.

**M1 — Domain core.** Merge engine, save triggers/defaults, removal, filters, overlay/badges, data-model version registry — fully unit-tested. `/api/shows*`, `/api/filters`, `/api/settings`. *Exit:* rules pass the PRD §5 matrix.

**M2 — Catalog.** TMDB adapter (search, movie/TV detail incl. transients, person, providers, genre-name mapping, image URL building, best-logo selection, multi-format date parsing), overlay wiring. *Exit:* search + detail payloads correct for movie and TV, keys server-side.

**M3 — Collection UX.** Home (sidebar filters, media toggle, status sections with Active prominence, collapsed Other, empty states), ShowTile badges, Detail non-AI sections in the mandated order + StatusToolbar/rating/tags flows with confirmation policy, Person Detail with charts, Settings (appearance/behavior/user), search-on-launch. *Exit:* journeys 1–5, 9 pass e2e.

**M4 — AI foundation.** Anthropic adapter, persona prompt system, Scoop (streaming + 4h cache + persistence rule), Ask (structured mentions, resolver, summarization after ~10 messages, starter prompts incl. authored pool), guardrail retry/fallback. *Exit:* journey 6 passes; quality-bar automated gates green.

**M5 — Concept discovery.** Concepts endpoint (single + multi), Explore Similar on Detail (5 recs), Alchemy mode (picker ≥2, cap 8 concepts, 6 recs, chaining, backtrack-clears), Ask-about-this-show seeding. *Exit:* journeys 7–8 pass; counts/format contracts enforced.

**M6 — Data ownership & hardening.** Export zip, AI/integration settings (key overrides, model select), data-migration upgrade path demo (v3→v4 fixture), visual snapshots, README polish, production-mode gating audit, rider success-criteria checklist run. *Exit:* journey 10 passes; §15 matrix fully checked.

---

## 15. Requirements Traceability (condensed)

| Requirement (source) | Where satisfied |
|---|---|
| Statuses active/later/wait/done/quit + hidden `next` (PRD §4.2) | DB check constraint §5.1; StatusToolbar (next not surfaced, D9) |
| Interest chips set Later+interest; interest retained off-Later (§4.2–4.3) | §7.1 |
| Save triggers ×4, defaults, rating→Done (§5.2–5.3) | §7.1 |
| Removal clears all My Data + confirmation + stop-asking (§5.4) | §7.2 |
| Re-add merge, per-field timestamps (§5.5–5.6) | §7.3 |
| AI persistence table: scoop 4h persisted-if-saved; Alchemy/Ask/mentions session-only (§5.7) | §8.5, D5, §9.4 |
| AI recs → real shows, id+title case-insensitive resolution, Search handoff (§5.8) | §8.4, §8.7 |
| Tile indicators (§5.9) | §7.4 |
| Sync consistency, per-field conflicts, duplicate merge (§5.10) | §5.4 |
| Data continuity / model version (§5.11) | §5.5 |
| Navigation: sidebar + Find hub + Settings, mode switcher (§6) | §9.1 Find/Home |
| Home grouping incl. Active prominence, collapsed Other, empty states (§7.1) | §9.1 |
| Search: grid, in-collection marks, auto-open on launch (§7.2) | §9.1, §11 |
| Ask: strip, starter prompts 6/refresh, ~10-msg summarization, about-show variant (§7.3) | §8.4 |
| Alchemy flow + backtracking (§7.4) | §9.1 AlchemyMode |
| Detail sections & order, toolbar chips, scoop toggle copy/stream, explore similar, providers, cast/crew, seasons, budget/revenue (§7.5 + detail spec) | §9.1–9.2 |
| Person page (§7.6) | §9.1 |
| Settings + export zip ISO-8601; import deferred (§7.7, §10) | §11, D9 |
| Cross-cutting: user version wins; actionable discovery; taste-aware; spoiler-safe; natural implicit saves; export first-class; user_id scoping; namespace isolation; backend source of truth (§8) | §7.4, §8, D1, D4 |
| Rider: Next.js+Supabase official libs; no Docker; env-only config; secrets hygiene; scripts; migrations; namespace; user_id; dev identity gated; OAuth-ready; disposable cache; namespace-scoped destructive tests | §3, §5, §6, §11, §13, D1–D5 |
| AI contracts: showList format+parser parity; scoop structure; concepts 8/1–3 words/no-generic/ordered/shared-for-multi/larger multi pool; 5/6 rec counts; reasons cite concepts; persona pillars; summarizer tone; retry-once fallback; search voiceless | §8.2–8.8 |
| Storage schema fidelity: fields, transients not stored, ProviderData IDs-only, CloudSettings version, dataModelVersion=3 default, FilterConfiguration shape, merge policy | §5.1, §7.3 |
| INSTRUCTIONS.md: fractal, naming, humble components, hooks, co-location, tokens, lint, adjacent unit tests, visual tests | §9.1, §12, D6, D8 |

---

## 16. Open Questions & Decisions Log

Resolved for v1 (all PRD §10 items — revisit post-benchmark):

1. **Next as first-class status:** no — kept in the data model only.
2. **Named custom lists:** no — tags remain the organizing primitive.
3. **Scoop implicitly saving unsaved shows:** no — scoop stays ephemeral until the user saves.
4. **Explicit Unrated state:** no — cleared rating stores `null` (+ timestamp), UI shows "unrated".
5. **Import/Restore:** deferred; export `formatVersion` + documented schema make it a pure-additive follow-up; Settings shows it as coming soon.
6. **Saving/sharing Alchemy blends:** deferred.
7. **Sidebar myStatus filters:** deferred; filter engine already supports `type: "myStatus"`.

Known risks & mitigations:

- **Structured-output drift from the model** → schema-validated responses, retry-once-with-stricter-instructions, graceful unstructured fallback (spec-mandated), contract tests with recorded fixtures.
- **TMDB shape/ratelimits** → single adapter, short server-side response memoization for hot detail requests (allowed: caching for performance only; correctness never depends on it).
- **Starter-prompt pool & prompt texts lost with companion docs** → authored fresh against `ai_voice_personality.md` do/don't lists and example snippets; reviewed against the quality-bar voice rubric before M4 exit.
- **Persona consistency across surfaces** → one shared base prompt module; per-surface deltas are additive; golden-set harness available when regression protection is wanted (quality bar §3).
