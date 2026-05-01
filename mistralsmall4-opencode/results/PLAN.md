# Implementation Plan for Personal TV + Movie Companion App

---

## 1. Overview

This plan outlines the comprehensive architecture, components, and execution strategy for building a **personal TV + movie companion app** based on the provided product requirements document (PRD). The app enables users to collect, organize, rate, and discover entertainment using taste-driven AI features while maintaining a clean, user-centric personal library.

---

## 2. Core Product Goals (Reiterated)

- Enable users to build and maintain a clean, browsable personal collection of movies and TV shows.
- Support lightweight organization via statuses, interest levels, free-form tags, and ratings.
- Provide high-quality, **taste-aware AI discovery** through multiple channels:
  - Conversational AI (Ask)
  - Alchemy (concept blending)
  - Explore Similar (per-show concept extraction)
- Ensure **data integrity, persistence, and sync** across devices.
- Maintain emotional voice and persona across all AI outputs.

---

## 3. System Architecture & Technology Stack

### 3.1 Runtime & Frontend
- **Framework**: Next.js 14+ (App Router), React 19
- **Styling**: Tailwind CSS + Shadcn/ui for component consistency
- **State Management**: Server Components + React Context/Server Actions
- **UI Paradigm**: Responsive, mobile-first design with sidebar navigation and dynamic content

### 3.2 Backend & Hosting
- **Hosting**: Vercel or Netlify (for static/experimental builds)
- **Optional Server**: Next.js server components or Edge API routes (for AI calls, auth, catalog API calls)
- **Persistence Layer (Benchmark Mode)**: Supabase (PostgreSQL + Auth)

### 3.3 Auth & Identity (Benchmark Mode)
- **Development Mode**: Use **dev-only identity injection** via:
  - `X-User-Id` header or
  - Local user selector or
  - Single default user per namespace (for testing)
- **Opaque `user_id`**: Stable UUID string, never encoding provider info
- **Migration Path**: Designed for drop-in replacement with real OAuth (e.g., Google, Supabase Auth) — no schema changes required

### 3.4 Persistence Layer (Supabase)
- **Core Table**: `shows` (mirrors `Show` type)
- **Secondary Tables**:
  - `users` (metadata: name, preferences)
  - `settings` (app-wide settings, synced)
  - `test_runs` (optional, for CI isolation)
- **Partitioning**: All writes scoped to `(namespace_id, user_id)` to prevent collisions
- **No Docker Requirement**: Supabase can be hosted or local; Docker optional

### 3.5 No-Runtime Guarantee
- **Backend is source of truth**: Clients can cache, but correctness must not depend on local storage
- **Clearing client cache may not lose data**: Ensures durability

---

## 4. Data Model (Core Entity: `Show`)

Based on `storage-schema.ts`, the following user-specific fields are stored per show:

| Field Name | Type | Purpose |
|----------|------|--------|
| `myStatus` | `MyStatusType` | User relationship to show (Active, Later, Wait, Done, Quit) |
| `myInterest` | `MyInterestType` | Priority when status = Later (Interested, Excited) |
| `myTags` | `[String]` | Free-form user labels |
| `myScore` | `Double?` | User rating (1–10) |
| `aiScoop` | `String?` | Spoiler-safe AI-generated personality review |

Each field tracks `*UpdateDate` for conflict resolution.

**In Collection**: A show is "in collection" when any status is set (incl. Later).

### 4.1 Default Save Rules

- **Set status** → Save as `Later` (default) or explicitly set status
- **Choose Interested/Excited** → Status = `Later`, Interest = value
- **Rate unsaved show** → Status = `Done`
- **Add tag to unsaved show** → Status = `Later`, Interest = `Interested`

---

## 5. Identity & Isolation Model

### 5.1 Namespace (`namespace_id`)
- **Purpose**: Build/run isolation (not a user concept)
- **Implementation**: Environment variable or config per CI run
- **Scope**: All stored records patched with `namespace_id`
- **Partition**: `(namespace_id, user_id)`

### 5.2 User Identity (`user_id`)
- **Requirements**: All user-owned records must include `user_id`
- **Injection (dev mode)**: Via header, UI, or config
- **Echo in UI**: Displayed in settings as "Your data"

---

## 6. Key Features & Implementation Breakdown

### 6.1 Collection Home

**UI**: Sidebar filters (All, Movies, TV, Genres, Decades, Tags) + Media-type toggle

**Content Organization**:
- Active (watching)
- Excited (Later + Excited)
- Interested (Later + Interested)
- Other: Wait, Done, Quit
- Empty states: "No shows? Try Search or Ask"

**Backend**:
- Query: `SELECT * FROM shows WHERE user_id = ? AND status IS NOT NULL AND (namespace_id, user_id) = (?, ?)`
- Filter by `showType`, `genres`, `decade`, `tags`, `myStatus`

### 6.2 Search (Global Catalog)

**Behavior**:
- Full-text search across titles
- Results: poster grid
- In-collection items marked
- Auto-open on launch (optional)

**Tech Stack**:
- Use external catalog API (e.g., TMDB) via search endpoint
- Integrate via Next.js API route

### 6.3 Ask (Conversational Discovery)

**AI Surface**: Uses same persona as Scoop/Alchemy

**Flow**:
- Natural language queries
- AI responds in chat UI
- Mentions: extract inline show references → "Mentioned Shows" row
- Session context retained (~10 turns), older summarized

**Structured Output Contract**:
```
{
  commentary: "string (user-facing)",
  showList: "Title::externalId::mediaType;;..."
}
```

**AI Model**: LLM integration (e.g., OpenAI, Anthropic, Ollama, or open model)

**Persistence**: None — chat history cleared on reset/leave

### 6.4 Alchemy (Multi-Show Concept Blending)

**User Journey**:
1. Select ≥2 shows (from library or catalog)
2. "Conceptualize Shows" → AI generates shared concept catalysts
3. User selects 1–8 concepts
4. "ALCHEMIZE!" → AI returns 6 recommended shows with reasons rooted in selected concepts
5. Option to chain another round

**AI Prompt Focus**: Shared vibe, structure, emotion across input shows

### 6.5 Explore Similar (Per-Show Concepts)

**User Journey**:
1. From Show Detail → **Get Concepts**
2. AI generates 8 concept bullets (1–3 words)
3. User selects 1+ concepts → **Explore Shows**
4. Returns 5 AI recommendations

**Concept Philosophy**: AI returns **ingredient-like** hooks (e.g., "hopeful absurdity", not "good characters")

### 6.6 The Scoop (AI Review)

**Features**:
- Spoiler-safe by default
- Cached for 4 hours
- Only stored if show is in collection
- Shows: personal take, stack-up vs community, Scoop centerpiece, fit/warnings, verdict

**UI**: Toggle in Detail page, streams progressively

---

## 7. Show Detail Page (Complete Layout)

| Section | Description |
|--------|-----------|
| **Header Media** | Backdrop, poster, logo, trailer (if available) |
| **Core Facts** | Year, runtime/seasons, genres, languages |
| **Rating + Status** | Community score, user rating slider, status chips (toolbar) |
| **Tags** | Display and picker for My Tags |
| **Overview** | Short synopsis |
| **AI Scoop** | Conditional toggle, shows cached or streams fresh |
| **Ask About This Show** | Button → seeds Ask context |
| **Traditional Recs** | Strand of similar shows |
| **Explore Similar** | "Get Concepts" → select → recs |
| **Streaming** | Providers (via provider IDs) |
| **Cast/Crew** | Person detail links |
| **Seasons (TV)** | Episode/season data |
| **Budget/Revenue (Movies)** | Optional depth |

---

## 8. AI Voice & Personality (Compliance Contract)

### Shared Persona
> **A fun, chatty TV/movie nerd friend**
- Joy-forward and warm
- Opinionated but honest
- Vibe-first, spoiler-safe
- Specific over generic
- Shot at 150–350 words for Scoop; concise for Ask

### Voice Pillars (Non-Negotiable)
1. Joy-forward, warm
2. Opinionated honesty
3. Vibe-first, spoiler-safe by default
4. Specific > generic
5. Short when needed, lush only when asked

### Surface-Specific Modes
| Surface | Tone / Style | Length |
|--------|------------|--------|
| **Scoop** | Magazine blog-post of taste | ~150–350w |
| **Ask** | Fast dialogue, friendly | 1–3 paragraphs + bullets |
| **Explore Search Chat** | Showman, mirror emotion | short, scan-friendly |
| **Concepts** | "Aha" vibes, playful | 1–3 word bullets |
| **Concept Recs** | Friend thrilled to share | 1–3 sentences/reason |

---

## 9. Technical Requirements & Infrastructure (Rider Compliance)

### 9.1 Environment Variables (`.env.example` Required)
```env
# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://<project>.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=ey...

# Namespace / Identity (dev mode)
NAMESPACE_ID=dev-test-run-123
X_USER_ID=dev-user-456

# AI Provider
AI_PROVIDER=anthropic
AI_MODEL=claude-3-haiku-20240307
AI_API_KEY=sk-...

# Catalog API
CATALOG_API_KEY=... (for TMDB or similar)

# Optional (UI features)
AUTO_SEARCH_ON_LAUNCH=false
```

### 9.2 Commands (Package.json)
```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "test": "jest",
    "test:reset": "node scripts/reset-test-data.js"
  }
}
```

### 9.3 Reset Mechanism (`test:reset`)
- Drops and recreates test namespace (`namespace_id`)
- Uses Supabase SQL or ORM schema
- Scoped to `(namespace_id, user_id)`

### 9.4 Schema Evolution
- Use **Supabase Migrations** or equivalent
- Track `app_metadata.dataModelVersion` for migrations
- Example: v3 schema includes `myInterest`, `aiScoop`, timestamps

### 9.5 Cloud Compatibility
- No Docker required
- Supabase connection string configurable via env
- Namespace injected in server hooks

---

## 10. Data Behaviors & Business Rules

### 10.1 Saving Triggers
| Action | Effect |
|-------|--------|
| Set status | Save show, apply defaults if missing |
| Choose Interested/Excited | Set status=Later, set interest |
| Rate unsaved show | Auto-save as status=Done |
| Add tag to unsaved show | Auto-save as status=Later, interest=Interested |

### 10.2 Defaults on First Save
| Trigger | Default Status | Default Interest |
|--------|----------------|-------------------|
| General save | Later | Interested |
| First save via rating | Done | (not set) |

### 10.3 Removal from Collection
- Action: Reselect status → confirm dialog
- Effect: Delete show record + My Data
- Persistence: All user fields cleared

### 10.4 Re-adding Same Show
- Preserve latest `myTags`, `myScore`, `myStatus`, `myInterest`, `aiScoop`
- Merge: Later wins if user edits; otherwise catalog refresh overwrites non-user data
- Use `*UpdateDate` for conflict resolution

---

## 11. Discovery AI Engine

### 11.1 Core AI Responsibilities
- **Scoop Generation**: Produce mini blog-post of taste per show
- **Ask**: Generate conversational response with structured `showList`
- **Concept Extraction**: From 1+ shows → shared vibe/structure/emotion
- **Recommendations**: 6 recs (Alchemy), 5 recs (Explore Similar) with reasons citing concepts

### 11.2 Inputs Sent to AI
- User library (Shows + My Data)
- Current context (e.g., specific show for Scoop or Ask context)
- Selected concepts (for recs)
- Optional: recent chat turns (summarized after ~10)

### 11.3 Output Contracts
All AI outputs must adhere to:
- Domain: TV/movies only
- Spoiler-safe default
- Structured outputs where required
- Actionable recs with real catalog IDs (or full title match)

---

## 12. Filters & Sidebar Navigation

### Sidebar Filters (Dynamic)
- **Show Type**: All / Movies / TV
- **Tag Filters**: One per tag + "No tags"
- **Data Filters**: Genre, Decade, Community Score ranges
- **My Status**: (optional UI toggle)

### Behavior
- Filters compose: e.g., Movies + Genre=Sci-Fi + My Status=Active
- UI updates immediately
- Empty state: "No results found"

---

## 13. Settings & Data Portability

### 13.1 Export / Backup
- From Settings → "Export My Data"
- Output: `.zip` containing:
  - `library.json` (all shows + My Data)
  - `dates` encoded ISO-8601

### 13.2 Import / Restore
- Out of scope (Open Question PRD)

### 13.3 Configurable Settings
- Font size (XS–XXL)
- Search on launch
- AI provider & model
- Catalog provider
- Username (synced if enabled)

---

## 14. AI Scoop Freshness & Cache

| AI Data | Persisted? | Freshness |
|-------|-----------|-----------|
| AI Scoop | Yes (if in collection) | 4 hours |
| Alchemy recs/reasons | No | Session only |
| Ask chat history | No | Session only |
| Mentioned shows | No | Session only |

---

## 15. Backup & Recovery Strategy

- **No offline requirement**, but client cache disposable
- **Cloud sync (optional)**: Enabled via settings; conflicts resolve by `timestamp`
- **Import future work**: Align with export format

---

## 16. High-Level Component Tree (UI/UX)

```
App
├── Sidebar (Filters: type, genre, status, tags)
├── Main Content Area
│   ├── Home (filtered library by status/type)
│   ├── Find/Discover Hub
│   │   ├── Search
│   │   ├── Ask (chat UI)
│   │   └── Alchemy (pipeline UI)
│   ├── Show Detail (full page per show)
│   ├── Person Detail
│   └── Settings
└── Global Actions (Modals: Tag picker, status change confirm)
```

---

## 17. Order of Operations for Implementation (Not Coding Yet)

This plan is for **planning only**. Actual coding order would follow:

1. **Setup & Isolation**: Configure Supabase + env vars + namespace model
2. **Data Layer**: Ensure `Show` schema supports all required fields and timestamps
3. **Identity**: Dev-only identity injection working with user_id
4. **Core CRUD**: Create, read, update, delete for shows with auto-save rules
5. **Collection Home**: Filtered lists with grouping
6. **Search Engine**: External API integration
7. **AI Integration**: Start with mock responses, then implement real AI
8. **AI Persona Layer**: Shared voice prompts, tone adapters
9. **Concept Engine**: AI prompt for concept generation and selection
10. **Show Detail Page**: Full layout
11. **AI Scoop**: With caching
12. **Ask Chat**: With session context
13. **Alchemy Pipeline**: Multi-show, concepts → recs
14. **Explore Similar**: Per-show concept extraction
15. **Settings & Export**
16. **Sidebar & Filters Implementation**
17. **Responsive UI & Polish**

---

## 18. Success Criteria (Build Compliance)

From `infra_rider_prd.md`:
- [ ] `.env.example` present and correct
- [ ] One-command experience (dev, test, reset)
- [ ] Database schema and migrations repeatable
- [ ] Namespace isolation enforced (`(namespace_id, user_id)`)
- [ ] `user_id` attached to all user records
- [ ] Destructive tests isolated per namespace
- [ ] No data collision between runs
- [ ] Migration path to real OAuth without schema redesign
- [ ] Supports both hosted Supabase and local config

---

## 19. Open Questions / Future Work (Not Planning Yet)

- Promote "Next" to first-class status
- Add named custom lists (beyond tags)
- Auto-save on Scoop generation (optional)
- Explicit Unrated state vs `null`
- Import/Restore from export
- Shareable Alchemy sessions
- myStatus filters in sidebar

---

## 20. Non-Goals (Explicitly Out of Scope)

- No offline-first architecture
- No vendor-locked AI provider
- No UI animation specs
- No social features
- No legacy layout replication
- No low-level schema/migration docs (handled by technical docs)

---

## 21. Companion Product Documents Referenced

These define **why** the app feels the way it does, and must be understood for rebuild parity:

1. `where_is_the_heart_opus.md` — Soul of the app
2. `ai_personality_opus.md` — Full AI personality + prompts
3. `philosophy_opus.md` — Design principles and emotional targets

(These must be read but not implemented mechanically in code.)

---

## 22. Final Deliverable

This file: `results/PLAN.md`

Contains everything needed to:
- Understand scope
- Architect the system
- Write code
- Ensure AI voice adherence
- Pass benchmark compliance checks

No implementation executed. Ready to begin coding phase only after sign-off on this plan.

---
