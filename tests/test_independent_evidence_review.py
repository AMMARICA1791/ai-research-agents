import hashlib
from research.primary_pdf_audit import extract
from research.independent_evidence_review import assess

def fixture():
    text=("nucleosynthesis iron-group yields and mass cut. "*18)+"\f"+("uncertainty in model yields. "*25)
    audit=extract(text)
    audit["source_text_sha256"]=hashlib.sha256(text.encode()).hexdigest()
    return text,audit

def test_independent_review_passes_only_integrity():
    text,audit=fixture()
    result=assess(text,audit)
    assert result["passed"],result
    assert result["scientific_entailment"]=="NOT_TESTED"
    assert result["claim_assessments"]["all_terrestrial_iron_from_supernovae"]=="NOT_ESTABLISHED_BY_THIS_AUDIT"

def test_forged_quote_fails():
    text,audit=fixture()
    audit["candidates"]["iron_group"][0]["excerpt"]="invented quote"
    assert not assess(text,audit)["passed"]

def test_wrong_page_fails():
    text,audit=fixture()
    audit["candidates"]["iron_group"][0]["pdf_page"]=2
    assert not assess(text,audit)["passed"]

def test_source_tampering_fails():
    text,audit=fixture()
    assert not assess(text+" changed",audit)["passed"]

def test_fake_truth_verification_fails():
    text,audit=fixture()
    audit["scientific_truth_verified"]=True
    assert not assess(text,audit)["passed"]
