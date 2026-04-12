## Planning Benchmark

This repo benchmarks how well coding agents plan against a product spec. The default collection workflow has two actions. Run each in a fresh context.

### Actions

1. **Generate a plan** — Read and follow `1-START_HERE.md`. Produces `results/PLAN.md`.
2. **Evaluate a plan** — Read and follow `2-EVALUATE_PLAN.md`. Produces both `results/PLAN_EVAL.md`.

### Benchmark Management

Use `/benchmark new` to create a new benchmark worktree. It will interview you for model, tool, effort, and variant, then create the worktree and open Cursor.

Worktrees live in `~/code/shows_tests/` and follow BEM-style naming: `{model}__{tool}[__{effort}][__{variant}]` — all snake_case, no dashes or dots.

### Development Guidelines

If a task involves planning or reasoning about code architecture, read `INSTRUCTIONS.md` for coding standards and architectural patterns.
