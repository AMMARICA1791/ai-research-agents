"""Build reproducible experiment seed files from actual radar signals."""
import argparse
import json
import re
from pathlib import Path

def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:48] or "signal"

def build(report, limit=5):
    signals = report.get("signals")
    if not isinstance(signals, list):
        raise ValueError("signals must be a list")
    selected = sorted(
        (s for s in signals if isinstance(s, dict) and
         isinstance(s.get("url"), str) and s["url"].startswith("https://") and
         isinstance(s.get("title"), str) and s["title"].strip()),
        key=lambda s: (-int(s.get("signal", {}).get("score", 0)), str(s.get("id", "")))
    )[:limit]
    return {
        "project": "Experiment Seed",
        "radar_scan_utc": report.get("generated_at_utc"),
        "experiments": [{
            "id": slug(s.get("title", "")) + "-" + str(s.get("id", ""))[:8],
            "source": s.get("source"),
            "source_url": s["url"],
            "source_title": s["title"],
            "published": s.get("published"),
            "radar_topics": sorted(s.get("signal", {}).get("topics", {})),
            "research_question": "Can the specific claim in this source be reproduced using public data?",
            "protocol": [
                "Read the linked original source and record its exact testable claim.",
                "Identify the public dataset or create a minimal synthetic fixture.",
                "Define a baseline and measurable outcome before implementation.",
                "Run a controlled test and record commands, data provenance and results.",
                "Mark unsupported claims explicitly; do not infer novelty from a radar match."
            ],
            "stage": "unreviewed_source_candidate",
            "scientific_claim_verified": False,
            "experiment_executed": False
        } for s in selected],
        "limitations": "Templates only: no experiment has been implemented or validated."
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--report", required=True)
    p.add_argument("--output", default="experiment-seeds.json")
    p.add_argument("--limit", type=int, default=5)
    a = p.parse_args()
    if a.limit < 1 or a.limit > 40:
        p.error("--limit must be between 1 and 40")
    result = build(json.loads(Path(a.report).read_text(encoding="utf-8")), a.limit)
    Path(a.output).write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("Experiment seeds:", len(result["experiments"]))

if __name__ == "__main__":
    main()
