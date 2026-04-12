# Implementation Plan: TV/Movie Companion App

## 1. Overview

Build a personal TV + movie companion app using **Next.js** and **Supabase**. Users collect, organize, rate, and discover entertainment through their taste profile. The app provides multiple discovery paths: traditional search, conversational AI ("Ask"), "Alchemy" concept blending, and per-show "Explore Similar."

---

## 2. Tech Stack & Infrastructure

### Runtime
- **Next.js** (latest stable) — full-stack web application

### Persistence
- **Supabase** — hosted or local (namespace-isolated)

### Environment Interface
- `.env.example` with required variables:
  - `NEXT_PUBLIC_SUPABASE_URL`
  - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
  - `SUPABASE_SERVICE_ROLE_KEY` (server-only)
  - `TMDB_API_KEY` (content catalog)
  - `OPENAI_API_KEY` or `AI_PROVIDER_KEY` (AI)
  - `AI_MODEL`
  - `NAMESPACE_ID` (build isolation)
  - `DEFAULT_USER_ID` (dev identity)

### Scripts
- `npm run dev` — start app
- `npm run test` — run tests
- `npm run test:reset` — reset test data for namespace

---

## 3. Data Model

### 3.1 Show Entity

| Field | Type | Notes |
|-------|------|-------|
| id | string | Primary key |
| title | string | |
| showType | enum | movie/tv/person/unknown |
| externalIds | object | Catalog IDs |
| overview | string? | |
| genres | string[] | |
| tagline | string? | |
| posterUrlString | string? | |
| backdropUrlString | string? | |
| logoUrlString | string? | |
| voteAverage | number? | |
| voteCount | number? | |
| popularity | number? | |
| releaseDate | date? | |
| runtime | number? | Movie |
| budget | number? | Movie |
| revenue | number? | Movie |
| numberOfEpisodes | number? | TV |
| numberOfSeasons | number? | TV |
| episodeRunTime | number[] | TV |
| seriesStatus | string? | TV |
| myTags | string[] | User |
| myTagsUpdateDate | date? | User |
| myScore | number? | User |
| myScoreUpdateDate | date? | User |
| myStatus | enum? | User (Active/Later/Wait/Done/Quit) |
| myStatusUpdateDate | date? | User |
| myInterest | enum? | User (Interested/Excited) |
| myInterestUpdateDate | date? | User |
| aiScoop | string? | AI |
| aiScoopUpdateDate | date? | AI |
| creationDate | date? | |
| detailsUpdateDate | date? | |
| providerData | object | Streaming availability |

### 3.2 CloudSettings Entity

| Field | Type |
|-------|------|
| id | string (default "globalSettings") |
| userName | string |
| version | number |
| catalogApiKey | string? |
| aiApiKey | string? |
| aiModel | string |

### 3.3 Namespace & User Isolation

- All records scoped to `(namespace_id, user_id)`
- Namespace from `NAMESPACE_ID` env var
- User from request header (`X-User-Id`) or `DEFAULT_USER_ID`

---

## 4. Core Features

### 4.1 Collection Home
- Display shows grouped by status: Active → Excited → Interested → Other (Wait/Done/Quit)
- Filter sidebar: All, tags, genres, decades, community score, media type
- Media toggle: All / Movies / TV
- Tile shows poster, title, user badges

### 4.2 Search
- Text search via external catalog (TMDB)
- Results in poster grid
- In-collection indicator on tiles
- Opens Show Detail on selection

### 4.3 Ask (AI Chat)
- Conversational discovery
- 80 starter prompts on welcome view
- Inline show mentions with selectable strip
- Context preserved during session
- Auto-summarization after ~10 messages

### 4.4 Alchemy
- Select 2+ shows → Extract concepts → Select concepts → Get recs
- Chaining allowed for more discovery
- 6 recommendations per round

### 4.5 Explore Similar
- From Detail: Get Concepts → Select → Explore Shows
- 5 recommendations per round

### 4.6 Show Detail
Sections in order:
1. Header media carousel
2. Core facts + Community score
3. My Status/Interest chips
4. My Rating
5. My Tags
6. Overview
7. AI Scoop ("The Scoop")
8. Traditional recommendations
9. Explore Similar
10. Streaming availability
11. Cast & Crew
12. Seasons (TV)
13. Budget/Revenue (movie)

### 4.7 Person Detail
- Image gallery, bio
- Analytics charts
- Filmography by year
- Credit selection → Show Detail

### 4.8 Settings
- Font size
- Search on launch
- Username
- API keys (catalog, AI)
- AI model selection
- Export My Data (.zip with JSON backup)

---

## 5. Auto-Save & Business Rules

### 5.1 Save Triggers
- Setting any status
- Choosing Interested/Excited chip
- Rating an unsaved show
- Adding a tag

### 5.2 Default Values
- No explicit status → `Later` + `Interested`
- Rating without status → `Done` (implies watched)

### 5.3 Removing
- Reselect active status → confirmation → clear all My Data

### 5.4 Merge Rules
- Public data: `selectFirstNonEmpty(new, old)`
- User data: newer timestamp wins

### 5.5 AI Scoop
- Cached 4 hours
- Only persisted if show is in collection

---

## 6. AI Surfaces

### 6.1 Voice Requirements
- Fun, chatty TV/movie nerd friend
- Opinionated, spoiler-safe by default
- Specific, not generic
- Warm but honest about mixed reception

### 6.2 Ask Chat
- Output structured: `{ commentary: string, showList: "Title::id::type;;..." }`

### 6.3 Scoop
- Personal take, stack-up vs reviews, The Scoop paragraph, fit/warnings, verdict
- 150-350 words

### 6.4 Concepts
- 1-3 word evocative bullets
- 8 concepts per generation
- Avoid generic: "good characters", "great story"

### 6.5 Concept Recs
- 5-6 recommendations with reasons citing concepts
- Real catalog items with valid IDs

---

## 7. Project Structure

```
/
├── app/
│   ├── layout.tsx
│   ├── page.tsx (Home/Collection)
│   ├── globals.css
│   ├── find/
│   │   ├── page.tsx (mode switcher)
│   │   ├── search/page.tsx
│   │   ├── ask/page.tsx
│   │   └── alchemy/page.tsx
│   ├── detail/[id]/page.tsx
│   ├── person/[id]/page.tsx
│   ├── settings/page.tsx
│   └── api/
│       ├── supabase/
│       ├── tmdb/
│       ├── openai/
│       └── user/
├── lib/
│   ├── supabase.ts
│   ├── tmdb.ts
│   ├── ai.ts
│   └── types.ts
├── components/
│   ├── layout/
│   ├── collection/
│   ├── detail/
│   ├── find/
│   └── shared/
├── hooks/
└── styles/
```

---

## 8. Implementation Order

### Phase 1: Foundation
1. Supabase schema + migrations
2. .env.example + config
3. Basic Next.js setup with layout
4. Supabase client + basic CRUD for Shows

### Phase 2: Collection
5. Collection Home with filters
6. Status/Interest/Tags/Rating editing
7. Auto-save triggers

### Phase 3: Discovery
8. Search (TMDB integration)
9. Show Detail page
10. Person Detail page

### Phase 4: AI Features
11. AI Scoop generation
12. Ask chat interface
13. Concepts + Explore Similar
14. Alchemy flow

### Phase 5: Settings & Polish
15. Settings page
16. Export functionality
17. UI polish + responsive

---

## 9. Critical Considerations

- **User always wins**: User data takes precedence over public data
- **Timestamps**: All user fields track modification time
- **Namespace isolation**: Every query filters by namespace_id
- **Spoiler-safe default**: AI surfaces avoid plot specifics
- **Real IDs**: AI recommendations must map to actual catalog items
- **Migration safety**: Preserve user data across schema changes

---

## 10. Open Questions (per PRD)

1. Should "Next" become first-class status?
2. Custom named lists beyond tags?
3. AI Scoop on unsaved show → auto-save?
4. Clear rating → explicit "Unrated" vs nil?
5. Import/Restore from export?
6. Save Alchemy sessions as reusable?