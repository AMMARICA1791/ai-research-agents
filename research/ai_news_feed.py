"""Collect recent AI news headlines from public RSS/Atom feeds.

Run: python -m research.ai_news_feed --output research_output/ai_news.json
No API keys. Headlines are unverified leads, not established facts.
"""
import argparse
import datetime as dt
import json
from pathlib import Path
import urllib.request
import xml.etree.ElementTree as ET

from research.live_news_research import NoRedirect, USER_AGENT, safe_url

FEEDS = {
    "Google DeepMind": "https://deepmind.google/blog/rss.xml",
    "arXiv cs.AI": "https://export.arxiv.org/rss/cs.AI",
}
ATOM = "{http://www.w3.org/2005/Atom}"
MAX_FEED_BYTES = 500_000

def _text(node, names):
    for name in names:
        child = node.find(name)
        if child is not None and child.text:
            return " ".join(child.text.split())[:500]
    return ""

def parse_feed(data, source, limit=12):
    root = ET.fromstring(data)
    entries = root.findall(".//item")
    atom = False
    if not entries:
        entries = root.findall(ATOM + "entry")
        atom = True
    items = []
    for entry in entries[:limit]:
        title = _text(entry, [ATOM + "title", "title"])
        published = _text(entry, [ATOM + "updated", ATOM + "published", "pubDate", "date"])
        if atom:
            link = ""
            for child in entry.findall(ATOM + "link"):
                if child.attrib.get("rel", "alternate") == "alternate":
                    link = child.attrib.get("href", "")
                    break
        else:
            link = _text(entry, ["link"])
        if not title or not link:
            continue
        try:
            safe_url(link)
        except (ValueError, OSError):
            continue
        items.append({"source": source, "title": title, "url": link, "published": published,
                      "verification": "UNVERIFIED_HEADLINE"})
    return items

def fetch_feed(url):
    safe_url(url)
    opener = urllib.request.build_opener(NoRedirect)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT,
                                               "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml"})
    with opener.open(req, timeout=15) as response:
        payload = response.read(MAX_FEED_BYTES + 1)
        if len(payload) > MAX_FEED_BYTES:
            raise ValueError("Feed exceeds size limit")
        return payload

def gather(feeds=None, limit=12):
    feeds = FEEDS if feeds is None else feeds
    stories, errors, seen = [], {}, set()
    for source, url in feeds.items():
        try:
            for story in parse_feed(fetch_feed(url), source, limit):
                if story["url"] not in seen:
                    stories.append(story)
                    seen.add(story["url"])
        except (ValueError, OSError, ET.ParseError) as exc:
            errors[source] = str(exc)[:240]
    return {"retrieved_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
            "status": "HEADLINES_ONLY_NOT_FACT_CHECKED",
            "stories": stories, "source_errors": errors,
            "note": "Some sources may redirect, block bots, or become unavailable. Errors are recorded, not silently ignored."}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="research_output/ai_news.json")
    parser.add_argument("--limit", type=int, default=12)
    args = parser.parse_args()
    if not 1 <= args.limit <= 50:
        parser.error("--limit must be 1..50")
    report = gather(limit=args.limit)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Collected {len(report['stories'])} unverified leads; {len(report['source_errors'])} feed errors. {output}")

if __name__ == "__main__":
    main()
