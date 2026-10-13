import json
from pathlib import Path
import pytest
from research.validate_provisional_review import validate

REVIEW = json.loads(Path("research/provisional_primary_paper_review.json").read_text())

def test_review_schema_is_provisional_and_covers_all_rows():
    assert len(REVIEW["cases"]) == 30
    assert REVIEW["audit_summary"] == {
        "extracted_rows": 30, "unique_excerpt_texts": 22,
        "duplicate_rows": 8, "independent_expert_labels": 0}
    assert REVIEW["scientific_acceptance"] == "NOT_PASSED"
    assert all(len(row["verbatim_sha256"]) == 64 for row in REVIEW["cases"])

def test_validator_rejects_unverified_synthetic_quotes():
    probe = {"cases": [{"source": item["source"],
                        "pdf_page": item["pdf_page"],
                        "ground_truth": "UNLABELED",
                        "verbatim_text": "synthetic text not from original PDF"}
                       for item in REVIEW["cases"]]}
    with pytest.raises(AssertionError, match="excerpt mismatch"):
        validate(REVIEW, probe)
