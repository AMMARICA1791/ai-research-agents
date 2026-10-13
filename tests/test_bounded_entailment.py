import json
from pathlib import Path
from research.bounded_entailment import classify, evaluate

def test_reference_cases():
    cases=json.loads(Path("tests/fixtures/bounded_entailment_cases.json").read_text())["cases"]
    assert evaluate(cases)["passed"]

def test_distant_words_abstain():
    quote="Iron-group nuclei are discussed. "+"unrelated words "*20+"The stellar yields are listed."
    assert classify("iron_group_yields",quote)=="INSUFFICIENT_EVIDENCE"

def test_unknown_claim_abstains():
    assert classify("religious_interpretation","Iron-group yields")=="INSUFFICIENT_EVIDENCE"
