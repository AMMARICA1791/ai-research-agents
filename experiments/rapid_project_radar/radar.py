"""Free-first public signal radar. Discovery and draft scaffolding only."""
# CI verification trigger: behavior unchanged; validates main-branch push workflow.
# Incubator integration check: no change to feed parsing or ranking.
# Topic-specific incubator validation trigger; runtime behavior unchanged.
import argparse
import datetime as dt
import hashlib
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

FEEDS = {
    "arxiv_cs_ai": "https://export.arxiv.org/rss/cs.AI",
    "arxiv_cs_cy": "https://export.arxiv.org/rss/cs.CY",
    "w3c_news": "https://www.w3.org/blog/news/feed/",
    "arxiv_cs_cr": "https://export.arxiv.org/rss/cs.CR",
    "arxiv_cs_lg": "https://export.arxiv.org/rss/cs.LG",
    "arxiv_cs_dc": "https://export.arxiv.org/rss/cs.DC",
    "arxiv_cs_hc": "https://export.arxiv.org/rss/cs.HC",
    "hacker_news": "https://hnrss.org/newest?q=AI",
    "github_blog": "https://github.blog/feed/",
    "cloudflare_blog": "https://blog.cloudflare.com/rss/",
    "google_research": "https://research.google/blog/rss/",
    "openai_news": "https://openai.com/news/rss.xml",
    # Experimental third-party public X profile feeds (FxEmbed, NOT X's official API).
    # Best-effort only: feeds may fail, lag, or become unavailable without notice.
    "x_nasa": "https://fxtwitter.com/NASA/feed.xml?count=20",
    "x_google_deepmind": "https://fxtwitter.com/GoogleDeepMind/feed.xml?count=20",
    "x_huggingface": "https://fxtwitter.com/huggingface/feed.xml?count=20",
    "x_arxiv": "https://fxtwitter.com/arxiv/feed.xml?count=20",
    # GDELT's public DOC 2.0 search endpoint in RSS mode. No credentials.
    # Best-effort search: neither exhaustive nor guaranteed real-time.
    "gdelt_ai_research": "https://api.gdeltproject.org/api/v2/doc/doc?query=%22artificial%20intelligence%22%20research&mode=artlist&maxrecords=30&timespan=1d&format=rss",
    "gdelt_science_discovery": "https://api.gdeltproject.org/api/v2/doc/doc?query=%22scientific%20discovery%22&mode=artlist&maxrecords=30&timespan=1d&format=rss",
    # Original research and journal feeds complement fast social/news signals.
    "arxiv_quant_ph": "https://rss.arxiv.org/rss/quant-ph",
    "arxiv_cs_ro": "https://rss.arxiv.org/rss/cs.RO",
    "nature_research": "https://www.nature.com/nature.rss",
}
KEYWORDS = {
    "agent_security": ("agent", "permission", "authorization", "prompt injection", "consent"),
    "provenance": ("provenance", "citation", "evidence", "verification", "authenticity"),
    "web_protocols": ("protocol", "webmcp", "browser", "interoperability", "web agent"),
    "privacy": ("privacy", "data minimization", "personal data", "local model"),
}
MAX_BYTES = 1_000_000

def score(title, description):
    text=(title+" "+description).lower()
    matches={topic:[k for k in words if k in text] for topic,words in KEYWORDS.items()}
    matches={k:v for k,v in matches.items() if v}
    return {"score":sum(len(v) for v in matches.values()),"topics":matches}

def parse_feed(xml, source):
    root=ET.fromstring(xml)
    entries=[]
    for item in root.findall(".//item"):
        title=" ".join((item.findtext("title") or "").split())
        link=(item.findtext("link") or "").strip()
        desc=" ".join(re.sub(r"<[^>]+>"," ",item.findtext("description") or "").split())
        if not link.startswith("https://") or not title:
            continue
        metrics=score(title,desc)
        entries.append({"id":hashlib.sha256(link.encode()).hexdigest()[:16],
                        "source":source,"title":title[:300],"url":link,
                        "published":item.findtext("pubDate"),
                        "description":desc[:2500],
                        "signal":metrics,"validated_market_need":False,
                        "novelty_verified":False})
    return entries

def fetch(url):
    req=urllib.request.Request(url,headers={"User-Agent":"ResearchRadar/0.1 (public RSS; no credentials)"})
    with urllib.request.urlopen(req,timeout=12) as resp:
        data=resp.read(MAX_BYTES+1)
        if len(data)>MAX_BYTES:
            raise ValueError("feed too large")
        return data

def run(feeds=FEEDS, fetcher=fetch):
    results=[]; errors=[]
    for name,url in feeds.items():
        try:
            results.extend(parse_feed(fetcher(url),name))
        except (OSError,ValueError,ET.ParseError) as exc:
            errors.append({"feed":name,"error":type(exc).__name__})
    dedup={x["id"]:x for x in results}
    items=sorted(dedup.values(),key=lambda x:(-x["signal"]["score"],x["id"]))
    return {"generated_at_utc":dt.datetime.now(dt.timezone.utc).isoformat(),
            "status":"unfiltered_source_discovery","signals":items[:40],
            "feed_errors":errors,"successful_feeds":len(feeds)-len(errors),
            "autonomous_code_generation":False}

def write_report(path, report):
    dest=Path(path)
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",default="radar-report.json")
    args=parser.parse_args()
    result=run()
    write_report(args.output,result)
    print(f"Signals: {len(result['signals'])}; feeds: {result['successful_feeds']}/{len(FEEDS)}")
    if result["successful_feeds"]==0:
        raise SystemExit("All feeds failed")
