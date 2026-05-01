# Implementation Plan: TV + Movie Companion

## 1. Overview
A personal entertainment companion for collecting, organizing, and discovering movies and TV shows. The system centers on a user's "taste profile" (collection, tags, ratings, statuses) which powers AI-driven discovery (Ask, Alchemy, Explore Similar).

## 2. Architecture & Tech Stack
- **Framework:** Next.js (latest stable)
- **Persistence:** Supabase (PostgreSQL)
- **Identity/Isolation:**
  - `namespace_id`: Build-level isolation to prevent data collisions.
  - `user_id`: User-level ownership for all records.
  - Partitioning: `(namespace_id, user_id)`.
- **Auth:** Development identity injection (e.g., `X-User-Id` header) with a path to migrate to OAuth.
- **AI Integration:** LLM integration for "The Scoop", "Ask" chat, "Alchemy" concept blending, and "Explore Similar".

## 3. Data Model
Based on `storage-schema.ts`, the primary entities are:
- **Show:** Stores catalog metadata + user overlay (`myStatus`, `myInterest`, `myTags`, `myScore`) + AI data (`aiScoop`).
- **CloudSettings:** User profile, API keys, and AI model selection.
- **AppMetadata:** Versioning for migrations.
- **LocalSettings/UIState:** Client-side preferences (font size, `autoSearch`, filters).

### Merge & Sync Rules
- **Catalog Refresh:** Merge new public data into existing `Show` using `selectFirstNonEmpty`.
- **User Data:** Conflict resolution via timestamps (`myStatusUpdateDate`, etc.)—newer wins.

## 4. Core Feature Implementation

### 4.1 Collection Home
- **Views:** Filtered library (All, Tag, Genre, Decade, Community Score).
- **Grouping:** Status-based sections:
  1. Active
  2. Excited (Later + Excited)
  3. Interested (Later + Interested)
  4. Other (Wait, Quit, Done, etc.)
- **Toggles:** All / Movies / TV.

### 4.2 Find & Discover Hub
- **Search:** External catalog search. Items in collection are marked.
- **Ask (AI Chat):**
  - Persona: "Fun, chatty TV/movie nerd friend".
  - Features: Context-aware chat, mentioned shows strip (`Title::externalId::mediaType`), conversation summarization.
- **Alchemy (Blending):**
  - Flow: Select 2+ shows $\rightarrow$ Conceptualize (shared concepts) $\rightarrow$ Select 1-8 concepts $\rightarrow$ AI Recommendations.
  - Ability to chain results.

### 4.3 Show Detail Page
- **Narrative Hierarchy:** Header Carousel $\rightarrow$ Core Facts/Score $\rightarrow$ My Tags $\rightarrow$ Overview/Scoop $\rightarrow$ Ask $\rightarrow$ Genres $\rightarrow$ Recs $\rightarrow$ Explore Similar $\rightarrow$ Streaming $\rightarrow$ Cast/Crew $\rightarrow$ Seasons/Budget.
- **Interactive Controls:**
  - Status chips in toolbar (Auto-save logic).
  - Rating slider (Auto-saves as `Done` if unsaved).
  - Tag picker (Auto-saves as `Later + Interested` if unsaved).
- **Explore Similar:** Get Concepts $\rightarrow$ Select $\rightarrow$ Explore Shows.

### 4.4 AI Services
- **The Scoop:** personality-driven, spoiler-safe review. Cached for 4 hours.
- **Concept Engine:** Generates 1-3 word evocative "ingredients" (e.g., "hopeful absurdity").
- **Recommendation Engine:** Maps AI output to real catalog items via external IDs.

### 4.5 Person Detail Page
- Bio, image gallery, filmography grouped by year.
- Analytics charts for project ratings, genres, and projects-by-year.

## 5. Infrastructure & DevEx
- **Environment:** `.env.example` for API keys and Supabase credentials.
- **Scripts:** `npm run dev`, `npm test`, `npm run test:reset` (scoped to `namespace_id`).
- **Deployment:** No Docker requirement for cloud agents.
- **Data Integrity:** JSON Export/Backup functionality.

## 6. Implementation Roadmap
1. **Phase 1: Foundation:** Setup Next.js + Supabase schema + Namespace/User isolation.
2. **Phase 2: Core Collection:** Implement Search, Show Detail (Basic), and Collection Home.
3. **Phase 3: User Overlay:** Implement Status/Interest/Tag/Rating logic and merge rules.
4. **Phase 4: AI Integration:**
   - AI Scoop generation & caching.
   - "Ask" chat interface and prompt engineering.
   - Concept generation and "Explore Similar".
   - "Alchemy" blending workflow.
5. **Phase 5: Refinement:** Person Detail page, Analytics charts, Settings, and Data Export.
6. **Phase 6: Validation:** Test against "Discovery Quality Bar" and Infrastructure Rider requirements.
