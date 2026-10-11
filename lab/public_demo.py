"""Reproducible public tour of bounded tests already implemented in the lab.

This command runs bundled synthetic fixtures and compares a reconstructed
historical real-repository defect with the current verified function.
It neither invokes an LLM nor runs untrusted external repository code.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from .autorepair import evaluate_repair_demo
from .benchmark import run_scanner_benchmark
from .real_repo_repair import TARGET, _check_source

SAFE_LINE = "    match = re.match(r'^https://github\\.com/([^/]+)/([^/]+)', value)"
HISTORICAL_LINE = '    match = re.search(r"github\\.com/([^/]+)/([^/]+)", value)'
EVIDENCE_PR = "https://github.com/AMMARICA1791/ai-research-agents/pull/17"


def collect_evidence(root: Path) -> dict:
    """Recheck three known experiments, fail closed if source changes."""
    root = root.resolve(strict=True)
    source = (root / TARGET).read_text(encoding="utf-8")
    if source.count(SAFE_LINE) != 1 or HISTORICAL_LINE in source:
        raise ValueError("Cannot confirm the exact previously-reviewed URL repair")
    historical = source.replace(SAFE_LINE, HISTORICAL_LINE, 1)
    historical_passed = _check_source(historical)
    current_passed = _check_source(source)
    if historical_passed or not current_passed:
        raise RuntimeError("Security regression could not be reproduced")

    benchmark = run_scanner_benchmark()
    if benchmark["case_count"] != 8 or benchmark["passed_cases"] != 8:
        raise RuntimeError("Bundled synthetic scanner benchmark has regressed")

    synthetic = evaluate_repair_demo()
    if (synthetic["status"] != "validated_synthetic_only"
            or synthetic["baseline"]["passed"]
            or not synthetic["repaired"]["passed"]):
        raise RuntimeError("Bundled synthetic red/green repair has regressed")

    return {
        "schema_version": 1,
        "name": "AI Research Agents — Public Proof Tour",
        "status": "verified_bounded_experiments",
        "no_paid_model_api_required": True,
        "model_inference_this_run": False,
        "external_user_code_executed": False,
        "repository_files_changed": False,
        "experiments": {
            "static_scanner": {
                "origin": "bundled_synthetic_cases",
                "tested_cases": benchmark["case_count"],
                "cases_passed": benchmark["passed_cases"],
                "precision_on_bundled_cases_only": benchmark["precision"],
                "recall_on_bundled_cases_only": benchmark["recall"],
            },
            "synthetic_repair": {
                "origin": "bundled_synthetic_fixture",
                "generator": synthetic["producer"],
                "test_before": "FAIL",
                "test_after": "PASS",
                "model_authored": False,
            },
            "real_repository_regression": {
                "origin": "historical GitHub URL parser from this repository",
                "target": TARGET.as_posix(),
                "current_sha256": hashlib.sha256(source.encode("utf-8")).hexdigest(),
                "reconstructed_historical_vulnerability": True,
                "test_before": "FAIL",
                "test_after": "PASS",
                "original_patch_authored_by_model": "Qwen2.5-Coder 1.5B",
                "model_run_replayed": False,
                "historical_pull_request": EVIDENCE_PR,
            },
        },
        "not_proven": [
            "automatic discovery of novel bugs",
            "model generation during this demo",
            "accuracy on previously unseen real-world repositories",
            "safe execution of untrusted external projects",
            "autonomous merging or deployment",
        ],
    }


def markdown_summary(evidence: dict) -> str:
    scanner = evidence["experiments"]["static_scanner"]
    url = evidence["experiments"]["real_repository_regression"]
    return (
        "# AI Research Agents — One-click evidence tour\n\n"
        "**This run passed three bounded demonstrations; it is not a claim "
        "of general autonomous engineering.**\n\n"
        "| Check | Origin | Result |\n"
        "|---|---|---|\n"
        f"| Static Python scanner | {scanner['tested_cases']} synthetic cases | "
        f"{scanner['cases_passed']} / {scanner['tested_cases']} passed |\n"
        "| Deterministic repair proposal | Trusted synthetic fixture | "
        "Test FAIL before to PASS after |\n"
        "| Previously model-authored real-repo repair | Historical vs. "
        "current GitHub URL parser | Test FAIL before to PASS after |\n\n"
        "## What you can verify\n\n"
        f"- [Inspect model-authored code and human merge (PR #17)]({url['historical_pull_request']}).\n"
        "- Download the JSON report artifact from this GitHub Actions run.\n"
        "- Inspect lab/public_demo.py and rerun python -m lab.public_demo "
        "on Python 3.11+ (no paid model API key).\n"
        "- This rerun tests the actual merged fix against a reconstructed "
        "historical vulnerable baseline, but does not rerun Qwen.\n\n"
        "## Boundaries\n\n"
        "This workflow evaluates repository-owned test fixtures only, runs "
        "no outside repositories, changes no project files, and does not "
        "create pull requests. The synthetic benchmark's observed 100% "
        "precision and recall applies only to its eight artificial cases. "
        "Neither the repaired URL parser nor these experiments demonstrate "
        "generic code-repair or complete URL security.\n"
    )


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Reproduce the public research evidence tour")
    parser.add_argument("--repo", default=".", help="Path to this repository")
    parser.add_argument("--out", default="results/public-demo", help="Directory for reports")
    args = parser.parse_args(argv)
    evidence = collect_evidence(Path(args.repo))
    output = Path(args.out)
    output.mkdir(parents=True, exist_ok=True)
    (output / "evidence.json").write_text(
        json.dumps(evidence, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (output / "SUMMARY.md").write_text(markdown_summary(evidence), encoding="utf-8")
    print(markdown_summary(evidence))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
