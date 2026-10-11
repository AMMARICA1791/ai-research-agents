"""Tests for conservative evidence-to-claim review workflow."""
import hashlib

import pytest

from research.evidence_claims import canonical_digest
from research.relationship_review import evaluate_relationships


def sample(tmp_path):
    text = tmp_path / "paper.txt"
    text.write_text("The observed effect was not statistically significant.", encoding="utf-8")
    ledger = {"schema_version": 1, "entries": [{"doi": "10.1234/paper"}]}
    ledger["ledger_sha256"] = canonical_digest(ledger)
    data = {
        "schema_version": 1, "ledger": ledger,
        "source_texts": [{"doi": "10.1234/paper", "file": "paper.txt",
                          "sha256": hashlib.sha256(text.read_bytes()).hexdigest()}],
        "claims": [{"id": "claim1", "proposition": "The treatment is effective",
                    "scope": "Adults", "review_status": "unreviewed",
                    "evidence": [{"doi": "10.1234/paper", "locator": "Results",
                                  "stance": "supports",
                                  "quote": "The observed effect was not statistically significant."}]}],
        "relationship_reviews": [],
    }
    return data


def review(relation="insufficient"):
    return {"claim_id": "claim1", "doi": "10.1234/paper", "locator": "Results",
            "review_status": "reviewed", "relation": relation,
            "rationale": "The reported observation alone does not establish the claimed effect.",
            "reviewer": "domain-reviewer-1"}


def test_default_pending_not_auto_support(tmp_path):
    result = evaluate_relationships(sample(tmp_path), tmp_path)
    assert result["pending_count"] == 1
    assert result["links"][0]["relation"] is None
    assert result["scientific_support_verified"] is False


def test_explicit_insufficient_review(tmp_path):
    data = sample(tmp_path)
    data["relationship_reviews"] = [review()]
    result = evaluate_relationships(data, tmp_path)
    assert result["reviewed_count"] == 1
    assert result["links"][0]["relation"] == "insufficient"
    assert result["machine_entailment_verified"] is False


def test_review_cannot_bypass_missing_quote(tmp_path):
    data = sample(tmp_path)
    data["claims"][0]["evidence"][0]["quote"] = "This quotation does not exist."
    data["relationship_reviews"] = [review("supports")]
    with pytest.raises(ValueError, match="unmatched quotation"):
        evaluate_relationships(data, tmp_path)


def test_review_requires_rationale(tmp_path):
    data = sample(tmp_path)
    record = review()
    record["rationale"] = ""
    data["relationship_reviews"] = [record]
    with pytest.raises(ValueError, match="rationale"):
        evaluate_relationships(data, tmp_path)


def test_unknown_evidence_review_rejected(tmp_path):
    data = sample(tmp_path)
    record = review()
    record["doi"] = "10.1234/other"
    data["relationship_reviews"] = [record]
    with pytest.raises(ValueError, match="Unknown"):
        evaluate_relationships(data, tmp_path)


def test_duplicate_reviews_rejected(tmp_path):
    data = sample(tmp_path)
    data["relationship_reviews"] = [review(), review()]
    with pytest.raises(ValueError, match="duplicate"):
        evaluate_relationships(data, tmp_path)


def test_pending_cannot_assert_relation(tmp_path):
    data = sample(tmp_path)
    record = review()
    record["review_status"] = "pending"
    data["relationship_reviews"] = [record]
    with pytest.raises(ValueError, match="Pending"):
        evaluate_relationships(data, tmp_path)
