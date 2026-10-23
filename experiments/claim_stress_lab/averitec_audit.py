"""Audit the compact AVeriTeC JSON dataset without requiring Wikipedia archives.

This is a REAL-DATA ingestion path, not quote-defect validation. AVeriTeC's
claim verdicts and question-answer annotations are not verbatim source quotes.
"""
import argparse
import json
from collections import Counter
from pathlib import Path


def audit(records):
    if not isinstance(records, list):
        raise ValueError("Expected an AVeriTeC JSON array")
    labels = Counter()
    answers = 0
    sourced_answers = 0
    preview = []
    for i, record in enumerate(records):
        if not isinstance(record, dict) or not isinstance(record.get("claim"), str):
            raise ValueError(f"Invalid claim at index {i}")
        labels[str(record.get("label", "MISSING"))] += 1
        qa = record.get("questions", [])
        if not isinstance(qa, list):
            raise ValueError(f"Invalid questions at index {i}")
        for question in qa:
            if not isinstance(question, dict):
                raise ValueError(f"Invalid question at index {i}")
            for answer in question.get("answers", []):
                if not isinstance(answer, dict):
                    raise ValueError(f"Invalid answer at index {i}")
                answers += 1
                if isinstance(answer.get("source_url"), str) and answer["source_url"].strip():
                    sourced_answers += 1
        if len(preview) < 5:
            preview.append({"index": i, "claim": record["claim"], "claim_verdict": record.get("label")})
    return {"dataset": "AVeriTeC", "claims": len(records), "claim_verdicts": dict(labels),
            "answers": answers, "answers_with_source_url": sourced_answers,
            "preview": preview, "quote_text_verified": False,
            "independent_quote_defect_labels": False,
            "ready_for_claim_stress_evaluation": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(audit(json.loads(args.input.read_text(encoding="utf-8"))),
                     indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
