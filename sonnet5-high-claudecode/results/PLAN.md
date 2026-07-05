# Implementation Plan — Personal TV/Movie Companion

Source: `docs/prd/product_prd.md`, `docs/prd/infra_rider_prd.md`, and all documents under `docs/prd/supporting_docs/` (including `technical_docs/`). This plan is scoped to *what to build and in what order*; it does not implement anything.

---

## 0. Reading Summary — What This Product Is

A personal TV/movie companion where users build "their version" of every show (status, interest, tags, rating, AI Scoop) layered on top of public catalog data. Discovery happens four ways: Search, AI chat ("Ask"), multi-show concept blending ("Alchemy"), and per-show concept exploration ("Explore Similar"). The single hard rule that shapes almost everything: **the user's saved data always wins over refreshed catalog data**, and **every AI recommendation must resolve to a real, selectable catalog item**.

Benchmark execution constraints (from the infra rider) that shape the architecture from day one:
- Next.js (latest stable) + Supabase, accessed via official client libraries.
- Every persisted record scoped to `(namespace_id, user_id)`. Namespace = build/run isolation; user_id = product identity, even in single-user/dev mode.
- Dev-mode identity injection (header or selector) now; must convert to real OAuth later **without schema changes**.
- Backend is the source of truth; client caches must be safely disposable.
- `.env.example`, one-command dev/test/reset scripts, and a repeatable migration mechanism are required deliverables, not nice-to-haves.
- No Docker dependency required to run the benchmark.

---

## 1. Architecture Overview

### 1.1 Stack
- **Runtime:** Next.js (App Router), single deployable app serving both UI and server boundary (Route Handlers / Server Actions).
- **Persistence:** Supabase Postgres, accessed through `@supabase/supabase-js`. Row-Level Security (RLS) enforced on every user-owned table using `(namespace_id, user_id)`.
- **AI provider:** Abstracted behind a server-only gateway module; provider/model selectable via settings + env, default from env at boot.
- **Catalog provider:** Abstracted behind a server-only catalog client (title/keyword search, details, images, credits, providers, similar/recommended). Provider-specific API key never reaches the client.

### 1.2 Layering
```
app/                          # Next.js routes (pages + route handlers)
server/
  db/                         # Supabase client factories (anon vs service-role), query modules
  services/                   # Domain logic: shows, collection, ai, catalog, export
  ai/                         # Prompt builders, provider gateway, streaming, resolvers
  catalog/                    # External catalog client + mapping/merge functions
  identity/                   # namespace/user resolution, dev identity injection
src/                          # Frontend — fractal Pages > Features > Sub-features (see INSTRUCTIONS.md)
supabase/
  migrations/                 # SQL migrations (schema evolution artifact)
  seed/                       # Optional fixtures for local/dev
scripts/                      # dev/test/reset CLI entry points
```

### 1.3 Key Architectural Decision — Catalog Cache vs. User Overlay

The technical reference (`storage-schema.ts`) models a single `Show` record that mixes catalog fields (title, overview, genres…) with per-user fields (`myStatus`, `myTags`, `myScore`, `myInterest`, `aiScoop`, and their update dates). That shape is correct for a single-user local client but not for a multi-user backend, where the same catalog title would otherwise be duplicated and could drift per user.

**Decision:** split storage into two tables, joined at read time into the same client-facing `Show` shape:

1. **`shows`** — catalog cache. One row per `(namespace_id, id, show_type)`. Holds every "Catalog meta / Images / Ratings / Dates / Movie-specific / TV-specific / providerData" field from the schema doc. Refreshed opportunistically when a show is viewed/searched. Merge rule on refresh: `selectFirstNonEmpty(new, old)` per field (never blank out a populated field), and `detailsUpdateDate = now()`.
2. **`user_shows`** — the per-user overlay ("My Data"). One row per `(namespace_id, user_id, show_id)`, created only when the show enters the collection (Section 5.1–5.3). Holds `myStatus`, `myInterest`, `myTags`, `myScore`, `aiScoop`, and each field's own update-date column. Deleting this row **is** "removing from collection" (Section 5.4).

Rationale: preserves every merge/timestamp rule in the PRD verbatim while avoiding catalog-data duplication and letting multiple users independently overlay the same show. The client-facing API composes `shows LEFT JOIN user_shows` so the app-level `Show` object still looks like the schema doc (display rule: overlay wins when present).

Catalog cache rows are namespace-scoped (not globally shared) to keep destructive test resets trivially safe (drop-by-namespace never touches another run's cache) at the cost of some duplicate fetches across namespaces — an acceptable tradeoff given catalog data is cheap to re-fetch and not user-owned.

---

## 2. Data Model

### 2.1 Tables (Postgres / Supabase)

**`namespaces`**
- `id` (text/uuid, PK) — stable per build/run.
- `created_at`.

**`users`**
- `id` (text/uuid, PK) — opaque, provider-agnostic.
- `namespace_id` (FK → namespaces, required) — a user belongs to exactly one namespace in this model (Section 4.3 of the rider: at minimum a single default user per namespace).
- `created_at`.
- Note: real OAuth migration later only changes *how* `id` is populated (from provider subject claim), not the column.

**`shows`** (catalog cache)
- `namespace_id` (FK, part of composite key)
- `id` (text, catalog id) — composite PK `(namespace_id, id)`
- `show_type` (`movie|tv|unknown`) — `person` excluded here; persons are not persisted (Section 2.3 below)
- `external_ids` (jsonb)
- `title`, `overview`, `tagline`, `homepage`, `original_language` (text/nullable)
- `genres` (text[], default `{}`)
- `spoken_languages`, `languages` (text[], default `{}`)
- `poster_url`, `backdrop_url`, `logo_url` (text/nullable), `network_logos` (text[], reserved)
- `vote_average`, `popularity` (float), `vote_count` (int)
- `last_air_date`, `first_air_date`, `release_date` (date/nullable)
- `runtime`, `budget`, `revenue` (int/nullable) — movie-specific
- `series_status` (text), `number_of_episodes`, `number_of_seasons` (int), `episode_run_time` (int[])
- `provider_data` (jsonb) — `{ countries: { [cc]: { flatrate?, rent?, buy?: number[] } } }`
- `details_update_date`, `creation_date`
- `is_test` (bool, default false)
- Index: `(namespace_id, show_type)`, GIN index on `genres`, trigram/FTS index on `title` for search.

**`user_shows`** (My Data overlay — collection membership)
- `namespace_id`, `user_id`, `show_id` — composite PK `(namespace_id, user_id, show_id)`, FK to `shows(namespace_id, id)`
- `my_status` (`active|next|later|done|quit|wait`, nullable) + `my_status_update_date`
- `my_interest` (`excited|interested`, nullable) + `my_interest_update_date`
- `my_tags` (text[], default `{}`) + `my_tags_update_date`
- `my_score` (float, nullable) + `my_score_update_date`
- `ai_scoop` (text, nullable) + `ai_scoop_update_date`
- `created_at`
- **Row existence with a non-null `my_status` = "in collection"** (Section 5.1). A row may transiently exist with only tags/rating set before status defaults are applied (Section 5.3), but the save flow always assigns a `my_status` in the same transaction, so in practice row-exists ⇔ in-collection.
- RLS: `namespace_id = current_namespace() AND user_id = current_user_id()`.

**`cloud_settings`** (synced app settings, per user)
- `namespace_id`, `user_id` — composite PK
- `user_name` (text, random on first creation)
- `catalog_api_key`, `ai_api_key` (text, nullable — see §7 on secret handling)
- `ai_model` (text)
- `version` (bigint epoch seconds, for conflict resolution)

**`app_metadata`**
- `namespace_id`, `user_id` — composite PK (data model version tracked per user so partial migrations are visible)
- `data_model_version` (int, default 3 to match reference schema's current version — bump on any future breaking change)

Local-only, never synced (kept client-side, not modeled server-side): `autoSearch`, `fontSize`, `hideStatusRemovalConfirmation`, `statusRemovalCountKey`, `lastSelectedFilter`. These are UI/device preferences the PRD does not require to sync; storing them in `localStorage`/equivalent satisfies "cache is disposable" (rider §6.2) since losing them has no data-loss consequence.

### 2.2 Migrations & Seed
- `supabase/migrations/0001_init.sql`: namespaces, users, shows, user_shows, cloud_settings, app_metadata, indexes, RLS policies.
- `supabase/migrations/0002_search_indexes.sql`: trigram/FTS index for title search (Section 7.2).
- `supabase/seed/dev_seed.sql` (optional): one default namespace + one default user for local dev, so `npm run dev` works with zero manual setup.
- Migration mechanism must be re-runnable against a clean database deterministically (rider §3.3, §9).

### 2.3 Person (Cast/Crew)
Person data (bio, images, filmography, credits) is **not** a first-class persisted entity — it's fetched live from the catalog provider per Person Detail view (mirrors "Not stored (transient)" list in the schema doc, which excludes `cast`/`crew`). No `persons` table. Analytics charts (average project ratings, top genres, projects-by-year) are computed client- or server-side on the fly from the fetched filmography plus the user's own ratings where the project happens to be in their collection (average project rating should default to community score when the user hasn't rated it — this is a product decision, see §11).

### 2.4 Field Mapping & Merge Rules (implementation contract)

Implement as pure, independently testable functions — these are the highest-risk-of-drift business rules in the whole app:

- `mapCatalogPayloadToShow(payload) -> ShowRow`: title required (fail decode if absent on both `title`/`name`); infer `show_type` from `name` (`tv`) vs `title` (`movie`) when catalog doesn't say; multi-format date parsing; genre id → name mapping; "best logo" chosen deterministically (e.g., highest vote count, English-preferred, stable tiebreak by id) — must be a pure function so the discovery-quality/regression suite can pin exact expected output.
- `mergeCatalogRefresh(existing, incoming) -> ShowRow`: per non-`my*` field, `selectFirstNonEmpty(incoming, existing)`; never null out a populated value; always bump `details_update_date`; never touch `creation_date` after first insert.
- `mergeUserFields(existing, incoming) -> UserShowRow`: per `my*` field independently — newer `*_update_date` wins; if only one side has a date, that side wins; ties keep existing (idempotent). This function is what powers both re-adding an already-saved show (Section 5.5) and cross-device sync conflict resolution (Section 5.10) — one implementation, two callers.

---

## 3. Identity, Namespace & Auth

- **Namespace resolution:** server reads `namespace_id` from an env var (`DEFAULT_NAMESPACE_ID`) or a request-scoped override header in test mode (`X-Namespace-Id`, gated to non-production). Every DB call goes through a helper that injects `namespace_id` so no query path can accidentally cross namespaces.
- **User resolution (dev mode):** `X-User-Id` header accepted by route handlers in dev/test, falling back to a single default user per namespace if absent (rider §5.1). A minimal dev-only "log in as user" selector in Settings lets manual testers switch identities without editing headers.
- **Production gating:** both the header-based namespace override and the dev user selector are compiled out / hard-disabled when `NODE_ENV=production` unless an explicit `ALLOW_DEV_IDENTITY=true` escape hatch is set (documented, defaulting to false).
- **RLS design:** policies reference two Postgres session settings (`app.namespace_id`, `app.user_id`) set per-request by the server using the service-role client after validating the dev-identity header; the anon key is never used to bypass RLS from the client directly — all writes go through server route handlers/Server Actions, never direct client-to-Supabase table writes, so the identity + namespace checks are always enforced in one place.
- **Auth migration path:** replacing dev identity injection with real OAuth means swapping the "resolve user_id" function to read from a verified session/JWT claim instead of a header — no schema change, no RLS policy change, satisfying rider §5.2.

---

## 4. Backend API Surface

All routes are namespace/user-scoped implicitly via the identity middleware (Section 3). Grouped by domain; exact HTTP verbs/paths are illustrative.

### 4.1 Catalog & Search
- `GET /api/catalog/search?q=` — text search, returns poster-grid-ready results with `inCollection` flag per item (join against `user_shows`).
- `GET /api/shows/:id` — full Show Detail payload: merged catalog+overlay fields, plus transient fetch (cast/crew, seasons, videos, recommendations/similar, streaming providers) fanned out to the catalog client and attached but not persisted.

### 4.2 Collection ("My Data") Mutations
- `POST /api/shows/:id/status` `{ status }` — sets `my_status`; if status is `later`, may pair with `interest`; creates `user_shows` row if absent; applies default-on-save rules (§5.3 below).
- `POST /api/shows/:id/interest` `{ interest }` — sets `my_interest`, forces `my_status = later` if not already (Section 4.2 nuance: Interested/Excited chips are Later+Interest under the hood).
- `POST /api/shows/:id/rating` `{ score }` — sets `my_score`; if unsaved, auto-saves as `Done` (§5.3 exception).
- `POST /api/shows/:id/tags` `{ tags }` — add/remove tag; if unsaved, auto-saves as `Later + Interested`.
- `DELETE /api/shows/:id/collection` — removal: deletes the `user_shows` row (clears status/interest/tags/rating/scoop atomically), server does not itself confirm — confirmation is a client-side UX gate before calling this endpoint (see §6.1).
- `GET /api/collection` — full library with computed status groupings + tile badges for Home; accepts filter query params (tag, genre, decade, score range, media type).
- `GET /api/tags` — derived tag library (distinct `my_tags` across the user's `user_shows`) for building sidebar tag filters + "No tags" virtual filter.

### 4.3 AI Surfaces
- `POST /api/ai/scoop/:showId` — generates or returns cached Scoop; streams response; persists only if `user_shows` row exists (in collection), otherwise ephemeral (§7 of PRD, §5.7 table).
- `POST /api/ai/ask` `{ messages, showContext? }` — chat turn; returns `{ commentary, showList }` structured per the mentions contract; server resolves `showList` entries to real shows via the resolver (§5.3 below) before returning, so the client never has to guess.
- `POST /api/ai/concepts` `{ showIds: string[] }` — single (`showIds.length === 1`, Explore Similar) or multi (`showIds.length >= 2`, Alchemy) concept generation; returns bullet concepts, ordered by strength.
- `POST /api/ai/recommendations` `{ showIds, concepts }` — concept-grounded recs; count depends on caller (5 for Explore Similar, 6 for Alchemy) — caller passes an explicit `count` or the endpoint infers it from context, decision: **explicit `surface: "explore_similar" | "alchemy"` param drives the count server-side** so the contract is enforced in one place, not per-client.

### 4.4 Person
- `GET /api/persons/:id` — bio, images, filmography grouped by year, computed analytics — all derived live from catalog client, no persistence.

### 4.5 Settings & Data
- `GET/PUT /api/settings` — `cloud_settings` (username, AI/catalog API keys, AI model); optimistic-concurrency via `version`.
- `GET /api/export` — streams a `.zip` containing a single JSON file: all `user_shows` rows joined with enough `shows` data to be self-describing, dates ISO-8601 encoded.
- `POST /api/import` — (see §11 Open Questions) accepts the export format and upserts via the same `mergeUserFields`/`mergeCatalogRefresh` functions used for sync, so import is "just another merge source."

### 4.6 Test/Dev Utilities (rider §7)
- `POST /api/test/reset` — deletes all rows scoped to the caller's `namespace_id` across `shows`, `user_shows`, `cloud_settings`, `app_metadata`. Gated to non-production, requires the namespace header/env to be explicit (never resets "all namespaces").
- `POST /api/test/seed` — inserts deterministic fixture shows/users into the current namespace for repeatable test runs.

---

## 5. AI Subsystem Design

### 5.1 Provider Gateway
A single server-side module (`server/ai/gateway.ts`) exposes `generate({ system, messages, stream })` and `generateStructured({ schema })`, backed by whichever provider/model is configured (env default, overridable per-user via `cloud_settings.ai_model` / `ai_api_key`). All prompt builders and resolvers sit above this gateway so swapping providers never touches feature code — directly satisfying the PRD's "rebuild parity, not a prompt cookbook" framing.

### 5.2 Shared Persona Layer
One base system prompt module encodes the persona pillars from `ai_voice_personality.md` (joy-forward, opinionated honesty, vibe-first/spoiler-safe, specific-not-generic, short-unless-earned; tone sliders 70/30 friend-critic, 60/40 hype-measured). Each surface-specific prompt builder (Scoop, Ask, Concepts, Concept-Recs) composes this shared base plus a surface addendum, rather than four independent prompts — this is what keeps "one consistent persona across surfaces" true by construction instead of by convention. **Search explicitly does not use this layer** (Section 1 of the voice spec) — it stays a plain catalog query path.

### 5.3 Contracts Per Surface
| Surface | Input | Output shape | Persistence | Count/limits |
|---|---|---|---|---|
| Scoop | show context, spoiler flag (default off) | streamed text, sectioned (personal take → honest stack-up → Scoop centerpiece → fit/warnings → verdict) | `user_shows.ai_scoop` if in collection, else ephemeral | 4h freshness cache before regenerating |
| Ask | recent turns (summarized older), optional show handoff context, user's library+My Data | `{ commentary, showList }`; `showList` format `Title::externalId::mediaType;;...` | none (session only) | summarize after ~10 messages |
| Concepts (single) | 1 show | bullet list, 1–3 words each | none | 8 concepts default |
| Concepts (multi/Alchemy) | 2+ shows | bullet list, shared-across-all-inputs only | none | larger pool than single-show; UI caps selection at 8 |
| Concept Recs (Explore Similar) | 1 show + selected concepts | list of `{ title, externalId, mediaType, reason }` | none | 5 recs |
| Concept Recs (Alchemy) | 2+ shows + selected concepts | same shape | none | 6 recs |

### 5.4 Real-Show Resolution (shared across Ask/Concepts/Alchemy)
`server/ai/resolveShowReferences(refs)`:
1. For each `{ title, externalId, mediaType }`, look up the catalog cache/provider by `externalId` first.
2. If not found (or no id given), fall back to case-insensitive exact title match, accept first hit.
3. If found: map to a real `Show`, attach the AI `reason`/mention as transient (non-persisted) text, mark selectable.
4. If not found: return as a non-interactive placeholder with a "search for this" affordance (client hands off to Search prefilled with the title).

This single resolver backs the "mentioned shows" strip in Ask, Explore Similar results, and Alchemy results — one implementation, three call sites, so the "every recommendation maps to a selectable real show" rule (PRD principle #2) can't drift between features.

### 5.5 Structured Output Parsing & Fallback
- Ask's `{ commentary, showList }` and Concept Recs are requested as structured/JSON output from the provider where supported; a strict parser validates shape.
- On parse failure: retry once with a stricter formatting instruction appended.
- On second failure: fall back to returning `commentary` only (best-effort raw text) with `showList: []`, and the client shows a generic "search for shows mentioned above" handoff rather than erroring.

### 5.6 Conversation Summarization
After each turn, if turn count exceeds ~10, the oldest turns are collapsed into a 1–2 sentence summary generated through the *same* persona layer (not a sterile system voice) and stored as a synthetic leading "context" message for subsequent calls. Summarization is a pure server-side transform, unit-testable independent of the live chat UI.

### 5.7 Concept & Recommendation Quality Guardrails
Enforced both in prompt instructions and a lightweight server-side post-filter before returning to the client:
- Reject/re-request concept lists containing known-generic terms ("good characters", "great story", "funny", "action", etc. — seed a small blocklist from `concept_system.md` §7).
- Enforce 1–3 word concept length server-side (truncate/reject oversized entries rather than trusting the model).
- Enforce ordering is "by strength" is a prompt instruction only (not mechanically verifiable) — covered instead by the manual quality-bar review process in §9.

---

## 6. Business Rules Implementation Map

Each rule from PRD §5 gets one authoritative implementation location so behavior can't diverge between entry points (Detail page vs. tile quick actions vs. AI-driven saves all call the same service functions).

### 6.1 Save/Remove Triggers (`server/services/collection.ts`)
- `setStatus`, `setInterest`, `rateShow`, `addTag` — each is "upsert-or-create" against `user_shows`: if no row exists, create one first, then apply the field, then apply **default-on-create** rules:
  - default create: `my_status = later`, `my_interest = interested`
  - exception: creation triggered by `rateShow` → `my_status = done` (no interest set)
  - creation triggered by `addTag` → `my_status = later`, `my_interest = interested`
  - creation triggered by `setInterest` (Interested/Excited chip) → `my_status = later` always, regardless of whichever default would otherwise apply
- `removeFromCollection(showId)` — hard-deletes the `user_shows` row. **Confirmation is a client responsibility**: the Detail page and any status-chip control must intercept "reselect current active status" and show a confirmation dialog before calling this endpoint, with a "stop asking" toggle persisted to local UI state (`hideStatusRemovalConfirmation`) and a running count (`statusRemovalCountKey`) used to decide when to offer that toggle.

### 6.2 Re-adding / Sync Merge (`mergeUserFields`, §2.4)
Single function reused by: viewing a show that already exists in another device's data (sync pull), and by `/api/import`. No separate "re-add" code path exists — re-adding *is* a merge with the current stored row as one side and freshly viewed/imported data as the other.

### 6.3 Timestamps
Every mutation to a `my*` field sets its paired `*_update_date = now()` in the same transaction. These columns are the single source of truth used for: Home sorting ("recently updated first" where applicable), sync conflict resolution, and AI Scoop freshness — never recompute "is this fresh" from anything but `ai_scoop_update_date`.

### 6.4 Tile Indicators
Computed at read time in `/api/collection` and `/api/catalog/search` responses (`inCollection: my_status != null`, `hasRating: my_score != null`) — never stored as separate flags, so they can never drift from the underlying fields.

### 6.5 Data Sync & Conflict Resolution
Implemented as: client fetches the current server state, applies local optimistic changes, and on any write conflict (concurrent update detected via update-date comparison), the server-side `mergeUserFields` resolves it — the client never needs its own merge logic, keeping "backend is source of truth" (rider §6.1) literally true.

### 6.6 Data Continuity Across Versions
`app_metadata.data_model_version` gates a migration runner executed on deploy (not per-request): each version bump ships a corresponding SQL migration that transforms existing rows forward, and the runner is idempotent (safe to re-run). No client-triggered migrations — this satisfies "without requiring user intervention."

---

## 7. Settings, Secrets & Export

- **API keys:** `ai_api_key` / `catalog_api_key` in `cloud_settings` are optional user-entered overrides; if absent, server falls back to the deployment's own env-provided keys (`AI_PROVIDER_API_KEY`, `CATALOG_API_KEY`). User-entered keys are never sent to the client after save (write-only field from the client's perspective — API returns a boolean "isSet" instead of the value). Elevated Supabase service-role key is server-only, never bundled to the client (rider §3.1).
- **Font size / Search-on-launch:** local settings, client-only, no server round trip needed for these (they don't need to sync per PRD).
- **Username:** synced, part of `cloud_settings`.
- **Export:** `/api/export` produces `{ exportedAt, shows: [...] }` JSON (ISO-8601 dates), zipped server-side, streamed as a download — matches "Export My Data" requirement verbatim.
- **Import:** flagged Open in the PRD; plan includes it as a fast-follow (Phase 10) built on the existing merge function rather than bespoke logic, since the format is already self-describing from Export.

---

## 8. Frontend Architecture (Fractal: Pages → Features → Sub-features)

Per `INSTRUCTIONS.md`: humble components (markup+binding only, logic in hooks), no magic numbers/inline styles, co-located feature code, `PageName/PageName.tsx` naming (no `index.tsx`).

```
src/pages/
  Home/
    Home.tsx                         # collection grouped by status + media-type toggle
    features/
      FiltersPanel/                  # All Shows / tag filters / data filters / media toggle
      StatusSection/                 # Active / Excited / Interested / Other(collapsed)
        features/ShowTile/           # poster, title, badges (in-collection, rating)
      EmptyState/                    # no shows vs. filter-yields-none copy
  Find/
    Find.tsx                         # mode switcher: Search | Ask | Alchemy
    features/
      Search/
        features/ResultsGrid/, SearchBar/
      Ask/
        features/ChatThread/, Composer/, MentionedShowsStrip/, StarterPrompts/
      Alchemy/
        features/ShowPicker/, ConceptSelector/, RecommendationResults/
  Detail/
    Detail.tsx
    features/
      HeaderMedia/                   # backdrops/posters/logos/trailers carousel
      CoreFactsRow/                  # year/runtime/seasons + community score
      MyRelationshipControls/        # status chips, interest, rating bar, tag picker
      OverviewAndScoop/              # overview text + Scoop toggle/stream
      AskAboutShowCta/
      RecommendationsStrand/         # traditional similar/recommended
      ExploreSimilar/                # Get Concepts -> select -> Explore Shows
      StreamingAvailability/
      CastCrewStrands/
      SeasonsStrand/                 # TV only
      BudgetRevenue/                 # movies only, when available
  Person/
    Person.tsx
    features/ImageGallery/, AnalyticsCharts/, FilmographyByYear/
  Settings/
    Settings.tsx
    features/AppSettings/, UserSettings/, AISettings/, Integrations/, YourData/
components/                          # shared primitives (StatusChip, RatingSlider, TagPicker, PosterCard…)
hooks/                                # useCollection, useShowDetail, useAiScoop, useAskSession, useAlchemySession…
utils/                                # formatting, date, merge helpers shared with server where isomorphic
config/                               # status/interest enums, filter types, concept caps, freshness windows
theme/                                # tokens (no hex/px in TSX)
```

Global entry points (persistent nav): **Find/Discover** and **Settings**, per PRD §6 — implemented as top-level nav items always visible regardless of current page, not nested inside Home.

### 8.1 State/Data Fetching
- Server state (collection, show detail, settings) via a query layer (e.g., React Query-equivalent) reading directly from the API routes in §4 — no bespoke client-side merge logic (per §6.5).
- Ephemeral AI session state (Ask messages, Alchemy step state, Explore Similar concepts) lives in page/feature-local state only, cleared on navigation away — matches the "session only, not persisted" rule (§5.7 table) by construction (nothing writes it to storage).

---

## 9. Cross-Cutting Rules → Where They're Enforced

| Rule (PRD §8) | Enforcement point |
|---|---|
| User's version takes precedence everywhere | `shows LEFT JOIN user_shows` composition happens in one server-side "hydrate show" function reused by every list/detail endpoint — never re-implemented per screen |
| Discovery must be actionable | `resolveShowReferences` (§5.4), used by every AI surface that returns titles |
| Taste-aware AI | Prompt builders (§5.2) always receive library + My Data + session context where the surface calls for it |
| Spoiler-safe by default | Base persona prompt hard-codes spoiler-safe instruction; explicit user request required to lift it (passed as an explicit flag, not inferred) |
| Implicit behaviors feel natural | Centralized default-on-save rules (§6.1) — one place, so every entry point behaves identically |
| Your data is yours | Export always available; import planned; no server-only lock-in of user data |
| Identity is explicit | `user_id` required column, non-null FK, enforced by RLS + service-layer checks (§3) |
| Runs/builds are isolated | `namespace_id` on every table, required by RLS + test reset/seed endpoints (§4.6) |
| Backend is source of truth | No client-side merge logic; client cache is a query cache, safely clearable |

---

## 10. Testing & Quality Strategy

- **Unit tests** (adjacent to source, per INSTRUCTIONS.md) for the highest-risk pure functions: `mapCatalogPayloadToShow`, `mergeCatalogRefresh`, `mergeUserFields`, default-on-save resolution, `resolveShowReferences`, concept generic-term filter, mentions `showList` parser (including malformed-input cases feeding the retry/fallback path).
- **Integration tests** against a real (local or hosted-test) Supabase instance scoped to a disposable test namespace, exercising: save/remove/re-add lifecycle, timestamp-wins merges, RLS isolation (user A cannot read/write user B's `user_shows`; namespace X cannot read/write namespace Y's rows).
- **AI quality checks:** not full golden-set automation (v1 golden set is explicitly unpopulated in the PRD), but a small fixed manual/scripted checklist wired to `discovery_quality_bar.md`'s rubric (voice, taste alignment, surprise-without-betrayal, specificity, real-show integrity) run against a handful of fixed prompts before shipping AI-surface changes; real-show integrity is treated as a hard gate (must be 2/2) since it's flagged non-negotiable.
- **Visual testing:** snapshot/screenshot tests for Detail page section ordering and Home status grouping, since layout/order is explicitly product-specified (narrative hierarchy, §7.5 of PRD).
- **Destructive test tooling:** `npm run test:reset` calls `/api/test/reset` for the active namespace only; CI/dev workflows always run against a namespace unique to that run to avoid any cross-run collision, satisfying rider §7.

---

## 11. Decisions on Open Questions (so the plan isn't blocked on them)

The PRD lists these as open; this plan makes an explicit, reversible call for each so implementation isn't blocked, and flags where the schema already accommodates a future reversal:

- **`Next` status:** keep in the data model (already an enum value) but do not surface it as a first-class UI status yet — no UI work planned this round; revisit if usage data asks for it.
- **Named custom lists beyond tags:** out of scope this round; tags already give ad hoc grouping. No schema changes needed later since lists could be layered as a `list_name` alongside tags without touching existing columns.
- **AI Scoop on unsaved show implicitly saving it:** **no** — keep Scoop generation available on unsaved shows without saving (matches "Persisted only if already in collection" in §5.7 and "Critical States: unsaved show" in the detail-page spec, which says Scoop "can be generated but only persists if user saves"). Implicit-save-on-Scoop would contradict that.
- **Clearing My Rating — explicit `Unrated` vs. nil:** use `nil`/`null` (simpler, and every other nullable `my*` field already uses null-as-unset; introducing a separate sentinel would be the one-off) — rating UI treats null as "unrated" state directly.
- **Import/Restore:** planned as Phase 10 (fast-follow), built on the same merge primitives as sync, since Export already defines the wire format.
- **Saving/sharing Alchemy sessions as reusable "blends":** out of scope this round; sessions remain ephemeral per PRD §5.7. No persistence path planned.
- **Explicit `myStatus` filters in sidebar:** include this round — it's low-cost (the filter model already supports a `myStatus` `FilterType`) and directly useful alongside existing tag/genre/decade/score filters.

---

## 12. Build Phases

Sequenced to de-risk the hardest shared primitives first (identity/merge/AI resolution), since nearly every later feature depends on them.

1. **Phase 0 — Infra scaffolding.** Next.js app skeleton, Supabase project wiring, `.env.example`, migrations 0001, dev identity injection, `npm run dev/test/test:reset` scripts, RLS policies, namespace/user resolution middleware.
2. **Phase 1 — Catalog + collection core.** Catalog client, `mapCatalogPayloadToShow`, `mergeCatalogRefresh`, Search (7.2), `user_shows` CRUD + default-on-save rules (§6.1), Home page with status grouping + filters + media toggle + tile indicators + empty states (7.1).
3. **Phase 2 — Show Detail (non-AI sections).** Header media, core facts, My Relationship controls (status/interest/rating/tags with auto-save + removal confirmation), overview, traditional recommendations strand, streaming availability, cast/crew strands, seasons, budget/revenue (7.5 minus AI sections).
4. **Phase 3 — AI Scoop.** Persona base layer, Scoop prompt/streaming, 4h freshness cache, persistence-if-in-collection rule.
5. **Phase 4 — Concepts + Explore Similar.** Concept generation (single-show), concept selection UX, concept-grounded recs (5), `resolveShowReferences`, generic-term guardrail.
6. **Phase 5 — Alchemy.** Multi-show picker, shared-concept generation (multi), selection cap (8), recs (6), chaining ("More Alchemy!"), backtracking clears downstream state.
7. **Phase 6 — Ask.** Chat UI, mentions structured output + parser/fallback, mentioned-shows strip, starter prompts (6 of 80, refreshable), summarization after ~10 turns, "Ask about this show" handoff/seeding.
8. **Phase 7 — Person Detail.** Live-fetched bio/gallery/filmography, analytics charts, credit → Detail navigation.
9. **Phase 8 — Settings & Your Data.** Font size, search-on-launch, username, AI/catalog key management (write-only keys), model selection, Export.
10. **Phase 9 — Cross-device sync & continuity.** Wire `mergeUserFields`/`mergeCatalogRefresh` into a pull/push sync path, `app_metadata` migration runner, verify "clear local storage → no data loss" end-to-end.
11. **Phase 10 — Fast-follows.** Import/Restore, `myStatus` sidebar filters, quality-bar checklist automation where feasible.

Each phase ends with the relevant slice of §10 tests passing before moving on; Phases 3–6 additionally get a manual quality-bar pass per `discovery_quality_bar.md` before being considered done.

---

## 13. Risks & Watch-Items

- **Structured-output reliability** (Ask mentions, concept recs) is the single biggest correctness risk to the "real-show integrity" bar — mitigated by the retry-once-then-fallback design (§5.5), but provider/model choice should be validated against this specifically before locking in a default.
- **Namespace scoping of catalog cache** duplicates fetches per namespace; acceptable now, but if namespaces multiply heavily in later benchmark rounds this may warrant a shared-cache-with-namespace-scoped-user-data revisit (flagged, not designed for now — avoiding speculative complexity per current scope).
- **RLS correctness** is load-bearing for the entire identity model; Phase 0 must include isolation tests (two namespaces, two users) before any feature work builds on top of it, not after.
- **Dev identity injection leaking to production** is a security footgun if the gating flag is misconfigured — Phase 0 includes an explicit build-time check, not just a runtime env check.
