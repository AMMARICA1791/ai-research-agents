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


def test_publication_metadata_cannot_be_lexical_evidence():
    record={"sources":{"type_ia":{"axes":{"methods":[
        {"pdf_page":1,"verbatim_text":"arXiv:astro-ph/0002337v1 17 Feb 2000 Published in the Astrophysical Journal Supplement Series, 1999, v.125, pp.439-462 Preprint typeset using LATEX style emulateapj NUCLEOSYNTHESIS IN CHANDRASEKHAR MASS MODELS FOR TYPE IA SUPERNOVAE"},
        {"pdf_page":3,"verbatim_text":"After a description of our model calculations in section 2, including initial models and hydrodynamic treatment, we present in section 3 detailed nucleosynthesis results."}
    ],"results":[],"limitations":[]}}}}
    rows=evaluate(record)["cases"]
    assert [x["claim_alignment"] for x in rows]==["EXCLUDED_FRONT_MATTER","EXCLUDED_SECTION_OVERVIEW"]
    assert all(x["candidate_claims"]==[] and x["classifications"]==[] for x in rows)
