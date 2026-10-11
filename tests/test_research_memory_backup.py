"""Offline verified backup/restore regression tests."""
import hashlib
import json
import sqlite3

import pytest

from research.memory_backup import backup, restore
from research.persistent_memory import history, remember_report


def report():
    stamp = "2026-10-11T12:00:00+00:00"
    return {
        "status": "public_scholarly_metadata_candidates",
        "research_question": "open weight model evaluation",
        "candidate_count": 1,
        "source": {"provider": "Crossref",
                   "endpoint": "https://api.crossref.org/works?rows=1",
                   "retrieved_at_utc": stamp,
                   "response_sha256": hashlib.sha256(b"source").hexdigest()},
        "records": [{"doi": "10.1234/example", "doi_url": "https://doi.org/10.1234/example",
                     "title": "Sample research", "year": 2026}],
    }


def test_round_trip_and_reopen(tmp_path):
    source, snapshot, recovered = (tmp_path / name for name in ("source.db", "backup.db", "restored.db"))
    original = remember_report(source, report())
    manifest = backup(source, snapshot)
    assert manifest["snapshots"] == 1
    assert manifest["entries"] == 1
    result = restore(snapshot, recovered)
    assert result["restored"] is True
    assert history(recovered, "10.1234/example")[0]["ledger_sha256"] == original["ledger_sha256"]
    with sqlite3.connect(recovered) as conn:
        assert conn.execute("PRAGMA integrity_check").fetchone()[0] == "ok"


def test_tampered_backup_rejected_without_output(tmp_path):
    source, snapshot, recovered = (tmp_path / name for name in ("source.db", "backup.db", "restored.db"))
    remember_report(source, report())
    backup(source, snapshot)
    with snapshot.open("ab") as stream:
        stream.write(b"tampered")
    with pytest.raises(ValueError, match="manifest mismatch"):
        restore(snapshot, recovered)
    assert not recovered.exists()


def test_tampered_manifest_rejected(tmp_path):
    source, snapshot, recovered = (tmp_path / name for name in ("source.db", "backup.db", "restored.db"))
    remember_report(source, report())
    backup(source, snapshot)
    manifest_path = tmp_path / "backup.db.manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["entries"] = 999
    manifest_path.write_text(json.dumps(manifest))
    with pytest.raises(ValueError, match="record counts"):
        restore(snapshot, recovered)
    assert not recovered.exists()


def test_restore_refuses_existing_database(tmp_path):
    source, snapshot, recovered = (tmp_path / name for name in ("source.db", "backup.db", "restored.db"))
    remember_report(source, report())
    backup(source, snapshot)
    recovered.write_bytes(b"existing must not be overwritten")
    with pytest.raises(ValueError, match="destination exists"):
        restore(snapshot, recovered)
    assert recovered.read_bytes() == b"existing must not be overwritten"


def test_backup_refuses_invalid_source(tmp_path):
    source, snapshot = tmp_path / "broken.db", tmp_path / "backup.db"
    source.write_bytes(b"broken")
    with pytest.raises(sqlite3.DatabaseError):
        backup(source, snapshot)
    assert not snapshot.exists()


def test_backup_refuses_duplicate_destination(tmp_path):
    source, snapshot = tmp_path / "source.db", tmp_path / "backup.db"
    remember_report(source, report())
    backup(source, snapshot)
    with pytest.raises(FileExistsError):
        backup(source, snapshot)
