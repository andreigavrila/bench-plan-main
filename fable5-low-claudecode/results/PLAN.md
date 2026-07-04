# Implementation Plan — Personal TV + Movie Companion

This plan covers the full scope of `docs/prd/product_prd.md`, the Infrastructure & Execution Rider, and all supporting specs (AI prompting context, AI voice/personality, concept system, detail-page experience, discovery quality bar, and the storage schema reference).

---

## 1. Scope Summary

Build a **Next.js (latest stable) + Supabase** web app: a personal TV/movie companion where users collect, organize (status/interest/tags/rating), and discover shows via four paths — catalog Search, conversational **Ask**, multi-show **Alchemy**, and per-show **Explore Similar** — plus an AI **Scoop** review, Person pages, filters, settings, and data export. The backend is the source of truth; all persisted user data is partitioned by `(namespace_id, user_id)` for benchmark run isolation.

External dependencies:
- **Catalog provider** (TMDB-style API): search, details, credits, seasons, images/videos, watch providers, similar/recommended, person data. Key via env var.
- **AI provider** (Anthropic Claude by default): chat, structured mentions, scoop streaming, concept extraction, concept-based recs. Key/model via env vars.

---

## 2. Architecture

### 2.1 High-level

```
Browser (Next.js App Router, React)
  ├─ UI: Home / Detail / Find (Search|Ask|Alchemy) / Person / Settings
  ├─ Client state: React Query cache (disposable; backend is truth)
  └─ Calls Next.js Route Handlers (/api/*)
        ├─ Identity middleware (dev identity injection; OAuth-ready)
        ├─ Catalog service (external catalog API; server-side key)
        ├─ AI service (provider SDK; server-side key; streaming)
        └─ Supabase (service-role key, server-only) — persistence
```

Key decisions:
- **All external API keys stay server-side.** The browser only talks to our route handlers. Supabase is accessed from the server with the service key (or from the client with anon key + RLS — see 2.2; server-only is the simpler, chosen path since dev identity is header-based).
- **React Query** for client caching; safe to clear at any time (rider §6.2).
- **Streaming** (SSE / ReadableStream) for Ask replies and Scoop generation.

### 2.2 Identity & isolation (rider §4–5)

- `NAMESPACE_ID` env var: stable per build/run; every DB row includes `namespace_id`. All queries filter by it; reset scripts delete only within it.
- `user_id`: opaque string. Dev identity injection: server reads `X-User-Id` header if present (dev/test only, gated by `NODE_ENV`/flag), else falls back to `DEFAULT_USER_ID` env var. A `users` table exists so real OAuth later only changes how `user_id` is derived — no schema redesign.
- Effective partition everywhere: `(namespace_id, user_id)`.

### 2.3 Database schema (Supabase / Postgres)

Derived from `storage-schema.ts`, normalized for a backend:

**`shows`** — user-scoped saved shows (a row *is* collection membership):
- PK: `(namespace_id, user_id, id)` where `id` = catalog show id (string).
- Catalog snapshot columns: `title`, `show_type` (`movie|tv|person|unknown`), `external_ids jsonb`, `overview`, `genres text[]`, `tagline`, `homepage`, `original_language`, `spoken_languages text[]`, `languages text[]`, `poster_url`, `backdrop_url`, `logo_url`, `network_logos text[]`, `vote_average`, `vote_count`, `popularity`, `release_date`, `first_air_date`, `last_air_date`, `runtime`, `budget`, `revenue`, `series_status`, `number_of_episodes`, `number_of_seasons`, `episode_run_time int[]`, `provider_data jsonb`.
- My Data: `my_status` (`active|next|later|done|quit|wait`), `my_interest` (`excited|interested`), `my_tags text[]`, `my_score double`, `ai_scoop text` + the five per-field timestamps (`my_status_update_date`, `my_interest_update_date`, `my_tags_update_date`, `my_score_update_date`, `ai_scoop_update_date`).
- Management: `details_update_date`, `creation_date`, `is_test bool default false`.

**`settings`** — per `(namespace_id, user_id)`: `user_name` (random on first launch), `ai_model`, `catalog_api_key`, `ai_api_key` (optional, never seeded from repo), `auto_search`, `font_size`, `version` (epoch seconds for conflict resolution).

**`ui_state`** — per `(namespace_id, user_id)`: `hide_status_removal_confirmation`, `status_removal_count`, `last_selected_filter jsonb`.

**`app_metadata`** — per namespace: `data_model_version int` (default 3) for migration continuity (PRD §5.11).

Migrations via Supabase SQL migration files (`supabase/migrations/`), applied with `supabase db push` or a plain `psql`/script runner so **Docker is not required**. Seed fixtures optional.

### 2.4 Business-rules service (server-side, single module)

Centralize the PRD §5 rules so every mutation path shares them:
- **Save triggers:** setting status / interest chip / rating / first tag on an unsaved show creates the row.
- **Defaults:** save without explicit status → `later` + `interested`; first save via rating → `done`.
- **Removal:** clearing status deletes the row (all My Data + scoop gone). Client shows confirmation, with "stop asking" after repeats (`ui_state`).
- **Merge:** catalog refresh uses `selectFirstNonEmpty(new, old)` for public fields (never overwrite non-empty with empty/nil); My-fields resolve by newer per-field timestamp; `details_update_date = now()` after merge; `creation_date` immutable.
- **Timestamps:** every My-field write stamps its `*_update_date`.
- **Overlay rule:** every list/search/AI result response is overlaid with the user's saved version (status/tags/rating/scoop badges) before returning to the client.

### 2.5 API surface (route handlers)

- `GET/PUT /api/shows/:id` — saved show read; upsert My Data (status/interest/tags/rating) applying rules; `DELETE` for removal.
- `GET /api/collection` — user library with filter params (tag, genre, decade, score range, media type); server returns grouped-by-status or client groups.
- `GET /api/catalog/search?q=` — catalog search, overlaid with in-collection markers.
- `GET /api/catalog/show/:id` — full detail (details+credits+videos+images+providers+similar+seasons), merged with stored row if present.
- `GET /api/catalog/person/:id` — person details + credits.
- `POST /api/ai/ask` — streaming chat; structured `{commentary, showList}` output (`Title::externalId::mediaType;;...` contract); server resolves showList to real shows.
- `POST /api/ai/scoop/:id` — streamed scoop; persisted only if show in collection; 4-hour freshness check.
- `POST /api/ai/concepts` — 1..n show ids → 8 concepts (shared commonality when multiple).
- `POST /api/ai/recommend` — concepts (+source shows) → 5 (Explore Similar) or 6 (Alchemy) recs, each resolved to a real catalog item + reason.
- `GET/PUT /api/settings`, `GET/PUT /api/ui-state`.
- `GET /api/export` — zip with JSON backup, ISO-8601 dates.
- `POST /api/test/reset` — dev/test only; deletes rows for the namespace (optionally `is_test` only).

### 2.6 AI layer

- Provider abstraction (model/key from settings or env; env wins in benchmark mode).
- **Persona system prompt** shared across surfaces, per `ai_voice_personality.md` (warm, opinionated, spoiler-safe, vibe-first, TV/movies only), with surface modes: Ask (brisk friend), Scoop (mini blog post, ~150–350 words, sections: personal take / honest stack-up / The Scoop centerpiece / fit & warnings / verdict), Concepts (bullet-only, 1–3 words, evocative, no generics, ordered by strength, diverse axes), Concept-recs (excited reasons naming the matched concepts, recency bias without dogma).
- **Taste context:** library + My Data summarized into the prompt; current-show context for "Ask about this show" and Scoop.
- **Conversation summarization:** after ~10 messages, older turns compressed to 1–2 sentences in-persona; chat state is session-only (client memory), never persisted.
- **Structured-output guardrails:** exact `showList` parser; on parse failure retry once with stricter instructions, else fall back to unstructured commentary + Search handoff. Rec resolution: look up by external id, accept first case-insensitive title match; unresolved titles render non-interactive/hand off to Search (real-show integrity is non-negotiable per quality bar).
- 6 random starter prompts (pool of ~80) with refresh for the Ask welcome view.

### 2.7 Frontend structure

- **Layout:** persistent sidebar (All Shows, tag filters + "No tags", data filters: genre/decade/community-score), top-level nav to Find and Settings; media-type toggle (All/Movies/TV) applied atop any filter; last selected filter persisted in `ui_state`.
- **Home:** status sections in order Active (larger tiles) → Excited → Interested → collapsed "Other" (Wait, Quit, Done, later-without-interest); tiles show poster/title + in-collection and rating badges; empty states per PRD.
- **Find hub:** mode switcher Search / Ask / Alchemy. Search: poster grid, in-collection marks, optional auto-open on launch (`autoSearch`). Ask: chat UI, mentioned-shows strip, starter prompts, streaming. Alchemy: pick 2+ shows (library + search) → "Conceptualize Shows" → select up to 8 concept chips → "ALCHEMIZE!" → 6 recs with reasons → "More Alchemy!" chaining; changing shows/concepts clears downstream state; results session-only.
- **Show Detail:** section order per `detail_page_experience.md` (header media carousel with trailer/poster fallback → core facts + community score → tag chips → overview + Scoop toggle ("Give me the scoop!"/"Show the scoop"/"The Scoop", streaming, 4-h cache) → "Ask about this show" (seeds Ask with show context) → genres/languages → recommendations strand → Explore Similar (Get Concepts → chips → Explore Shows, 5 recs) → streaming providers → cast/crew strands → seasons (TV) → budget/revenue (movies)). Status/interest chips in toolbar; reselect-to-remove with confirmation; rating slider auto-save-as-Done; tag picker auto-save-as-Later+Interested.
- **Person Detail:** gallery, bio, analytics charts (avg ratings, top genres, projects-by-year — lightweight, e.g. Recharts), filmography grouped by year linking back to Detail.
- **Settings:** font size, search-on-launch, username, AI key/model, catalog key, Export My Data (zip download). Import listed as a stretch (PRD open question).

---

## 3. Implementation Phases

**Phase 0 — Scaffold & infra (rider compliance first)**
Next.js app, TypeScript, `.env.example` (SUPABASE_URL, SUPABASE_SERVICE_KEY, SUPABASE_ANON_KEY, NAMESPACE_ID, DEFAULT_USER_ID, CATALOG_API_KEY, AI_API_KEY, AI_MODEL), `.gitignore` for `.env*`, scripts `dev` / `test` / `test:reset`, Supabase migrations, identity middleware, health check.

**Phase 1 — Data core**
`shows` repository + business-rules module (save triggers, defaults, removal, merge, timestamps, overlay), settings/ui-state endpoints, unit tests for every §5 rule (these are the benchmark-critical behaviors).

**Phase 2 — Catalog integration**
Catalog client (search, movie/tv details, person, providers, similar), mapping to the Show shape (genre-name mapping, image URL building, best-logo pick, multi-format date parsing, tv/movie inference), merge-on-fetch flow.

**Phase 3 — Library UI**
Layout + sidebar filters + media toggle, Home status grouping, tiles with badges, Show Detail (non-AI sections) with all My Data interactions, Person Detail, Search mode.

**Phase 4 — AI surfaces**
Provider abstraction + persona prompts; Scoop (streaming, cache, persist-if-saved); Ask (chat, summarization, mentions strip, starter prompts, "Ask about this show" seeding); Concepts + Explore Similar (5 recs); Alchemy flow (6 recs, chaining); resolution + fallback guardrails.

**Phase 5 — Settings, export, polish**
Settings page, Export zip, empty states, error/network handling, font-size readability setting, removal-confirmation suppression.

**Phase 6 — Testing & quality bar**
- Unit: business rules, merge policy, showList parser, catalog mapping.
- Integration (against namespaced Supabase, reset via `test:reset`): save/remove/re-add flows, overlay, filters, export contents.
- E2E (Playwright) for key journeys 1–10 in PRD §9, using `X-User-Id` injection and `is_test` data.
- Manual AI quality check against `discovery_quality_bar.md` rubric (voice ≥1, taste ≥1, real-show integrity = 2, total ≥7/10).

---

## 4. Compliance Checklist (rider §9)

- ✅ `.env.example` + config-only setup, secrets never committed, elevated keys server-only.
- ✅ One-command dev/test/reset scripts.
- ✅ Deterministic migrations for fresh DB state; no Docker required (hosted Supabase primary path).
- ✅ All rows carry `namespace_id` + `user_id`; destructive tests scoped to namespace; no global teardown.
- ✅ Dev identity injection documented and prod-gated; OAuth swap = auth wiring only.
- ✅ Backend source of truth; client cache disposable.

## 5. Risks & Open Questions

- **Catalog/AI rate limits & latency:** mitigate with server-side request coalescing and React Query caching; AI failures degrade to Search handoff.
- **Rec resolution accuracy:** hallucinated IDs handled by title-match validation + non-interactive fallback (quality bar's non-negotiable).
- **PRD open questions** (Next status in UI, custom lists, import/restore, unrated state, saved Alchemy blends, myStatus sidebar filters): treated as out of scope; schema already supports `next` status and `myStatus` filter type so they can be added without migration.
