"""Read-only five-agent laboratory; proposals require a separate human decision."""
from __future__ import annotations

from pathlib import Path

from .inspector import inspect_repository
from .memory import LabMemory
from .model import OptionalModel


class LabOrchestrator:
    stages = ("explorer", "analyst", "engineer", "validator", "synthesizer")

    def __init__(self, memory: LabMemory | None = None, model: OptionalModel | None = None):
        self.memory = memory or LabMemory()
        self.model = model or OptionalModel()

    def run(self, root: str | Path, goal: str) -> dict:
        goal = goal.strip()
        if not 8 <= len(goal) <= 500:
            raise ValueError("Research goal must be between 8 and 500 characters")
        scan = inspect_repository(Path(root))
        events = []
        discoveries = {"files_scanned": scan["files_scanned"], "python_files_parsed": scan["python_files_parsed"], "truncated": scan["truncated"]}
        events.append({"stage": "explorer", "result": discoveries})
        findings = scan["findings"]
        risk_counts = {level: sum(f["severity"] == level for f in findings) for level in ("high", "medium", "low")}
        events.append({"stage": "analyst", "result": {"findings": findings, "risk_counts": risk_counts}})
        # Actionable, evidence-backed proposals; nothing is automatically modified.
        proposal_rules = {
            "syntax_error": "Repair Python syntax and add a regression test",
            "silent_exception": "Replace silent exception handling with observable error reporting",
            "dynamic_execution": "Review dynamic execution and replace with a bounded parser if practical",
            "missing_tests": "Add automated tests for the inspected project",
            "unreadable_python": "Investigate unreadable Python source",
            "inspection_limit": "Split the audit into bounded project scopes",
        }
        proposals = []
        for finding in findings[:15]:
            proposals.append({"title": proposal_rules.get(finding["rule"], "Review finding") + ": " + finding["evidence"], "evidence": finding["evidence"]})
        if not proposals:
            evidence = "tests/" if any(x.startswith("tests/") for x in scan["sources"]) else "."
            proposals.append({"title": "Extend test coverage for the next research iteration", "evidence": evidence})
        events.append({"stage": "engineer", "result": {"proposals": proposals}})
        evidence_paths = {p for p in scan["sources"]}
        is_grounded = all(p["evidence"].split(":")[0] in evidence_paths or p["evidence"] in {".", "tests/"} for p in proposals)
        validation = {"evidence_grounded": is_grounded, "syntax_findings": risk_counts["high"], "changes_applied": False}
        events.append({"stage": "validator", "result": validation})
        model_result = self.model.summarize(goal, findings)
        summary = {
            "goal": goal,
            "source": "local_read_only_scan",
            "scope": scan["root"],
            "discovery": discoveries,
            "risk_counts": risk_counts,
            "findings": findings,
            "proposal_count": len(proposals),
            "validation": validation,
            "model": model_result,
            "next_action": "Human review required before any source changes",
        }
        events.append({"stage": "synthesizer", "result": {"model_mode": model_result["mode"], "finding_count": len(findings)}})
        mission_id = self.memory.save_mission(goal, summary, events, proposals)
        return {"id": mission_id, "status": "completed", "report": summary, "agent_stages": list(self.stages),
                "proposals": self.memory.get_mission(mission_id)["proposals"]}
