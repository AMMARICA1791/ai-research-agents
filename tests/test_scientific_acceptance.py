from research.scientific_acceptance import evaluate

def test_lexical_comparison_cannot_pass_semantic_gate():
    report={"sources":{"a":{"topics":{"iron_group":{"pdf_page":1,"exact_excerpt":"iron-group yields"}}},
                       "b":{"topics":{"iron_group":{"pdf_page":2,"exact_excerpt":"iron-group yields"}}}},
            "common_topics":["iron_group"]}
    result=evaluate(report)
    assert result["decision"]=="FAIL"
    assert result["checks"]["page_anchored_claims_from_both_sources"] is True
    assert result["checks"]["claim_evidence_semantic_entailment_verified"] is False

def test_missing_primary_sources_fails():
    assert evaluate({"sources":{}})["passed"] is False
