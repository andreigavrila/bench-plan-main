# Implementation Plan — Personal TV/Movie Companion App

Status: Planning only (per `1-START_HERE.md`). No source files, schemas, or app code have been created. This document is the sole deliverable.

Sources read in full: `docs/prd/product_prd.md`, `docs/prd/infra_rider_prd.md`, `docs/prd/supporting_docs/ai_prompting_context.md`, `ai_voice_personality.md`, `concept_system.md`, `detail_page_experience.md`, `discovery_quality_bar.md`, `technical_docs/storage-schema.md`, `technical_docs/storage-schema.ts`. Architecture conventions taken from `INSTRUCTIONS.md` (Fractal Architecture) as directed by `CLAUDE.md`.

---

## 0. Scope & Reading Note

The product PRD is intentionally name/platform/technology-agnostic; the Infrastructure & Execution Rider pins this benchmark round to **Next.js + Supabase, Docker-free, namespace-isolated, multi-tenant-ready**. This plan treats the rider's constraints as hard requirements and the product PRD's behaviors as the functional target, and resolves every place the two intersect (e.g., how a single-user client schema becomes a multi-tenant server schema).

The product PRD's §12 references three companion documents — `where_is_the_heart_opus.md`, `ai_personality_opus.md`, `philosophy_opus.md` — that are **not present in this repository** (confirmed via repo-wide search). Their described contents (voice/personality detail, the 80 starter prompts, product philosophy) are treated as **absent source material**, not silently ignored. Where those docs would normally be authoritative (e.g., the exact 80 Ask starter prompts, verbatim system prompts), this plan substitutes the next-best available source (`ai_voice_personality.md`, `ai_prompting_context.md`, `concept_system.md`) and flags the gap explicitly in §14/§15 rather than inventing content and presenting it as spec-derived.

---

## 1. Executive Summary

Build a personal TV/movie collection + AI discovery app on **Next.js (App Router) + Supabase (Postgres)**. Users maintain a personal overlay ("My Data": status, interest, tags, rating, AI Scoop) on top of a public catalog. Four discovery paths — Search, Ask (chat), Alchemy (multi-show concept blending), Explore Similar (single-show concepts) — all funnel into the same collection model, and every AI recommendation must resolve to a real, selectable catalog item.

The architecture centers on four pillars that recur throughout this plan:

1. **One overlay-merge function, used everywhere a show is displayed** — so "user's version always wins" (PRD §8.1) can't drift between Search, Detail, AI mentions, and recommendations.
2. **A domain service layer owning every save/default/removal rule** (PRD §5.2–§5.4), independent of UI and independent of Postgres specifics, so the subtle auto-save semantics are implemented once and unit-tested directly.
3. **Namespace + user_id as non-optional dimensions on every persisted row**, enforced at the data-access layer, not just convention (rider §4).
4. **A shared AI persona + shared "resolve AI reference to a real show" pipeline**, reused by Ask mentions, Explore Similar, and Alchemy, so voice consistency and real-show integrity (PRD §8.2, discovery_quality_bar §1.5) are structural guarantees rather than per-surface prompt hygiene.

---

## 2. Assumptions, Interpretations & Resolved Ambiguities

The PRD is thorough but leaves some implementation-level decisions open by design ("implementation-defined," Open Questions). Rather than leaving these as loose threads, this plan takes an explicit position on each. Full Open-Questions dispositions are in §14; the interpretive/technical ones are below.

| # | Ambiguity | Decision | Rationale |
|---|---|---|---|
| A1 | `Show.id` uniqueness across movie/TV catalogs (many catalog providers number movies and TV series in independent ID spaces) | Internal `shows.id` is a deterministic composite key: `{catalogSource}:{mediaType}:{externalId}` (e.g. `tmdb:movie:550`) | Prevents silent collisions between a movie and a TV series that happen to share a numeric external ID. `externalIds` still stores the raw provider ID(s) for outbound lookups. |
| A2 | Concept generation count: `concept_system.md` says multi-show should return "a larger pool" than single-show; `discovery_quality_bar.md` states a flat default of 8 | Single-show (Explore Similar): generate **8** concepts (matches the quality bar exactly). Multi-show (Alchemy): generate **12**, but the UI selection cap stays **8** on both surfaces | Reconciles both docs instead of picking one silently: the "default 8" in the quality bar reads as the single-show baseline the doc actually measures; Alchemy's explicit "larger pool" instruction is honored by generating more candidates while the shared selection cap (already stated for Alchemy) is applied uniformly. |
| A3 | Wire format for AI-generated recommendations (Explore Similar / Alchemy) is unspecified, unlike Ask's `showList` format which is exact | Ask's `commentary`/`showList` (`Title::externalId::mediaType;;...`) is implemented **verbatim** as specified (parity requirement). Concept-recommendations use **structured JSON** (`{title, externalId, mediaType, reason}[]`) since no wire format is mandated and JSON is materially more robust to parse for a payload that also carries a `reason` string per item | Only Ask's format is explicitly prescribed ("the structured format and the parser must exactly match"); everywhere else is implementation-defined, so the more robust option is used without deviating from anything the PRD actually pins down. |
| A4 | Catalog + AI provider identity | Concrete default adapters: **TMDB-shaped** catalog provider (the schema's fields — posters/backdrops/logos, genres-as-names, budget/revenue, seasons, `flatrate/rent/buy` provider IDs by country, `externalIds` — map directly to a TMDB-style API), and a configurable **LLM provider** behind an interface, defaulting to whatever `AI_PROVIDER`/`AI_MODEL` env vars specify | PRD explicitly keeps vendor specifics out of scope, but a plan needs a concrete target to be buildable. Both are implemented behind interfaces (`CatalogProvider`, `AIProvider`) so the concrete choice is swappable without touching call sites — satisfies the rider's "not permanent" framing (stated for Supabase/auth, applied here by extension). |
| A5 | Person (`showType: "person"`) is **not** a persisted entity | Person/cast/crew data is always fetched live from the catalog provider and never written to the `shows` table | `storage-schema.md` explicitly lists `cast`, `crew` as transient/not-stored. The `"person"` value in `ShowType` is read as a tagging artifact of multi-type search decoding (a search endpoint mixing movies/TV/people), not an instruction to cache people as shows. |
| A6 | Chat/session AI state persistence | Ask and Alchemy sessions are **not** persisted server-side at all — transcript/session state lives in client memory only, sent to stateless API routes each turn | Directly matches PRD §5.7 ("Session only... Cleared when resetting/leaving"). Avoids building and then immediately discarding a server-side session store. |
| A7 | Namespace scoping of the catalog cache | The `shows` cache table is **namespace-scoped**, not global | Rider §4.1 says a namespace must partition "all persisted data" and destructive tests must stay scoped to one namespace. A cached catalog row could be mutated by a destructive test; scoping it avoids any cross-namespace bleed at the cost of duplicate cache rows across namespaces. Documented as a deliberate tradeoff — a global unscoped cache (keyed only by the composite external id) is a valid future optimization once isolation is proven safe in tests, not a v1 default. |

---

## 3. Technology Stack & High-Level Architecture

Per the Infrastructure Rider (non-negotiable for this round):

- **Runtime:** Next.js (latest stable), App Router, TypeScript strict mode. Next.js Route Handlers serve as the server boundary — the browser never talks to Supabase directly.
- **Persistence:** Supabase (Postgres), accessed via `@supabase/supabase-js`. Hosted instance is the primary target (cloud-agent-friendly); local Supabase via CLI is a documented developer convenience, never a requirement (no Docker dependency assumed).
- **Data fetching/caching (client):** TanStack Query for server-state caching + invalidation. This is the "clients may cache for performance" layer (rider §6.1) — it is never the source of truth; every mutation invalidates the relevant query keys, and clearing it (e.g., reinstall) loses nothing (rider §6.2).
- **Styling:** Tailwind CSS driven entirely by tokens defined in `src/theme/` (no literal hex/px values in components — see §7 and `INSTRUCTIONS.md`).
- **Validation:** Zod schemas at every API boundary (request bodies, AI structured outputs, import/export payloads).
- **AI:** Provider-agnostic `AIProvider` interface (complete / stream / completeStructured), default adapter targets the configured Claude model; swappable per §2/A4.
- **Testing:** Vitest + React Testing Library (unit/component), Playwright (E2E/visual smoke).

### 3.1 Request Flow

```
Browser (Next.js client components)
   │  fetch("/api/...")            — no direct Supabase calls from the browser
   ▼
Next.js Route Handlers (server)
   │  1. resolve (namespace_id, user_id) from dev-identity middleware
   │  2. call domain/service layer (collection rules, AI orchestration, catalog proxy)
   ▼
Data-access layer (repository functions — every query takes namespace_id + user_id explicitly)
   │
   ▼
Supabase Postgres  ◄──────────────►  External Catalog Provider (TMDB-shaped)
                                     External AI Provider (Claude, via AIProvider)
```

Why server-mediated instead of direct client-to-Supabase: the dev-mode identity mechanism (rider §5.1) is a header/selector, not a real Supabase Auth session, so Postgres RLS keyed on `auth.uid()` cannot enforce isolation yet. Routing everything through the server lets the data-access layer enforce `(namespace_id, user_id)` scoping in code today, with RLS enabled as defense-in-depth, and gives a clean seam to flip to direct-client + `auth.uid()`-based RLS later (see §4.3) without a schema change (rider §5.2).

### 3.2 Directory Structure (Fractal Architecture, per `INSTRUCTIONS.md`)

Next.js's file-system router stays thin; real page composition lives under `src/pages/` per the mandated Pages → Features → Sub-Features pattern.

```
src/
├── app/                              # Next.js App Router — thin route files only
│   ├── (collection)/page.tsx         # renders src/pages/CollectionHomePage
│   ├── find/page.tsx                 # renders src/pages/FindDiscoverPage
│   ├── show/[id]/page.tsx            # renders src/pages/ShowDetailPage
│   ├── person/[id]/page.tsx          # renders src/pages/PersonDetailPage
│   ├── settings/page.tsx             # renders src/pages/SettingsPage
│   └── api/                          # route handlers (see §6)
├── pages/
│   ├── CollectionHomePage/
│   │   ├── CollectionHomePage.tsx
│   │   └── features/
│   │       ├── StatusSections/{ActiveSection,ExcitedSection,InterestedSection,OtherStatusesGroup}/
│   │       └── FiltersSidebar/features/{TagFilters,DataFilters,MediaTypeToggle}/
│   ├── FindDiscoverPage/
│   │   ├── FindDiscoverPage.tsx
│   │   └── features/
│   │       ├── ModeSwitcher/
│   │       ├── SearchMode/
│   │       ├── AskMode/features/{ChatThread,MentionedShowsStrip,StarterPrompts}/
│   │       └── AlchemyMode/features/{ShowPicker,ConceptSelector,RecommendationResults}/
│   ├── ShowDetailPage/
│   │   ├── ShowDetailPage.tsx
│   │   └── features/
│   │       ├── HeaderMediaCarousel/
│   │       ├── CoreFactsRow/
│   │       ├── MyRelationshipControls/features/{StatusChips,RatingSlider,TagPicker}/
│   │       ├── OverviewAndScoop/features/{ScoopToggle,ScoopStream}/
│   │       ├── AskAboutShowCta/
│   │       ├── RecommendationsStrand/
│   │       ├── ExploreSimilar/features/{ConceptChips,ExploreShowsResults}/
│   │       ├── StreamingAvailability/
│   │       ├── CastCrewStrands/
│   │       ├── SeasonsStrand/            # TV only
│   │       └── BudgetRevenue/            # movie only, when available
│   ├── PersonDetailPage/
│   │   └── features/{ImageGallery,Bio,AnalyticsCharts,FilmographyByYear}/
│   └── SettingsPage/
│       └── features/{AppSettings,UserSettings,AISettings,IntegrationSettings,YourDataSettings}/
├── components/                       # shared primitives: PosterTile, Chip, Slider, Modal, etc.
├── hooks/                            # global hooks: useCurrentUser, useNamespace, useMediaTypeFilter
├── theme/                            # design tokens (no hex/px in TSX)
├── config/                           # env access, enums, numeric constants (see table below)
└── lib/
    ├── supabase/                     # server-only client factory (service-role + scoped role)
    ├── catalog/                      # CatalogProvider interface + TMDB-shaped adapter
    ├── ai/
    │   ├── provider.ts               # AIProvider interface
    │   ├── prompts/                  # basePersona.ts + per-surface prompt builders
    │   └── resolution/               # shared "AI reference → real Show" resolver + retry/fallback
    ├── collection/                   # domain service: save/merge/remove/defaults (pure, unit-tested)
    └── export/                       # backup zip/JSON builder (+ import, phase 4)
```

All shared numeric/behavioral constants live in one place (`src/config/constants.ts`) so the "magic numbers" the PRD does specify are defined once:

| Constant | Value | Source |
|---|---|---|
| `SCOOP_FRESHNESS_HOURS` | 4 | PRD §4.9 / §5.7 |
| `ASK_SUMMARIZE_AFTER_TURNS` | 10 | PRD §7.3 |
| `ASK_STARTER_PROMPT_COUNT` | 6 (shown), pool TBD (see §14) | PRD §7.3 |
| `EXPLORE_SIMILAR_CONCEPT_COUNT` | 8 | discovery_quality_bar §2.3 |
| `ALCHEMY_CONCEPT_POOL_COUNT` | 12 | resolved in §2/A2 |
| `MAX_SELECTED_CONCEPTS` | 8 | concept_system.md §5 |
| `EXPLORE_SIMILAR_REC_COUNT` | 5 | concept_system.md §6 |
| `ALCHEMY_REC_COUNT` | 6 | concept_system.md §6 |
| `ALCHEMY_MIN_STARTING_SHOWS` | 2 | PRD §4.7 |

---

## 4. Identity, Namespace & Multi-Tenancy Model

### 4.1 Dimensions

Every persisted row carries **both**:
- `namespace_id` — build/run isolation primitive (rider §4.1). Not user-facing.
- `user_id` — opaque UUID, forward-compatible with a future `auth.users.id` (rider §4.2).

Effective partition key everywhere: **`(namespace_id, user_id)`**.

### 4.2 Resolution (Dev-Mode Identity Injection)

A single middleware (`src/lib/identity/resolveIdentity.ts`) runs before every API route:

1. `namespace_id` = `X-Namespace-Id` header if present, else `NAMESPACE_ID` env var (one running instance ⇒ one default namespace; header override supports local multi-namespace testing).
2. `user_id` = `X-User-Id` header if present, else the namespace's default dev user (created by seed data, rider §4.3 "a single default user MAY exist").
3. A dev-only "log in as…" selector UI (Settings-adjacent, gated by `ENABLE_DEV_AUTH` and `NODE_ENV !== 'production'`) lists/creates dev users within the current namespace and sets the header for subsequent requests via a cookie.

This mechanism is documented as temporary and clearly isolated to one module so that swapping it for real OAuth later (rider §5.2) means replacing `resolveIdentity()`'s internals with a Supabase Auth session lookup — no change to `user_id`'s type, no change to any table.

### 4.3 RLS Posture

RLS is **enabled on every table** from the first migration, with default-deny policies for `anon`/`authenticated` roles. All application traffic uses a server-side Supabase client (service role, or a scoped role granted explicit bypass) — the data-access layer, not Postgres policy, is the primary enforcement of `(namespace_id, user_id)` scoping during this phase, covered by isolation tests (§11). When real Supabase Auth lands, add `USING (auth.uid() = user_id)`-style policies per table and optionally allow direct client reads — additive, no schema redesign, satisfying rider §5.2.

### 4.4 Namespace Lifecycle & Destructive Testing

- `namespaces` table tracks known namespaces (id, label, created_at) purely for tooling/reset convenience.
- `npm run test:reset` truncates all namespace-scoped tables `WHERE namespace_id = $NAMESPACE_ID` (service role) and re-runs the seed for that namespace only — never a global teardown (rider §7).
- An orthogonal `is_test` boolean (carried over from the reference schema) marks synthetic/seeded rows within a namespace, letting seed fixtures be filtered out of exports or targeted individually without needing a whole-namespace reset.

---

## 5. Data Model & Persistence

### 5.1 Entity Overview

The reference client schema (`storage-schema.ts`) merges "catalog snapshot" and "user overlay" into one `Show` object because it was modeling a single-user local store. For a multi-tenant server, this plan splits it into a **shared-shape catalog cache** and a **per-user overlay**, joined at read time — this is what makes `(namespace_id, user_id)` partitioning possible without duplicating catalog metadata per user.

| Table | Purpose | Namespace-scoped? | User-scoped? |
|---|---|---|---|
| `namespaces` | Known build/run ids (tooling) | — (is the scope) | no |
| `app_users` | Dev-mode identity records (pre-OAuth) | yes | is the scope |
| `shows` | Catalog snapshot cache (public fields only) | yes (§2/A7) | no |
| `user_shows` | The collection / "My Data" overlay — **row existence = in-collection** (PRD §5.1) | yes | yes |
| `user_settings` | Synced app/AI/integration settings | yes | yes |

### 5.2 Schema Sketch

```sql
-- namespaces --------------------------------------------------------------
create table namespaces (
  id          text primary key,
  label       text,
  created_at  timestamptz not null default now()
);

-- app_users (dev-mode identity; superseded by auth.users post-OAuth) -------
create table app_users (
  id            uuid primary key default gen_random_uuid(),
  namespace_id  text not null references namespaces(id) on delete cascade,
  display_name  text not null,
  is_dev_user   boolean not null default true,
  created_at    timestamptz not null default now()
);

-- shows (catalog cache; composite external identity, see A1) --------------
create table shows (
  id                  text not null,          -- '{source}:{mediaType}:{externalId}'
  namespace_id        text not null references namespaces(id) on delete cascade,
  external_id         text not null,
  catalog_source      text not null default 'tmdb',
  show_type           text not null check (show_type in ('movie','tv','unknown')),
  title               text not null,
  overview            text,
  tagline             text,
  homepage            text,
  original_language   text,
  spoken_languages     text[] not null default '{}',
  languages            text[] not null default '{}',
  genres               text[] not null default '{}',
  poster_url           text,
  backdrop_url         text,
  logo_url             text,
  network_logos        text[] not null default '{}',
  vote_average         numeric,
  vote_count           integer,
  popularity           numeric,
  last_air_date        date,
  first_air_date       date,
  release_date         date,
  runtime               integer,
  budget                bigint,
  revenue               bigint,
  series_status         text,
  number_of_episodes    integer,
  number_of_seasons     integer,
  episode_run_time      integer[] not null default '{}',
  provider_data         jsonb,               -- { countries: { [cc]: {flatrate,rent,buy: number[]} } }
  details_update_date   timestamptz,
  created_at            timestamptz not null default now(),
  is_test               boolean not null default false,
  primary key (namespace_id, id)
);

-- user_shows (the collection overlay — existence implies myStatus) --------
create table user_shows (
  id                     uuid primary key default gen_random_uuid(),
  namespace_id           text not null references namespaces(id) on delete cascade,
  user_id                uuid not null references app_users(id) on delete cascade,
  show_id                text not null,
  my_status              text not null check (my_status in ('active','next','later','done','quit','wait')),
  my_status_update_date  timestamptz not null default now(),
  my_interest            text check (my_interest in ('excited','interested')),
  my_interest_update_date timestamptz,
  my_tags                 text[] not null default '{}',
  my_tags_update_date     timestamptz,
  my_score                numeric,
  my_score_update_date    timestamptz,
  ai_scoop                text,
  ai_scoop_update_date    timestamptz,
  creation_date           timestamptz not null default now(),
  is_test                 boolean not null default false,
  unique (namespace_id, user_id, show_id),
  foreign key (namespace_id, show_id) references shows(namespace_id, id) on delete cascade
);
create index user_shows_status_idx on user_shows (namespace_id, user_id, my_status);
create index user_shows_tags_idx   on user_shows using gin (my_tags);

-- user_settings (synced across devices, per user) --------------------------
create table user_settings (
  user_id                     uuid primary key references app_users(id) on delete cascade,
  namespace_id                text not null references namespaces(id) on delete cascade,
  username                    text not null,
  font_size                   text not null default 'M' check (font_size in ('XS','S','M','L','XL','XXL')),
  auto_search                 boolean not null default false,
  ai_provider                 text,
  ai_model                    text,
  ai_api_key_encrypted        text,           -- optional user-supplied override; see §5.4
  catalog_api_key_encrypted   text,
  updated_at                  timestamptz not null default now()
);
```

Ephemeral UI-only state (status-removal nag counters, last-selected filter) is **client-local only** (not a DB table) — it's cosmetic, not enumerated among the PRD's "synced across devices" settings, and is safe to lose on cache clear per rider §6.2.

### 5.3 Business-Rule Functions (pure, unit-tested, called by the API layer)

All of PRD §5's rules live in `src/lib/collection/` as pure functions operating on plain data, independent of Postgres — this is what makes the subtle default/merge rules directly testable:

| Function | Encodes |
|---|---|
| `computeSaveDefaults(trigger)` | §5.3 — status set → as given; interest chip → status=`later` + given interest; rating an unsaved show → status=`done`; tag added to unsaved show → status=`later` + interest=`interested`. |
| `mergeCatalogSnapshot(existing, incoming)` | storage-schema.md merge policy — non-`my*` fields via `selectFirstNonEmpty` (never overwrite non-empty with empty/nil); `details_update_date` set to now. |
| `mergeUserOverlay(existing, incoming)` | Per-field timestamp resolution for `my*` fields (§5.5/§5.6) — newer `*_update_date` wins per field independently, not as a whole-row comparison. |
| `isInCollection(userShowRow)` | §5.1 — row exists ⟺ in collection (existence check only; `my_status` is NOT NULL by constraint). |
| `computeRemoval()` | §5.4 — full row delete (status, interest, tags, rating, scoop all cleared together), gated by confirmation UX with a "stop asking" escape hatch driven by client-local nag state. |
| `getDisplayShow(catalogRow, overlayRow | null)` | §8.1 "user's version always wins" — the **single** merge-for-display function used by every surface (tiles, search results, AI mentions, recommendation cards). No surface is allowed to hand-roll this. |

### 5.4 Settings & Secret Handling

- Server-default AI/catalog API keys come from env vars (`AI_API_KEY`, `CATALOG_API_KEY`) and are never sent to the browser.
- A user may optionally override with their own key in Settings; if stored, it is encrypted at the application layer using a server-only symmetric key (`SETTINGS_ENCRYPTION_KEY` env var) before being written to `user_api_key_encrypted` columns — never logged, never included in exports (§9.6 below explicitly excludes it from the backup zip).
- Per PRD §7.7, storing/syncing a user-entered key is optional; if the encryption dependency isn't ready in early phases, the Settings field is present but a request without an env-default and without a stored key returns a clear "no AI key configured" state rather than silently failing.

### 5.5 Migration & Continuity Policy (PRD §5.11)

- Supabase CLI migrations (`supabase/migrations/NNNN_*.sql`), strictly additive/backward-compatible: new columns nullable or defaulted, no destructive drops without a preceding data-migration step.
- `is_test`/seed fixtures live in `supabase/seed.sql`, applied per namespace, never mixed with migration files.
- Because user data lives server-side (not on-device), "preserve libraries across app updates" reduces to "never ship a breaking migration" — there is no client-side data model to version-migrate the way the original single-device schema needed (`AppMetadata.dataModelVersion`). This is called out explicitly since it's a meaningful simplification the server architecture buys us over the original client-only design.

---

## 6. API Surface

All routes are Next.js Route Handlers under `src/app/api/`, all server-side, all resolve `(namespace_id, user_id)` via the identity middleware (§4.2) before touching data.

### 6.1 Catalog (proxied, transient, not user-scoped)

| Route | Purpose |
|---|---|
| `GET /api/catalog/search?q=&mediaType=` | Text search; results annotated with `isInCollection` + overlay via `getDisplayShow` |
| `GET /api/catalog/shows/:id` | Full detail: live fetch + merge into `shows` cache (§2/A7), overlay applied if saved |
| `GET /api/catalog/shows/:id/credits` \| `/videos` \| `/recommendations` \| `/similar` \| `/providers` | Transient sub-resources, never persisted |
| `GET /api/catalog/people/:id` | Person bio/gallery/credits — always live, never cached (§2/A5) |

### 6.2 Collection

| Route | Purpose |
|---|---|
| `GET /api/collection?filter=&mediaType=` | Grouped library (join `shows` + `user_shows`), drives Collection Home sections |
| `GET /api/collection/tags` | Distinct tags + whether any tagless shows exist (drives "No tags" filter) |
| `GET /api/collection/filters/meta` | Available genres/decades/score bands for Data Filters |
| `PUT /api/collection/:showId/status` | Set status; applies `computeSaveDefaults` if unsaved |
| `PUT /api/collection/:showId/interest` | Set interest chip → status=later + interest (auto-save) |
| `PUT /api/collection/:showId/tags` | Add/replace tags; first tag on an unsaved show auto-saves as later+interested |
| `PUT /api/collection/:showId/rating` | Set rating; auto-saves as done if unsaved |
| `DELETE /api/collection/:showId` | Full removal — clears status/interest/tags/rating/scoop together |

### 6.3 AI

| Route | Purpose |
|---|---|
| `POST /api/ai/scoop/:showId` | Streams Scoop; returns cached copy if `< SCOOP_FRESHNESS_HOURS` old and show is saved; persists on completion only if saved |
| `GET /api/ai/ask/starters` | Returns 6 random prompts from the seeded starter pool (§14) |
| `POST /api/ai/ask` | Stateless chat turn: client sends full/summarized transcript + optional handoff show; server streams `commentary`, resolves `showList` into real shows server-side before the client renders the mentioned-shows strip |
| `POST /api/ai/explore/concepts` | Single-show concepts (8) |
| `POST /api/ai/explore/recommendations` | Concept-steered recs (5), resolved to real shows |
| `POST /api/ai/alchemy/concepts` | Multi-show shared concepts (pool of 12) |
| `POST /api/ai/alchemy/recommendations` | Concept-steered recs (6), resolved to real shows |

### 6.4 Settings, Export, Dev Identity

| Route | Purpose |
|---|---|
| `GET/PUT /api/settings` | `user_settings` row — username, font size, auto-search, AI/catalog provider + optional keys, AI model |
| `GET /api/export` | Streams a `.zip` containing an ISO-8601-dated JSON backup of the caller's `shows` (saved subset) + `user_shows` |
| `POST /api/import` | Phase-4 stretch — see §12/§14 |
| `GET/POST /api/dev/users` | Dev-only, gated by `ENABLE_DEV_AUTH` + non-production; lists/creates dev users in the current namespace for the "log in as" selector |

---

## 7. Frontend Architecture Notes

Directory layout is in §3.2. Applying `INSTRUCTIONS.md`'s standards concretely:

- **Humble components:** every `FeatureName.tsx` only renders markup and wires handlers; all state/effects/business logic live in a co-located `useFeatureName()` hook (e.g., `MyRelationshipControls/hooks/useMyRelationshipControls.ts` calls the `/api/collection/:showId/*` endpoints via TanStack Query mutations and exposes `{ status, interest, setStatus, setInterest, isRemoving, confirmRemoval }`).
- **No magic numbers/inline styles:** all the constants in §3.2's table live in `src/config/constants.ts`; all colors/spacing/typography reference `src/theme/tokens.ts` → Tailwind theme extension, never literals in TSX.
- **Co-location:** e.g. `ExploreSimilar` is only meaningful inside `ShowDetailPage`, so it lives at `ShowDetailPage/features/ExploreSimilar/`, not promoted to a global feature.
- **Fractal consistency:** `AlchemyMode` under `FindDiscoverPage` follows the exact same Page → Feature → Sub-Feature shape as `ShowDetailPage`, even though it's reached via a mode switch rather than a route, so the same mental model applies everywhere.
- **Testing:** unit tests for every hook that wraps a `lib/collection` rule; component tests for `StatusChips`/`RatingSlider`/`TagPicker` (the three auto-save triggers); Playwright smoke tests for the ten Key User Journeys (§13).

---

## 8. AI Subsystem

### 8.1 Shared Persona Foundation

`src/lib/ai/prompts/basePersona.ts` encodes, once, the non-negotiable voice pillars from `ai_voice_personality.md`: joy-forward/warm, opinionated honesty (say when reception is mixed, never gush), vibe-first + spoiler-safe by default, specific-not-generic, concise-by-default. Every surface-specific prompt builder composes this base rather than restating it, so a voice tweak happens in one place. `Search` explicitly imports none of this (PRD: "Search has no AI voice").

### 8.2 Per-Surface Contracts

| Surface | Input | Output contract | Notes |
|---|---|---|---|
| Scoop | show + (if saved) library context | Free text: personal take → honest stack-up → centerpiece "Scoop" paragraph → fit/warnings → verdict; ~150–350 words | Streamed token-by-token; persisted only if saved (§8.4) |
| Ask | transcript (+ summary of turns beyond 10) + optional handoff show | `{ commentary: string, showList: "Title::externalId::mediaType;;..." }` | Exact wire format per PRD (§2/A3); commentary streams, `showList` resolved server-side after stream completes |
| Concepts (single/multi) | 1 show, or 2+ shows for Alchemy | Bullet list, 1–3 words each, no explanation | Multi-show concepts must reflect commonality across **all** inputs, not a union |
| Concept recommendations | selected concepts (≤8) + source show(s) | Structured JSON `{title, externalId, mediaType, reason}[]` | Reason must name the matching concept(s) explicitly (discovery_quality_bar §1.4) |

### 8.3 Shared Resolution Pipeline

`src/lib/ai/resolution/resolveShowReference.ts` is used by Ask mentions, Explore Similar recs, and Alchemy recs alike:

1. If `externalId` present → catalog lookup by ID.
2. Else → catalog search by title, accept the first **case-insensitive exact title match**.
3. If resolved → becomes a real, selectable `Show` (carrying the AI `reason`/mention context as transient display text, never persisted).
4. If unresolved → render non-interactive, or hand off to Search (PRD §5.8, ai_prompting_context.md §5).

Structured-output parsing failures (Ask's `showList`, or the recs JSON) get **one retry** with stricter formatting instructions before falling back to unstructured commentary + Search handoff — implemented once as `withStructuredRetry()` and reused by all three call sites, not re-implemented per surface.

### 8.4 Scoop Caching & Streaming

1. Request comes in for `showId`.
2. If the show is saved and `ai_scoop_update_date` is within `SCOOP_FRESHNESS_HOURS`, return the cached `ai_scoop` immediately (no generation).
3. Otherwise stream a fresh generation (SSE) so the client shows "Generating…" progressively rather than a blank wait (detail_page_experience.md §3.4).
4. On stream completion, persist `ai_scoop` + `ai_scoop_update_date` **only if** the show is (still) saved at that point; unsaved-show generations are fully ephemeral and never written.

### 8.5 Context Assembly ("Taste-Aware" Requirement)

`buildTasteContext(userId)` assembles a bounded summary for Ask/Alchemy/Explore Similar — not a raw dump of the whole library: most-recently-updated N saved shows (status/interest/tags/rating), plus tag/genre frequency counts. This keeps token usage predictable as a library grows while still satisfying "taste-aware AI" (PRD §8.3). The exact N is a tunable constant, not hardcoded logic, so it can be adjusted based on real token/quality tradeoffs during Phase 2.

### 8.6 Conversation Summarization

After `ASK_SUMMARIZE_AFTER_TURNS` (10) messages, the server summarizes the oldest turns into 1–2 sentences **in the same persona voice** (a small dedicated prompt, not a generic "system summary"), and returns the compacted transcript to the client to resend on the next turn — consistent with the stateless/session-only design (§2/A6).

---

## 9. Cross-Cutting Business Rules → Implementation Mapping

Direct traceability from PRD §8's principles to concrete mechanisms, so none of them stay as unimplemented intent:

| Principle (PRD §8) | Mechanism |
|---|---|
| 1. User's version precedence everywhere | Single `getDisplayShow()` (§5.3), used by every surface — no per-component reimplementation |
| 2. Discovery must be actionable | Shared `resolveShowReference()` pipeline (§8.3), used by all three AI-recommendation surfaces |
| 3. Taste-aware AI | `buildTasteContext()` (§8.5), one implementation feeding Ask/Alchemy/Explore Similar |
| 4. Spoiler-safe by default | Enforced in `basePersona.ts` (§8.1) + spot-checked by the golden set (§11) |
| 5. Implicit behaviors feel natural | `computeSaveDefaults()` (§5.3) unit-tested directly against PRD §5.2/§5.3's exact trigger list |
| 6. Your data is yours | Export is a Phase-1 (not backlog) feature; §6.4, §12 |
| 7. Identity explicit | `resolveIdentity()` middleware (§4.2) runs before every route; no table omits `user_id` |
| 8. Runs/builds isolated | `namespace_id` on every persisted table (§5.2) + isolation test suite (§11) |
| 9. Backend is source of truth | TanStack Query is cache-only (§3); no authoritative collection data in `localStorage` |

---

## 10. Infrastructure Rider Compliance Checklist

| Requirement | Plan reference |
|---|---|
| Next.js + Supabase baseline, no Docker requirement | §3 |
| `.env.example` + `.gitignore` secret exclusion | §5.4, env sketch below |
| One-command dev/test/reset scripts | §12 (Phase 0), table below |
| Repeatable schema (migrations + seed) | §5.5 |
| `namespace_id` isolation, destructive-testing scoped to a namespace | §4, §11 |
| `user_id` on every user-owned record | §5.2 |
| Dev identity injection, gated for production | §4.2 |
| Backend = source of truth; disposable client cache | §3, §9 |
| Straightforward path to real OAuth (no schema redesign) | §4.2, §4.3 |

Illustrative `.env.example` (documented here, not created — no files are written in this planning step):

```
# App runtime
NAMESPACE_ID=local-dev
NODE_ENV=development

# Supabase
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=        # reserved for future direct-client reads; unused by browser today
SUPABASE_SERVICE_ROLE_KEY=            # server-only, never bundled to the client

# Dev identity (benchmark mode only — must be unset/false in production)
ENABLE_DEV_AUTH=true
DEV_DEFAULT_USER_ID=

# Settings encryption (for optionally-stored user API keys)
SETTINGS_ENCRYPTION_KEY=

# AI provider (server default; per-user override lives in Settings)
AI_PROVIDER=anthropic
AI_API_KEY=
AI_MODEL=

# Catalog provider (server default; per-user override lives in Settings)
CATALOG_PROVIDER=tmdb
CATALOG_API_KEY=
```

Illustrative scripts (`package.json`, documented not created):

| Script | Behavior |
|---|---|
| `npm run dev` | `next dev` |
| `npm test` | Vitest (unit + integration) |
| `npm run test:e2e` | Playwright, against a running dev server + test namespace |
| `npm run test:reset` | Truncate all `namespace_id = $NAMESPACE_ID` rows via service role, re-seed |
| `npm run db:migrate` | Apply Supabase migrations |
| `npm run db:seed` | Apply `supabase/seed.sql` for the active namespace |

---

## 11. Testing Strategy

| Layer | Tool | Covers |
|---|---|---|
| Unit | Vitest | `computeSaveDefaults`, `mergeCatalogSnapshot`, `mergeUserOverlay`, `getDisplayShow`, `resolveShowReference`, showList/concept parsers |
| Component | React Testing Library | `StatusChips`, `RatingSlider`, `TagPicker` (the three auto-save triggers), `ScoopToggle` states (no scoop / cached / generating) |
| Integration | Vitest + test Supabase namespace | Full API routes; explicit **namespace isolation tests** (two namespaces, assert zero cross-visibility); re-add/merge-by-timestamp scenarios; removal clears all `my*` fields atomically |
| E2E / visual smoke | Playwright | The 10 Key User Journeys (§13) end to end against a seeded test namespace |
| AI quality | Manual + scripted golden set | Seed 8–10 scenarios across Scoop/Ask/Concepts/Alchemy/Explore Similar per `discovery_quality_bar.md`'s rubric (voice ≥1, taste alignment ≥1, **real-show integrity = 2 non-negotiable**, total ≥7/10); re-run before any prompt/model change ships |

`npm test` must be runnable without global teardown and without Docker, consistent with rider §7/§8 — the integration suite targets a disposable namespace, never the whole database.

---

## 12. Phased Delivery Plan

### Phase 0 — Foundations & Infra
- Next.js + TypeScript scaffold, lint/format config, theme tokens, `config/constants.ts`.
- Supabase project wiring, migrations (§5.2), seed script, `.env.example`.
- Identity middleware (§4.2) + data-access layer with mandatory `(namespace_id, user_id)` scoping.
- `dev` / `test` / `test:reset` / `db:migrate` / `db:seed` scripts.
- `CatalogProvider` interface + TMDB-shaped adapter; server-side proxy routes with BYO-key fallback to env default.

### Phase 1 — Collection Core (no AI)
- `mergeCatalogSnapshot`/`mergeUserOverlay`/`getDisplayShow`/`computeSaveDefaults` (unit-tested first).
- Collection domain service + `/api/collection/*` routes.
- Collection Home (grouped sections, media-type toggle, tile badges), Filters sidebar (tags incl. "No tags", genre/decade/score, media-type).
- Show Detail (all non-AI sections: header media, core facts, community score + rating, status/interest chips, tags, overview, recommendations strand, streaming availability, cast/crew, seasons, budget/revenue).
- Person Detail (gallery, bio, filmography by year, analytics charts).
- Search (catalog search + in-collection markers + "search on launch" setting).
- Settings (app/user/AI-key/catalog-key fields wired, even before AI calls exist) + Export.

### Phase 2 — AI Surfaces
- `AIProvider` interface + `basePersona` + per-surface prompt builders.
- Scoop end-to-end (cache/stream/persist-if-saved).
- Ask (general + "about this show" handoff, mentioned-shows resolution, starter prompts, 10-turn summarization).
- Explore Similar (concepts → selection → recs) on Show Detail.
- Alchemy (multi-show picker → concepts → selection → recs → chaining).
- Shared resolution pipeline (§8.3) wired into all three; retry/fallback guardrails.
- Seed the discovery-quality golden set (§11).

### Phase 3 — Cross-Cutting Hardening
- Namespace isolation test suite + destructive-reset verification (rider §7/§9).
- Multi-device merge/conflict simulation tests (§5.5/§5.6, §5.10).
- Migration-safety pass (additive-only checklist, §5.5).
- Font-size/accessibility wiring, responsive layout pass.
- Playwright smoke tests across all 10 Key User Journeys.
- Finalize `.env.example`, README/dev docs.

### Phase 4 — Stretch / Deferred (see §14 for rationale per item)
- Import/Restore from export zip.
- Explicit `myStatus` sidebar filters.
- `Next` as a first-class UI status.
- Named custom lists beyond tags.
- Expand Ask starter-prompt pool toward the PRD-referenced 80 (content work, not architecture — see §15).

---

## 13. Key User Journeys → Acceptance Criteria

Directly from PRD §9, each mapped to the phase and surface that must satisfy it, for use as Playwright smoke-test targets:

| # | Journey | Primary surfaces | Phase |
|---|---|---|---|
| 1 | Build collection: Search → open show → set status → tag/rate | Search, Detail, Collection Home | 1 |
| 2 | Rate-to-save: rate an unsaved show → auto-saved Done | Detail (Rating) | 1 |
| 3 | Tag-to-save: tag an unsaved show → auto-saved Later+Interested | Detail (Tags) | 1 |
| 4 | Maintain collection: browse by status → update My Data | Collection Home, Detail | 1 |
| 5 | Tag-driven organization: add tag → filter appears → filter by it | Filters, Collection Home | 1 |
| 6 | Ask discovery: ask → mentioned show → save | Ask, mentioned-shows strip | 2 |
| 7 | Explore Similar: Get Concepts → select → Explore Shows → save | Detail → Explore Similar | 2 |
| 8 | Alchemy: pick 3 → Conceptualize → select → Alchemize → chain | Alchemy | 2 |
| 9 | Talent deep-dive: Detail → Person → credit → new Detail | Person Detail | 1 |
| 10 | Backup: Export My Data → zip | Settings → Export | 1 |

---

## 14. Open Questions — Decisions Taken

The PRD leaves these explicitly open (§10). A comprehensive plan should take a position rather than leave them dangling:

| Question | Decision | Rationale |
|---|---|---|
| Should **Next** become a first-class UI status? | No for v1 — keep it modeled (already in `my_status` check constraint) but not surfaced | Matches current behavior exactly; revisit with real usage data. Zero cost to leave the door open since the schema already supports it. |
| Named custom lists beyond tags? | Out of scope for v1 | Tags already give free-form grouping + filtering; no stated user need beyond that yet. |
| Should generating an AI Scoop on an unsaved show implicitly save it? | **No** | Scoop generation is not in the PRD's enumerated saving-trigger list (§5.2), and implicit saves must "not surprise" (§8.5). Treat Scoop-on-unsaved as a pure preview action. |
| Should clearing My Rating store an explicit "Unrated" state vs nil? | Store as `nil`/absent | Matches `myScore?: number | null` in the reference schema exactly (no `Unrated` enum exists there); "Unrated" stays a UI-derived label over `null`, not a stored value. Keeps "has the user rated this" a trivial null-check everywhere. |
| Add Import/Restore from export zip? | Yes, but **Phase 4** | Export/import share one schema, so risk is low, but it's not required for the core loop and the PRD itself flags it as "desired, not implemented" rather than required. When built: apply the same §5.5 timestamp-wins merge rules on conflict so restoring an old backup can't clobber newer live data. |
| Support saving/sharing Alchemy sessions as reusable "blends"? | Out of scope for v1 | Directly contradicts the current "session only" persistence rule for Alchemy (§5.7); making Alchemy results durable is a product-level decision that needs an explicit rule change first, not something to slip in silently during a rebuild. |
| Add explicit `myStatus` filters in sidebar? | Yes — **Phase 4**, low cost | PRD explicitly notes "model supports it"; it's the same shape as existing Data Filters (genre/decade/score), so it's additive UI work, not new data modeling. |

---

## 15. Risks & Residual Gaps

- **Missing companion documents.** `where_is_the_heart_opus.md`, `ai_personality_opus.md`, and `philosophy_opus.md` are referenced by the PRD but absent from the repo (§0). The largest concrete impact: the canonical **80 Ask starter prompts** don't exist anywhere in-repo. Phase 2 ships with a small curated seed pool (~20, spanning mood/genre/nostalgia/"surprise me" categories) explicitly flagged as placeholder content, structured as a plain data file so growing it to 80 is a content task, not an engineering one. This is a content gap, not an architecture gap — flagging it here so it isn't silently "solved" by inventing prompts and presenting them as spec-derived.
- **Golden set is genuinely empty in v1** (`discovery_quality_bar.md` §3 says so explicitly). Phase 2 seeds an initial 8–10 scenarios as a starting point; it is not a substitute for a product-owner-curated set and should be revisited once real usage surfaces good/bad examples.
- **Namespace-scoped catalog cache duplication (§2/A7).** Chosen for strict isolation correctness; worth revisiting as a shared/global cache purely for performance once isolation tests give confidence that a shared cache can't leak namespace-specific mutations.
- **BYO API key rate limits.** Both catalog and AI calls can be made with user-supplied keys; Phase 2/3 should include basic backoff + a clear rate-limit-specific error state so a user's own key limits don't surface as generic failures.
- **Streaming + structured output together (Ask).** Streaming `commentary` while still needing a fully-parsed `showList` before rendering mentions is the trickiest single technical interaction in the plan (§8.3/§8.4). Worth a short technical spike at the start of Phase 2 before committing to the exact streaming protocol.
