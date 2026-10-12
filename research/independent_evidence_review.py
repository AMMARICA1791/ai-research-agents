"""Independent falsification-oriented audit of deterministic PDF evidence.

A pass means integrity/provenance only, NOT scientific entailment.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

def assess(text, audit):
    pages = text.split("\f")
    if pages and not pages[-1].strip():
        pages.pop()
    failures = []
    count = 0
    for category, items in audit.get("candidates", {}).items():
        for item in items:
            count += 1
            page_no = item.get("pdf_page")
            if not isinstance(page_no, int) or not 1 <= page_no <= len(pages):
                failures.append(f"{category}:invalid_pdf_page")
                continue
            page = re.sub(r"\s+", " ", pages[page_no - 1]).strip()
            excerpt = item.get("excerpt", "")
            if not excerpt or excerpt not in page:
                failures.append(f"{category}:excerpt_not_in_cited_page")
            if item.get("matched_text", "").lower() not in excerpt.lower():
                failures.append(f"{category}:keyword_not_in_excerpt")
            if item.get("status") != "text_match_only_not_fact_verified":
                failures.append(f"{category}:unsupported_verification_status")
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    if audit.get("source_text_sha256") != digest:
        failures.append("source_digest_mismatch")
    if audit.get("scientific_truth_verified") is not False:
        failures.append("invalid_truth_claim")
    if audit.get("pdf_pages_detected") != len(text.split("\f")):
        failures.append("page_count_mismatch")
    if count < 1:
        failures.append("no_evidence_candidates")
    return {
        "test": "independent_source_provenance_and_scope",
        "passed": not failures,
        "evidence_candidates_checked": count,
        "pdf_pages_with_content": len(pages),
        "failures": failures,
        "scientific_entailment": "NOT_TESTED",
        "claim_assessments": {
            "paper_discusses_stellar_nucleosynthesis": "TOPIC_LOCATED_NOT_SCIENTIFICALLY_ADJUDICATED",
            "all_terrestrial_iron_from_supernovae": "NOT_ESTABLISHED_BY_THIS_AUDIT",
            "specific_iron_atoms_traced_to_earth": "NOT_ESTABLISHED",
            "quran_57_25_interpretation": "OUTSIDE_ASTROPHYSICS_TEST"
        }
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source",required=True)
    p.add_argument("--audit",required=True)
    p.add_argument("--output",required=True)
    a=p.parse_args()
    path=Path(a.source)
    text=path.read_text(encoding="utf-8",errors="replace")
    audit=json.loads(Path(a.audit).read_text())
    result=assess(text,audit)
    Path(a.output).write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2),flush=True)
    if not result["passed"]:
        raise SystemExit("INDEPENDENT_PROVENANCE_TEST_FAILED")

if __name__=="__main__":
    main()
