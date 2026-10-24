"""Signal Delta: distinguish newly observed radar signals from previously seen ones."""
import argparse
import json
from pathlib import Path

def evaluate(report):
    signals = report.get("signals")
    if not isinstance(signals, list):
        raise ValueError("report must include signals list")
    new = [s for s in signals if s.get("first_seen_this_scan") is True]
    known = [s for s in signals if s.get("first_seen_this_scan") is False]
    unknown = len(signals) - len(new) - len(known)
    return {
        "project": "Signal Delta",
        "radar_generated_at_utc": report.get("generated_at_utc"),
        "total_selected": len(signals),
        "newly_observed": len(new),
        "previously_observed": len(known),
        "unknown_first_seen_status": unknown,
        "new_signal_links": [{"title":s.get("title"),"url":s.get("url"),"source":s.get("source"),
                              "first_seen_utc":s.get("first_seen_utc")} for s in new],
        "note": "New means first seen by this radar registry, not globally new or independently verified."
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--report", required=True)
    p.add_argument("--output", default="signal-delta.json")
    a = p.parse_args()
    result = evaluate(json.loads(Path(a.report).read_text(encoding="utf-8")))
    Path(a.output).write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("New signals:", result["newly_observed"])

if __name__ == "__main__":
    main()
