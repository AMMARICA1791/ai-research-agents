"""Real primary-paper excerpt: exact-text check, not scientific verification."""
from pathlib import Path
from research.paper_evidence import validate, quote_quality_gate

def test_original_paper_abstract_provenance():
    # Woosley & Weaver 1995, ApJS 101 p.181, DOI 10.1086/192237.
    source = Path("tests/fixtures/woosley_weaver_1995_primary_excerpt.txt").read_text()
    lines = source.splitlines()
    raw = {
        "methods": {"claim": "78 simulated explosions", "quote": lines[0], "line": 1},
        "limitations": {"claim": "Model-parameter sensitivity discussed", "quote": lines[1], "line": 2},
    }
    evidence = validate(raw, source)
    assert evidence["methods"]["status"] == "quote_matched_not_fact_verified"
    assert evidence["limitations"]["status"] == "quote_matched_not_fact_verified"
    gate = quote_quality_gate(evidence)
    assert gate["matched"] == 2
    assert gate["passed"] is False
    assert gate["scientific_truth_verified"] is False
