"""Bounded, no-key scholarly METADATA discovery from public Crossref records.

An evidence inventory, not an AI research agent, a literature review, or an
evaluation of a paper's scientific claims. Never fetches or executes paper code.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode, quote
from urllib.request import HTTPRedirectHandler, Request, build_opener

API = "https://api.crossref.org/works"
MAX_RESPONSE_BYTES = 400_000
MAX_WORKS = 8
DOI_RE = re.compile(r"10\.[0-9]{4,9}/[^\s\x00-\x1f\x7f]{1,160}\Z", re.IGNORECASE)


class _NeverRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError("Scholarly provider redirects are not permitted")


def _safe_text(value: object, length: int) -> str:
    if not isinstance(value, str):
        return ""
    value = unicodedata.normalize("NFC", value).strip()
    if len(value) > length or not value or any(not ch.isprintable() for ch in value):
        return ""
    return value


def validate_question(question: str) -> str:
    question = _safe_text(question, 120)
    if (len(question) < 8 or "://" in question or "@" in question
            or any(ch in question for ch in "<>{}[]\\$") or chr(96) in question
            or not any(ch.isalpha() for ch in question)):
        raise ValueError("Use an 8–120-character public research topic; no URLs, code, credentials or emails")
    return question


def _year(item: dict) -> int | None:
    for key in ("published", "published-print", "published-online", "issued"):
        value = item.get(key)
        if not isinstance(value, dict):
            continue
        parts = value.get("date-parts")
        if (isinstance(parts, list) and parts and isinstance(parts[0], list)
                and parts[0] and type(parts[0][0]) is int
                and 1600 <= parts[0][0] <= 2200):
            return parts[0][0]
    return None


def _entry(item: object) -> dict | None:
    if not isinstance(item, dict):
        return None
    doi = _safe_text(item.get("DOI"), 180)
    if not DOI_RE.fullmatch(doi):
        return None
    titles = item.get("title")
    if not isinstance(titles, list) or not titles:
        return None
    title = _safe_text(titles[0], 260)
    if not title:
        return None
    container = item.get("container-title")
    venue = (_safe_text(container[0], 150) if isinstance(container, list) and container
             else "")
    record_type = _safe_text(item.get("type"), 60)
    return {
        "doi": doi.lower(),
        "doi_url": "https://doi.org/" + quote(doi, safe="/-._~"),
        "title": title,
        "year": _year(item),
        "venue": venue or None,
        "publication_type": record_type or "unknown",
        "evidence_status": "bibliographic_metadata_only",
        "abstract_or_full_text_reviewed": False,
    }


def normalize_crossref(
    payload: bytes, *, question: str, source_url: str,
    max_results: int, retrieved_at: str,
) -> dict:
    if type(payload) is not bytes or len(payload) > MAX_RESPONSE_BYTES:
        raise ValueError("Crossref payload exceeds inspection limits")
    if not isinstance(source_url, str) or not source_url.startswith(API + "?"):
        raise ValueError("Invalid provenance URL")
    if type(max_results) is not int or not 1 <= max_results <= MAX_WORKS:
        raise ValueError("Invalid research result cap")
    question = validate_question(question)
    try:
        document = json.loads(payload.decode("utf-8"))
        entries = document["message"]["items"]
    except (UnicodeError, ValueError, KeyError, TypeError) as exc:
        raise ValueError("Scholarly provider returned malformed JSON metadata") from exc
    if not isinstance(entries, list) or len(entries) > MAX_WORKS:
        raise ValueError("Scholarly response violates bounded entry limits")
    unique = {}
    invalid = 0
    for item in entries:
        record = _entry(item)
        if record is None:
            invalid += 1
            continue
        unique.setdefault(record["doi"], record)
    return {
        "schema_version": 1,
        "status": "public_scholarly_metadata_candidates",
        "research_question": question,
        "source": {
            "provider": "Crossref",
            "endpoint": source_url,
            "retrieved_at_utc": retrieved_at,
            "response_sha256": hashlib.sha256(payload).hexdigest(),
        },
        "candidate_count": len(unique),
        "invalid_or_incomplete_records": invalid,
        "duplicate_dois": len(entries)-invalid-len(unique),
        "records": list(unique.values())[:max_results],
        "model_inference": False,
        "full_papers_reviewed": False,
        "scientific_claims_verified": False,
        "results_ranked_by": "provider_returned_order_not_quality",
        "limitations": [
            "Crossref is a bibliographic metadata index; a listing does not prove a research claim",
            "Matches can be irrelevant or incomplete; coverage varies across publishers",
            "No abstracts, papers, code, or external files were downloaded or executed",
            "Results change across retrieval dates and Crossref may rate-limit public requests",
            "No comparative model evaluation or independent AI research was carried out",
        ],
    }


def discover(question: str, max_results: int = 5) -> dict:
    question = validate_question(question)
    if type(max_results) is not int or not 1 <= max_results <= MAX_WORKS:
        raise ValueError("max_results must be an integer between 1 and 8")
    url = API + "?" + urlencode({
        "query.bibliographic": question,
        "rows": max_results,
        "select": "DOI,title,published,type,container-title",
    })
    request = Request(url, headers={
        "Accept": "application/json",
        "User-Agent": "AIResearchAgents-EvidenceFirst/0.1 (public metadata inventory)",
    })
    try:
        with build_opener(_NeverRedirect()).open(request, timeout=20) as response:
            if response.status != 200:
                raise ValueError(f"Scholarly provider returned HTTP {response.status}")
            data = response.read(MAX_RESPONSE_BYTES + 1)
    except ValueError:
        raise
    except (OSError, TimeoutError) as exc:
        raise ValueError("Scholarly metadata request failed; no offline results substituted") from exc
    if len(data) > MAX_RESPONSE_BYTES:
        raise ValueError("Scholarly metadata response too large")
    return normalize_crossref(
        data, question=question, source_url=url, max_results=max_results,
        retrieved_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
    )


def _md(value: str) -> str:
    """Escape arbitrary source titles in generated GitHub Markdown."""
    result = html.escape(value, quote=True)
    for char in (chr(92), "[", "]", "(", ")", "*", "_", "#", "|"):
        result = result.replace(char, chr(92) + char)
    return result


def summary_md(report: dict) -> str:
    lines = [
        "# Research explorer — public scholarly metadata", "",
        "**Metadata retrieval only: not a literature review or scientific conclusion.**", "",
        f"- Research topic: {_md(report['research_question'])}",
        "- Provider: Crossref",
        f"- Retrieved (UTC): {report['source']['retrieved_at_utc']}",
        f"- Metadata candidates: {report['candidate_count']}",
        f"- Invalid or incomplete records: {report['invalid_or_incomplete_records']}",
        f"- Response SHA-256: {report['source']['response_sha256']}",
        "", "## Bibliographic candidates", "",
    ]
    if not report["records"]:
        lines.append("No complete candidate records returned. This is **not** proof of absence.")
    for item in report["records"]:
        lines.append(
            f"- {_md(item['title'])} ({item['year'] or 'year not reported'}) "
            f"— [DOI record]({item['doi_url']}) — *metadata only*"
        )
    lines += [
        "", "### Uncertainty",
        "These records are unreviewed suggestions from a live index. "
        "No abstracts, full papers, or model results were verified. "
        "Crossref return order is not research quality.",
    ]
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Discover public research metadata without paid LLM keys")
    parser.add_argument("--question", required=True, help="Non-sensitive research topic, not a secret")
    parser.add_argument("--max-results", type=int, default=5)
    parser.add_argument("--output", default="results/research-explorer/records.json")
    parser.add_argument("--summary", default="results/research-explorer/SUMMARY.md")
    args = parser.parse_args(argv)
    try:
        report = discover(args.question, args.max_results)
    except ValueError as exc:
        parser.error(str(exc))
    output, summary = Path(args.output), Path(args.summary)
    output.parent.mkdir(parents=True, exist_ok=True)
    summary.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    summary.write_text(summary_md(report), encoding="utf-8")
    print(json.dumps({
        "status": report["status"], "candidates": report["candidate_count"],
        "provider": "Crossref", "full_papers_reviewed": False, "model_inference": False,
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
