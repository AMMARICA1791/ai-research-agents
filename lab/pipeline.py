"""Evidence-based multi-role laboratory: inspect, reason, compare, propose and record.

No source file is written by this pipeline. An optional model can critique
aggregated rule counts, but its text never becomes an executable instruction.
"""
from __future__ import annotations

import os
from pathlib import Path

from .dependency import analyze_internal_dependencies
from .inspector import inspect_repository
from .knowledge import historical_context, load_state, record, save_state
from .memory import LabMemory
from .model import OptionalModel
from .local_model import LocalOllamaModel
from .improvement import propose_work_orders


class LabOrchestrator:
    stages = ("explorer", "analyst", "dependency_mapper", "engineer",
              "critic", "validator", "synthesizer")

    def __init__(self, memory: LabMemory | None = None,
                 model: OptionalModel | None = None,
                 knowledge_path: str | Path | None = None):
        self.memory = memory or LabMemory()
        self.model = model if model is not None else (LocalOllamaModel() if os.getenv("LAB_MODEL_BACKEND") == "ollama" else OptionalModel())
        self.knowledge_path = Path(knowledge_path) if knowledge_path else (
            Path(os.environ["LAB_KNOWLEDGE_PATH"]) if os.getenv("LAB_KNOWLEDGE_PATH") else None)

    def run(self, root: str | Path, goal: str) -> dict:
        goal = goal.strip()
        if not 8 <= len(goal) <= 500:
            raise ValueError("Research goal must be between 8 and 500 characters")
        state = load_state(self.knowledge_path) if self.knowledge_path else {"schema_version": 1, "runs": []}
        history = historical_context(state)
        scan = inspect_repository(Path(root))
        events: list[dict] = []
        discoveries = {
            "files_scanned": scan["files_scanned"],
            "python_files_parsed": scan["python_files_parsed"],
            "truncated": scan["truncated"],
        }
        events.append({"stage": "explorer", "result": discoveries})

        findings = list(scan["findings"])
        dependency_graph = analyze_internal_dependencies(scan["files"])
        for cycle in dependency_graph["cycles"]:
            findings.append({
                "rule": "internal_dependency_cycle", "severity": "medium",
                "evidence": cycle[0], "message": "Static internal import cycle: " + " → ".join(cycle)
            })
        findings.sort(key=lambda f: ({"high": 0, "medium": 1, "low": 2}[f["severity"]], f["evidence"]))
        findings = findings[:100]
        risk_counts = {level: sum(f["severity"] == level for f in findings) for level in ("high", "medium", "low")}
        events.append({"stage": "analyst", "result": {"finding_count": len(findings), "risk_counts": risk_counts}})
        events.append({"stage": "dependency_mapper", "result": {
            "edge_count": dependency_graph["edge_count"],
            "cycles": dependency_graph["cycles"], "module_count": dependency_graph["module_count"]
        }})

        proposal_rules = {
            "syntax_error": "Repair Python syntax and add a regression test",
            "silent_exception": "Replace silent exception handling with observable error reporting",
            "dynamic_execution": "Review dynamic execution and replace with a bounded parser if practical",
            "missing_tests": "Add automated tests for the inspected project",
            "unreadable_python": "Investigate unreadable Python source",
            "inspection_limit": "Split the audit into bounded project scopes",
            "internal_dependency_cycle": "Review and untangle cyclic imports",
        }
        proposals = [
            {"title": proposal_rules.get(f["rule"], "Review finding") + ": " + f["evidence"],
             "evidence": f["evidence"]}
            for f in findings[:15]
        ]
        if not proposals:
            evidence = "tests/" if any(x.startswith("tests/") for x in scan["sources"]) else "."
            proposals.append({"title": "Extend test coverage for the next research iteration", "evidence": evidence})
        events.append({"stage": "engineer", "result": {"proposal_count": len(proposals)}})
        repeated = {
            rule: {"previous": previous, "current": sum(f["rule"] == rule for f in findings)}
            for rule, previous in history["previous_rule_counts"].items()
            if previous > 0 and any(f["rule"] == rule for f in findings)
        }
        events.append({"stage": "critic", "result": {
            "repeated_rule_counts": repeated,
            "previous_runs": history["previous_runs"],
            "model_is_optional": True,
        }})

        evidence_paths = set(scan["sources"])
        grounded = all(p["evidence"].split(":")[0] in evidence_paths or p["evidence"] in {".", "tests/"}
                       for p in proposals)
        validation = {
            "evidence_grounded": grounded,
            "syntax_findings": risk_counts["high"],
            "changes_applied": False,
            "proposals_review_required": True,
        }
        events.append({"stage": "validator", "result": validation})

        # Language-model requests receive aggregate counts only. Never raw goals,
        # source text, filenames, secrets, memory or user prompts.
        model_result = (self.model.summarize(goal, findings, history=history)
                        if isinstance(self.model, LocalOllamaModel)
                        else self.model.summarize(goal, findings))
        work_orders = propose_work_orders(findings, history)
        summary = {
            "goal": goal, "source": "local_read_only_scan", "scope": scan["root"],
            "discovery": discoveries, "risk_counts": risk_counts, "findings": findings,
            "dependencies": dependency_graph, "prior_knowledge": history,
            "proposal_count": len(proposals), "work_orders": work_orders,
            "validation": validation,
            "model": model_result,
            "next_action": "Human review required before any source changes",
        }
        events.append({"stage": "synthesizer", "result": {
            "model_mode": model_result["mode"], "finding_count": len(findings)}})
        mission_id = self.memory.save_mission(goal, summary, events, proposals)
        result = {
            "id": mission_id, "status": "completed", "report": summary,
            "agent_stages": list(self.stages),
            "proposals": self.memory.get_mission(mission_id)["proposals"],
        }
        if self.knowledge_path:
            save_state(self.knowledge_path, record(state, result))
        return result
