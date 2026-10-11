"""Offline integration tests for metadata evidence and durable memory."""
import hashlib

import pytest

from research.integration_pipeline import integrate


def report(title="First title", stamp="2026-10-11T12:00:00+00:00"):
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


def test_end_to_end_reproducible_replay(tmp_path):
    db = tmp_path / "memory.sqlite3"
    first = integrate(report(), db)
    again = integrate(report(), db)
    assert first["stored_new_snapshot"] is True
    assert again["stored_new_snapshot"] is False
    assert first["ledger_sha256"] == again["ledger_sha256"]
    assert first["observations"] == again["observations"]
    assert first["observations"][0]["historical_observations_returned"] == 1
    assert first["observations"][0]["scientific_claim_verified"] is False


def test_detects_metadata_revision_without_scientific_claim(tmp_path):
    db = tmp_path / "memory.sqlite3"
    integrate(report(), db)
    revised = integrate(report("Updated title", "2026-10-11T13:00:00+00:00"), db)
    assert len(revised["observations"][0]["metadata_changes"]) == 1
    assert revised["status"] == "integrated_unreviewed_bibliographic_metadata"


def test_rejects_invalid_question_without_writing(tmp_path):
    db = tmp_path / "memory.sqlite3"
    bad = report()
    bad["research_question"] = "secret@example.com"
    with pytest.raises(ValueError):
        integrate(bad, db)
    assert not db.exists()


def test_rejects_tampered_provenance(tmp_path):
    db = tmp_path / "memory.sqlite3"
    bad = report()
    bad["source"]["response_sha256"] = "corrupted"
    with pytest.raises(ValueError):
        integrate(bad, db)
    assert not db.exists()


def test_empty_inventory_is_reportable(tmp_path):
    empty = report()
    empty["candidate_count"] = 0
    empty["records"] = []
    result = integrate(empty, tmp_path / "memory.sqlite3")
    assert result["observations"] == []
