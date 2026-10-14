"""Prepare a source-bound semantic review packet; do not auto-generate gold labels.

Examples:
  python -m research.news_semantic_review --sources <sources.json> \
      --probe <probe.json> --audit <audit.json> --output <review_packet.json>
  python -m research.news_semantic_review --packet <review_packet.json> \
      --reviews <independent_reviews.json> --output <review_result.json>

Packet contains copyrighted source excerpts ONLY in short-lived workflow artifacts,
not committed to the public repository. Two reviewers must label independently.
"""
import argparse
import json
from collections import Counter
from pathlib import Path

from research.news_eval import verify_quote

ANSWERABLE = {"direct", "inference"}
LABELS = {
    "direct": {"SUPPORTED", "PARTIAL", "UNSUPPORTED", "INSUFFICIENT_CONTEXT"},
    "inference": {"SUPPORTED", "PARTIAL", "UNSUPPORTED", "INSUFFICIENT_CONTEXT"},
    "unanswerable": {"CORRECT_ABSTENTION", "INCORRECT_ABSTENTION", "INSUFFICIENT_CONTEXT"},
}
NO_GOLD_STATUS = "AWAITING_INDEPENDENT_HUMAN_LABELS"


def build_packet(sources, probe, audit):
    """Join by source URL + retrieved content SHA; model echo is not provenance."""
    source_rows = sources.get("article_cases")
    model_rows = probe.get("results")
    audit_rows = audit.get("results")
    if not all(isinstance(v, list) and v for v in (source_rows, model_rows, audit_rows)):
        raise ValueError("Nonempty archived sources, model results and audit results required")
    if len(model_rows) != len(audit_rows):
        raise ValueError("Model/audit result lengths differ")

    by_source = {}
    for case in source_rows:
        if not isinstance(case, dict) or case.get("retrieval_status") != "ARTICLE_RETRIEVED":
            continue
        evidence = case.get("evidence", {})
        src = evidence.get("source", {}) if isinstance(evidence, dict) else {}
        if not isinstance(src, dict):
            continue
        key = (src.get("url"), src.get("sha256"))
        if not all(isinstance(x, str) and x for x in key):
            raise ValueError("Incomplete archived source provenance")
        if key in by_source:
            raise ValueError("Duplicate source archive fingerprint")
        by_source[key] = evidence

    cases = []
    for i, (model, checked) in enumerate(zip(model_rows, audit_rows), start=1):
        if not isinstance(model, dict) or not isinstance(checked, dict):
            raise ValueError("Malformed model/audit result")
        if checked.get("question_number") != i or checked.get("question_type") != model.get("type"):
            raise ValueError(f"Unaligned audit case {i}")
        kind = model.get("type")
        if kind not in LABELS:
            raise ValueError(f"Unknown question class at {i}")
        key = (model.get("url"), model.get("source_sha256"))
        evidence = by_source.get(key)
        check = checked.get("audit", {})
        if not isinstance(check, dict):
            raise ValueError("Malformed mechanical audit")
        if evidence is None or check.get("trusted_source_url") != key[0] or check.get("trusted_source_sha256") != key[1]:
            raise ValueError(f"No exact archived source+hash for case {i}")
        excerpt = evidence.get("source_excerpt")
        if not isinstance(excerpt, str) or not excerpt.strip():
            raise ValueError(f"Missing archived excerpt for case {i}")

        cases.append({
            "case_id": f"Q{i:02d}",
            "question_type": kind,
            "question": model.get("question") if isinstance(model.get("question"), str) else None,
            "source_url": key[0],
            "source_sha256": key[1],
            "source_excerpt": excerpt,
            "model_answer": model.get("parsed_answer") if model.get("valid_json") is True else None,
            "model_quote": model.get("parsed_quote") if model.get("valid_json") is True else None,
            "mechanical_audit_status": check.get("status"),
            "model_quote_matches_excerpt": bool(check.get("exact_quote_found")),
            "model_source_echo_matches_archive": bool(check.get("model_source_url_matches")),
            "review_labels": [],
            "semantic_label": None,
            "human_review_status": "UNREVIEWED",
            "publication_allowed": False,
        })

    if not cases:
        raise ValueError("No reviewable cases")
    return {
        "schema": "news-semantic-review-v1",
        "status": NO_GOLD_STATUS,
        "case_count": len(cases),
        "cases": cases,
        "review_protocol": {
            "reviewers_per_case": 2,
            "reviewer_ids_are_self_reported": True,
            "judgment_scope": "ONLY the archived 1200-character excerpt, not full source or independent truth",
            "labels_by_type": {k: sorted(v) for k, v in LABELS.items()},
            "required_review_fields": ["case_id", "reviewer_id", "label", "rationale", "supporting_quote"],
            "notes": [
                "Review the source excerpt, answer and quote: does the quote substantiate the answer?",
                "Exact quote matching is NOT semantic entailment",
                "Reviewers must not use model predictions as gold labels",
                "Human review identities and independence cannot be authenticated by this software",
                "Do not publish answers on this packet's authority",
            ],
        },
        "semantic_accuracy": None,
        "publication_allowed": False,
    }


def evaluate_reviews(packet, submitted):
    """Check two distinct *self-declared* reviewers per case; do not invent a score."""
    if packet.get("schema") != "news-semantic-review-v1":
        raise ValueError("Unexpected packet schema")
    cases = packet.get("cases")
    entries = submitted.get("reviews") if isinstance(submitted, dict) else None
    if not isinstance(cases, list) or not cases or not isinstance(entries, list):
        raise ValueError("Review packet and review list required")
    by_id = {case.get("case_id"): case for case in cases if isinstance(case, dict)}
    if len(by_id) != len(cases):
        raise ValueError("Duplicate or invalid case IDs")
    seen, grouped = set(), {key: [] for key in by_id}
    for rev in entries:
        if not isinstance(rev, dict):
            raise ValueError("Invalid reviewer record")
        case_id, reviewer = rev.get("case_id"), rev.get("reviewer_id")
        if case_id not in by_id or not isinstance(reviewer, str) or len(reviewer.strip()) < 3:
            raise ValueError("Invalid case or reviewer ID")
        key = (case_id, reviewer.strip())
        if key in seen:
            raise ValueError("Duplicate reviewer on a case")
        seen.add(key)
        case = by_id[case_id]
        label = rev.get("label")
        if label not in LABELS.get(case.get("question_type"), set()):
            raise ValueError("Invalid label for question type")
        rationale = rev.get("rationale")
        if not isinstance(rationale, str) or len(rationale.strip()) < 25:
            raise ValueError("Human rationale must explain the judgment")
        supporting_quote = rev.get("supporting_quote", "")
        if not isinstance(supporting_quote, str):
            raise ValueError("Human quote must be text")
        if label in ("SUPPORTED", "PARTIAL") and verify_quote(supporting_quote, case["source_excerpt"]) != "exact":
            raise ValueError("Positive reviewer label must identify an exact source passage")
        if label == "CORRECT_ABSTENTION" and case.get("model_answer") != "NOT_IN_SOURCE":
            raise ValueError("Cannot mark non-abstaining model answer as correct abstention")
        grouped[case_id].append({"reviewer_id": reviewer.strip(), "label": label})

    coverage = {cid: len(v) for cid, v in grouped.items()}
    if any(n > 2 for n in coverage.values()):
        raise ValueError("Only two independently submitted reviews per case")
    complete = all(n == 2 for n in coverage.values())
    agreed = sum(len(v) == 2 and v[0]["label"] == v[1]["label"] for v in grouped.values())
    disagreements = sorted(cid for cid, v in grouped.items() if len(v) == 2 and v[0]["label"] != v[1]["label"])
    status = ("REVIEWER_LABELS_INCOMPLETE" if not complete else
              "DISAGREEMENT_REQUIRES_ADJUDICATION" if disagreements else
              "TWO_REVIEWER_AGREEMENT_UNADJUDICATED")
    return {
        "status": status,
        "cases_total": len(cases),
        "cases_with_two_reviews": sum(n == 2 for n in coverage.values()),
        "case_agreements": agreed,
        "disagreement_case_ids": disagreements,
        "semantic_accuracy": None,
        "publication_allowed": False,
        "limits": [
            "Reviewer identity and independence are self-reported, not technically verified",
            "Agreement is not proof of truth and is not an accuracy score",
            "No independent source corroboration or full-article review",
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sources")
    parser.add_argument("--probe")
    parser.add_argument("--audit")
    parser.add_argument("--packet")
    parser.add_argument("--reviews")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    if args.reviews:
        if not args.packet or any([args.sources, args.probe, args.audit]):
            parser.error("--reviews requires --packet only")
        packet = json.loads(Path(args.packet).read_text(encoding="utf-8"))
        user_reviews = json.loads(Path(args.reviews).read_text(encoding="utf-8"))
        result = evaluate_reviews(packet, user_reviews)
    else:
        if not all((args.sources, args.probe, args.audit)) or args.packet:
            parser.error("Provide --sources, --probe, --audit to prepare review packet")
        source = json.loads(Path(args.sources).read_text(encoding="utf-8"))
        probe = json.loads(Path(args.probe).read_text(encoding="utf-8"))
        audit = json.loads(Path(args.audit).read_text(encoding="utf-8"))
        result = build_packet(source, probe, audit)
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("SEMANTIC_REVIEW_STATUS:", result["status"])
    print("SEMANTIC_ACCURACY_NOT_ESTABLISHED")
    print("Output:", target)


if __name__ == "__main__":
    main()
