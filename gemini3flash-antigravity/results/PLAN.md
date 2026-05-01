# Implementation Plan - Antigravity

This document outlines the architectural strategy and implementation roadmap for **Antigravity**, a personal TV and movie companion application.

---

## 1. Project Overview

Antigravity is a high-end personal library and discovery tool for entertainment. It emphasizes "taste-aware" AI discovery grounded in the user's personal collection, status, and custom ratings.

### Key Value Propositions
- **Personalized Library**: Effortless organization using statuses (Active, Later, Wait, Done, Quit) and free-form tags.
- **AI-Powered Discovery**: "Ask" (conversational), "Alchemy" (concept blending), and "Explore Similar" (per-show concepts).
- **Premium Aesthetics**: A modern, immersive UI with glassmorphism, dynamic transitions, and cinematic media presentation.

---

## 2. Technical Stack & Architecture

### Core Technologies
- **Framework**: Next.js (App Router) for hybrid rendering and server-side logic.
- **Persistence**: Supabase for relational data storage and real-time capabilities.
- **Styling**: Vanilla CSS with a centralized Design System (Design Tokens).
- **AI Integration**: OpenAI / Anthropic / Google AI via server-side routes.

### Architectural Pattern: Fractal Architecture
We will use a fractal directory structure to ensure isolation, co-location, and scalability.

```text
src/
├── config/              # Environment variables, constants, API endpoints
├── theme/               # CSS Variables (colors, spacing, glassmorphism tokens)
├── components/          # Shared UI primitives (Buttons, Inputs, PosterGrid)
├── hooks/               # Global hooks (useSupabase, useAuthInjection)
├── utils/               # Global pure functions (date formatting, ID mapping)
├── services/            # Edge functions/Server actions for AI and Catalog
└── pages/               # Top-level routes
    ├── Home/            # Collection Library
    ├── Find/            # Discovery Hub (Search, Ask, Alchemy)
    ├── Detail/          # Show Detail Experience
    ├── Person/          # Talent Deep-Dive
    └── Settings/        # User Settings & Export
```

#### Humble Component Rule
All UI components in `.tsx` files will be "humble," containing only markup and bindings. Complex logic, data fetching, and event handlers will be extracted into custom hooks (e.g., `useShowDetailLogic`).

---

## 3. Data Model & Persistence

### Supabase Schema (Primary Entities)
1. **`shows`**: The core entity storing public catalog data + user overlay.
   - `id`: Unique stable identifier (external ID).
   - `user_id`: Opaque stable string for ownership.
   - `namespace_id`: Build/run isolation identifier.
   - `my_status`: Enum (active, later, wait, done, quit).
   - `my_interest`: Enum (excited, interested).
   - `my_rating`: Double (user score).
   - `my_tags`: Array of strings.
   - `ai_scoop`: Text (personality review).
   - `*_update_date`: Timestamps for all user-editable fields.
   - `catalog_data`: JSONB for metadata (title, overview, genres, poster_url, etc.).

2. **`settings`**: User-specific application settings.
   - `user_id` / `namespace_id`
   - `user_name`
   - `catalog_api_key`, `ai_api_key`, `ai_model`

### Build Isolation (Namespace)
Every build/run will be assigned a `namespace_id`. All queries will include this ID to prevent data collisions between benchmark runs.

---

## 4. UI & Feature Roadmap

### 4.1. Design System (Foundation)
- **Fluid Grid**: Responsive layout for mobile and desktop.
- **Glassmorphism**: Translucent panels and blurred backgrounds using `backdrop-filter`.
- **Typography**: Modern sans-serif (e.g., Inter/Outfit) with strict hierarchy.
- **Transitions**: Smooth page transitions and micro-animations for hover/click states.

### 4.2. Core Features
- **Collection Home**: 
  - Dynamic grouping by status: Active (hero), Excited, Interested, and Collapsed Others.
  - Sidebar for Tag and Data filters.
- **Show Detail**:
  - Immersive header with trailers (inline playback) and cinematic media.
  - Toolbar for "One-tap" status updates.
  - Progressive streaming for "The Scoop."
- **Find/Discover Hub**:
  - **Search**: Direct external catalog query.
  - **Ask**: Chat interface returning structured objects (`commentary` + `showList`). 
  - **Alchemy**: Step-based blending UI (Select Shows -> Conceptualize -> Alchemize).

---

## 5. AI Service Strategy

### Personality Enforcement
The "TV/movie nerd friend" persona will be maintained via specific system prompts across all surfaces:
- **Scoop**: Magazine sidebar style, opinionated, 150-350 words.
- **Concepts**: 1-3 evocative words, vibe-based, no generic filler.
- **Ask**: Conversational, picks favorites, spoiler-safe by default.

### Structured Output Contracts
All AI responses will follow strict mapping rules to ensure discovery is actionable:
- **Mentioned Shows**: `Title::externalId::mediaType;;...`
- **Alchemy Reasons**: Explicitly referencing selected concepts in 1-3 sentences.

---

## 6. Implementation Phases

1. **Phase 1: Foundation**
   - Setup Next.js boilerplate and Supabase client.
   - Implement `theme` tokens and `X-User-Id` injection.
   - Define migrations for `shows` and `settings`.

2. **Phase 2: Management UI**
   - Create Show Detail page with My Data controls (status, rating, tags).
   - Implement "Auto-save" and "Removal confirmation" logic.
   - Build Collection Home with status-based layout.

3. **Phase 3: AI Discovery (Core)**
   - Implement "The Scoop" with streaming.
   - Build "Ask" chat interface with mentioned-shows row.
   - Implement per-show "Explore Similar" (Concepts -> Recs).

4. **Phase 4: Advanced Discovery & Tools**
   - Implement "Alchemy" multi-round blending logic.
   - Create Person Detail page with filmography and analytics.
   - Build Settings page with Data Export (.zip/JSON).

5. **Phase 5: Polish & Test**
   - Final visual pass (animations, premium aesthetic).
   - Implement namespace reset scripts for benchmark testing.
   - Ensure lint-clean and modular codebase.

---

## 7. Success & Compliance

- **Isolation**: Confirmed through namespace-scoped queries.
- **Identity**: Opaque `user_id` handled via injection.
- **Persistence**: Server-side Supabase as the single source of truth.
- **Parity**: Adherence to the functional and emotional requirements defined in the PRD.
