import pytest
from research.scientific_comparison_engine import compare

def test_realistic_comparison_retains_pages_and_abstains():
    a=("The supernova model calculates iron-group nucleosynthesis yields. "*200)
    b=("The type Ia simulation produces nickel isotopes with uncertain yields. "*200)
    report=compare(a,b)
    assert report["comparison"]["results"]["coverage"]=="BOTH_SOURCES"
    assert report["comparison"]["results"]["first_source_evidence"][0]["pdf_page"]==1
    assert report["comparison"]["results"]["agreement_or_conflict"]=="NOT_DETERMINED"
    assert report["scientific_truth_verified"] is False

def test_no_fabricated_comparison_when_missing_evidence():
    a="Ordinary text without scientific results. "*400
    b="Ordinary text without scientific results. "*400
    report=compare(a,b)
    assert report["comparison"]["methods"]["coverage"]=="INSUFFICIENT"
    assert report["cross_paper_scientific_conclusion"]=="ABSTAIN_PENDING_SEMANTIC_REVIEW"

def test_rejects_tiny_excerpt():
    with pytest.raises(ValueError):
        compare("tiny","tiny")
