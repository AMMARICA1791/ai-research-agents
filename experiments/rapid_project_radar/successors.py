"""Create bounded successor experiments when a fresh, distinct research question is observed.

This is hypothesis branching, not proof of scientific novelty. Historical branch
content is treated strictly as data; no remote code is executed.
"""
import argparse
import hashlib
import json
from pathlib import Path
from experiments.rapid_project_radar.anticipate import scaffold

def successors(projects_dir, inventory_file, output_dir, limit=12):
    root = Path(projects_dir)
    inventory = json.loads(Path(inventory_file).read_text(encoding="utf-8"))
    history = inventory.get("projects", [])
    if not isinstance(history, list):
        raise ValueError("invalid historical inventory")
    output = []
    for source in sorted(root.glob("*/hypothesis.json")):
        if len(output) >= limit:
            break
        h = json.loads(source.read_text(encoding="utf-8"))
        question = str(h.get("research_question", "")).strip()
        topic = h.get("topic")
        source_id = h.get("source_id")
        if not question or not source_id or not topic:
            continue
        candidates = []
        for item in history:
            old = item.get("hypothesis") or {}
            if old.get("topic") != topic or old.get("source_id") == source_id:
                continue
            old_question = str(old.get("research_question", "")).strip()
            if not old_question or old_question.casefold() == question.casefold():
                continue
            if item.get("metadata_only"):
                continue
            candidates.append(item)
        if not candidates:
            continue
        parent = sorted(candidates, key=lambda x: x.get("project_id", ""))[0]
        parent_id = parent["project_id"]
        digest = hashlib.sha256((parent_id + "\n" + question).encode()).hexdigest()[:16]
        successor_id = f"{topic}-{source_id}-next-{digest}"
        successor_h = dict(h)
        successor_h["experiment_type"] = "successor_question"
        successor_h["parent_project_id"] = parent_id
        successor_h["parent_branch"] = parent["branch"]
        successor_h["trigger"] = "distinct_source_grounded_question_same_topic"
        successor_h["difference_from_parent"] = {
            "previous_question": parent["hypothesis"]["research_question"],
            "new_question": question,
        }
        successor_h["novelty_verified"] = False
        dest = Path(scaffold(successor_h, output_dir, successor_id))
        with (dest / "README.md").open("a", encoding="utf-8") as f:
            f.write("\n## Successor lineage\n\nParent: `" + parent_id +
                    "` (`" + parent["branch"] + "`).\n\nNew question: " +
                    question + "\n\nThis is a separate question to investigate, "
                    "not evidence of scientific progress or independent validation.\n")
        output.append({"project_id": successor_id, "parent": parent_id,
                       "question": question, "path": str(dest)})
    return output

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--projects", required=True)
    p.add_argument("--portfolio", required=True)
    p.add_argument("--output-dir", required=True)
    p.add_argument("--limit", type=int, default=12)
    a = p.parse_args()
    print(json.dumps(successors(a.projects, a.portfolio, a.output_dir, a.limit), indent=2))
