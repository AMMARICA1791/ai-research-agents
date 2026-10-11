"""Deterministic, source-linked ledger for bounded public research metadata.

No network access, scientific judgment, or model inference.
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

SHA256 = re.compile(r"[0-9a-f]{64}\Z")
DOI = re.compile(r"10\.[0-9]{4,9}/[^\s]{1,160}\Z")


def build_ledger(report: dict) -> dict:
    """Validate a metadata inventory and create a versioned evidence ledger."""
    if not isinstance(report, dict) or report.get("status") != "public_scholarly_metadata_candidates":
        raise ValueError("Expected a public scholarly metadata inventory")
    source = report.get("source")
    if not isinstance(source, dict) or source.get("provider") != "Crossref":
        raise ValueError("Missing trusted provider provenance")
    digest = source.get("response_sha256")
    timestamp = source.get("retrieved_at_utc")
    endpoint = source.get("endpoint")
    if not isinstance(digest, str) or not SHA256.fullmatch(digest):
        raise ValueError("Missing or invalid source response digest")
    if not isinstance(timestamp, str):
        raise ValueError("Missing UTC retrieval time")
    try:
        dt = datetime.fromisoformat(timestamp)
    except ValueError as exc:
        raise ValueError("Invalid retrieval time") from exc
    if dt.utcoffset() is None or dt.utcoffset().total_seconds() != 0:
        raise ValueError("Retrieval time must be UTC")
    if not isinstance(endpoint, str) or not endpoint.startswith("https://api.crossref.org/works?"):
        raise ValueError("Unexpected source endpoint")
    records = report.get("records")
    if not isinstance(records, list) or len(records) > 8:
        raise ValueError("Invalid bounded record list")
    if report.get("candidate_count") != len(records):
        raise ValueError("Candidate count mismatch")
    entries = []
    seen = set()
    for record in records:
        if not isinstance(record, dict):
            raise ValueError("Invalid record")
        doi = record.get("doi")
        title = record.get("title")
        url = record.get("doi_url")
        if (not isinstance(doi, str) or not DOI.fullmatch(doi)
                or not isinstance(title, str) or not title.strip()
                or not isinstance(url, str) or url != "https://doi.org/" + quote(doi, safe="/-._~")):
            raise ValueError("Incomplete record")
        year = record.get("year")
        if year is not None and (type(year) is not int or not 1600 <= year <= 2200):
            raise ValueError("Invalid publication year")
        if doi in seen:
            raise ValueError("Duplicate DOI in ledger")
        seen.add(doi)
        entries.append({
            "doi": doi, "doi_url": url, "title": title,
            "year": record.get("year"),
            "source_response_sha256": digest,
            "evidence_level": "unreviewed_bibliographic_metadata",
            "scientific_claim_verified": False,
        })
    ledger = {
        "schema_version": 1,
        "status": "unreviewed_source_linked_evidence",
        "research_question": report.get("research_question"),
        "source": {"provider": "Crossref", "endpoint": endpoint,
                   "retrieved_at_utc": timestamp, "response_sha256": digest},
        "entries": entries,
        "limitations": ["Bibliographic metadata only; no full-text review",
                        "No independent scientific verification or model inference",
                        "Revalidate against original provider before making research claims"],
    }
    canonical = json.dumps(ledger, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    ledger["ledger_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return ledger


def write_ledger(report_path: str, output_path: str) -> dict:
    report = json.loads(Path(report_path).read_text(encoding="utf-8"))
    ledger = build_ledger(report)
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return ledger


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    result = write_ledger(args.input, args.output)
    print(json.dumps({"entries": len(result["entries"]), "ledger_sha256": result["ledger_sha256"]}))
