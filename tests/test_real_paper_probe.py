from research.real_paper_probe import evaluate

def test_real_excerpt_probe_does_not_forge_accuracy():
    record={"sources":{"paper1":{"axes":{"results":[{"pdf_page":3,"verbatim_text":"The iron-group yields are calculated."}],"methods":[],"limitations":[]}},
                       "paper2":{"axes":{"results":[{"pdf_page":8,"verbatim_text":"No iron-group yields are calculated."}],"methods":[],"limitations":[]}}}}
    r=evaluate(record)
    assert r["total_verbatim_cases"]==2
    assert r["scientific_acceptance"]=="NOT_PASSED"
    assert all(x["ground_truth"]=="UNLABELED" for x in r["cases"])

def test_keywords_are_not_scientific_evidence():
    record={"sources":{"paper":{"axes":{"results":[
        {"pdf_page":1,"verbatim_text":"Keywords: iron-group yields, supernova nucleosynthesis."},
        {"pdf_page":4,"verbatim_text":"The iron-group yields were calculated for several models."}
    ],"methods":[],"limitations":[]}}}}
    rows=evaluate(record)["cases"]
    assert rows[0]["claim_alignment"]=="EXCLUDED_FRONT_MATTER"
    assert rows[0]["classifications"]==[]
    assert rows[1]["claim_alignment"]=="LEXICAL_CANDIDATE"
    assert rows[1]["evidence_role"]=="UNDETERMINED_PENDING_EXPERT_REVIEW"
