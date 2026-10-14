"""Fail-closed evidence audit tests; no paid model and no live data required."""
from research.news_eval import audit_model_evidence
from research.news_probe_audit import audit_probe

URL = "https://example.org/research"
SHA = "0123456789abcdef"
EXCERPT = "The study reports an increase of twenty percent in the evaluation."


def evidence():
    return {"source": {"url": URL, "sha256": SHA}, "source_excerpt": EXCERPT}


def model(answer="The study reported a twenty percent increase.",
          quote=EXCERPT, url=URL):
    return {"answer": answer, "quote": quote, "source_url": url}


def test_positive_quote_is_review_only_not_verified_truth():
    result = audit_model_evidence("direct", model(), evidence())
    assert result["status"] == "QUOTE_MATCH_ONLY_SEMANTICS_UNVERIFIED"
    assert result["review_quote"] == EXCERPT
    assert result["trusted_source_url"] == URL
    assert result["publication_allowed"] is False
    assert result["human_semantic_review_required"] is True


def test_invented_quote_is_quarantined_not_repaired():
    result = audit_model_evidence("inference", model(quote="The study achieved a perfect hundred percent."), evidence())
    assert result["status"] == "WITHHELD_INVALID_EVIDENCE"
    assert "quote_not_in_archived_excerpt" in result["issues"]
    assert result["review_answer"] is None
    assert result["review_quote"] is None


def test_model_cannot_override_archived_url():
    result = audit_model_evidence("direct", model(url="https://malicious.example/inject"), evidence())
    assert result["trusted_source_url"] == URL
    assert result["model_source_url_matches"] is False
    assert result["status"] == "WITHHELD_INVALID_EVIDENCE"
    assert "model_source_url_mismatch" in result["issues"]


def test_absence_detection_separate_from_invalid_envelope():
    result = audit_model_evidence("unanswerable", model("NOT_IN_SOURCE", "", ""), evidence())
    assert result["model_detected_absence"] is True
    assert result["status"] == "WITHHELD_INVALID_EVIDENCE"
    assert result["publication_allowed"] is False


def test_abstention_requires_empty_quote():
    result = audit_model_evidence("unanswerable", model("NOT_IN_SOURCE", "Some verification state", URL), evidence())
    assert result["model_detected_absence"] is True
    assert "nonempty_quote_for_absence" in result["issues"]
    assert result["status"] == "WITHHELD_INVALID_EVIDENCE"


def test_valid_abstention_is_still_not_publishable():
    result = audit_model_evidence("unanswerable", model("NOT_IN_SOURCE", "", URL), evidence())
    assert result["status"] == "VALID_ABSTENTION_ENVELOPE"
    assert result["review_answer"] == "NOT_IN_SOURCE"
    assert result["publication_allowed"] is False


def test_missing_source_or_malformed_json_fail_closed():
    assert audit_model_evidence("direct", model(), {})["status"] == "WITHHELD_INVALID_EVIDENCE"
    assert audit_model_evidence("direct", ["not", "json"], evidence())["status"] == "WITHHELD_INVALID_EVIDENCE"


def test_archival_replay_requires_matching_sha():
    data = {"article_cases": [{"retrieval_status": "ARTICLE_RETRIEVED", "evidence": evidence()}]}
    good = {"url": URL, "source_sha256": SHA, "type": "direct",
            "valid_json": True, "parsed_answer": model()["answer"],
            "parsed_quote": EXCERPT, "model_source_url": URL}
    bad = dict(good, source_sha256="tamperedhash")
    report = audit_probe(data, {"results": [good, bad]})
    assert report["quote_review_cases"] == 1
    assert report["quarantined_cases"] == 1
    assert "unmatched_archived_source" in report["results"][1]["audit"]["issues"]
    assert report["results"][1]["audit"]["trusted_source_url"] is None
    assert all(not item["audit"]["publication_allowed"] for item in report["results"])
