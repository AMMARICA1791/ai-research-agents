"""Offline regression tests; no remote inference and no invented human gold."""
import hashlib

import pytest

from research.ai_entailment_triage import score_against_human, suggest
from research.evidence_claims import canonical_digest


def data(tmp_path, reviewed=True):
    paper = tmp_path / "study.txt"
    paper.write_text("No statistically significant difference was observed.", encoding="utf-8")
    ledger = {"schema_version": 1, "entries": [{"doi": "10.1234/study"}]}
    ledger["ledger_sha256"] = canonical_digest(ledger)
    return {
        "schema_version": 1, "ledger": ledger,
        "source_texts": [{"doi": "10.1234/study", "file": "study.txt",
                          "sha256": hashlib.sha256(paper.read_bytes()).hexdigest()}],
        "claims": [{"id": "c1", "proposition": "The intervention improves outcomes",
                    "scope": "Adults", "review_status": "unreviewed",
                    "evidence": [{"doi": "10.1234/study", "locator": "Results",
                                  "stance": "supports",
                                  "quote": "No statistically significant difference was observed."}]}],
        "relationship_reviews": [{
            "claim_id": "c1", "doi": "10.1234/study", "locator": "Results",
            "review_status": "reviewed", "relation": "insufficient",
            "rationale": "A null statistical result cannot establish benefit.",
            "reviewer": "reviewer-1",
        }] if reviewed else [],
    }


def model(_claim, _link):
    return {"relation": "insufficient", "rationale": "The quote does not demonstrate efficacy."}


def test_model_suggestions_are_not_scientific_proof(tmp_path):
    result = suggest(data(tmp_path), tmp_path, model)
    assert result["suggestions"][0]["relation"] == "insufficient"
    assert result["scientific_support_verified"] is False


def test_accuracy_scored_only_against_reviewed_labels(tmp_path):
    payload = data(tmp_path)
    predictions = suggest(payload, tmp_path, model)
    result = score_against_human(payload, tmp_path, predictions)
    assert result["reviewed_count"] == 1
    assert result["accuracy"] == 1.0
    assert result["scientific_validity_established"] is False


def test_no_human_gold_means_no_accuracy(tmp_path):
    payload = data(tmp_path, reviewed=False)
    result = score_against_human(payload, tmp_path, suggest(payload, tmp_path, model))
    assert result["reviewed_count"] == 0
    assert result["accuracy"] is None


def test_wrong_prediction_counted(tmp_path):
    payload = data(tmp_path)
    predictions = suggest(payload, tmp_path,
                          lambda _c, _l: {"relation": "supports", "rationale": "Proposed."})
    result = score_against_human(payload, tmp_path, predictions)
    assert result["accuracy"] == 0.0


def test_missing_quote_abstains_without_model_call(tmp_path):
    payload = data(tmp_path)
    payload["claims"][0]["evidence"][0]["quote"] = "A quote that is not present"
    result = suggest(payload, tmp_path, lambda *_: pytest.fail("model must not be called"))
    assert result["suggestions"][0]["relation"] is None
    assert result["suggestions"][0]["status"] == "abstained_quote_mismatch"


def test_invalid_model_output_fails_closed(tmp_path):
    with pytest.raises(ValueError, match="Invalid model prediction"):
        suggest(data(tmp_path), tmp_path, lambda *_: {"relation": "proven", "rationale": "No"})


def test_unknown_predictions_rejected(tmp_path):
    payload = data(tmp_path)
    predictions = suggest(payload, tmp_path, model)
    predictions["suggestions"][0]["doi"] = "10.1234/unknown"
    with pytest.raises(ValueError, match="unknown evidence"):
        score_against_human(payload, tmp_path, predictions)
