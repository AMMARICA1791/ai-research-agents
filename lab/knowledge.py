"""Sanitized, cross-run knowledge journal safe for a PUBLIC repository branch.

Never store prompts, source code, filenames, model narratives, API keys or full SQLite.
Only bounded aggregate counters and rule codes are kept in Git history.
"""
from __future__ import annotations
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path

MAX_ENTRIES = 120
ALLOWED_RULES = {
    "syntax_error", "silent_exception", "dynamic_execution", "missing_tests",
    "unreadable_python", "inspection_limit", "internal_dependency_cycle",
}

def empty_state() -> dict:
    return {"schema_version": 1, "runs": []}

def load_state(path: str | Path) -> dict:
    path = Path(path)
    if not path.is_file():
        return empty_state()
    if path.stat().st_size > 100_000:
        raise ValueError("Knowledge state exceeds 100 KB")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema_version") != 1 or not isinstance(data.get("runs"), list):
        raise ValueError("Invalid knowledge state schema")
    if len(data["runs"]) > MAX_ENTRIES:
        raise ValueError("Knowledge journal entry limit exceeded")
    for entry in data["runs"]:
        if not isinstance(entry, dict) or set(entry) != {
            "at", "files_scanned", "python_parsed", "finding_count",
            "risk_counts", "rule_counts", "model_mode"
        }:
            raise ValueError("Unexpected fields in knowledge state")
    return data

def historical_context(state: dict) -> dict:
    runs = state["runs"]
    previous = runs[-1] if runs else None
    return {"previous_runs": len(runs),
            "previous_finding_count": previous["finding_count"] if previous else None,
            "previous_rule_counts": previous["rule_counts"] if previous else {},
            "storage": "sanitized_public_branch" if runs else "new_journal"}

def record(state: dict, result: dict) -> dict:
    # Defensive allowlisting: no paths, goals, content or identifiers enter state.
    report = result["report"]
    rule_counts = {}
    for finding in report.get("findings", []):
        key = finding.get("rule", "")
        if key in ALLOWED_RULES:
            rule_counts[key] = min(rule_counts.get(key, 0) + 1, 100)
    discovery = report["discovery"]
    counts = report.get("risk_counts", {})
    state["runs"].append({
        "at": datetime.now(timezone.utc).isoformat(),
        "files_scanned": min(int(discovery["files_scanned"]), 400),
        "python_parsed": min(int(discovery["python_files_parsed"]), 400),
        "finding_count": min(len(report.get("findings", [])), 100),
        "risk_counts": {v: min(max(0, int(counts.get(v, 0))), 100) for v in ("high", "medium", "low")},
        "rule_counts": dict(sorted(rule_counts.items())),
        "model_mode": report.get("model", {}).get("mode", "not_configured") if report.get("model", {}).get("mode") in {
            "not_configured", "remote_model", "provider_error", "invalid_endpoint"} else "unknown",
    })
    state["runs"] = state["runs"][-MAX_ENTRIES:]
    return state

def save_state(path: str | Path, state: dict) -> None:
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
