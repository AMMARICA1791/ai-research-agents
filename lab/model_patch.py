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
    """Ask local model for complete Python source, then verify without trusting it."""
    prompt = (
        "You are completing a Python code repair task. Output the full "
        "corrected Python module as a JSON object with exactly one field: code.\n"
        "Goal: divide(2) returns 5, divide(0) raises ZeroDivisionError.\n"
        "Keep all function definitions, try/except blocks, expression values "
        "and statements identical, EXCEPT change the single pass in "
        "except ZeroDivisionError to an unqualified raise statement.\n"
        "Input Python:\n" + FIXTURE + "\n"
        "Output ONLY valid JSON with the complete corrected file in code. "
        "Do not return markdown, tests, explanations or additional fields."
    )
    report = {
        "model": MODEL, "source": "synthetic_fixture_only",
        "generator": "real_local_ollama_generation",
        "status": "model_unavailable",
        "candidate_rejected": True, "repository_modified": False,
        "human_approval_required": True, "model_text_retained_on_failure": False,
        "attempts": 0, "rejection_reasons": [],
    }
    # Allow exactly one constrained second attempt, not unlimited cost/compute.
    for attempt in range(2):
        report["attempts"] = attempt + 1
        attempt_prompt = prompt
        if attempt == 1:
            attempt_prompt += (
                "\nPrevious candidate failed the strict AST gate. "
                "IMPORTANT: The entire repaired function must be exactly "
                "the same Python structure; the only behavioral statement "
                "to change is the word pass to the word raise. "
                "Provide the complete module source as JSON code."
            )
        try:
            response = requests.post(
                ENDPOINT,
                json={
                    "model": MODEL, "prompt": attempt_prompt, "stream": False,
                    "format": {
                        "type": "object",
                        "properties": {"code": {"type": "string"}},
                        "required": ["code"], "additionalProperties": False,
                    },
                    "keep_alive": "0s",
                    "options": {"temperature": 0, "seed": 42 + attempt,
                                "num_predict": 260, "num_ctx": 1536},
                },
                timeout=(5, 120), allow_redirects=False,
            )
            response.raise_for_status()
            raw = response.json()["response"]
            if not isinstance(raw, str) or len(raw) > 5_000:
                report["rejection_reasons"].append("invalid_payload_size")
                report["status"] = "rejected_invalid_model_output"
                continue
            parsed = json.loads(raw)
            candidate = parsed.get("code") if isinstance(parsed, dict) else None
            if not isinstance(candidate, str):
                report["rejection_reasons"].append("missing_python_code_string")
                report["status"] = "rejected_unsafe_or_incorrect_candidate"
                continue
            if not _validate_candidate(candidate):
                # Do not include rejected text, even when the issue was harmless.
                report["rejection_reasons"].append("candidate_ast_outside_allowlist")
                report["status"] = "rejected_unsafe_or_incorrect_candidate"
                continue
            with tempfile.TemporaryDirectory(prefix="lab-qwen-coder-") as directory:
                folder = Path(directory)
                before = _run_fixture(FIXTURE, folder)
                after = _run_fixture(candidate, folder)
            report["baseline_failed_as_expected"] = not before["passed"]
            report["repaired_test_passed"] = after["passed"]
            if before["passed"] or not after["passed"]:
                report["rejection_reasons"].append("behavioral_test_failed")
                report["status"] = "rejected_behavioral_test"
                continue
            report["status"] = "accepted_verified_model_generated_patch"
            report["candidate_rejected"] = False
            report["patch"] = propose_fail_closed(FIXTURE)["patch"]
            report["candidate"] = candidate
            return report
        except (requests.RequestException, ValueError, TypeError, KeyError,
                IndexError, json.JSONDecodeError):
            report["rejection_reasons"].append("provider_or_json_error")
            report["status"] = "model_unavailable_or_invalid_response"
    return report


def main() -> int:
    output = run_coder_challenge()
    print(json.dumps(output, indent=2, ensure_ascii=False))
    # Automated evaluator failure means experiment did not prove AI coding.
    return 0 if output["status"] == "accepted_verified_model_generated_patch" else 2


if __name__ == "__main__":
    raise SystemExit(main())
