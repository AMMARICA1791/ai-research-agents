"""Offline evidence-based report generator: no model, no invented facts.

python -m research.news_report --dossier research_output/news_research.json
"""
import argparse
import json
from pathlib import Path

def build_report(dossier):
    lines = ["# AI News Evidence Report", "",
             "Status: SOURCE EXCERPTS ONLY — NOT INDEPENDENTLY VERIFIED", "",
             "Generated: " + str(dossier.get("generated_at_utc", "unknown")), "",
             "Feed headlines found: " + str(dossier.get("feed_headlines_found", 0)), ""]
    retrieved = 0
    for i, case in enumerate(dossier.get("article_cases", []), 1):
        lines.extend([f"## {i}. {case.get('headline', 'Untitled')}", "",
                      "Feed: " + str(case.get("feed_source", "unknown")),
                      "Link: " + str(case.get("url", "")),
                      "Retrieval: " + str(case.get("retrieval_status", "unknown")), ""])
        if case.get("retrieval_status") == "ARTICLE_RETRIEVED":
            retrieved += 1
            ev = case.get("evidence", {})
            source = ev.get("source", {})
            excerpt = ev.get("source_excerpt", "")
            lines.extend(["Final source URL: " + str(source.get("url", case.get("url", ""))),
                          "SHA-256: " + str(source.get("sha256", "unknown")),
                          "", "### Retrieved excerpt (publisher content, unverified)", "",
                          excerpt[:1200] if excerpt else "(empty excerpt)", "",
                          "### Review questions", "",
                          "- What is the original evidence behind the headline?",
                          "- Is there an independent source confirming the claim?",
                          "- What limitations or counterexamples are missing?", ""])
        else:
            lines.extend(["Retrieval error: " + str(case.get("error", "unknown")), ""])
    lines.extend(["## Collection totals", "",
                  f"Article cases: {len(dossier.get('article_cases', []))}",
                  f"Retrieved: {retrieved}",
                  f"Not retrieved: {len(dossier.get('article_cases', [])) - retrieved}", "",
                  "Feed errors: `" + json.dumps(dossier.get("feed_errors", {}), ensure_ascii=False) + "`", "",
                  "This report does not use an LLM, cross-check external claims, or establish truth."])
    return "\n".join(lines) + "\n"

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dossier", default="research_output/news_research.json")
    p.add_argument("--output", default="research_output/news_report.md")
    args = p.parse_args()
    dossier = json.loads(Path(args.dossier).read_text(encoding="utf-8"))
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(build_report(dossier), encoding="utf-8")
    print("Report:", target)

if __name__ == "__main__":
    main()
