# Implementation Plan — Personal TV + Movie Companion

> **Scope of this document.** This is a *planning-only* deliverable. It describes what to build and how the pieces fit together, grounded in `docs/prd/product_prd.md`, `docs/prd/infra_rider_prd.md`, and every supporting doc under `docs/prd/supporting_docs/` (AI prompting, AI voice/personality, concept system, detail page experience, discovery quality bar, and the `technical_docs/storage-schema.{md,ts}`). It also honors the architecture/code standards in `INSTRUCTIONS.md`. No product code is written here.

---

## 1. Product understanding (the "why", condensed)

The app is a **personal library + taste-aware discovery** product. A user builds *their version* of each show/movie — status, interest, tags, rating, AI "Scoop" — and that taste profile powers four discovery paths:

1. **Search** — plain external-catalog search, *no AI voice*.
2. **Ask** — conversational AI discovery with a consistent "fun TV/movie nerd friend" persona.
3. **Alchemy** — blend 2+ shows into shared *concepts*, then get 6 grounded recommendations, chainable.
4. **Explore Similar** — per-show concept extraction → 5 grounded recommendations.

Two invariants define the product's soul and thread through every feature:

- **The user's version always wins.** Wherever a show appears (home, search, AI output, recommendations), if the user has saved it, the overlaid My Data (status/interest/tags/rating/scoop) is shown. User edits beat refreshed catalog data.
- **Discovery is actionable.** Every AI recommendation must resolve to a *real, selectable* catalog item, or be handed off to Search.

The infra rider adds three non-UX invariants: **Next.js + Supabase**, **runs are isolated by `namespace_id`**, and **every user-owned record is scoped to a `user_id`** with a migration-friendly path to real OAuth. The backend is the source of truth; client caches are disposable.

The plan below is organized so these invariants are enforced structurally (schema + server layer) rather than by convention.

---

## 2. Technology decisions (and why)

| Concern | Choice | Rationale (tie to a requirement) |
|---|---|---|
| App runtime | **Next.js (latest stable), App Router, TypeScript** | Required by `infra_rider_prd.md §2`. App Router gives us Server Components for catalog reads and Route Handlers as the server boundary that enforces identity. |
| Persistence | **Supabase (Postgres) via official `@supabase/supabase-js`** | Required by `infra_rider_prd.md §2`. Postgres RLS + columns give first-class `(namespace_id, user_id)` partitioning. |
| Server data caching (client) | **TanStack Query** | Rider §6.2 — cache must be *disposable*. TanStack Query is a pure cache over server truth; clearing it loses nothing. |
| Session-only AI state | **React Context + `useReducer` (or Zustand) per Find session** | PRD §5.7 — Ask/Alchemy state is session-only, never persisted. Lives in memory, cleared on leave/reset. |
| Styling | **Tailwind CSS v4 with a centralized design-token layer** (`src/theme/`) | `INSTRUCTIONS.md`: no hex/pixels/inline styles in TSX; reference theme tokens only. Tokens defined once; Tailwind theme is generated from them. |
| Validation / schema | **Zod** | Validate env, API payloads, AI structured output, and import files at boundaries. |
| AI provider | **Anthropic (Claude) via `@anthropic-ai/sdk`, behind a provider abstraction** | Default to the latest capable Claude model (`claude-opus-4-8`) with the model selectable in Settings. Streaming for the Scoop; structured outputs for the Ask "mentioned shows" contract. Abstraction keeps PRD §7's "AI model selection" and future provider swaps clean. |
| External catalog | **TMDB adapter behind a `CatalogProvider` interface** | The schema (`voteAverage`, `providerData.countries.flatrate/rent/buy`, genre-id→name mapping, external_ids, videos/credits/similar) maps 1:1 to TMDB. PRD keeps vendor specifics out of scope, so TMDB lives behind an interface (`§9`). |
| Testing | **Vitest + React Testing Library (unit/logic), Playwright (visual/E2E)** | `INSTRUCTIONS.md`: unit tests for critical logic; "visual testing highly preferred". |
| Packaging of export | server-side `.zip` (e.g. `jszip`/`archiver`) | PRD §7.7 — "Export My Data" produces a `.zip` of JSON with ISO-8601 dates. |

> **AI model note.** Default model `claude-opus-4-8` (adaptive thinking, streaming). The Ask "mentioned shows" contract uses **structured outputs** (`output_config.format` JSON schema) so `commentary` + `showList` come back reliably; on a parse failure we retry once with stricter instructions, then fall back to unstructured commentary + Search handoff (`ai_prompting_context.md §5`). The Scoop **streams** progressively. Prompt caching keys the stable persona/system prefix so per-request cost stays low.

---

## 3. Identity, isolation & the server boundary (rider-critical)

This is designed first because it constrains the schema and every data path.

### 3.1 Namespace (build isolation)
- A single stable **`NAMESPACE_ID`** is read from env at boot (rider §4.1). It is a *build* primitive, not a user concept.
- Every persisted row carries a `namespace_id` column. All queries filter on it. Two namespaces can never read/write each other's data.
- Destructive test resets are scoped to `(namespace_id [, isTest])` — never a global teardown (rider §7).

### 3.2 User identity (opaque, multi-user-ready)
- Every user-owned row carries a `user_id` (opaque stable string/UUID; no provider meaning encoded — rider §4.2).
- The system behaves as if multiple users exist even though the UI is single-user today.
- Effective partition key everywhere: **`(namespace_id, user_id)`** (rider §4.3).

### 3.3 Dev identity injection, prod-gated (rider §5)
- A single **`getIdentity(request)`** resolver runs on the server:
  - **dev/test**: accept `X-User-Id` header, else a configured `DEFAULT_USER_ID` for the namespace.
  - **prod**: read the authenticated session (OAuth wired later).
- Gated by `APP_MODE`/`NODE_ENV`; the header path is refused in prod.
- **Migration to OAuth requires config + auth wiring only, not a schema redesign** (rider §5.2) — because `user_id` is already the opaque partition key.

### 3.4 Backend is the source of truth (rider §6, PRD §8.9)
- All persisted user data lives in Supabase. The browser may cache via TanStack Query, but **clearing client storage loses nothing**.
- **All writes and identity-scoped reads go through Next.js Route Handlers / Server Actions**, never directly from the browser to Supabase. This is what lets us enforce `(namespace_id, user_id)` and keep the elevated key server-only.

### 3.5 Key handling (rider §3.1)
- Browser/client code uses only the Supabase **anon key**. Any elevated key (service role) is **server-only**.
- Row-Level Security policies are added as defense-in-depth so a leaked anon key still can't cross namespace/user boundaries. The server layer remains the primary enforcement point.
- Secrets are never committed; `.gitignore` excludes `.env*` except `.env.example`.

---

## 4. Data model & persistence

Mirrors `technical_docs/storage-schema.ts` while adding the isolation columns and merge semantics.

### 4.1 `shows` table (the core entity)
Columns (grouped as in `storage-schema.md`):
- **Isolation/identity:** `namespace_id`, `user_id`, `id` (catalog id / stable key). **Primary key `(namespace_id, user_id, id)`** so the same catalog item can be owned by different users/namespaces independently.
- **Identity/meta:** `title`, `show_type` (`movie|tv|person|unknown`), `external_ids` (jsonb), `overview`, `genres` (text[]), `tagline`, `homepage`, `original_language`, `spoken_languages` (text[]), `languages` (text[]).
- **Images:** `poster_url`, `backdrop_url`, `logo_url`, `network_logos` (text[]).
- **Ratings/popularity:** `vote_average`, `vote_count`, `popularity`.
- **Dates:** `last_air_date`, `first_air_date`, `release_date`.
- **Movie:** `runtime`, `budget`, `revenue`. **TV:** `series_status`, `number_of_episodes`, `number_of_seasons`, `episode_run_time` (int[]), `last_episode_run_time`.
- **My Data + per-field timestamps:** `my_tags` (text[]) + `my_tags_update_date`; `my_score` + `my_score_update_date`; `my_status` + `my_status_update_date`; `my_interest` + `my_interest_update_date`.
- **AI:** `ai_scoop` + `ai_scoop_update_date`.
- **Management:** `details_update_date`, `creation_date`, `is_test` (bool default false).
- **Providers:** `provider_data` (jsonb; **IDs only**, by country → flatrate/rent/buy — `storage-schema.md §ProviderData`).

**Transient (never stored):** cast, crew, seasons, images arrays, videos, recommendations, similar, lastEpisodeToAir, aiDescription, tile/selection UI state. These are re-fetched from the catalog for UI (`storage-schema.md §"Not stored"`).

### 4.2 Supporting tables
- **`cloud_settings`** (synced settings, PRD §7 + schema): `namespace_id`, `user_id`, `id` (default `"globalSettings"`), `user_name`, `version` (epoch seconds, for conflict resolution), `catalog_api_key`, `ai_api_key`, `ai_model`. Keys stored here are **optional** and never committed; in benchmark mode they may come from env instead (PRD §7 AI note).
- **`app_metadata`**: `namespace_id`, `user_id`, `data_model_version` (default 3) — drives migrations (§4.5).

### 4.3 Client-only settings (disposable cache, not source of truth)
Stored in `localStorage` per `storage-schema.md §"Other persistent storage"`:
- **Local settings:** `autoSearch` (bool), `fontSize` (`XS|S|M|L|XL|XXL`).
- **UI state:** `hideStatusRemovalConfirmation` (bool), `statusRemovalCountKey` (int), `lastSelectedFilter` (the `FilterConfiguration` JSON).

These are UX conveniences; nothing user-*owned* depends on them (clearing them is safe — rider §6.2).

### 4.4 Merge / overwrite engine (`storage-schema.md §"Merge / overwrite policy"`)
A pure, unit-tested server module `mergeShow(existing, incoming)`:
- **Non-`my` fields:** `selectFirstNonEmpty(newValue, oldValue)` — never overwrite a non-empty string/array with empty, never overwrite non-nil with nil.
- **`my` fields (`my_tags`, `my_score`, `my_status`, `my_interest`):** resolve by update timestamp — newer wins; if only one side has a timestamp, keep it. This preserves user edits across both catalog refreshes and cloud sync merges.
- `details_update_date` = now after merge; `creation_date` set only on first create.
This one module underwrites re-adding (PRD §5.5), catalog refresh, and cross-device sync (§5.10).

### 4.5 Migrations & data continuity (PRD §5.11, rider §3.3)
- **Schema evolution:** Supabase SQL migrations (checked into `supabase/migrations/`) + optional seed/fixtures, so a fresh DB state is created deterministically.
- **Data-model versioning:** `app_metadata.data_model_version` (default 3). On boot, a `runDataMigrations()` step brings any existing saved shows + My Data forward into the new model **automatically and transparently** — users never lose collection/ratings/tags/statuses/interest/scoop on upgrade. Each version bump ships an idempotent forward migration with tests.

### 4.6 Sync & conflict resolution (PRD §5.10, §5.6)
- Optional cross-device sync keeps library + settings consistent.
- Per-field conflicts resolve by most-recent edit timestamp (the same `mergeShow` engine).
- Duplicate items (same `id` within `(namespace_id, user_id)`) are detected and merged transparently.
- `cloud_settings.version` (epoch seconds) resolves settings conflicts.

---

## 5. Backend / API design

All under `app/api/**` (Route Handlers) or Server Actions. Every handler: (1) resolves identity via `getIdentity`, (2) scopes to `(namespace_id, user_id)`, (3) validates payload with Zod, (4) returns overlaid data.

### 5.1 Collection & My Data
- `GET /api/shows` — list the user's collection (optionally filtered server-side); used by Home.
- `GET /api/shows/:id` — a single saved show (My Data overlay).
- `PATCH /api/shows/:id/my-data` — apply a My Data change (status, interest, tag add/remove, rating). Encapsulates **saving triggers & defaults** (§7.3 below) and stamps the correct per-field timestamp.
- `DELETE /api/shows/:id` — remove from collection (clears all My Data). Server enforces the semantics; the confirmation UX lives client-side.
- `POST /api/shows/import` (future) — restore from export zip (open question; §12).

### 5.2 Catalog (proxy + mapping)
Server routes wrap the `CatalogProvider` so the catalog API key stays server-side and responses are mapped into `Show` shape (`storage-schema.md §"External catalog → Show mapping"`):
- `GET /api/catalog/search?q=` — title/keyword search → poster grid.
- `GET /api/catalog/show/:id` — full detail (merges catalog into any stored show, overlays My Data, attaches transient cast/crew/seasons/videos/recommendations/similar).
- `GET /api/catalog/person/:id` — person profile + credits.
- `GET /api/catalog/resolve` — resolve `{title, externalId, mediaType}` → real `Show` (used by AI recommendation mapping, §8.5).
- `GET /api/catalog/providers/:id` — streaming availability (region-aware; store IDs, fetch provider metadata separately).

### 5.3 AI surfaces
- `POST /api/ai/scoop/:id` — **streamed** Scoop (SSE). Reads freshness (4h) and persistence rules (§8.3).
- `POST /api/ai/ask` — Ask turn; returns structured `{commentary, showList}`; server resolves `showList` → real shows for the mentioned-shows strip; handles summarization of older turns.
- `POST /api/ai/concepts` — single- or multi-show concept extraction.
- `POST /api/ai/recommend` — concept-based recs (Explore Similar = 5, Alchemy = 6); resolves to real shows carrying transient reasons.

### 5.4 Settings, export, test-reset
- `GET/PUT /api/settings` — cloud settings (username, model, keys).
- `GET /api/export` — build `.zip` (JSON of all saved shows + My Data, ISO-8601 dates).
- `POST /api/test/reset` — **namespace-scoped** destructive reset (delete rows where `namespace_id = env` and, optionally, `is_test = true`). Backs `npm run test:reset`. Gated to dev/test.

---

## 6. Frontend architecture (fractal, per `INSTRUCTIONS.md`)

**Pattern:** Pages contain Features contain Sub-Features, each self-contained (own `hooks/`, `utils/`, child `features/`). **Humble components** — TSX is markup + binding only; all logic in hooks (`const { data, handlers } = useX()`). **No magic numbers / inline styles** — constants in `config/` or local `constants.ts`; colors/spacing from `theme/` tokens only. Co-locate feature-only sub-features. Avoid `index.tsx` — main file matches directory name.

```
src/
├── config/            # env access, global constants (namespace, model defaults, caps)
├── theme/             # design tokens → Tailwind theme; font-size scale (XS…XXL)
├── components/        # shared primitives: ShowTile, PosterGrid, Chip, StatusChips, RatingBar, StrandRow, Badge…
├── hooks/             # global hooks (useIdentity, useCollectionQuery, useMediaTypeToggle)
├── utils/             # merge, filters, showList parser, date/ISO helpers
├── lib/               # server: supabase clients, catalog provider, ai provider, identity
└── pages/ (App Router: app/ + colocated feature dirs)
    ├── Home/                 # Collection Home
    │   └── features/{StatusSections, MediaTypeToggle, FiltersPanel, EmptyStates}
    ├── Detail/               # Show Detail (section order preserved — §7.5)
    │   └── features/{HeaderMedia, CoreFacts, MyRelationship(Status/Interest/Rating/Tags),
    │                  Overview+Scoop, AskAboutShow, Recommendations, ExploreSimilar,
    │                  Providers, CastCrew, Seasons, BudgetRevenue}
    ├── Find/                 # Discover hub (mode switcher)
    │   └── features/{Search, Ask, Alchemy}
    ├── Person/               # Person Detail
    │   └── features/{Gallery, Bio, Analytics, FilmographyByYear}
    └── Settings/
        └── features/{AppSettings, UserSettings, AiSettings, Integrations, YourData(Export)}
```

Global layout: a **Filters/navigation panel** (All Shows, tag filters, data filters) + a main content area, with **persistent Find/Discover and Settings** entry points in primary navigation (PRD §6).

---

## 7. Feature specifications (mapped to PRD)

### 7.1 Status, Interest & the "collection membership" rules
- **Statuses:** `active`, `later`, `wait`, `done`, `quit`, plus **hidden `next`** (in the data model, not surfaced as a first-class UI status — PRD §4.2).
- **Interest** (`interested`, `excited`) only applies when status is `later`. Changing away from Later makes interest irrelevant but may be retained for return to Later.
- **The nuance:** "Interested"/"Excited" surface as primary status chips, but selecting either sets `my_status=later` + `my_interest=<chosen>` (PRD §4.2). This is centralized in the My-Data handler so every entry point behaves identically.
- **Membership:** a show is "in collection" iff it has a non-nil `my_status` (PRD §5.1). Removing all status removes the show and clears all My Data.

### 7.2 Saving triggers & defaults (implicit-save, must feel natural — PRD §5.2/§5.3)
Any of these save an unsaved show:
- Setting any status.
- Choosing Interested/Excited.
- **Rating** an unsaved show → saves as **`done`** (rating implies watched).
- Adding ≥1 tag to an unsaved show → saves as **`later` + `interested`**.

Default when saved without explicit status: `later` + `interested`. These live in one place (`useMyData`/the PATCH handler) so Detail, Search results, and any tile share the behavior.

### 7.3 Removal semantics (PRD §5.4)
- Trigger: user re-selects the active status chip → confirm removal.
- Effect: delete the stored show; clear status/interest/tags/rating/scoop.
- Show a warning confirmation with an option to **stop asking after repeated removals** (`hideStatusRemovalConfirmation` + `statusRemovalCountKey` in UI state).

### 7.4 Collection Home (PRD §7.1)
- Shows matching active filter(s), grouped into status sections in order:
  1. **Active** (prominent / larger tiles),
  2. **Excited** (Later + Excited),
  3. **Interested** (Later + Interested),
  4. **Other** (collapsed): Wait, Quit, Done, and unclassified Later without interest.
- **Media-type toggle** at top: All / Movies / TV, applied on top of any filter.
- Tiles show poster, title, and **My Data badges** (in-collection + rating — PRD §5.9).
- Empty states: no collection → prompt to Search/Ask; filter empty → "No results found."

### 7.5 Filters (PRD §4.5)
Sidebar/menu views over the collection:
- **Quick/default:** All Shows.
- **Tag filters:** one per tag; plus **"No tags"** when tagless shows exist.
- **Data filters:** genre, decade, community-score ranges.
- **Media-type toggle** stacks on top of any filter.
- Persist `lastSelectedFilter` in UI state. (Explicit `myStatus` sidebar filters are an open extension — §12.)

### 7.6 Search (PRD §7.2, voice: none)
- Text search by title/keyword → poster grid; in-collection items marked; select → Detail.
- Auto-open on launch when `autoSearch` is enabled.
- **No AI voice** — plain catalog experience (`ai_voice_personality.md §1`).

### 7.7 Show Detail (section order preserved — `detail_page_experience.md §3`)
Order (rebuild must preserve unless intentionally changed):
1. Header media carousel (backdrops/posters/logos/trailers; graceful poster/logo fallback; motion prioritized but never blocks reading).
2. Core facts (year, runtime **or** seasons/episodes) + community-score bar.
3. Tag chips (My Tags).
4. Overview + **Scoop** toggle/stream.
5. "Ask about this show" CTA.
6. Genres + languages.
7. Recommendations strand (traditional similar/recommended).
8. Explore Similar (concepts → recs).
9. Providers ("Stream It").
10. Cast, Crew (strands → Person Detail).
11. Seasons (TV only).
12. Budget/Revenue (movies where available).

**Relationship controls in the toolbar** (not the scroll body): status/interest chips, rating bar, tags. Auto-save rules from §7.2 apply. Destructive removal only behind confirmation. Critical states handled: unsaved show (Scoop generatable but persists only on save), no trailers/backdrops (premium poster/logo layout), TV-vs-movie gating (seasons only for TV, financials only for movies).

### 7.8 Person Detail (PRD §7.6)
- Image gallery, name, bio.
- Analytics charts: average project ratings, top genres, projects-by-year.
- Filmography grouped by year; selecting a credit opens that show's Detail.

### 7.9 Settings & Your Data (PRD §7.7)
- **App:** font size (drives `theme/` scale), search on launch.
- **User:** username (synced).
- **AI:** provider API key (env-provided in benchmark mode; never committed), model selection (synced).
- **Integrations:** catalog provider API key (synced).
- **Your data:** **Export/Backup** → `.zip` of JSON (all saved shows + My Data, ISO-8601 dates). Import/Restore is desired but an open question (§12).

---

## 8. The AI layer (voice, contracts, quality)

The AI is the product's "heart." All surfaces share **one persona** — a warm, opinionated, spoiler-safe "fun TV/movie nerd friend" (`ai_voice_personality.md`). Search never has AI voice.

### 8.1 Provider abstraction
`AiProvider` interface (methods: `streamScoop`, `ask`, `extractConcepts`, `recommend`, `summarizeTurns`) with an **Anthropic adapter** as the concrete impl. Model selectable in Settings; default `claude-opus-4-8`. A shared **persona/system prefix** is cached (prompt caching) so per-surface prompts only append their mode-specific instructions and inputs.

### 8.2 Shared rules & inputs (`ai_prompting_context.md §1–2`)
- Stay in TV/movies (redirect if asked to leave); spoiler-safe by default; opinionated + honest (acknowledge mixed reception, don't gush); prefer specific vibe/structure/craft reasoning over genre boilerplate; outputs actionable (titles resolve to real items).
- Surface-appropriate context: the user's library + My Data, current show context, selected concepts, recent conversation turns (older ones summarized).

### 8.3 Scoop (`ai_voice_personality.md §4.1`, `detail_page_experience.md §3.4`)
- Structured mini-blog-of-taste: personal take → honest stack-up vs reviews → the **Scoop** centerpiece paragraph → fit/warnings → "Worth it?" verdict. ~150–350 words, Scoop paragraph largest.
- **Streams progressively** ("Generating…", never a blank wait).
- Toggle copy changes by state: none → "Give me the scoop!"; cached → "Show the scoop"; open → title "The Scoop".
- **Freshness 4h**; regenerate on demand after expiry. **Persist only if the show is in collection**; otherwise ephemeral (PRD §4.9, §5.7).

### 8.4 Ask (`product_prd.md §7.3`, `ai_prompting_context.md §3.1–3.2`, §4)
- Chat UI, friend-in-dialogue tone, 1–3 tight paragraphs then a bulleted list for multi-recs; confident picks; direct answer in the first few lines (`discovery_quality_bar.md §2.2`).
- **Mentioned-shows contract (must match exactly):** structured object `{ commentary, showList }` where `showList` is `Title::externalId::mediaType;;Title2::externalId::mediaType;;…` (no external IDs inside `commentary`). Implemented via structured outputs; a dedicated `parseShowList` util is the single source of truth for the format, with a **retry-once** on malformed output, then fallback to unstructured commentary + Search handoff (`§5`).
- **Mentioned-shows strip:** parsed `showList` → resolve to real shows (§8.5) → horizontal strip; tapping opens Detail or hands off to Search on mapping failure.
- **Welcome view:** 6 random starter prompts (from the 80-prompt set), with refresh.
- **Summarization:** after ~10 messages, older turns are summarized into 1–2 sentences **in the same persona/tone** (no sterile system voice) to control token depth (`ai_prompting_context.md §4`).
- **Ask about a show:** launched from Detail seeds the conversation with that show's context (handoff show).
- Session-only: chat history + mentioned-shows strip are cleared on reset/leave (PRD §5.7).

### 8.5 Concepts, Explore Similar & Alchemy (`concept_system.md`, `ai_prompting_context.md §3.4–3.5`)
- **Concepts:** bullet list only; each 1–3 words; evocative, spoiler-free; avoid generic ("good characters"); **ordered by strongest "aha" first**; varied across axes (structure/tone/emotion/relationship/craft). **8 by default** (`discovery_quality_bar.md §2.3`). Multi-show concepts must be **shared across all inputs** and drawn from a **larger option pool** (`concept_system.md §8`).
- **Selection UX:** chips; require ≥1 concept; cap selection at **8**; changing inputs/selection **clears downstream results** (PRD §7.4).
- **Recommendations:** each rec names which concept(s) it matches, with a concise 1–3 sentence reason (not a synopsis); recent bias but classics/hidden gems allowed; **Explore Similar = 5 recs**, **Alchemy = 6 recs** (`concept_system.md §6`).
- **Alchemy flow:** select 2+ shows (library + global) → **Conceptualize** → select catalysts (max 8) → **Alchemize** → review → **More Alchemy!** chains results as new inputs. Backtracking clears concepts/results. Alchemy results/reasons are session-only.
- **AI→real-show resolution (PRD §5.8):** AI outputs `title + externalId(if available) + mediaType`; look up the catalog by `externalId`, accept the first result whose title matches **case-insensitively**; if found → real selectable Show carrying the AI reason as transient text; else show non-interactive or hand off to Search (`ai_prompting_context.md §5`). This is the same `catalog/resolve` path used by Ask.

### 8.6 Quality bar (`discovery_quality_bar.md`)
Bake the acceptance rubric into review/eval fixtures: **Voice ≥1, Taste alignment ≥1, Real-show integrity = 2 (non-negotiable), total ≥7/10.** Surface-specific minimums (Scoop sections present + honest; Ask direct + bulleted; Concepts = 8 evocative; Explore/Alchemy = 5/6 with per-rec concept citation). Real-show integrity is enforced structurally by §8.5, not left to the model.

---

## 9. Catalog provider abstraction (TMDB adapter)

`CatalogProvider` interface (`search`, `getShow`, `getPerson`, `getProviders`, `resolveByExternalId`) with a TMDB adapter implementing the mapping rules from `storage-schema.md`:
- IDs → `id`/`external_ids`; title prefers movie title / TV name (fail if neither); media-type from catalog else inferred (`name`→tv, `title`→movie, else reject).
- Genre ids → display names (stored as `string[]`).
- Multi-format date parsing; ratings/popularity stored directly; movie runtime/budget/revenue and TV series-status/episode/season counts when present.
- Images mapped to renderable URLs; when multiple logos exist, pick a single "best" deterministically (prefer English).
- Providers: store IDs only, by region.
- Transient (`credits`, `seasons`, `videos`, `recommendations`, `similar`, `images.*`) attached for UI, never persisted.

Keeping this behind an interface satisfies the PRD's "vendor-specific specs out of scope" while letting the schema stay concrete.

---

## 10. Repo deliverables & developer experience (rider §3, §8)

- **`.env.example`** listing every required var with short comments: `NAMESPACE_ID`, `DEFAULT_USER_ID`, `APP_MODE`, `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY` (server-only), `ANTHROPIC_API_KEY`, `AI_MODEL` (default `claude-opus-4-8`), `TMDB_API_KEY`. Build runs by filling env — **no source edits** (rider §3.1).
- **`.gitignore`** excludes `.env*` except `.env.example`; browser code uses only the anon key; service role is server-only (rider §3.1).
- **Scripts** (rider §3.2): `npm run dev` (start), `npm test` (unit + E2E), `npm run test:reset` (namespace-scoped reset via §5.4). Plus `supabase db push` / migration + seed scripts (rider §3.3).
- **No Docker required** (rider §8): the primary path connects to a **hosted** Supabase instance and relies on namespace isolation; local Supabase (Docker) is optional and documented as such.
- A short `README` documents the dev identity-injection mechanism and how it's prod-gated (rider §5.1).

---

## 11. Testing strategy (`INSTRUCTIONS.md`, rider §7)

- **Unit (Vitest):** the highest-leverage pure logic — `mergeShow` (all overwrite/timestamp branches), saving-triggers/defaults, removal semantics, filter grouping (Active/Excited/Interested/Other), `parseShowList` (round-trip + malformed), concept caps, AI→real-show resolution, ISO-8601 export encoding, data-model migrations. Tests co-located with source.
- **Visual/E2E (Playwright):** the 10 key journeys (PRD §9) — build collection, rate-to-save (→Done), tag-to-save (→Later+Interested), maintain, tag-driven filters, Ask discovery, Explore Similar, Alchemy chaining, talent deep-dive, backup/export.
- **Destructive tests** create data inside the namespace (mark `is_test = true`) and reset via `POST /api/test/reset` — **no global teardown** (rider §7).
- **AI quality:** golden-set fixtures scored against `discovery_quality_bar.md`; real-show integrity is a hard gate.
- **Lint-clean, token-only styling** enforced in CI.

---

## 12. Sequencing (milestones)

1. **Foundations & isolation.** Next.js + Supabase wiring; env interface + `.env.example`/`.gitignore`; `getIdentity` + `(namespace_id, user_id)` scoping + RLS; `shows`/`cloud_settings`/`app_metadata` schema + migrations/seed; `test:reset`; theme tokens + fractal skeleton. *(Rider §2–8; PRD §8.7–8.9.)*
2. **Collection core.** `mergeShow`; My-Data handler with all saving triggers/defaults/removal; Home grouping + media toggle + tile badges; Filters + persisted `lastSelectedFilter`; empty states. *(PRD §4–5, §7.1.)*
3. **Catalog + Detail + Search.** CatalogProvider (TMDB adapter) + mapping/merge on refresh; Search (no AI voice); full Detail in the specified section order with toolbar relationship controls; Person Detail. *(PRD §7.2, §7.5, §7.6; storage-schema mapping.)*
4. **AI layer.** Provider abstraction + persona prefix; Scoop (stream + 4h freshness + save-gated persistence); Ask (structured `commentary/showList`, mentioned-shows strip, 6 starters, summarization, ask-about-show seeding, retry/fallback); Concepts + Explore Similar (5) + Alchemy (6) with resolution to real shows. *(PRD §7.3–7.4, §4.9, §5.7–5.8; AI docs.)*
5. **Settings, export, sync, continuity.** Settings (font size, search-on-launch, username, model, keys); Export `.zip`; optional cross-device sync (per-field newest-wins, dup merge); data-model migrations for continuity across versions. *(PRD §7.7, §5.10–5.11.)*
6. **Hardening.** Quality-bar golden set; full journey E2E; accessibility/readability (font-size scale); prod-mode gating of dev auth; OAuth wiring stub proving "no schema redesign."

---

## 13. Open questions / optional extensions (PRD §10, §12; supporting docs)

Tracked but out of the committed scope; each maps to an existing model affordance so it can be added without redesign:
- Promote hidden **`next`** to a first-class UI status (model already supports it).
- **Named custom lists** beyond tags.
- Should generating a **Scoop on an unsaved show** implicitly save it? (Current rule: persist only if saved.)
- Explicit **Unrated** state vs nil for cleared ratings.
- **Import/Restore** from the export zip (Settings mentions it; UI missing — `POST /api/shows/import` is stubbed).
- Save/share **Alchemy sessions** as reusable "blends."
- Explicit **`myStatus` sidebar filters** (model supports it).
- Inline trailer playback and a one-line "why concepts matter" explainer under Get Concepts (`detail_page_experience.md §6`).

---

## 14. How this plan honors each source document

- **`product_prd.md`** — every core object, business rule (implicit saves, defaults, removal, re-add merge, timestamps, AI persistence, tile indicators, sync, continuity), the four discovery paths, navigation, all major features, and the cross-cutting principles are covered in §3–§9 and §12–§13.
- **`infra_rider_prd.md`** — Next.js + Supabase, `.env.example`/gitignore/no-code-edit config, one-command scripts, migrations, namespace + user isolation, dev identity injection prod-gated, OAuth-without-redesign, backend-as-truth, disposable cache, namespace-scoped destructive tests, no-Docker cloud path — §2, §3, §5, §10, §11.
- **`storage-schema.{md,ts}`** — the `shows`/`cloud_settings`/`app_metadata` model, transient-vs-stored split, provider-IDs-only, local/UI key-value settings, catalog→Show mapping, and the merge/overwrite policy — §4, §9.
- **`ai_prompting_context.md`, `ai_voice_personality.md`, `concept_system.md`, `discovery_quality_bar.md`, `detail_page_experience.md`** — one persona, per-surface contracts, the exact `showList` format, summarization tone, concept generation/selection rules and counts (8 / 5 / 6), the Scoop structure/freshness/persistence, Detail section order and states, and the acceptance rubric — §7.7, §8.
- **`INSTRUCTIONS.md`** — fractal Pages→Features→Sub-Features, humble components, no magic numbers/inline styles (theme tokens), co-location, lint-clean, unit tests for critical logic, visual testing — §2, §6, §11.
