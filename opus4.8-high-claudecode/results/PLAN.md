# Implementation Plan — Personal TV & Movie Companion

This plan is the deliverable for the planning step. It does **not** implement anything; it
describes *what to build* and *how the pieces fit together* so that a follow-on build can be
executed deterministically and scored against the PRD rubric.

Sources synthesized: `docs/prd/product_prd.md`, `docs/prd/infra_rider_prd.md`, and every file in
`docs/prd/supporting_docs/` (`ai_prompting_context.md`, `ai_voice_personality.md`,
`concept_system.md`, `detail_page_experience.md`, `discovery_quality_bar.md`,
`technical_docs/storage-schema.md`, `technical_docs/storage-schema.ts`), plus the repo's
`INSTRUCTIONS.md` architecture standards.

> Note on companion docs: `product_prd.md` §12 references `where_is_the_heart_opus.md`,
> `ai_personality_opus.md`, and `philosophy_opus.md`. These files are **not present** in the repo.
> Where they would have informed voice/craft decisions, this plan relies on
> `ai_voice_personality.md`, `ai_prompting_context.md`, and `concept_system.md`, which cover the
> same ground. If those companion docs surface later, revisit the AI-voice sections.

---

## 0. Executive Summary

We are building a personal TV + movie companion: a user curates *their version* of each show
(status, interest, tags, rating, AI "Scoop"), and that taste profile powers four discovery paths —
Search, conversational **Ask**, **Alchemy** (concept blending), and per-show **Explore Similar**.

**Mandated baseline (Infra Rider §2):** Next.js (latest stable, App Router) as the UI + server
boundary, and Supabase (Postgres) as the persistence layer via official client libraries. No Docker
required. Everything runs by filling in env vars — no source edits.

**Core architectural stance:**
- **Backend is the source of truth** (Cross-Cutting Rule §8.9, Rider §6). All user-owned data lives
  in Supabase. Clients may cache for speed, but clearing client storage must never lose data.
- **All persisted user data is partitioned by `(namespace_id, user_id)`** (Rider §4). `namespace_id`
  isolates benchmark runs; `user_id` scopes ownership even in single-user mode.
- **User data access is server-mediated.** Browser code holds only the Supabase anon key; every
  read/write of user data goes through Next.js Route Handlers / Server Actions that use a
  server-only client and always scope queries by `(namespace_id, user_id)`. This is what makes
  dev-identity injection today and OAuth later a *config swap, not a schema redesign* (Rider §5.2).
- **User overlay always wins** over refreshed public catalog data (Product §4.1 display rule;
  merge rules in storage-schema).
- **One consistent AI persona** across Scoop / Ask / Alchemy / Explore Similar; Search has no AI
  voice.

**Suggested phasing** (detail in §14): (1) Foundations/infra, (2) Data model + collection CRUD +
save rules, (3) Collection Home + filters, (4) Search + Detail, (5) AI surfaces, (6) Person + charts,
(7) Settings + export + sync, (8) Testing/reset/migrations hardening.

---

## 1. Technology & Dependency Choices

| Concern | Choice | Rationale |
|---|---|---|
| App runtime | **Next.js latest stable, App Router** | Rider §2 mandate; server routes give us the server boundary for identity + secret handling. |
| Language | **TypeScript** | Matches the reference schema and enables typed contracts across client/server. |
| Persistence | **Supabase (Postgres)** via `@supabase/supabase-js` (+ `@supabase/ssr` for server helpers) | Rider §2 mandate; official client libraries required. |
| Schema evolution | **Supabase SQL migrations** in `supabase/migrations/`, optional seed fixtures | Rider §3.3 "repeatable schema definition; fresh state deterministically." |
| Data fetching/cache (client) | **TanStack Query** | Disposable client cache over server-of-truth; satisfies "cache is disposable" (Rider §6.2). |
| Styling / theme | Token-based system (CSS variables or a utility framework driven by `src/theme/` tokens) | INSTRUCTIONS.md: "no hex/px in TSX, reference theme tokens only." |
| External catalog | Provider-agnostic **catalog adapter** (TMDB-style is the reference shape) | PRD is vendor-agnostic; storage-schema fields (voteAverage, providerData, genres-by-name) map cleanly to a TMDB-shaped provider. |
| AI provider | **Anthropic Claude** as default provider, model selectable (Settings) | Build AI features on the latest, most capable Claude models; provider/model are configurable per PRD §7.7. Structured outputs used for mentions/concepts/recs. |
| Validation | **Zod** | Validate AI structured outputs and API payloads; enables the "retry once, then fall back" contract. |
| ZIP export | A JS zip library (e.g. `jszip`) | Export My Data `.zip` (PRD §7.7). |
| Testing | **Vitest** (unit) + **Playwright** (e2e/visual) | INSTRUCTIONS.md: unit tests for critical logic, visual testing preferred. Destructive e2e scoped to a namespace. |

**Model note:** default to the latest Claude models (e.g. Opus / Sonnet / Haiku 4.x tiers) via the
Anthropic SDK; expose model selection in Settings (`CloudSettings.aiModel`). Never commit keys.

---

## 2. Project Structure (Fractal Architecture)

Per `INSTRUCTIONS.md`: Pages → Features → Sub-Features, each self-contained (own `hooks/`, `utils/`,
child `features/`). Humble components (TSX = markup + binding only; logic in hooks). Avoid
`index.tsx` — main file matches directory name.

```
/
├── .env.example                 # all required vars, names + comments (Rider §3.1)
├── .gitignore                   # excludes .env* except .env.example
├── package.json                 # scripts: dev, build, test, test:e2e, db:migrate, test:reset, seed
├── next.config.*
├── supabase/
│   ├── migrations/              # ordered SQL migrations (schema evolution, Rider §3.3)
│   └── seed/                    # optional deterministic fixtures
├── scripts/
│   ├── reset-namespace.ts       # delete/reset all data for NAMESPACE_ID (Rider §7)
│   └── seed-namespace.ts        # create test data inside a namespace
├── src/
│   ├── config/                  # env parsing, global constants, feature counts (see §11)
│   ├── theme/                   # design tokens (colors, spacing, type scale incl. font-size steps)
│   ├── components/              # shared primitives: ShowTile, PosterGrid, Chip, StatusChips,
│   │                            #   RatingBar, TagPicker, ConceptChip, Carousel, EmptyState, Charts
│   ├── hooks/                   # global hooks (useIdentity, useMediaTypeToggle, useFontSize)
│   ├── utils/                   # global pure fns (mergeShow, saveRules, dateParse, showListParse)
│   ├── lib/
│   │   ├── supabase/            # server client (service role) + browser client (anon)
│   │   ├── identity/            # resolveIdentity(): namespace_id + user_id (dev injection)
│   │   ├── catalog/             # external catalog adapter (search, detail, credits, providers)
│   │   ├── ai/                  # provider client, prompt builders, output parsers/validators
│   │   └── mapping/             # catalog payload → Show; merge policy (selectFirstNonEmpty, ts)
│   ├── app/                     # Next.js App Router
│   │   ├── (routes)/            # home, detail/[id], find, person/[id], settings
│   │   └── api/                 # Route Handlers: /collection, /search, /catalog, /ai/*, /export, /sync
│   └── pages/                   # (fractal UI trees per INSTRUCTIONS.md; see §5)
│       ├── Home/
│       ├── Detail/
│       ├── Find/                # Search | Ask | Alchemy modes
│       ├── Person/
│       └── Settings/
└── tests/                       # e2e/visual specs (namespace-scoped)
```

> App Router route files (`app/`) stay thin and delegate into the fractal `pages/*` feature trees,
> keeping route wiring separate from feature logic.

---

## 3. Identity, Isolation & Auth Model (Infra Rider §4–5)

This is a correctness-critical, cross-cutting concern; build it first.

### 3.1 Partition keys
- **`namespace_id`** — one stable value per build/run, read from env (`NAMESPACE_ID` / `RUN_ID` /
  `BUILD_ID`; pick one canonical name, accept aliases). A **build-isolation primitive, not a user
  concept.** Every persisted row carries a `namespace_id` column.
- **`user_id`** — opaque stable string/UUID. Every user-owned row carries `user_id`. System behaves
  as if multiple users can exist even though the UI exposes one.
- **Effective partition = `(namespace_id, user_id)`** for all user-owned data.

### 3.2 Identity resolution (dev injection now, OAuth later)
Implement `resolveIdentity(request)` in `src/lib/identity/`:
1. `namespace_id` from server env (fixed for the process lifetime).
2. `user_id` resolution order (dev/test mode): `X-User-Id` request header → dev "login as" selector
   value → fixed **default user** for the namespace.
3. Production mode: same function, but `user_id` comes from a real auth session (OAuth). Because
   every route already calls `resolveIdentity()` and scopes by it, switching to OAuth is
   **config + auth wiring, not a schema change** (Rider §5.2). Dev injection must be **gated/disabled
   in production mode** and clearly documented.

### 3.3 Enforcement strategy
- **Server-mediated data access.** User data is only read/written through Next.js server routes /
  server actions using a **server-only Supabase client (service role key)** that *always* injects
  `namespace_id` and the resolved `user_id` into every query. The browser never queries user tables
  directly.
- Browser Supabase client uses the **anon/public key only** (Rider §3.1 credential rule).
- **RLS as defense-in-depth:** enable Row Level Security on all user tables. Since the primary path
  is service-role-behind-server-routes, RLS policies act as a backstop; document that correctness is
  enforced at the server route layer (so a future move to direct-from-browser + JWT auth only
  requires turning the policies "on" against `auth.uid()`).

### 3.4 Reset & destructive testing (Rider §7)
- `scripts/reset-namespace.ts` deletes/resets **only** rows where `namespace_id = $NAMESPACE_ID`
  (optionally further limited to `is_test = true`). No global teardown ever required.
- Test data is created inside the namespace and torn down by namespace. `isTest`/`is_test` flag
  (from schema) marks synthetic data for targeted cleanup.

---

## 4. Data Model & Persistence (from storage-schema.md/.ts)

### 4.1 Tables (Postgres, all user tables carry `namespace_id` + `user_id`)

**`shows`** — the merged catalog-item + user-overlay record (mirrors the `Show` interface). One row
per `(namespace_id, user_id, id)`.
- Identity: `id` (PK component, stable catalog id), `title`, `show_type`
  (`movie|tv|person|unknown`), `external_ids` (jsonb).
- Catalog meta: `overview`, `genres` (text[] of **names**, not ids), `tagline`, `homepage`,
  `original_language`, `spoken_languages` (text[]), `languages` (text[]).
- Images: `poster_url`, `backdrop_url`, `logo_url`, `network_logos` (text[]).
- Ratings/popularity: `vote_average`, `vote_count`, `popularity`.
- Dates: `last_air_date`, `first_air_date`, `release_date`.
- Movie: `runtime`, `budget`, `revenue`.
- TV: `series_status`, `number_of_episodes`, `number_of_seasons`, `episode_run_time` (int[]),
  `last_episode_run_time`.
- **My data (user overlay):** `my_tags` (text[]) + `my_tags_update_date`; `my_score` +
  `my_score_update_date`; `my_status` (`active|next|later|done|quit|wait`) + `my_status_update_date`;
  `my_interest` (`excited|interested`) + `my_interest_update_date`.
- AI: `ai_scoop` + `ai_scoop_update_date`.
- Management: `details_update_date`, `creation_date`, `is_test` (default false).
- Providers: `provider_data` (jsonb) — **IDs only**, region-keyed (`ProviderData` shape).
- **PK:** `(namespace_id, user_id, id)`. Indexes: on `my_status`, `my_score` (badges/sorting),
  GIN on `my_tags` (tag filters), `genres` (data filters), and `*_update_date` (recently-updated
  sorting + conflict resolution).

**`cloud_settings`** — synced app settings (per user). `id` default `"globalSettings"`, `user_name`,
`version` (epoch seconds, used for conflict resolution), `catalog_api_key?`, `ai_api_key?`,
`ai_model`. Scoped by `(namespace_id, user_id)`.

**`app_metadata`** — `data_model_version` (int, default 3). Drives migrations / data continuity
(§4.4). Scoped per namespace (and per user if needed for user-model upgrades).

**Client-only (NOT server):** `LocalSettings` (`autoSearch`, `fontSize`) and `UserDefaultsUIState`
(`hideStatusRemovalConfirmation`, `statusRemovalCountKey`, `lastSelectedFilter`) live in browser
storage (localStorage). These are device-local preferences, not user-owned durable data — clearing
them is acceptable and must not affect collection data.

**Transient (never persisted):** `cast`, `crew`, `seasons`, `images.*`, `videos`, `recommendations`,
`similar`, `lastEpisodeToAir`, `aiDescription`, tile UI state. Fetched live from the catalog for UI.

### 4.2 External-catalog → Show mapping (`src/lib/mapping/`)
Implement the documented flow:
1. Decode external payload into a fresh `Show` (title from movie title or TV name; if neither →
   decode fails; infer `show_type` from media type, else name→tv / title→movie / else reject).
2. Map genre ids → **names**; parse dates with multiple accepted formats; store community metrics +
   popularity; movie runtime/budget/revenue; TV series-status/episode/season counts; images →
   renderable URLs with a **deterministic "best logo"** rule (prefer English/highest-rated); spoken
   languages; provider availability by region (**IDs only**).
3. If a stored show with the same `id` exists, **merge** (§4.3), else create.

### 4.3 Merge / overwrite policy (correctness-critical)
- **Non-`my` fields:** `selectFirstNonEmpty(newValue, oldValue)` — never overwrite a non-empty
  stored string/array with empty; never overwrite non-nil with nil. (Catalog refresh must not erase
  data.)
- **`my` fields** (`my_tags`, `my_score`, `my_status`, `my_interest`): resolve by update timestamp —
  newer wins; if only one side has a timestamp, keep that side. Preserves user edits across catalog
  refreshes **and** cross-device sync merges.
- `details_update_date` = now after merge; `creation_date` set only on first creation.
- This single merge function backs three flows: catalog refresh, re-encountering a saved show
  (§5.5), and cross-device sync conflict resolution (§5.10). Build it once, unit-test it hard.

### 4.4 Data continuity across versions (Product §5.11)
- `app_metadata.data_model_version` tracks the model version. On startup, if stored version <
  current, run **forward data migrations** that bring existing shows + My Data into the new model
  transparently — users never lose collection/ratings/tags/statuses/interest/scoop.
- Two migration surfaces: (a) **DB schema** migrations in `supabase/migrations/`; (b) **data-shape**
  migrations keyed off `data_model_version`. Both must be idempotent and namespace-safe.

---

## 5. Feature Specifications (UI Pages & Features)

Navigation (Product §6): Filters/nav panel (All Shows, tag filters, data filters) + main content
(Home, Detail, Find/Discover, Person, Settings). Persistent Find and Settings entry points. A
media-type toggle (All/Movies/TV) applies on top of any filter.

### 5.1 Collection Home (`pages/Home`)
- **Filters panel feature:** All Shows (default); one filter per tag + "No tags" if any tagless
  shows; data filters (genre, decade, community-score ranges); media-type toggle. Persist last
  selected filter to `lastSelectedFilter` (client UI state).
- **Grouped library feature** — status sections in this order:
  1. **Active** (prominent / larger tiles)
  2. **Excited** (Later + Excited)
  3. **Interested** (Later + Interested)
  4. **Other** (collapsed): Wait, Quit, Done, and Later items without interest.
- **Tiles** (`components/ShowTile`): poster, title, **in-collection badge** (has `my_status`),
  **user-rating badge** (has `my_score`).
- **Empty states:** empty collection → prompt to Search/Ask; filter yields none → "No results found."

### 5.2 Find / Discover hub (`pages/Find`)
A mode switcher over three modes:

**Search** (`features/Search`) — no AI voice.
- Text search of external catalog → poster grid; in-collection items marked; selecting opens Detail.
- Honor **Search on Launch** setting (auto-open Search when `autoSearch` is true).

**Ask** (`features/Ask`) — conversational discovery.
- Chat UI (user/assistant turns). Welcome view shows **6 random starter prompts** (refreshable) drawn
  from a starter-prompt set. (The PRD references "80 starter prompts" in the missing companion doc;
  seed a curated list in `config/` and expose 6 at random — sized so it's easy to expand to 80.)
- AI may mention shows inline → parsed into a **"mentioned shows" strip**; tapping a mention opens
  Detail (or hands off to Search if mapping fails).
- **Session context** retained; after ~10 messages, older turns **summarized** (persona-preserving).
- **Two entry variants:** General Ask (from Find) and **Ask About a Show** (from Detail CTA) — seed
  the conversation with the show's context on entry.
- Persistence: **session-only** — chat history + mentioned strip cleared on reset/leave (§5.7).

**Alchemy** (`features/Alchemy`) — structured blending.
- Flow: select **≥2** starting shows (library + global catalog) → **Conceptualize Shows** → select
  concept catalysts (**cap 8**) → **ALCHEMIZE!** → **6 recommendations** with short reasons →
  optional **More Alchemy!** to chain (results become new inputs).
- Backtracking: changing shows clears concepts + results; changing concept selection clears
  downstream results.
- Persistence: results/reasons **session-only**, cleared on leaving Alchemy (§5.7).

### 5.3 Show Detail (`pages/Detail`) — single source of truth
Preserve the documented narrative order (Detail-page spec §3):
1. Header media carousel (backdrops/posters/logos/trailers; graceful fallback to poster/logo; motion
   preferred but never blocks reading).
2. Core facts (year, runtime **or** seasons/episodes) + community score bar.
3. **My Tags** chips + picker.
4. Overview + **Scoop** toggle/stream.
5. **Ask about this show** CTA (seeds Ask with this show).
6. Genres + languages.
7. Traditional **Recommendations** strand (similar/recommended; low-effort next steps).
8. **Explore Similar**: Get Concepts → select 1+ → **Explore Shows** → **5 recs**.
9. Streaming providers ("Stream It").
10. Cast, Crew (horizontal strands → Person Detail).
11. Seasons (TV only).
12. Budget vs Revenue (movies, when available).

**Toolbar (not in scroll body):** Status/Interest chips + Rating bar. Chips shown:
Active / Interested / Excited / Done / Quit / Wait. Save/auto-save rules per §6. Reselecting the
active status → removal confirmation (§6.4). Scoop toggle copy: no scoop → "Give me the scoop!";
cached → "Show the scoop"; open → title "The Scoop". Scoop streams progressively ("Generating…",
never a blank wait).

Critical states: unsaved show (Scoop generatable but persists only on save; status/rating/tag
trigger auto-save), no trailers/backdrops (premium poster/logo layout), TV vs movie (seasons only
when relevant; runtime vs episode counts handled gracefully).

### 5.4 Person Detail (`pages/Person`)
- Image gallery, name, bio.
- **Analytics charts** (`components/Charts`): average project ratings, top genres, projects-by-year.
- Filmography grouped by year; selecting a credit opens that show's Detail.
- (Person is fetched/transient catalog data; `show_type` includes `"person"` in the model.)

### 5.5 Settings (`pages/Settings`)
- **App:** font size (`XS…XXL`, drives `theme` type scale), Search on Launch (`autoSearch`).
- **User:** username (synced if enabled).
- **AI:** provider API key (benchmark: may come from env; user-entered key optional and never
  committed), model selection (synced).
- **Integrations:** catalog provider API key (synced).
- **Your data:** **Export / Backup** — "Export My Data" → `.zip` containing a JSON backup of all
  saved shows + My Data, dates **ISO-8601**. **Import / Restore** — not currently implemented
  (Open Question §10); plan the export format to be import-friendly.

---

## 6. Business Rules — Save / Default / Remove / Merge (Product §5)

These are the highest-risk correctness rules; centralize them in `utils/saveRules` + server route
enforcement and unit-test exhaustively.

- **Collection membership (§5.1):** a show is "in collection" iff it has a non-nil `my_status`.
- **Saving triggers (§5.2):** any of — setting any status; choosing an interest chip
  (Interested/Excited → sets `my_status=later` + corresponding `my_interest`); rating an unsaved
  show; adding ≥1 tag to an unsaved show.
- **Defaults when saving without explicit status (§5.3):** status `later`, interest `interested`.
  **Exception:** first save **via rating** defaults status to **`done`** (rating implies watched).
  First save **via tag** defaults to `later + interested`.
- **Removal (§5.4):** user clears status (reselect active status + confirm) → remove show from
  storage; clear ALL My Data (status, interest, tags, rating, scoop). Show warning confirmation with
  an option to stop asking after repeated removals (`hideStatusRemovalConfirmation`,
  `statusRemovalCountKey`).
- **Interest semantics (§4.3):** interest only meaningful when status is `later`; if status leaves
  `later`, interest becomes irrelevant (may be retained for when it returns to `later`).
- **Re-adding a saved show (§5.5):** preserve latest My Data; refresh public metadata; resolve
  conflicts by most-recent per-field timestamp (same merge fn as §4.3).
- **Timestamps (§5.6):** every My field updates its `*_update_date` on change → used for sorting,
  cloud conflict resolution, and AI cache freshness.
- **Tile indicators (§5.9):** in-collection badge + user-rating badge.

---

## 7. AI Surfaces — Behavioral Contracts (ai_prompting_context.md, ai_voice_personality.md, concept_system.md, discovery_quality_bar.md)

All AI logic lives in `src/lib/ai/` and executes **server-side** (keys are server-held). One
consistent persona across surfaces; **Search has no AI voice**.

### 7.1 Shared rules
- Stay within TV/movies (redirect back if asked to leave the domain).
- **Spoiler-safe by default** unless the user explicitly asks for spoilers.
- Opinionated + honest (acknowledge mixed reception; don't gush for no reason).
- Specific, vibe/structure/craft reasoning over generic genre summaries; **every listed show gets a
  reason**; recommendations **resolve to real catalog items** when possible.
- **Persona (voice spec):** "fun, chatty TV/movie nerd friend" — joy-forward/warm, opinionated
  honesty, vibe-first/spoiler-safe, specific-not-generic, short-when-needed/lush-when-earned. Tone
  sliders: 70/30 friend/critic, 60/40 hype/measured, playfulness adaptive to the show, concise by
  default (lyrical for Scoop).

### 7.2 Shared inputs (taste-aware)
Depending on surface: user library + My Data; current show context (Ask-about / Scoop); selected
concepts (Explore Similar / Alchemy); recent conversation turns (chat), older turns summarized.

### 7.3 Surface contracts

**Ask (chat):** respond like a friend in dialogue (not an essay) unless depth is asked; willing to
pick favorites; simple formatting + bulleted lists when recommending multiple. Direct answer within
first 3–5 lines (quality bar).

**Ask with mentions (structured):** output a structured object:
- `commentary`: user-facing text, **no external IDs inline**.
- `showList`: machine-readable, **exact format**
  `Title::externalId::mediaType;;Title2::externalId::mediaType;;...`
- Parser and format must match exactly (build parser + generator together;
  `utils/showListParse` with round-trip unit tests). `externalId` resolves the show in the catalog.

**Explore Search Chat (showman mode):** mirrors the show's emotion (funny for comedies, serious for
dramas), may drop light insider context (cancellations/reception), stays in-domain, short enough to
scan in one screen.

**Scoop (Detail):** structured "mini blog post of taste": personal take (make a stand), honest
stack-up vs reviews, **the "Scoop" paragraph as emotional centerpiece** (most real estate), practical
fit/warnings, "Worth it?" verdict. Target ~150–350 words. **Streams progressively** if UI supports.
Freshness **4 hours**; regenerate on demand after expiry. **Persists only if the show is in
collection.**

**Concepts (single + multi-show):** bullet list only; **8 by default** (quality bar §2.3); each
**1–3 words**, evocative, spoiler-free, no explanation; avoid generic ("good characters"); cover
different axes (structure/vibe/emotion/relationship/craft) not 8 synonyms; **order by strength**. For
**multi-show (Alchemy)**, concepts must be **shared across all inputs**; return a larger pool than
single-show while keeping UI selection capped at 8.

**Concept-based recs (Explore Similar / Alchemy):** list of real shows with concise reasons (not
synopses); reasons **explicitly name which selected concept(s)** they match; recent-bias but allow
classics/hidden gems; **Explore Similar = 5 recs, Alchemy = 6 recs**; ≥1–2 pleasant-but-defensible
surprises.

### 7.4 Conversation summarization
Older turns summarized into 1–2 sentences that **preserve the surface's persona/tone** (no sterile
"system summary" voice). Triggered after ~10 messages.

### 7.5 Real-show resolution (Product §5.8, ai_prompting §5, quality bar §1.5)
Pipeline (`lib/ai` + `lib/catalog`): AI outputs `title + externalId(if available) + mediaType` →
look up catalog by `externalId` → **accept first result whose title matches case-insensitively** →
becomes a real selectable Show carrying the AI "reason" as **transient** text. If not found → show
non-interactive and/or hand off to Search. **Real-show integrity is non-negotiable (score must = 2).**

### 7.6 Guardrails / fallbacks
If structured-output parsing fails: **retry once** with stricter formatting instructions; else fall
back to unstructured commentary + Search handoff. Validate all structured outputs with Zod.

### 7.7 AI data persistence (Product §5.7)
| AI data | Persisted? | Freshness |
|---|---|---|
| AI Scoop | Yes (if in collection) | 4 hours (regenerate on demand after expiry) |
| Alchemy results/reasons | No (session only) | cleared on leaving Alchemy |
| Ask chat history | No (session only) | cleared on reset/leave |
| Mentioned shows strip | No (session only) | derived from current chat |

---

## 8. External Catalog Integration (`src/lib/catalog/`)

- **Provider-agnostic adapter** exposing: `search(query)`, `getDetail(id, mediaType)`,
  `getCredits(id)`, `getPersonDetail(id) + credits`, `getProviders(id, region)`, `getVideos/images`,
  `getRecommendations/similar`, `resolveByExternalId(externalId, title, mediaType)`.
- **Catalog API key held server-side**; calls proxied through Next.js Route Handlers (`/api/catalog`,
  `/api/search`). Browser never sees the catalog key. Key configurable via env or `cloud_settings`.
- Adapter output feeds `lib/mapping` to build/merge `Show` records; transient fields (cast, videos,
  recommendations…) attached for UI only, never persisted.
- Genre mapping stores **names** (not ids); dates parsed with multiple formats; provider data stores
  **IDs only** by region (fetch provider metadata separately for display).

---

## 9. API / Server Boundary (Next.js Route Handlers & Server Actions)

Every handler calls `resolveIdentity()` and scopes by `(namespace_id, user_id)`.

- `GET/POST /api/collection` — list (with filter/media-type params), upsert (apply save rules +
  merge), delete (removal + clear My Data).
- `POST /api/collection/:id/rating|status|tags|scoop` — granular My-Data mutations with correct
  auto-save/default behavior and timestamp bumps.
- `GET /api/search?q=` , `GET /api/catalog/:type/:id` , `GET /api/person/:id` — catalog proxies.
- `POST /api/ai/ask` , `/api/ai/scoop` , `/api/ai/concepts` , `/api/ai/recommend` — server-side AI
  with structured-output validation + real-show resolution.
- `GET /api/export` — build the `.zip` (JSON, ISO-8601 dates) of the user's shows + My Data.
- `POST /api/sync` (if sync enabled) — per-field timestamp conflict resolution, duplicate detection
  + transparent merge (Product §5.10), `cloud_settings.version` for settings conflicts.
- All secrets (service-role, catalog key, AI key) are **server-only**; browser holds anon key only.

---

## 10. Cross-Device Sync & Integrity (Product §5.10, §5.11)

- Optional; when enabled, library + settings stay consistent across devices.
- **Per-field conflict resolution by most-recent update timestamp** (reuse §4.3 merge fn for shows;
  `cloud_settings.version` epoch-seconds for settings).
- Duplicate items detected + merged **transparently** (no user disruption).
- Because backend is source of truth, clearing a client / reinstalling never loses data (Rider §6).

---

## 11. Constants, Theme & Config (INSTRUCTIONS.md compliance)

No magic numbers / inline styles. Centralize:
- **Feature counts** in `config/`: concepts default **8**, concept selection cap **8**, Explore
  Similar recs **5**, Alchemy recs **6**, min Alchemy input shows **2**, starter prompts shown **6**,
  summarize-after **~10** messages, Scoop freshness **4h**, Scoop word target **150–350**.
- **Theme tokens** in `theme/`: colors, spacing, radii, and a **type scale mapping** for the six
  font-size steps (`XS…XXL`). TSX references tokens only — no hex/px inline.
- **Env parsing** in `config/env.ts` (typed, validated at boot).

---

## 12. Environment, Scripts & Deliverables (Infra Rider §3)

**`.env.example`** (names + short comments; no secrets):
- `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY` (browser-safe).
- `SUPABASE_SERVICE_ROLE_KEY` (**server-only**).
- `NAMESPACE_ID` (a.k.a. `RUN_ID`/`BUILD_ID`) — run isolation.
- `AI_API_KEY`, `AI_MODEL` (default to a latest Claude model), `CATALOG_API_KEY`.
- `APP_MODE` / `NODE_ENV` gate for dev identity injection; optional `DEFAULT_USER_ID`.

**`.gitignore`** excludes `.env*` **except** `.env.example`. No secret ever committed.

**Scripts** (names flexible, Rider §3.2):
- `npm run dev` — start app.
- `npm test` / `npm run test:e2e` — unit + e2e.
- `npm run db:migrate` (+ optional `npm run seed`) — deterministic fresh schema/state.
- `npm run test:reset` → `scripts/reset-namespace.ts` — reset test data **for the namespace only**.

**The build must run by filling env vars — no source edits** (Rider §3.1). **No Docker required**
(Rider §8); if local Supabase via Docker is used it must be optional + documented.

---

## 13. Testing & Quality Strategy

- **Unit (Vitest)** on critical logic (adjacent to source): merge policy (`selectFirstNonEmpty` +
  timestamp resolution), save-rules state machine (all §6 triggers/defaults incl. rating→Done and
  tag→Later+Interested), showList parser round-trip, catalog→Show mapping, date parsing, filter
  grouping/ordering, real-show resolver.
- **AI output validation:** Zod schemas + the retry-once-then-fallback contract; assert concept
  count/word-length, rec counts (5/6), and that reasons cite concepts.
- **Discovery quality bar (discovery_quality_bar.md):** a lightweight rubric harness scoring Voice,
  Taste Alignment, Surprise, Specificity, **Real-Show Integrity (must=2)**; passing threshold ≥7/10.
  Golden set is optional in v1 but wire the harness so it can be populated later.
- **E2E / visual (Playwright):** key journeys (§ Product §9): build collection, rate-to-save,
  tag-to-save, maintain, tag-driven filtering, Ask discovery, Explore Similar, Alchemy chain, talent
  deep-dive, export. All e2e create/reset data **inside the namespace** (destructive-safe, Rider §7).
- Lint-clean; humble components verified (no logic in TSX).

---

## 14. Delivery Phases (suggested order)

1. **Foundations:** Next.js app skeleton, `.env.example`/`.gitignore`, Supabase clients (anon +
   service role), `resolveIdentity()` (dev injection), config/theme scaffolding, migration + reset
   scripts. → *Satisfies Rider success criteria early.*
2. **Data model + collection CRUD:** `shows`/`cloud_settings`/`app_metadata` migrations, mapping +
   merge policy, save-rules engine, server routes for collection. Heavy unit tests.
3. **Collection Home + filters + tiles:** grouped status sections, filter panel, media-type toggle,
   badges, empty states.
4. **Search + Show Detail:** catalog adapter + proxies, poster grid, full Detail narrative order,
   toolbar status/rating/tag with auto-save + removal confirmation.
5. **AI surfaces:** `lib/ai` persona + prompt builders + parsers; Scoop (stream + 4h cache +
   collection-gated persistence); Ask (mentions strip, starter prompts, summarization, Ask-about
   variant); Concepts + Explore Similar (5) + Alchemy (6, chaining); real-show resolution + fallbacks.
6. **Person Detail + analytics charts.**
7. **Settings + Export (.zip/JSON/ISO-8601) + optional Sync** (per-field timestamp resolution,
   dup-merge, `cloud_settings.version`).
8. **Hardening:** data continuity migrations (`data_model_version`), quality-bar harness,
   destructive-test coverage, production identity gating.

---

## 15. Open Questions & Risks (carry forward; do not silently resolve)

From Product §10 / Detail §6 / gaps found while planning:
- **Missing companion docs** (`where_is_the_heart_opus.md`, `ai_personality_opus.md`,
  `philosophy_opus.md`): the "80 starter prompts" and some voice nuance live there. Mitigation: seed
  a curated, easily-expandable starter-prompt list; keep persona centralized so it's swappable.
- Should **Next** become a first-class UI status? (Model supports it; hidden today.)
- Named **custom lists** beyond tags?
- Should generating **Scoop on an unsaved show** implicitly save it? (Currently no — persists only on
  save.)
- Clearing **My Rating**: explicit "Unrated" state vs nil?
- **Import/Restore** from export zip (Settings mentions it; UI missing) — plan export to be
  import-ready.
- Saving/sharing **Alchemy sessions** as reusable "blends."
- Explicit **myStatus filters** in the sidebar (model supports it).
- **Ask-about-a-show** exact prefill/seed behavior is TBD (spec says current app hands off a show).
- Detail TODOs: Alchemy entry hidden on Detail; inline trailer playback; 1-line "why concepts
  matter" explainer under Get Concepts.

**Top risks:** (1) merge/save-rule correctness (single most bug-prone area — one shared, tested merge
fn); (2) AI structured-output reliability + real-show resolution (non-negotiable integrity); (3)
identity/namespace scoping leaks (enforce at every server route); (4) sync conflict correctness; (5)
data continuity across model-version upgrades.

---

## 16. Compliance Checklist (maps back to the rubrics)

- [ ] Next.js latest + Supabase via official clients; no Docker required. *(Rider §2, §8)*
- [ ] `.env.example` + `.gitignore` (excl. `.env*` but keep example); runs via env only, no code
  edits; anon key in browser, service role server-only. *(Rider §3.1)*
- [ ] Scripts: start / test / reset-namespace; migrations for deterministic fresh state. *(§3.2–3.3)*
- [ ] All user rows scoped by `(namespace_id, user_id)`; multi-user-ready. *(Rider §4)*
- [ ] Dev identity injection, gated in prod; OAuth swap = config not schema. *(Rider §5)*
- [ ] Backend source of truth; client cache disposable. *(Rider §6, Product §8.9)*
- [ ] Destructive tests scoped to namespace; no global teardown. *(Rider §7)*
- [ ] User overlay wins everywhere; merge = non-my `selectFirstNonEmpty`, my = newer-timestamp.
  *(Product §4.1, storage-schema)*
- [ ] Save/default/remove rules incl. rating→Done, tag→Later+Interested, removal clears My Data.
  *(Product §5.2–5.4)*
- [ ] AI: one persona, Search voiceless, spoiler-safe, structured mentions, Scoop (4h/collection-
  gated/stream), concepts (8/1–3 words), recs (5/6, concept-cited), real-show integrity, retry+
  fallback. *(AI docs, quality bar)*
- [ ] Detail narrative order preserved; toolbar status/rating/tags; Person analytics; Export
  `.zip`/JSON/ISO-8601. *(Detail spec, Product §7)*
- [ ] Data continuity across `data_model_version` upgrades. *(Product §5.11)*
- [ ] Fractal architecture, humble components, no magic numbers/inline styles, tests on critical
  logic. *(INSTRUCTIONS.md)*

---

*Deliverable complete: this is a planning artifact only. No product source files were created or
modified.*
