# Implementation Plan — Personal TV + Movie Companion

This plan covers the full scope defined in `docs/prd/product_prd.md`, the infrastructure rider (`docs/prd/infra_rider_prd.md`), and all supporting docs (AI prompting contracts, voice/personality spec, concept system, detail page experience, discovery quality bar, and the storage schema reference).

---

## 1. Scope Summary (What We're Building)

A personal TV/movie companion where users build a library of shows with a personal overlay ("My Data": status, interest, tags, rating, AI Scoop), and use that taste profile to power four discovery paths:

1. **Search** — plain external-catalog search (no AI voice).
2. **Ask** — conversational AI discovery with structured "mentioned shows."
3. **Alchemy** — blend 2+ shows → shared concepts → 6 grounded recommendations, chainable.
4. **Explore Similar** — per-show concepts → 5 grounded recommendations (on Detail page).

Plus: Show Detail (the single source of truth per show), Person Detail with analytics, filterable Collection Home, Settings, and Export/Backup.

**Benchmark baseline (mandated):** Next.js (latest stable) + Supabase (hosted preferred, Docker never required). All persisted user data is server-side, partitioned by `(namespace_id, user_id)`, with dev identity injection and no real OAuth required — but schema-ready for OAuth later.

---

## 2. Architecture Overview

### 2.1 Stack

| Layer | Choice | Rationale |
|---|---|---|
| App runtime | Next.js (App Router, latest stable) | Mandated by rider; server boundary for secrets |
| Persistence | Supabase (Postgres) via `@supabase/supabase-js` | Mandated by rider |
| External catalog | TMDB-compatible provider behind a `CatalogProvider` interface | PRD is provider-agnostic; TMDB shapes match the schema (posters/backdrops/logos, providers-by-region, credits, seasons, budget/revenue) |
| AI | Anthropic API behind an `AIProvider` interface; model selectable in Settings | PRD requires configurable provider key + model |
| Client state | React Query (server cache) + lightweight UI store | Cache is disposable per rider §6.2 |
| Styling | Tailwind CSS | Fast, consistent with "clean, playful" UI tone |
| Validation | Zod schemas shared between API routes and client | Enforces structured AI output contracts |
| Tests | Vitest (unit) + Playwright (e2e) | One-command test experience |

### 2.2 Trust boundary

- **Browser** talks only to Next.js API routes (Route Handlers). It never holds the AI key, the catalog key, or the Supabase service-role key.
- **Server routes** hold: Supabase service-role key (or anon key + RLS — see §4.4), catalog API key, AI API key.
- Supabase browser access is not needed at all in v1: all reads/writes go through our API routes. This keeps the namespace/user partitioning enforceable in one place and makes the "backend is source of truth" rule trivial to satisfy.

### 2.3 Module layout

```
src/
  app/                      # Next.js App Router
    (app)/                  # main shell: sidebar + content
      page.tsx              # Home (filtered library)
      show/[id]/page.tsx    # Show Detail
      person/[id]/page.tsx  # Person Detail
      find/page.tsx         # Find hub (Search / Ask / Alchemy modes)
      settings/page.tsx
    api/
      shows/                # collection CRUD + merge
      catalog/              # search, details, credits, providers, person
      ai/                   # scoop, ask, concepts, recommendations
      export/               # zip export
      admin/                # namespace reset (dev/test-gated)
  lib/
    db/                     # supabase client, queries, merge rules
    catalog/                # CatalogProvider interface + TMDB impl + mapping
    ai/                     # AIProvider interface, prompts, parsers, persona
    identity/               # namespace + user resolution
    domain/                 # Show model, statuses, save/remove rules, filters
  components/               # tiles, chips, strands, chat UI, concept chips...
supabase/
  migrations/               # SQL migrations (repeatable schema)
  seed/                     # optional fixtures
```

---

## 3. Data Model (Supabase / Postgres)

Derived from `storage-schema.ts` / `storage-schema.md`, adapted to relational + rider requirements. Every user-owned table carries `namespace_id text NOT NULL` and `user_id text NOT NULL` (opaque strings).

### 3.1 Tables

**`shows`** — one row per (namespace, user, show). The "user's version" of a catalog item.
- PK: `(namespace_id, user_id, id)` where `id` = catalog ID string (e.g. `tmdb:movie:603`, media-type-qualified to avoid movie/TV ID collisions).
- Catalog columns: `title`, `show_type` (`movie|tv|person|unknown`), `external_ids jsonb`, `overview`, `genres text[]`, `tagline`, `homepage`, `original_language`, `spoken_languages text[]`, `languages text[]`, `poster_url`, `backdrop_url`, `logo_url`, `network_logos text[]`, `vote_average`, `vote_count`, `popularity`, `first_air_date`, `last_air_date`, `release_date`, `runtime`, `budget`, `revenue`, `series_status`, `number_of_episodes`, `number_of_seasons`, `episode_run_time int[]`, `provider_data jsonb`.
- My Data columns (each with its own timestamp per PRD §5.6): `my_status` (enum incl. hidden `next`), `my_status_update_date`, `my_interest` (`excited|interested`), `my_interest_update_date`, `my_tags text[]`, `my_tags_update_date`, `my_score`, `my_score_update_date`.
- AI: `ai_scoop`, `ai_scoop_update_date`.
- Management: `details_update_date`, `creation_date`, `is_test boolean default false`.
- Invariant: a row exists **iff** the show is in collection (`my_status IS NOT NULL`) — removal deletes the row (PRD §5.4). Transient data (cast, seasons, videos, recommendations, images) is **never stored**; re-fetched from catalog.

**`user_settings`** — per (namespace, user): `user_name` (random on first creation), `ai_model`, optional `catalog_api_key`, `ai_api_key` (encrypted at rest via pgcrypto or left null in benchmark mode where env vars supply keys), `version` (epoch seconds for conflict resolution), local-ish synced prefs if desired.
**`app_metadata`** — per namespace: `data_model_version int default 3` (continuity across model versions, PRD §5.11).
**Client-only key-value state** (`autoSearch`, `fontSize`, `hideStatusRemovalConfirmation`, `statusRemovalCount`, `lastSelectedFilter`) lives in `localStorage` — explicitly disposable UI state, safe to lose per rider §6.2.

### 3.2 Merge rules (server-side, `lib/db/merge.ts`)

Implements storage-schema merge policy exactly:
- **Non-my fields:** `selectFirstNonEmpty(new, old)` — never overwrite non-empty with empty/nil.
- **My fields:** newer `*_update_date` wins; a side without a timestamp loses to a side with one.
- `details_update_date` set to now after any catalog merge; `creation_date` set once.
- Duplicate detection on upsert (same PK) merges transparently (PRD §5.10).

### 3.3 Migrations & seed

- `supabase/migrations/*.sql` applied via Supabase CLI (`supabase db push`) or a small `npm run db:migrate` script using the connection string — works against hosted instance, no Docker.
- Seed script creates the default user + optional fixture shows flagged `is_test = true`.

---

## 4. Identity, Namespace & Isolation (Rider Compliance)

### 4.1 Namespace

- `NAMESPACE_ID` env var, required. Generated once per build/run (documented in README: `openssl rand -hex 8` or similar). Every query filters by it; every insert stamps it.
- No cross-namespace reads/writes are possible because all DB access flows through `lib/db/` helpers that require a `Scope { namespaceId, userId }` argument — there is no raw-table escape hatch in app code.

### 4.2 User identity

- `DEFAULT_USER_ID` env var seeds the default user.
- Dev identity injection: server routes accept `X-User-Id` header **only when** `IDENTITY_MODE=dev` (default in benchmark). In `IDENTITY_MODE=production`, the header is rejected and a real session (future OAuth) is required — wiring point isolated in `lib/identity/resolveUser.ts` so swapping in OAuth changes one module, not the schema (rider §5.2).
- Optional dev-only user selector in Settings (visible only in dev mode).

### 4.3 Destructive testing

- `POST /api/admin/reset` (gated to dev/test mode) deletes all rows for the current namespace (optionally only `is_test = true` rows). Exposed as `npm run test:reset`. No global teardown ever.

### 4.4 RLS decision

Since browser never talks to Supabase directly, use the service-role key server-side only and enforce scoping in the query layer. Still enable RLS with a deny-all policy on all tables as defense-in-depth (anon key grants nothing). This satisfies "anon key in client / elevated key server-only" trivially — the client has no Supabase key at all.

---

## 5. External Catalog Integration

`lib/catalog/CatalogProvider` interface with a TMDB implementation:

- `search(query, mediaType?)` → tiles.
- `getDetails(id, mediaType)` → full show incl. transient credits, videos, images, seasons, similar/recommended, watch providers (append-to-response for efficiency).
- `getPerson(id)` → bio, images, combined credits.
- `resolveByExternalId(externalId, mediaType)` + `resolveByTitle(title, mediaType)` → for AI recommendation grounding (PRD §5.8: try external ID first, accept first case-insensitive title match).

Mapping layer implements storage-schema rules: genre IDs → names, image paths → full URLs, best-logo selection (highest-rated, prefer English — deterministic), multi-format date parsing, media-type inference (`name`→tv, `title`→movie, else reject), provider data reduced to IDs-by-region.

**Overlay rule (PRD §4.1):** every list-returning API route runs results through `applyUserOverlay(scope, shows)`: batch-fetch saved rows for the returned IDs and merge My Data on top, so the user's version wins everywhere (search, recs, AI mentions, filmography).

---

## 6. Domain Rules Engine

Centralized in `lib/domain/collection.ts` so every surface behaves identically:

- **Save triggers** (PRD §5.2): set status / pick interest chip / rate unsaved / tag unsaved → upsert row.
- **Defaults** (§5.3): implicit save → `later + interested`; save-via-rating → `done`.
- **Interest chips**: "Interested"/"Excited" set `status=later` + corresponding interest; interest retained when status moves off Later (may resurface if it returns).
- **Removal** (§5.4): clearing status deletes row + all My Data (scoop included). Client shows confirmation dialog with "stop asking" option (localStorage-backed count + suppression flag per storage schema).
- **Timestamps**: every My-field mutation stamps its own `*_update_date` server-side.
- **Scoop persistence** (§4.9/§5.7): scoop saved only when the show is in collection; otherwise returned to the client transient-only, 4-hour freshness check on `ai_scoop_update_date`.

API routes (all namespace/user scoped):
- `GET /api/shows` (with filter params), `PUT /api/shows/:id/status|interest|rating|tags`, `DELETE /api/shows/:id` (remove-from-collection), `POST /api/shows/:id/refresh` (catalog merge).
- `GET /api/filters` → available tag/genre/decade/score filters derived from collection.

---

## 7. AI Layer

### 7.1 Provider abstraction

`lib/ai/AIProvider` with an Anthropic implementation. Model name from user settings (fallback env default). API key from env in benchmark mode; user-entered key in settings is optional and never committed.

### 7.2 One persona, five surfaces

A shared base persona module (`lib/ai/persona.ts`) encodes the voice pillars from `ai_voice_personality.md`: joy-forward, opinionated honesty, vibe-first spoiler-safe, specific not generic, concise by default; 70/30 friend-critic, 60/40 hype-measured; TV/movie domain lock. Each surface composes base persona + surface mode:

| Surface | Endpoint | Contract |
|---|---|---|
| **Scoop** | `POST /api/ai/scoop` | Streams (SSE) a ~150–350-word structured mini blog post: personal take, honest stack-up, "The Scoop" centerpiece, fit/warnings, "Worth it?" verdict. Persist only if in collection; 4h cache. |
| **Ask** | `POST /api/ai/ask` | Structured output: `{ commentary, showList }` with `showList` in exact `Title::externalId::mediaType;;...` format. Parser matches format exactly; commentary contains no IDs. Context: library + My Data summary + recent turns. |
| **Ask about a show** | same endpoint, `seedShow` param | Seeds conversation with the show's context; same persona, "showman/emotional chameleon" mode mirroring the show's tone. |
| **Concepts** | `POST /api/ai/concepts` | Input: 1..n shows. Output: bullet list only, **8 concepts** (larger pool for multi-show), 1–3 words, evocative, no explanation, no spoilers, diverse across axes (structure/vibe/emotion/relationships/craft), ordered by strength, shared-across-all-inputs when multi-show. |
| **Concept recs** | `POST /api/ai/recommend` | Input: source shows + selected concepts + count (5 Explore Similar / 6 Alchemy). Output: recs with title + external ID + media type + 1–3-sentence reason that names the matching concepts. Recent-bias, not dogmatic. |

### 7.3 Grounding pipeline (PRD §5.8 + quality bar §1.5)

For every AI-recommended title: resolve by external ID → verify case-insensitive title match → fall back to title search → attach transient `reason`. Unresolvable titles are returned flagged `unresolved` (UI renders non-interactive with Search handoff). **Real-show integrity is the non-negotiable quality gate** — the pipeline never fabricates a Show object without catalog confirmation.

### 7.4 Structured-output resilience (prompting guide §5)

Parse failure → retry once with stricter formatting instructions → fall back to unstructured commentary + Search handoff.

### 7.5 Conversation management

Ask sessions are client-held (session-only per PRD §5.7 — nothing persisted). After ~10 messages, older turns are summarized server-side into 1–2 sentences **in-persona** (no sterile system voice) and substituted into context. Welcome view: 6 random starter prompts from a curated pool (~80 prompts authored to match persona), refreshable.

### 7.6 Session-only AI data

Alchemy results/reasons, Ask history, and mentioned-shows strip live in client memory only, cleared on leave/reset. Only Scoop persists (when in collection).

---

## 8. Feature Build Plan (UI)

### 8.1 App shell & navigation

- Sidebar: **All Shows**, tag filters (one per tag + "No tags" when applicable), data filters (genre, decade, community-score ranges), plus persistent **Find** and **Settings** entries. Last selected filter remembered (localStorage).
- Main content area renders Home / Detail / Find / Person / Settings.
- Media-type toggle (All / Movies / TV) applies on top of any filter.

### 8.2 Collection Home

- Status-section grouping: **Active** (larger tiles) → **Excited** (later+excited) → **Interested** (later+interested) → collapsed **Other** (Wait, Quit, Done, later-without-interest).
- Tiles: poster, title, in-collection badge, rating badge (PRD §5.9); recently-updated ordering within sections.
- Empty states: empty collection → prompt to Search/Ask; empty filter → "No results found."

### 8.3 Find hub

Mode switcher: **Search / Ask / Alchemy**.
- **Search:** text query → poster grid, in-collection marks via overlay, tap → Detail. Honors "Search on Launch" setting. No AI voice.
- **Ask:** chat UI, streaming responses, mentioned-shows horizontal strip (tap → Detail, unresolved → Search handoff), 6 refreshable starter prompts, reset clears session.
- **Alchemy:** stepped cards — (1) pick 2+ shows via library picker + catalog search; (2) **Conceptualize Shows**; (3) select 1–8 concept chips ("pick the ingredients you want more of"; changing shows clears concepts/results, changing concepts clears results); (4) **ALCHEMIZE!** → 6 recs with reasons; (5) **More Alchemy!** chains results as new inputs.

### 8.4 Show Detail

Section order preserved exactly per `detail_page_experience.md` §3: header media carousel (trailers inline when available, graceful poster/logo fallback) → core facts + community score → tag chips → overview + Scoop toggle (copy states: "Give me the scoop!" / "Show the scoop" / "The Scoop"; streams with "Generating…") → "Ask about this show" CTA → genres/languages → recommendations strand → Explore Similar (Get Concepts → chips → Explore Shows, 5 recs, one-line "why concepts matter" explainer) → streaming providers → cast/crew strands → seasons (TV) → budget vs revenue (movies).

**Status/interest chips live in the toolbar**, not scroll body: Active / Interested / Excited / Done / Quit / Wait. Rating slider auto-saves as Done; tagging auto-saves as Later+Interested; reselecting active status → removal confirmation. No modal walls except destructive ops.

### 8.5 Person Detail

Image gallery, name, bio; analytics charts (average project ratings, top genres, projects-by-year — lightweight, e.g. Recharts); filmography grouped by year; credit tap → Show Detail.

### 8.6 Settings & Your Data

- App: font size (XS–XXL), Search-on-launch.
- User: username (synced).
- AI: provider key (env-first in benchmark; user field optional), model selection.
- Integrations: catalog key.
- **Export My Data:** server route streams a `.zip` containing JSON of all saved shows + My Data, ISO-8601 dates (via `archiver`/`jszip`).
- Import/Restore: out of scope (open question in PRD) — leave a documented stub.

---

## 9. Repo Deliverables (Rider §3)

- **`.env.example`:** `NEXT_PUBLIC_APP_URL`, `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_ANON_KEY`, `NAMESPACE_ID`, `DEFAULT_USER_ID`, `IDENTITY_MODE`, `CATALOG_API_KEY`, `AI_API_KEY`, `AI_MODEL_DEFAULT` — each commented. `.gitignore` excludes `.env*` except `.env.example`.
- **Scripts:** `npm run dev`, `npm run build`, `npm test` (unit), `npm run test:e2e`, `npm run test:reset` (namespace reset), `npm run db:migrate`, `npm run db:seed`.
- **README:** setup (hosted Supabase, no Docker), namespace generation, dev identity injection docs, production-gating notes.

---

## 10. Testing Strategy

- **Unit (Vitest):** merge rules (`selectFirstNonEmpty`, timestamp resolution), save/default/removal rules for all four save triggers, `showList` parser (exact format, retry path), catalog mapping (genre names, logo selection, media-type inference), filter derivation, overlay application.
- **Integration:** API routes against the hosted Supabase using a throwaway namespace per test run (`NAMESPACE_ID=test-<uuid>`), reset via `test:reset` — proves rider §7 destructive-testing compliance. All fixtures `is_test=true`.
- **E2E (Playwright):** the 10 key journeys from PRD §9 (build collection, rate-to-save, tag-to-save, maintain, tag filters, Ask discovery, Explore Similar, Alchemy chain, talent deep-dive, export). AI calls mocked at the provider interface for determinism.
- **AI quality (manual, rubric-driven):** discovery quality bar scoring — Voice ≥1, Taste ≥1, Real-show integrity =2 (non-negotiable), total ≥7/10; verify counts (8 concepts, 5/6 recs) and format contracts.

---

## 11. Phased Execution Order

| Phase | Deliverable | Key risks retired |
|---|---|---|
| **0. Foundation** | Next.js scaffold, Supabase migrations, env interface, identity/namespace middleware, reset endpoint, scripts, README | Rider compliance end-to-end |
| **1. Catalog + domain core** | CatalogProvider (TMDB), mapping + merge rules, shows CRUD API with save/default/removal semantics, overlay helper; unit tests | The behavioral heart: implicit saves, merges, timestamps |
| **2. Library UX** | App shell, sidebar filters, Home grouping, Search mode, Show tiles/badges, Show Detail (non-AI sections), Person Detail, Settings basics | Journeys 1–5, 9 |
| **3. AI core** | AIProvider, persona module, Scoop (streaming + 4h cache + persistence rule), grounding pipeline | Persona + real-show integrity |
| **4. Discovery surfaces** | Ask (structured mentions, summarization, starters, seed-show variant), Explore Similar, Alchemy full flow with chaining | Journeys 6–8 |
| **5. Data durability** | Export zip, `data_model_version` + migration path stub, sync conflict merge verification, duplicate merge | PRD §5.10–5.11, journey 10 |
| **6. Polish + quality bar** | Empty/critical states, streaming polish, copy pass against voice spec, rubric evaluation, e2e suite green | Quality bar; "heart" of the product |

Each phase ends runnable (`npm run dev` + tests green) so the build is verifiable incrementally.

---

## 12. Cross-Cutting Compliance Checklist

- [ ] User's version wins everywhere (overlay on every list surface).
- [ ] Every recommendation actionable → resolved to a real catalog item, else non-interactive + Search handoff.
- [ ] Spoiler-safe defaults across all AI surfaces; domain-locked to TV/movies.
- [ ] All user-owned rows carry `(namespace_id, user_id)`; no cross-namespace access possible.
- [ ] Secrets server-only; `.env.example` complete; no secrets in repo.
- [ ] Clearing client storage loses nothing user-owned (backend source of truth).
- [ ] Destructive tests scoped to namespace; no global teardown.
- [ ] OAuth adoption later = swap `resolveUser`, zero schema change.
- [ ] Section order on Detail preserved; status chips in toolbar; Scoop toggle copy states exact.
- [ ] Counts honored: 8 concepts default, max 8 selected, 5 recs (Explore Similar), 6 recs (Alchemy), 6 starter prompts, ~10-message summarization threshold, 4-hour Scoop freshness.

## 13. Open Questions (Deferred, per PRD §10)

Not built in v1, but the design leaves room: `next` status stays in the enum (hidden); import/restore stub documented; named custom lists, Alchemy session sharing, explicit myStatus sidebar filters, and unrated-vs-nil rating semantics deferred as noted in the PRD.
