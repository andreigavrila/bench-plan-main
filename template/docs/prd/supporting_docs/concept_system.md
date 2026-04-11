# Concept System Spec (v1)

Defines what “concepts” are in the product, why they matter to users, and the generation/selection rules needed to preserve the app’s alchemy.

Grounded in `ShowConceptRequest` and usage in Explore Similar + Alchemy.

---

## 1. What a Concept Is (User Definition)

A **concept** is a *short ingredient* that captures the **core feeling** of a show: its vibe, structure, emotional temperature, or signature style.  

Concepts are not genres or plot points. They are the *taste DNA* that lets the app find “shows like this in the way I actually mean.”

Examples:
- “hopeful absurdity”
- “case‑a‑week”
- “quirky makeshift family”
- “light in dark moments”

---

## 2. Why Concepts Matter

Concepts power discovery that:
- reflects *how you experience* a show, not just what category it’s in,
- exposes *surprising similarities* across genres,
- gives users control over *which ingredients* they want more of.

---

## 3. Concept Taxonomy (Implicit Today)

Concepts may draw from:
1. **Format/structure**
   - procedural vs serialized  
   - episodic flow, season arcs.
2. **Tone & vibe**
   - quirky, fast‑paced, cozy, tense, romantic, etc.
3. **Emotional palette**
   - optimism, togetherness, catharsis, dread, bittersweetness.
4. **Relationship dynamics**
   - found family, oddball pairings, rivals‑to‑friends.
5. **Craft / intelligence**
   - sharp writing, puzzle‑box plotting, stylish cinematography, music‑forward.
6. **Genre‑flavor (not label)**
   - “ironic crime‑solving” vs “crime drama.”

---

## 4. Generation Rules

Current hard rules (from `ShowConceptRequest`):
- Generate a short list of concepts per request (current implementation uses a small fixed number).
- When multiple shows are provided (Alchemy), concepts must be **shared across all** input shows.
- Output format:
  - bullet list only,
  - each concept 1–3 words,
  - evocative phrasing, no explanation,
  - no plot details or spoilers.

Prompt focus axes used today:
- structural form (procedural vs serialized, episodic flow, season arcs),
- unique tone/vibe (quirky, fast‑paced, unusual),
- emotional tones (optimism, togetherness, “light in dark moments”),
- relationship dynamics (makeshift family, evolving bonds),
- craft cues (script intelligence, pacing),
- music/cinematography presence when relevant.

Quality constraints (product requirements):
- **Specificity over genericity.**
  - “good characters” is invalid.
  - “hopeful absurdity” is valid.
- **Diversity.**
  - Concepts should cover different axes (structure, vibe, emotion) rather than 8 synonyms.
- **Order by strength.**
  - Best “aha” concepts first.

Recommended rebuild quality heuristic (non‑prescriptive):
- Prefer concepts that are:
  - shared and core (for multi‑show),
  - evocative and specific (ingredient‑like),
  - useful to steer recommendations,
  - varied across axes (structure/vibe/emotion/craft).

---

## 5. Selection UX Rules

Explore Similar (single show):
- User selects **Get Concepts**.
- Concepts appear as selectable chips.
- User can choose 1+ concepts.
- Selection limits should stay consistent with Alchemy’s selection cap.

Alchemy (multi‑show):
- User selects **≥2 input shows**.
- User selects **Conceptualize Shows** to fetch concepts.
- User selects up to a capped number of concepts (current UI caps selection at 8).
- Selecting/unselecting concepts clears downstream results.

User guidance:
- UI should hint “pick the ingredients you want more of.”
- Empty state copy should nudge toward selecting at least one concept.

---

## 6. Concepts → Recommendations Contract

Concept Recommendations must:
- reference selected concepts explicitly in reasoning,
- bias toward recent shows but allow classics/hidden gems,
- return real items with valid external catalog IDs (or enough data to resolve them).

Counts:
- Explore Similar: **5 recs** per round.
- Alchemy: **6 recs** per round.

---

## 7. Great vs Weak Concepts (Illustrative)

Great:
- “hopeful absurdity”
- “slow‑burn dread”
- “sincere teen chaos”
- “elegant puzzle‑box”

Weak:
- “good writing”
- “great characters”
- “funny”
- “action”

---

## 8. Notes

- This spec intentionally does not prescribe concept chip layout or grouping.
- Multi‑show concept generation should return a larger pool of options than single‑show (while still keeping selection capped in the UI).
- No long‑press concept explainers are specified.
