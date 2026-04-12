# AI Prompting & Context Guide (v1)

This document captures the *behavioral contracts* for the app’s AI surfaces: what context is included, what the AI must output, and the constraints that preserve the product’s voice and usefulness. It is intentionally platform- and technology-agnostic.

This is not a “prompt cookbook.” The goal is rebuild parity: a new implementation should reproduce the same *user-visible behavior* even if prompts and providers change.

---

## 1. Shared Rules (All AI Surfaces)

All AI surfaces must:
- Stay within TV/movies (redirect back if asked to leave that domain).
- Be spoiler-safe by default unless the user explicitly requests spoilers.
- Be opinionated and honest (don’t gush for no reason; acknowledge mixed reception when relevant).
- Prefer specific, vibe/structure/craft-based reasoning over generic genre summaries.

Where possible, AI outputs should be actionable:
- recommended titles should resolve to real catalog items.

---

## 2. Shared Inputs (Typical)

Depending on surface, the AI may receive:
- the user’s library (saved shows) and associated My Data (status/interest/tags/rating/scoop)
- current show context (for “Ask about this show” and Scoop)
- selected concepts (for Explore Similar / Alchemy)
- recent conversation turns (for chat surfaces), with older turns summarized

The product intent is “taste-aware AI”: it should feel grounded in what the user saves and how they label it.

---

## 3. Surface Contracts

### 3.1 Ask (Chat)
Purpose:
- conversational discovery grounded in taste.

Contract:
- respond like a friend in dialogue (not an essay) unless the user asks for depth
- be willing to pick favorites
- use simple formatting and bulleted lists when recommending multiple titles

### 3.2 Ask with Mentions (Structured “Mentioned Shows”)
Purpose:
- chat + a reliable, machine-readable list of shows mentioned so the UI can render a “mentioned shows” row.

Contract:
- output a structured object with:
  - `commentary`: the user-facing response text (no external IDs included)
  - `showList`: a machine-readable list of shows referenced in `commentary`

Required `showList` string format:
- `Title::externalId::mediaType;;Title2::externalId::mediaType;;...`

Notes:
- The structured format and the parser must exactly match (no ambiguity).
- `externalId` must be an identifier the app can use to resolve the show in the external catalog (implementation-defined).

### 3.3 Scoop (Detail Page)
Purpose:
- a personality-driven, spoiler-safe “taste review” that helps the user decide if it’s worth it.

Contract:
- structured as a short “mini blog post of taste”
- includes: personal take, honest “stack-up,” the Scoop centerpiece, fit/warnings, and a verdict
- streams progressively if the UI supports it (user shouldn’t stare at a blank state)

### 3.4 Concepts (Single-Show and Multi-Show)
Purpose:
- generate short, evocative concept “ingredients” that capture the core feeling and steer discovery.

Contract:
- returns a bullet list only
- concepts are 1–3 words, evocative, and spoiler-free
- avoids generic concepts (“good characters,” “great story”)
- for multi-show concept generation: concepts must represent shared commonality across all inputs

### 3.5 Concept-Based Recommendations (Explore Similar / Alchemy)
Purpose:
- recommendations steered by user-selected concepts.

Contract:
- returns a list of recommended shows with concise reasons (not synopses)
- reasons should explicitly reflect the selected concepts
- recommendations must resolve to real catalog items when possible

---

## 4. Conversation Summarization (Chat Surfaces)

Purpose:
- preserve the feel of the conversation while controlling context depth.

Contract:
- older turns may be summarized into 1–2 sentences
- summaries must preserve the same persona/tone as the chat surface (no sterile “system summary” voice)

---

## 5. Guardrails & Fallbacks

If recommendations cannot be resolved to real catalog items:
- show them as non-interactive and/or hand off to Search.

If structured output parsing fails:
- retry once with stricter formatting instructions,
- otherwise fall back to unstructured commentary + Search handoff.

