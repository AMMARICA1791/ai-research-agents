"""Freshness Lens: transparent monitoring of radar source recency and coverage."""
import argparse
import json
from collections import Counter
from pathlib import Path

def evaluate(report):
    if not isinstance(report, dict) or not isinstance(report.get("signals"), list):
        raise ValueError("radar report must contain signals array")
    signals = report["signals"]
    counts = Counter(str(s.get("source", "unknown")) for s in signals)
    ages = [s["age_hours"] for s in signals if isinstance(s.get("age_hours"), (int, float)) and not isinstance(s["age_hours"], bool) and s["age_hours"] >= 0]
    return {
        "project": "Freshness Lens",
        "generated_at_utc": report.get("generated_at_utc"),
        "observed_signals": len(signals),
        "successful_feeds": report.get("successful_feeds"),
        "feed_errors": report.get("feed_errors", []),
        "signals_by_source": dict(sorted(counts.items())),
        "observed_within_6h": sum(age <= 6 for age in ages),
        "observed_within_24h": sum(age <= 24 for age in ages),
        "undated_or_unmeasured": len(signals) - len(ages),
        "median_feed_age_hours": sorted(ages)[len(ages)//2] if ages else None,
        "source_diversity": len(counts),
        "status": "no_signals" if not signals else ("limited_source_diversity" if len(counts) < 2 else "multiple_sources"),
        "caution": "Age is calculated from feed pubDate, not proof of early discovery or true first publication."
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--report", required=True)
    p.add_argument("--output", default="freshness.json")
    a = p.parse_args()
    result = evaluate(json.loads(Path(a.report).read_text(encoding="utf-8")))
    Path(a.output).write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("Signals:", result["observed_signals"], "Sources:", result["source_diversity"])

if __name__ == "__main__":
    main()
