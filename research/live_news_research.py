"""First runnable live-source research entry point. Standard library only.

Usage: python -m research.live_news_research "https://example.org/article"
Fetches one public HTML page, extracts bounded text and links, and creates a
source-grounded review dossier. It does NOT verify truth or browse social logins.
"""
import argparse
import datetime as dt
import hashlib
import html.parser
import json
import pathlib
import re
import urllib.parse
import urllib.request
import ipaddress
import socket

MAX_BYTES = 600_000
USER_AGENT = "AIResearchAgents/0.1 (research source reader)"

class PageParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.article_parts = []
        self.article_depth = 0
        self.navigation_depth = 0
        self.links = []
        self.title = []
        self.skip = 0
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        if tag in ("main", "article"):
            self.article_depth += 1
        if tag in ("nav", "aside", "footer"):
            self.navigation_depth += 1
        if tag in ("script", "style", "noscript", "svg"):
            self.skip += 1
        if tag == "title":
            self.in_title = True
        if tag == "a":
            href = dict(attrs).get("href")
            if href and len(self.links) < 100:
                self.links.append(href)

    def handle_endtag(self, tag):
        if tag in ("main", "article"):
            self.article_depth = max(0, self.article_depth - 1)
        if tag in ("nav", "aside", "footer"):
            self.navigation_depth = max(0, self.navigation_depth - 1)
        if tag in ("script", "style", "noscript", "svg"):
            self.skip = max(0, self.skip - 1)
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.skip or self.navigation_depth:
            return
        value = " ".join(data.split())
        if value:
            if self.in_title:
                self.title.append(value)
            if len(self.parts) < 3000:
                self.parts.append(value)
            if self.article_depth and len(self.article_parts) < 3000:
                self.article_parts.append(value)

def extracted_text(page):
    """Prefer actual HTML main/article text over boilerplate site chrome."""
    focused = " ".join(page.article_parts)
    selected = focused if len(focused) >= 150 else " ".join(page.parts)
    return re.sub(r"\s+", " ", selected)[:20000]

def safe_url(url):
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("Only public HTTPS URLs without credentials are supported")
    host = parsed.hostname
    for item in socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM):
        ip = ipaddress.ip_address(item[4][0])
        if not ip.is_global:
            raise ValueError("Private or non-public addresses are blocked")
    return url

class SafeRedirect(urllib.request.HTTPRedirectHandler):
    """Permit bounded public HTTPS redirects, validating every destination."""
    max_redirections = 4
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        safe_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError("Redirects are disabled to protect against private-network access")

def collect(url):
    safe_url(url)
    opener = urllib.request.build_opener(SafeRedirect)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html"})
    with opener.open(req, timeout=15) as response:
        final_url = response.geturl()
        safe_url(final_url)
        ctype = response.headers.get_content_type()
        if ctype != "text/html":
            raise ValueError("Source is not an HTML document")
        raw = response.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise ValueError("Source exceeds size limit")
        charset = response.headers.get_content_charset() or "utf-8"
    page = PageParser()
    page.feed(raw.decode(charset, errors="replace"))
    text = extracted_text(page)
    links = []
    for href in page.links:
        target = urllib.parse.urljoin(final_url, href)
        p = urllib.parse.urlsplit(target)
        if p.scheme == "https" and p.hostname and target not in links:
            links.append(target)
    return {"url": final_url, "requested_url": url, "title": " ".join(page.title)[:250], "text": text,
            "outbound_links": links[:30], "sha256": hashlib.sha256(raw).hexdigest()}

def dossier(source, question):
    excerpt = source["text"][:1200]
    return {
        "question": question,
        "retrieved_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "source": {"url": source["url"], "title": source["title"],
                   "sha256": source["sha256"]},
        "source_excerpt": excerpt,
        "source_links": source["outbound_links"],
        "review": {
            "status": "SOURCE_COLLECTED_NOT_INDEPENDENTLY_VERIFIED",
            "summary": "The linked page was retrieved. Its claims have not been independently corroborated.",
            "follow_up_questions": [
                "Who published the original announcement or study?",
                "Which measurable evidence supports the headline?",
                "Are there independent evaluations or contradictory sources?"
            ],
            "limitations": [
                "One page only; no independent cross-source verification",
                "HTML text extraction may include navigation or omit dynamic content",
                "No LLM inference or ongoing conversational memory",
                "No authenticated social-media content"
            ]
        }
    }

def main():
    p = argparse.ArgumentParser(description="Retrieve a public news page and produce an evidence dossier")
    p.add_argument("url", help="Public HTTPS news/article URL")
    p.add_argument("--question", default="What does this source actually establish?")
    p.add_argument("--output", default="research_output/live_news_dossier.json")
    args = p.parse_args()
    report = dossier(collect(args.url), args.question)
    target = pathlib.Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("SOURCE_COLLECTED_NOT_VERIFIED", str(target))

if __name__ == "__main__":
    main()
