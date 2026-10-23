"""Offline, auditable multi-reviewer council for radar project triage.

Reviewers communicate via a shared structured dossier; no model API or secret is used.
Scores are heuristics, not scientific novelty or impact measurements.
"""
import argparse
import json
import re
from pathlib import Path

def _words(text):
    return set(re.findall(r"[a-z]{4,}", str(text).lower()))

def review(hypothesis, peers=()):
    title = str(hypothesis.get("source_title") or hypothesis.get("title") or "")
    excerpt = str(hypothesis.get("source_excerpt") or "")
    question = str(hypothesis.get("research_question") or "")
    project_id = str(hypothesis.get("topic", "unknown")) + "-" + str(hypothesis.get("source_id", ""))
    dossier = {"project_id": project_id, "protocol": "shared_dossier_v1", "reviewers": [], "peer_messages": []}
    # Analyst: reads evidence and transmits its findings to validator.
    grounded = bool(title and excerpt and question)
    analyst = {"agent": "source_analyst", "finding": "source_excerpt_present" if grounded else "source_evidence_incomplete",
               "source_words": len(_words(excerpt)), "confidence": "limited"}
    dossier["reviewers"].append(analyst)
    dossier["peer_messages"].append({"from": "source_analyst", "to": "evidence_validator", "message": analyst["finding"]})
    # Comparator: overlap is a lead for human inspection, not a duplicate verdict.
    this_words = _words(title)
    comparisons = []
    for other in peers:
        other_title = str(other.get("source_title") or other.get("title") or "")
        if not other_title or other_title == title:
            continue
        other_words = _words(other_title)
        overlap = len(this_words & other_words) / max(1, len(this_words | other_words))
        if overlap >= 0.35:
            comparisons.append({"title": other_title[:200], "title_jaccard": round(overlap, 3)})
    comparisons.sort(key=lambda x: -x["title_jaccard"])
    comparator = {"agent": "similarity_reviewer", "possible_overlaps": comparisons[:5],
                  "method": "title_word_jaccard_not_semantic_equivalence"}
    dossier["reviewers"].append(comparator)
    dossier["peer_messages"].append({"from": "similarity_reviewer", "to": "priority_coordinator",
                                      "message": "potential_overlap_count=" + str(len(comparisons))})
    # Validator: checks actual implementation class, not green CI alone.
    specific = bool(hypothesis.get("independent_validation"))
    validator = {"agent": "evidence_validator", "source_grounded": grounded,
                 "scientific_result_reproduced": specific,
                 "finding": "scientific_validation_not_established" if not specific else "validation_claim_requires_manual_audit"}
    dossier["reviewers"].append(validator)
    dossier["peer_messages"].append({"from": "evidence_validator", "to": "priority_coordinator", "message": validator["finding"]})
    # Coordinator assigns attention, never asserts commercial impact or originality.
    score = 20 + (25 if grounded else 0) + (10 if len(_words(excerpt)) >= 30 else 0) + (15 if specific else 0) - (10 if comparisons else 0)
    score = max(0, min(100, score))
    priority = "REVIEW_FIRST" if score >= 55 else ("RESEARCH_NEXT" if score >= 35 else "EVIDENCE_NEEDED")
    dossier["priority"] = {"score": score, "band": priority, "basis": "heuristic_triage_only",
                           "not_measured": ["global_novelty", "scientific_impact", "commercial_value"]}
    dossier["reviewers"].append({"agent": "priority_coordinator", "decision": priority,
                                  "next_action": "design_domain_specific_replication" if grounded else "retrieve_full_source"})
    dossier["status"] = "reviewed_not_validated"
    return dossier

def write_review(project, peers=()):
    project = Path(project)
    hypothesis = json.loads((project / "hypothesis.json").read_text(encoding="utf-8"))
    dossier = review(hypothesis, peers)
    (project / "COUNCIL_REVIEW.json").write_text(json.dumps(dossier, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return dossier

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--projects", required=True)
    args = parser.parse_args()
    root = Path(args.projects)
    projects = sorted(root.glob("*/hypothesis.json"))
    all_hypotheses = [json.loads(p.read_text(encoding="utf-8")) for p in projects]
    output = []
    for path, hypothesis in zip(projects, all_hypotheses):
        peers = [other for other in all_hypotheses if other is not hypothesis]
        output.append(write_review(path.parent, peers))
    print(json.dumps({"reviewed": len(output), "priority_bands": {band: sum(d["priority"]["band"] == band for d in output) for band in ("REVIEW_FIRST", "RESEARCH_NEXT", "EVIDENCE_NEEDED")}}, indent=2))
