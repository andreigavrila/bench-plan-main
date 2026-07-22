#!/usr/bin/env python3
"""Build a deterministic integrity report and a fixed-anchor coverage matrix."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


CATALOG_RELATIVE = Path("template/evaluator/requirements_catalog_v1.md")
REQUIRED_HEADINGS = (
    "### 1. Requirements Extraction",
    "### 2. Coverage Table",
    "### 3. Coverage Scores",
    "### 4. Top Gaps",
    "### 5. Coverage Narrative",
)
VALID_COVERAGE = {"full", "partial", "missing"}
EXPECTED_SEVERITIES = {"critical": 30, "important": 67, "detail": 2}
CATALOG_ROW = re.compile(
    r"^-\s+(PRD-\d{3})\s+\|\s+`(critical|important|detail)`\s+\|\s+([^|]+?)\s+\|",
    re.MULTILINE | re.IGNORECASE,
)
EVAL_ROW = re.compile(
    r"^\|\s*(PRD-\d{3})\s*\|\s*([^|]+?)\s*\|\s*"
    r"(critical|important|detail)\s*\|\s*(full|partial|missing)\s*\|",
    re.MULTILINE | re.IGNORECASE,
)
OVERALL_SCORE = re.compile(r"Overall:\s*`*\s*([0-9]+(?:\.[0-9]+)?)%", re.IGNORECASE)
CONTAMINATION_PATTERNS = (
    ("evaluator catalog path", re.compile(r"evaluator[\\/]requirements_catalog_v1\.(?:md|json)", re.I)),
    ("canonical evaluator catalog", re.compile(r"Canonical Requirements Catalog", re.I)),
    ("evaluator-only material", re.compile(r"evaluator[- ]only", re.I)),
)


@dataclass(frozen=True)
class CatalogEntry:
    requirement: str
    severity: str
    label: str


@dataclass(frozen=True)
class EvalEntry:
    requirement: str
    label: str
    severity: str
    coverage: str


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig")


def find_repo_root(start: Path) -> Path:
    current = start.resolve()
    if current.is_file():
        current = current.parent
    for candidate in (current, *current.parents):
        if (candidate / CATALOG_RELATIVE).is_file():
            return candidate
    raise FileNotFoundError(
        f"Could not find {CATALOG_RELATIVE.as_posix()} from {start}."
    )


def resolve_results_path(raw_target: Path, repo_root: Path) -> Path:
    target = raw_target if raw_target.is_absolute() else repo_root / raw_target
    target = target.resolve()
    if target.is_file():
        if target.name.lower() != "plan_eval.md":
            raise FileNotFoundError(f"Target file is not PLAN_EVAL.md: {target}")
        target = target.parent
    elif (target / "results" / "PLAN_EVAL.md").is_file():
        target = target / "results"
    if not (target / "PLAN_EVAL.md").is_file():
        raise FileNotFoundError(f"Missing PLAN_EVAL.md under target: {target}")
    if not (target / "PLAN.md").is_file():
        raise FileNotFoundError(f"Missing PLAN.md under target: {target}")
    return target


def parse_catalog(path: Path) -> tuple[list[CatalogEntry], list[str]]:
    matches = [
        CatalogEntry(req.upper(), severity.lower(), label.strip())
        for req, severity, label in CATALOG_ROW.findall(read_text(path))
    ]
    ids = [entry.requirement for entry in matches]
    duplicates = sorted(req for req, count in Counter(ids).items() if count > 1)
    return matches, duplicates


def parse_evaluation(path: Path) -> tuple[dict[str, EvalEntry], list[str], str]:
    content = read_text(path)
    parsed = [
        EvalEntry(req.upper(), label.strip(), severity.lower(), coverage.lower())
        for req, label, severity, coverage in EVAL_ROW.findall(content)
    ]
    duplicates = sorted(
        req for req, count in Counter(entry.requirement for entry in parsed).items() if count > 1
    )
    rows: dict[str, EvalEntry] = {}
    for entry in parsed:
        rows.setdefault(entry.requirement, entry)
    return rows, duplicates, content


def score(rows: dict[str, EvalEntry], catalog: list[CatalogEntry]) -> float:
    points = 0.0
    for item in catalog:
        coverage = rows.get(item.requirement)
        if coverage is None:
            continue
        points += {"full": 1.0, "partial": 0.5, "missing": 0.0}[coverage.coverage]
    return round(points / len(catalog) * 100, 1)


def score_for_severity(
    rows: dict[str, EvalEntry], catalog: list[CatalogEntry], severity: str
) -> float:
    selected = [item for item in catalog if item.severity == severity]
    points = 0.0
    for item in selected:
        coverage = rows.get(item.requirement)
        if coverage is not None:
            points += {"full": 1.0, "partial": 0.5, "missing": 0.0}[coverage.coverage]
    return round(points / len(selected) * 100, 1)


def apply_overrides(
    rows: dict[str, EvalEntry], overrides: dict[str, str]
) -> dict[str, EvalEntry]:
    adjusted = dict(rows)
    for requirement, coverage in overrides.items():
        requirement = requirement.upper()
        coverage = coverage.lower()
        if requirement not in adjusted:
            raise ValueError(f"Override references absent row {requirement}.")
        if coverage not in VALID_COVERAGE:
            raise ValueError(f"Invalid override coverage {coverage!r} for {requirement}.")
        old = adjusted[requirement]
        adjusted[requirement] = EvalEntry(old.requirement, old.label, old.severity, coverage)
    return adjusted


def integrity_warnings(
    rows: dict[str, EvalEntry], duplicates: list[str], catalog: list[CatalogEntry]
) -> list[str]:
    expected = {entry.requirement for entry in catalog}
    actual = set(rows)
    catalog_by_id = {entry.requirement: entry for entry in catalog}
    warnings: list[str] = []
    if duplicates:
        warnings.append("duplicate rows: " + ", ".join(duplicates))
    if expected - actual:
        warnings.append("missing rows: " + ", ".join(sorted(expected - actual)))
    if actual - expected:
        warnings.append("extra rows: " + ", ".join(sorted(actual - expected)))
    mismatches = [
        req
        for req in sorted(expected & actual)
        if rows[req].severity != catalog_by_id[req].severity
    ]
    if mismatches:
        warnings.append("severity mismatches: " + ", ".join(mismatches))
    return warnings


def published_score(content: str) -> float | None:
    match = OVERALL_SCORE.search(content)
    return float(match.group(1)) if match else None


def relative_display(path: Path, repo_root: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return str(path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, type=Path, help="Result folder, model folder, or PLAN_EVAL.md")
    parser.add_argument("--repo-root", type=Path, help="Repository root; auto-detected when omitted")
    parser.add_argument("--anchors", type=Path, help="Anchor manifest; defaults to the skill reference")
    parser.add_argument("--summary-only", action="store_true", help="Omit the 99-row comparison matrix")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    script_dir = Path(__file__).resolve().parent
    try:
        root_seed = args.repo_root or Path.cwd()
        repo_root = find_repo_root(root_seed)
        target_results = resolve_results_path(args.target, repo_root)
        anchor_manifest = args.anchors or script_dir.parent / "references" / "anchors.json"
        if not anchor_manifest.is_absolute():
            anchor_manifest = repo_root / anchor_manifest

        catalog, catalog_duplicates = parse_catalog(repo_root / CATALOG_RELATIVE)
        if catalog_duplicates:
            raise ValueError("Catalog has duplicate IDs: " + ", ".join(catalog_duplicates))
        if len(catalog) != 99:
            raise ValueError(f"Catalog has {len(catalog)} parsed rows; expected 99.")
        severity_counts = Counter(item.severity for item in catalog)
        if dict(severity_counts) != EXPECTED_SEVERITIES:
            raise ValueError(
                f"Catalog severities are {dict(severity_counts)}; expected {EXPECTED_SEVERITIES}."
            )

        target_rows, target_duplicates, target_eval_text = parse_evaluation(
            target_results / "PLAN_EVAL.md"
        )
        target_plan_text = read_text(target_results / "PLAN.md")
        manifest = json.loads(read_text(anchor_manifest))
        target_id = target_results.parent.name
        anchors: list[tuple[dict[str, object], dict[str, EvalEntry]]] = []
        missing_anchors: list[str] = []
        anchor_warnings: list[str] = []

        for anchor in manifest.get("anchors", []):
            anchor_id = str(anchor["id"])
            if anchor_id == target_id:
                continue
            anchor_results = repo_root / str(anchor["results_path"])
            if not (anchor_results / "PLAN_EVAL.md").is_file():
                missing_anchors.append(anchor_id)
                continue
            anchor_rows, duplicates, _ = parse_evaluation(anchor_results / "PLAN_EVAL.md")
            warnings = integrity_warnings(anchor_rows, duplicates, catalog)
            if warnings:
                anchor_warnings.extend(f"{anchor_id}: {warning}" for warning in warnings)
            adjusted = apply_overrides(anchor_rows, dict(anchor.get("coverage_overrides", {})))
            calculated = score(adjusted, catalog)
            reviewed = float(anchor["reviewed_score"])
            if calculated != reviewed:
                anchor_warnings.append(
                    f"{anchor_id}: manifest score {reviewed:.1f}% != adjusted rows {calculated:.1f}%"
                )
            anchors.append((anchor, adjusted))

        warnings = integrity_warnings(target_rows, target_duplicates, catalog)
        headings_missing = [heading for heading in REQUIRED_HEADINGS if heading not in target_eval_text]
        contamination = [
            label for label, pattern in CONTAMINATION_PATTERNS if pattern.search(target_plan_text)
        ]
        published = published_score(target_eval_text)
        recalculated = score(target_rows, catalog)
        counts = Counter(entry.coverage for entry in target_rows.values())

        print("# Grounding inventory")
        print()
        print(f"- Target: `{relative_display(target_results, repo_root)}`")
        print(f"- Parsed target rows: {len(target_rows)} / {len(catalog)}")
        print(f"- Published overall: {published:.1f}%" if published is not None else "- Published overall: not found")
        print(f"- Recomputed from published rows: {recalculated:.1f}%")
        print(
            "- Recomputed severity scores: "
            + ", ".join(
                f"{severity} {score_for_severity(target_rows, catalog, severity):.1f}%"
                for severity in ("critical", "important", "detail")
            )
        )
        print(f"- Available fixed anchors after excluding target: {len(anchors)}")
        print()
        print("## Integrity checks")
        print()
        print("- Row integrity: " + ("OK" if not warnings else "; ".join(warnings)))
        print("- Required headings: " + ("OK" if not headings_missing else "missing " + ", ".join(headings_missing)))
        print("- Explicit contamination indicators: " + (", ".join(contamination) if contamination else "none detected"))
        print("- Missing anchors: " + (", ".join(missing_anchors) if missing_anchors else "none"))
        print("- Anchor integrity: " + ("OK" if not anchor_warnings else "; ".join(anchor_warnings)))
        print()
        print("## Published coverage counts")
        print()
        print(f"- Full: {counts['full']}")
        print(f"- Partial: {counts['partial']}")
        print(f"- Missing: {counts['missing']}")

        if not args.summary_only:
            print()
            print("## Fixed-anchor comparison matrix")
            print()
            headers = ["Requirement", "Severity", "Target"] + [str(anchor[0]["id"]) for anchor in anchors]
            print("| " + " | ".join(headers) + " |")
            print("| " + " | ".join("---" for _ in headers) + " |")
            for item in catalog:
                target_coverage = target_rows.get(item.requirement)
                values = [
                    item.requirement,
                    item.severity,
                    target_coverage.coverage if target_coverage else "absent",
                ]
                values.extend(
                    rows[item.requirement].coverage if item.requirement in rows else "absent"
                    for _, rows in anchors
                )
                print("| " + " | ".join(values) + " |")
            print()
            print("## Anchor roles")
            print()
            for anchor, _ in anchors:
                print(
                    f"- `{anchor['id']}` ({float(anchor['reviewed_score']):.1f}% reviewed): "
                    f"{anchor['role']}"
                )

        if len(anchors) < 3:
            print("\nERROR: Fewer than three fixed anchors are available.", file=sys.stderr)
            return 1
        return 0
    except (FileNotFoundError, ValueError, KeyError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
