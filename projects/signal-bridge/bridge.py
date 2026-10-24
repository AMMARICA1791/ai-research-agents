"""Signal Bridge: evidence-linked cross-source candidate connections."""
import argparse
import json
import re
from itertools import combinations
from pathlib import Path

STOP = set("about after against among based between could from have into more over study that their these this through using with research paper news latest".split())

def terms(text):
    return {w for w in re.findall(r"[a-z][a-z0-9-]{3,}", text.lower()) if w not in STOP}

def connect(signals, min_shared=2):
    """Produce candidate links, not claims of causation or scientific novelty."""
    edges = []
    for a, b in combinations(signals, 2):
        if a.get("source") == b.get("source") or a.get("url") == b.get("url"):
            continue
        if not all(isinstance(x.get(k), str) and x[k].startswith("https://") for x in (a, b) for k in ("url",)):
            continue
        ta, tb = terms(a.get("title", "")), terms(b.get("title", ""))
        shared = sorted(ta & tb)
        if len(shared) < min_shared:
            continue
        similarity = len(shared) / len(ta | tb) if ta | tb else 0
        edges.append({
            "sources": [{"source": x.get("source"), "title": x.get("title"), "url": x["url"],
                         "published": x.get("published"), "first_seen_utc": x.get("first_seen_utc")}
                        for x in (a, b)],
            "shared_terms": shared, "title_jaccard": round(similarity, 4),
            "relationship": "candidate topical overlap; causal relationship unverified",
            "confidence": "low", "novelty_verified": False,
            "evidence_level": "source metadata only; full texts not examined"
        })
    return sorted(edges, key=lambda e: (-e["title_jaccard"], e["sources"][0]["url"], e["sources"][1]["url"]))

def analyze(report):
    if not isinstance(report, dict) or not isinstance(report.get("signals"), list):
        raise ValueError("expected radar report with signals array")
    return {"status": "candidate_links_not_discoveries",
            "radar_generated_at_utc": report.get("generated_at_utc"),
            "input_signals": len(report["signals"]),
            "connections": connect(report["signals"]),
            "limitations": ["Title token overlap is not semantic inference.",
                            "No claim of early media detection, novelty or causation.",
                            "Source URLs are evidence pointers, not independently verified full text."]}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", required=True)
    parser.add_argument("--output", default="connections.json")
    args = parser.parse_args()
    data = analyze(json.loads(Path(args.report).read_text(encoding="utf-8")))
    Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Candidate connections: {len(data['connections'])}")

if __name__ == "__main__":
    main()
