from research.claim_scope_review import judge

def test_narrow_claim_has_page_anchored_candidate_not_truth_claim():
    text=("Explosive nucleosynthesis in a supernova produces yields of iron-group nuclei. "*12)+"\f"+("Other methods and uncertainties. "*25)
    result=judge(text)
    x=result["claims"]["paper_models_explosive_nucleosynthesis"]
    assert x["verdict"]=="EVIDENCE_CANDIDATE_REQUIRES_SEMANTIC_REVIEW"
    assert x["evidence"][0]["pdf_page"]==1
    assert x["scientific_truth_verified"] is False

def test_unrelated_words_do_not_prove_claim():
    text="nucleosynthesis "+(" unrelated material "*200)+"supernova"
    result=judge(text)
    assert result["claims"]["paper_models_explosive_nucleosynthesis"]["verdict"]=="INSUFFICIENT_EVIDENCE"

def test_overreach_always_abstains():
    text="All Earth iron came from supernovae and the Quran proves it. "*100
    result=judge(text)
    for key in ("all_earth_iron_came_from_supernovae","every_iron_atom_came_from_one_supernova","quran_57_25_is_scientifically_proven"):
        assert result["claims"][key]["verdict"]=="INSUFFICIENT_EVIDENCE"
