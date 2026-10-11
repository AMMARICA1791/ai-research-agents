"""Evidence-first, deterministic triage of bounded Python AST findings.

No model, patch execution, remote writes, source snippets, or risk certainty.
Every recommendation is a *human review task*, not an established defect.
"""
from __future__ import annotations

import hashlib
import re
from urllib.parse import quote

PRIORITY = {
    "syntax_error": (1, 90, "Python parser rejected this file", "Confirm the syntax error using Python ast.parse on this file only; add an import-independent syntax regression."),
    "dynamic_execution": (2, 70, "A direct eval or exec call was observed", "Review whether this call can receive untrusted input; add a unit test for the authorized input boundary before proposing a replacement."),
    "silent_exception": (2, 60, "An exception handler contains only pass", "Review the intended error-handling contract; add a test for the relevant exception path before proposing a behavior change."),
    "internal_dependency_cycle": (2, 50, "A possible import cycle was observed", "Inspect the related modules and their imports manually; test the planned refactor without running the target project in this auditor."),
    "missing_tests": (3, 35, "No Python test file was found in the inspected subset", "Verify the project's test strategy and scan coverage; locate tests or propose one focused regression for an actual defect."),
    "unreadable_python": (3, 30, "A Python source file was not decoded", "Confirm file encoding and byte integrity manually before changing this file."),
    "inspection_limit": (3, 20, "The bounded static inspection reached a limit", "Increase coverage by reviewing smaller authorized scopes; do not interpret missing findings as safety."),
}
SEVERITY = {"high", "medium", "low"}
EVIDENCE_LINE = re.compile(r"(.+):([1-9][0-9]{0,6})\Z")


def _location(raw: str) -> tuple[str, int | None] | None:
    if not isinstance(raw, str) or not raw or len(raw) > 350:
        return None
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in raw):
        return None
    if raw == ".":
        return "", None
    match = EVIDENCE_LINE.fullmatch(raw)
    path = match.group(1) if match else raw
    line = int(match.group(2)) if match else None
    if (path.startswith("/") or "\\" in path or "//" in path or
            any(part in ("", ".", "..") for part in path.split("/"))):
        return None
    return path, line


def build_work_orders(
    repository: str, sha: str, findings: list[dict], limit: int = 12
) -> dict:
    """Order known scanner rules for manual review; reject malformed evidence."""
    if (not isinstance(repository, str) or not re.fullmatch(
            r"https://github\.com/[A-Za-z0-9][A-Za-z0-9-]{0,38}/[A-Za-z0-9_-][A-Za-z0-9._-]{0,99}",
            repository) or not isinstance(sha, str)
            or not re.fullmatch(r"[0-9a-f]{40}", sha)):
        raise ValueError("Untrusted repository or commit identity")
    if not isinstance(findings, list) or len(findings) > 100:
        raise ValueError("Findings outside bounded scanner limits")
    if type(limit) is not int or not 1 <= limit <= 20:
        raise ValueError("Work order limit must be between 1 and 20")
    result = []
    rejected = 0
    seen = set()
    for f in findings:
        if (not isinstance(f, dict) or type(f.get("rule")) is not str
                or type(f.get("severity")) is not str
                or f["rule"] not in PRIORITY or f["severity"] not in SEVERITY):
            rejected += 1
            continue
        location = _location(f.get("evidence"))
        if location is None:
            rejected += 1
            continue
        path, line = location
        key = (f["rule"], path, line)
        if key in seen:
            continue
        seen.add(key)
        rank, weight, reason, next_test = PRIORITY[f["rule"]]
        ref = f"{repository}/blob/{sha}/{quote(path, safe='/')}" if path else f"{repository}/tree/{sha}"
        if line is not None:
            ref += f"#L{line}"
        stable_id = hashlib.sha256(
            ("\n".join([repository, sha, f["rule"], path, str(line)])).encode("utf-8")
        ).hexdigest()[:16]
        result.append({
            "id": stable_id,
            "priority": f"P{rank}",
            "priority_score": weight,
            "rule": f["rule"],
            "scanner_severity": f["severity"],
            "evidence": f["evidence"],
            "evidence_url": ref,
            "observation": reason,
            "suggested_check": next_test,
            "review_status": "pending_human_verification",
            "evidence_type": "static_python_ast_heuristic",
            "fix_generated": False,
            "uncertainty": "Not confirmed as a defect or security vulnerability",
        })
    result.sort(key=lambda item: (
        -item["priority_score"], item["evidence"], item["rule"]
    ))
    return {
        "method": "fixed_rule_review_order_v1",
        "source_commit": sha,
        "work_orders": result[:limit],
        "total_valid_unique_findings": len(result),
        "rejected_malformed_findings": rejected,
        "not_shown_due_to_cap": max(0, len(result)-limit),
        "human_review_required": True,
        "automated_patch_generated": False,
        "priority_meaning": "Review sequence only; not exploit severity, business impact, probability or confidence",
    }
