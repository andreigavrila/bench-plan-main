# Grounding Review Protocol

## Coverage standard

- **Full:** The plan explicitly and completely addresses the requirement with concrete mechanisms, and those mechanisms are semantically capable of satisfying it.
- **Partial:** The plan implies the behavior, makes a mandatory behavior optional, names only a component, supplies an incomplete contract, or proposes a mechanism that cannot fully deliver the requirement.
- **Missing:** No meaningful plan coverage exists.
- Judge plan coverage, not implementation. A plan need not contain finished code, but it must make the intended behavior and delivery mechanism clear enough to implement.

## Strictness rules

- Treat `may`, `where practical`, `if supported`, and similar discretionary language as partial when the source requirement is mandatory.
- Do not infer coverage from PRD IDs, traceability tables, directory names, checklists, test names, or claims that all requirements are covered.
- Generic promises such as "guardrails", "synchronization", or "safe settings" do not satisfy a precise requirement without the relevant behavior or contract.
- Combine evidence across plan sections when the combined mechanism is concrete and internally consistent.
- Downgrade contradictions that undermine the stated mechanism. Examples include later treating a supposedly trusted namespace as untrusted, or exporting settings that may contain secrets after promising secret exclusion.
- Do not penalize open implementation detail when the plan already fixes the required behavior, ownership, and acceptance condition.
- Keep architecture or quality concerns that are not canonical requirements outside the 99-row coverage score.

## Cross-anchor calibration

- Use the fixed anchor manifest; do not choose anchors based on which ones support a desired conclusion.
- When the target is an anchor, exclude it and use the remaining four.
- Compare disputed rows to raw plan evidence in at least one stronger and one weaker relevant anchor when available.
- An anchor label is a calibration aid, not proof. Apply this protocol to the anchor evidence as well as to the target.
- Treat manifest overrides as the reviewed anchor baseline. They record prior cross-review corrections that are not necessarily written back into `PLAN_EVAL.md`.
- If an anchor appears wrong under this protocol, disclose the conflict instead of bending the target judgment to match it.

## Contamination

- **High-confidence contamination:** The plan explicitly references evaluator-only paths or artifacts, such as `evaluator/requirements_catalog_v1.md`, the canonical evaluator catalog, or evaluator-only materials.
- **Medium-confidence contamination indicator:** The plan reproduces evaluator IDs, exact evaluator ordering, or evaluator-specific phrasing without an explicit path. Report this as an indicator, not proof.
- Using the Step 2 evaluation template during evaluation is expected and is not plan contamination.
- Report contamination separately from coverage unless the benchmark rules prescribe a score penalty.

## Score calculation

Use the benchmark formula for each severity and overall:

`(full + 0.5 * partial) / total * 100`

Round displayed scores to one decimal place. Preserve the row labels used to calculate the score.

## Required integrity checks

- Exactly 99 unique catalog requirements are evaluated.
- Catalog severity totals are 30 critical, 67 important, and 2 detail.
- Coverage values are only `full`, `partial`, or `missing`.
- Evaluation severities match the catalog.
- Published count tables and scores agree with the row table.
- All required Step 2 output sections exist.
- Evidence quotes or references are traceable to the plan and are not fabricated.
