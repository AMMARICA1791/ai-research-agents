"""Source Gap: report radar feed failures and missing coverage."""
import argparse
import json
from collections import Counter
from pathlib import Path

def analyze(report):
    if not isinstance(report, dict) or not isinstance(report.get("signals"), list):
        raise ValueError("expected radar report with signals list")
    errors = report.get("feed_errors", [])
    if not isinstance(errors, list):
        raise ValueError("feed_errors must be list")
    by_source = Counter(str(x.get("source", "unknown")) for x in report["signals"] if isinstance(x, dict))
    failed = sorted({str(x.get("feed", "unknown")) for x in errors if isinstance(x, dict)})
    return {
        "project": "Source Gap",
        "generated_at_utc": report.get("generated_at_utc"),
        "successful_feeds": report.get("successful_feeds"),
        "failed_feeds": failed,
        "failed_feed_count": len(failed),
        "selected_signal_counts": dict(sorted(by_source.items())),
        "coverage_warning": "feed_errors" if failed else ("no_selected_signals" if not by_source else "none_reported"),
        "limitations": "Selected signals are capped by radar ranking; absent source does not prove feed outage."
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--report", required=True)
    p.add_argument("--output", default="source-gap.json")
    a = p.parse_args()
    result = analyze(json.loads(Path(a.report).read_text(encoding="utf-8")))
    Path(a.output).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Failed feeds:", result["failed_feed_count"])

if __name__ == "__main__":
    main()
