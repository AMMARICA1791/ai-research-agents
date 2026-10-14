"""Replay an archived real-news Qwen probe without calling a model or a network.

Run:
 python -m research.news_probe_audit --sources research_output/news_qwen_sources.json \
   --probe research_output/news_qwen_probe.json --output research_output/news_audit.json
This checks provenance and literal quotes, NOT model truth or entailment.
"""
import argparse
import json
from collections import Counter
from pathlib import Path
from research.news_eval import audit_model_evidence


def audit_probe(source_data, probe_data):
    """Join by archived URL plus content SHA-256; never trust model-generated URL."""
    cases = source_data.get("article_cases", [])
    rows = probe_data.get("results", [])
    if not isinstance(cases, list) or not isinstance(rows, list) or not rows:
        raise ValueError("Source inventory and nonempty model results are required")

    archived = {}
    for case in cases:
        if not isinstance(case, dict) or case.get("retrieval_status") != "ARTICLE_RETRIEVED":
            continue
        evidence = case.get("evidence")
        if not isinstance(evidence, dict):
            continue
        source = evidence.get("source", {})
        if not isinstance(source, dict):
            continue
        key = (source.get("url"), source.get("sha256"))
        if not all(isinstance(part, str) and part for part in key):
            continue
        if key in archived:
            raise ValueError("Duplicate source URL + SHA-256 in archive")
        archived[key] = evidence

    audited = []
    for index, row in enumerate(rows, 1):
        if not isinstance(row, dict):
            raise ValueError(f"Non-object model result at item {index}")
        key = (row.get("url"), row.get("source_sha256"))
        evidence = archived.get(key)
        if evidence is None:
            # There is no trustworthy source excerpt for this model response.
            reviewed = audit_model_evidence(row.get("type"), None, {})
            reviewed["issues"].append("unmatched_archived_source")
        else:
            parsed = None
            if row.get("valid_json") is True:
                parsed = {
                    "answer": row.get("parsed_answer"),
                    "quote": row.get("parsed_quote"),
                    "source_url": row.get("model_source_url"),
                }
            reviewed = audit_model_evidence(row.get("type"), parsed, evidence)
        audited.append({
            "question_number": index,
            "question_type": row.get("type"),
            "source_url_claim_from_run": row.get("url"),
            "audit": reviewed,
        })

    stats = Counter(item["audit"]["status"] for item in audited)
    return {
        "status": "MECHANICAL_REVIEW_ONLY",
        "source_archive_count": len(archived),
        "question_count": len(audited),
        "matched_quote_cases": sum(x["audit"]["exact_quote_found"] for x in audited),
        "explicit_absence_decisions": sum(
            x["audit"]["model_detected_absence"] for x in audited
            if x["question_type"] == "unanswerable"
        ),
        "valid_abstention_envelopes": stats["VALID_ABSTENTION_ENVELOPE"],
        "quarantined_cases": stats["WITHHELD_INVALID_EVIDENCE"],
        "quote_review_cases": stats["QUOTE_MATCH_ONLY_SEMANTICS_UNVERIFIED"],
        "model_url_mismatch_cases": sum(
            "model_source_url_mismatch" in x["audit"]["issues"] for x in audited
        ),
        "results": audited,
        "limitations": [
            "No answer semantic entailment assessment or independent human gold labels",
            "All extracted source excerpts are bounded snapshots from publisher pages",
            "Trusted source URL and SHA are derived from archived retrieval, never from model output",
            "All responses remain prohibited from automatic publication",
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sources", required=True)
    parser.add_argument("--probe", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    source_data = json.loads(Path(args.sources).read_text(encoding="utf-8"))
    probe_data = json.loads(Path(args.probe).read_text(encoding="utf-8"))
    report = audit_probe(source_data, probe_data)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("MECHANICAL_REVIEW_ONLY:", report["question_count"])
    print("QUARANTINED:", report["quarantined_cases"])
    print("QUOTE_MATCHED:", report["matched_quote_cases"])
    print("VALID_ABSTENTIONS:", report["valid_abstention_envelopes"])
    print("OUTPUT:", output)


if __name__ == "__main__":
    main()
