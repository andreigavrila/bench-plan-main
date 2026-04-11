# Detail Page Experience Spec (v1)

Defines the intended user experience and narrative hierarchy of the Show Detail page, including the AI‑powered actions that create the app’s “alchemy.”

Grounded in `DetailScreen`, `DetailsDescriptionControl`, `DetailsExploreRecommendationsControl`, and toolbar controls.

---

## 1. Purpose

The Detail page is the **single source of truth** for a show:  
**public facts + your personal relationship + discovery launchpad.**

Users should leave this page feeling:
- oriented in what the show *is*,
- clear on what they *think/feel* about it,
- excited about what to watch next.

---

## 2. First‑15‑Seconds Experience

1. **Mood immersion.**
   - The header carousel (backdrops/posters/logos/trailers where available) sets emotional tone immediately.
2. **Quick taste signal.**
   - Year/length + community score + your rating/status are visible without hunting.
3. **Personal relationship.**
   - Status chips in the toolbar (“Active / Interested / Excited / Done / Quit / Wait”) invite an instant save with minimal friction.
4. **What’s it about, and should I care?**
   - Overview appears early and is short enough to scan.
5. **The Scoop toggle.**
   - “Give me the scoop!” is an *affordance for delight*, not a requirement.

---

## 3. Narrative Hierarchy (Section Intent)

Current order in the app (rebuild must preserve unless intentionally changed):
1) Header media carousel  
2) Core facts row (year/length) + community score  
3) Tag chips (My Tags)  
4) Overview text + Scoop toggle/stream  
5) “Ask about this show” CTA  
6) Genres + languages  
7) Recommendations strand  
8) Explore Similar (concepts → recs)  
9) Providers (“Stream It”)  
10) Cast, Crew  
11) Seasons (TV only)  
12) Budget/Revenue (movies where available)

### 3.1 Header Media
Intent:
- make the show feel alive and cinematic,
- prioritize motion (trailers) when present, but never block reading.

Rules:
- graceful fallback to poster/backdrop only.

### 3.2 Core Facts + Community Score
Intent:
- fast orientation (“what am I looking at?”).

Includes:
- year, runtime/seasons,
- community score bar.

### 3.3 My Relationship Controls
Intent:
- **frictionless save + maintenance.**

Controls:
- **Status/Interest chips in toolbar** (not in the scroll body)
  - “Interested/Excited” map to `Later + Interest`.
  - Reselecting a status triggers removal confirmation and clears My Data.
- **My Rating bar**
  - rating an unsaved show auto‑saves as `Done`.
- **Tags**
  - adding a tag to unsaved show auto‑saves as `Later + Interested`.

Feel:
- quick, playful, no modal walls unless destructive.

### 3.4 Overview + Scoop
Intent:
- overview = factual setup,
- Scoop = emotional taste + fit.

Scoop UX:
- toggle copy changes:
  - no scoop: “Give me the scoop!”
  - cached scoop: “Show the scoop”
  - open: title “The Scoop”
- streams in progressively; user sees “Generating…” not a blank wait.
- freshness: regenerate after ~4 hours on demand.
- persistence intent: Scoop should only persist long‑term if the show is in collection; otherwise it may be ephemeral.

Feel:
- *magazine sidebar review* from a trusted friend.

### 3.5 Ask About This Show
Intent:
- quick deep‑dive with the same persona as Ask.

Rule:
- entering Ask should seed context with this show.

### 3.6 Traditional Recommendations Strand
Intent:
- fast, low‑effort next steps for users who don’t want AI steering.

### 3.7 Explore Similar (Concept Discovery)
Intent:
- turn the user into a co‑curator.

Flow:
1. Tap **Get Concepts**.
2. Select 1+ concepts.
3. Tap **Explore Shows**.

Copy should imply:
- “pick the ingredients you want more of.”

Feel:
- playful experimentation; quick reward.

### 3.8 Streaming Availability
Intent:
- answer “where can I watch it?” without leaving the vibe.

### 3.9 Cast, Crew, Seasons, Budget/Revenue
Intent:
- optional depth for fans; never mandatory to reach discovery.

---

## 4. Busyness vs Power

The page should feel **powerful but not overwhelming**:
- primary actions are clustered early (status, rating, scoop, concepts),
- long‑tail info is down‑page and full‑bleed to reduce clutter.

---

## 5. Critical States

- **Unsaved show**
  - Scoop can be generated but only persists if user saves.
  - Status/rating/tagging triggers auto‑save rules.
- **No trailers / no backdrops**
  - header still feels premium via poster/logo layout.
- **No concepts yet**
  - Explore Similar shows only “Get Concepts” CTA.
- **TV vs Movie**
  - seasons strand only when relevant,
  - runtime vs episode counts handled gracefully.

---

## 6. Open TODOs / Questions

- Alchemy entry remains hidden on Detail for now.
- Trailer playback should be inline.
- Add a 1‑line “why concepts matter” explainer under Get Concepts.
