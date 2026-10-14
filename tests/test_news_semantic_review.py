"""A semantic-review packet is NOT gold data until independent review occurs."""
import copy
import pytest
from research.news_semantic_review import build_packet, evaluate_reviews

URL = "https://example.org/research"
HASH = "sha256-example"
EXCERPT = "The report describes a new system that was tested on twenty samples in a controlled demonstration. No financial revenue was reported."


def fixture():
    evidence = {"source": {"url": URL, "sha256": HASH}, "source_excerpt": EXCERPT}
    source = {"article_cases": [{"retrieval_status": "ARTICLE_RETRIEVED", "evidence": evidence}]}
    model_rows = [
        {"type": "direct", "question": "What was tested?", "url": URL,
         "source_sha256": HASH, "valid_json": True,
         "parsed_answer": "A new system was tested on twenty samples.",
         "parsed_quote": "The report describes a new system that was tested on twenty samples in a controlled demonstration.",
         "model_source_url": URL},
        {"type": "inference", "question": "What can we infer?", "url": URL,
         "source_sha256": HASH, "valid_json": True,
         "parsed_answer": "The test might not generalize beyond twenty samples.",
         "parsed_quote": "The report describes a new system that was tested on twenty samples in a controlled demonstration.",
         "model_source_url": URL},
        {"type": "unanswerable", "question": "What was revenue?", "url": URL,
         "source_sha256": HASH, "valid_json": True,
         "parsed_answer": "NOT_IN_SOURCE", "parsed_quote": "", "model_source_url": URL},
    ]
    audit_rows = [{
        "question_number": i, "question_type": row["type"],
        "audit": {"trusted_source_url": URL, "trusted_source_sha256": HASH,
                  "status": "QUOTE_MATCH_ONLY_SEMANTICS_UNVERIFIED",
                  "exact_quote_found": i < 3, "model_source_url_matches": True}
    } for i, row in enumerate(model_rows, 1)]
    return source, {"results": model_rows}, {"results": audit_rows}


def reviews_packet():
    return build_packet(*fixture())


def test_build_packet_has_no_gold_labels_or_accuracy_claim():
    packet = reviews_packet()
    assert packet["status"] == "AWAITING_INDEPENDENT_HUMAN_LABELS"
    assert packet["case_count"] == 3
    assert packet["semantic_accuracy"] is None
    assert packet["publication_allowed"] is False
    for row in packet["cases"]:
        assert row["human_review_status"] == "UNREVIEWED"
        assert row["review_labels"] == []
        assert row["semantic_label"] is None
        assert row["source_url"] == URL
        assert row["source_sha256"] == HASH
        assert row["source_excerpt"] == EXCERPT


def test_rejects_tampered_hash_or_audit():
    sources, probe, audit = fixture()
    probe["results"][0]["source_sha256"] = "different"
    with pytest.raises(ValueError, match="No exact archived source"):
        build_packet(sources, probe, audit)
    sources, probe, audit = fixture()
    audit["results"][0]["question_number"] = 2
    with pytest.raises(ValueError, match="Unaligned"):
        build_packet(sources, probe, audit)


def review(case_id, who, label, quote=""):
    return {"case_id": case_id, "reviewer_id": who, "label": label,
            "rationale": "The supplied excerpt supports this scoped assessment.",
            "supporting_quote": quote}


def test_no_reviews_or_only_one_reviewer_cannot_claim_accuracy():
    packet = reviews_packet()
    empty = evaluate_reviews(packet, {"reviews": []})
    assert empty["status"] == "REVIEWER_LABELS_INCOMPLETE"
    assert empty["semantic_accuracy"] is None
    one = evaluate_reviews(packet, {"reviews": [review("Q01", "human-A", "SUPPORTED", EXCERPT[:100])]})
    assert one["cases_with_two_reviews"] == 0
    assert one["publication_allowed"] is False


def test_positive_review_requires_exact_source_quote():
    packet = reviews_packet()
    with pytest.raises(ValueError, match="exact source passage"):
        evaluate_reviews(packet, {"reviews": [review("Q01", "human-A", "SUPPORTED", "Fabricated and unsupported phrase")]})
    with pytest.raises(ValueError, match="exact source passage"):
        evaluate_reviews(packet, {"reviews": [review("Q01", "human-A", "PARTIAL", "")]})


def test_duplicate_or_invalid_reviewer_is_rejected():
    packet = reviews_packet()
    entries = [review("Q01", "human-A", "SUPPORTED", EXCERPT[:100])] * 2
    with pytest.raises(ValueError, match="Duplicate reviewer"):
        evaluate_reviews(packet, {"reviews": entries})
    with pytest.raises(ValueError, match="Invalid label"):
        evaluate_reviews(packet, {"reviews": [review("Q01", "human-A", "CORRECT_ABSTENTION")]})


def test_false_correct_abstention_is_rejected():
    packet = reviews_packet()
    fake = copy.deepcopy(packet)
    fake["cases"][2]["model_answer"] = "invented revenue"
    with pytest.raises(ValueError, match="non-abstaining"):
        evaluate_reviews(fake, {"reviews": [review("Q03", "human-A", "CORRECT_ABSTENTION")]})


def full_reviews(disagree=False):
    rows = []
    for who in ("human-A", "human-B"):
        rows.extend([
            review("Q01", who, "SUPPORTED", EXCERPT[:100]),
            review("Q02", who, "PARTIAL" if (disagree and who == "human-B") else "UNSUPPORTED", EXCERPT[:100] if (disagree and who == "human-B") else ""),
            review("Q03", who, "CORRECT_ABSTENTION"),
        ])
    return {"reviews": rows}


def test_two_reviewers_agreement_is_not_automatic_truth():
    result = evaluate_reviews(reviews_packet(), full_reviews())
    assert result["case_agreements"] == 3
    assert result["status"] == "TWO_REVIEWER_AGREEMENT_UNADJUDICATED"
    assert result["semantic_accuracy"] is None
    assert result["publication_allowed"] is False


def test_disagreement_requires_adjudication_and_blocks_score():
    result = evaluate_reviews(reviews_packet(), full_reviews(disagree=True))
    assert result["status"] == "DISAGREEMENT_REQUIRES_ADJUDICATION"
    assert result["disagreement_case_ids"] == ["Q02"]
    assert result["semantic_accuracy"] is None
