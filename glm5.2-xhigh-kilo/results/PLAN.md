# Implementation Plan — Personal TV + Movie Companion

**Source specs:** `docs/prd/product_prd.md`, `docs/prd/infra_rider_prd.md`, and all of `docs/prd/supporting_docs/**` (incl. `technical_docs/storage-schema.{md,ts}`).
**Architectural guidelines:** `INSTRUCTIONS.md` (fractal architecture, humble components, co-location, theme tokens, no magic numbers).
**Deliverable type:** Plan only. No implementation in this step.

---

## 0. How to read this plan

- Sections 1–4 establish product scope and the non-negotiable technology/structure decisions.
- Sections 5–9 define the foundation: persistence, identity/isolation, external catalog, AI, and core domain logic. Everything else depends on these.
- Section 10 is the feature-by-feature build spec.
- Sections 11–14 cover server routes, client state, cross-cutting rules, and testing.
- Section 15 sequences the work into phases; Section 16 traces every PRD requirement to a plan section; Section 17 is the infra-rider compliance checklist.

The plan is technology-specific only where the infra rider forces it (Next.js + Supabase). Elsewhere it stays provider-agnostic and names the contracts that must be reproduced.

---

## 1. Product Overview (recap for context)

A personal TV + movie companion. Users build *their version* of each show (status, interest, tags, rating, AI "Scoop") and the app uses that taste profile to power discovery via four paths: traditional **Search**, conversational **Ask**, **Alchemy** (concept blending of 2+ shows), and per-show **Explore Similar** (concept-driven recs). Supporting surfaces: **Collection Home** (filtered library by status), **Show Detail** (single source of truth), **Person Detail** (cast/crew deep-dive), and **Settings** with first-class **Export My Data**.

Core product principles (PRD §8) that shape every decision:
1. The user's overlaid version wins everywhere a show appears.
2. Discovery must be actionable — every recommendation maps to a real, selectable show.
3. AI is taste-aware (library + My Data + session context).
4. Spoiler-safe by default unless explicitly invited otherwise.
5. Implicit auto-save/default behaviors must feel natural, not surprising.
6. The user's data is theirs (export is first-class).
7. Identity is explicit: every user-owned record is scoped to `user_id`.
8. Runs/builds are isolated via a stable `namespace_id`.
9. The backend is the source of truth; clients may cache; clearing client storage never loses user data.

---

## 2. Technology Decisions & Rationale

Mandated by `infra_rider_prd.md` §2 and §8; chosen elsewhere for fit.

| Concern | Decision | Rationale / Source |
|---|---|---|
| App runtime (UI + server boundary) | **Next.js (latest stable)**, App Router | Infra rider §2 (required) |
| Persistence | **Supabase** (Postgres + official client libs), hosted preferred, local optional, Docker optional | Infra rider §2, §8 |
| Client key | Anon/public key in browser | Infra rider §3.1 |
| Server key | Service-role key, **server-only**, never shipped to client | Infra rider §3.1 |
| Auth (now) | Dev identity injection (`X-User-Id` header + `namespace_id`), gated to non-production | Infra rider §5.1 |
| Auth (later) | Supabase Auth / OAuth — config + wiring change only, **no schema redesign** | Infra rider §5.2 |
| External catalog | Provider abstraction with a TMDB-style reference adapter (configurable) | PRD §11 (vendor-agnostic); schema is TMDB-shaped |
| AI provider | OpenAI-compatible abstraction (base URL + key + model, all env-configurable) | ai_prompting_context; Settings §7.7 |
| Language | TypeScript (Next.js implies it; also matches `storage-schema.ts`) | Practical default |
| Styling | Design-token theme system (no hex/pixels in markup) | INSTRUCTIONS.md |
| State | Server Components + Server Actions/Route Handlers for data; lightweight client state for AI sessions | Backend-is-source-of-truth (PRD §8.9) |
| Containerization | None required; Docker only if local Supabase, documented as optional | Infra rider §8 |

**Non-goals honored (PRD §3, §11):** no offline-first requirement; no complex search preloading/caching (live queries fine); no UI animation prescriptions; no social features; no vendor lock-in specs.

---

## 3. Repository & Directory Structure

Follows the **fractal architecture** in `INSTRUCTIONS.md`: Pages → Features → Sub-Features, each self-contained with its own `hooks/`, `utils/`, `constants.ts`. Main file matches directory name (no `index.tsx`). Humble components: TSX holds markup + binding only; logic lives in `useFeatureLogic()` hooks.

```
/
├── .env.example
├── .gitignore                      # excludes .env* except .env.example
├── package.json                    # dev, test, test:reset, lint, typecheck, build, supabase:*
├── next.config.js
├── tsconfig.json
├── supabase/
│   ├── migrations/                 # versioned SQL, ordered, repeatable
│   └── seed/                       # default user + sample shows per namespace
├── src/
│   ├── config/                     # global constants, env parsing, limits (TTLs, caps)
│   ├── theme/                      # design tokens (colors, spacing, type scale incl. font sizes)
│   ├── components/                 # shared UI primitives (Tile, Badge, Chip, Carousel, etc.)
│   ├── hooks/                      # global hooks
│   ├── utils/                      # global pure utils (dates, ids, formatting)
│   ├── lib/
│   │   ├── supabase/               # server + browser clients, RLS helpers, service-role guard
│   │   ├── identity/               # namespace + user_id resolution (dev injection / future auth)
│   │   ├── catalog/                # provider abstraction + reference adapter (decode/map/merge)
│   │   ├── ai/                     # provider abstraction + prompt templates + parsers
│   │   ├── domain/                 # Show entity, merge rules, save/default/removal, timestamps
│   │   └── export/                 # Export My Data zip builder
│   └── pages/
│       ├── Home/                   # Collection Home (filtered library)
│       ├── Detail/                 # Show Detail (13-section narrative)
│       ├── Find/                   # Find/Discover hub (Search | Ask | Alchemy)
│       ├── Person/                 # Person Detail
│       └── Settings/               # Settings + Export My Data
└── tests/                          # cross-cutting tests (unit, integration, e2e)
```

Each page mirrors the INSTRUCTIONS.md pattern, e.g.:

```
src/pages/Detail/
├── Detail.tsx
└── features/
    ├── HeaderMedia/               # carousel: backdrops/posters/logos/videos
    ├── CoreFacts/                 # year/runtime + community score
    ├── MyRelationship/            # status/interest chips, rating bar, tags
    ├── OverviewScoop/             # overview + Scoop (stream)
    ├── AskAboutShow/              # "Ask about this show" CTA + handoff
    ├── Recommendations/           # traditional similar/recommended strand
    ├── ExploreSimilar/            # Get Concepts → select → Explore Shows
    ├── Providers/                 # streaming availability
    ├── CastCrew/                  # → Person
    ├── Seasons/                   # TV only
    └── BudgetRevenue/             # movies where available
```

Feature dirs contain their own `hooks/`, `utils/`, `constants.ts`, and nested `features/` where needed.

---

## 4. Environment & Configuration

### 4.1 `.env.example` (all required vars with short comments)

```dotenv
# ---- Supabase (hosted preferred; local optional) ----
NEXT_PUBLIC_SUPABASE_URL=           # project URL (anon-safe, exposed to browser)
NEXT_PUBLIC_SUPABASE_ANON_KEY=       # public/anon key (browser; RLS-enforced)
SUPABASE_SERVICE_ROLE_KEY=          # SECRET: server-only; never shipped to client

# ---- Build/run isolation (infra rider §4) ----
NAMESPACE_ID=                       # stable build isolation id; partitions ALL persisted data
DEV_IDENTITY_ENABLED=true            # gate dev identity injection (disable in prod)

# ---- Dev identity injection (benchmark mode; infra rider §5.1) ----
DEFAULT_USER_ID=                     # opaque stable string for the default dev user
# In dev/test, server also accepts X-User-Id header to override per request.

# ---- External catalog provider (TMDB-style reference) ----
CATALOG_PROVIDER=tmdb               # provider key (pluggable)
CATALOG_API_KEY=                     # catalog provider key (benchmark may supply via env)
CATALOG_BASE_URL=                    # optional override
CATALOG_IMAGE_BASE_URL=              # poster/backdrop/logo URL base

# ---- AI provider (OpenAI-compatible) ----
AI_PROVIDER=openai                  # provider key (pluggable)
AI_API_KEY=                          # SECRET: server-side only; never exposed to client
AI_BASE_URL=                         # optional custom endpoint
AI_MODEL=                            # default model key

# ---- Tunable product constants (sensible defaults) ----
AI_SCOOP_TTL_HOURS=4                # Scoop freshness (PRD §4.9, §5.7)
ASK_SUMMARIZE_AFTER=10              # turns before chat summarization (PRD §7.3)
ALCHEMY_MAX_CONCEPTS=8             # concept selection cap (PRD §4.7, concept_system §5)
EXPLORE_SIMILAR_RECS=5             # recs per round (concept_system §6)
ALCHEMY_RECS=6                     # recs per round (concept_system §6)
CONCEPTS_PER_REQUEST=8            # concepts generated (discovery_quality_bar §2.3)
STARTER_PROMPTS_COUNT=6           # welcome starters (PRD §7.3)
```

### 4.2 `.gitignore` essentials
- Ignore `.env`, `.env.local`, `.env.*` **except** `.env.example`.
- Ignore `node_modules`, `.next`, build outputs.
- Never ignore `supabase/migrations` or `.env.example`.

### 4.3 One-command DX (infra rider §3.2)
- `npm run dev` — start app
- `npm test` — unit + integration
- `npm run test:reset` — reset **namespace-scoped** test data (creates + deletes within `NAMESPACE_ID` only; no global teardown — infra rider §7)
- Plus: `npm run lint`, `npm run typecheck`, `npm run build`, `npm run supabase:migrate`, `npm run supabase:seed`

**Credential rules (infra rider §3.1):** secrets never committed; anon key in browser; service-role key server-only; AI key never sent to the browser (AI calls route through Next.js server).

---

## 5. Persistence Layer (Supabase Schema & Migrations)

The reference `storage-schema.ts` is a single-user/local `Show` that bundles catalog meta + "my data" in one object. For a multi-user backend (infra rider §4.2, §6.1) this is **normalized** into:

- `shows` — catalog cache of public metadata (namespace-scoped, **not** user-owned; one row per external catalog item).
- `library_items` — the per-user "My Data" overlay (one row per `(namespace_id, user_id, show_id)`).
- `cloud_settings` — synced user settings.
- `app_metadata` — data-model version for migrations (PRD §5.11).
- Client-only prefs (LocalSettings + UI state) in `localStorage`.

This split is what lets "user's version wins everywhere" work: rendering overlays a `library_item` onto a `show` at query/render time.

### 5.1 Tables (DDL sketch; ordered migrations)

**`shows` (catalog cache)**
```sql
create table shows (
  id uuid primary key default gen_random_uuid(),
  namespace_id text not null,
  external_id text not null,
  show_type text not null check (show_type in ('movie','tv','person','unknown')),
  external_ids jsonb,                     -- {tmdb, imdb, ...}
  title text not null,
  overview text,
  genres text[] not null default '{}',    -- display names, not ids
  tagline text, homepage text,
  original_language text,
  spoken_languages text[] not null default '{}',
  languages text[] not null default '{}',
  poster_url text, backdrop_url text, logo_url text,
  network_logos text[] not null default '{}',
  vote_average numeric, vote_count int, popularity numeric,
  last_air_date timestamptz, first_air_date timestamptz, release_date timestamptz,
  runtime int, budget bigint, revenue bigint,
  series_status text, number_of_episodes int, number_of_seasons int,
  episode_run_time int[] not null default '{}',
  provider_data jsonb,                    -- ProviderData blob (IDs only)
  details_update_date timestamptz,
  creation_date timestamptz not null default now(),
  is_test boolean not null default false
);
-- TMDB movie/tv id spaces can overlap, so key on (external_id, show_type).
create unique index shows_unique on shows (namespace_id, external_id, show_type);
create index shows_title on shows (namespace_id, title);
```

**`library_items` (user overlay — the "My Data")**
```sql
create table library_items (
  id uuid primary key default gen_random_uuid(),
  namespace_id text not null,
  user_id text not null,                  -- opaque stable string (infra rider §4.2)
  show_id uuid not null references shows(id) on delete cascade,
  my_status text check (my_status in ('active','next','later','done','quit','wait')),
  my_interest text check (my_interest in ('excited','interested')),
  my_tags text[] not null default '{}',
  my_score numeric,
  ai_scoop text,
  my_status_update_date timestamptz,
  my_interest_update_date timestamptz,
  my_tags_update_date timestamptz,
  my_score_update_date timestamptz,
  ai_scoop_update_date timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  is_test boolean not null default false
);
create unique index library_unique on library_items (namespace_id, user_id, show_id);
create index library_status on library_items (namespace_id, user_id, my_status, my_interest);
create index library_tags on library_items using gin (my_tags);  -- tag filters
```

**`cloud_settings` (synced)**
```sql
create table cloud_settings (
  namespace_id text not null,
  user_id text not null,
  user_name text not null,
  ai_model text not null,
  ai_api_key text, catalog_api_key text,   -- optional; never committed; syncable per PRD §7.7
  version bigint not null default 0,       -- epoch seconds; conflict resolution (§5.6, §5.10)
  updated_at timestamptz not null default now(),
  primary key (namespace_id, user_id)
);
```

**`app_metadata`**
```sql
create table app_metadata (
  namespace_id text primary key,
  data_model_version int not null default 3,  -- storage-schema AppMetadata
  updated_at timestamptz not null default now()
);
```

**Transient catalog data** (cast, crew, seasons, videos, recommendations, similar, images, `lastEpisodeToAir`) is **not persisted** (storage-schema.md §"Not stored"). It is fetched on demand from the catalog provider and attached to the Show for rendering. An optional short-TTL server cache (in-memory/edge) is allowed for performance but is not a correctness dependency.

**Tag library** (PRD §4.4): derived from `library_items.my_tags` via `unnest(distinct ...)` per `(namespace_id, user_id)`. No separate table needed; the GIN index supports tag filters. "No tags" filter = shows where `my_tags = '{}'`.

### 5.2 Row-Level Security & isolation

Defense-in-depth even though the app primarily uses server-mediated access (§5.4):

- `library_items`: RLS denies by default; policy allows rows where `namespace_id = current_namespace() AND user_id = current_user_claim()`.
- `shows`: readable within namespace; writes restricted to service role (catalog writes are server-side).
- `cloud_settings`: policy scoped to `(namespace_id, user_id)`.
- `app_metadata`: scoped to namespace.

`current_namespace()` / `current_user_claim()` read session/JWT claims set per request. In benchmark/dev these are populated from `NAMESPACE_ID` + `X-User-Id` (or `DEFAULT_USER_ID`); in production they map to `auth.uid()` and a namespace claim. **Swapping dev injection for real OAuth changes claim wiring, not schema** (infra rider §5.2).

### 5.3 Migrations & seed (infra rider §3.3)

- `supabase/migrations/NNNN_name.sql` — ordered, idempotent SQL. Apply via `npm run supabase:migrate`. A fresh DB can be created deterministically.
- `supabase/seed/` — fixtures: a default user for the namespace + a small set of sample shows/library items tagged `is_test = true` so destructive resets (§5.4 reset script) only touch test rows.
- `dataModelVersion` gating: a migration step that runs an upgrade transform when the stored version < target, bringing existing shows + My Data forward transparently (PRD §5.11). Migration logic is unit-tested.

### 5.4 Data access layer (`src/lib/supabase/`)

- `serverClient()` — service-role client; server-only; used by Route Handlers/Server Actions.
- `browserClient()` — anon client; for optional direct reads under RLS.
- `identity/` — resolves `namespace_id` (env) + `user_id` (dev header/`DEFAULT_USER_ID`, future: auth) into a request-scoped context injected into all queries.
- **All user-owned writes go through server routes** using the service-role client with explicit `(namespace_id, user_id)` filters. This is the primary correctness path; RLS is backup.
- `test:reset` deletes/inserts only rows where `namespace_id = NAMESPACE_ID` (and `is_test = true`), then re-seeds — **no global teardown** (infra rider §7).

---

## 6. Identity & Isolation Model (infra rider §4, §5)

- **`namespace_id`** (build isolation): read from env at build/run start; stable for the build's lifetime. Partitions **all** persisted data (shows cache, library_items, settings, metadata). Two namespaces never read/write each other's data. Destructive tests scoped to it. It is a *build* primitive, not a user concept.
- **`user_id`** (identity): opaque stable string/UUID on every user-owned record. System behaves as if multiple users exist even if UI exposes only one. Within a namespace, the effective partition is `(namespace_id, user_id)`. At minimum one default user exists.
- **Dev identity injection (now):** `DEV_IDENTITY_ENABLED` gates a middleware that reads `X-User-Id` (falling back to `DEFAULT_USER_ID`) and attaches it to the request context. Documented and disabled/gated in production.
- **Migration to OAuth (later):** replace the dev middleware with Supabase Auth; `user_id` becomes `auth.uid()`. Because `user_id` is already an opaque column on every user-owned table, this is **config + wiring**, not a schema redesign (infra rider §5.2).

---

## 7. External Catalog Provider (`src/lib/catalog/`)

A pluggable abstraction with a TMDB-style reference adapter (schema is TMDB-shaped: genres, vote_average, provider IDs, etc.). All vendor specifics live here; the rest of the app speaks only the internal `Show`/transient shapes.

### 7.1 Interface
- `search(query, {page}) → Show[]` (title/keyword; live, no preload required — PRD §3)
- `getDetails(externalId, showType) → Show` (+ transient: cast, crew, seasons, videos, recommendations, similar, images, `lastEpisodeToAir`)
- `lookupByExternalId(externalId, showType) → Show | null`
- `getPerson(personId) → Person` (+ transient: image gallery, bio, filmography/credits)
- `getProviders(externalId, showType) → ProviderData` (store IDs only; fetch provider display metadata separately — storage-schema.md)
- `resolveMention(title, externalId, showType) → Show | null` — for AI recommendation mapping (PRD §5.8): look up by external id, accept first result whose title matches **case-insensitively**; else null → non-interactive/Search handoff.

### 7.2 Decode → `Show` mapping rules (storage-schema.md §"Field mapping")
- External catalog `id` → `Show.id`-equivalent (`external_id` + `show_type`); extra ids → `external_ids`.
- Title: prefer catalog title (movie) / series name (tv); decoding fails if neither exists.
- `showType`: from catalog media type; else infer (`name`→tv, `title`→movie, else `unknown` → reject).
- Genres → display **names** (not ids); dates parsed from multiple accepted formats; ratings/popularity stored directly; movie runtime/budget/revenue and tv status/episode/season counts stored directly.
- Images → renderable URLs constructed from image base + path; **single "best" logo** chosen deterministically (documented rule, e.g., highest `vote_average` among English-language logos).
- Providers → `ProviderData` (IDs by region). Transient fetches (credits, seasons, videos, recommendations, similar, images.*) decoded for UI but **not persisted**.

### 7.3 Catalog → store merge (`src/lib/domain/mergeShows.ts`)
Pure, fully unit-tested. Implements storage-schema.md §"Merge / overwrite policy":
- **Non-my fields:** `selectFirstNonEmpty(newValue, oldValue)` — never overwrite a non-empty stored string/array with empty/empty-array, and never overwrite non-nil with nil.
- **My fields** (`myStatus`, `myInterest`, `myTags`, `myScore`, `aiScoop`): resolve by timestamp — keep the side with the newer `*_update_date`; if only one side has a date, keep that side. This preserves user edits across sync merges and catalog refreshes.
- `details_update_date = now` after a successful merge; `creation_date` set only on first creation (never changed by refresh).
- Same function powers catalog refresh, re-add (PRD §5.5), and cloud-sync conflict resolution (PRD §5.10) — one merge path, reused everywhere.

---

## 8. AI Provider & Prompt Architecture (`src/lib/ai/`)

OpenAI-compatible abstraction (`base URL`, `key`, `model` all env-configurable; key server-only). One shared persona (ai_voice_personality.md §1): a fun, chatty, opinionated TV/movie nerd friend — **joy-forward, opinionated honesty, vibe-first & spoiler-safe, specific not generic, short-when-needed/lush-when-earned**. Tone sliders: 70% friend / 30% critic; 60% hype / 40% measured; adaptive playful↔serious; concise by default, lyrical for Scoop. **Search has no AI voice** (ai_voice_personality §1).

Shared inputs (ai_prompting_context §2): user library + My Data; current show context; selected concepts; recent turns (older summarized). Shared rules: stay in TV/movies (redirect if asked to leave), spoiler-safe by default, opinionated/honest, specific vibe/structure/craft reasoning, recommendations resolve to real catalog items.

### 8.1 Surfaces & contracts

| Surface | Contract | Output | Freshness/Persistence |
|---|---|---|---|
| **Scoop** (Detail) | Mini blog-post of taste: personal take, honest stack-up vs reviews, **"The Scoop" centerpiece**, fit/warnings, "Worth it?" verdict; streams progressively ("Generating…", not blank) | ~150–350 words | TTL **4h**; persist **only if in collection** (PRD §4.9, §5.7) |
| **Ask** (general + "Ask about a show") | Dialogue, picks favorites, simple formatting + bullets for multi-recs; seed context for "ask about a show" | 1–3 tight paragraphs + list | Session-only; summarize after ~10 turns |
| **Ask with mentions** | Structured output: `commentary` (no ids) + `showList` | `Title::externalId::mediaType;;...` | Session-only; renders "mentioned shows" strip |
| **Concepts** (single-show) | 1–3 word evocative bullets, no plot, diverse axes, ordered by strength | bullet list (8 default) | Session-only |
| **Concepts** (multi-show/Alchemy) | Same rules but **shared across all** input shows; larger pool | bullet list | Session-only |
| **Concept recs** (Explore Similar / Alchemy) | Real shows + concise reasons naming matched concepts; recent bias but allow classics/gems | **5** (Explore Similar) / **6** (Alchemy) | Session-only |
| **Conversation summarization** | Older turns → 1–2 sentences, **same persona** (no sterile "system summary") | short summary | Session-only |

### 8.2 Structured output, parsing & fallbacks (ai_prompting_context §5)
- Strict parser for `commentary` + `showList`; the format and parser must match exactly. On parse failure: **retry once** with stricter formatting; otherwise fall back to unstructured commentary + Search handoff.
- Each mentioned/recommended title → `catalog.resolveMention(title, externalId, mediaType)` (PRD §5.8). Resolved → real selectable Show carrying the transient AI "reason"; unresolved → non-interactive or Search handoff.

### 8.3 Streaming
- Scoop streams token-by-token (the user sees progress, not a blank wait — detail_page_experience §3.4).
- Ask streams assistant turns for responsiveness.

### 8.4 Quality bar (discovery_quality_bar.md)
Voice adherence, taste alignment, surprise-without-betrayal, specificity of reasoning, **real-show integrity (non-negotiable =2)**. Passing: Voice ≥1, Taste ≥1, Real-show integrity =2, total ≥7/10. A golden set is **optional in v1**; the plan leaves a hook to add regression fixtures later (discovery_quality_bar §3).

---

## 9. Core Domain Logic (`src/lib/domain/`)

Pure, heavily unit-tested. This is the heart of correctness.

### 9.1 The `Show` render model
A unified object combining `shows` (catalog) + an optional `library_items` overlay. **Display rule (PRD §4.1, §8.1):** wherever a show appears — lists, search, recommendations, AI outputs — if a library item exists, overlay My Data (status/tags/rating/scoop); user edits always win over refreshed public data. Implemented as a single `overlayMyData(show, libraryItem?)` used by every list/grid/detail renderer.

### 9.2 Collection membership (PRD §5.1)
A show is "in collection" iff it has a stored library item with non-null `my_status`.

### 9.3 Saving triggers (PRD §5.2) → ensure library item exists:
- Setting any status.
- Choosing an interest chip (Interested/Excited).
- Rating an unsaved show.
- Adding ≥1 tag to an unsaved show.

### 9.4 Defaults when saving (PRD §5.3)
- No explicit status → `my_status = later`, `my_interest = interested`.
- **Exception:** first save via rating → `my_status = done` (rating implies watched).

### 9.5 Removal (PRD §5.4)
- Trigger: user clears status (reselects active status) + confirms.
- Effects: delete library item (cascade clears status/interest/tags/rating/scoop). The `shows` catalog row remains (it's cache, not user data).
- UX: warning confirmation with "stop asking" after repeated removals — backed by client UI state `hideStatusRemovalConfirmation` + `statusRemovalCountKey` (storage-schema.md).

### 9.6 Re-add (PRD §5.5)
- Encounter a show already saved: preserve latest status/interest/tags/rating/scoop; refresh public metadata via catalog; merge conflicts by most-recent `*_update_date` per field (reuses `mergeShows`).

### 9.7 Timestamps (PRD §5.6, storage-schema)
Each My field has its own `*_update_date`, set on every change. Uses: sorting (recently updated first where applicable), cloud conflict resolution (newer wins), AI cache freshness (Scoop TTL). A single `touch(field, now)` helper updates only the relevant timestamp.

### 9.8 Tile indicators (PRD §5.9)
Badges: in-collection (library item + status exists); user rating (`my_score` exists). Applied uniformly on every tile component.

### 9.9 AI persistence matrix (PRD §5.7)
| Data | Persisted? | Freshness |
|---|---|---|
| Scoop | Yes — **only if in collection** | 4h, regenerate on demand |
| Alchemy results/reasons | No — session only | cleared on leave |
| Ask chat history | No — session only | cleared on reset/leave |
| Mentioned shows strip | No — session only | derived from current context |

---

## 10. Feature Implementation Plan

Each feature maps to a page dir under `src/pages/` with features following the fractal pattern. AI sessions (Ask, Alchemy) are client-held (session-only) and do not persist.

### 10.1 Collection Home (`src/pages/Home/`) — PRD §7.1, §4.5
- **Filters/navigation panel (sidebar):** All Shows (default); one filter per tag (+ "No tags" if any tagless items exist); data filters (genre, decade, community-score ranges); **media-type toggle All/Movies/TV** applied on top of any filter. Filter model = `FilterConfiguration` (storage-schema.ts): `{type, label, value}` with `type ∈ {all, genre, myStatus, communityScore, decade, myTag}`. Selected filter persisted as client UI state `lastSelectedFilter`.
- **Status grouping (fixed order):** 1) Active (prominent/larger tiles), 2) Excited (later+excited), 3) Interested (later+interested), 4) Other (collapsed: Wait, Quit, Done, and unclassified Later without interest). TV's `next` status is model-only, **not** a UI section (PRD §4.2, §10 open question).
- **Tiles:** poster, title, My Data badges (§9.8). Sorting: recently-updated first where applicable (uses `*_update_date`).
- **Empty states:** no shows → prompt to Search/Ask; filter yields none → "No results found."

### 10.2 Search (`src/pages/Find/features/Search/`) — PRD §7.2
- Live text search by title/keywords via catalog `search()`; poster grid results; in-collection items marked (overlay My Data — §9.1); selecting opens Detail. **Auto-opens on launch** if `autoSearch` enabled (LocalSettings). No AI voice, no complex preloading (PRD §3, ai_voice_personality §1).

### 10.3 Ask (`src/pages/Find/features/Ask/`) — PRD §7.3, ai_prompting_context §3.1–3.2
- Chat UI (user/assistant turns); friendly, opinionated, spoiler-safe; honest about mixed reception.
- **Mentioned shows:** structured `commentary` + `showList`; rendered as a horizontal strip; tap → Detail (or Search handoff if mapping fails). Strict parse + retry + fallback (§8.2).
- **Welcome view:** 6 random starter prompts, refreshable (`STARTER_PROMPTS_COUNT`).
- **Context:** retained during session; older turns summarized after ~`ASK_SUMMARIZE_AFTER` (~10) messages; summary keeps persona (§8.1).
- **Variants:** General Ask (from Find); **Ask About a Show** (from Detail "Ask about this show") seeds context with the show. Exact prefill is TBD (PRD §7.3) — implementation seeds the conversation with show context and hands off into Ask mode; flagged as a tuning decision.

### 10.4 Alchemy (`src/pages/Find/features/Alchemy/`) — PRD §4.7, §7.4, concept_system §5–6
- Flow: select **≥2** starting shows (library + global catalog) → **Conceptualize Shows** → fetch shared concepts → select **≤`ALCHEMY_MAX_CONCEPTS` (8)** concepts → **ALCHEMIZE!** → **6** recommendations grounded to real catalog items.
- **Chaining:** "More Alchemy!" uses results as new inputs.
- **Backtracking:** changing input shows clears concepts/results; toggling concepts clears results (concept_system §5).
- **UX:** step cards/sections for clarity; "pick the ingredients you want more of" guidance; empty state nudges ≥1 concept.
- Results/reasons are **session-only** (PRD §5.7).

### 10.5 Show Detail (`src/pages/Detail/`) — PRD §7.5, detail_page_experience.md
Narrative hierarchy (preserve this order unless intentionally changed):
1. **Header media** — carousel of backdrops/posters/logos + videos (trailers) when available; graceful fallback to poster/logo only; trailers inline (open TODO).
2. **Core facts** — year, runtime or seasons/episodes, genres, languages; **community score** bar.
3. **My Tags** — display + picker; adding a tag to an unsaved show auto-saves as **later + interested** (§9.4).
4. **Overview** + **Scoop** toggle — toggle copy: "Give me the scoop!" / "Show the scoop" / open "The Scoop"; streams; 4h freshness; persists only if in collection (§8.1).
5. **"Ask about this show"** CTA → Ask seeded with show context.
6. Genres + languages.
7. **Traditional recommendations** strand (catalog similar/recommended — no AI voice).
8. **Explore Similar** — Get Concepts → select ≥1 → Explore Shows → **5** AI recs (§8.1).
9. **Streaming availability** ("Stream It").
10. **Cast & Crew** horizontal strands → Person Detail.
11. **Seasons** (TV only).
12. **Budget vs Revenue** (movies where available).

**My Relationship controls** (toolbar, not scroll body — detail_page_experience §3.3):
- Status/Interest chips: "Interested/Excited" map to `later + interest`; Active/Done/Quit/Wait chips; setting status saves; **reselecting the active status triggers removal confirmation** (§9.5).
- **Rating bar:** rating an unsaved show auto-saves as **done** (§9.4).
- Feel: quick, playful, no modal walls unless destructive.

**Critical states:** unsaved show (Scoop generatable but persists only on save; auto-save rules fire on status/rating/tag); no trailers/backdrops (premium poster/logo layout); no concepts yet (only "Get Concepts" CTA); TV vs movie (seasons/runtime handling).

### 10.6 Person Detail (`src/pages/Person/`) — PRD §4.10, §7.6
- Image gallery, name, bio (catalog person endpoint).
- **Analytics charts:** average project ratings, top genres, projects-by-year.
- **Filmography** grouped by year; tapping a credit opens Show Detail.
- Person is stored as a `shows` row of `show_type='person'`; filmography/credits are transient (fetched, not persisted).

### 10.7 Settings & Your Data (`src/pages/Settings/`) — PRD §7.7
- **App settings:** font size/readability (`fontSize ∈ {XS,S,M,L,XL,XXL}` — LocalSettings, applies theme token), search-on-launch (`autoSearch`).
- **User:** username (synced via `cloud_settings.user_name`).
- **AI:** API key + model (server-side; storing/syncing user-entered keys optional, never committed; benchmark supplies via env). Model synced.
- **Integrations:** catalog provider API key (synced).
- **Your data — Export My Data:** produces a `.zip` containing a **JSON backup of all saved shows + My Data**, dates ISO-8601 (PRD §8.6, §7.7). Built by `src/lib/export/`. **Import/Restore** is desired but **not implemented** (open question — §18).

---

## 11. API / Server Route Surface

Next.js Route Handlers / Server Actions own all mutations and AI calls (service-role key + AI key never reach the browser). All scoped by `(namespace_id, user_id)`.

- `GET  /api/library?filter=...&media=...` — filtered collection for Home (overlay applied).
- `GET  /api/library/:showId` — single library item (for Detail My Data).
- `PUT  /api/library/:showId/status` — set/clear status (trigger save defaults / removal).
- `PUT  /api/library/:showId/interest` — set interest (later + interested/excited).
- `PUT  /api/library/:showId/score` — set rating (auto-save done if unsaved).
- `PUT  /api/library/:showId/tags` — add/remove tags (auto-save later+interested if unsaved).
- `GET  /api/catalog/search?q=...` — catalog search passthrough.
- `GET  /api/catalog/:externalId?type=...` — details + transient (cast/crew/seasons/vids/recs/similar/providers).
- `GET  /api/person/:id` — person + filmography.
- `POST /api/ai/scoop` — generate Scoop (stream); persists only if in collection; 4h cache check.
- `POST /api/ai/ask` — Ask turn (stream); returns `commentary` + parsed `showList`.
- `POST /api/ai/ask/seed` — "Ask about a show" handoff (seed context).
- `POST /api/ai/concepts` — single-show concepts.
- `POST /api/ai/concepts/alchemy` — multi-show shared concepts.
- `POST /api/ai/recommendations` — concept-based recs (Explore Similar = 5 / Alchemy = 6).
- `POST /api/ai/summarize` — chat summarization.
- `GET/PUT /api/settings` — cloud settings (synced, version-based conflict resolution).
- `GET  /api/export` — Export My Data zip.

Middleware attaches the identity context (`namespace_id` + `user_id`) from env/header (dev) or auth (prod) before handlers run.

---

## 12. Client Architecture & State

- **Server Components** for data-heavy pages (Home, Detail, Person, Settings) — backend is source of truth.
- **Server Actions / Route Handlers** for all writes and AI calls (keys stay server-side).
- **Client state (session-only)** for Ask chat history + mentioned strip and Alchemy selections/concepts/results — held in memory / a lightweight store; intentionally **not persisted** (PRD §5.7). Reset on leave/reset.
- **Client prefs (localStorage):** `autoSearch`, `fontSize`, `hideStatusRemovalConfirmation`, `statusRemovalCountKey`, `lastSelectedFilter`. Losing these is acceptable — they are preferences, not user-owned collection data. The collection itself lives in Supabase, so clearing localStorage never loses user data (infra rider §6.2).
- **Caching:** clients may cache reads for performance; correctness never depends on local persistence (PRD §8.9). Cache is disposable.
- **Humble components:** TSX = markup + binding; logic in `useFeatureLogic()` hooks. No hex/colors/pixels in markup — theme tokens only. Constants in `config/` or local `constants.ts`.

---

## 13. Cross-Cutting Concerns

- **Merge single path:** `mergeShows()` reused for catalog refresh, re-add, and sync conflicts (§7.3, §9.6). Newest `*_update_date` wins per My field; non-My fields use `selectFirstNonEmpty`.
- **Display overlay single path:** `overlayMyData()` reused on every surface so the user's version always wins (§9.1).
- **Real-show integrity:** every AI recommendation/mention is resolved via `catalog.resolveMention()` before being shown as selectable (PRD §5.8, discovery_quality_bar §1.5).
- **Spoiler-safety default:** enforced in every AI prompt + a runtime guard; lifted only on explicit user request.
- **Sync (optional, PRD §5.10):** when enabled, per-field newest-wins via timestamps; duplicates merged transparently; `cloud_settings.version` (epoch) resolves settings conflicts. Designed but may be a later phase.
- **Data continuity (PRD §5.11):** `app_metadata.data_model_version` + upgrade transforms in migrations preserve libraries across model changes automatically, no user action, no data loss.
- **Isolation enforcement:** `(namespace_id, user_id)` filter on every query; destructive ops scoped to namespace + `is_test`.

---

## 14. Testing Strategy

- **Unit (pure domain — the critical logic):**
  - `mergeShows` (non-My `selectFirstNonEmpty`, My-field timestamp resolution, creation/details-date semantics).
  - Save/default/removal rules (§9.3–9.5) incl. rating→done, tag→later+interested, status→later+interested.
  - Re-add merge (preserve latest, refresh meta, newer-wins).
  - Catalog decode/mapping (title/showType inference, genre→name, date parsing, best-logo rule, ProviderData).
  - AI output parsing (`commentary`+`showList`; retry/fallback).
  - Filter + media-type composition; status grouping; tag-library derivation.
  - Scoop TTL/freshness; AI persistence gating (only-if-in-collection).
- **Integration:** Route Handlers against a **namespace-scoped** Supabase (test namespace, `is_test` rows); verify isolation (namespace A cannot see namespace B; user X cannot see user Y within a namespace). `test:reset` resets only the test namespace.
- **AI quality (optional v1):** discovery quality-bar rubric scoring + a hook for golden-set fixtures (left unpopulated per discovery_quality_bar §3).
- **E2E:** the 10 key user journeys (PRD §9) — build collection, rate-to-save, tag-to-save, maintain, tag-driven organization, Ask discovery, Explore Similar, Alchemy, talent deep-dive, backup.
- **Visual:** Detail page, Home, Alchemy flow where protective.
- **Quality gates:** `npm run lint` + `npm run typecheck` must pass before merge.

---

## 15. Implementation Phases & Milestones

Ordered so each phase is independently testable and later phases depend only on stable foundations.

- **Phase 0 — Scaffold & foundation.** Repo, Next.js + Supabase clients, `.env.example`, migrations, identity/isolation middleware, data-access layer, `test:reset`, lint/typecheck/CI. *Exit:* isolated CRUD of a library item for the default dev user; reset works without global teardown.
- **Phase 1 — Catalog provider.** Search + details + person + providers; decode→Show mapping; transient fields; `resolveMention`. *Exit:* Search page + read-only Detail (public data only).
- **Phase 2 — Domain core & persistence.** `Show` render model + `overlayMyData`; `mergeShows`; save/default/removal rules; timestamps; tile indicators. *Exit:* Detail My Relationship controls (status/interest/rating/tags) with auto-save + removal confirmation; Collection Home with status grouping + filters + media toggle + empty states.
- **Phase 3 — Settings + Export.** cloud_settings, font size, search-on-launch, AI key/model, catalog key; Export My Data zip (ISO-8601 JSON). *Exit:* export round-trips saved shows + My Data.
- **Phase 4 — AI provider + Scoop.** AI abstraction, persona prompts, streaming, 4h TTL, persist-only-if-in-collection. *Exit:* Scoop generates/streams/caches/persists correctly on Detail.
- **Phase 5 — Concepts + Explore Similar.** Single-show concepts; concept selection; 5 concept-recs; resolveMention mapping. *Exit:* Explore Similar flow on Detail.
- **Phase 6 — Ask.** Chat UI, mentions strip + strict parse/retry/fallback, starter prompts, summarization after ~10 turns, "Ask about a show" handoff. *Exit:* Ask discovery journey.
- **Phase 7 — Alchemy.** 2+ show select, shared concepts, ≤8 select, 6 recs, chaining, backtracking. *Exit:* Alchemy journey.
- **Phase 8 — Person Detail.** Gallery, bio, analytics charts, filmography-by-year, credit→Detail. *Exit:* talent deep-dive journey.
- **Phase 9 — Cross-device sync (optional) & migrations hardening.** Per-field newest-wins sync, `cloud_settings.version` conflict resolution, data-continuity upgrade transforms. *Exit:* sync + version-upgrade preserve data.
- **Phase 10 — Test hardening & polish.** E2E for all 10 journeys, AI quality-bar scoring, golden-set hook, performance pass, edge states.

---

## 16. Requirements Traceability Matrix

| PRD / spec requirement | Plan section |
|---|---|
| §1–2 Product summary, goals | §1 |
| §3 Non-goals | §2 (non-goals honored), §10.2 (live search, no preload) |
| §4.1 Show + display rule | §5.1, §9.1, §9.8 |
| §4.2 Status system (incl. Interested/Excited → later+interest; Next hidden) | §9.3–9.4, §10.1, §10.5 |
| §4.3 Interest levels | §9.3, §10.5 |
| §4.4 Tags | §5.1 (tag library via unnest+GIN), §10.1, §10.5 |
| §4.5 Filters | §10.1, storage-schema FilterConfiguration |
| §4.6 Ask session | §8.1, §10.3 |
| §4.7 Alchemy session | §8.1, §10.4 |
| §4.8 Explore Similar | §8.1, §10.5 (§8), §10.4 |
| §4.9 AI Scoop | §8.1, §10.5 (§4), §9.9 |
| §4.10 Person | §7.1, §10.6 |
| §5.1 Membership | §9.2 |
| §5.2 Saving triggers | §9.3 |
| §5.3 Defaults | §9.4 |
| §5.4 Removal | §9.5, §10.5 |
| §5.5 Re-add | §7.3, §9.6 |
| §5.6 Timestamps | §9.7 |
| §5.7 AI persistence | §9.9 |
| §5.8 AI recs → real shows | §7.1 (`resolveMention`), §8.2, §13 |
| §5.9 Tile indicators | §9.8 |
| §5.10 Sync | §13 (Phase 9) |
| §5.11 Data continuity | §5.3, §13 |
| §6 App structure & navigation | §3, §10, §11 |
| §7.1 Collection Home | §10.1 |
| §7.2 Search | §10.2 |
| §7.3 Ask (+variants) | §10.3 |
| §7.4 Alchemy | §10.4 |
| §7.5 Show Detail (13 sections) | §10.5, detail_page_experience |
| §7.6 Person Detail | §10.6 |
| §7.7 Settings & Export | §10.7, §4.1 |
| §8 Cross-cutting principles 1–9 | §13 (1,2,3,4,5,6), §6 (7,8), §12 (9) |
| §9 Key journeys | §14 (E2E), §15 (phases) |
| §10 Open questions | §18 |
| infra rider §2 baseline (Next.js/Supabase, no Docker) | §2, §4 |
| infra rider §3 deliverables (.env, scripts, migrations) | §4, §5.3 |
| infra rider §4 namespace+user_id | §5.2, §6 |
| infra rider §5 dev identity / OAuth migration | §6 |
| infra rider §6 backend source of truth / disposable cache | §12 |
| infra rider §7 destructive scoped testing | §5.4, §14 |
| infra rider §8 cloud-agent compat | §2, §4 |
| infra rider §9 success criteria | §17 |
| storage-schema merge/mapping | §7.2, §7.3, §9 |
| ai_voice_personality persona | §8 |
| ai_prompting_context contracts | §8.1, §8.2 |
| concept_system rules | §8.1, §10.4, §10.5 |
| discovery_quality_bar | §8.4, §14 |
| detail_page_experience hierarchy | §10.5 |
| INSTRUCTIONS fractal architecture | §3, §12 |

---

## 17. Infra Rider Compliance Checklist (infra rider §9)

- [x] `.env.example` provided; app configurable without code edits (§4).
- [x] Repeatable runs without data collisions via `namespace_id` isolation (§5.2, §6).
- [x] All user-owned records carry `user_id` (§5.1 `library_items`, `cloud_settings`; §6).
- [x] Destructive test runs without global teardown (`test:reset` scoped to namespace + `is_test`) (§5.4, §14).
- [x] Real OAuth adoptable later without schema redesign (`user_id` opaque; dev injection swappable for `auth.uid()`) (§6).
- [x] `.gitignore` excludes `.env*` except `.env.example`; secrets never committed (§4.2).
- [x] Browser uses anon key; service-role + AI keys server-only (§4.1, §11).
- [x] Docker not required; local Supabase optional and documented (§2).
- [x] One-command DX: `dev`, `test`, `test:reset` (§4.3).
- [x] Repeatable schema via versioned migrations + seed (§5.3).

---

## 18. Open Questions / Deferred Decisions (PRD §10)

Explicitly **not** built as features now; recommended stance noted for future rounds:
1. **Next as first-class UI status** — keep model-only (`next` in enum, not a Home section) until product decides.
2. **Named custom lists beyond tags** — out of scope; tags remain the only grouping primitive.
3. **AI Scoop on unsaved show implicitly saving it** — keep current behavior: Scoop generatable but persists only if already in collection (§9.9).
4. **Explicit "Unrated" state vs nil** — store `my_score = null` for unrated; no separate sentinel (matches schema).
5. **Import/Restore from export zip** — desired, not implemented; export shipped first (§10.7).
6. **Save/share Alchemy sessions as reusable "blends"** — out of scope; sessions stay session-only (§9.9).
7. **myStatus filters in sidebar** — model supports; UI exposes tag/data/media filters only for now.

Detail-page TODOs (detail_page_experience §6): Alchemy entry hidden on Detail (keep hidden); trailer playback inline (implement in §10.5 header); add a 1-line "why concepts matter" explainer under Get Concepts.

---

## 19. Risks & Mitigations

| Risk | Mitigation |
|---|---|
| AI hallucinated/unresolvable titles break "real-show integrity" (non-negotiable) | `resolveMention` + strict parse + retry + Search handoff; quality-bar `=2` gate; golden-set hook (§8.2, §8.4) |
| Merge logic drift across refresh/re-add/sync | One pure `mergeShows()` reused everywhere; comprehensive unit tests (§7.3, §9.6, §13) |
| Dev identity leaking into prod | `DEV_IDENTITY_ENABLED` gate; service-role key server-only; RLS as backup (§4.1, §5.2, §6) |
| Data loss across model-version updates | `dataModelVersion` + upgrade transforms in migrations; tested (§5.3, §13) |
| Namespace/user collisions between benchmark runs | Mandatory `namespace_id` on every row + RLS + reset scoped to namespace (§5.2, §6) |
| Catalog provider lock-in | Provider abstraction; vendor specifics isolated in `src/lib/catalog/` (§7) |
| AI key exposure to client | All AI calls server-side; key never sent to browser (§8, §11) |
| Session-only AI data accidentally persisted | Ask/Alchemy state in memory only; explicit persistence gating for Scoop (§9.9, §12) |

---

**End of plan.** This plan covers the full PRD, the infra rider, all supporting docs, and the fractal-architecture guidelines, with every requirement traced (§16) and the infra-rider success criteria met (§17). No product code is implemented in this step; the sole deliverable is this file.
