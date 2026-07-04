# Implementation Plan — Personal TV & Movie Companion

**Status:** Planning deliverable only (Step 1). No source code is written in this step.
**Scope source:** `docs/prd/product_prd.md`, `docs/prd/infra_rider_prd.md`, and all of `docs/prd/supporting_docs/**` (AI prompting, AI voice, concept system, detail-page experience, discovery quality bar, storage schema `.md` + `.ts`).
**Architecture standard:** `INSTRUCTIONS.md` (fractal architecture, humble components, no magic numbers/inline styles, co-location, tests).

> Grounding note: This plan is derived from the PRD documents and the repo's own architecture guidelines. It intentionally does **not** reverse-engineer the frozen evaluator catalog (which the repo marks as hidden from Step 1); the traceability table in §19 maps back to PRD sections directly.

---

## 1. What We Are Building (Understanding)

A **personal TV + movie companion**: users build *their own version* of each show (status, interest, tags, rating, AI "Scoop"), and the app turns that taste profile into four discovery paths:

1. **Search** — straightforward catalog search (no AI voice).
2. **Ask** — conversational AI discovery grounded in taste.
3. **Alchemy** — blend 2+ shows into shared "concept catalysts," then get grounded recommendations.
4. **Explore Similar** — per-show concept extraction → recommendations.

Two non-negotiable pillars run through everything:

- **The user's version always wins.** Wherever a show appears (home, search, AI output, recommendations), the saved overlay (status/interest/tags/rating/scoop) is shown instead of raw catalog data.
- **Discovery is actionable and grounded.** Every AI recommendation must resolve to a real, selectable catalog item; nothing hallucinated.

Alongside the product spec, the **Infrastructure & Execution Rider** constrains *how* it runs: Next.js + Supabase, env-var configuration with no code edits, per-build **namespace isolation**, per-record **`user_id`** scoping, dev-friendly identity injection with a clean path to real OAuth, backend as source of truth, and destructive test resets scoped to a namespace.

### 1.1 The "heart" we must preserve
The supporting docs make clear this is not a generic CRUD catalog. The differentiators are:
- A **distinct AI persona** — a warm, opinionated, spoiler-safe "TV/movie nerd friend" that is consistent across surfaces yet adapts its mode (Scoop = mini-review, Ask = quick dialogue, Concepts = evocative ingredients, Recs = thrilled friend sharing gold).
- **Vibes over genres** — "concepts" are 1–3 word taste ingredients (`hopeful absurdity`, `slow-burn dread`), never genre labels or plot points.
- **Frictionless, implicit saves** — rating/tagging an unsaved show quietly saves it with sensible defaults; the UX never feels like data entry.

A rebuild that nails the data model but flattens the voice/concepts has missed the product.

---

## 2. Guiding Principles & Cross-Cutting Rules (must hold everywhere)

1. **User overlay precedence** — a single `applyOverlay(catalogShow)` path merges saved My Data onto any show before render; used by tiles, search, AI recs, and detail.
2. **Backend is source of truth** — clients may cache (React Query, localStorage) but correctness never depends on local persistence; clearing client storage loses nothing user-owned.
3. **Identity is explicit** — every user-owned row carries `user_id`; every persisted row is partitioned by `(namespace_id, user_id)`. The app behaves as if multiple users exist even when the UI exposes one.
4. **Isolation** — one stable `namespace_id` per build; destructive resets scope to the namespace only (never global teardown).
5. **Spoiler-safe by default** — all AI surfaces avoid plot/twists unless the user explicitly asks.
6. **Actionable discovery** — recommendations resolve to real shows or degrade gracefully (non-interactive / Search handoff).
7. **Secrets never in the repo** — provider/AI keys live in env or server-only settings; browser code only ever sees public/anon keys.
8. **Data is the user's** — export/backup is first-class; data survives model upgrades.
9. **Testable by construction** — humble components, logic in hooks, unit tests adjacent to logic, destructive tests namespace-scoped.

---

## 3. Technology Stack & Rationale

| Concern | Choice | Why |
|---|---|---|
| App runtime / server boundary | **Next.js (latest stable), App Router, TypeScript** | Required by rider; App Router gives us server route handlers + server components as the trust boundary for secrets. |
| Persistence | **Supabase (Postgres)** via official `@supabase/supabase-js` | Required by rider. Hosted instance for cloud agents; no Docker required. |
| Server data access | **Server-mediated** through Next.js route handlers using a server Supabase client | Cleanest fit for dev identity injection + namespace injection + keeping the elevated key server-only (see §7). |
| Client server-state | **TanStack Query (React Query)** | Caching, invalidation, optimistic updates for saves; disposable cache aligned with "backend is source of truth." |
| Styling | **CSS Modules + design tokens** (CSS custom properties generated from a typed token source in `src/theme`) | Satisfies "no hex/inline styles in TSX; reference tokens only." Font-size setting drives a root scale variable. (Tailwind-with-token-config is an acceptable alternative but risks styling-in-markup.) |
| AI provider | **Provider-agnostic adapter**, default **Anthropic Claude** (latest, e.g. `claude-sonnet-5` for chat/concepts, a capable model for Scoop); model + key configurable | PRD requires model selection + provider key; adapter keeps us swappable. |
| Catalog provider | **Provider-agnostic adapter**, TMDB-shaped (schema implies id→genre-name maps, provider IDs, image paths, `media_type`) | PRD/schema are provider-agnostic; adapter isolates the vendor. |
| Zip export | Server route assembling JSON + zip (e.g. `archiver`/`jszip`) | Export My Data as `.zip` with ISO-8601 dates. |
| Testing | **Vitest** (unit) + **Playwright** (integration/visual) | Unit tests adjacent to logic; Playwright for visual + namespace-scoped destructive flows. |

Docker is **optional** only (local Supabase convenience) and documented as such; the supported path is a hosted Supabase URL + keys in env.

---

## 4. High-Level Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│ Browser (React / Next client components)                           │
│  • Pages → Features → Sub-Features (fractal)                        │
│  • React Query cache (disposable)                                   │
│  • applyOverlay(): user version wins on every show render          │
│  • Session-only AI state (Ask chat, Alchemy, mentions)             │
└───────────────▲───────────────────────────────┬────────────────────┘
                │ fetch (same-origin API)        │
┌───────────────┴───────────────────────────────▼────────────────────┐
│ Next.js server (route handlers / server actions) = TRUST BOUNDARY  │
│  • Identity middleware → (namespace_id, user_id)                    │
│  • Persistence service (Supabase server client)                    │
│  • Catalog proxy (keeps catalog key server-side, maps → domain)    │
│  • AI proxy (keeps AI key server-side, prompts, parse/guardrails)  │
│  • Merge engine, save-trigger/default engine, data-model migrator  │
└───────┬──────────────────────┬───────────────────────┬─────────────┘
        │                      │                       │
   ┌────▼─────┐         ┌──────▼──────┐          ┌──────▼──────┐
   │ Supabase │         │ Catalog API │          │  AI API     │
   │ Postgres │         │ (TMDB-like) │          │ (Claude…)   │
   └──────────┘         └─────────────┘          └─────────────┘
```

**Layering:** UI (pages/features) → client hooks → API routes → domain services (merge, saves, migration, resolution) → adapters (Supabase, catalog, AI). Domain services are pure/testable and provider-agnostic.

---

## 5. Repository Layout (fractal + Next reconciliation)

Next's `app/` router entries are **thin**: each route file renders a page component that lives in `src/pages/<Page>/<Page>.tsx`, preserving the fractal structure (Pages → Features → Sub-Features) from `INSTRUCTIONS.md`. Main files match their directory name (no `index.tsx`).

```
app/                                   # Next routing only (thin)
  layout.tsx                           # shell providers (Query, theme, identity)
  page.tsx                             # → src/pages/Home/Home.tsx
  show/[id]/page.tsx                   # → src/pages/Detail/Detail.tsx
  person/[id]/page.tsx                 # → src/pages/Person/Person.tsx
  find/page.tsx                        # → src/pages/Find/Find.tsx (Search|Ask|Alchemy)
  settings/page.tsx                    # → src/pages/Settings/Settings.tsx
  api/
    shows/route.ts                     # list/upsert/delete collection
    shows/[id]/route.ts                # get/patch My Data, remove
    catalog/search/route.ts
    catalog/details/[id]/route.ts
    catalog/person/[id]/route.ts
    ai/scoop/route.ts                  # streaming
    ai/ask/route.ts                    # chat + structured mentions
    ai/summarize/route.ts
    ai/concepts/route.ts               # single + multi
    ai/recommendations/route.ts        # explore similar + alchemy
    settings/route.ts                  # cloud + user settings
    export/route.ts                    # zip
    test/reset/route.ts                # namespace-scoped reset (dev/test only)
src/
  config/                              # env access, enums, caps, freshness, counts
    constants.ts                       # STATUS/INTEREST, CONCEPT_COUNT=8, ALCHEMY_RECS=6, EXPLORE_RECS=5, SCOOP_TTL_MS, SUMMARIZE_AFTER=10, MAX_CONCEPTS=8
  theme/                              # tokens.ts + tokens.css (vars), fontScale
  components/                          # shared primitives (ShowTile, PosterGrid, Chip, StatusChips, RatingBar, Strand, Carousel, EmptyState, MediaTypeToggle, MentionStrip…)
  hooks/                               # useIdentity, useCollection, useOverlay, useMediaTypeFilter…
  utils/                              # merge.ts, saveRules.ts, dates.ts, showList.ts, resolveRecs.ts, grouping.ts
  lib/
    supabase/                          # serverClient.ts, types
    identity/                          # resolveIdentity.ts (namespace + user)
    catalog/                           # provider.ts (adapter) + mappers (toShow, toPerson)
    ai/                                # provider.ts, prompts/*, parsers/*
    domain/                            # mergeShow.ts, applySaveTriggers.ts, migrateModel.ts, resolveRecommendation.ts
  pages/
    Home/ Detail/ Find/ Person/ Settings/   # each: Page.tsx + features/** + hooks/ + utils/
```

Feature-specific logic (e.g. `Detail/features/ScoopSection/hooks/useScoop.ts`) is co-located; only genuinely shared logic is promoted to `src/utils` / `src/hooks`.

---

## 6. Data Model & Persistence (Supabase)

### 6.1 Design decision — one row per saved show, per user
The reference schema models a single merged `Show` object carrying both catalog snapshot and My Data, and defines "in collection" as *has a non-nil `myStatus`*. We follow that: the `shows` table stores **saved** collection items (created by save triggers), scoped by `(namespace_id, user_id)`. Transient catalog data (`cast/crew/seasons/videos/recommendations/similar/images`) is **never** persisted — it is re-pullable on demand.

### 6.2 Tables (all user-owned tables carry `namespace_id` + `user_id`)

**`shows`** — primary key `(namespace_id, user_id, id)`; columns mirror `storage-schema.ts` 1:1 (snake_case): identity (`id`, `title`, `show_type`, `external_ids jsonb`), catalog meta (`overview`, `genres text[]`, `tagline`, `homepage`, `original_language`, `spoken_languages text[]`, `languages text[]`), images (`poster_url`, `backdrop_url`, `logo_url`, `network_logos text[]`), ratings/popularity (`vote_average`, `vote_count`, `popularity`), dates (`last_air_date`, `first_air_date`, `release_date`), movie fields (`runtime`, `budget`, `revenue`), TV fields (`series_status`, `number_of_episodes`, `number_of_seasons`, `episode_run_time int[]`, `last_episode_run_time`), **My Data** (`my_tags text[]`, `my_score`, `my_status`, `my_interest` + a `*_update_date` per field), AI (`ai_scoop`, `ai_scoop_update_date`), management (`details_update_date`, `creation_date`, `is_test bool`), `provider_data jsonb`. Indexes on `(namespace_id, user_id, my_status)` and a partial index `where my_status is not null`.

**`cloud_settings`** — PK `(namespace_id, user_id, id='globalSettings')`: `user_name`, `version double precision` (epoch seconds, conflict resolution), `catalog_api_key`, `ai_api_key`, `ai_model`. Keys never returned to the browser (see §16).

**`app_metadata`** — PK `(namespace_id, user_id)`: `data_model_version int default 3`. Drives data-continuity migration (§6.5).

**`user_settings`** — PK `(namespace_id, user_id)`: `auto_search bool`, `font_size text`, `hide_status_removal_confirmation bool`, `status_removal_count int`, `last_selected_filter jsonb`. Server-side mirror so "clearing client storage loses nothing," with a localStorage cache for instant UX. (The schema classifies these as device-local UserDefaults; we mirror them server-side to satisfy the rider's source-of-truth rule while keeping a local fast-path.)

### 6.3 Isolation & access
- **All reads/writes go through server route handlers** that always filter by the resolved `(namespace_id, user_id)`. This is the primary isolation guarantee.
- **RLS as defense-in-depth (staged):** enable Row-Level Security with policies keyed on request-scoped GUCs (`current_setting('app.namespace_id')`, `app.user_id`), set per transaction. In benchmark/dev the server sets these from the injected identity; when OAuth lands, they come from the verified JWT — **no schema change**.
- **`is_test` flag** allows fine-grained destructive scoping (reset only test rows) without touching real dev data in the same namespace.

### 6.4 Merge / overwrite policy (from `storage-schema.md`, exact)
Implemented in `lib/domain/mergeShow.ts`, unit-tested:
- **Non-My fields:** `selectFirstNonEmpty(newValue, oldValue)` — never overwrite a non-empty stored string/array with empty; never overwrite non-nil with nil.
- **My fields** (`my_tags`, `my_score`, `my_status`, `my_interest`): resolve by `*_update_date` — newer wins; if only one side has a date, keep that side. Preserves user edits across catalog refreshes and cross-device sync.
- `details_update_date` = now after any catalog merge; `creation_date` set only on first create (refreshes never change it).
- **Re-add** an already-saved show → preserve My Data + Scoop, refresh public metadata via the same merge.

### 6.5 Data continuity across versions (`product_prd.md §5.11`)
Distinct from SQL migrations. `lib/domain/migrateModel.ts` holds an ordered chain of pure transforms `vN → vN+1`. On read (or a one-shot batch), if a user's `app_metadata.data_model_version` < current, apply transforms in order, persist, bump the version — **no My Data lost** (statuses/interest/tags/rating/scoop always carried forward). Baseline current version = 3.

### 6.6 Schema evolution artifacts (rider §3.3)
Plain SQL migration files in `supabase/migrations/*.sql` (timestamped), applied to the **hosted** DB via `supabase db push` or a tiny `node-postgres` runner — **no Docker needed**. Optional `supabase/seed.sql` fixtures. Goal: deterministic fresh DB state.

---

## 7. Identity, Namespace & Isolation (rider §§4–8)

- **`NAMESPACE_ID`** env var — one stable value per build; injected into every persisted row and every query filter. Two namespaces can never read/write each other's data.
- **User identity** — opaque stable string/UUID, no provider meaning encoded. `lib/identity/resolveIdentity.ts` resolves it per request:
  - **Dev/test:** accept `X-User-Id` header, or a dev-only "login as" selector, or fall back to `DEFAULT_USER_ID`. Clearly documented; gated behind `APP_MODE=development|test`.
  - **Production:** the same function reads the verified auth session (OAuth/JWT) instead. Because `user_id` already scopes every row, adopting OAuth is **wiring only, not a schema redesign** (rider §5.2).
- **Effective partition** = `(namespace_id, user_id)` everywhere.
- **Destructive reset** — `POST /api/test/reset` (dev/test only) and `npm run test:reset` delete rows where `namespace_id = $NAMESPACE_ID` (optionally `and is_test = true`). No global teardown. Cloud-agent path needs no privileged container access.

---

## 8. External Catalog Integration Layer

`lib/catalog/provider.ts` defines a vendor-agnostic interface; a TMDB-shaped adapter implements it. All calls are **proxied through server routes** so the catalog key stays server-side and payloads are mapped to domain objects before reaching the client.

Capabilities:
- `search(query)` → poster grid results (title, year, poster, id, media type).
- `getDetails(id, type)` → append credits, videos, images, recommendations, similar, watch/providers in one call; map → `Show` (persist-eligible fields) + transient attachments.
- `getPerson(id)` → bio, images, combined credits.
- `configuration()` / genre maps → resolve image base URLs and **genre id → display name** (schema stores genre *names*).
- `bestLogo()` deterministic selection (prefer English), per schema note.

Mappers (`toShow`, `toPerson`) live here and encode the schema's field-mapping rules: title preference (movie title / TV name; else reject), `show_type` inference, multi-format date parsing, provider IDs by region only, spoken-language codes, etc.

**Recommendation resolver** (`lib/domain/resolveRecommendation.ts`, shared by Ask/Alchemy/Explore): given AI output `title + externalId + mediaType`, look up by external ID (if present) and accept the **first result whose title matches case-insensitively** → real selectable `Show` carrying the AI "reason" as transient text. If unresolved → non-interactive label or Search handoff.

---

## 9. AI Integration Layer

`lib/ai/provider.ts` is a thin adapter (model + key from `cloud_settings` or env); all AI calls run **server-side**. Prompts are treated as **behavioral contracts** (per `ai_prompting_context.md`): a new implementation must reproduce the same *user-visible behavior* even if prompt wording/model changes. One consistent persona (§ `ai_voice_personality.md`), different modes per surface.

**Shared guardrails (every surface):** stay in TV/movies (redirect if asked to leave); spoiler-safe unless asked; opinionated + honest (acknowledge mixed reception, don't gush); specific vibe/craft reasoning over genre boilerplate; recommendations resolve to real items. Context inputs are surface-specific (library + My Data, current show, selected concepts, recent turns).

### 9.1 Surfaces
| Surface | Route | Output contract | Notes |
|---|---|---|---|
| **Scoop** | `ai/scoop` (streaming) | Mini "blog-post of taste": personal take → honest stack-up vs reviews → **The Scoop** centerpiece → fit/warnings → "Worth it?" verdict. ~150–350 words. | Streams progressively ("Generating…", never blank). Persist only if in collection; 4h freshness then regenerate on demand. |
| **Ask (chat)** | `ai/ask` | Structured `{ commentary, showList }`. `commentary` = user-facing text (no IDs). `showList` = `Title::externalId::mediaType;;…` exactly. | Friend-in-dialogue, 1–3 tight paragraphs + bulleted list when multi-rec; confident picks. Parser in `utils/showList.ts` must match format exactly. |
| **Summarize** | `ai/summarize` | 1–2 sentence summary preserving persona/tone. | Triggered after ~10 messages; older turns compressed, not sterilized. |
| **Concepts** | `ai/concepts` | Bullet list only; each concept 1–3 words, evocative, spoiler-free, no explanation. **8 by default.** | Diverse axes (structure/vibe/emotion/relationship/craft), ordered by strongest "aha." Multi-show: concepts **shared across all inputs**, from a **larger pool** (selection still capped at 8). Reject generic ("good characters"). |
| **Concept recs** | `ai/recommendations` | List of real shows + concise reasons (not synopses) that **name which concept(s)** align. | **Explore Similar = 5 recs; Alchemy = 6 recs.** Recent-bias but allow classics/hidden gems. Each rec runs through the resolver (§8). |

### 9.2 Persona modes (voice spec)
- **Warm, joy-forward, opinionated, spoiler-safe.** Tone sliders: ~70% friend / 30% critic; ~60% hype / 40% measured; playful↔serious adapts to the show ("emotional chameleon"); concise by default, lush for Scoop.
- **Search has no AI voice** (plain catalog).
- Language signatures: contractions, vivid vibe adjectives ("hopeful absurdity"), quick contrasts ("cozy but sharp"), "fit" framing ("perfect if you like… might not land if…"). Avoid encyclopedic tone, hedging walls, moralizing, listing a show without a reason.

### 9.3 Guardrails & fallbacks (`ai_prompting_context.md §5`)
- Structured parse fails → **retry once** with stricter formatting instructions → else fall back to unstructured commentary + Search handoff.
- Unresolvable recs → non-interactive / Search handoff.
- A lightweight **quality check** encodes the discovery rubric (voice ≥1, taste ≥1, **real-show integrity = 2 non-negotiable**, total ≥7/10) as a dev/test assertion harness for regression, not a runtime gate.

---

## 10. Domain Logic & Business Rules (pure, unit-tested)

Centralized in `lib/domain` / `src/utils` so every entry point behaves identically.

- **Collection membership** = row exists with non-nil `my_status`.
- **Save triggers** (`applySaveTriggers`): setting any status; choosing Interested/Excited; rating an unsaved show; adding ≥1 tag to an unsaved show.
- **Defaults on save:** status `Later` + interest `Interested`; **exception** — first save via **rating** → status `Done` (rating implies watched).
- **Interested/Excited chips** set `my_status=Later` **and** `my_interest=Interested|Excited` (they surface as primary chips though they are interest levels).
- **Interest applies only when Later**; if status leaves Later, interest becomes irrelevant (may be retained for return to Later).
- **Removal:** reselecting the active status → confirm → **delete row + clear all My Data** (status, interest, tags, rating, Scoop). Confirmation supports "stop asking" after repeated removals (`hide_status_removal_confirmation`, `status_removal_count`).
- **Timestamps:** every My field write stamps its `*_update_date`; used for recency sorting, sync conflict resolution, and Scoop freshness.
- **Overlay display rule:** `applyOverlay(show)` merges the user's saved My Data onto any catalog show before render — used by tiles, search results, AI recs, detail. User edits always win over refreshed public data.
- **Tile indicators:** in-collection badge when `my_status` exists; rating badge when `my_score` exists.

---

## 11. Feature-by-Feature Plan

Each page follows the fractal pattern; only key features/hooks/states/edge-cases are listed.

### 11.1 App shell & navigation (`app/layout.tsx`, `src/pages/*`)
- **Filters/navigation panel:** All Shows (default); one **tag filter per tag** + "No tags" when tagless shows exist; **data filters** (genre, decade, community-score ranges); persistent **Find/Discover** and **Settings** entry points. Persist `last_selected_filter`. (Model also supports `myStatus` filters — offered as an optional extension per Open Questions.)
- **Main content area:** Home, Detail, Find, Person, Settings.
- Providers: React Query, theme (+ font scale), identity context.

### 11.2 Collection Home (`src/pages/Home`)
- **Features:** `MediaTypeToggle` (All/Movies/TV, applied on top of any filter), `StatusSections`, `ShowTile`.
- **Grouping** (in order): **Active** (prominent/larger tiles) → **Excited** (Later+Excited) → **Interested** (Later+Interested) → **Others** collapsed (Wait, Quit, Done, unclassified Later without interest; hidden `Next` folded here/not surfaced). Grouping in `utils/grouping.ts`.
- Tiles: poster, title, My Data badges (in-collection, rating).
- **Empty states:** empty library → prompt to Search/Ask; filter yields none → "No results found."
- Hook `useCollection` (React Query) provides normalized saved shows for overlay + membership checks.

### 11.3 Search (`src/pages/Find/features/Search`)
- Text search by title/keywords → **poster grid**; in-collection items marked (overlay); select → Detail.
- **No AI voice.** Auto-open on launch when `auto_search` enabled.
- Live queries (no heavy pre-load/cache required per Non-Goals).

### 11.4 Show Detail (`src/pages/Detail`)
**Preserve section order** (`detail_page_experience.md §3`):
1. Header media carousel (backdrops/posters/logos/trailers; **motion prioritized, never blocks reading**; graceful poster/logo fallback).
2. Core facts (year, runtime **or** seasons/episodes) + **community score** bar.
3. **My Tags** chips + picker (adding a tag to unsaved show → auto-save Later+Interested).
4. Overview + **Scoop** toggle/stream (states: "Give me the scoop!" / "Show the scoop" / open "The Scoop"; streams; 4h freshness; persists only if saved).
5. **Ask about this show** CTA → enters Ask **seeded with this show's context** (handoff).
6. Genres + languages.
7. **Traditional recommendations** strand (low-effort next steps).
8. **Explore Similar:** Get Concepts → select 1+ (cap 8) → Explore Shows → **5 recs** with concept-cited reasons; changing selection clears downstream results.
9. Streaming availability ("Stream It"; provider IDs → provider metadata fetched separately).
10. Cast & Crew strands → **Person Detail**.
11. Seasons (**TV only**).
12. Budget vs Revenue (**movies, when available**).

**Toolbar (not in scroll body):** Status/Interest chips (Active / Interested / Excited / Done / Quit / Wait) — setting saves; **reselecting current status → removal confirmation**. **My Rating** bar — rating an unsaved show auto-saves as **Done**.

**Critical states:** unsaved (Scoop ephemeral until save; auto-save rules), no trailers/backdrops (premium poster/logo layout), TV vs movie section gating. Primary actions clustered early; long-tail info down-page/full-bleed to stay "powerful but not overwhelming."

### 11.5 Ask (`src/pages/Find/features/Ask`)
- Chat UI (user/assistant turns), friendly/opinionated/spoiler-safe.
- **Welcome:** 6 random starter prompts with refresh (from a starter-prompt pool).
- **Mentioned-shows strip:** parse `showList` → resolve to real shows (§8) → horizontal strip; tap → Detail (or Search handoff if mapping fails).
- **Summarization** of older turns after ~10 messages, persona-preserving.
- **Session-only** state (chat history + mentions cleared on reset/leave; nothing persisted).
- **Ask-about-a-show** variant: seeded with handoff show context on entry.

### 11.6 Alchemy (`src/pages/Find/features/Alchemy`)
Step-clear flow: select **2+** shows (library + global catalog) → **Conceptualize Shows** (shared multi-show concepts, larger pool) → select up to **8** catalysts → **ALCHEMIZE!** → **6 recs** with concept-cited reasons → **More Alchemy!** chains results as new inputs. Backtracking (changing shows/concepts) **clears downstream** results. Session-only.

### 11.7 Explore Similar — covered as Detail §8 (single-show concepts → 5 recs), sharing the concept/rec components with Alchemy.

### 11.8 Person Detail (`src/pages/Person`)
- Image gallery, name, bio.
- **Analytics charts:** average project ratings, top genres, projects-by-year (computed from credits).
- **Filmography grouped by year**; select a credit → Show Detail.
- Persons are transient catalog fetches (not collection items).

### 11.9 Settings & Your Data (`src/pages/Settings`)
- **App:** font size (XS–XXL → drives theme scale), Search-on-launch.
- **User:** username (synced).
- **AI:** provider API key (benchmark: may come from env; storing/syncing user-entered keys optional and **never committed**), model selection (synced).
- **Integrations:** catalog provider API key (synced).
- **Export/Backup:** "Export My Data" → `.zip` containing JSON of all saved shows + My Data, **dates ISO-8601** (via `export/route.ts`).
- **Import/Restore:** not in current scope; stub/flagged as an Open Question (see §18).

---

## 12. Cross-Cutting UI Concerns
- **Theming & font scale:** tokens in `src/theme` (CSS vars); font-size setting sets a root scale variable → all type sizes derive from it. No hex/px in TSX.
- **State:** server state via React Query (disposable); session AI state via feature-scoped context; overlay via `useOverlay`/`applyOverlay`.
- **Loading/error/empty:** every data surface has explicit states; AI surfaces stream/skeleton rather than block; network failures handled (no offline mode required).
- **Accessibility & copy:** playful, low-friction tone; destructive actions (removal) are the only modal walls.

---

## 13. Testing Strategy
- **Unit (Vitest, adjacent to source):** merge rules (`selectFirstNonEmpty` + timestamp resolution), save triggers/defaults (incl. rating→Done), removal clears all My Data, overlay precedence, status grouping, `showList` parser, rec resolver (case-insensitive title match), date/ISO encoding, data-model migration chain.
- **AI contract tests:** concept output (bullet-only, 1–3 words, 8, non-generic), rec counts (5/6) + concept-citation, mentions structure + retry-once fallback, spoiler-safety/domain redirect, discovery rubric harness (real-show integrity hard-fail).
- **Integration (Playwright):** namespace isolation (two namespaces don't cross-read), identity injection, save/re-add/remove journeys, auto-save (rate→Done, tag→Later+Interested), export zip shape + ISO dates, **`test:reset` scoped to namespace**.
- **Visual (Playwright):** Home grouping, Detail section order/toolbar, Ask strip, Alchemy steps, Person analytics. Visual testing preferred where protective.

---

## 14. Environment & Developer Experience (rider §3)
- **`.env.example`** with all vars + short comments: `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY` (server-only), `NAMESPACE_ID`, `DEFAULT_USER_ID`, `APP_MODE`, `CATALOG_API_KEY`, `AI_API_KEY`, `AI_MODEL`.
- **`.gitignore`** excludes `.env*` except `.env.example`.
- **Runs by filling env only — no source edits.**
- **Scripts:** `npm run dev` (start), `npm test` (unit+integration), `npm run test:reset` (namespace-scoped data reset), plus `db:push`/`db:migrate` for schema. Docker never required; documented as optional for local Supabase.

---

## 15. Security & Secrets
- Browser only ever holds **public/anon** values; **service role + catalog/AI keys are server-only** (route handlers). Settings API never returns raw stored keys to the client (write-only / masked).
- All persistence and provider calls flow through the server trust boundary.
- RLS staged for defense-in-depth and OAuth readiness.

---

## 16. Phased Delivery Plan (dependency-ordered)

| Phase | Deliverable | Depends on |
|---|---|---|
| **0 — Foundation** | Next.js app, env interface, `.env.example`/`.gitignore`, Supabase server client, identity middleware, `NAMESPACE_ID`, migrations + `shows`/settings tables, `test:reset`. | — |
| **1 — Data core** | `Show` mapping, merge engine, save-trigger/default engine, timestamps, collection CRUD API, overlay, model-migration chain. | 0 |
| **2 — Catalog** | Catalog adapter + proxy routes (search/details/person), genre/image config, rec resolver. | 1 |
| **3 — Collection UI** | Home (grouping + media toggle + tiles/badges + empty states), filters panel + persistence, Search. | 1–2 |
| **4 — Detail** | Full Detail (sections + toolbar saves + rating/tag auto-save + streaming + cast/crew + seasons/financials), traditional recs. | 2–3 |
| **5 — AI core** | AI adapter, persona/guardrails, Scoop (streaming + persistence/freshness). | 4 |
| **6 — Concepts & discovery** | Concepts (single/multi), Explore Similar (5), Alchemy loop (6 + chaining), Ask (chat + mentions + starters + summarization + seeded handoff). | 5 |
| **7 — Person & Settings** | Person Detail + analytics; Settings (all groups) + Export zip. | 4–6 |
| **8 — Hardening** | Full test suites, visual baselines, RLS policies, docs/README, quality-bar regression harness. | all |

---

## 17. Key Risks & Mitigations
- **AI real-show integrity (hallucinated titles/IDs)** → resolver + retry-once + non-interactive/Search fallback + rubric hard-fail in tests.
- **Namespace/user leakage** → single enforced query filter path + staged RLS + isolation integration tests.
- **Persona drift across surfaces / into genre-speak** → shared persona module, contract tests, "off-brand smell" checks (reject generic concepts).
- **Merge data loss on catalog refresh/sync** → `selectFirstNonEmpty` + timestamp resolution, heavily unit-tested; My fields never clobbered.
- **Secret leakage** → server-only key handling, masked settings responses, `.env*` gitignored.
- **Docker assumption creep** (Supabase CLI) → hosted DB + `db push`/SQL runner; Docker optional only.
- **Structured `showList` parser mismatch** → single canonical format constant shared by prompt + parser; exact-match tests.

---

## 18. Open Questions (from PRD) & Recommended Resolutions
- **`Next` as first-class status?** Keep in model, hidden in UI for now (fold into Others). Revisit post-launch.
- **Named custom lists beyond tags?** Out for v1; tags cover the need.
- **Scoop on unsaved show auto-saves?** No — keep Scoop ephemeral until an explicit save trigger; least surprising.
- **Explicit `Unrated` state vs nil?** Use nil `my_score` = unrated for v1 (schema-aligned); revisit if UI needs a distinct state.
- **Import/Restore from export zip?** Not implemented now; design the export JSON to be round-trippable so import is a later additive feature.
- **Save/share Alchemy "blends"?** Out for v1 (session-only), but concept-selection state is structured to allow persistence later.
- **Explicit `myStatus` sidebar filters?** Model supports it; offer as a low-cost optional filter.

---

## 19. Requirement Traceability (by PRD area → plan section)

| PRD area | Source | Plan coverage |
|---|---|---|
| Benchmark runtime & isolation | `infra_rider_prd.md` | §3, §5, §6.6, §7, §14, §15 |
| Collection data & persistence | `product_prd.md §4–5`, `storage-schema.*` | §6, §10 |
| Merge & data continuity | `storage-schema.md`, `product_prd.md §5.5/5.10/5.11` | §6.4, §6.5, §10 |
| App navigation & Discover shell | `product_prd.md §6` | §11.1, §11.5–11.6 |
| Collection Home & Search | `product_prd.md §7.1–7.2` | §11.2, §11.3 |
| Show Detail & relationship UX | `detail_page_experience.md`, `product_prd.md §7.5` | §11.4, §10 |
| Ask chat | `product_prd.md §7.3`, `ai_prompting_context.md` | §9.1, §11.5 |
| Concepts / Explore Similar / Alchemy | `concept_system.md`, `product_prd.md §7.4/4.7–4.8` | §9.1, §11.4(8), §11.6–11.7 |
| AI voice, persona & quality | `ai_voice_personality.md`, `discovery_quality_bar.md` | §9.2, §9.3, §13 |
| Person Detail | `product_prd.md §7.6` | §11.8 |
| Settings & Export | `product_prd.md §7.7` | §11.9, §14 |
| Cross-cutting principles | `product_prd.md §8` | §2, §10, §12, §15 |

---

## 20. Definition of Done (rider §9 + product acceptance)
- Configures via `.env` with **no code edits**; `.env.example` complete; secrets server-only.
- Repeatable runs with **no data collisions** (namespace isolation); destructive `test:reset` scoped to namespace, no global teardown.
- **Every user-owned record carries `user_id`**; partitioned by `(namespace_id, user_id)`.
- Real OAuth adoptable **without schema redesign**.
- All PRD features implemented with the **user overlay winning everywhere**, AI recs **resolving to real shows**, the **persona consistent** across surfaces, and **My Data preserved** across catalog refresh, sync, and model upgrades.
- Export produces a valid `.zip` (JSON, ISO-8601 dates); backend remains source of truth (clearing client cache loses nothing).
```
