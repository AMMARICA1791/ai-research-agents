"""Offline regression tests for deterministic PDF text audit."""
from research.primary_pdf_audit import extract

def test_page_provenance_and_exact_source_context():
    text = ("Introduction to nucleosynthesis. " * 20
            + "\f" + "The iron-group yields depend on mass cut and fallback. " * 12)
    audit = extract(text)
    assert audit["scientific_truth_verified"] is False
    assert audit["pdf_pages_detected"] == 2
    assert audit["candidates"]["nucleosynthesis"][0]["pdf_page"] == 1
    assert audit["candidates"]["iron_group"][0]["pdf_page"] == 2
    assert audit["candidates"]["model_uncertainty"][0]["pdf_page"] == 2
    assert "iron-group" in audit["candidates"]["iron_group"][0]["excerpt"]
    assert audit["candidates"]["iron_group"][0]["status"] == "text_match_only_not_fact_verified"

def test_absent_evidence_is_reported_as_missing():
    audit = extract("plain unrelated text " * 40)
    assert len(audit["missing_categories"]) == 4
    assert not any(audit["candidates"].values())
