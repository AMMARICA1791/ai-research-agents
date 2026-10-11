"""Public-safe longitudinal research journal: fixed taxonomy, never private text.

Legacy schema v1 journals with only "runs" are read without migration failure.
New writes add a bounded derived "lessons" catalog with controlled vocabulary.
"""
from __future__ import annotations

import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path

MAX_ENTRIES = 120
RULE_CHECKS = {
    "syntax_error": "verify_python_syntax",
    "silent_exception": "test_exception_observability",
    "dynamic_execution": "review_dynamic_execution",
    "missing_tests": "check_test_coverage",
    "unreadable_python": "check_file_encoding",
    "inspection_limit": "review_scan_scope",
    "internal_dependency_cycle": "review_import_graph",
}
ALLOWED_RULES = set(RULE_CHECKS)
MODES = {
    "not_configured", "remote_model", "provider_error", "invalid_endpoint",
    "local_model", "local_model_unavailable", "unknown",
}


def empty_state() -> dict:
    return {"schema_version": 1, "runs": [], "lessons": []}


def _lessons_from_runs(runs: list[dict]) -> list[dict]:
    """Derive safe continuity signals from observations; never claim a fix."""
    lessons = []
    for rule in sorted(ALLOWED_RULES):
        observations = sum(int(x["rule_counts"].get(rule, 0) > 0) for x in runs)
        if not observations:
            continue
        consecutive = 0
        for x in reversed(runs):
            if x["rule_counts"].get(rule, 0) > 0:
                consecutive += 1
            else:
                break
        lessons.append({
            "rule": rule,
            "observed_runs": min(observations, MAX_ENTRIES),
            "consecutive_runs": min(consecutive, MAX_ENTRIES),
            "status": "observed" if consecutive else "not_observed_in_last_scan",
            "next_check": RULE_CHECKS[rule],
        })
    return lessons


def _validate_state(data: dict) -> None:
    if (not isinstance(data, dict) or set(data) not in (
        {"schema_version", "runs"}, {"schema_version", "runs", "lessons"}
    ) or type(data.get("schema_version")) is not int
            or data["schema_version"] != 1
            or not isinstance(data.get("runs"), list)
            or len(data["runs"]) > MAX_ENTRIES):
        raise ValueError("Invalid public research journal schema")
    for entry in data["runs"]:
        if not isinstance(entry, dict) or set(entry) != {
            "at", "files_scanned", "python_parsed", "finding_count",
            "risk_counts", "rule_counts", "model_mode"
        }:
            raise ValueError("Unexpected run fields")
        counts, categories = entry["risk_counts"], entry["rule_counts"]
        if not isinstance(counts, dict) or set(counts) != {"high", "medium", "low"}:
            raise ValueError("Invalid risk categories")
        if not isinstance(categories, dict) or not set(categories).issubset(ALLOWED_RULES):
            raise ValueError("Unexpected rule category")
        if any(type(x) is not int or x < 0 or x > 400
               for x in (entry["files_scanned"], entry["python_parsed"], entry["finding_count"])):
            raise ValueError("Invalid file counts")
        if any(type(x) is not int or x < 0 or x > 100
               for x in [*counts.values(), *categories.values()]):
            raise ValueError("Invalid finding counts")
        if (entry["model_mode"] not in MODES or not isinstance(entry["at"], str)
                or len(entry["at"]) > 50):
            raise ValueError("Invalid status or timestamp")
    if "lessons" in data:
        expected = _lessons_from_runs(data["runs"])
        if data["lessons"] != expected:
            raise ValueError("Unexpected or inconsistent longitudinal lesson data")


def load_state(path: str | Path) -> dict:
    path = Path(path)
    if not path.is_file():
        return empty_state()
    if path.stat().st_size > 100_000:
        raise ValueError("Knowledge journal exceeds 100 KB")
    data = json.loads(path.read_text(encoding="utf-8"))
    _validate_state(data)
    # Migrates the schema in memory without adding untrusted strings.
    data["lessons"] = _lessons_from_runs(data["runs"])
    return data


def historical_context(state: dict) -> dict:
    _validate_state(state)
    runs = state["runs"]
    previous = runs[-1] if runs else None
    return {
        "previous_runs": len(runs),
        "previous_finding_count": previous["finding_count"] if previous else None,
        "previous_rule_counts": previous["rule_counts"] if previous else {},
        "lessons": _lessons_from_runs(runs),
        "storage": "sanitized_public_branch" if runs else "new_journal",
    }


def record(state: dict, result: dict) -> dict:
    _validate_state(state)
    # Defensive allowlisting: no goals, paths, code, model text or identifiers.
    report = result["report"]
    rule_counts = {}
    for finding in report.get("findings", []):
        key = finding.get("rule", "")
        if key in ALLOWED_RULES:
            rule_counts[key] = min(rule_counts.get(key, 0) + 1, 100)
    discovery = report["discovery"]
    counts = report.get("risk_counts", {})
    mode = report.get("model", {}).get("mode", "not_configured")
    state["runs"].append({
        "at": datetime.now(timezone.utc).isoformat(),
        "files_scanned": min(max(int(discovery["files_scanned"]), 0), 400),
        "python_parsed": min(max(int(discovery["python_files_parsed"]), 0), 400),
        "finding_count": min(len(report.get("findings", [])), 100),
        "risk_counts": {level: min(max(0, int(counts.get(level, 0))), 100)
                        for level in ("high", "medium", "low")},
        "rule_counts": dict(sorted(rule_counts.items())),
        "model_mode": mode if mode in MODES else "unknown",
    })
    state["runs"] = state["runs"][-MAX_ENTRIES:]
    state["lessons"] = _lessons_from_runs(state["runs"])
    _validate_state(state)
    return state


def save_state(path: str | Path, state: dict) -> None:
    _validate_state(state)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(state, ensure_ascii=True, indent=2) + "\n"
    if len(encoded.encode()) > 100_000:
        raise ValueError("Knowledge journal exceeded size limit")
    fd, temp = tempfile.mkstemp(prefix=".knowledge-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(encoded)
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.remove(temp)
