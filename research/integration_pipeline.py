"""One bounded research metadata-to-memory-to-report integration path.

No external code execution, model claims, or scientific conclusions.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from research.evidence_ledger import build_ledger
from research.persistent_memory import history, remember_report
from research.scholarly_discovery import discover, validate_question


def _digest(value: dict) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def integrate(report: dict, database_path: str | Path) -> dict:
    """Validate, persist and independently retrieve every candidate's history."""
    ledger = build_ledger(report)
    if not isinstance(ledger["research_question"], str):
        raise ValueError("Missing research question")
    validate_question(ledger["research_question"])
    saved = remember_report(database_path, report)
    if saved["ledger_sha256"] != ledger["ledger_sha256"]:
        raise ValueError("Persisted evidence identifier differs")
    observations = []
    for item in ledger["entries"]:
        versions = history(database_path, item["doi"], limit=100)
        current = next((v for v in versions if v["ledger_sha256"] == ledger["ledger_sha256"]), None)
        if current is None or current["title"] != item["title"] or current["year"] != item["year"]:
            raise ValueError("Persisted evidence cannot be reproduced")
        # A difference is a metadata change, NOT a scientific contradiction.
        changed = [
            {"ledger_sha256": v["ledger_sha256"], "retrieved_at_utc": v["retrieved_at_utc"]}
            for v in versions if v["ledger_sha256"] != ledger["ledger_sha256"]
            and (v["title"] != current["title"] or v["year"] != current["year"])
        ]
        observations.append({
            "doi": item["doi"], "doi_url": item["doi_url"],
            "title": item["title"], "year": item["year"],
            "ledger_sha256": ledger["ledger_sha256"],
            "historical_observations_returned": len(versions),
            "metadata_changes": changed,
            "scientific_claim_verified": False,
        })
    result = {
        "schema_version": 1,
        "status": "integrated_unreviewed_bibliographic_metadata",
        "research_question": ledger["research_question"],
        "source": ledger["source"],
        "ledger_sha256": ledger["ledger_sha256"],
        "stored_new_snapshot": saved["stored"],
        "observations": observations,
        "limitations": [
            "Metadata only; no full papers or scientific claims reviewed",
            "Differences in titles/years are metadata changes, not scientific contradictions",
            "History is bounded to 100 records per DOI; this is not exhaustive for larger databases",
            "Local SQLite only; no automatic cross-run or cross-device synchronization",
        ],
    }
    result["report_sha256"] = _digest(result)
    return result


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Research metadata integration, no paid model API")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--input", help="Existing scholarly discovery JSON report (offline replay)")
    group.add_argument("--question", help="Public Crossref topic (requires network)")
    parser.add_argument("--max-results", type=int, default=5)
    parser.add_argument("--db", default="results/research-memory.sqlite3")
    parser.add_argument("--output", default="results/research-integration/report.json")
    args = parser.parse_args(argv)
    if args.input:
        report = json.loads(Path(args.input).read_text(encoding="utf-8"))
    else:
        report = discover(args.question, max_results=args.max_results)
    result = integrate(report, args.db)
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "count": len(result["observations"]),
                      "report_sha256": result["report_sha256"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
