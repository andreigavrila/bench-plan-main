# Implementation Plan: Personal TV + Movie Companion App

## Executive Summary

This plan covers a full rebuild of a personal TV/movie companion app as a Next.js + Supabase web application. The app lets users collect, organize, rate, and discover entertainment through traditional browsing, AI chat, and concept-based "Alchemy" blending. This plan addresses all product requirements from `product_prd.md`, all infrastructure constraints from `infra_rider_prd.md`, and all supporting documents.

---

## 1. Technology Stack

| Layer | Choice | Rationale |
|---|---|---|
| Runtime | Next.js (latest stable, App Router) | Required by infra rider |
| Persistence | Supabase (hosted) | Required by infra rider |
| Language | TypeScript | Type safety for complex data model |
| Styling | Tailwind CSS | Rapid, consistent UI |
| External catalog | TMDB API (provider-agnostic interface) | Industry standard, PRD is agnostic |
| AI provider | Anthropic Claude API (configurable via env) | Best fit for persona; switchable |
| State management | React Context + SWR/TanStack Query | Server-cache sync |
| Export | JSZip | Zip export for backup |

---

## 2. Project Structure

```
/
├── .env.example                  # All required env vars with comments
├── .gitignore                    # Excludes .env* except .env.example
├── package.json                  # Scripts: dev, build, test, test:reset
├── supabase/
│   └── migrations/               # Repeatable schema migrations (SQL)
│       ├── 001_initial_schema.sql
│       ├── 002_rls_policies.sql
│       └── 003_indexes.sql
├── src/
│   ├── app/                      # Next.js App Router
│   │   ├── layout.tsx            # Root layout: nav panel + main area
│   │   ├── page.tsx              # Collection Home
│   │   ├── find/
│   │   │   └── page.tsx          # Find/Discover hub (Search | Ask | Alchemy tabs)
│   │   ├── shows/
│   │   │   └── [id]/
│   │   │       └── page.tsx      # Show Detail page
│   │   ├── people/
│   │   │   └── [id]/
│   │   │       └── page.tsx      # Person Detail page
│   │   ├── settings/
│   │   │   └── page.tsx          # Settings + Your Data
│   │   └── api/
│   │       ├── shows/            # Collection CRUD
│   │       │   ├── route.ts      # GET (list), POST (upsert)
│   │       │   └── [id]/
│   │       │       └── route.ts  # GET, PATCH, DELETE
│   │       ├── catalog/
│   │       │   ├── search/route.ts
│   │       │   ├── [id]/route.ts
│   │       │   └── person/[id]/route.ts
│   │       ├── ai/
│   │       │   ├── ask/route.ts
│   │       │   ├── scoop/route.ts
│   │       │   ├── concepts/route.ts
│   │       │   └── recommendations/route.ts
│   │       ├── settings/route.ts
│   │       └── export/route.ts
│   ├── components/
│   │   ├── layout/
│   │   │   ├── NavPanel.tsx      # Filter sidebar
│   │   │   └── TopBar.tsx
│   │   ├── show/
│   │   │   ├── ShowTile.tsx      # Poster tile with badges
│   │   │   ├── StatusChips.tsx   # Status/interest selector
│   │   │   ├── RatingBar.tsx     # My Rating slider
│   │   │   ├── TagPicker.tsx     # Tag add/remove
│   │   │   └── ScoopPanel.tsx    # AI Scoop display
│   │   ├── collection/
│   │   │   ├── StatusGroup.tsx   # Section per status
│   │   │   └── ShowGrid.tsx      # Poster grid
│   │   ├── find/
│   │   │   ├── ModeSwitcher.tsx  # Search | Ask | Alchemy tabs
│   │   │   ├── SearchView.tsx
│   │   │   ├── AskView.tsx       # Chat UI
│   │   │   ├── MentionedShows.tsx
│   │   │   └── AlchemyView.tsx
│   │   ├── detail/
│   │   │   ├── HeaderCarousel.tsx
│   │   │   ├── CoreFacts.tsx
│   │   │   ├── ConceptsPanel.tsx
│   │   │   ├── RecommendationsStrand.tsx
│   │   │   ├── StreamingProviders.tsx
│   │   │   ├── CastStrand.tsx
│   │   │   └── SeasonsPanel.tsx
│   │   └── person/
│   │       ├── PersonHeader.tsx
│   │       ├── FilmographyList.tsx
│   │       └── PersonAnalytics.tsx
│   ├── lib/
│   │   ├── supabase/
│   │   │   ├── client.ts         # Browser anon client
│   │   │   └── server.ts         # Server-only service role client
│   │   ├── catalog/
│   │   │   ├── tmdb.ts           # TMDB API wrapper
│   │   │   └── mapper.ts         # Catalog payload → Show shape
│   │   ├── ai/
│   │   │   ├── client.ts         # AI provider abstraction
│   │   │   ├── prompts.ts        # All prompt templates
│   │   │   └── parser.ts         # Structured output parsers
│   │   ├── merge.ts              # Show merge/conflict resolution
│   │   ├── identity.ts           # User ID injection (dev mode)
│   │   └── export.ts             # ZIP export builder
│   ├── types/
│   │   └── schema.ts             # TypeScript types (based on storage-schema.ts)
│   └── hooks/
│       ├── useCollection.ts
│       ├── useShow.ts
│       └── useSettings.ts
├── scripts/
│   ├── reset-namespace.ts        # Destructive test data cleanup
│   └── seed.ts                   # Optional seed data
└── tests/
    ├── unit/
    └── integration/
```

---

## 3. Environment Variables

`.env.example`:

```bash
# Supabase
NEXT_PUBLIC_SUPABASE_URL=          # Supabase project URL
NEXT_PUBLIC_SUPABASE_ANON_KEY=     # Public anon key (safe for browser)
SUPABASE_SERVICE_ROLE_KEY=         # Server-only elevated key (never exposed to client)

# Catalog provider (TMDB)
TMDB_API_KEY=                      # Content catalog API key

# AI provider
AI_API_KEY=                        # AI provider API key (e.g., Anthropic)
AI_MODEL=claude-sonnet-4-6         # Default model; overridable in Settings

# Identity & isolation (benchmark/dev mode)
NAMESPACE_ID=dev-local             # Stable namespace for this build/run
DEFAULT_USER_ID=                   # Optional: fixed user ID for dev/test
DEV_IDENTITY_ENABLED=true          # Set to false in production

# App
NEXT_PUBLIC_APP_ENV=development    # "development" | "production"
```

`.gitignore` additions:
```
.env
.env.local
.env.*.local
!.env.example
```

---

## 4. Database Schema (Supabase / PostgreSQL)

### 4.1 Core Tables

#### `shows`
All user-owned records are scoped to `(namespace_id, user_id)`.

```sql
CREATE TABLE shows (
  -- Partition keys
  namespace_id    text        NOT NULL,
  user_id         text        NOT NULL,
  -- Identity
  id              text        NOT NULL,   -- catalog external ID
  title           text        NOT NULL,
  show_type       text        NOT NULL,   -- 'movie' | 'tv' | 'person' | 'unknown'
  external_ids    jsonb,
  -- Catalog metadata
  overview        text,
  genres          text[]      NOT NULL DEFAULT '{}',
  tagline         text,
  homepage        text,
  original_language text,
  spoken_languages text[]     NOT NULL DEFAULT '{}',
  languages       text[]      NOT NULL DEFAULT '{}',
  -- Images
  poster_url      text,
  backdrop_url    text,
  logo_url        text,
  network_logos   text[]      NOT NULL DEFAULT '{}',
  -- Ratings
  vote_average    float8,
  vote_count      int,
  popularity      float8,
  -- Dates
  release_date    timestamptz,
  first_air_date  timestamptz,
  last_air_date   timestamptz,
  -- Movie-specific
  runtime         int,
  budget          bigint,
  revenue         bigint,
  -- TV-specific
  series_status   text,
  number_of_episodes int,
  number_of_seasons  int,
  episode_run_time   int[]    NOT NULL DEFAULT '{}',
  -- User data ("My*")
  my_tags         text[]      NOT NULL DEFAULT '{}',
  my_tags_update_date timestamptz,
  my_score        float8,
  my_score_update_date timestamptz,
  my_status       text,       -- 'active' | 'next' | 'later' | 'done' | 'quit' | 'wait'
  my_status_update_date timestamptz,
  my_interest     text,       -- 'excited' | 'interested'
  my_interest_update_date timestamptz,
  -- AI data
  ai_scoop        text,
  ai_scoop_update_date timestamptz,
  -- Management
  details_update_date timestamptz,
  creation_date   timestamptz NOT NULL DEFAULT now(),
  is_test         boolean     NOT NULL DEFAULT false,
  -- Streaming
  provider_data   jsonb,

  PRIMARY KEY (namespace_id, user_id, id)
);
```

#### `cloud_settings`
```sql
CREATE TABLE cloud_settings (
  namespace_id    text        NOT NULL,
  user_id         text        NOT NULL,
  user_name       text        NOT NULL DEFAULT '',
  version         float8      NOT NULL DEFAULT 0,  -- epoch seconds
  catalog_api_key text,
  ai_api_key      text,
  ai_model        text        NOT NULL DEFAULT 'claude-sonnet-4-6',

  PRIMARY KEY (namespace_id, user_id)
);
```

#### `app_metadata`
```sql
CREATE TABLE app_metadata (
  namespace_id        text  NOT NULL PRIMARY KEY,
  data_model_version  int   NOT NULL DEFAULT 3
);
```

### 4.2 Indexes

```sql
-- Collection queries (filter by status, tags)
CREATE INDEX idx_shows_namespace_user_status
  ON shows (namespace_id, user_id, my_status);

CREATE INDEX idx_shows_tags
  ON shows USING GIN (my_tags);

CREATE INDEX idx_shows_genres
  ON shows USING GIN (genres);

-- Sorting by update recency
CREATE INDEX idx_shows_status_update
  ON shows (namespace_id, user_id, my_status_update_date DESC);
```

### 4.3 Row-Level Security

```sql
-- Enable RLS on all tables
ALTER TABLE shows ENABLE ROW LEVEL SECURITY;
ALTER TABLE cloud_settings ENABLE ROW LEVEL SECURITY;

-- In dev/benchmark mode, namespace + user_id from request headers control access.
-- Policies are permissive (no auth token required) when DEV_IDENTITY_ENABLED=true.
-- These policies are replaced with real auth policies when OAuth is wired.
```

---

## 5. Identity & Isolation Model

### 5.1 Dev Identity Injection

All server routes extract identity from:
1. `X-Namespace-Id` request header (falls back to `NAMESPACE_ID` env var)
2. `X-User-Id` request header (falls back to `DEFAULT_USER_ID` env var)

```typescript
// src/lib/identity.ts
export function getIdentity(req: Request): { namespaceId: string; userId: string } {
  if (process.env.DEV_IDENTITY_ENABLED !== 'true') {
    // In production: extract from verified session/JWT
    throw new Error('Production auth not yet wired');
  }
  const namespaceId = req.headers.get('X-Namespace-Id') ?? process.env.NAMESPACE_ID!;
  const userId = req.headers.get('X-User-Id') ?? process.env.DEFAULT_USER_ID!;
  return { namespaceId, userId };
}
```

**Migration path to OAuth:** Replace `getIdentity()` internals only. No schema changes needed—`user_id` is already an opaque string.

### 5.2 Namespace Isolation

Every DB query includes `WHERE namespace_id = $1 AND user_id = $2`. No cross-namespace reads are possible. Destructive test resets scope to one namespace only.

---

## 6. Data Layer: Merge & Conflict Resolution

Implemented in `src/lib/merge.ts`:

### Non-user fields: `selectFirstNonEmpty`
- Never overwrite a non-empty stored value with null/empty.
- New catalog data wins only when stored value is empty.

### User ("My*") fields: timestamp wins
- Compare `my_*_update_date` for each field independently.
- Keep whichever side has the newer timestamp.
- If only one side has a timestamp, keep that side.

### `detailsUpdateDate`
- Always set to `NOW()` after a catalog merge.

### `creationDate`
- Set only on first insert; never updated.

---

## 7. API Routes

All routes are Next.js Route Handlers under `src/app/api/`.

### 7.1 Collection (Shows)

| Method | Route | Description |
|---|---|---|
| GET | `/api/shows` | List collection; supports `?filter=`, `?status=`, `?mediaType=`, `?tag=` |
| POST | `/api/shows` | Upsert a show (create or merge) |
| GET | `/api/shows/[id]` | Get single saved show |
| PATCH | `/api/shows/[id]` | Update My* fields (status, interest, tags, rating, scoop) |
| DELETE | `/api/shows/[id]` | Remove from collection (clears all My Data) |

Upsert logic (POST):
1. Fetch existing show from DB.
2. If exists: apply merge rules.
3. If new: set `creation_date`, apply defaults per §5.2–5.3 of PRD.
4. Persist merged result.

### 7.2 Catalog Proxy

| Method | Route | Description |
|---|---|---|
| GET | `/api/catalog/search?q=&type=` | Search external catalog |
| GET | `/api/catalog/[id]?type=` | Full show details + transient data |
| GET | `/api/catalog/person/[id]` | Person details + filmography |

Catalog responses are mapped through `src/lib/catalog/mapper.ts` to the internal `Show` shape. Transient fields (cast, crew, seasons, videos, recommendations) are returned but not persisted.

### 7.3 AI Endpoints

All AI routes are server-only (API key never reaches client).

#### `/api/ai/ask` (POST, streaming)
- Input: `{ messages: ChatMessage[], libraryContext: Show[], showContext?: Show }`
- Output: Server-Sent Events stream
- Structured output: `{ commentary: string, showList: "Title::externalId::mediaType;;" }`
- Retry once with stricter format on parse failure; fallback to unstructured commentary.
- Context window management: summarize turns older than ~10 messages.

#### `/api/ai/scoop` (POST, streaming)
- Input: `{ show: Show, userLibrary?: Show[] }`
- Output: streamed Scoop text
- Freshness: caller checks `ai_scoop_update_date`; only call if > 4 hours stale or null.
- Persistence: only if show is in collection (has `my_status`).

#### `/api/ai/concepts` (POST)
- Input: `{ shows: Show[] }` (1 show = Explore Similar; 2+ = Alchemy)
- Output: `{ concepts: string[] }` — 8 concepts for single-show; larger pool for multi-show
- Format: 1–3 word evocative bullets, no explanation, no plot.

#### `/api/ai/recommendations` (POST)
- Input: `{ concepts: string[], inputShows: Show[], userLibrary: Show[] }`
- Output: `{ recommendations: { show: Show, reason: string }[] }`
- Count: 5 for Explore Similar; 6 for Alchemy.
- Each recommendation must resolve to a real catalog item.
- Resolution: use external ID to fetch catalog item; fallback to title search.

### 7.4 Settings

| Method | Route | Description |
|---|---|---|
| GET | `/api/settings` | Get cloud settings + local settings |
| PATCH | `/api/settings` | Update cloud settings |

API keys are only stored server-side, never returned to the client in plaintext beyond the session that set them (or masked).

### 7.5 Export

| Method | Route | Description |
|---|---|---|
| GET | `/api/export` | Stream a ZIP containing `shows.json` and `settings.json` |

ZIP structure:
```
export-{date}.zip
  shows.json        # All shows with My Data, ISO-8601 dates
  settings.json     # cloud_settings fields (no API keys)
```

---

## 8. Frontend: Page-by-Page

### 8.1 Root Layout (`app/layout.tsx`)

```
┌─────────────────────────────────────────────────────┐
│  NavPanel (left)     │  Main content (right)         │
│  ─────────────────   │  ──────────────────────────── │
│  All Shows           │  [page content]               │
│  ── Tag filters ──   │                               │
│  #tag1, #tag2...     │                               │
│  No Tags (if any)    │                               │
│  ── Data filters ──  │                               │
│  Genre, Decade,      │                               │
│  Score               │                               │
│  ──────────────────  │                               │
│  [Find/Discover]     │                               │
│  [Settings]          │                               │
└─────────────────────────────────────────────────────┘
```

NavPanel state: selected filter persisted in `lastSelectedFilter` (DB or localStorage backup).

### 8.2 Collection Home (`app/page.tsx`)

- Media-type toggle: All / Movies / TV
- Status groups in order:
  1. **Active** — larger tiles (prominent)
  2. **Excited** (Later + Excited interest)
  3. **Interested** (Later + Interested)
  4. **Other** (collapsed): Wait, Quit, Done, unclassified Later
- Each group: heading + horizontal or grid layout of ShowTiles
- ShowTile badges: in-collection indicator, rating indicator
- Empty state: "Add shows to your collection" → links to Find

### 8.3 Find/Discover (`app/find/page.tsx`)

Mode switcher: **Search | Ask | Alchemy**

#### Search Mode
- Text input → debounced catalog search
- Poster grid with in-collection markers
- Setting: "Search on Launch" auto-focuses on mount

#### Ask Mode
- Welcome view: 6 random starter prompts (refreshable)
- Chat UI: user/assistant message bubbles
- Mentioned shows horizontal strip below assistant messages
- Each mentioned show is a tappable tile → Show Detail
- Context summarization: after ~10 messages, older turns are summarized server-side
- "Ask About a Show" variant: seeded from Show Detail with show context prefilled

#### Alchemy Mode
1. Show picker (library + catalog search) → 2+ selected shows
2. **Conceptualize Shows** button → fetches concepts
3. Concept chips (selectable, max 8 selected)
4. **ALCHEMIZE!** button → fetches recommendations
5. Results: 6 show tiles with AI reasons
6. **More Alchemy!** → use results as new inputs (chain)

Backtracking: changing selected shows clears concepts and results.

### 8.4 Show Detail (`app/shows/[id]/page.tsx`)

Section order (per `detail_page_experience.md`):

1. **Header media carousel** — backdrops, posters, logos, inline video trailer
2. **Core facts row** — year, runtime or seasons/episodes, community score bar
3. **Tag chips (My Tags)** + tag picker
4. **Overview text** + Scoop toggle ("Give me the scoop!" / "Show the scoop" / "The Scoop")
5. **Ask about this show** CTA → navigates to Find/Ask with show context
6. **Genres + languages**
7. **My Rating bar** — slider; rating unsaved show auto-saves as Done
8. **Status/interest chips** (in toolbar, not scroll body):
   - Interested / Excited (= Later + interest level)
   - Active / Wait / Done / Quit
   - Reselecting active status → confirmation to remove from collection
9. **Traditional recommendations strand** — horizontal scroll
10. **Explore Similar** — Get Concepts → chip selection → Explore Shows (5 recs)
11. **Streaming availability** ("Stream It")
12. **Cast strand** → Person Detail
13. **Crew strand** → Person Detail
14. **Seasons** (TV only)
15. **Budget vs Revenue** (movies where available)

**Critical states:**
- Unsaved: Scoop ephemeral; auto-save triggers on status/rating/tagging
- No trailers/backdrops: graceful fallback to poster/logo
- No concepts yet: show only "Get Concepts" CTA

### 8.5 Person Detail (`app/people/[id]/page.tsx`)

- Image gallery, name, bio
- Analytics charts:
  - Average project ratings by genre
  - Projects by year (bar chart)
  - Top genres (pie/bar)
- Filmography grouped by year
- Credit card → Show Detail

### 8.6 Settings (`app/settings/page.tsx`)

Sections:
- **App** — Font size (XS/S/M/L/XL/XXL), Search on Launch toggle
- **User** — Username (synced)
- **AI** — AI provider API key (masked input), AI model selection (synced)
- **Integrations** — Catalog provider API key (synced)
- **Your Data** — Export My Data button (downloads ZIP)

---

## 9. AI Integration Details

### 9.1 Provider Abstraction

`src/lib/ai/client.ts` wraps the AI SDK behind an interface:

```typescript
interface AIClient {
  chat(messages: Message[], options?: ChatOptions): AsyncIterable<string>;
  complete(messages: Message[], options?: ChatOptions): Promise<string>;
}
```

The concrete implementation is selected at runtime from env vars. This allows swapping providers without changing AI surface code.

### 9.2 Prompt Templates (`src/lib/ai/prompts.ts`)

Each surface has a dedicated prompt builder:

- `buildScoopPrompt(show, userLibrary)` → Scoop system + user messages
- `buildAskPrompt(messages, userLibrary, showContext?)` → Ask system + history
- `buildConceptsPrompt(shows)` → Concepts generation
- `buildRecommendationsPrompt(concepts, inputShows, userLibrary)` → Recs

All prompts enforce:
- Persona: fun, chatty TV/movie nerd friend (joy-forward, opinionated, vibe-first)
- Spoiler-safe by default
- TV/movie domain only
- Specific over generic

### 9.3 Structured Output Parsing (`src/lib/ai/parser.ts`)

Mentioned shows format: `Title::externalId::mediaType;;...`

Parser:
1. Split on `;;`
2. Split each on `::`
3. Validate 3 parts; skip malformed entries
4. Retry once if full parse fails

### 9.4 Catalog Resolution for AI Recs

When AI returns a recommendation:
1. Extract `title + externalId + mediaType`
2. If `externalId` provided: fetch catalog by ID; verify title matches case-insensitively
3. If match: show becomes real selectable item with AI `reason` as transient text
4. If no match or no ID: show as non-interactive title or hand off to Search

---

## 10. Data Behaviors Implementation

### 10.1 Auto-Save Defaults

Implemented in `PATCH /api/shows/[id]` and show update hooks:

| Action | If unsaved | Result |
|---|---|---|
| Set status | — | Save with that status |
| Rate | No status | Save with `my_status = done` |
| Add tag | No status | Save with `my_status = later`, `my_interest = interested` |
| Select Interested chip | — | Save with `my_status = later`, `my_interest = interested` |
| Select Excited chip | — | Save with `my_status = later`, `my_interest = excited` |

### 10.2 Status Removal

- User reselects their current status → confirmation modal
- `hideStatusRemovalConfirmation` preference suppresses modal after user opts out
- On confirm: `DELETE /api/shows/[id]` clears entire row including all My* fields

### 10.3 AI Scoop Freshness

```typescript
const SCOOP_TTL_MS = 4 * 60 * 60 * 1000; // 4 hours

function isScoopStale(updateDate: string | null): boolean {
  if (!updateDate) return true;
  return Date.now() - new Date(updateDate).getTime() > SCOOP_TTL_MS;
}
```

Scoop is only persisted to DB if `my_status != null` (show is in collection).

### 10.4 Timestamps

Every My* field mutation sets its corresponding `*_update_date` to `NOW()` server-side.

---

## 11. Scripts & Developer Experience

### `package.json` scripts

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "test": "jest --testPathPattern=tests/",
    "test:reset": "npx ts-node scripts/reset-namespace.ts",
    "db:migrate": "supabase db push",
    "db:reset": "supabase db reset"
  }
}
```

### `scripts/reset-namespace.ts`

```typescript
// Deletes all rows where namespace_id = NAMESPACE_ID env var
// Safe: scoped to one namespace only, no global teardown
async function resetNamespace() {
  const namespaceId = process.env.NAMESPACE_ID;
  await supabase.from('shows').delete().eq('namespace_id', namespaceId);
  await supabase.from('cloud_settings').delete().eq('namespace_id', namespaceId);
}
```

---

## 12. Implementation Phases

### Phase 1: Foundation (Days 1–2)
- Initialize Next.js project with TypeScript, Tailwind
- Set up Supabase project + migrations (all tables, indexes, RLS)
- `.env.example`, `.gitignore`
- Identity injection middleware (`identity.ts`)
- Supabase client wrappers (browser anon + server service role)

### Phase 2: Core Data Layer (Days 2–3)
- `src/types/schema.ts` — full TypeScript types
- `src/lib/merge.ts` — merge/conflict resolution
- `/api/shows` CRUD routes with merge logic
- `/api/catalog` proxy routes + TMDB mapper
- `/api/settings` and `/api/export` routes

### Phase 3: Collection UI (Days 3–4)
- Root layout with NavPanel
- Collection Home with status groups
- ShowTile component with badges
- Filter sidebar (All, tag filters, genre, decade, score)
- Media-type toggle
- Empty states

### Phase 4: Show Detail (Days 4–6)
- Header carousel (backdrops, posters, logos, video)
- Core facts + community score
- My Rating bar with auto-save
- Status/interest chips with auto-save and removal confirmation
- Tag picker with auto-save
- Overview + Scoop toggle (ephemeral until saved)
- Traditional recommendations strand
- Streaming providers
- Cast/crew strands
- Seasons panel (TV)
- Budget/revenue (movies)

### Phase 5: AI Infrastructure (Days 5–6)
- AI provider abstraction + Anthropic client
- Prompt builders for all surfaces
- Structured output parser
- Catalog resolution for AI recommendations
- Conversation summarization logic

### Phase 6: Find/Discover (Days 6–8)
- Search mode: text search → catalog grid
- Ask mode: chat UI + mentioned shows strip + starter prompts
- Alchemy mode: full multi-step flow with chaining
- Explore Similar on Show Detail
- "Ask About This Show" with context seeding

### Phase 7: AI Scoop (Day 7)
- Scoop streaming endpoint
- Progressive rendering in UI
- Freshness check + regeneration
- Conditional persistence (in-collection only)

### Phase 8: Person Detail (Day 8)
- Person page: gallery, bio, analytics charts, filmography

### Phase 9: Settings & Export (Day 9)
- Settings page: all sections
- Dev user selector (when `DEV_IDENTITY_ENABLED=true`)
- Export endpoint + ZIP download

### Phase 10: Polish & Testing (Days 9–10)
- Test reset script
- Integration tests for CRUD + merge logic
- Edge cases: empty collection, no trailers, parse failures
- Responsive/accessibility pass

---

## 13. Cross-Cutting Concerns

### 13.1 User Data Consistency ("User Wins")
Every Show upsert applies merge rules. My* fields are never overwritten by catalog refreshes unless the catalog has a newer timestamp (impossible since catalog has no timestamps for user fields).

### 13.2 Data Migration (`dataModelVersion`)
`app_metadata.data_model_version` is checked on startup. Migration scripts in `supabase/migrations/` handle schema evolution. Client-side: stored `Show` objects are validated on read and migrated forward in place.

### 13.3 Client Caching
SWR/TanStack Query caches responses client-side. Cache is disposable—clearing it triggers a re-fetch from Supabase. No user data lives exclusively in client storage.

### 13.4 Security
- `SUPABASE_SERVICE_ROLE_KEY` is server-only; never sent to browser.
- AI and catalog API keys are server-only; client communicates via `/api/*` routes.
- `DEV_IDENTITY_ENABLED` is checked in every server route; must be `false` or absent in production.
- RLS policies ensure namespace isolation at the DB level.

### 13.5 Discovery Quality
AI outputs are validated against the quality bar from `discovery_quality_bar.md`:
- Voice: persona-consistent, warm, opinionated, spoiler-safe
- Taste alignment: grounded in selected concepts + user library
- Real-show integrity: every rec must resolve to a catalog item (non-negotiable)
- Specificity: reasons cite concrete concepts/vibe/structure

---

## 14. Open Questions (Deferred per PRD §10)

1. **Next as first-class status** — data model already supports it (`my_status = 'next'`); UI surfacing deferred.
2. **Named custom lists** — tags are the current mechanism; named lists would require a separate `lists` table.
3. **AI Scoop implicit save** — currently: Scoop is ephemeral for unsaved shows. Could be changed to auto-save with default status.
4. **Import/Restore** — export ZIP format is designed to be parseable; import route can be added later.
5. **Alchemy session persistence** — currently session-only; could serialize to `alchemy_sessions` table.

---

## 15. Compliance Checklist (Infra Rider)

| Requirement | Implementation |
|---|---|
| `.env.example` with all vars | ✓ Section 3 |
| Secrets excluded from git | ✓ `.gitignore` |
| `npm run dev` | ✓ Section 11 |
| `npm test` | ✓ Section 11 |
| `npm run test:reset` | ✓ Section 11 + `scripts/reset-namespace.ts` |
| Repeatable schema (migrations) | ✓ `supabase/migrations/` |
| Stable namespace isolation | ✓ `namespace_id` on all rows |
| `user_id` on all user records | ✓ DB schema + identity middleware |
| No cross-namespace reads | ✓ Every query scoped to `(namespace_id, user_id)` |
| Destructive tests scoped to namespace | ✓ `reset-namespace.ts` |
| No Docker required | ✓ Hosted Supabase primary path |
| OAuth migration without schema change | ✓ `user_id` is opaque string; `identity.ts` is the only swap point |
| Anon key browser-only | ✓ `supabase/client.ts` (browser) vs `supabase/server.ts` (service role) |
