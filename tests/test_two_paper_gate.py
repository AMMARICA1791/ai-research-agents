from research.two_paper_gate import compare
import pytest

def test_two_distinct_full_sources_required():
    with pytest.raises(ValueError):
        compare({"same":"nucleosynthesis "*1000})
    with pytest.raises(ValueError):
        compare({"a":"tiny","b":"nucleosynthesis "*1000})

def test_comparison_never_claims_scientific_truth():
    a="nucleosynthesis iron-group uncertainties "+"stellar model "*1000
    b="nucleosynthesis iron group electron capture "+"type ia model "*1000
    r=compare({"core_collapse":a,"type_ia":b})
    assert "nucleosynthesis" in r["common_topics"]
    assert r["scientific_entailment"]=="NOT_TESTED"
    assert r["independent_scientific_reasoning"]=="NOT_DEMONSTRATED"
    assert r["claim_all_earth_iron_from_supernovae"]=="NOT_ESTABLISHED"
