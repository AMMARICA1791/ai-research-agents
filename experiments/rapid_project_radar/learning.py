"""Append-only, bounded experiment learning records for radar council.

Records observations, not model-weight training or scientific proof.
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ALLOWED = {"PASS", "FAIL", "INCONCLUSIVE"}

def record(project, outcome, observation, correction="", previous=None):
    if outcome not in ALLOWED:
        raise ValueError("unsupported outcome")
    if not isinstance(observation, str) or not observation.strip():
        raise ValueError("observation required")
    history = list(previous or [])
    if len(history) >= 100:
        raise ValueError("history limit reached; archive before continuing")
    entry = {"iteration": len(history) + 1, "outcome": outcome,
             "observation": observation[:2000], "proposed_correction": str(correction)[:2000],
             "evidence_status": "self_report_not_independently_verified"}
    history.append(entry)
    failures = [x for x in history if x["outcome"] == "FAIL"]
    return {"project_id": str(project), "iterations": history,
            "lessons": [{"iteration": x["iteration"], "avoid_repeating": x["observation"],
                         "try_next": x["proposed_correction"]} for x in failures],
            "automatic_code_changes": False, "model_weights_updated": False}

def save(project_dir, outcome, observation, correction=""):
    root = Path(project_dir)
    path = root / "LEARNING_LOG.json"
    old = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    data = record(root.name, outcome, observation, correction, old.get("iterations", []))
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return data

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--project", required=True)
    p.add_argument("--outcome", required=True, choices=sorted(ALLOWED))
    p.add_argument("--observation", required=True)
    p.add_argument("--correction", default="")
    args = p.parse_args()
    result = save(args.project, args.outcome, args.observation, args.correction)
    print(json.dumps({"project_id": result["project_id"], "iterations": len(result["iterations"])}))
