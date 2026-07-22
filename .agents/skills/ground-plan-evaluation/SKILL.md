---
name: ground-plan-evaluation
description: Cross-review an existing PLAN_EVAL.md against its PLAN.md, the canonical 99-requirement benchmark catalog, and a fixed set of reviewed benchmark anchors. Use when a user doubts whether a plan evaluation is fair, biased, too lenient, too strict, internally inconsistent, or contaminated, especially for result folders in this planning benchmark repository.
---

# Ground Plan Evaluation

Audit one completed plan evaluation from a fresh context and calibrate it against the same reviewed anchors on every run. Treat the audit as read-only unless the user explicitly asks to update files afterward.

## Inputs

Accept any of these target forms:

- `<model>/results`
- `<model>/results/PLAN_EVAL.md`
- `<model>` when it contains `results/PLAN.md` and `results/PLAN_EVAL.md`

Resolve the repository root containing `template/evaluator/requirements_catalog_v1.md`. Stop and report the missing input if the target, catalog, or requirement documents cannot be found.

## Fixed anchors

Read [references/anchors.json](references/anchors.json). Use this fixed pool and its reviewed overrides every time so separate context windows remain comparable.

- Exclude the target itself and compare against the other four anchors.
- Never substitute a different result without explicit user approval.
- Require at least three available anchors and report any missing anchor.
- Never use Gemini 3.5 Flash as an anchor because its plan is contaminated by evaluator-only material.

## Workflow

1. Resolve the target and repository root.
2. Run `scripts/compare_evaluations.py` to inventory rows, arithmetic, headings, contamination indicators, and the fixed comparison matrix.
3. Read `template/2-EVALUATE_PLAN.md` completely.
4. Read `template/evaluator/requirements_catalog_v1.md` completely.
5. Read the canonical requirement sources in semantic order: product requirements, infrastructure requirements, then every supporting requirements document recursively.
6. Read the complete target `PLAN.md` and `PLAN_EVAL.md`; do not sample them.
7. Re-adjudicate all 99 catalog requirements against the target plan.
8. Read every selected anchor evaluation. For each disputed or borderline target row, inspect the corresponding raw anchor-plan evidence rather than relying only on the anchor label.
9. Apply [references/review-protocol.md](references/review-protocol.md) consistently to target and anchors.
10. Recompute severity scores and overall score from corrected coverage labels.
11. Report important plan-level architecture gaps outside the 99-row denominator separately.

## Required judgments

For every requirement classify the published evaluation as `fair`, `too lenient`, or `too strict`. Full credit requires explicit, concrete, semantically correct coverage. Do not award coverage from requirement IDs, directory names, generic checklists, or test names alone. Treat evaluator contamination as a separate integrity issue rather than silently folding it into the score.

## Required output

Return a self-contained review with:

1. Overall verdict on fairness and consistency.
2. Published score, recalibrated score, and delta.
3. Every corrected row, with target evidence and a fixed-anchor comparison.
4. Any rows judged too strict.
5. Recurring evaluation patterns or inconsistencies.
6. Major architecture gaps outside the denominator.
7. Contamination and format/integrity findings.
8. Confidence level and any unresolved ambiguity.

Do not modify the target evaluation, `README.md`, or score files unless the user separately authorizes those changes.

## Script execution

The helper uses only the Python standard library. Prefer the available Python launcher; on this Windows workspace use:

```powershell
uv run --python 3.12 python .agents/skills/ground-plan-evaluation/scripts/compare_evaluations.py --target <target>
```

Use `--summary-only` for a compact integrity check. The helper is deterministic bookkeeping, not a substitute for the semantic audit.
