import json
from pathlib import Path
from research.evidence_quality_report import summarize

def test_evidence_quality_uses_unique_excerpts():
    review=json.loads(Path("research/provisional_primary_paper_review.json").read_text())
    r=summarize(review)
    assert r["extracted_rows"] == 30
    assert r["unique_excerpts"] == 22
    assert r["duplicate_rows"] == 8
    assert r["provisional_directly_stated"] == 14
    assert r["provisional_context_required"] == 6
    assert r["provisional_not_evidence"] == 2
    assert r["excluded_case_indices"] == [15,24]
    assert r["independent_expert_labels"] == 0
    assert r["scientific_acceptance"] == "NOT_PASSED"
