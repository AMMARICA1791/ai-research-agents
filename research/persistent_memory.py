"""Local, persistent research evidence memory backed by SQLite.

Stores validated, unreviewed evidence-ledger snapshots. No model inference,
network access, autonomous mutation, or claims of scientific verification.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
from pathlib import Path

from research.evidence_ledger import build_ledger

SCHEMA = """
CREATE TABLE IF NOT EXISTS evidence_snapshots (
    ledger_sha256 TEXT PRIMARY KEY,
    research_question TEXT NOT NULL,
    retrieved_at_utc TEXT NOT NULL,
    response_sha256 TEXT NOT NULL,
    payload_json TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS evidence_entries (
    ledger_sha256 TEXT NOT NULL REFERENCES evidence_snapshots(ledger_sha256),
    doi TEXT NOT NULL,
    title TEXT NOT NULL,
    year INTEGER,
    PRIMARY KEY (ledger_sha256, doi)
);
CREATE INDEX IF NOT EXISTS idx_evidence_doi ON evidence_entries(doi);
"""


def _canonical_digest(ledger: dict) -> str:
    unsigned = {key: value for key, value in ledger.items() if key != "ledger_sha256"}
    canonical = json.dumps(unsigned, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def open_memory(database_path: str | Path) -> sqlite3.Connection:
    path = Path(database_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript(SCHEMA)
    return conn


def remember_report(database_path: str | Path, report: dict) -> dict:
    """Persist one validated immutable snapshot; repeated ingestion is idempotent."""
    ledger = build_ledger(report)
    digest = ledger["ledger_sha256"]
    if digest != _canonical_digest(ledger):
        raise ValueError("Ledger digest mismatch")
    payload = json.dumps(ledger, ensure_ascii=False, sort_keys=True)
    with open_memory(database_path) as conn:
        with conn:
            existing = conn.execute(
                "SELECT payload_json FROM evidence_snapshots WHERE ledger_sha256=?",
                (digest,),
            ).fetchone()
            if existing is not None:
                if json.loads(existing[0]) != ledger:
                    raise ValueError("Stored snapshot conflicts with digest")
                return {"ledger_sha256": digest, "stored": False, "entries": len(ledger["entries"])}
            conn.execute(
                "INSERT INTO evidence_snapshots VALUES (?, ?, ?, ?, ?)",
                (digest, ledger["research_question"], ledger["source"]["retrieved_at_utc"],
                 ledger["source"]["response_sha256"], payload),
            )
            conn.executemany(
                "INSERT INTO evidence_entries VALUES (?, ?, ?, ?)",
                [(digest, item["doi"], item["title"], item["year"]) for item in ledger["entries"]],
            )
    return {"ledger_sha256": digest, "stored": True, "entries": len(ledger["entries"])}


def history(database_path: str | Path, doi: str, limit: int = 20) -> list[dict]:
    """Return historical observations for one exact DOI, newest first."""
    if not isinstance(doi, str) or not doi.startswith("10.") or len(doi) > 180:
        raise ValueError("Expected an exact DOI")
    if type(limit) is not int or not 1 <= limit <= 100:
        raise ValueError("History limit must be 1..100")
    with open_memory(database_path) as conn:
        rows = conn.execute(
            """SELECT s.ledger_sha256, s.retrieved_at_utc, s.response_sha256,
                      e.doi, e.title, e.year
               FROM evidence_entries e
               JOIN evidence_snapshots s ON s.ledger_sha256=e.ledger_sha256
               WHERE e.doi=? ORDER BY s.retrieved_at_utc DESC, s.ledger_sha256 DESC
               LIMIT ?""",
            (doi.lower(), limit),
        ).fetchall()
    return [
        {"ledger_sha256": row[0], "retrieved_at_utc": row[1],
         "source_response_sha256": row[2], "doi": row[3],
         "title": row[4], "year": row[5],
         "scientific_claim_verified": False}
        for row in rows
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Local versioned metadata evidence memory")
    parser.add_argument("--db", default="results/research-memory.sqlite3")
    sub = parser.add_subparsers(dest="action", required=True)
    ingest = sub.add_parser("ingest", help="Ingest a public Crossref discovery report")
    ingest.add_argument("--input", required=True)
    query = sub.add_parser("history", help="Retrieve observations for one DOI")
    query.add_argument("--doi", required=True)
    args = parser.parse_args()
    if args.action == "ingest":
        report = json.loads(Path(args.input).read_text(encoding="utf-8"))
        result = remember_report(args.db, report)
    else:
        result = history(args.db, args.doi)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
