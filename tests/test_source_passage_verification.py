"""Offline source quote verification regression tests."""
import hashlib

import pytest

from research.evidence_claims import canonical_digest
from research.source_passage_verification import verify_passages


def fixture(tmp_path):
    source = tmp_path / "paper.txt"
    source.write_text("Methods. Sample size was 30. Results were inconclusive.", encoding="utf-8")
    ledger = {"schema_version": 1, "entries": [{"doi": "10.1234/paper", "title": "Study"}]}
    ledger["ledger_sha256"] = canonical_digest(ledger)
    payload = {
        "schema_version": 1,
        "ledger": ledger,
        "source_texts": [{
            "doi": "10.1234/paper",
            "file": "paper.txt",
            "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        }],
        "claims": [{
            "id": "c1",
            "proposition": "Treatment works",
            "scope": "Adults",
            "review_status": "unreviewed",
            "evidence": [{
                "doi": "10.1234/paper",
                "stance": "supports",
                "locator": "Results",
                "quote": "Results were inconclusive.",
            }],
        }],
    }
    return payload, source


def test_exact_quote_present_does_not_verify_support(tmp_path):
    payload, _ = fixture(tmp_path)
    result = verify_passages(payload, tmp_path)
    assert result["exact_match_count"] == 1
    assert result["scientific_support_verified"] is False
    assert result["source_authenticity_verified"] is False


def test_missing_quote_is_reported_not_invented(tmp_path):
    payload, _ = fixture(tmp_path)
    payload["claims"][0]["evidence"][0]["quote"] = "Results were conclusive."
    result = verify_passages(payload, tmp_path)
    assert result["exact_match_count"] == 0
    assert result["findings"][0]["quote_exact_match"] is False


def test_modified_source_fails_digest(tmp_path):
    payload, source = fixture(tmp_path)
    source.write_text("Changed after archival", encoding="utf-8")
    with pytest.raises(ValueError, match="digest mismatch"):
        verify_passages(payload, tmp_path)


def test_path_traversal_rejected(tmp_path):
    payload, _ = fixture(tmp_path)
    payload["source_texts"][0]["file"] = "../paper.txt"
    with pytest.raises(ValueError, match="flat"):
        verify_passages(payload, tmp_path)


def test_unknown_source_fails_closed(tmp_path):
    payload, _ = fixture(tmp_path)
    payload["source_texts"] = []
    with pytest.raises(ValueError, match="not in manifest"):
        verify_passages(payload, tmp_path)


def test_missing_quote_fails_closed(tmp_path):
    payload, _ = fixture(tmp_path)
    del payload["claims"][0]["evidence"][0]["quote"]
    with pytest.raises(ValueError, match="exact nonempty quote"):
        verify_passages(payload, tmp_path)
