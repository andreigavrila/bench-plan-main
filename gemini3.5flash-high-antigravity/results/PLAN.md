# Implementation Plan: Personal TV & Movie Companion

This document details the architecture, data schema, API design, and phase-by-step execution roadmap for the Personal TV & Movie Companion app. It strictly adheres to the Fractal Architecture rules, Humble Component patterns, database constraints, and the isolation/test parameters required by the PRD.

---

## 1. Requirement Traceability Matrix

The following matrix ensures that every requirement from the Canonical Requirements Catalog (`evaluator/requirements_catalog_v1.md`) is mapped to specific implementation elements and architectural decisions.

### 1.1 Benchmark Runtime & Isolation
| ID | Requirement | Severity | Implementation Design |
|---|---|---|---|
| **PRD-001** | Use Next.js latest stable runtime | Critical | Build using Next.js App Router (v14/v15 stable) with Server Components. |
| **PRD-002** | Use Supabase official client libraries | Critical | Integrate `@supabase/supabase-js` and `@supabase/ssr` for server/client context. |
| **PRD-003** | Ship `.env.example` with required variables | Critical | Create a comprehensive `.env.example` detailing catalog, AI keys, and DB connections. |
| **PRD-004** | Ignore `.env*` secrets except example | Important | Configure `.gitignore` to block `.env`, `.env.local`, `.env.production` files. |
| **PRD-005** | Configure build through env without code edits | Critical | Pull all configuration (`NAMESPACE_ID`, API keys, model selections) from `process.env`. |
| **PRD-006** | Keep secrets out of repo and server-only | Critical | Elevated credentials like the Supabase service role key are restricted to Server Actions and API Routes. |
| **PRD-007** | Provide app, test, reset command scripts | Critical | Implement `npm run dev`, `npm run test` (Vitest/Playwright), and `npm run test:reset` in `package.json`. |
| **PRD-008** | Include repeatable schema evolution artifacts | Critical | Standardize on SQL migration scripts in a `/supabase/migrations` directory. |
| **PRD-009** | Use one stable namespace per build | Critical | Scope the environment variable `NEXT_PUBLIC_NAMESPACE_ID` (or `NEXT_PUBLIC_RUN_ID`) to isolate builds. |
| **PRD-010** | Isolate namespaces and scope destructive resets | Critical | Filter database operations on `namespace_id` and construct resets targeting only that partition. |
| **PRD-011** | Attach every user record to `user_id` | Critical | Force all rows in tables (`shows`, `cloud_settings`) to belong to a `user_id`. |
| **PRD-012** | Partition persisted data by namespace and user | Critical | Compound primary keys set to `(namespace_id, user_id, show_id)` or `(namespace_id, user_id)`. |
| **PRD-013** | Support documented dev auth injection, prod-gated | Important | Dev mode reads `X-User-Id` header or a custom session cookie; blocked in production. |
| **PRD-014** | Real OAuth later needs no schema redesign | Important | Database design is built on standard `user_id` text/uuid keys matching standard auth tables. |
| **PRD-015** | Keep backend as persisted source of truth | Critical | Always resolve mutations and reads against Supabase tables. No local-only persistence for core library. |
| **PRD-016** | Make client cache safe to discard | Critical | Store library cache in memory or disposable IndexedDB. Clearing client storage triggers re-pull from server. |
| **PRD-017** | Avoid Docker requirement for cloud-agent compatibility | Important | Provide local sqlite fallback or remote hosted database connection mode to avoid mandatory local Docker. |

### 1.2 Collection Data & Persistence
| ID | Requirement | Severity | Implementation Design |
|---|---|---|---|
| **PRD-018** | Overlay saved user data on every show appearance | Critical | Query library on load and merge user metadata attributes into public catalog shows dynamically. |
| **PRD-019** | Support visible statuses plus hidden `Next` | Important | Include `"active" | "later" | "wait" | "done" | "quit" | "next"` in DB constraints; hide `next` in main UI. |
| **PRD-020** | Map Interested/Excited chips to Later interest | Critical | Selection of Interested/Excited updates `myStatus = 'later'` and `myInterest = 'interested' | 'excited'`. |
| **PRD-021** | Support free-form multi-tag personal tag library | Important | Store `my_tags` as a text array `TEXT[]` on the `shows` table. |
| **PRD-022** | Define collection membership by assigned status | Critical | A show is in the collection if and only if `myStatus` is not null (or equivalent non-empty status). |
| **PRD-023** | Save shows from status, interest, rating, tagging | Critical | Implicitly save shows to Supabase upon updating any of these four overlays. |
| **PRD-024** | Default save to Later/Interested except rating-save Done | Critical | If rating an unsaved show, set status to `done`. If tagging/interest-picking, set status to `later` (interest `interested`). |
| **PRD-025** | Removing status deletes show and all My Data | Critical | resetted status triggers validation/confirmation. Upon confirmation, execute SQL DELETE for that show. |
| **PRD-026** | Re-add preserves My Data and refreshes public data | Critical | Keep user timestamps. Merging a catalog re-add will retain existing `my_*` data and only update outdated public keys. |
| **PRD-027** | Track per-field My Data modification timestamps | Critical | Maintain distinct timestamps in DB: `my_tags_update_date`, `my_score_update_date`, `my_status_update_date`, etc. |
| **PRD-028** | Use timestamps for sorting, sync, freshness | Important | Sort home library by `myStatusUpdateDate` descending. Compare update dates during sync conflict resolution. |
| **PRD-029** | Persist Scoop only for saved shows, 4h freshness | Critical | Cache `ai_scoop` with `ai_scoop_update_date` in DB. Regenerate on-demand if > 4 hours old. Wipe on status removal. |
| **PRD-030** | Keep Ask and Alchemy state session-only | Important | Store chat history and active Alchemy catalysts/results in component state / session storage, never in DB. |
| **PRD-031** | Resolve AI recommendations to real selectable shows | Critical | Compare AI-emitted details with catalog search, match case-insensitively, and load complete show details. |
| **PRD-032** | Show collection and rating tile indicators | Important | Grid tiles render checkmark/in-collection icons and overlay the user's rating out of 10. |
| **PRD-033** | Sync libraries/settings consistently and merge duplicates | Important | Sync settings table and resolve concurrent conflicts via timestamp comparison ("newer wins"). |
| **PRD-034** | Preserve saved libraries across data-model upgrades | Critical | Write database schema upgrade scripts that map existing columns forward without dropping rows. |
| **PRD-035** | Persist synced settings, local settings, UI state | Important | Keep local preferences (font size, auto-search) in `localStorage`. Synced settings in Supabase `cloud_settings`. |
| **PRD-036** | Keep provider IDs persisted and detail fetches transient | Important | Keep `providerData` JSON containing provider IDs in DB. Transient streams, trailers, and cast are resolved dynamically. |
| **PRD-037** | Merge catalog fields safely and maintain timestamps | Critical | Implement `selectFirstNonEmpty` rules for public details. Do not overwrite user-updated fields. |

### 1.3 App Navigation & Discover Shell
| ID | Requirement | Severity | Implementation Design |
|---|---|---|---|
| **PRD-038** | Provide filters panel and main screen destinations | Important | Create a master sidebar navigation layout (left column) and main detail/view panel (right column). |
| **PRD-039** | Keep Find/Discover in persistent primary navigation | Important | Place "Find" button in the left sidebar, which loads the Discover Hub workspace (Search/Ask/Alchemy). |
| **PRD-040** | Keep Settings in persistent primary navigation | Important | Place "Settings" button at the bottom of the left sidebar. |
| **PRD-041** | Offer Search, Ask, Alchemy discover modes | Important | Implement a sub-tab bar inside the Discover workspace for Search, Ask, and Alchemy modes. |

### 1.4 Collection Home & Search
| ID | Requirement | Severity | Implementation Design |
|---|---|---|---|
| **PRD-042** | Show only library items matching active filters | Important | Filter local/persisted shows based on selected sidebar filter (Tag, Genre, Decade, Score). |
| **PRD-043** | Group home into Active, Excited, Interested, Others | Important | Group matches into 4 UI list sections: Active, Excited (Later+Excited), Interested (Later+Interested), and Others. |
| **PRD-044** | Support All, tag, genre, decade, score, media filters | Important | Expose all these filter criteria in the left panel. Tags dynamically update lists based on actual tags in DB. |
| **PRD-045** | Render poster, title, and My Data badges | Important | Construct standard grid cards showing poster backdrop, title text, and overlay badges for user status/rating. |
| **PRD-046** | Provide empty-library and empty-filter states | Detail | Display clean UX states encouraging users to go to Find or adjust filtering when matches count = 0. |
| **PRD-047** | Search by title or keywords | Important | Call TMDB (or catalog provider) search endpoint on keystroke (debounced) or form submit. |
| **PRD-048** | Use poster grid with collection markers | Important | Display Search results in cards with overlay indicators (e.g., Green checkmark) if present in user library. |
| **PRD-049** | Auto-open Search when setting is enabled | Detail | Read `autoSearch` setting on load; route to Discover/Search automatically if true and library is empty/new. |
| **PRD-050** | Keep Search non-AI in tone | Important | Keep Search purely factual (title, posters, metadata, direct overview text). No AI summaries here. |

### 1.5 Show Detail & Relationship UX
| ID | Requirement | Severity | Implementation Design |
|---|---|---|---|
| **PRD-051** | Preserve Show Detail narrative section order | Important | Hardcode the layout hierarchy in the detail template matching the exact PRD order (1 to 12). |
| **PRD-052** | Prioritize motion-rich header with graceful fallback | Important | Render trailer video player in header; fallback to background poster/backdrop image. |
| **PRD-053** | Surface year, runtime/seasons, and community score early | Important | Show these core stats prominently underneath the media header. |
| **PRD-054** | Place status/interest controls in toolbar | Important | Toolbar above detail pane displays "Active / Interested / Excited / Done / Quit / Wait" chips. |
| **PRD-055** | Auto-save unsaved tagged show as Later/Interested | Critical | Tag interaction on unsaved show implicitly creates item in DB with `myStatus = 'later'`, `myInterest = 'interested'`. |
| **PRD-056** | Auto-save unsaved rated show as Done | Critical | Rating interaction on unsaved show implicitly creates item with `myStatus = 'done'`. |
| **PRD-057** | Show overview early for fast scanning | Important | Position show overview paragraph immediately below the core details and tags chips. |
| **PRD-058** | Scoop shows correct states and progressive feedback | Important | Stream LLM chunk-by-chunk with spinner and "Generating..." loading states. Save only if saved to collection. |
| **PRD-059** | Ask-about-show deep-link seeds Ask context | Important | Deep-link navigates to Ask chat with initial prompt pre-filled about this specific show. |
| **PRD-060** | Include traditional recommendations strand | Important | Render a horizontal slider of similar shows sourced from standard catalog provider recommendations. |
| **PRD-061** | Explore Similar uses CTA-first concept flow | Important | Concept flow displays "Get Concepts" button first, which fetches concepts, renders chips, and unlocks "Explore Shows". |
| **PRD-062** | Include streaming availability and person-linking credits | Important | Fetch provider streaming lines and cast/crew items. Credits link dynamically to the Person page. |
| **PRD-063** | Gate seasons to TV and financials to movies | Important | Check `showType` in React components; conditionally hide seasons or budget/revenue blocks. |
| **PRD-064** | Keep primary actions early and page not overwhelming | Important | Layout clusters interactive items (status, rating, scoop, tags) in a clean top deck. |

### 1.6 Ask Chat
| ID | Requirement | Severity | Implementation Design |
|---|---|---|---|
| **PRD-065** | Provide conversational Ask chat interface | Important | Build standard chat view with user/assistant bubbles, text field, and clean typography. |
| **PRD-066** | Answer directly with confident, spoiler-safe recommendations | Important | Prompt instructions demand spoiler-safe, friendly, direct, and opinionated TV/movie guidance. |
| **PRD-067** | Show horizontal mentioned-shows strip from chat | Important | Parse the assistant's structured response and render a carousel of matching show posters below the message. |
| **PRD-068** | Open Detail from mentions or Search fallback | Important | Clicking poster navigates to Detail; if ID not present, triggers catalog search using Title. |
| **PRD-069** | Show 6 random starter prompts with refresh | Important | Load 6 prompts from static list of 80; show "Refresh" icon to load a new randomized set. |
| **PRD-070** | Summarize older turns while preserving voice | Important | When conversation turns > 10, run background LLM call to summarize old turns using the "critic friend" voice. |
| **PRD-071** | Seed Ask-about-show sessions with show handoff | Important | Prefill chat window with context payload about the source show, instructing assistant to answer user questions about it. |
| **PRD-072** | Emit `commentary` plus exact `showList` contract | Critical | Force LLM response format: `{ commentary: "text", showList: "Title::externalId::mediaType;;..." }`. |
| **PRD-073** | Retry malformed mention output once, then fallback | Important | Catch JSON/parser errors, resubmit query with strict warning instruction once, then fallback to unstructured response. |
| **PRD-074** | Redirect Ask back into TV/movie domain | Important | System prompt mandates refusal of any request outside of the entertainment and film domain. |

### 1.7 Concepts, Explore Similar & Alchemy
| ID | Requirement | Severity | Implementation Design |
|---|---|---|---|
| **PRD-075** | Treat concepts as taste ingredients, not genres | Important | Prompt instructs extraction of vibes, pacing, themes, and structures (e.g., "hopeful absurdity"). |
| **PRD-076** | Return bullet-only, 1-3 word, non-generic concepts | Important | Prompt strict validation: bullet list, 1-3 word phrases, no descriptions. |
| **PRD-077** | Order concepts by strongest aha and varied axes | Important | Sort outputs putting the most evocative concepts first, spanning structure, tone, and dynamics. |
| **PRD-078** | Require concept selection and guide ingredient picking | Important | Force user to select at least one concept chip before enabling the recommendations request. |
| **PRD-079** | Return exactly five Explore Similar recommendations | Important | Constrain the LLM output to exactly 5 shows matching the selected concepts, with short reasons. |
| **PRD-080** | Support full Alchemy loop with chaining | Important | Let users search and pick 2+ shows, pull concepts, choose, and generate 6 recs. Enable chaining. |
| **PRD-081** | Clear downstream results when inputs change | Important | React state handlers wipe concept and recommendation arrays when selected starting shows change. |
| **PRD-082** | Generate shared multi-show concepts with larger option pool | Important | Prompt instructions for multi-show concept extraction request a larger list of commonalities (e.g., 10-15 concepts). |
| **PRD-083** | Cite selected concepts in concise recommendation reasons | Important | Recommendations must state "Because it blends [concept A] and [concept B]...". |
| **PRD-084** | Deliver surprising but defensible taste-aligned recommendations | Important | Calibrate prompts to introduce diverse results while defending the picks with the chosen concepts. |

### 1.8 AI Voice, Persona & Quality
| ID | Requirement | Severity | Implementation Design |
|---|---|---|---|
| **PRD-085** | Keep one consistent AI persona across surfaces | Important | Create a central `ai_system_persona` prompt module used to initialize all LLM requests. |
| **PRD-086** | Enforce shared AI guardrails across all surfaces | Critical | Validate system instructions: TV/movie limits, spoiler-safe defaults, and mixed-review honesty. |
| **PRD-087** | Make AI warm, joyful, and light in critique | Important | Set temperature and tone parameters to ensure the assistant is a warm critic friend. |
| **PRD-088** | Structure Scoop as personal taste mini-review | Important | Structure scoop format as personal take, stack-up, Scoop paragraph, fit/warnings, and verdict. |
| **PRD-089** | Keep Ask brisk and dialogue-like by default | Important | Prompt tells LLM to keep chat turns under 3 paragraphs unless user explicitly demands depth. |
| **PRD-090** | Feed AI the right surface-specific context inputs | Important | Inject user library status/ratings data into prompts to contextualize recommendations. |
| **PRD-091** | Validate discovery with rubric and hard-fail integrity | Important | Run evaluation assertions against LLM outputs checking format, count, and real catalog keys. |

### 1.9 Person Detail
| ID | Requirement | Severity | Implementation Design |
|---|---|---|---|
| **PRD-092** | Show person gallery, name, and bio | Important | Render page with profile picture, biography text, and other facts. |
| **PRD-093** | Include ratings, genres, and projects-by-year analytics | Important | Compute metrics over their catalog projects and display lightweight CSS charts. |
| **PRD-094** | Group filmography by year | Important | Organize credits in descending order by year. |
| **PRD-095** | Open Show Detail from selected credit | Important | Bind click events on filmography list rows to load the Show Detail screen. |

### 1.10 Settings & Export
| ID | Requirement | Severity | Implementation Design |
|---|---|---|---|
| **PRD-096** | Include font size and Search-on-launch settings | Important | Expose controls in Settings; persist options to local storage and bind to global CSS classes. |
| **PRD-097** | Support username, model, and API-key settings safely | Important | Read/write username, model key, and external keys in `cloud_settings`. Never hardcode keys in code. |
| **PRD-098** | Export saved shows and My Data as zip | Critical | Collect DB snapshot, serialize metadata, encode dates, create zip payload, and trigger download. |
| **PRD-099** | Encode export dates using ISO-8601 | Important | Format all timestamps to `YYYY-MM-DDTHH:mm:ss.sssZ` when writing output backup files. |

---

## 2. Technical Architecture & Database Design

### 2.1 Supabase Schema (`/supabase/migrations/20260519220000_init_schema.sql`)

```sql
-- Enable UUID extension if required
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. App Metadata Table (PRD-008, PRD-034)
CREATE TABLE app_metadata (
    namespace_id TEXT NOT NULL,
    data_model_version INT NOT NULL DEFAULT 3,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
    PRIMARY KEY (namespace_id)
);

-- 2. Cloud Settings Table (PRD-035, PRD-097)
CREATE TABLE cloud_settings (
    namespace_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    user_name TEXT NOT NULL,
    version DOUBLE PRECISION NOT NULL, -- Epoch seconds
    catalog_api_key TEXT,
    ai_api_key TEXT,
    ai_model TEXT NOT NULL DEFAULT 'gpt-4o',
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
    PRIMARY KEY (namespace_id, user_id)
);

-- 3. Shows Table (PRD-011, PRD-012, PRD-018)
CREATE TABLE shows (
    namespace_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    id TEXT NOT NULL, -- Catalog ID
    title TEXT NOT NULL,
    show_type TEXT NOT NULL CHECK (show_type IN ('movie', 'tv', 'person', 'unknown')),
    external_ids JSONB DEFAULT '{}'::jsonb,
    
    -- Catalog Metadata
    overview TEXT,
    genres TEXT[] DEFAULT '{}'::TEXT[],
    tagline TEXT,
    homepage TEXT,
    original_language TEXT,
    spoken_languages TEXT[] DEFAULT '{}'::TEXT[],
    languages TEXT[] DEFAULT '{}'::TEXT[],
    
    -- Images
    poster_url_string TEXT,
    backdrop_url_string TEXT,
    logo_url_string TEXT,
    network_logos TEXT[] DEFAULT '{}'::TEXT[],
    
    -- Ratings & Stats
    vote_average DOUBLE PRECISION,
    vote_count INT,
    popularity DOUBLE PRECISION,
    
    -- Dates
    last_air_date TEXT,
    first_air_date TEXT,
    release_date TEXT,
    
    -- Movie details
    runtime INT,
    budget INT,
    revenue INT,
    
    -- TV details
    series_status TEXT,
    number_of_episodes INT,
    number_of_seasons INT,
    episode_run_time INT[] DEFAULT '{}'::INT[],
    last_episode_run_time INT,
    
    -- User Overlays (PRD-027)
    my_tags TEXT[] DEFAULT '{}'::TEXT[],
    my_tags_update_date TEXT,
    my_score DOUBLE PRECISION,
    my_score_update_date TEXT,
    my_status TEXT CHECK (my_status IN ('active', 'next', 'later', 'done', 'quit', 'wait')),
    my_status_update_date TEXT,
    my_interest TEXT CHECK (my_interest IN ('excited', 'interested')),
    my_interest_update_date TEXT,
    
    -- AI Scoop (PRD-029)
    ai_scoop TEXT,
    ai_scoop_update_date TEXT,
    
    -- Management fields
    details_update_date TEXT NOT NULL,
    creation_date TEXT NOT NULL,
    is_test BOOLEAN NOT NULL DEFAULT FALSE,
    provider_data JSONB DEFAULT '{}'::jsonb, -- (PRD-036)
    
    PRIMARY KEY (namespace_id, user_id, id)
);

-- Enable Row Level Security (RLS) and configure isolation rules
ALTER TABLE app_metadata ENABLE ROW LEVEL SECURITY;
ALTER TABLE cloud_settings ENABLE ROW LEVEL SECURITY;
ALTER TABLE shows ENABLE ROW LEVEL SECURITY;

-- Dynamic isolation policies targeting namespace_id and user_id (PRD-010, PRD-012)
CREATE POLICY shows_isolation_policy ON shows
    FOR ALL
    USING (
        namespace_id = current_setting('request.headers', true)::json->>'x-namespace-id'
        AND user_id = current_setting('request.headers', true)::json->>'x-user-id'
    )
    WITH CHECK (
        namespace_id = current_setting('request.headers', true)::json->>'x-namespace-id'
        AND user_id = current_setting('request.headers', true)::json->>'x-user-id'
    );
```

### 2.2 Local Storage Schema (Client-Only Preferences) (PRD-035)

Stored in browser `localStorage`:
*   `companion_local_settings`: `{ autoSearch: boolean, fontSize: "XS" | "S" | "M" | "L" | "XL" | "XXL" }` (PRD-096)
*   `companion_ui_state`: `{ hideStatusRemovalConfirmation: boolean, statusRemovalCountKey: number, lastSelectedFilter: FilterConfiguration }`

---

## 3. Directory Layout (Fractal Architecture)

Adhering to standard Fractal Architecture guidelines. Under this layout, features house their own hooks, components, and logic, ensuring complete isolation and reuse boundaries. No `index.tsx` files are permitted.

```
src/
├── config/
│   ├── env.ts              # Reads all process.env values safely (PRD-005)
│   └── constants.ts        # App configuration constants
├── theme/
│   └── tokens.ts           # CSS variables, HSL colors, sizing arrays
├── components/             # Shared UI Primitives
│   ├── Button/
│   │   └── Button.tsx
│   ├── RatingBar/
│   │   └── RatingBar.tsx
│   └── ShowTile/
│       └── ShowTile.tsx    # Renders poster, title, checkmarks, score indicators (PRD-032)
├── hooks/                  # Global hooks
│   ├── useSupabase.ts      # Instantiates isolated client context
│   └── usePreferences.ts   # Font size and local layout state
├── utils/                  # Pure utility modules
│   ├── dbMerge.ts          # Merge logic for incoming catalog properties (PRD-037)
│   └── dataExport.ts       # ZIP creation helper using JSZip (PRD-098)
└── pages/
    ├── Home/
    │   ├── Home.tsx        # Container for Home route layout
    │   └── features/
    │       ├── NavigationPanel/
    │       │   ├── NavigationPanel.tsx  # Sidebar filter navigation (PRD-038)
    │       │   └── hooks/
    │       │       └── useFilters.ts
    │       └── CollectionHome/
    │           ├── CollectionHome.tsx   # Displays filtered, grouped library sections (PRD-043)
    │           └── hooks/
    │               └── useCollectionLogic.ts
    ├── Find/
    │   ├── Find.tsx        # Container for search/chat hub
    │   └── features/
    │       ├── ModeSwitcher/
    │       │   └── ModeSwitcher.tsx # Switches Discover modes (PRD-041)
    │       ├── Search/
    │       │   ├── Search.tsx
    │       │   └── hooks/
    │       │       └── useSearchLogic.ts
    │       ├── Ask/
    │       │   ├── Ask.tsx
    │       │   └── hooks/
    │       │       └── useAskLogic.ts
    │       └── Alchemy/
    │           ├── Alchemy.tsx
    │           └── hooks/
    │               └── useAlchemyLogic.ts
    ├── Detail/
    │   ├── Detail.tsx      # Main layout enforcing visual section stack (PRD-051)
    │   └── features/
    │       ├── HeaderMedia/
    │       │   └── HeaderMedia.tsx
    │       ├── FactsRow/
    │       │   └── FactsRow.tsx
    │       ├── RelationshipToolbar/
    │       │   ├── RelationshipToolbar.tsx
    │       │   └── hooks/
    │       │       └── useSaveHandlers.ts # Manages save/auto-save state mappings (PRD-024)
    │       ├── Scoop/
    │       │   ├── Scoop.tsx
    │       │   └── hooks/
    │       │       └── useScoopStreaming.ts
    │       ├── RecommendationsStrand/
    │       │   └── RecommendationsStrand.tsx
    │       └── ExploreSimilar/
    │           ├── ExploreSimilar.tsx
    │           └── hooks/
    │               └── useConceptsExplorer.ts
    └── Person/
        ├── Person.tsx      # Person Details View
        └── features/
            ├── PersonProfile/
            │   └── PersonProfile.tsx
            ├── AnalyticsCharts/
            │   └── AnalyticsCharts.tsx # Visual ratings and metrics (PRD-093)
            └── Filmography/
                └── Filmography.tsx
```

---

## 4. Key Business Logic & Saving Rules

### 4.1 Auto-Save Trigger Logic (PRD-024, PRD-055, PRD-056)
All mutations must route through a unified save handler `saveShowOverlay` to enforce the following defaults:
```typescript
interface UpdatePayload {
  myStatus?: MyStatusType;
  myInterest?: MyInterestType;
  myScore?: number;
  myTags?: string[];
}

export function computeSaveDefaults(existing: Show | null, update: UpdatePayload): ShowDefaults {
  const defaults: ShowDefaults = {};
  
  const currentStatus = update.myStatus || existing?.myStatus;
  const currentTags = update.myTags || existing?.myTags || [];
  const currentScore = update.myScore !== undefined ? update.myScore : existing?.myScore;
  
  if (!currentStatus) {
    if (currentScore !== undefined && currentScore !== null) {
      // Rating an unsaved show sets status to Done (PRD-024, PRD-056)
      defaults.myStatus = "done";
    } else if (currentTags.length > 0 || update.myInterest) {
      // Tagging/Interest setting an unsaved show sets status to Later (PRD-024, PRD-055)
      defaults.myStatus = "later";
      defaults.myInterest = update.myInterest || "interested";
    }
  }
  
  return defaults;
}
```

### 4.2 Field Merge Policy (PRD-037)
When public catalog changes are updated, we apply the `selectFirstNonEmpty` strategy:
```typescript
export function mergeShowDetails(stored: Show, incoming: Show): Show {
  const merged = { ...stored };
  
  // Apply selectFirstNonEmpty for non-user fields
  const keysToMerge: Array<keyof Show> = [
    'overview', 'tagline', 'homepage', 'originalLanguage',
    'posterUrlString', 'backdropUrlString', 'logoUrlString'
  ];
  
  for (const key of keysToMerge) {
    const newVal = incoming[key];
    const oldVal = stored[key];
    if (newVal !== null && newVal !== undefined && newVal !== "") {
      merged[key] = newVal as any;
    }
  }

  // Update timestamps
  merged.detailsUpdateDate = new Date().toISOString();
  return merged;
}
```

### 4.3 Show Removal and confirmation (PRD-025)
When a user deselects a status or triggers removal:
1.  Read `hideStatusRemovalConfirmation` from `localStorage`.
2.  If false, prompt using a modal: *"Are you sure you want to remove this show? This will delete all ratings, tags, and AI summaries."*
3.  Increment the confirmation counter. If >= 3, show a checkbox: *"Don't show this warning again."* (If checked, write true to `hideStatusRemovalConfirmation`).
4.  If confirmed, fire delete query to Supabase: `DELETE FROM shows WHERE namespace_id = ? AND user_id = ? AND id = ?`. Wipe all client states.

---

## 5. AI Engineering & Surface Prompt Specs

We establish a primary voice wrapper (PRD-085, PRD-086) centered on the "critic friend" persona: warm, TV/movie-obsessed, opinionated, and spoiler-safe.

### 5.1 System Prompt Wrapper (`src/utils/ai/systemPersona.ts`)
```typescript
export const SYSTEM_PERSONA_PROMPT = `
You are the user's TV/movie nerd friend.
- Love entertainment deeply and show it.
- Have sharp, opinionated taste. Be honest and acknowledge mixed reception.
- Focus on tone, structure, theme, and craft (e.g. pacing, soundtrack, cinematography). Avoid plot twists (spoiler-safe by default).
- You MUST only talk about movies and TV shows. If asked to leave this domain, politely redirect back to entertainment.
- Never mention internal database IDs or metadata keys to the user.
`;
```

### 5.2 Ask Mode Contract (PRD-072)
For Ask with Mentions, the LLM receives the system wrapper, the user prompt, and the user's active library titles. It must return a structured JSON string matching this signature:
```typescript
interface AskResponse {
  commentary: string; // Factual commentary written in "critic friend" voice (no raw IDs)
  showList: string;   // Structured mentions list formatted exactly as: Title::externalId::mediaType;;Title2::externalId::mediaType
}
```
*Parser Guardrail (PRD-073)*:
```typescript
export async function queryAskAgent(prompt: string, context: string): Promise<AskResponse> {
  const instruction = `${SYSTEM_PERSONA_PROMPT}\nResponse Format MUST be JSON matching: { "commentary": "...", "showList": "Title::externalId::mediaType;;..." }`;
  let result = await callLLM(instruction, prompt);
  
  try {
    return JSON.parse(result);
  } catch (err) {
    // Malformed JSON retry logic (PRD-073)
    const retryInstruction = `${instruction}\nCRITICAL: Your last response was invalid JSON. Retrying. Please output valid JSON.`;
    result = await callLLM(retryInstruction, prompt);
    try {
      return JSON.parse(result);
    } catch {
      // Fallback
      return { commentary: result, showList: "" };
    }
  }
}
```

### 5.3 AI Scoop Generation (PRD-029)
*   **Trigger**: Show Detail page "Give me the scoop!" click.
*   **Format**: Short mini-blog review.
    1.  **High-level Stand**: Positive or critical opinion.
    2.  **Community vs Critic**: Real contrast.
    3.  **The Scoop**: Vibe focus.
    4.  **Warnings**: Who is it NOT for.
    5.  **Verdict**: Final score/opinion.
*   **Cache Rule**: Save `ai_scoop` with `ai_scoop_update_date` (ISO timestamp). If requested again, only regenerate if `now - updateDate > 4 hours`.

---

## 6. Development & Implementation Roadmap

### Phase 1: Environment Setup & Isolation Layer (PRD-003, PRD-007, PRD-009)
*   Define `package.json` command scripts: `dev`, `test`, `test:reset`.
*   Create `.env.example` mapping Supabase credentials, model configuration, and namespace defaults.
*   Configure Vitest setup and write the reset script targeting dynamic namespace tables.

### Phase 2: Schema Migration & Persistence API (PRD-008, PRD-011, PRD-012)
*   Write initial SQL migrations containing compound key checks for namespace partitioning.
*   Construct dynamic server client config utilizing custom client headers (`x-namespace-id`, `x-user-id`) to partition RLS.
*   Write repository helper files implementing user save, rating-save, tag-save defaults, and safe catalog overrides.

### Phase 3: Layout Shell & Navigation Panel (PRD-038, PRD-044)
*   Build the main root layout containing left sidebar panel and routing targets.
*   Create navigation feature including custom genre arrays, decadal groupings, community rating sliders, and dynamic tag lists.
*   Verify that selecting filters successfully updates reactive query builders.

### Phase 4: Collection Home Grid & Search Page (PRD-043, PRD-047)
*   Build the main collection feature implementing Active, Excited, Interested, and Others columns.
*   Write Search component wrapping debounced catalog searches, matching against active collection checkmarks, and supporting auto-search routing.

### Phase 5: Show Detail View & Relationship Toolbar (PRD-051, PRD-054, PRD-058)
*   Wire the detail page layout strictly preserving the twelve-part block sequence.
*   Implement toolbar chips binding save/remove workflows.
*   Integrate Scoop streaming and the concept-catalyst exploration buttons.

### Phase 6: Discover AI Services (Ask & Alchemy) (PRD-067, PRD-080)
*   Build Ask chat interface wrapping structured mention parser.
*   Build Alchemy flow including starter lists, concept catalog selection cards, recommendations, and recursive session loops.

### Phase 7: Backup Export & Sync Systems (PRD-097, PRD-098)
*   Build the backup exporter querying local collection databases and writing ISO-8601 values to a single structured ZIP file.
*   Verify username and API model settings in persistent cloud fields.

---

## 7. Testing & Verification Plan

### 7.1 Namespace Data Isolation Testing (PRD-010)
*   Write unit tests to verify isolation boundaries:
    1.  Initialize client A with `namespace_1` and save movie *X*.
    2.  Initialize client B with `namespace_2` and query library. Assert movie *X* is absent.
    3.  Call `npm run test:reset` with `namespace_1`. Assert database for `namespace_1` is empty, while `namespace_2` retains all records.

### 7.2 Save Defaults Validation (PRD-024)
*   Validate implicit saves in tests:
    1.  Submit rating update on unsaved show. Assert record status automatically becomes `done`.
    2.  Submit tag updates on unsaved show. Assert record status becomes `later` and interest defaults to `interested`.

### 7.3 Exporter Integrity Testing (PRD-099)
*   Write unit tests checking export output:
    1.  Create mock database values with varying tags, status dates, and ratings.
    2.  Trigger backup generation. Unzip output block and parse JSON.
    3.  Validate ISO-8601 patterns on all update date strings (e.g., `2026-05-19T22:00:00.000Z`).
