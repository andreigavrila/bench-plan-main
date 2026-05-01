# Implementation Plan: TV + Movie Companion App

## 1. Executive Summary

This plan describes the full implementation of a personal TV + movie companion app. The app allows users to collect, organize, rate, and discover entertainment through a taste-aware AI system. The build uses **Next.js (latest stable)** with **Supabase** as the persistence layer, per the Infrastructure Rider requirements.

All user-owned data is partitioned by `(namespace_id, user_id)`. Identity is injected via environment variables in benchmark/dev mode and designed to adopt real OAuth without schema redesign.

---

## 2. Tech Stack

| Layer | Choice | Notes |
|---|---|---|
| Application runtime | Next.js (latest stable, App Router) | Required by infra rider |
| Language | TypeScript | Implied by schema spec and Next.js best practice |
| Persistence | Supabase (PostgreSQL) | Required by infra rider; hosted preferred |
| Styling | Tailwind CSS | Utility-first, works well with Next.js |
| Component primitives | Radix UI / shadcn/ui | Accessible headless components |
| Data fetching | TanStack Query (React Query) | Server + client data sync |
| State management | Zustand | Lightweight; for filter/session UI state |
| External catalog | TMDB API | Server-side proxy; key from env |
| AI provider | Configurable (env-injected key + model) | Anthropic Claude by default |
| Export | `jszip` | Client-side ZIP generation for data export |

---

## 3. Repository Structure

```
/
├── .env.example                        # All required env vars, commented
├── .gitignore                          # Excludes .env* except .env.example
├── package.json
├── next.config.ts
├── tailwind.config.ts
├── supabase/
│   ├── migrations/                     # Numbered SQL migration files
│   │   ├── 001_initial_schema.sql
│   │   ├── 002_cloud_settings.sql
│   │   └── 003_app_metadata.sql
│   └── seed.sql                        # Optional: dev seed data
├── src/
│   ├── app/                            # Next.js App Router
│   │   ├── layout.tsx                  # Root layout (providers, fonts)
│   │   ├── page.tsx                    # Collection Home
│   │   ├── find/
│   │   │   ├── page.tsx                # Find/Discover hub (mode switcher)
│   │   │   ├── search/page.tsx         # Search mode
│   │   │   ├── ask/page.tsx            # Ask (AI chat) mode
│   │   │   └── alchemy/page.tsx        # Alchemy mode
│   │   ├── show/[id]/page.tsx          # Show Detail
│   │   ├── person/[id]/page.tsx        # Person Detail
│   │   ├── settings/page.tsx           # Settings & Your Data
│   │   └── api/
│   │       ├── shows/
│   │       │   ├── route.ts            # GET (list), POST (upsert)
│   │       │   └── [id]/route.ts       # GET, PATCH, DELETE
│   │       ├── catalog/
│   │       │   ├── search/route.ts     # TMDB multi-search proxy
│   │       │   ├── movie/[id]/route.ts # TMDB movie detail proxy
│   │       │   ├── tv/[id]/route.ts    # TMDB TV detail proxy
│   │       │   └── person/[id]/route.ts
│   │       ├── ai/
│   │       │   ├── ask/route.ts        # AI chat (streaming)
│   │       │   ├── scoop/route.ts      # AI Scoop (streaming)
│   │       │   ├── concepts/route.ts   # Concept generation
│   │       │   └── recommendations/route.ts
│   │       ├── settings/route.ts       # Cloud settings CRUD
│   │       └── export/route.ts         # Data export (ZIP)
│   ├── components/
│   │   ├── collection/
│   │   │   ├── CollectionHome.tsx
│   │   │   ├── StatusSection.tsx       # Status group (Active, Excited, etc.)
│   │   │   ├── ShowTile.tsx            # Poster tile with badges
│   │   │   ├── FilterSidebar.tsx
│   │   │   └── MediaTypeToggle.tsx
│   │   ├── find/
│   │   │   ├── FindHub.tsx             # Mode switcher
│   │   │   ├── SearchPanel.tsx
│   │   │   ├── AskPanel.tsx
│   │   │   │   ├── ChatTurn.tsx
│   │   │   │   ├── MentionedShowsStrip.tsx
│   │   │   │   └── StarterPrompts.tsx
│   │   │   └── AlchemyPanel.tsx
│   │   │       ├── ShowSelector.tsx
│   │   │       ├── ConceptChips.tsx
│   │   │       └── AlchemyResults.tsx
│   │   ├── detail/
│   │   │   ├── ShowDetail.tsx
│   │   │   ├── HeaderMediaCarousel.tsx
│   │   │   ├── StatusChips.tsx         # Toolbar status/interest chips
│   │   │   ├── RatingBar.tsx
│   │   │   ├── TagPicker.tsx
│   │   │   ├── AIScoopSection.tsx
│   │   │   ├── ExploreSimilar.tsx
│   │   │   ├── RecommendationsStrand.tsx
│   │   │   ├── StreamingProviders.tsx
│   │   │   ├── CastCrewStrand.tsx
│   │   │   └── SeasonsSection.tsx
│   │   ├── person/
│   │   │   ├── PersonDetail.tsx
│   │   │   ├── FilmographyList.tsx
│   │   │   └── PersonAnalyticsCharts.tsx
│   │   ├── settings/
│   │   │   ├── SettingsPage.tsx
│   │   │   └── ExportButton.tsx
│   │   └── ui/                         # Shared primitives (Button, Sheet, etc.)
│   ├── lib/
│   │   ├── supabase/
│   │   │   ├── client.ts               # Browser Supabase client (anon key)
│   │   │   └── server.ts               # Server Supabase client (service role)
│   │   ├── catalog/
│   │   │   ├── tmdb.ts                 # TMDB API wrapper
│   │   │   └── mappers.ts              # TMDB → Show mapping + merge logic
│   │   ├── ai/
│   │   │   ├── client.ts               # AI provider client
│   │   │   ├── prompts.ts              # All system prompts
│   │   │   └── parsers.ts              # showList parser, structured output
│   │   ├── identity.ts                 # Resolve namespace_id + user_id
│   │   └── export.ts                   # ZIP export builder
│   ├── hooks/
│   │   ├── useCollection.ts
│   │   ├── useShowActions.ts           # save/update/remove with auto-save logic
│   │   ├── useFilters.ts
│   │   └── useAskSession.ts
│   ├── stores/
│   │   ├── filterStore.ts              # Zustand: active filter state
│   │   └── sessionStore.ts             # Zustand: ask/alchemy session state
│   └── types/
│       ├── show.ts                     # TypeScript types (mirrors schema.ts)
│       └── api.ts                      # API request/response types
├── scripts/
│   ├── dev.sh                          # Start app
│   ├── test.sh                         # Run tests
│   └── reset-test-data.ts              # Delete namespace test data
└── tests/
    ├── unit/
    └── e2e/
```

---

## 4. Environment Configuration

### `.env.example`

```env
# Supabase
NEXT_PUBLIC_SUPABASE_URL=            # Supabase project URL
NEXT_PUBLIC_SUPABASE_ANON_KEY=       # Public/anon key (safe for browser)
SUPABASE_SERVICE_ROLE_KEY=           # Server-only elevated key

# External catalog (e.g. TMDB)
CATALOG_API_KEY=                     # Content catalog API key

# AI provider
AI_API_KEY=                          # AI provider API key (server-only)
AI_MODEL=claude-sonnet-4-6           # AI model identifier

# Identity (benchmark/dev)
NAMESPACE_ID=                        # Stable identifier for this build/run
DEFAULT_USER_ID=                     # Default user for single-user benchmark mode

# Dev settings
NODE_ENV=development
```

**Rules:**
- `SUPABASE_SERVICE_ROLE_KEY` and `AI_API_KEY` are server-only; never sent to the browser.
- `NEXT_PUBLIC_*` variables are safe for browser use.
- Secrets are never committed; `.gitignore` excludes all `.env*` except `.env.example`.

---

## 5. Database Schema

### Migration 001: `shows` table

```sql
CREATE TABLE shows (
  -- Partition keys
  namespace_id    TEXT        NOT NULL,
  user_id         TEXT        NOT NULL,

  -- Identity
  id              TEXT        NOT NULL,
  title           TEXT        NOT NULL,
  show_type       TEXT        NOT NULL CHECK (show_type IN ('movie','tv','person','unknown')),
  external_ids    JSONB,

  -- Catalog meta
  overview        TEXT,
  genres          TEXT[]      NOT NULL DEFAULT '{}',
  tagline         TEXT,
  homepage        TEXT,
  original_language TEXT,
  spoken_languages TEXT[]     NOT NULL DEFAULT '{}',
  languages       TEXT[]      NOT NULL DEFAULT '{}',

  -- Images
  poster_url      TEXT,
  backdrop_url    TEXT,
  logo_url        TEXT,
  network_logos   TEXT[]      NOT NULL DEFAULT '{}',

  -- Ratings / popularity
  vote_average    FLOAT,
  vote_count      INT,
  popularity      FLOAT,

  -- Dates
  last_air_date   TIMESTAMPTZ,
  first_air_date  TIMESTAMPTZ,
  release_date    TIMESTAMPTZ,

  -- Movie-specific
  runtime         INT,
  budget          BIGINT,
  revenue         BIGINT,

  -- TV-specific
  series_status   TEXT,
  number_of_episodes INT,
  number_of_seasons  INT,
  episode_run_time INT[]      NOT NULL DEFAULT '{}',

  -- User data ("my*")
  my_tags         TEXT[]      NOT NULL DEFAULT '{}',
  my_tags_update_date TIMESTAMPTZ,
  my_score        FLOAT,
  my_score_update_date TIMESTAMPTZ,
  my_status       TEXT        CHECK (my_status IN ('active','next','later','done','quit','wait')),
  my_status_update_date TIMESTAMPTZ,
  my_interest     TEXT        CHECK (my_interest IN ('excited','interested')),
  my_interest_update_date TIMESTAMPTZ,

  -- AI data
  ai_scoop        TEXT,
  ai_scoop_update_date TIMESTAMPTZ,

  -- Management
  details_update_date TIMESTAMPTZ,
  creation_date   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  is_test         BOOLEAN     NOT NULL DEFAULT FALSE,

  -- Providers
  provider_data   JSONB,

  PRIMARY KEY (namespace_id, user_id, id)
);

CREATE INDEX shows_namespace_user_status ON shows (namespace_id, user_id, my_status);
CREATE INDEX shows_namespace_user_tags ON shows USING GIN (my_tags);
CREATE INDEX shows_namespace_user_genres ON shows USING GIN (genres);
CREATE INDEX shows_is_test ON shows (namespace_id, is_test);
```

### Migration 002: `cloud_settings` table

```sql
CREATE TABLE cloud_settings (
  namespace_id    TEXT    NOT NULL,
  user_id         TEXT    NOT NULL,
  user_name       TEXT    NOT NULL,
  version         FLOAT   NOT NULL DEFAULT 0,  -- epoch seconds; conflict resolution
  catalog_api_key TEXT,
  ai_api_key      TEXT,
  ai_model        TEXT    NOT NULL DEFAULT 'claude-sonnet-4-6',
  PRIMARY KEY (namespace_id, user_id)
);
```

### Migration 003: `app_metadata` table

```sql
CREATE TABLE app_metadata (
  namespace_id        TEXT  NOT NULL,
  user_id             TEXT  NOT NULL,
  data_model_version  INT   NOT NULL DEFAULT 3,
  PRIMARY KEY (namespace_id, user_id)
);
```

### Key-value settings (stored in `cloud_settings` or a separate `local_settings` table)

For settings that must stay local (font size, autoSearch, UI state), use `localStorage` on the client as a cache — but record defaults in the DB so they survive reinstall.

```sql
CREATE TABLE local_settings (
  namespace_id        TEXT    NOT NULL,
  user_id             TEXT    NOT NULL,
  auto_search         BOOLEAN NOT NULL DEFAULT FALSE,
  font_size           TEXT    NOT NULL DEFAULT 'M' CHECK (font_size IN ('XS','S','M','L','XL','XXL')),
  hide_status_removal_confirmation BOOLEAN NOT NULL DEFAULT FALSE,
  status_removal_count INT    NOT NULL DEFAULT 0,
  last_selected_filter JSONB,
  PRIMARY KEY (namespace_id, user_id)
);
```

---

## 6. Identity & Isolation Model

### Resolution order

```typescript
// src/lib/identity.ts
export function resolveIdentity(request?: Request) {
  const namespaceId = process.env.NAMESPACE_ID ?? 'default';
  let userId = process.env.DEFAULT_USER_ID ?? 'default-user';

  // Dev-only: allow header override for testing multi-user scenarios
  if (process.env.NODE_ENV !== 'production' && request) {
    const headerUserId = request.headers.get('X-User-Id');
    if (headerUserId) userId = headerUserId;
  }

  return { namespaceId, userId };
}
```

- `NAMESPACE_ID` is stable for the lifetime of a build (set once in `.env`).
- `DEFAULT_USER_ID` is the single user in benchmark mode.
- `X-User-Id` header is only respected in non-production mode.
- All Supabase queries include `AND namespace_id = $1 AND user_id = $2`.
- When real OAuth is added: replace header injection with JWT claim extraction — no schema changes required.

---

## 7. External Catalog Integration (TMDB)

All catalog calls go through server-side API routes; the API key never reaches the browser.

### Key endpoints to proxy

| Route | TMDB call | `append_to_response` |
|---|---|---|
| `GET /api/catalog/search` | `/search/multi` | — |
| `GET /api/catalog/movie/[id]` | `/movie/{id}` | `credits,videos,images,recommendations,similar,watch/providers,external_ids` |
| `GET /api/catalog/tv/[id]` | `/tv/{id}` | `credits,aggregate_credits,videos,images,recommendations,similar,watch/providers,external_ids,seasons` |
| `GET /api/catalog/person/[id]` | `/person/{id}` | `combined_credits,images` |

### TMDB → Show mapping

The `mappers.ts` module implements:

1. **Fresh decode:** Map TMDB response fields to the `Show` TypeScript interface.
2. **Merge with stored show:** Apply merge rules:
   - Non-`my*` fields: `selectFirstNonEmpty(newValue, storedValue)` — never overwrite non-empty with empty.
   - `my*` fields: timestamp-based winner (newer wins; if only one has timestamp, keep that side).
   - `detailsUpdateDate`: always set to `NOW()` after merge.
   - `creationDate`: never updated after first write.
3. **Transient attachment:** `cast`, `crew`, `videos`, `recommendations`, `similar`, `seasons`, `images` are returned in the API response but NOT persisted.

**Genre mapping:** Fetch TMDB genre lists on startup (or cache in-memory) to map genre IDs → names for storage.

**Image URL construction:** `https://image.tmdb.org/t/p/{size}{path}`. Logo selection: prefer English-language logos sorted by `vote_average` descending; fall back to first available.

**AI recommendations → catalog resolution:**
- AI output: `Title::externalId::mediaType`
- System calls `GET /api/catalog/{mediaType}/{externalId}` and validates title match (case-insensitive).
- If not found: show as non-interactive or hand off to Search.

---

## 8. API Route Contracts

### Shows API

```
GET    /api/shows                    → list user's collection (with filters)
POST   /api/shows                    → upsert show (create or merge)
GET    /api/shows/[id]               → get single saved show
PATCH  /api/shows/[id]               → partial update (my* fields)
DELETE /api/shows/[id]               → remove from collection (clears all my* data)
```

All routes extract identity via `resolveIdentity(request)` and scope all queries to `(namespace_id, user_id)`.

**PATCH body structure:**
```typescript
{
  myStatus?: MyStatusType | null,
  myInterest?: MyInterestType | null,
  myTags?: string[],
  myScore?: number | null,
  aiScoop?: string | null,
}
// Each field present in the patch updates the corresponding *UpdateDate to NOW()
```

### AI API Routes

```
POST /api/ai/ask          → { messages, libraryContext } → streaming text response
POST /api/ai/scoop        → { showId, showContext }      → streaming text response
POST /api/ai/concepts     → { shows[] }                  → { concepts: string[] }
POST /api/ai/recommendations → { concepts[], sourceShows[] } → { recommendations[] }
```

All AI routes are server-only (API key never exposed to client).

---

## 9. Data Behaviors Implementation

### 9.1 Auto-save rules (in `useShowActions` hook)

| Trigger | Action |
|---|---|
| Set any status chip | Save show; set `myStatus` + `myStatusUpdateDate` |
| Set Interested chip | Save; `myStatus = 'later'`, `myInterest = 'interested'` |
| Set Excited chip | Save; `myStatus = 'later'`, `myInterest = 'excited'` |
| Adjust rating on unsaved show | Save; `myStatus = 'done'`, `myScore = value` |
| Add tag to unsaved show | Save; `myStatus = 'later'`, `myInterest = 'interested'`, `myTags = [tag]` |

**Default status on first save without explicit status:** `later` + `interested`.

### 9.2 Removal

- User re-taps their current status chip.
- Show confirmation dialog (suppress after N confirmations if `hideStatusRemovalConfirmation = true`).
- On confirm: `DELETE /api/shows/[id]` — removes all `my*` data.

### 9.3 Re-add after removal

- Show is already gone from DB.
- Next interaction that triggers a save creates a fresh row.
- Public catalog metadata is re-fetched; any previously cleared `my*` data is lost (by design — user explicitly removed it).

### 9.4 AI Scoop freshness

- Before displaying cached scoop: check `aiScoopUpdateDate`. If older than 4 hours and user requests it, re-generate.
- If show is NOT in collection: scoop is displayed but not persisted to DB.
- If show IS in collection: persist scoop + `aiScoopUpdateDate` via `PATCH /api/shows/[id]`.

### 9.5 Tile indicators

`ShowTile` component accepts the `Show` object and renders:
- A status badge if `myStatus` is non-null.
- A rating badge if `myScore` is non-null.

---

## 10. AI System Design

### Prompts structure (`src/lib/ai/prompts.ts`)

All prompts encode the **shared persona**: fun, chatty TV/movie nerd — warm, opinionated, spoiler-safe, specific over generic.

#### 10.1 Ask (chat) system prompt

Core elements:
- Role: "You are a fun, knowledgeable TV and movie companion. You help users discover great entertainment grounded in their personal taste."
- Persona directives: warm, opinionated, vibe-first, spoiler-safe by default.
- Context injection: user's library (titles, statuses, ratings, tags) as a structured block.
- Domain restriction: stay within TV/movies.
- Output format for mentions: structured `{ commentary, showList }` where `showList` = `Title::externalId::mediaType;;...`.

#### 10.2 Ask with show context

Same prompt + prepended show context block: "The user is asking about: [title] ([year]). [overview]."

#### 10.3 Scoop system prompt

Structure requirement in prompt:
- Personal take (make a stand)
- Honest stack-up vs reviews
- "The Scoop" paragraph (emotional centerpiece, most real estate)
- Practical fit / warnings
- "Worth it?" gut check

Length target: ~150–350 words. Stream progressively.

#### 10.4 Concepts prompt

Input: show title(s) + overview(s).
Output format: bullet list only, 1–3 words per concept, evocative, no explanation.
For multi-show: "concepts must be shared across ALL input shows."
Count: generate ~8 concepts.

Axis guidance in prompt: structural form, tone/vibe, emotional palette, relationship dynamics, craft/intelligence, genre-flavor (not label).

Quality constraints: specificity required ("hopeful absurdity" ✓ / "good writing" ✗).

#### 10.5 Concept-based recommendations prompt

Input: selected concepts + source show(s).
Output: JSON array of `{ title, externalId, mediaType, reason }`.
Count: 5 (Explore Similar) or 6 (Alchemy).
Reason requirement: explicitly reference which concept(s) align and how.
Bias: more recent shows, but allow classics/hidden gems.

### 10.6 Conversation summarization

After approximately 10 message turns in Ask:
- Summarize the oldest turns (keeping last 4–6 turns verbatim).
- Summary tone must match the persona (not sterile "system summary").
- Replace early turns with a single `{ role: 'assistant', content: '[Summary: ...]' }` entry.

### 10.7 Structured output parsing

For the Ask `showList` field:
```typescript
function parseShowList(raw: string): MentionedShow[] {
  return raw.split(';;').map(entry => {
    const [title, externalId, mediaType] = entry.split('::');
    return { title, externalId, mediaType };
  });
}
```
On parse failure: retry once with stricter instructions; otherwise render commentary only with a Search handoff CTA.

---

## 11. Feature-by-Feature Implementation Detail

### 11.1 Collection Home

**Data:** `GET /api/shows` returns the full collection. Client groups by `myStatus`:
1. **Active** section (prominent, larger tiles)
2. **Excited** section (`myStatus = 'later'` AND `myInterest = 'excited'`)
3. **Interested** section (`myStatus = 'later'` AND `myInterest = 'interested'`)
4. **Other** collapsed section: Wait, Quit, Done, and any Later without interest

**Filters (sidebar):**
- All Shows (default)
- Tag filters: one per unique tag in the collection; "No tags" if tagless shows exist
- Genre filter (derived from `genres` field)
- Decade filter (derived from release/air date)
- Community score filter (ranges: e.g., 0–5, 5–7, 7–10)

**Media type toggle:** All / Movies / TV — applied on top of any active filter.

**Empty states:**
- Empty collection → "Start building your collection. Search or Ask for shows."
- Filter yields no results → "No results found."

### 11.2 Search

- `GET /api/catalog/search?q={query}` proxies TMDB multi-search.
- Results grid: poster tiles with in-collection badges.
- Selecting a result navigates to `/show/[id]` (Detail page).
- `autoSearch` setting: if true, auto-focus search input on `/find` load.

### 11.3 Ask (AI Chat)

**State** (Zustand `sessionStore`):
- `messages: ChatMessage[]`
- `mentionedShows: MentionedShow[]`
- `starterPrompts: string[]` (6 random from a pool of ~80)

**Flow:**
1. User types a message → POST to `/api/ai/ask` with `{ messages, libraryContext }`.
2. Stream response to chat UI.
3. Parse `showList` from structured response → resolve each to catalog item → populate `mentionedShows`.
4. Render `MentionedShowsStrip` with resolved shows (tapping opens Detail).
5. If catalog resolution fails: show non-interactive tile with Search CTA.
6. After ~10 turns: trigger summarization (roll up old turns on next send).

**Starter prompts:** load 6 random strings from a static pool; "Refresh" button randomizes again.

**"Ask About This Show":** Navigates to `/find/ask` with `showId` query param. On load, seed the first message with show context.

### 11.4 Alchemy

**State** (Zustand `sessionStore.alchemy`):
- `selectedShows: Show[]`
- `concepts: string[]`
- `selectedConcepts: string[]`
- `recommendations: Recommendation[]`

**Flow:**
1. Show selector: search library + global catalog; add ≥2 shows.
2. **Conceptualize Shows** → `POST /api/ai/concepts` with selected shows → display concept chips.
3. User selects up to 8 concepts. Changing shows clears concepts + results.
4. **ALCHEMIZE!** → `POST /api/ai/recommendations` with selected concepts + source shows → display 6 recommendation tiles.
5. **More Alchemy!** → clear results, pre-populate show selector with previous results (user selects which to chain).

**Session lifetime:** Alchemy state is component-level only; not persisted.

### 11.5 Show Detail

**Data fetching:**
- Server component: `GET /api/catalog/movie/[id]` or `GET /api/catalog/tv/[id]` for public metadata.
- Client: `GET /api/shows/[id]` for user overlay (my* fields).
- Merge happens in the display layer: public data + user overlay.

**Section order** (per spec):
1. Header media carousel (backdrops/posters/logos, inline trailer)
2. Core facts (year, runtime/seasons) + community score
3. Tag chips (My Tags) + tag picker
4. Overview text + Scoop toggle/stream
5. "Ask about this show" CTA → navigates to `/find/ask?showId=`
6. Genres + languages
7. Traditional recommendations strand
8. Explore Similar (Get Concepts → concept chips → Explore Shows)
9. Streaming providers
10. Cast, Crew strands (horizontal scroll) → Person Detail
11. Seasons (TV only)
12. Budget/Revenue (movies, when available)

**Status chips (toolbar):** Always visible; not in scroll body. Chips: Interested, Excited, Active, Done, Quit, Wait. Reselecting active chip triggers removal confirmation.

**Rating:** Slider 0–10. Rating an unsaved show auto-saves as Done.

**Tags:** Chip display + "Add tag" affordance. Adding to unsaved show auto-saves as Later + Interested.

**AI Scoop:**
- Default button text: "Give me the scoop!"
- While loading: "Generating…" with progressive stream display.
- If cached scoop exists: "Show the scoop" / "The Scoop" (open state).
- Freshness: if `aiScoopUpdateDate` > 4 hours ago, re-generate on demand.
- Persist to DB only if `myStatus` is non-null (show is in collection).

**Explore Similar:**
1. "Get Concepts" button → `POST /api/ai/concepts` with single show.
2. Concept chips appear; user selects 1+.
3. "Explore Shows" button → `POST /api/ai/recommendations` → 5 recommendation tiles.

**Fallbacks:**
- No trailers/backdrops: header uses poster + logo layout.
- TV vs Movie: conditional rendering of seasons vs runtime.

### 11.6 Person Detail

**Data:** `GET /api/catalog/person/[id]` (combined_credits + images).

**Sections:**
- Image gallery (cast photos)
- Name, bio
- Analytics charts:
  - Average project rating (by year or overall)
  - Top genres (from filmography)
  - Projects by year (bar chart)
- Filmography grouped by year → tapping opens Show Detail

### 11.7 Settings

**Sections:**

| Section | Fields | Notes |
|---|---|---|
| App | Font size, Search on launch | Persisted locally + DB |
| User | Username | Synced via `cloud_settings` |
| AI | API key, model selection | Env-injected in benchmark; user-entered for production |
| Integrations | Catalog API key | Env-injected in benchmark |
| Your Data | Export My Data button | Generates ZIP |

**Export My Data:**
- Client calls `GET /api/export`.
- Server fetches all shows + settings for the user.
- Returns JSON packaged as a ZIP:
  - `shows.json`: `Show[]` with all fields, dates as ISO-8601.
  - `settings.json`: `CloudSettings`.
  - `metadata.json`: `AppMetadata`.
- Browser downloads the ZIP file.

---

## 12. Developer Scripts

```
npm run dev            # next dev — start development server
npm test               # jest + playwright test suite
npm run test:reset     # run scripts/reset-test-data.ts
npm run db:migrate     # apply supabase migrations
npm run db:seed        # optional: seed dev data
```

### `reset-test-data.ts`

```typescript
// scripts/reset-test-data.ts
// Deletes all rows for the configured NAMESPACE_ID
// Safe: scoped to namespace; does NOT drop tables or affect other namespaces

import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!
);

const namespaceId = process.env.NAMESPACE_ID!;

await supabase.from('shows').delete().eq('namespace_id', namespaceId);
await supabase.from('cloud_settings').delete().eq('namespace_id', namespaceId);
await supabase.from('app_metadata').delete().eq('namespace_id', namespaceId);
await supabase.from('local_settings').delete().eq('namespace_id', namespaceId);

console.log(`Reset complete for namespace: ${namespaceId}`);
```

---

## 13. Data Continuity & Migrations

- `app_metadata.data_model_version` tracks the current schema version (starts at 3).
- On app startup (server-side), read `data_model_version` for the user's namespace; run any pending migration functions.
- Migration functions are additive/non-destructive:
  - Add new columns with defaults.
  - Rename columns using `UPDATE` + `ALTER TABLE RENAME COLUMN` (never drop old column until all clients are updated).
  - Bump `data_model_version` atomically.
- Users never lose collection, ratings, tags, statuses, interest, or AI Scoop due to an update.

---

## 14. Cross-Cutting Concerns

### Display rule (user data wins)
Every component that renders a show first checks if the user has a saved version (from collection store). If yes, render with `my*` overlay. This is enforced at the component level in `ShowTile` and `ShowDetail`.

### Spoiler safety
All AI prompts include an explicit "be spoiler-safe by default" directive. The setting is never exposed as a toggle to the user in the current spec (it is always on).

### Real-show integrity
Before rendering any AI recommendation as an interactive tile:
1. Resolve via catalog API using the `externalId` + `mediaType` from AI output.
2. Validate title matches case-insensitively.
3. If resolution fails: render as non-interactive text with "Search for [title]" CTA.
This is enforced in `parsers.ts` and the recommendation display component.

### Session isolation
Ask and Alchemy sessions are:
- Held in Zustand store (client-side only).
- Never persisted to DB.
- Cleared when user navigates away or resets the session.

### Supabase client separation
- `src/lib/supabase/client.ts`: uses `NEXT_PUBLIC_SUPABASE_ANON_KEY` — imported in Client Components.
- `src/lib/supabase/server.ts`: uses `SUPABASE_SERVICE_ROLE_KEY` — imported only in API Route Handlers and Server Components.

---

## 15. Implementation Phases

### Phase 1: Project Foundation
1. Initialize Next.js project (TypeScript, App Router, Tailwind)
2. Configure Supabase project + apply migrations
3. Set up `.env.example`, `.gitignore`
4. Implement `resolveIdentity` middleware
5. Set up Supabase server/client wrappers
6. Basic routing skeleton (pages without content)

### Phase 2: Core Data Layer
1. Shows API routes (list, upsert, patch, delete)
2. TMDB catalog proxy routes (search, movie detail, TV detail)
3. Show → DB mapping + merge logic
4. `useShowActions` hook (save, update status/interest/rating/tags, remove)
5. Auto-save logic for rating, tags, implicit saves

### Phase 3: Collection Home + Search
1. Collection Home page with status grouping
2. Filter sidebar (tags, genre, decade, score)
3. Media type toggle
4. Show tile with My Data badges
5. Search page (`/find/search`)
6. Basic Show Detail page (public metadata + My Data controls)

### Phase 4: Show Detail — Full
1. Header media carousel (images + trailer)
2. Status chips (toolbar)
3. Rating bar with auto-save
4. Tag picker with auto-save
5. Traditional recommendations strand
6. Streaming providers display
7. Cast/Crew strands → Person Detail page
8. Seasons section (TV)
9. Budget/Revenue section (movies)

### Phase 5: AI Features
1. AI Scoop (streaming, 4-hour freshness, persist-if-saved logic)
2. Ask chat (`/find/ask`) with mentioned shows strip + starter prompts
3. "Ask About This Show" CTA (seeded context)
4. Explore Similar (Get Concepts → chips → Explore Shows)
5. Alchemy (`/find/alchemy`) — full flow including chaining

### Phase 6: Person Detail + Settings + Export
1. Person Detail page (analytics charts, filmography)
2. Settings page (all sections)
3. Data export endpoint + ZIP generation
4. `test:reset` script
5. Font size + autoSearch settings wired to UI

### Phase 7: Polish & Compliance
1. Empty states for all views
2. Error handling + AI fallbacks (retry, Search handoff)
3. Conversation summarization (Ask, after ~10 turns)
4. Removal confirmation dialog with suppress-after-N logic
5. `NEXT` status data-model support (hidden in UI per spec)
6. Full `.env.example` documentation pass
7. Verify all user-owned records scoped to `(namespace_id, user_id)`
8. Verify no secrets in client bundles

---

## 16. Open Questions (Deferred per PRD)

These are noted in the PRD as optional/open; not planned for initial build:

- **Next** status as first-class UI element (data model supports it; UI hidden).
- **Named custom lists** beyond tags.
- **Import/Restore** from export ZIP.
- **Alchemy session sharing/saving.**
- **Explicit myStatus sidebar filters** (model supports it; UI not specified).
- Whether AI Scoop on an unsaved show should implicitly save it (current plan: no implicit save).
- Whether clearing rating stores an explicit "Unrated" state vs null (current plan: null).

---

## 17. Compliance Checklist (Infra Rider)

| Requirement | Implementation |
|---|---|
| Next.js (latest stable) | ✓ App Router, TypeScript |
| Supabase persistence | ✓ Hosted instance via env vars |
| `.env.example` provided | ✓ All vars with comments |
| `.gitignore` excludes secrets | ✓ Excludes `.env*` except `.env.example` |
| `npm run dev` | ✓ |
| `npm test` | ✓ |
| `npm run test:reset` | ✓ Namespace-scoped reset |
| Migrations / repeatable schema | ✓ `supabase/migrations/` |
| Namespace isolation | ✓ All queries scoped to `namespace_id` |
| `user_id` on all user records | ✓ Composite PK `(namespace_id, user_id, id)` |
| Destructive testing scoped to namespace | ✓ `reset-test-data.ts` |
| No global teardown required | ✓ |
| OAuth migration path without schema redesign | ✓ `user_id` is opaque string; swap inject source only |
| No Docker required | ✓ Hosted Supabase; Docker optional for local |
| Anon key in browser, service role server-only | ✓ Separate client/server Supabase wrappers |
| Secrets never committed | ✓ |
