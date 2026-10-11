"""Real open-weight model code experiment with strict fail-closed validation.

Only a bundled synthetic Python exercise is ever sent to localhost Ollama
and executed after proving the candidate AST exactly matches the expected safe
repair. No repository code, secrets, customer data or arbitrary commands.
"""
from __future__ import annotations

import ast
import json
import tempfile
from pathlib import Path

import requests

from .autorepair import FIXTURE, _run_fixture, propose_fail_closed

MODEL = "qwen2.5-coder:1.5b"
ENDPOINT = "http://127.0.0.1:11434/api/generate"


def _validate_candidate(candidate: str) -> bool:
    if not isinstance(candidate, str) or len(candidate.encode("utf-8")) > 3_000:
        return False
    try:
        baseline = propose_fail_closed(FIXTURE)
        expected = ast.parse(baseline["candidate"])
        proposed = ast.parse(candidate)
        # An AI candidate may vary formatting, but must not introduce imports,
        # new statements, new calls, code side effects or arbitrary operations.
        return ast.dump(expected, include_attributes=False) == ast.dump(
            proposed, include_attributes=False
        )
    except (SyntaxError, ValueError, TypeError, UnicodeError):
        return False


def run_coder_challenge() -> dict:
    """Ask a local code model for a FULL patch, then independently prove it."""
    prompt = (
        "You are repairing a small standalone Python function in a synthetic "
        "coding evaluation. Produce the ENTIRE corrected Python file.\n"
        "Requirements: divide(2) must equal 5, divide(0) must RAISE "
        "ZeroDivisionError rather than quietly returning None. Edit ONLY the "
        "pass statement in the typed exception handler; keep all other Python "
        "statements and the function name and signature unchanged.\n"
        "Original Python file:\n" + FIXTURE + "\n"
        "Respond with ONLY one JSON object containing a string field named "
        "'code' that holds the ENTIRE corrected Python source. No Markdown."
    )
    report = {
        "model": MODEL, "source": "synthetic_fixture_only",
        "generator": "real_local_ollama_generation",
        "status": "model_unavailable",
        "candidate_rejected": True,
        "repository_modified": False, "human_approval_required": True,
        "model_text_retained_on_failure": False,
    }
    try:
        response = requests.post(
            ENDPOINT,
            json={
                "model": MODEL, "prompt": prompt, "stream": False,
                "format": "json", "keep_alive": "0s",
                "options": {"temperature": 0, "seed": 42,
                            "num_predict": 230, "num_ctx": 1536},
            },
            timeout=(5, 120), allow_redirects=False,
        )
        response.raise_for_status()
        raw = response.json()["response"]
        if not isinstance(raw, str) or len(raw) > 5_000:
            report["status"] = "rejected_invalid_model_output"
            return report
        parsed = json.loads(raw)
        candidate = parsed.get("code") if isinstance(parsed, dict) else None
        if not _validate_candidate(candidate):
            report["status"] = "rejected_unsafe_or_incorrect_candidate"
            return report
        with tempfile.TemporaryDirectory(prefix="lab-qwen-coder-") as directory:
            folder = Path(directory)
            before = _run_fixture(FIXTURE, folder)
            after = _run_fixture(candidate, folder)
        report["baseline_failed_as_expected"] = not before["passed"]
        report["repaired_test_passed"] = after["passed"]
        if before["passed"] or not after["passed"]:
            report["status"] = "rejected_behavioral_test"
            return report
        report["status"] = "accepted_verified_model_generated_patch"
        report["candidate_rejected"] = False
        report["patch"] = propose_fail_closed(FIXTURE)["patch"]
        report["candidate"] = candidate
        return report
    except (requests.RequestException, ValueError, TypeError, KeyError,
            IndexError, json.JSONDecodeError):
        report["status"] = "model_unavailable_or_invalid_response"
        return report


def main() -> int:
    output = run_coder_challenge()
    print(json.dumps(output, indent=2, ensure_ascii=False))
    # Automated evaluator failure means experiment did not prove AI coding.
    return 0 if output["status"] == "accepted_verified_model_generated_patch" else 2


if __name__ == "__main__":
    raise SystemExit(main())
