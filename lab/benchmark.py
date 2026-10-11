"""Reproducible precision/recall experiment using only synthetic fixtures.

A high score here is NOT evidence about unseen production code or LLM quality.
"""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

from .inspector import inspect_repository

CASES = (
    ("silent_except", "def f():\n    try:\n        return 1\n    except Exception:\n        pass\n", {"silent_exception"}),
    ("unsafe_eval", "def f():\n    return eval('2+2')\n", {"dynamic_execution"}),
    ("syntax_broken", "def broken(:\n", {"syntax_error"}),
    ("safe_raise", "def f():\n    try:\n        return 1\n    except Exception:\n        raise\n", set()),
    ("safe_fallback", "def f():\n    try:\n        return 1\n    except Exception:\n        return None\n", set()),
    ("safe_quoted_eval", "def f():\n    return 'eval(2)'\n", set()),
    ("dynamic_and_silent", "def f():\n    try:\n        return eval('1')\n    except ValueError:\n        pass\n", {"dynamic_execution", "silent_exception"}),
    ("safe_simple", "def f():\n    return True\n", set()),
)


def run_scanner_benchmark() -> dict:
    tp = fp = fn = 0
    case_results = []
    with tempfile.TemporaryDirectory(prefix="lab-bench-") as directory:
        root = Path(directory)
        for name, body, expected in CASES:
            case = root / name
            case.mkdir()
            (case / "agent.py").write_text(body, encoding="utf-8")
            (case / "tests").mkdir()
            (case / "tests" / "test_stub.py").write_text("def test_ok(): assert True\n")
            inspection = inspect_repository(case)
            observed = {x["rule"] for x in inspection["findings"]}
            tp += len(expected & observed)
            fp += len(observed - expected)
            fn += len(expected - observed)
            case_results.append({
                "fixture": name, "expected": sorted(expected),
                "observed": sorted(observed), "passed": expected == observed,
            })
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "scope": "bundled_synthetic_fixtures_only",
        "case_count": len(case_results),
        "passed_cases": sum(case["passed"] for case in case_results),
        "true_positive": tp, "false_positive": fp, "false_negative": fn,
        "precision": round(precision, 4), "recall": round(recall, 4),
        "f1": round(f1, 4), "fixtures": case_results,
        "not_measured": ["production_generalization", "LLM_reasoning_quality", "automatic_real_repository_code_fixes"],
    }


def main() -> int:
    result = run_scanner_benchmark()
    print(json.dumps(result, indent=2))
    return 0 if result["passed_cases"] == result["case_count"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
