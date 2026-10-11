"""Regression tests for persistent evidence snapshots; no external services."""
import hashlib

import pytest

from research.persistent_memory import history, remember_report


def sample(title="Example", stamp="2026-10-11T19:00:00+00:00"):
    return {
        "status": "public_scholarly_metadata_candidates",
        "research_question": "small language model evaluation",
        "candidate_count": 1,
        "source": {
            "provider": "Crossref",
            "endpoint": "https://api.crossref.org/works?rows=1",
            "retrieved_at_utc": stamp,
            "response_sha256": hashlib.sha256((title + stamp).encode()).hexdigest(),
        },
        "records": [{
            "doi": "10.1234/example", "doi_url": "https://doi.org/10.1234/example",
            "title": title, "year": 2026,
        }],
    }


def test_persists_after_reopen_and_is_idempotent(tmp_path):
    db = tmp_path / "evidence.sqlite3"
    first = remember_report(db, sample())
    assert first["stored"] is True
    assert remember_report(db, sample()) == {**first, "stored": False}
    found = history(db, "10.1234/example")
    assert len(found) == 1
    assert found[0]["title"] == "Example"
    assert found[0]["ledger_sha256"] == first["ledger_sha256"]
    assert found[0]["scientific_claim_verified"] is False


def test_preserves_two_versions_instead_of_overwriting(tmp_path):
    db = tmp_path / "evidence.sqlite3"
    remember_report(db, sample("Old", "2026-10-10T10:00:00+00:00"))
    remember_report(db, sample("New", "2026-10-11T10:00:00+00:00"))
    assert [r["title"] for r in history(db, "10.1234/example")] == ["New", "Old"]


def test_invalid_source_does_not_write_snapshot(tmp_path):
    db = tmp_path / "evidence.sqlite3"
    bad = sample()
    bad["source"]["response_sha256"] = "not-a-digest"
    with pytest.raises(ValueError):
        remember_report(db, bad)
    assert history(db, "10.1234/example") == []


def test_exact_doi_query_not_sql_expression(tmp_path):
    db = tmp_path / "evidence.sqlite3"
    remember_report(db, sample())
    assert history(db, "10.1234/example' OR 1=1 --") == []
    assert history(db, "10.1234/other") == []


@pytest.mark.parametrize("limit", [0, 101, True, -1])
def test_invalid_history_limit_rejected(tmp_path, limit):
    with pytest.raises(ValueError):
        history(tmp_path / "evidence.sqlite3", "10.1234/example", limit)
