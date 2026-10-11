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
