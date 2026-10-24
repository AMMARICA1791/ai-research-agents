"""Topic Pulse: summarize topic occurrences in a public radar report."""
import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

def analyze(report):
    signals = report.get("signals")
    if not isinstance(signals, list):
        raise ValueError("report must include signals list")
    counts = Counter()
    sources = defaultdict(set)
    examples = defaultdict(list)
    for item in signals:
        if not isinstance(item, dict):
            continue
        topics = item.get("signal", {}).get("topics", {})
        if not isinstance(topics, dict):
            continue
        for topic in topics:
            counts[topic] += 1
            sources[topic].add(str(item.get("source", "unknown")))
            if len(examples[topic]) < 3:
                examples[topic].append({"title": item.get("title"), "url": item.get("url")})
    return {
        "project": "Topic Pulse",
        "generated_at_utc": report.get("generated_at_utc"),
        "topics": [
            {"topic": topic, "signal_count": count,
             "distinct_sources": len(sources[topic]), "examples": examples[topic]}
            for topic, count in sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))
        ],
        "scope": "keyword-tagged radar signals; not verified global trends"
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--report", required=True)
    p.add_argument("--output", default="topic-pulse.json")
    a = p.parse_args()
    result = analyze(json.loads(Path(a.report).read_text(encoding="utf-8")))
    Path(a.output).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Topics:", len(result["topics"]))

if __name__ == "__main__":
    main()
