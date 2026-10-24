"""Review the entire historical incubator portfolio and publish an English report.

This ranks evidence readiness, not scientific merit. No auto-merge or deletion.
"""
import argparse
import json
from pathlib import Path
from experiments.rapid_project_radar.council import review

def run(inventory, output):
    projects = inventory.get("projects", [])
    hypotheses = []
    for item in projects:
        h = dict(item.get("hypothesis") or {})
        h["_branch"] = item.get("branch", "")
        h["_project_id"] = item.get("project_id", "")
        hypotheses.append(h)
    dossiers = []
    for i, h in enumerate(hypotheses):
        dossier = review(h, [p for j, p in enumerate(hypotheses) if j != i])
        dossier["project_id"] = h["_project_id"]
        dossier["branch"] = h["_branch"]
        dossier["metadata_only"] = bool(projects[i].get("metadata_only"))
        if dossier["metadata_only"]:
            dossier["priority"]["band"] = "EVIDENCE_NEEDED"
        dossiers.append(dossier)
    dossiers.sort(key=lambda d: (-d["priority"]["score"], d["project_id"]))
    root = Path(output)
    root.mkdir(parents=True, exist_ok=True)
    (root / "portfolio_reviews.json").write_text(json.dumps({
        "scope": inventory.get("scope"), "inventory_complete": inventory.get("complete"),
        "reviewed": len(dossiers), "reviews": dossiers
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = ["# Radar Project Council — Historical Portfolio Review", "",
             "Automated evidence-readiness triage, **not** independent scientific validation.",
             "Priority is not proof of novelty, significance, or reproducibility.", "",
             f"Projects reviewed: **{len(dossiers)}**.",
             f"Historical inventory complete: **{bool(inventory.get('complete'))}**.", "",
             "| Rank | Project | Attention | Score | Evidence |",
             "| --- | --- | --- | ---: | --- |"]
    for i, d in enumerate(dossiers, 1):
        branch = d["branch"]
        project_id = d["project_id"]
        link = "https://github.com/" + inventory["repository"] + "/tree/" + branch + "/projects/incubator/" + project_id
        evidence = "metadata only" if d["metadata_only"] else "source metadata reviewed"
        lines.append(f"| {i} | [{project_id}]({link}) | {d['priority']['band']} | {d['priority']['score']} | {evidence} |")
    lines += ["", "## Interpretation", "",
              "These rankings identify projects to **inspect next**, not projects approved as scientific discoveries.",
              "No projects are deleted, merged or certified automatically.",
              "Every project remains publicly accessible in its independent branch.",
              ""]
    (root / "PORTFOLIO_COUNCIL_REVIEW.md").write_text("\n".join(lines), encoding="utf-8")
    return dossiers

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--inventory", required=True)
    p.add_argument("--output", required=True)
    args = p.parse_args()
    result = run(json.loads(Path(args.inventory).read_text(encoding="utf-8")), args.output)
    print(json.dumps({"reviewed": len(result), "top": [d["project_id"] for d in result[:5]]}))
