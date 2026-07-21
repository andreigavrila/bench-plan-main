# Implementation Plan — Personal TV & Movie Companion

**Source documents:** `docs/prd/product_prd.md`, `docs/prd/infra_rider_prd.md`, and all of `docs/prd/supporting_docs/` (concept system, AI voice/personality, AI prompting context, detail page experience, discovery quality bar, technical storage schema).

> **Note:** `product_prd.md` §12 references three companion docs (`where_is_the_heart_opus.md`, `ai_personality_opus.md`, `philosophy_opus.md`) that are **not present** in this repo. Behavior they describe is partially captured by the supporting docs that *are* present (voice, prompting context, concepts). Gaps this creates (e.g., the verbatim pool of 80 starter prompts) are flagged in §15.

---

## 1. Product Understanding (What We Are Building)

A personal TV + movie companion for **collecting, organizing, rating, and discovering** entertainment.

- A **Show** (movie or TV) = public/community catalog data + a user overlay ("My Data": status, interest, tags, rating, AI Scoop).
- **The user's version always wins**: wherever a show appears (lists, search, AI outputs), the user-overlaid version is displayed.
- Discovery is **grounded in the user's library**, via four paths: Search (external catalog), Ask (AI chat), Alchemy (multi-show concept blending), Explore Similar (per-show concepts).
- Discovery must be **actionable**: every AI recommendation resolves to a real, selectable catalog show.
- The AI is **one consistent persona** across Scoop/Ask/Alchemy/Explore Similar: a fun, chatty, opinionated, spoiler-safe TV/movie nerd friend. **Search has no AI voice.**

### Cross-cutting principles honored throughout the plan
1. User's version takes precedence everywhere.
2. Every recommendation maps to a real show.
3. AI surfaces are taste-aware (library + My Data + session context).
4. Spoiler-safe by default.
5. Implicit saves/defaults feel natural (never surprising).
6. Export/backup is first-class.
7. Every user-owned record is scoped to a `user_id`.
8. Every build runs in a stable `namespace_id` that partitions all persisted data.
9. Backend (Supabase) is the source of truth; client caches are disposable.

---

## 2. Technology Baseline (from Infrastructure Rider — mandatory)

| Requirement | Decision |
|---|---|
| Runtime | **Next.js (latest stable)**, App Router, TypeScript strict mode. UI + server boundary in one app. |
| Persistence | **Supabase** (hosted preferred) via official client libraries (`@supabase/supabase-js`, `@supabase/ssr`). Docker NOT required; local Supabase optional/documented only. |
| Schema evolution | SQL **migrations** (Supabase migrations) committed to repo; fresh DB state creatable deterministically. Optional seed/fixtures for dev. |
| Env config | `.env.example` with all variables + comments; `.gitignore` excludes `.env*` except `.env.example`. App runs by filling env vars only — no source edits. |
| Keys | Browser/client code uses only the **anon/public key** (if it touches Supabase at all). The **service-role key is server-only** (Route Handlers / Server Actions). No secrets committed. AI/catalog keys via env in benchmark mode. |
| Scripts | `npm run dev` (start), `npm test` (tests), `npm run test:reset` (reset test data for the namespace). |
| Identity | Dev **identity injection**: `X-User-Id` header accepted by server routes in dev/test + a dev-only "login as user" selector + fixed default user per namespace. Documented; gated/disabled in production mode. |
| Isolation | Stable `namespace_id` per build (env var, e.g. `NAMESPACE_ID`); all persisted data partitioned by `(namespace_id, user_id)`; destructive ops scoped to namespace. |
| OAuth migration path | `user_id` is an opaque stable string with no provider meaning; replacing dev injection with OAuth later = config + auth wiring change only, **no schema redesign**. |

---

## 3. High-Level Architecture

```
┌────────────────────────────────────────────────────────────┐
│ Next.js App (App Router)                                   │
│                                                            │
│  Pages (RSC + client components, fractal structure)        │
│    Home / Find(Search|Ask|Alchemy) / Detail / Person / ... │
│        │  calls via fetch / Server Actions                 │
│        ▼                                                   │
│  Server layer (Route Handlers + Server Actions)            │
│    • Identity resolver (dev injection → user_id; prod-gated)│
│    • Namespace resolver (env NAMESPACE_ID)                 │
│    • Domain services (collection rules, filters, merge)    │
│    • AI orchestration (Scoop, Ask, Concepts, Recs)         │
│    • Catalog orchestration (search, details, people)       │
│        │                    │                    │         │
│        ▼                    ▼                    ▼         │
│  Data Access Layer    AI Provider Adapter   Catalog Adapter│
│  (Supabase, service   (env-configured,      (env-configured│
│   role, server-only)   streaming, mockable)  e.g. TMDB-like)│
└────────────────────────────────────────────────────────────┘
```

**Key architectural decisions**

1. **All user-data persistence goes through the Next.js server.** The browser never holds the service-role key; server routes/actions resolve `(namespace_id, user_id)` and scope every query. This satisfies the rider's credential rules, makes dev identity injection trivial to gate, and keeps the backend as the single source of truth (client state is a disposable cache).
2. **Domain logic lives in pure, framework-free modules** (`src/server/domain/`) so business rules (save triggers, defaults, merge policy, filters, parsers) are unit-testable without Next.js or Supabase.
3. **Adapters for externals** (AI provider, content catalog) behind interfaces, so providers can be swapped and tests can mock them. PRD is vendor-agnostic; keys come from env/settings.
4. **Fractal feature structure** per `INSTRUCTIONS.md` (see §4).
5. **Streaming-first AI UX**: Scoop and Ask stream via server-streamed responses so users never stare at a blank state.

---

## 4. Repository Layout (fractal, per INSTRUCTIONS.md)

Naming rule: no `index.tsx`; main file matches directory name (`FeatureName/FeatureName.tsx`).

```
repo-root/
├── .env.example                 # all required vars + comments
├── .gitignore                   # excludes .env* except .env.example
├── package.json                 # scripts: dev, test, test:reset, build, lint
├── next.config.ts
├── supabase/
│   └── migrations/              # deterministic schema (0001_init.sql, ...)
├── scripts/
│   └── reset-test-data.ts       # namespace-scoped destructive reset
├── src/
│   ├── config/                  # env parsing, constants (NO magic numbers elsewhere)
│   ├── theme/                   # design tokens (colors, spacing, font sizes XS–XXL)
│   ├── components/              # shared UI primitives (Tile, Chip, PosterGrid, ...)
│   ├── hooks/                   # global hooks
│   ├── utils/                   # global pure functions (dates ISO-8601, etc.)
│   ├── server/
│   │   ├── identity/            # resolveIdentity(): dev injection, prod-gated
│   │   ├── namespace/           # resolveNamespace(): env-driven, stable per build
│   │   ├── db/                  # Supabase server client (service role), DAL
│   │   ├── domain/              # PURE logic: collectionRules, mergePolicy,
│   │   │                        # filters, statusEngine, mentionParser, exportBuilder
│   │   ├── ai/                  # AiProvider interface + impl, prompts/, parsers/
│   │   └── catalog/             # CatalogProvider interface + impl, mappers/
│   ├── app/                     # Next.js routes
│   │   ├── page.tsx             # Collection Home
│   │   ├── find/                # hub: ?mode=search|ask|alchemy
│   │   ├── show/[id]/           # Show Detail
│   │   ├── person/[id]/         # Person Detail
│   │   ├── settings/
│   │   └── api/                 # route handlers (collection, ai/*, catalog/*, export)
│   └── pages/ → (mirrored as app/ routes; features co-located per fractal rule)
└── tests/                       # unit (adjacent where practical), integration, e2e
```

**Code standards applied everywhere** (from INSTRUCTIONS.md): humble TSX (markup/binding only; logic in `useFeatureLogic()` hooks); no magic numbers/hex/px in TSX (theme tokens + `src/config/`); feature-specific hooks/utils co-located inside the feature directory; lint-clean; unit tests for critical logic adjacent to source; visual tests where protective.

---

## 5. Data Model & Persistence (Supabase/Postgres)

Derived from `technical_docs/storage-schema.ts`, adapted relationally, with the rider's `(namespace_id, user_id)` partition added to every user-owned row. `user_id` is an opaque string (UUID-compatible but not provider-meaningful).

### 5.1 Tables

**`shows`** — one row per saved show per user per namespace.
- Partition/keys: `namespace_id text not null`, `user_id text not null`, `id text not null` (catalog ID), PK `(namespace_id, user_id, id)`.
- Identity/catalog: `title text not null`, `show_type text not null check in ('movie','tv','person','unknown')`, `external_ids jsonb`, `overview text`, `genres text[] default '{}'`, `tagline text`, `homepage text`, `original_language text`, `spoken_languages text[] default '{}'`, `languages text[] default '{}'`.
- Images: `poster_url text`, `backdrop_url text`, `logo_url text`, `network_logos text[] default '{}'` (reserved).
- Ratings/popularity: `vote_average double`, `vote_count int`, `popularity double`.
- Dates: `last_air_date timestamptz`, `first_air_date timestamptz`, `release_date timestamptz`.
- Movie: `runtime int`, `budget bigint`, `revenue bigint`.
- TV: `series_status text`, `number_of_episodes int`, `number_of_seasons int`, `episode_run_time int[] default '{}'`, `last_episode_run_time int` (reserved).
- **My Data**: `my_tags text[] default '{}'`, `my_tags_update_date timestamptz`, `my_score double`, `my_score_update_date timestamptz`, `my_status text check in ('active','next','later','done','quit','wait')`, `my_status_update_date timestamptz`, `my_interest text check in ('excited','interested')`, `my_interest_update_date timestamptz`.
- AI: `ai_scoop text`, `ai_scoop_update_date timestamptz`.
- Management: `details_update_date timestamptz`, `creation_date timestamptz default now()`, `is_test boolean default false` (supports destructive testing hygiene).
- Providers: `provider_data jsonb` (opaque blob; country → `{flatrate?, rent?, buy?}` provider **IDs only**).
- Index: `(namespace_id, user_id, my_status)` for Home sections; GIN on `my_tags` for tag filters.

**`cloud_settings`** — synced app/user settings. PK `(namespace_id, user_id)`; `id text default 'globalSettings'`; `user_name text` (random name on first launch); `version double` (epoch seconds, for conflict resolution); `catalog_api_key text`, `ai_api_key text`, `ai_model text`.

**`app_metadata`** — per-namespace model versioning for data continuity: PK `(namespace_id)`; `data_model_version int default 3`. Drives transparent migrations of user data across app updates (PRD §5.11 — users never lose My Data on upgrade).

**Transient data is NOT persisted** (fetched per-view from catalog, re-pullable): cast, crew, seasons, images galleries, videos, recommendations, similar, lastEpisodeToAir, aiDescription, tile UI state. Ask chat history, Alchemy results/reasons, and the mentioned-shows strip are **session-only** (client memory), never written to DB.

**Local-only preferences** (device-level, non-synced; safe to lose): `autoSearch`, `fontSize` (XS|S|M|L|XL|XXL), `hideStatusRemovalConfirmation`, `statusRemovalCountKey`, `lastSelectedFilter` (`{type: all|genre|myStatus|communityScore|decade|myTag, label, value}` as JSON). Stored in client storage; clearing it must not lose user-owned data (which lives server-side).

### 5.2 Access control & isolation
- All DAL queries filter by `(namespace_id, user_id)` resolved server-side — enforced in one place (`db/forUser(ctx)` helper) so no query can cross namespaces/users.
- Row Level Security enabled with policies keyed to the injected identity claim as defense-in-depth; destructive operations (test reset) accept `namespace_id` and delete only matching rows.
- `test:reset` script: deletes `shows`/`cloud_settings` where `namespace_id = current` (optionally only `is_test = true`), never global teardown.

### 5.3 Migrations & data continuity
- `supabase/migrations/0001_init.sql` creates the above; later changes are additive migrations.
- App boot checks `app_metadata.data_model_version` and runs safe, transparent upgrade transforms for persisted user data if behind (PRD §5.11).

---

## 6. Identity, Namespace & Auth Policy

- **Namespace**: `NAMESPACE_ID` env var, required, stable for the build's lifetime. Server middleware stamps it into a per-request context object; DAL requires it.
- **User**: `resolveIdentity()` in server layer:
  - Dev/test mode: accept `X-User-Id` header; else a dev-only "login as user" selector cookie; else fixed default user (`default-user`) for the namespace.
  - Production mode: injection disabled/gated (`NODE_ENV` + explicit flag); ready to swap in OAuth (Supabase Auth later) by mapping provider subject → opaque `user_id`. **No schema change needed** — `user_id` is already opaque and provider-agnostic.
- Effective partition everywhere: **`(namespace_id, user_id)`**.
- Documented in README/`AGENTS.md`-style docs: how identity works, that it's dev-only, and the OAuth migration path.

---

## 7. Core Domain Logic (pure modules, heavily unit-tested)

These modules encode PRD §5 business rules exactly.

### 7.1 Collection membership & save triggers (`domain/collectionRules.ts`)
- "In collection" ⇔ stored show with non-null `my_status`.
- **Saving triggers** (any one saves an unsaved show): setting a status; choosing an interest chip (Interested/Excited); rating an unsaved show; adding ≥1 tag to an unsaved show.
- **Defaults on save without explicit status**: `my_status = later`, `my_interest = interested`. **Exception**: first save via rating ⇒ `my_status = done` (rating implies watched).
- **Status chip mapping**: Interested/Excited chips set `my_status=later` + `my_interest=interested|excited`. If status leaves `later`, interest is retained but irrelevant until return.
- Every My-Data mutation stamps its own timestamp (`my_status_update_date`, etc.).

### 7.2 Removal (`domain/collectionRules.ts`)
- Reselecting the active status ⇒ confirmation dialog (suppressed when `hideStatusRemovalConfirmation` is true; `statusRemovalCountKey` tracks shows of the warning and offers "stop asking").
- On confirm: **delete the row** — status, interest, tags, rating, and AI Scoop all cleared (row removal clears everything by construction).

### 7.3 Merge policy (`domain/mergePolicy.ts`) — catalog refresh & re-add
- `selectFirstNonEmpty(new, old)` for **non-my** fields: never overwrite a non-empty stored string/array with empty; never overwrite non-null with null.
- **My fields** resolve per field by timestamp: both sides dated ⇒ keep newer; only one dated ⇒ keep that side.
- After merge: `details_update_date = now`; `creation_date` only on first creation.
- Re-adding an already-saved show preserves all My Data and refreshes public metadata via this policy. Duplicate items (same catalog id) merge transparently.

### 7.4 Sync semantics (`domain/mergePolicy.ts` + settings)
- Cross-device consistency is inherent (server is source of truth). Concurrent edits merge per field, newest-update-wins, using the per-field timestamps. `cloud_settings.version` (epoch seconds) resolves settings conflicts.

### 7.5 Filters (`domain/filters.ts`)
- Filter types: `all`, `myTag` (one per tag + synthetic **"No tags"** filter iff tagless shows exist), `genre`, `decade`, `communityScore` ranges, `myStatus` (model supports; UI exposure optional per open questions).
- **Media-type toggle** (All / Movies / TV) composes on top of any filter.
- Pure function `applyFilter(shows, filter, mediaType)` — unit-tested.

### 7.6 Mentioned-shows parser (`domain/mentionParser.ts`)
- Parses AI structured output exactly: `commentary` + `showList` where `showList = "Title::externalId::mediaType;;Title2::externalId::mediaType;;..."`. Parser and prompt format must match exactly (contract test).

### 7.7 Recommendation resolution (`server/ai/resolveRecs.ts`)
- Input: title + externalId (if any) + mediaType.
- Look up catalog by externalId if provided; accept the **first result whose title matches case-insensitively**; else attempt title search.
- Resolved ⇒ real selectable Show (may carry transient AI "reason" text). Unresolved ⇒ render non-interactive or hand off to Search (pre-filled query).

### 7.8 Export builder (`domain/exportBuilder.ts`)
- Produces a `.zip` containing a JSON backup of all saved shows + My Data for `(namespace_id, user_id)`, dates encoded **ISO-8601**. (Import/Restore is an explicit open question — out of scope for v1.)

---

## 8. External Catalog Integration (`server/catalog/`)

- `CatalogProvider` interface: `search(query)`, `getShow(id, type)`, `getPerson(id)`, `getPersonCredits(id)`, `getImages/videos/recommendations/similar(id)`, `getProviders(id)`, `getGenres()`.
- Reference implementation against a TMDB-style API; key from env (`CATALOG_API_KEY`) or `cloud_settings.catalog_api_key` (env wins in benchmark mode).
- **Mapping** (per storage-schema §"External catalog → Show mapping"): catalog id → `Show.id`; title (movie) / name (TV), reject if neither; media type inference (`name` ⇒ tv, `title` ⇒ movie, else reject unknown); genre IDs → display **names** stored as strings; multi-format date parsing; images mapped to full URLs with deterministic best-logo selection (prefer English, best-rated); provider availability stored as ID lists by region.
- Catalog detail responses merge into stored shows via `mergePolicy` (§7.3) before persisting; transient sections (credits, seasons, videos, recs, similar) attach to the response only.
- Catalog is also the source for Alchemy/Explore input shows beyond the library ("library + global catalog").

---

## 9. AI Integration Layer (`server/ai/`)

### 9.1 Provider adapter
- `AiProvider` interface: `streamChat(messages, options)`, `generateStructured(schemaHint, messages)`. Provider-agnostic (env `AI_API_KEY`, `AI_MODEL`; fallback to `cloud_settings`). Mock implementation for tests/dev without keys.
- Taste-aware context builder: injects the user's library snapshot (titles + status/interest/tags/rating) into prompts for Ask/Alchemy/Explore Similar, per "taste-aware AI" rule.

### 9.2 Surface contracts (prompts co-located in `server/ai/prompts/`)

All surfaces: TV/movie domain only (redirect otherwise); spoiler-safe unless asked; opinionated/honest (acknowledge mixed reception); specific vibe/structure/craft reasoning over genre boilerplate; one shared persona (joy-forward, warm, 70/30 friend-critic, concise by default). **Search gets no AI voice.**

1. **Scoop** (`/api/ai/scoop`): mini blog-post of taste — personal take, honest stack-up vs reviews, "The Scoop" centerpiece paragraph, fit/warnings, "Worth it?" verdict; ~150–350 words; **streams progressively**. Freshness: regenerate on demand if `ai_scoop_update_date` older than **4 hours**; **persist only if the show is in the collection** (unsaved ⇒ ephemeral response).
2. **Ask** (`/api/ai/ask`): conversational, 1–3 tight paragraphs + bullets when recommending; confident picks. Structured variant returns `{commentary, showList}` in the exact `::`/`;;` format; commentary contains no external IDs. On parse failure: **retry once with stricter formatting instructions**, else fall back to unstructured commentary + Search handoff.
3. **Concepts** (`/api/ai/concepts`): bullet list only; **1–3 words** each; evocative, ingredient-like, spoiler-free; no generic concepts ("good characters" invalid, "hopeful absurdity" valid); ordered by strength; diverse across axes (structure/vibe/emotion/dynamics/craft). **8 concepts by default**; multi-show (Alchemy) requires concepts **shared across all inputs** and a larger pool than single-show.
4. **Concept recommendations** (`/api/ai/concept-recs`): **5 recs for Explore Similar, 6 for Alchemy**; each with a 1–3 sentence reason that **explicitly names which selected concept(s)** it matches; recent bias but classics/hidden gems allowed; must return title + externalId + mediaType for resolution (§7.7).
5. **Conversation summarization**: after ~10 messages, older turns summarized into 1–2 sentences **in the same persona tone** (no sterile system-summary voice) to control token depth while preserving feel.

### 9.3 Session state
Ask history, Alchemy rounds/results, mentioned-shows strips: client-side session state only (cleared on leaving/resetting), per PRD §5.7. Nothing AI-generated persists except Scoop-on-saved-shows.

### 9.4 Quality bar
Implement `docs/.../discovery_quality_bar.md` as the acceptance rubric: 5 dimensions scored 0–2 (voice, taste alignment, surprise-without-betrayal, specificity, real-show integrity); pass = voice ≥1, taste ≥1, **real-show integrity = 2 (non-negotiable)**, total ≥7/10. Golden set optional in v1; hooks left to add one.

---

## 10. Feature Plans (UI)

App shell: persistent **filters/navigation panel** (All Shows, tag filters, data filters) + main content area; persistent **Find/Discover** and **Settings** entries in primary nav. Find hub has a clear **mode switcher** (Search | Ask | Alchemy). Show tiles everywhere display **badges**: in-collection indicator (status exists) and user-rating indicator.

### 10.1 Collection Home (`app/page.tsx` + features)
- Displays shows for the selected filter + media-type toggle (All/Movies/TV) at top.
- **Status sections in order**: 1) **Active** (prominent, larger tiles), 2) **Excited** (later+excited), 3) **Interested** (later+interested), 4) **Other** (collapsed: wait, quit, done, unclassified later-without-interest).
- Tiles: poster, title, My-Data badges.
- Empty states: no shows ⇒ prompt to Search/Ask; filter yields none ⇒ "No results found."
- Sorting: recently updated first where applicable (per-field timestamps).
- Hook: `useCollection(filter, mediaType)`; server action streams sections.

### 10.2 Search (`app/find/` mode=search)
- Text search by title/keywords against the catalog (live queries; no caching required).
- Poster grid results; **in-collection items marked**; selecting opens Show Detail.
- Honors "Search on Launch" setting (auto-opens Find→Search on app launch).
- Straightforward catalog UX — no AI voice on this surface.

### 10.3 Ask (`app/find/` mode=ask)
- Chat UI with user/assistant turns, streaming responses.
- **Welcome view**: 6 random starter prompts with refresh (pool authored per voice spec — see §15 assumption about the missing 80-prompt doc).
- **Mentioned shows**: structured `showList` parsed (§7.6), resolved to real shows (§7.7), rendered as a horizontal strip; tapping opens Detail (or Search handoff if unresolved).
- Session context retained; **summarization after ~10 messages** (§9.2.5); cleared on reset/leave.
- **Ask About a Show variant**: launched from Detail; enters Ask mode with the handoff show seeded as context (prefill copy TBD — flagged open question).

### 10.4 Alchemy (`app/find/` mode=alchemy)
- Step-clear flow (cards/sections): 1) select **≥2 shows** (library + global catalog search), 2) **Conceptualize Shows**, 3) select **1–8 concept catalysts**, 4) **ALCHEMIZE!**, 5) 6 recommendations with reasons; **More Alchemy!** chains a round using results as new inputs.
- **Backtracking rules**: changing input shows clears concepts + results; selecting/unselecting concepts clears results.
- Guidance copy: "pick the ingredients you want more of"; empty state nudges to select ≥1 concept.
- Session-only; cleared when leaving Alchemy.

### 10.5 Show Detail (`app/show/[id]/`)
Narrative order preserved exactly (per detail-page spec):
1. **Header media carousel** (backdrops/posters/logos; trailers inline when available, never blocking; graceful poster fallback).
2. **Core facts row** (year, runtime or seasons/episodes) + **community score** bar.
3. **My Tags** chips + tag picker (adding a tag to an unsaved show auto-saves as later+interested).
4. **Overview + Scoop toggle/stream**: copy states "Give me the scoop!" → "Show the scoop" (cached) → "The Scoop" (open); streams with "Generating…" state; 4-hour freshness; persists only if saved.
5. **"Ask about this show"** CTA (seeds Ask with show context).
6. **Genres + languages**.
7. **Traditional recommendations strand** (catalog similar/recommended).
8. **Explore Similar**: Get Concepts → select 1+ chips → Explore Shows (5 AI recs with concept-citing reasons); unresolved recs non-interactive/Search handoff.
9. **Streaming availability** ("Stream It") from `provider_data` + provider metadata fetch.
10. **Cast & Crew** horizontal strands → Person Detail.
11. **Seasons** (TV only).
12. **Budget vs Revenue** (movies when available).
- **Toolbar status/interest chips** (Active / Interested / Excited / Done / Quit / Wait): set to save; reselect active status ⇒ removal confirmation (with stop-asking option) ⇒ delete + clear My Data.
- **My Rating slider**: rating an unsaved show auto-saves as **done**; unrated state handled (explicit Unrated vs nil is an open question — v1 uses nil).
- Critical states handled: unsaved show, no trailers/backdrops (premium poster layout), no concepts yet (only Get Concepts CTA), TV vs movie differences.

### 10.6 Person Detail (`app/person/[id]/`)
- Image gallery, name, bio.
- **Analytics charts**: average project ratings, top genres, projects-by-year (computed from credits; chart lib in theme tokens).
- **Filmography grouped by year**; selecting a credit opens that Show Detail.

### 10.7 Settings & Your Data (`app/settings/`)
- App: font size (XS–XXL, theme token scale), Search on Launch toggle.
- User: username (random on first launch; synced).
- AI: provider API key (benchmark: env-provided; user-entered storage optional, never committed), model selection (synced).
- Integrations: catalog provider API key (synced).
- **Your data**: "Export My Data" ⇒ downloads `.zip` (JSON backup, ISO-8601 dates). Import/Restore listed as desired-but-unimplemented (open question).

---

## 11. Cross-Cutting Concerns

- **User overlay everywhere**: any show render path (Home tiles, Search results, AI strips, recs, Person credits) joins stored My Data for `(namespace_id, user_id)` and displays badges/overlay; user edits always win over refreshed public data.
- **Spoiler safety** default in all AI surfaces; explicit user ask required to lift.
- **Theme**: font-size scale and colors via tokens only; no inline styles/hex/px in TSX.
- **Config**: all constants (4-hour Scoop TTL, 8-concept cap, 5/6 rec counts, ~10-message summarization threshold, status/interest enums, filter defs) in `src/config/`.
- **Error handling**: network failure messaging (no offline mode required); AI/catalog failures degrade gracefully (Search handoff).
- **Performance**: catalog detail fetches parallelized; images lazy; streaming for AI.

---

## 12. Testing Strategy

- **Unit (critical logic, adjacent to source)**: collection rules (all save triggers/defaults/removal), merge policy (selectFirstNonEmpty, per-field timestamps), filters (+ "No tags", media-type composition), mention parser (exact format contract), export builder (ISO-8601), concept/rec validators (counts, 1–3 words), rec resolution (case-insensitive first match).
- **Integration**: DAL against hosted Supabase in the build's namespace; verify `(namespace_id, user_id)` isolation (two namespaces can't see each other); RLS spot checks.
- **Destructive tests**: create/reset test data **within the namespace only** via `npm run test:reset`; no global teardown; `is_test` rows for synthetic fixtures.
- **AI contract tests**: mocked provider asserting prompt contracts (structured format, counts, persona guardrails) and parser fallback path (retry-once then Search handoff).
- **E2E/visual** (preferred where protective): Playwright screenshots for Home sections, Detail hierarchy, Alchemy flow; key journeys from PRD §9 (rate-to-save ⇒ Done; tag-to-save ⇒ Later+Interested; removal confirmation; export zip).
- **Scripts**: `npm test` (unit+integration), `npm run test:reset`, `npm run dev`, `npm run lint`.
- **Quality bar**: manual rubric checklist (§9.4) run before milestone sign-off; golden-set harness stubbed.

---

## 13. Implementation Phases

1. **Scaffold**: Next.js + TS + lint + theme/config skeleton; `.env.example`, `.gitignore`; Supabase client + migrations; identity/namespace plumbing; scripts (`dev`, `test`, `test:reset`).
2. **Data core**: DAL, domain modules (collection rules, merge, filters) with unit tests.
3. **Catalog adapter**: search/details/people/credits/providers + mapping/merge.
4. **Collection Home + filters + tiles/badges**; status sections; empty states.
5. **Show Detail (non-AI sections)**: header, facts, toolbar status chips, rating slider, tags, overview, recs strand, providers, cast/crew, seasons, budget/revenue; save/remove rules wired.
6. **Search** + search-on-launch; in-collection markers.
7. **Person Detail** + analytics charts + filmography.
8. **AI layer**: provider adapter + Scoop (streaming, 4h TTL, persist-if-saved).
9. **Ask**: chat, structured mentions + strip, summarization, starter prompts, Ask-about-show handoff.
10. **Explore Similar** (concepts → recs) on Detail.
11. **Alchemy** (full flow + chaining + backtracking).
12. **Settings + Export zip**; cloud settings sync via `version`.
13. **Hardening**: data-continuity migration check, destructive-test pass, quality-bar validation, visual tests, docs (identity model, OAuth path, env setup).

---

## 14. Repo Deliverables Checklist (Rider §9 success criteria)

- [x] `.env.example` (Supabase URL + anon key + service-role key, `NAMESPACE_ID`, `AI_API_KEY`, `AI_MODEL`, `CATALOG_API_KEY`, dev-identity flag) — runs without code edits.
- [x] Namespace isolation (`NAMESPACE_ID` partitions all rows; reset scoped).
- [x] All user-owned records carry `user_id`.
- [x] Destructive test runs without global teardown (`test:reset`).
- [x] OAuth adoptable later without schema redesign (opaque `user_id`, gated injection).
- [x] No Docker requirement; hosted Supabase path primary.
- [x] Migrations for deterministic fresh DB.

---

## 15. Assumptions, Risks & Open Questions

**Assumptions**
- The three companion docs referenced in PRD §12 are absent; the verbatim **80 starter prompts** are unavailable → we will author a prompt pool consistent with the voice spec (welcome view still shows 6 random + refresh). Flagged, not blocking.
- A TMDB-style catalog is the reference external provider; adapter keeps it swappable. Genre ID→name mapping and best-logo rule are implementation-defined per storage schema.
- Benchmark identity: single default user per namespace unless the dev selector/header overrides.

**Open questions carried from PRD §10 (v1 defaults chosen, change-friendly)**
- `next` status stays in the data model, not surfaced as first-class UI.
- No named custom lists beyond tags in v1.
- Generating Scoop on an unsaved show does **not** implicitly save it.
- Clearing My Rating stores nil (no explicit Unrated) in v1.
- Import/Restore not implemented in v1 (export format designed to be restorable).
- Alchemy sessions not savable/sharable in v1.
- `myStatus` sidebar filters supported by the model; UI exposure optional.
- "Ask about this show" exact prefill behavior TBD; v1 hands off the show as seeded context.

**Risks & mitigations**
- *AI hallucinated titles/IDs* → strict structured output, resolution rule (§7.7), retry-once-then-handoff fallback, real-show-integrity = 2 gate.
- *Structured format drift* → single parser shared by contract tests; prompt and parser versioned together.
- *Merge regressions losing user data* → merge policy is pure + exhaustively unit-tested; per-field timestamps on every mutation.
- *Namespace leakage* → single DAL entry point enforcing `(namespace_id, user_id)`; isolation integration tests.
- *Key leakage* → service-role/AI keys server-only; `.env*` ignored except `.env.example`.
