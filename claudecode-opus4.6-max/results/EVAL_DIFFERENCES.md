# Evaluation Scoring Differences: PLAN_EVAL vs PLAN_EVAL_SELF

Both evaluators extracted the same 99 requirements and agreed on 85 of them.
They disagreed on **14 requirements** — listed below with each side's justification, the original doc text, and a verdict.

| | PLAN_EVAL (external) | PLAN_EVAL_SELF (self) |
|---|---|---|
| **Overall** | **90.9%** | **97.0%** |
| Critical (30) | 98.3% | 98.3% |
| Important (67) | 87.3% | 97.0% |
| Partial count | 18 | 5 |

---

## Disagreement 1: PRD-013 — Dev auth injection documentation

**Severity:** important

| Evaluator | Score | Justification |
|---|---|---|
| PLAN_EVAL | **partial** | "The injection path and production gating are specified, but the plan never assigns a documentation task for benchmark operators." |
| PLAN_EVAL_SELF | **full** | "In dev/test mode: accept `X-User-Id` header... In production mode: the dev injection path is disabled" |

**Original doc** (`infra_rider_prd.md` 5.1):
> This must be: **clearly documented**, disabled or gated for production mode.

**Plan says** (1.3): "In dev/test mode: accept `X-User-Id` header or fall back to `DEV_USER_ID` env var. Expose a lightweight dev-only user selector in the UI (gated by `NODE_ENV !== 'production'`)."

**Verdict: PLAN_EVAL is right.** The PRD explicitly requires it be "clearly documented." The plan describes the mechanism but never includes a documentation deliverable. The self-evaluator conflated *describing* the feature with *planning to document* it.

---

## Disagreement 2: PRD-017 — No Docker requirement

**Severity:** important

| Evaluator | Score | Justification |
|---|---|---|
| PLAN_EVAL | **partial** | "The plan chooses cloud-friendly technologies, but it never explicitly commits to a no-Docker-required path or documents Docker as optional only." |
| PLAN_EVAL_SELF | **full** | "Plan uses env vars for Supabase connection and npm for Next.js; no Docker dependency anywhere in the plan" |

**Original doc** (`infra_rider_prd.md` 2):
> The Supabase instance may be hosted (preferred for cloud-agent runs) or local (optional for developer convenience). **Builds MUST NOT assume Docker is available.**

**Plan says** (0, 1.1): Uses Next.js + Supabase with env vars. No mention of Docker anywhere.

**Verdict: PLAN_EVAL_SELF is right.** The absence of Docker in the plan *is* the compliance. The PRD says "MUST NOT assume Docker is available" — the plan doesn't assume it. Requiring an explicit "we don't use Docker" statement is over-reading the requirement.

---

## Disagreement 3: PRD-030 — Ask and Alchemy state session-only

**Severity:** important

| Evaluator | Score | Justification |
|---|---|---|
| PLAN_EVAL | **partial** | "Alchemy is explicitly session-only, but Ask is only described as client-side state and the plan does not explicitly say it clears on leave/reset." |
| PLAN_EVAL_SELF | **full** | "Conversation state: held in client-side React state"; "Session-only: all Alchemy state is client-side" |

**Original doc** (`product_prd.md` 5.7):
> | Ask chat history | No | Session only | **Cleared when resetting/leaving Ask.** |
> | Mentioned shows strip | No | Session only | Derived from current chat context. |

**Plan says** (6.4.2): "Conversation state: held in client-side React state." (6.4.3): "Session-only: all Alchemy state is client-side. Leaving the page clears it."

**Verdict: PLAN_EVAL is right.** The PRD explicitly says Ask is "cleared when resetting/leaving Ask." The plan says Ask state is in React state (which *implies* clearing) but never states the clearing behavior. Alchemy explicitly says "Leaving the page clears it" — Ask doesn't get the same treatment. An implementer could reasonably persist Ask state across navigation.

---

## Disagreement 4: PRD-033 — Sync libraries/settings and merge duplicates

**Severity:** important

| Evaluator | Score | Justification |
|---|---|---|
| PLAN_EVAL | **partial** | "The plan covers settings conflict resolution and show-field merges, but it does not plan duplicate detection or a fuller cross-device library sync strategy." |
| PLAN_EVAL_SELF | **full** | "Server-side source of truth inherently syncs library; Phase 6 task 1 settings sync; merge logic + PK dedup" |

**Original doc** (`product_prd.md` 5.10):
> When sync is enabled:
> - The library and settings remain consistent across devices.
> - Conflicts resolve per field using the most recent edit timestamp.
> - **Duplicate items are detected and merged transparently, without user disruption.**

**Plan says** (3.4): Merge logic for catalog vs user fields with timestamp comparison. (Phase 6 Task 1): "Implement cloud settings sync (conflict resolution by `version` timestamp)."

**Verdict: PLAN_EVAL is right.** The PRD explicitly requires duplicate detection and transparent merging. The plan's merge logic only handles the case where catalog data refreshes for an *existing* show — it doesn't address detecting duplicates across devices or merging them transparently. The self-evaluator's claim that PK dedup handles this is a stretch: composite PKs prevent exact duplicates but not semantic duplicates (same show saved from different catalog lookups).

---

## Disagreement 5: PRD-034 — Preserve libraries across data-model upgrades

**Severity:** critical

| Evaluator | Score | Justification |
|---|---|---|
| PLAN_EVAL | **partial** | "The plan mentions versioning and additive migrations, but it does not plan concrete upgrade/backfill steps that guarantee legacy libraries carry forward safely." |
| PLAN_EVAL_SELF | **full** | "Sequential migrations + data_model_version tracking; migrations are additive; PRD 5.11 requires data continuity" |

**Original doc** (`product_prd.md` 5.11):
> The app must preserve user libraries across updates, even when the underlying data model changes. On upgrade, any existing saved shows and "My Data" are **automatically brought forward** into the new model in a safe, transparent way, without requiring user intervention. Users should **never lose** their collection, ratings, tags, statuses, interest levels, or AI Scoop due to an update.

**Plan says** (2.2): "Future migrations are numbered sequentially. `app_metadata.data_model_version` tracks schema version for any application-level migration logic." (9): "Migrations are additive where possible."

**Verdict: PLAN_EVAL is right.** The PRD demands automatic data carry-forward — the plan only provides the *infrastructure* for migrations (version tracking, sequential files) without any concrete strategy for backfilling, transforming, or verifying that existing data survives a schema change. "Additive where possible" is aspirational, not a plan. This is the most consequential gap because it's the only `critical` item one evaluator marks partial.

---

## Disagreement 6: PRD-050 — Search has no AI voice

**Severity:** important

| Evaluator | Score | Justification |
|---|---|---|
| PLAN_EVAL | **partial** | "The Search flow is non-AI by design, but the plan does not explicitly preserve a straight catalog-search tone as a UX constraint." |
| PLAN_EVAL_SELF | **full** | "Search page is purely TMDB catalog queries with no AI involvement" |

**Original doc** (`ai_voice_personality.md` 1):
> **Search has no AI voice** (it should remain a straightforward catalog search experience).

**Plan says** (6.4.1): "Text input with live or submit-based search. Results displayed as ShowGrid." No AI mentioned.

**Verdict: PLAN_EVAL_SELF is right.** The plan describes Search as a pure catalog operation with no AI involvement. The requirement is that Search has no AI voice — the plan doesn't give it one. Requiring an explicit "this must not be AI" constraint in the plan is unnecessary when the design already excludes AI by construction.

---

## Disagreement 7: PRD-051 — Show Detail narrative section order

**Severity:** important

| Evaluator | Score | Justification |
|---|---|---|
| PLAN_EVAL | **partial** | "The plan front-loads rating and status controls and does not preserve the supporting doc's exact narrative section order." |
| PLAN_EVAL_SELF | **full** | "Lists 15 sections following the detail_page_experience.md narrative hierarchy" |

**Original doc** (`detail_page_experience.md` 3):
> 1) Header media carousel
> 2) Core facts row + community score
> 3) **Tag chips (My Tags)**
> 4) **Overview text + Scoop toggle**
> 5) "Ask about this show" CTA
> 6) Genres + languages
> 7) Recommendations strand
> 8) Explore Similar
> 9) Providers
> 10) Cast, Crew
> 11) Seasons (TV only)
> 12) Budget/Revenue

**Plan says** (6.5):
> 1) Header media carousel
> 2) Core facts row
> 3) **My Rating bar** (not in original order)
> 4) **Status/Interest toolbar** (not in original order)
> 5) **My Tags**
> 6) **Overview** (was item 4 in original)
> 7) AI Scoop toggle (was combined with Overview)
> ...

**Verdict: PLAN_EVAL is right.** The PRD says "rebuild must preserve unless intentionally changed." The plan reorders: it inserts Rating (item 3) and Status toolbar (item 4) before Tags and Overview, and separates Scoop from Overview. The self-evaluator claimed the plan follows the hierarchy, but it demonstrably doesn't — Rating and Status are promoted ahead of Tags and Overview.

---

## Disagreement 8: PRD-064 — Page not overwhelming

**Severity:** important

| Evaluator | Score | Justification |
|---|---|---|
| PLAN_EVAL | **partial** | "The plan places actions early, but it does not specify any approach for keeping the dense page from feeling visually overwhelming." |
| PLAN_EVAL_SELF | **full** | "Clusters status/rating/scoop/concepts in items 1-11; long-tail info in items 12-15" |

**Original doc** (`detail_page_experience.md` 4):
> The page should feel **powerful but not overwhelming**:
> - primary actions are clustered early (status, rating, scoop, concepts),
> - long-tail info is down-page and full-bleed to reduce clutter.

**Plan says** (6.5): Lists 15 sections in order with items 12-15 being cast/crew/seasons/budget.

**Verdict: PLAN_EVAL_SELF is right.** The plan does cluster primary actions early and pushes long-tail info down the page — this matches the PRD's guidance. The PRD requirement is about section ordering and clustering, which the plan achieves. Demanding specific visual de-cluttering techniques goes beyond what the PRD asks for.

---

## Disagreement 9: PRD-066 — Confident, direct Ask responses

**Severity:** important

| Evaluator | Score | Justification |
|---|---|---|
| PLAN_EVAL | **partial** | "Spoiler safety and taste awareness are planned, but the prompt contract does not explicitly require the answer-first, confident response pattern from the quality bar." |
| PLAN_EVAL_SELF | **full** | "Spoiler-safe default, opinionated honesty; references discovery quality bar contracts" |

**Original doc** (`discovery_quality_bar.md` 2.2):
> - **Direct answer within first 3-5 lines.**
> - Bulleted lists for multi-recs.
> - **Confident picks.**

**Plan says** (5.2 ask.ts): "Establishes the persona (fun, chatty TV/movie nerd friend), spoiler-safe default, opinionated honesty, library awareness."

**Verdict: PLAN_EVAL is right.** The quality bar has concrete behavioral rules: "direct answer within first 3-5 lines" and "confident picks." The plan says "opinionated honesty" which is adjacent but not the same as the answer-first pacing requirement. An implementer could build an Ask surface that's opinionated but buries the answer under preamble, violating the quality bar.

---

## Disagreement 10: PRD-074 — Redirect Ask to TV/movie domain

**Severity:** important

| Evaluator | Score | Justification |
|---|---|---|
| PLAN_EVAL | **partial** | "The plan references shared prompting docs, but it never explicitly calls out redirecting off-domain Ask prompts back to TV and movies." |
| PLAN_EVAL_SELF | **full** | "Constructs the system prompt according to the contracts in ai_prompting_context.md which specifies domain redirection" |

**Original doc** (`ai_prompting_context.md` 1):
> All AI surfaces must: **Stay within TV/movies (redirect back if asked to leave that domain).**

**Plan says** (5.2): "Each AI surface has a dedicated prompt builder that constructs the system prompt and user messages according to the contracts in `ai_prompting_context.md`"

**Verdict: PLAN_EVAL is right.** The plan delegates to the spec by reference ("according to the contracts in ai_prompting_context.md") rather than incorporating the domain-redirect rule into the plan itself. A plan should translate spec requirements into implementation guidance. The self-evaluator gave credit for a pointer to a document, not for planning the behavior.

---

## Disagreement 11: PRD-075 — Concepts are taste ingredients, not genres

**Severity:** important

| Evaluator | Score | Justification |
|---|---|---|
| PLAN_EVAL | **partial** | "The concept plan emphasizes evocative outputs, but it does not explicitly frame concepts as ingredients rather than genre labels." |
| PLAN_EVAL_SELF | **full** | "Evocative, no plot, no generics. Focus axes: Structure, tone/vibe, emotional palette, craft, genre-flavor" |

**Original doc** (`concept_system.md` 1):
> A **concept** is a *short ingredient* that captures the **core feeling** of a show: its vibe, structure, emotional temperature, or signature style. Concepts are **not genres or plot points.** They are the **taste DNA** that lets the app find "shows like this in the way I actually mean."

**Plan says** (5.2 concepts.ts): "Bullet list only, 1-3 words each, evocative, no plot, no generics. Focus axes: Structure, tone/vibe, emotional palette, relationship dynamics, craft, genre-flavor."

**Verdict: PLAN_EVAL_SELF is right.** The plan says "no generics" and lists taste-oriented axes (tone/vibe, emotional palette, craft) — this effectively captures the "ingredients not genres" framing. The plan's rules would produce ingredient-style concepts. Requiring the exact word "ingredient" is pedantic when the behavioral constraint is captured.

---

## Disagreement 12: PRD-084 — Surprising but defensible recommendations

**Severity:** important

| Evaluator | Score | Justification |
|---|---|---|
| PLAN_EVAL | **partial** | "The plan reviews taste alignment and surprise late, but it does not bake surprising-but-defensible recommendation behavior into the recommendation contract itself." |
| PLAN_EVAL_SELF | **full** | "Recommendations include library context; Phase 6 task 6 reviews against discovery quality bar including surprise" |

**Original doc** (`discovery_quality_bar.md` 1.3):
> Pass if: at least 1-2 recs are **pleasantly unexpected but defensible**.
> Fail smells: all safe obvious picks, surprise that breaks the vibe.

**Plan says** (5.2 recommendations.ts): "List of shows with per-show reasons explicitly referencing concepts." (Phase 6 Task 6): "Review all AI surfaces against the discovery quality bar (voice adherence, taste alignment, real-show integrity, specificity, surprise)."

**Verdict: PLAN_EVAL is right.** The recommendation prompt module doesn't include any instruction to produce surprising results — it only requires reasons referencing concepts. The "surprise" check only appears as a late-stage review in Phase 6, not as a behavioral rule in the recommendation contract. If the prompt doesn't ask for surprise, the Phase 6 review will just discover the problem after the fact.

---

## Disagreement 13: PRD-089 — Ask should be brisk and dialogue-like

**Severity:** important

| Evaluator | Score | Justification |
|---|---|---|
| PLAN_EVAL | **partial** | "The Ask persona is defined, but the plan does not explicitly constrain default responses to brisk, dialogue-like length and rhythm." |
| PLAN_EVAL_SELF | **full** | "Ask.ts describes persona; references ai_voice_personality.md contracts for tone" |

**Original doc** (`ai_voice_personality.md` 4.2):
> Behavior: responds like a friend in **dialogue (not an essay)**, picks favorites confidently, adapts depth to the user's question.
> Feel: **low-friction, fast, and fun.**
> Length target: **1-3 tight paragraphs**, then a list if recommending multiple titles.

**Plan says** (5.2 ask.ts): "Establishes the persona (fun, chatty TV/movie nerd friend), spoiler-safe default, opinionated honesty, library awareness."

**Verdict: PLAN_EVAL is right.** The spec gives concrete behavioral constraints: "dialogue not essay," "1-3 tight paragraphs," "low-friction, fast." The plan captures the persona but not the pacing/length rules. An implementer could build a chatty, opinionated Ask that produces essay-length responses, violating the spec.

---

## Disagreement 14: PRD-086 — Enforce shared AI guardrails across all surfaces

**Severity:** critical

| Evaluator | Score | Justification |
|---|---|---|
| PLAN_EVAL | **full** | "5.2 AI Prompt Modules; 9. Risk Mitigation" |
| PLAN_EVAL_SELF | **partial** | "Plan delegates guardrails to per-surface prompt modules referencing the spec; does not enumerate the shared guardrails or describe a unified enforcement mechanism" |

**Original doc** (`ai_prompting_context.md` 1):
> All AI surfaces must:
> - Stay within TV/movies (redirect back if asked to leave that domain).
> - Be spoiler-safe by default unless the user explicitly requests spoilers.
> - Be opinionated and honest.
> - Prefer specific, vibe/structure/craft-based reasoning over generic genre summaries.
> - AI outputs should be actionable: recommended titles should resolve to real catalog items.

**Plan says** (5.2): "Each AI surface has a dedicated prompt builder that constructs the system prompt and user messages according to the contracts in `ai_prompting_context.md` and the voice spec in `ai_voice_personality.md`."

**Verdict: PLAN_EVAL_SELF is right.** The plan delegates guardrails to individual prompt modules via a doc reference, but never enumerates the shared rules as a cross-cutting contract. An implementer building Scoop could omit domain redirection while the Ask implementer includes it. This is a real gap — and importantly it's `critical` severity. The external evaluator missed this.

---

## Summary Scorecard

| PRD-ID | Severity | PLAN_EVAL | PLAN_EVAL_SELF | Verdict |
|---|---|---|---|---|
| PRD-013 | important | partial | full | **PLAN_EVAL correct** |
| PRD-017 | important | partial | full | **PLAN_EVAL_SELF correct** |
| PRD-030 | important | partial | full | **PLAN_EVAL correct** |
| PRD-033 | important | partial | full | **PLAN_EVAL correct** |
| PRD-034 | critical | partial | full | **PLAN_EVAL correct** |
| PRD-050 | important | partial | full | **PLAN_EVAL_SELF correct** |
| PRD-051 | important | partial | full | **PLAN_EVAL correct** |
| PRD-064 | important | partial | full | **PLAN_EVAL_SELF correct** |
| PRD-066 | important | partial | full | **PLAN_EVAL correct** |
| PRD-074 | important | partial | full | **PLAN_EVAL correct** |
| PRD-075 | important | partial | full | **PLAN_EVAL_SELF correct** |
| PRD-084 | important | partial | full | **PLAN_EVAL correct** |
| PRD-086 | critical | full | partial | **PLAN_EVAL_SELF correct** |
| PRD-089 | important | partial | full | **PLAN_EVAL correct** |

**Results: PLAN_EVAL was right on 9/14 disagreements. PLAN_EVAL_SELF was right on 5/14.**

### Corrected Score

Applying the verdicts above to produce a "true" score:

```
Full:    85 (agreed) + 5 (SELF correct) = 90 adjusted-full from EVAL's 81
         85 (agreed) + 9 (EVAL correct) = 94 adjusted-full — wait, let me recount.
```

Both agreed on 85 full. Of the 14 disputed:
- 9 should be partial (EVAL was right)
- 5 should be full (SELF was right)

Also, PRD-086 (agreed-full by EVAL but partial per SELF, and SELF was right) flips one of EVAL's "full" to partial.

Corrected partials: 9 (EVAL correct) + 1 (PRD-086, SELF correct that it's partial) = **10 partial**
Corrected fulls: 99 - 10 = **89 full**

```
Corrected overall = (89 x 1.0 + 10 x 0.5) / 99 x 100 = 95.0 / 99 x 100 = 94.9 / 99 = 95.0%
```

**Corrected score: ~95.0%** — between the two evaluations, closer to the self-eval but meaningfully lower.

### Which Evaluation Is More Trustworthy Overall?

**PLAN_EVAL (external) is the more reliable evaluator.** It was right on 9 of 14 disagreements, and its errors were mostly over-strictness on items where the plan's design implicitly satisfies the requirement (no Docker, no AI in Search, concepts-as-ingredients, page clustering). Its core strength is requiring explicit specification rather than giving credit for references and implications.

**PLAN_EVAL_SELF** suffered from systematic self-evaluation bias: it gave itself credit for *intent* rather than *what was written*. However, it caught the PRD-086 shared-guardrails gap that the external evaluator missed — a genuine critical-tier finding.

The ideal evaluation would combine the external evaluator's strictness with the self-evaluator's architectural self-awareness.
