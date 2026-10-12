from research.real_paper_probe import evaluate

def test_real_excerpt_probe_does_not_forge_accuracy():
    record={"sources":{"paper1":{"axes":{"results":[{"pdf_page":3,"verbatim_text":"The iron-group yields are calculated."}],"methods":[],"limitations":[]}},
                       "paper2":{"axes":{"results":[{"pdf_page":8,"verbatim_text":"No iron-group yields are calculated."}],"methods":[],"limitations":[]}}}}
    r=evaluate(record)
    assert r["total_verbatim_cases"]==2
    assert r["scientific_acceptance"]=="NOT_PASSED"
    assert all(x["ground_truth"]=="UNLABELED" for x in r["cases"])
