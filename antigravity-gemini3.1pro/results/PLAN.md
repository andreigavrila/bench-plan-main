# Comprehensive Implementation Plan

## 1. Project Overview & Objectives

**Goal**: Build a personal TV + movie companion for organizing, rating, and discovering entertainment powered by a "taste-aware" AI.
**Core Value proposition**:
- A personalized user collection grouped by distinct statuses (Active, Later, Done, Quit, Wait) and Interest levels.
- Flexible, free-form user tags and an integer-based rating system.
- Robust catalog integration providing access to global entertainment properties seamlessly merged with local data.
- AI discovery driven by user's personal tastes, focusing on conceptual ingredients and interactive conversational curation.

---

## 2. Infrastructure & Execution Architecture

Conforming to the `infra_rider_prd.md`, the platform is designed to run in both local and hosted environments securely.

- **Stack**: Next.js (latest stable) serving both the frontend client and the backend API interactions.
- **Persistence Layer**: Supabase, leveraging a relational database interface with official client SDKs.
- **Benchmarking & Isolation**:
  - `namespace_id`: Every execution, test, or local run operates explicitly in an isolated namespace partition. This mitigates cross-test data pollution.
  - `user_id`: An opaque, stable identifier used to scope user-owned information. 
  - For benchmark context, no OAuth is enforced. Simple header-based injection (e.g., `X-User-Id`) or local dev-mode selectors map users directly into their namespace.
- **Development Experience**:
  - Secretless execution using a standard `.env.example` skeleton.
  - Predictable npm scripts (`npm run dev`, `npm test`, `npm run test:reset`) for rapid testing teardown and reconstruction of isolated namespaces.

---

## 3. Data Model Schema (Supabase)

Following the exact specifications provided in `storage-schema.ts`:

### Primary Models

1. **Shows (`shows`)**
   - Partitioned by combination of `(namespace_id, user_id, id)`.
   - **Fields**: External catalog IDs (`id`, `externalIds`), Title, Classification (`showType`), Posters/Images, Air/Release metrics, and Runtime attributes.
   - **User Overlay Fields**: Status (`myStatus`), Tags (`myTags`), Rating (`myScore`), Interest (`myInterest`), and `aiScoop`.
   - Each user-owned field possesses a corresponding `UpdateDate` to resolve synchronization collisions.

2. **Settings State (`settings`)**
   - Scoped by `(namespace_id, user_id)`.
   - Captures cloud settings, AI token keys, theme toggles, and metadata versioning.

### Merge & Persistence Dynamics
- System adopts a "Backend-as-SSOT" (Single Source of Truth) architecture.
- Re-adding or updating a show fetches public metadata, performing a `selectFirstNonEmpty` overwrite on public metadata fields without destroying user modifications.
- User data conflicts are adjudicated by `*UpdateDate` comparisons.

---

## 4. Application Layout & Routing (Next.js)

- **`/` (Collection Home)**
  - Visual grid grouped explicitly by statuses:
    1. Active (Main focus)
    2. Excited (Later + Excited interest)
    3. Interested (Later + Interested interest)
    4. Compressed collapsible blocks for Wait, Done, Quit.
  - Dynamic filtering capability (Tags, Genres, Media Type toggles).
- **`/search` (Find)**
  - Direct proxy UI for the external content catalog allowing user-initiated curation.
- **`/ask` (Find → Ask AI)**
  - Conversational chat UI resolving context over TV/Movies. 
  - Inline "Mentioned Shows" extraction parser (`Title::externalId::mediaType`).
- **`/alchemy` (Find → Alchemy)**
  - A multi-step blending wizard: Select ≥ 2 catalog items -> Request overlapping Concepts -> Select Catalyst Concepts -> Recommend resultant Titles.
- **`/detail/[type]/[id]` (Show Detail Page)**
  - Centralized truth node. Merges remote public attributes and local context tags.
  - Streaming generation for "The Scoop" (Cache-busting roughly every ~4 hours).
  - Component strands for Similar items, Seasons, and Person/Crew horizontal profiles.
  - Interactive "Get Concepts" discovery gateway (Explore Similar feature).
- **`/person/[id]` (Cast & Crew)**
  - Person-focused insights: bios, credits, and lightweight analytics widgets mapping back to `/detail`.
- **`/settings`**
  - AI selection, API Key injections, and robust ZIP/JSON "Export My Data" functions.

---

## 5. AI Services & Discovery Ecology

The AI layer maintains consistent persona requirements: warm, hyper-focused on movie/TV craft ("Taste-Aware"), opinionated, concise, and spoiler-safe. 

### Core Generative Pipelines

1. **Ask (Conversational Engine)**:
  - Operates dynamically given short-turn message sets and the local user's show library contextual data.
  - Automatically summarizes history roughly every ~10 segments to avoid token exhaustion.
2. **The Scoop (Review Evaluator)**:
  - Targeted structural output (~150-350 avg limit). Implements strong subjective stances, fit-warnings, and a core conversational recommendation paragraph.
3. **Concept Extracts**:
  - Specialized extraction pipeline mapping complex themes/structures into 1-3 word bulleted abstractions (e.g., "slow-burn dread").
4. **Alchemy Recommendations**:
  - Leverages user-supplied combinations to isolate specific overlapping concepts.
  - Maps to deterministic JSON/structured responses that inherently carry catalog IDs (`externalId`), resolving strictly to valid data nodes with specific 1-3 sentence rationales tied to concepts.

---

## 6. Implementation Stages & Build Steps

1. **Setup & Orchestration**: 
  - Initialize Next.js environment & Tailwind configuration.
  - Stand up Supabase models with RLS tuned precisely for `(namespace_id, user_id)` isolation blocks.
2. **Catalog Broker (Data Ingestion Layer)**:
  - Create the agnostic TMDB/Trakt proxy, normalizing data payload to match `Show` definitions. 
  - Implement the `merge` mechanics handling public freshness + user overlay timestamps.
3. **Core UX Development**:
  - Formulate Detail page layout, Home Library grids, and status toggling components.
4. **AI Layering**:
  - Spin up system prompts matching the "Water-cooler gossip" personality mappings.
  - Integrate concept generation, Scoop streaming, and chat memory abstractions.
5. **Quality Hardening & Packaging**:
  - Guarantee "zero setup" developer access. Validate export backup scripts.
  - Establish `npm run test:reset` scripts targeting isolated cleanup testing.
