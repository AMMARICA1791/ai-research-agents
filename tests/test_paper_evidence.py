from research.paper_evidence import validate, FIELDS


def test_exact_line_quote_required():
    source = "Iron is created in stellar processes.\nThe model uses simulated explosions."
    raw = {"methods": {"claim": "simulations", "quote": "simulated explosions", "line": 2},
           "findings": {"claim": "iron", "quote": "simulated explosions", "line": 1}}
    result = validate(raw, source)
    assert result["methods"]["status"] == "quote_matched_not_fact_verified"
    assert result["findings"]["status"] == "unverified"
    assert all(result[x]["status"] == "unverified" for x in FIELDS if x not in raw)


def test_rejects_fabricated_quote_and_bool_line():
    raw = {"evidence": {"claim": "proof", "quote": "iron came from Mars", "line": True}}
    assert validate(raw, "iron came from Mars")["evidence"]["status"] == "unverified"


def test_quality_gate_fails_for_one_of_five():
    from research.paper_evidence import quote_quality_gate
    evidence = {k: {"status": "unverified"} for k in FIELDS}
    evidence["limitations"]["status"] = "quote_matched_not_fact_verified"
    gate = quote_quality_gate(evidence)
    assert gate["matched"] == 1
    assert gate["passed"] is False
    assert gate["scientific_truth_verified"] is False


def test_quality_gate_requires_four_of_five():
    from research.paper_evidence import quote_quality_gate
    evidence = {k: {"status": "quote_matched_not_fact_verified"} for k in FIELDS}
    evidence["hypothesis"]["status"] = "unverified"
    assert quote_quality_gate(evidence)["passed"] is True
    evidence["methods"]["status"] = "unverified"
    assert quote_quality_gate(evidence)["passed"] is False
