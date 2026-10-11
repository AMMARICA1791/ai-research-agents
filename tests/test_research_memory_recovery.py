"""Recovery and integrity tests for the existing research evidence SQLite store."""
import hashlib
import sqlite3

import pytest

from research.integration_pipeline import integrate
from research.persistent_memory import history, open_memory


def report():
    title = "First title"
    stamp = "2026-10-11T12:00:00+00:00"
    return {
        "status": "public_scholarly_metadata_candidates",
        "research_question": "open weight model evaluation",
        "candidate_count": 1,
        "source": {
            "provider": "Crossref",
            "endpoint": "https://api.crossref.org/works?rows=1",
            "retrieved_at_utc": stamp,
            "response_sha256": hashlib.sha256((title + stamp).encode()).hexdigest(),
        },
        "records": [{"doi": "10.1234/example", "doi_url": "https://doi.org/10.1234/example",
                     "title": title, "year": 2026}],
    }


def test_reopen_after_successful_commit(tmp_path):
    db = tmp_path / "evidence.sqlite3"
    result = integrate(report(), db)
    with sqlite3.connect(db) as conn:
        assert conn.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
        assert conn.execute("SELECT count(*) FROM evidence_snapshots").fetchone()[0] == 1
    assert history(db, "10.1234/example")[0]["ledger_sha256"] == result["ledger_sha256"]


def test_transaction_rolls_back_when_entry_insert_fails(tmp_path):
    db = tmp_path / "evidence.sqlite3"
    with open_memory(db) as conn:
        conn.execute("""
            CREATE TRIGGER reject_entry BEFORE INSERT ON evidence_entries
            BEGIN SELECT RAISE(ABORT, 'simulated interrupted entry write'); END;
        """)
        conn.commit()
    with pytest.raises(sqlite3.IntegrityError, match="simulated interrupted"):
        integrate(report(), db)
    with sqlite3.connect(db) as conn:
        assert conn.execute("SELECT count(*) FROM evidence_snapshots").fetchone()[0] == 0
        assert conn.execute("SELECT count(*) FROM evidence_entries").fetchone()[0] == 0
        assert conn.execute("PRAGMA integrity_check").fetchone()[0] == "ok"


def test_corrupt_database_fails_closed_without_replacing_it(tmp_path):
    db = tmp_path / "evidence.sqlite3"
    original = b"not a valid sqlite database\x00broken"
    db.write_bytes(original)
    with pytest.raises(sqlite3.DatabaseError):
        integrate(report(), db)
    assert db.read_bytes() == original


def test_foreign_key_enforced(tmp_path):
    db = tmp_path / "evidence.sqlite3"
    with open_memory(db) as conn:
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(
                "INSERT INTO evidence_entries VALUES (?, ?, ?, ?)",
                ("0" * 64, "10.1234/missing", "Missing", 2026),
            )


def test_snapshot_replay_does_not_duplicate_entries(tmp_path):
    db = tmp_path / "evidence.sqlite3"
    for _ in range(3):
        integrate(report(), db)
    with sqlite3.connect(db) as conn:
        assert conn.execute("SELECT count(*) FROM evidence_snapshots").fetchone()[0] == 1
        assert conn.execute("SELECT count(*) FROM evidence_entries").fetchone()[0] == 1
