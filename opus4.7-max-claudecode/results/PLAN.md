# Implementation Plan — Personal TV/Movie Companion

This plan is derived from a full read of `docs/prd/product_prd.md`, `docs/prd/infra_rider_prd.md`, all of `docs/prd/supporting_docs/*` (AI prompting, AI voice, concept system, detail page experience, discovery quality bar), and the technical schema in `docs/prd/supporting_docs/technical_docs/`.

The benchmark baseline is **Next.js (latest stable) + Supabase**, with hard constraints on identity injection, namespace isolation, and env-var-only configuration. This plan is organized to produce a compliant, behaviorally faithful build without prescribing UI micro-interactions beyond what the PRDs specify.

---

## 0. Guiding Principles (Distilled)

1. **User overlay wins everywhere.** Wherever a show appears, the saved `my*` data is authoritative. Refreshed catalog metadata merges with `selectFirstNonEmpty` (non-my fields) and timestamp-LWW (my fields).
2. **Collection membership = non-null `myStatus`.** Saving triggers are implicit: any status, interest chip, rating, or first tag saves. Rating defaults status to `Done`; tagging/interest default to `Later + Interested`.
3. **Backend is source of truth.** Clients may cache but must tolerate full cache wipes. No offline-first requirement.
4. **Identity is explicit even in single-user mode.** Every user-owned row is scoped to `(namespace_id, user_id)`. Dev identity injection (header / selector / default user) must be replaceable by OAuth later without schema redesign.
5. **AI stays on-brand.** One persona across Ask / Scoop / Concepts / Alchemy — warm, opinionated, vibe-first, spoiler-safe, in-domain only. Search has no AI voice.
6. **Recommendations must resolve.** AI recs carry `Title::externalId::mediaType`; the app looks them up in the external catalog and falls back to non-interactive or Search handoff if they don't resolve.
7. **Destructive tests are scoped to a namespace.** No global teardown.

---

## 1. Technology Choices

| Concern | Choice | Why |
|---|---|---|
| App runtime | Next.js (latest stable), App Router, TypeScript | Rider-mandated |
| Persistence | Supabase (Postgres + Auth placeholder + RLS) | Rider-mandated |
| Client data access | `@supabase/supabase-js` (browser, anon key) + `@supabase/ssr` for Next.js server actions/route handlers | Official libs; anon-only in browser per rider §3.1 |
| Server-only access | Server Components + Route Handlers using Supabase service-role key (never exposed to browser) | Rider §3.1 credential split |
| AI provider | Pluggable interface (`AIProvider`); default implementation calls whichever provider key is configured; streaming via SSE/ReadableStream | PRD §7 + AI contracts (4 surfaces, streaming Scoop) |
| External catalog | Pluggable `CatalogProvider` interface behind a server adapter; default adapter uses a TMDB-shaped contract (the schema uses IDs/paths consistent with it) | PRD is provider-agnostic; technical_docs reference catalog id + image paths |
| Styling | Tailwind CSS + a small primitive set (Radix UI) | Fast, readable, no heavy design system |
| Schema management | `supabase/migrations/*.sql` + an optional seed script | Rider §3.3 repeatable DB state |
| Testing | Vitest for unit, Playwright for end-to-end against a namespaced dev DB | Destructive tests scoped by namespace |
| Package mgr / scripts | `npm` | Rider example; any is allowed |
| Containers | None required; Docker is strictly optional | Rider §8 |

---

## 2. Repository Layout

```
/
├── .env.example                      # all env vars, commented
├── .gitignore                        # excludes .env*, except .env.example
├── package.json                      # dev / build / start / test / test:reset / db:migrate / db:seed
├── next.config.ts
├── tsconfig.json
├── tailwind.config.ts
├── supabase/
│   ├── migrations/
│   │   ├── 0001_init_core.sql        # users, namespaces, shows, show_user_data, etc.
│   │   ├── 0002_ui_state.sql
│   │   └── 0003_rls_policies.sql
│   └── seed.sql                      # optional starter data (gated to test namespaces)
├── scripts/
│   ├── dev-reset.ts                  # namespace-scoped reset (see §11)
│   └── export-backup.ts              # (dev convenience for export round-trip)
├── src/
│   ├── app/
│   │   ├── layout.tsx                # shell: sidebar + main area
│   │   ├── page.tsx                  # Home (Collection, filtered)
│   │   ├── find/
│   │   │   ├── search/page.tsx
│   │   │   ├── ask/page.tsx
│   │   │   └── alchemy/page.tsx
│   │   ├── detail/[showId]/page.tsx
│   │   ├── person/[personId]/page.tsx
│   │   ├── settings/page.tsx
│   │   └── api/
│   │       ├── ai/
│   │       │   ├── ask/route.ts
│   │       │   ├── scoop/route.ts
│   │       │   ├── concepts/route.ts
│   │       │   └── recommend/route.ts
│   │       ├── catalog/
│   │       │   ├── search/route.ts
│   │       │   ├── show/[id]/route.ts
│   │       │   └── person/[id]/route.ts
│   │       ├── collection/           # CRUD for my*
│   │       │   ├── status/route.ts
│   │       │   ├── interest/route.ts
│   │       │   ├── tags/route.ts
│   │       │   ├── rating/route.ts
│   │       │   └── scoop/route.ts
│   │       ├── export/route.ts       # zip of user data
│   │       └── dev/
│   │           └── reset/route.ts    # namespace-scoped reset; dev-only gate
│   ├── components/
│   │   ├── ShowTile.tsx
│   │   ├── StatusChips.tsx
│   │   ├── RatingBar.tsx
│   │   ├── TagPicker.tsx
│   │   ├── ScoopPanel.tsx
│   │   ├── ConceptChips.tsx
│   │   ├── MentionedShowsStrip.tsx
│   │   ├── AlchemySteps.tsx
│   │   ├── FilterSidebar.tsx
│   │   ├── MediaTypeToggle.tsx
│   │   └── ...
│   ├── lib/
│   │   ├── supabase/
│   │   │   ├── client.ts             # browser anon client
│   │   │   ├── server.ts             # server RLS-scoped client
│   │   │   └── admin.ts              # service-role client (server-only)
│   │   ├── identity/
│   │   │   ├── namespace.ts          # resolve namespace_id from env
│   │   │   ├── user.ts               # resolve user_id via dev injection / future OAuth
│   │   │   └── guard.ts              # request-scope context + assertions
│   │   ├── catalog/
│   │   │   ├── provider.ts           # CatalogProvider interface
│   │   │   └── tmdb.ts               # default adapter (server-only)
│   │   ├── ai/
│   │   │   ├── provider.ts           # AIProvider interface
│   │   │   ├── prompts/              # per-surface prompt builders
│   │   │   │   ├── ask.ts
│   │   │   │   ├── scoop.ts
│   │   │   │   ├── concepts.ts
│   │   │   │   └── recs.ts
│   │   │   ├── parser.ts             # showList parser (Title::externalId::mediaType;;...)
│   │   │   └── summarize.ts          # chat-turn summarizer
│   │   ├── domain/
│   │   │   ├── show.ts               # Show type + helpers
│   │   │   ├── merge.ts              # selectFirstNonEmpty + timestamped my* merge
│   │   │   ├── save-rules.ts         # implicit save triggers & defaults
│   │   │   └── filter.ts             # FilterConfiguration evaluation
│   │   └── export/
│   │       └── zip.ts                # build export bundle
│   └── styles/
└── tests/
    ├── unit/
    │   ├── merge.test.ts
    │   ├── save-rules.test.ts
    │   ├── parser.test.ts
    │   └── filter.test.ts
    └── e2e/
        ├── collection.spec.ts
        ├── search-to-save.spec.ts
        ├── rate-to-save.spec.ts
        ├── tag-to-save.spec.ts
        ├── scoop.spec.ts
        ├── ask.spec.ts
        ├── alchemy.spec.ts
        ├── explore-similar.spec.ts
        ├── person.spec.ts
        └── export.spec.ts
```

---

## 3. Environment Variables (`.env.example`)

Rider §3.1: the build must run purely by filling env vars; no secrets are committed.

```
# --- App ---
APP_ENV=development                      # development | test | production
NAMESPACE_ID=default-dev-namespace       # stable isolation key for this build

# --- Dev identity (removed/gated in production) ---
DEV_DEFAULT_USER_ID=dev-user-1           # used when no X-User-Id header is present
DEV_IDENTITY_INJECTION=true              # accepts X-User-Id header; must be false in prod

# --- Supabase ---
NEXT_PUBLIC_SUPABASE_URL=...
NEXT_PUBLIC_SUPABASE_ANON_KEY=...
SUPABASE_SERVICE_ROLE_KEY=...            # server-only; never exposed to browser

# --- AI provider (benchmark-friendly) ---
AI_PROVIDER=openai                       # openai | anthropic | ...
AI_API_KEY=...
AI_MODEL=gpt-4o-mini                     # or equivalent

# --- External catalog ---
CATALOG_PROVIDER=tmdb
CATALOG_API_KEY=...
CATALOG_IMAGE_BASE=https://image.tmdb.org/t/p
```

`.gitignore` excludes `.env*` except `.env.example`.

---

## 4. Identity & Isolation

### 4.1 Namespace

- `NAMESPACE_ID` env var resolves at server startup via `lib/identity/namespace.ts`.
- Every persisted row carries a `namespace_id` column.
- Row-Level Security: read/write restricted to `namespace_id = current_setting('app.namespace_id')::text`. The server Supabase client injects `app.namespace_id` via `set_config` per request.
- The namespace is a *build* primitive — it is NOT user-visible.

### 4.2 User identity

- Every user-owned row also carries `user_id` (UUID or opaque string).
- In dev, `lib/identity/user.ts` resolves user like this (in order):
  1. If `DEV_IDENTITY_INJECTION=true` and request has `X-User-Id` → use it.
  2. Else use `DEV_DEFAULT_USER_ID`.
- In production, the same function will call `supabase.auth.getUser()` — the dev fallback code path is compiled out when `APP_ENV=production`.
- Effective partition: `(namespace_id, user_id)`. RLS combines both.

### 4.3 Migration to OAuth later

- Schema already uses a `users(id uuid primary key, namespace_id text, ...)` table; provider-specific columns (`auth_provider`, `provider_user_id`, `email`, `display_name`) are optional and default to null in benchmark mode.
- Replacing dev identity with OAuth means wiring `supabase.auth` + route middleware; no schema redesign.

---

## 5. Data Model (Supabase / Postgres)

Mirrors the conceptual schema in `docs/prd/supporting_docs/technical_docs/storage-schema.ts`, but relationalized so that user overlay is separated from catalog data. All tables carry `namespace_id`.

### 5.1 `namespaces`
```
id              text primary key
created_at      timestamptz default now()
```

### 5.2 `users`
```
id                  uuid primary key default gen_random_uuid()
namespace_id        text not null references namespaces(id)
external_handle     text                 -- e.g. X-User-Id when dev-injected
display_name        text
auth_provider       text                 -- null in benchmark; later 'google' etc.
provider_user_id    text
created_at          timestamptz default now()
unique (namespace_id, external_handle)
```

### 5.3 `shows` — catalog-projection (cached public data + AI scoop is NOT stored here)
```
id                  text not null                 -- stable catalog id
namespace_id        text not null references namespaces(id)
title               text not null
show_type           text not null check (show_type in ('movie','tv','person','unknown'))
external_ids        jsonb
overview            text
genres              text[] not null default '{}'
tagline             text
homepage            text
original_language   text
spoken_languages    text[] not null default '{}'
languages           text[] not null default '{}'
poster_url          text
backdrop_url        text
logo_url            text
network_logos       text[] not null default '{}'
vote_average        double precision
vote_count          integer
popularity          double precision
last_air_date       timestamptz
first_air_date      timestamptz
release_date        timestamptz
runtime             integer
budget              bigint
revenue             bigint
series_status       text
number_of_episodes  integer
number_of_seasons   integer
episode_run_time    integer[] not null default '{}'
last_episode_runtime integer
provider_data       jsonb                         -- {countries:{...}}
details_update_date timestamptz
creation_date       timestamptz default now()
is_test             boolean not null default false
primary key (namespace_id, id)
```

Rationale for splitting catalog and `my*`:
- Catalog projection can be refreshed from the provider without racing user edits.
- User overlay is selected by `(namespace_id, user_id, show_id)` and merged with timestamp-LWW.
- A "stored show" in the PRD sense = `LEFT JOIN shows ON show_user_data`.

### 5.4 `show_user_data` — the "my*" overlay
```
namespace_id        text not null
user_id             uuid not null references users(id) on delete cascade
show_id             text not null

my_status           text check (my_status in ('active','next','later','done','quit','wait'))
my_status_update    timestamptz
my_interest         text check (my_interest in ('interested','excited'))
my_interest_update  timestamptz
my_tags             text[] not null default '{}'
my_tags_update      timestamptz
my_score            double precision
my_score_update     timestamptz
ai_scoop            text
ai_scoop_update     timestamptz

primary key (namespace_id, user_id, show_id)
foreign key (namespace_id, show_id) references shows(namespace_id, id)
```

"Collection membership" is equivalent to `my_status is not null`.

### 5.5 `cloud_settings` — optional per-user synced settings
```
namespace_id     text not null
user_id          uuid not null references users(id) on delete cascade
user_name        text not null
version          double precision not null default extract(epoch from now())
catalog_api_key  text   -- optional; only if user-supplied; never logged
ai_api_key       text   -- optional; only if user-supplied
ai_model         text not null
primary key (namespace_id, user_id)
```

### 5.6 `local_settings` — per-user, stored server-side (single user assumption per device is OK, but correctness is server-side)
```
namespace_id  text not null
user_id       uuid not null
auto_search   boolean not null default false
font_size     text not null default 'M' check (font_size in ('XS','S','M','L','XL','XXL'))
primary key (namespace_id, user_id)
```

### 5.7 `ui_state` — per-user UI preferences
```
namespace_id                      text not null
user_id                           uuid not null
hide_status_removal_confirmation  boolean not null default false
status_removal_count              integer not null default 0
last_selected_filter              jsonb  -- {type,label,value}
primary key (namespace_id, user_id)
```

### 5.8 `app_metadata`
```
namespace_id         text primary key
data_model_version   integer not null default 3
```

### 5.9 Indexes
- `shows (namespace_id, show_type)`
- `shows (namespace_id, popularity desc)`
- `show_user_data (namespace_id, user_id, my_status)`
- `show_user_data (namespace_id, user_id)` where `my_status is not null`
- GIN on `show_user_data.my_tags` for tag filters
- GIN on `shows.genres`

### 5.10 RLS policies
- Enable RLS on every user-scoped table.
- Policy template: `using (namespace_id = current_setting('app.namespace_id') and user_id = current_setting('app.user_id')::uuid)`.
- The server client sets both settings before each query.
- `shows` is readable within the namespace regardless of user (it's a cache).

---

## 6. Domain Logic

### 6.1 Save triggers & defaults (`lib/domain/save-rules.ts`)

Deterministic pure functions so the rules are testable without Supabase:
- `onSetStatus(status, prev) → { my_status, my_interest, saved }`
- `onSelectInterest('interested'|'excited', prev) → { my_status:'later', my_interest, saved }`
- `onRateUnsaved(score, prev) → { my_status:'done' if !prev.my_status, my_score, saved }`
- `onAddTagUnsaved(tag, prev) → { my_status:'later' if !prev.my_status, my_interest:'interested' if !prev.my_interest, my_tags:[...,tag] }`
- `onClearStatus(prev) → remove` (returns a tombstone, caller runs confirmation UX)
- Every change stamps the appropriate `*_update` timestamp to `now()`.

### 6.2 Merge (`lib/domain/merge.ts`)
- `selectFirstNonEmpty(newVal, oldVal)` for non-`my` fields (string/array/number/date) — never clobber non-empty with empty/null.
- Timestamp-LWW for `my_*` fields: if both have `*_update`, newer wins; if only one, keep that side.
- `details_update_date` set to now after merge; `creation_date` preserved.
- Implemented server-side; used on catalog refresh and when re-adding a previously-saved show.

### 6.3 Filter evaluation (`lib/domain/filter.ts`)
- `FilterConfiguration { type, label, value }` drives a SQL-builder that returns a `PostgrestFilterBuilder`.
- Supported types: `all`, `genre`, `myStatus`, `communityScore` (ranges), `decade`, `myTag`.
- Composed with the media-type toggle (`All | Movies | TV`).
- Sidebar derives dynamically:
  - "All Shows" always present.
  - Tag filters: `distinct unnest(my_tags)` across the user's collection.
  - "No tags" filter if any collection item has empty `my_tags`.
  - Genre, decade, score filters derived from the user's saved shows' metadata (so sidebar is relevant).

### 6.4 Home grouping (`app/page.tsx`)
Sections in render order:
1. **Active** — prominent tiles.
2. **Excited** — `my_status='later' and my_interest='excited'`.
3. **Interested** — `my_status='later' and my_interest='interested'`.
4. **Other** — `wait | quit | done | later-without-interest`.

Empty states per PRD §7.1.

---

## 7. External Catalog Integration

### 7.1 Adapter interface (`lib/catalog/provider.ts`)
```
interface CatalogProvider {
  search(query: string, opts?: {mediaType?: 'movie'|'tv'|'all'}): Promise<ShowStub[]>
  getShow(id: string, mediaType: 'movie'|'tv'): Promise<CatalogShow>
  getPerson(id: string): Promise<CatalogPerson>
  getSimilar(id: string, mediaType: 'movie'|'tv'): Promise<ShowStub[]>
}
```

### 7.2 Default TMDB adapter (server-only)
- API key via `CATALOG_API_KEY` env.
- Image URLs composed from `CATALOG_IMAGE_BASE` + TMDB path conventions (poster `w500`, backdrop `w1280`, logo best-rated English).
- Maps genre ids → names; picks "best" logo deterministically (highest vote average, English preferred, then first).
- Response caches at the edge (`Cache-Control: s-maxage=...`) but never returns user-scoped data from the cache.

### 7.3 Mapping into our `shows` table
- Follows rules in `technical_docs/storage-schema.md` §"Field mapping rules".
- On refresh, call `merge()` (see §6.2) before upserting.

---

## 8. AI Layer

### 8.1 Provider interface (`lib/ai/provider.ts`)
```
interface AIProvider {
  complete(messages, opts): Promise<string>
  stream(messages, opts): AsyncIterable<string>
}
```
One default implementation behind `AI_PROVIDER` env, picking OpenAI/Anthropic clients. All invocations run server-side; browser never sees `AI_API_KEY`.

### 8.2 Prompt builders (per `ai_prompting_context.md` + `ai_voice_personality.md`)
- **Base persona** injected into every call: warm, opinionated, vibe-first, spoiler-safe, TV/movies only, acknowledges mixed reception. Lives in one file so voice is shared.
- **Ask** (`prompts/ask.ts`): conversational, short by default, may mention shows → returns structured `{commentary, showList}` when mentions exist. `showList` format `Title::externalId::mediaType;;...`. Supplies recent turns; older turns collapsed by `summarize.ts`.
- **Ask-about-this-show**: same as Ask but seeded with current show context (title, genres, overview, user's rating/status if saved).
- **Scoop** (`prompts/scoop.ts`): structured multi-section (personal take, honest stack-up, Scoop centerpiece, fit/warnings, verdict); 150–350 words; streams progressively.
- **Concepts single-show** (`prompts/concepts.ts`): 8 bullets, 1–3 words each, vibe/structure/emotion axes, no generic concepts, no explanations.
- **Concepts multi-show (Alchemy)**: concepts must be shared across inputs; return a larger pool than single-show so the 8-cap selection has variety.
- **Concept-based recs** (`prompts/recs.ts`): 5 recs for Explore Similar, 6 recs for Alchemy; each rec has 1–3 sentence reason that names which concept(s) match; must emit resolvable `externalId` + `mediaType`.

### 8.3 Parser (`lib/ai/parser.ts`)
- Parses `Title::externalId::mediaType;;...`.
- Resolves each via `CatalogProvider.getShow(externalId, mediaType)`; if that fails, case-insensitive title match from a catalog search accepts the first hit.
- Unresolved titles: returned as non-interactive items with a "Search" handoff affordance.

### 8.4 Summarization
- After ~10 Ask turns, oldest turns condensed to 1–2 sentences keeping the same persona's voice (not a sterile "system summary" tone).
- Summaries replace those turns in the context window.

### 8.5 Transience vs persistence
Per PRD §5.7:
| Data | Persisted | Freshness |
|---|---|---|
| AI Scoop | Yes, only if `my_status is not null` | 4 hours |
| Alchemy results/reasons | No — session only | — |
| Ask chat history | No — session only | — |
| Mentioned shows strip | No — derived | — |

Scoop persistence gate lives in the `/api/ai/scoop` handler.

### 8.6 Quality bar enforcement
Per `discovery_quality_bar.md`: programmatic checks before returning:
- **Real-show integrity (non-negotiable):** every rec resolves; if any fail, retry once with a stricter prompt, then drop unresolved items.
- **Concept shape check:** 8 items, each ≤3 words, rejects items in a small blocklist ("good characters", "great story", "funny", "action", etc.).
- **Structured-output parse failure:** one retry with tighter instructions; otherwise fall back to unstructured commentary + Search handoff.

---

## 9. Feature-by-Feature Build

### 9.1 Shell & navigation
- App Router layout with **Filters sidebar** + main area.
- Persistent entry points: **Find** (Search/Ask/Alchemy switcher) and **Settings**.
- Sidebar reads from server (tag/genre/decade/score derivations memoized per user).

### 9.2 Collection Home (`app/page.tsx`)
- Media-type toggle at top (`All | Movies | TV`).
- Groups: Active → Excited → Interested → Other (Wait/Quit/Done/Later-no-interest).
- Tiles show poster + title + badges (`in-collection` + `my-rating` per §5.9).
- Empty states per §7.1.

### 9.3 Search (`app/find/search/page.tsx`)
- Text input → calls `/api/catalog/search`.
- Poster grid with `in-collection` badges (join with `show_user_data` server-side).
- `autoSearch` local setting auto-focuses search on launch if `true`.
- Selecting a result → `/detail/[showId]`.

### 9.4 Ask (`app/find/ask/page.tsx`)
- Chat UI, user/assistant turns, streaming.
- 6 random starter prompts; refresh button (starter pool lives in `lib/ai/prompts/starters.ts`; 80-ish variants per `ai_personality_opus.md` reference).
- Mentioned-shows strip derived from latest assistant turn's `showList`.
- Session-only; clearing resets context.
- Variants: General Ask (from Find) vs Ask-about-a-show (from Detail) — the latter seeds with the show context before the first user message.

### 9.5 Alchemy (`app/find/alchemy/page.tsx`)
Five-step flow, backtracking allowed:
1. **Pick inputs**: 2+ shows (library picker + global catalog search).
2. **Conceptualize Shows** → server extracts shared concepts (larger pool).
3. **Select concepts** (cap 8).
4. **ALCHEMIZE!** → 6 recs with reasons.
5. **More Alchemy!** chains, using current results as new inputs.

Changing inputs clears downstream state.

### 9.6 Show Detail (`app/detail/[showId]/page.tsx`)
Section order per `detail_page_experience.md` §3:
1. Header media carousel (trailer-priority, poster fallback).
2. Core facts + community score.
3. Tag chips.
4. Overview + Scoop toggle/stream.
5. "Ask about this show" CTA → Ask seeded with show.
6. Genres + languages.
7. Recommendations strand.
8. Explore Similar (`Get Concepts` → select → `Explore Shows`, 5 recs).
9. Streaming providers.
10. Cast, Crew strands → Person Detail.
11. Seasons (TV only).
12. Budget/Revenue (movies).

Toolbar hosts status chips + rating. Interactions run through `save-rules.ts`.

### 9.7 Person Detail (`app/person/[personId]/page.tsx`)
- Image gallery, bio, filmography grouped by year.
- Analytics: avg project rating, top genres, projects-by-year — computed client-side from the fetched filmography.
- Credit click → `/detail/[showId]`.

### 9.8 Settings (`app/settings/page.tsx`)
- **App**: font size, search-on-launch.
- **User**: username.
- **AI**: provider API key (optional; env always wins in benchmark mode), model name.
- **Integrations**: catalog provider API key (optional; env wins).
- **Your Data**:
  - **Export My Data**: `/api/export` → streams a `.zip` containing a JSON backup of all saved shows + my data, dates ISO-8601.
  - **Import/Restore**: flagged as an open question in PRD §10 — NOT implemented in v1. A placeholder link notes it.

### 9.9 Tile indicators
Reusable `<ShowTile>` that renders:
- Always: poster + title.
- If `my_status`: small badge.
- If `my_score`: rating badge.

---

## 10. API Surface (Next.js Route Handlers)

All handlers:
1. Resolve `namespace_id` + `user_id` via `lib/identity/*`.
2. Set Supabase session settings (`app.namespace_id`, `app.user_id`).
3. Validate body with Zod.
4. Return typed JSON.

Key routes:
- `GET /api/catalog/search?q=` → proxy to provider; tags results with `in_collection` via DB join.
- `GET /api/catalog/show/[id]?type=movie|tv` → provider fetch + merge into `shows` cache.
- `GET /api/catalog/person/[id]` → provider fetch; not persisted.
- `POST /api/collection/status` `{ showId, status }` → upsert `show_user_data` applying save-rules.
- `POST /api/collection/interest` `{ showId, interest }` → upsert; implies `my_status='later'`.
- `POST /api/collection/rating` `{ showId, score }` → upsert; first save defaults to `done`.
- `POST /api/collection/tags` `{ showId, tags }` → upsert; first save defaults to `later+interested`.
- `DELETE /api/collection/[showId]` → remove row (after confirmation flow on client).
- `POST /api/ai/ask` (SSE) — streaming chat, `{ messages }` → `{ commentary, showList? }`.
- `POST /api/ai/scoop` (SSE) `{ showId }` → streaming scoop; persisted iff `my_status not null`; respects 4-hour freshness.
- `POST /api/ai/concepts` `{ showIds }` → 8 concepts (single) or shared-pool (multi).
- `POST /api/ai/recommend` `{ showIds?, concepts, count: 5|6 }` → recs.
- `GET /api/export` → zip stream.
- `POST /api/dev/reset` (gated: returns 404 when `APP_ENV=production` and `DEV_IDENTITY_INJECTION=false`) — deletes rows within current `namespace_id`.

---

## 11. Scripts & One-Command DX

`package.json` scripts:
- `dev` — Next.js dev server.
- `build` / `start` — production build.
- `lint` / `typecheck`.
- `test` — Vitest unit tests.
- `test:e2e` — Playwright (spins up a namespaced dev DB slice).
- `test:reset` — calls `scripts/dev-reset.ts` → truncates within `NAMESPACE_ID` only.
- `db:migrate` — applies `supabase/migrations/*.sql` (uses Supabase CLI if present, else `psql`).
- `db:seed` — optional seeds flagged `is_test=true`.

Rider §7 compliance: `test:reset` never touches rows outside the current namespace.

---

## 12. Testing Strategy

### 12.1 Unit (Vitest)
- `merge.test.ts` — `selectFirstNonEmpty`, timestamp-LWW for `my_*`.
- `save-rules.test.ts` — every implicit save path + defaults (status-sets-save, rating-unsaved-defaults-done, tagging-unsaved-defaults-later-interested, interest-chip-sets-later, clear-status-removes).
- `parser.test.ts` — `Title::externalId::mediaType;;...` round-trip + graceful failure.
- `filter.test.ts` — each FilterType + media-type toggle composition.
- `concepts.test.ts` — blocklist and shape checks on AI output stubs.

### 12.2 End-to-end (Playwright)
Matches Key User Journeys (PRD §9):
1. Build collection: search → set Interested → tag → verify Home grouping.
2. Rate-to-save: search → open → rate → verify auto-save as Done.
3. Tag-to-save: search → open → add tag → verify auto-save as Later+Interested.
4. Maintain collection: change statuses from Detail; verify Home regroups.
5. Tag-driven organization: add tags; verify sidebar gains tag filters + "No tags".
6. Ask discovery: Ask → save a mentioned show.
7. Explore Similar: Detail → concepts → recs.
8. Alchemy: pick 3 → conceptualize → recs → chain.
9. Talent deep-dive: Detail → Person → credit → Detail.
10. Backup: Settings → Export → verify zip contains ISO-8601 dates and all `my_*`.

All e2e tests:
- Use a fresh namespace (`TEST_NAMESPACE_ID=test-{uuid}`) so runs don't collide.
- Call `test:reset` before/after.
- Stub AI with deterministic fixtures (so voice/structural assertions are reliable) but run at least one smoke test against the real AI provider behind a tag.

### 12.3 Discovery quality bar (manual, scripted harness)
A small `scripts/quality-harness.ts` that loads a handful of scenarios (e.g., "library of sitcoms" → Ask "something cozy"), records outputs, and prints a scorecard along the dimensions in `discovery_quality_bar.md` (Voice, Taste, Surprise, Specificity, Real-show integrity). Not a blocking test — used for regression checks when swapping models.

---

## 13. Compliance Checklist (maps to Rider §9)

| Criterion | How this plan satisfies it |
|---|---|
| `.env.example` + no code edits needed | §3 full inventory |
| Repeatable runs, no collisions | Namespace column on every table + RLS |
| Every user-owned record has `user_id` | `show_user_data`, `cloud_settings`, `local_settings`, `ui_state` all keyed by `(namespace_id, user_id, …)` |
| Destructive tests without global teardown | `test:reset` is namespace-scoped; RLS also prevents leakage |
| OAuth migratable without schema redesign | `users.auth_provider` / `provider_user_id` columns already present; dev injection lives outside schema |
| Secrets not in repo | `.gitignore` excludes `.env*`; browser only sees `NEXT_PUBLIC_*` + anon key; service-role key is server-only |
| No Docker required | Plan targets hosted Supabase; local Supabase via CLI is optional |

---

## 14. Build Order (Phased)

The plan is written so each phase produces something runnable.

**Phase 1 — Foundations**
- Next.js + Tailwind scaffolding; env plumbing; Supabase project + initial migration; RLS + identity helpers; `.env.example`.

**Phase 2 — Catalog + Shows**
- Catalog adapter (TMDB), `GET /api/catalog/search`, `GET /api/catalog/show/[id]`, merge logic, upsert into `shows`.
- Bare Detail page showing catalog data (no user overlay yet).

**Phase 3 — Collection (user overlay)**
- `show_user_data` writes, save-rules, status chips, rating bar, tags, remove-confirmation.
- Home grouping + sidebar "All Shows" + media-type toggle.
- Tile indicators.

**Phase 4 — Filters**
- Dynamic sidebar (tags / "No tags" / genres / decades / score ranges).
- Filter evaluation + last-selected persistence.

**Phase 5 — AI surface 1: Scoop**
- Prompt + streaming route + 4h freshness + persistence gate.
- Detail page Scoop toggle.

**Phase 6 — AI surface 2: Ask**
- Chat UI + mentioned-shows strip + summarization + starter prompts.
- "Ask about this show" Detail CTA.

**Phase 7 — AI surface 3: Concepts + Explore Similar**
- Single-show concepts, selection, 5-rec output on Detail.

**Phase 8 — AI surface 4: Alchemy**
- Multi-input concepts, 6-rec output, chaining.

**Phase 9 — Person Detail**
- Fetch + gallery + filmography + charts.

**Phase 10 — Settings + Export**
- Font size, auto-search, username, AI model, API keys (optional overrides), Export zip.

**Phase 11 — Polish + test coverage**
- Empty states, error toasts, loading skeletons.
- Full Playwright journeys green.
- Quality harness once-over against live AI provider.

---

## 15. Known Open Questions Tracked (from PRD §10 & detail-page §6)

Not blocking v1, but recorded for post-v1 review:
- First-class `Next` status in UI.
- Named custom lists beyond tags.
- Scoop-on-unsaved implicit save.
- Explicit "Unrated" state vs null.
- Import/Restore from export zip (UI stub already placed in Settings).
- Saveable/shareable Alchemy blends.
- Explicit myStatus filters in sidebar.
- Alchemy entry on Detail page.
- Inline trailer playback.

These are listed in `README.md` and tagged as `// TODO(post-v1)` in code where relevant.

---

## 16. Risks & Mitigations

| Risk | Mitigation |
|---|---|
| AI hallucinated shows break "real-show integrity" | Mandatory catalog resolution + retry + drop unresolved; quality-bar rule is non-negotiable |
| RLS misconfiguration leaks across namespaces | Integration test that inserts under namespace A and asserts it's invisible under namespace B |
| Catalog rate limits during tests | Stub adapter in e2e by default; one "live" smoke test |
| Provider key accidentally committed | `.gitignore` + CI grep for `AI_API_KEY=` / `CATALOG_API_KEY=` in staged files |
| Model/prompt drift regresses voice | Quality harness kept in repo for periodic regression review |
| Next.js streaming + Supabase session settings clash | Centralize in a single server client factory that applies `set_config` before every request |

---

## 17. Deliverables for This Benchmark Round

- `.env.example`, `.gitignore` per §3.
- `supabase/migrations/*.sql` producing the schema in §5 with RLS.
- Source tree per §2 implementing §9 features and §10 API.
- Unit + e2e tests per §12.
- `README.md` explaining env setup, `npm run dev|test|test:reset|db:migrate`.

The implementation plan is intentionally comprehensive enough that a separate evaluator (per `2-EVALUATE_PLAN.md`) can score completeness against the PRDs without re-reading the source materials in full.
