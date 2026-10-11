"""Bounded fail-closed repair proposal with reproducible red/green evidence.

Deterministic AST-guided engineering, NOT LLM-written code. Never edits the
user's repository, pushes to main, or executes code from arbitrary repositories.
"""
from __future__ import annotations

import ast
import difflib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

FIXTURE_PATH = "synthetic_silent_exception.py"
FIXTURE = (
    "def divide(value):\n"
    "    try:\n"
    "        return 10 / value\n"
    "    except ZeroDivisionError:\n"
    "        pass\n"
)
DRIVER = (
    "import importlib.util, sys\n"
    "spec = importlib.util.spec_from_file_location('synthetic_candidate', sys.argv[1])\n"
    "module = importlib.util.module_from_spec(spec)\n"
    "spec.loader.exec_module(module)\n"
    "assert module.divide(2) == 5\n"
    "try:\n"
    "    module.divide(0)\n"
    "except ZeroDivisionError:\n"
    "    sys.exit(0)\n"
    "sys.exit(2)\n"
)


def propose_fail_closed(source: str, filename: str = FIXTURE_PATH) -> dict:
    """Propose exactly one typed except/pass to except/raise conversion."""
    if (not isinstance(source, str) or len(source.encode("utf-8")) > 32_000
            or not isinstance(filename, str) or not filename.endswith(".py")
            or len(filename) > 100 or "/" in filename or "\\" in filename
            or filename.startswith(".")):
        raise ValueError("Only small standalone Python inputs are supported")
    tree = ast.parse(source, filename=filename)
    candidates = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.ExceptHandler) and len(node.body) == 1
        and isinstance(node.body[0], ast.Pass) and node.type is not None
    ]
    if len(candidates) != 1:
        raise ValueError("Expected exactly one typed except handler containing only pass")
    node = candidates[0].body[0]
    lines = source.splitlines(keepends=True)
    if lines[node.lineno - 1].strip() != "pass":
        raise ValueError("Pass statement must be alone on its line")
    original_line = lines[node.lineno - 1]
    indent = original_line[:len(original_line) - len(original_line.lstrip())]
    ending = "\r\n" if original_line.endswith("\r\n") else "\n" if original_line.endswith("\n") else ""
    lines[node.lineno - 1] = indent + "raise" + ending
    candidate = "".join(lines)
    ast.parse(candidate, filename=filename)
    if candidate == source:
        raise ValueError("Candidate unchanged")
    patch = "".join(difflib.unified_diff(
        source.splitlines(keepends=True),
        candidate.splitlines(keepends=True),
        fromfile="a/" + filename, tofile="b/" + filename,
    ))
    return {
        "rule": "silent_exception", "candidate": candidate, "patch": patch,
        "changed_line": node.lineno,
        "method": "deterministic_ast_guided_fail_closed",
        "source_changed": False, "approval_required": True,
        "caveat": "Reraising alters failure behavior; require human review before real use.",
    }


def _run_fixture(source: str, directory: Path) -> dict:
    target = directory / FIXTURE_PATH
    target.write_text(source, encoding="utf-8")
    process = subprocess.run(
        [sys.executable, "-I", "-c", DRIVER, str(target)],
        cwd=directory, capture_output=True, text=True, timeout=15, check=False,
    )
    return {"exit_code": process.returncode, "passed": process.returncode == 0}


def evaluate_repair_demo() -> dict:
    """Real red/green test, on bundled nonsecret fixture only."""
    proposed = propose_fail_closed(FIXTURE)
    with tempfile.TemporaryDirectory(prefix="lab-repair-") as workspace:
        root = Path(workspace)
        before = _run_fixture(FIXTURE, root)
        after = _run_fixture(proposed["candidate"], root)
    if before["passed"] or not after["passed"]:
        raise RuntimeError("Red/green proof failed; no validated repair")
    return {
        "status": "validated_synthetic_only",
        "origin": "bundled_nonsecret_fixture",
        "producer": proposed["method"],
        "baseline": before, "repaired": after,
        "changes_applied_to_repository": False,
        "candidate": proposed["candidate"], "patch": proposed["patch"],
        "safety": {
            "requires_human_review_for_real_code": True,
            "auto_merge": False,
            "commands_from_model_executed": False,
            "arbitrary_project_code_executed": False,
        },
    }


def main() -> int:
    print(json.dumps(evaluate_repair_demo(), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
