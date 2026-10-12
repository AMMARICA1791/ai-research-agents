"""Fail-closed semantic acceptance benchmark for two original papers.

A lexical match is NEVER accepted as scientific entailment. The current
deterministic system is evaluated against requirements it cannot satisfy.
"""
import json
from research.two_paper_gate import compare

ACCEPTANCE_REQUIREMENTS = (
    "page_anchored_claims_from_both_sources",
    "methodological_comparison",
    "quantitative_or_qualitative_results_comparison",
    "limitations_and_disagreement_assessed",
    "claim_evidence_semantic_entailment_verified",
)

def evaluate(two_paper_report):
    sources=two_paper_report.get("sources",{})
    checks={
        "page_anchored_claims_from_both_sources": len(sources)==2 and all(
            any(x and x.get("pdf_page") and x.get("exact_excerpt") for x in s.get("topics",{}).values())
            for s in sources.values()),
        "methodological_comparison": False,
        "quantitative_or_qualitative_results_comparison": False,
        "limitations_and_disagreement_assessed": False,
        "claim_evidence_semantic_entailment_verified": False,
    }
    # Never infer semantic competence from keywords or provenance.
    return {"test":"scientific_semantic_acceptance_v1",
            "checks":checks,
            "passed":all(checks.values()),
            "decision":"PASS" if all(checks.values()) else "FAIL",
            "reason":"Lexical source comparison is not an independent scientific interpretation; method, results, limitations and entailment are not established.",
            "next_action":"Do not merge as scientifically validated."}

def main():
    import argparse
    from pathlib import Path
    p=argparse.ArgumentParser()
    p.add_argument("--comparison",required=True)
    p.add_argument("--output",required=True)
    a=p.parse_args()
    result=evaluate(json.loads(Path(a.comparison).read_text()))
    Path(a.output).write_text(json.dumps(result,indent=2)+"\n")
    print("SCIENTIFIC_ACCEPTANCE",result["decision"],result["checks"],flush=True)
    # This workflow is a diagnostic scientific gate: an honest FAIL is recorded
    # in the report without generating misleading green scientific acceptance.

if __name__=="__main__":
    main()
