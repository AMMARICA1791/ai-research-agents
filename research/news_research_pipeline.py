"""Run a bounded news-to-evidence pipeline using public feeds and source pages.

python -m research.news_research_pipeline --output research_output/news_research.json

This is source collection and an evidence review queue, NOT automatic fact checking.
"""
import argparse
import datetime as dt
import json
from pathlib import Path
from research.ai_news_feed import gather
from research.live_news_research import collect, dossier

def run(max_articles=3):
    inventory = gather(limit=8)
    cases = []
    for story in inventory["stories"][:max_articles]:
        case = {"headline": story["title"], "feed_source": story["source"],
                "url": story["url"], "published": story["published"]}
        try:
            page = collect(story["url"])
            report = dossier(page, "What evidence supports this headline?")
            case["retrieval_status"] = "ARTICLE_RETRIEVED"
            case["evidence"] = report
        except Exception as exc:
            # Fail individually; preserve the headline and the error for review.
            case["retrieval_status"] = "ARTICLE_NOT_RETRIEVED"
            case["error"] = f"{type(exc).__name__}: {exc}"[:300]
        cases.append(case)
    return {"generated_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
            "status": "SOURCE_INVENTORY_NOT_FACT_CHECKED",
            "article_cases": cases, "feed_errors": inventory["source_errors"],
            "feed_headlines_found": len(inventory["stories"]),
            "limitations": [
                "A source repeating its own headline is not independent corroboration",
                "No LLM reasoning, semantic claim verification, or conversational memory",
                "Dynamic websites, paywalls, and redirects may block retrieval",
                "Human review required before publishing any truth verdict"
            ]}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", default="research_output/news_research.json")
    p.add_argument("--max-articles", type=int, default=3)
    args = p.parse_args()
    if not 1 <= args.max_articles <= 10:
        p.error("--max-articles must be 1..10")
    result = run(args.max_articles)
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Feed headlines:", result["feed_headlines_found"])
    print("Retrieved articles:", sum(c["retrieval_status"] == "ARTICLE_RETRIEVED" for c in result["article_cases"]))
    print("Feed errors:", result["feed_errors"])
    print("Output:", target)

if __name__ == "__main__":
    main()
