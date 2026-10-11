"""Deterministic tests: source linkage, conflict candidates, metadata differences."""
import copy

import pytest

from research.evidence_claims import assess_conflicts, canonical_digest


def example():
    ledger = {
        "schema_version": 1,
        "entries": [
            {"doi": "10.1234/one", "title": "Paper One"},
            {"doi": "10.1234/two", "title": "Paper Two"},
        ],
    }
    ledger["ledger_sha256"] = canonical_digest(ledger)
    return {"schema_version": 1, "ledger": ledger, "claims": [
        {"id": "a", "proposition": "Treatment X improves outcome Y",
         "scope": "Adults; 12-week follow-up", "review_status": "unreviewed",
         "evidence": [{"doi": "10.1234/one", "stance": "supports", "locator": "Table 2"}]},
        {"id": "b", "proposition": "Treatment X improves outcome Y",
         "scope": "Adults; 12-week follow-up", "review_status": "unreviewed",
         "evidence": [{"doi": "10.1234/two", "stance": "refutes", "locator": "Figure 3"}]},
    ]}


def test_opposing_stances_flagged_not_verified():
    result = assess_conflicts(example())
    assert result["candidate_count"] == 1
    assert result["candidates"][0]["scientific_contradiction_verified"] is False


def test_metadata_title_difference_not_a_conflict():
    data = example()
    data["ledger"]["entries"][1]["title"] = "Revised bibliographic title"
    data["ledger"]["ledger_sha256"] = canonical_digest({
        k: v for k, v in data["ledger"].items() if k != "ledger_sha256"
    })
    data["claims"][1]["evidence"][0]["stance"] = "supports"
    assert assess_conflicts(data)["candidate_count"] == 0


def test_different_scope_not_conflated():
    data = example()
    data["claims"][1]["scope"] = "Children; 2-week follow-up"
    assert assess_conflicts(data)["candidate_count"] == 0


def test_unknown_doi_fails_closed():
    data = example()
    data["claims"][1]["evidence"][0]["doi"] = "10.1234/unknown"
    with pytest.raises(ValueError, match="Unknown source"):
        assess_conflicts(data)


def test_modified_ledger_fails_closed():
    data = example()
    data["ledger"]["entries"][0]["title"] = "tampered"
    with pytest.raises(ValueError, match="digest mismatch"):
        assess_conflicts(data)


def test_missing_locator_fails_closed():
    data = example()
    data["claims"][0]["evidence"][0]["locator"] = ""
    with pytest.raises(ValueError, match="locator"):
        assess_conflicts(data)


def test_duplicate_claim_ids_rejected():
    data = example()
    data["claims"][1]["id"] = "a"
    with pytest.raises(ValueError, match="Duplicate"):
        assess_conflicts(data)
