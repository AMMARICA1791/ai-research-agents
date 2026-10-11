"""Evidence-based improvement work orders for owner review (never executable).

Plans are deterministic proposals, not code patches, tests or proven fixes.
"""
from __future__ import annotations

from .knowledge import ALLOWED_RULES

RULE_PLANS = {
    "syntax_error": ("Repair parser error, then add a syntax regression test",
                     ["python -m compileall -q lab agents research web", "python -m pytest -q tests/"]),
    "silent_exception": ("Investigate exception handler, add observability and regression coverage",
                         ["python -m pytest -q tests/", "python -m compileall -q lab web"]),
    "dynamic_execution": ("Review the necessity of eval or exec and replace with safer parsing",
                          ["python -m pytest -q tests/"]),
    "missing_tests": ("Introduce a tested fixture for an untested behavior",
                      ["python -m pytest -q tests/"]),
    "unreadable_python": ("Review file encoding and update tests",
                          ["python -m compileall -q lab", "python -m pytest -q tests/"]),
    "inspection_limit": ("Review scan limits and split project scopes",
                         ["python -m pytest -q tests/"]),
    "internal_dependency_cycle": ("Break the internal import cycle without changing public imports",
                                  ["python -m compileall -q lab agents", "python -m pytest -q tests/"]),
}


def propose_work_orders(findings: list[dict], prior_knowledge: dict, limit: int = 10) -> list[dict]:
    previous = prior_knowledge.get("previous_rule_counts", {})
    tasks = []
    for finding in findings:
        rule = finding.get("rule")
        if rule not in ALLOWED_RULES:
            continue
        check = finding.get("evidence", "")
        if not isinstance(check, str) or not check or len(check) > 280:
            continue
        action, checks = RULE_PLANS[rule]
        recurring = type(previous.get(rule)) is int and previous[rule] > 0
        priority = "high" if rule == "syntax_error" else ("medium" if recurring else "normal")
        tasks.append({
            "rule": rule,
            "evidence": check,
            "recommended_action": action,
            "verification_commands": checks,
            "observed_in_prior_run": recurring,
            "priority": priority,
            "approval": "required",
            "status": "proposed_not_executed",
        })
    priority_rank = {"high": 0, "medium": 1, "normal": 2}
    tasks.sort(key=lambda x: (priority_rank[x["priority"]], x["rule"], x["evidence"]))
    return tasks[:max(0, min(limit, 10))]
