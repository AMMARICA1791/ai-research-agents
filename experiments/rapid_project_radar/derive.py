"""Evidence-bound, dependency-free extraction of testable research questions.

This is a transparent linguistic heuristic, NOT an LLM or validated semantic reasoner.
Untrusted feed text is only data and never executed.
"""
import re

SPLIT = re.compile(r"(?<=[.!?])\\s+")
CLAIM = re.compile(r"\\b(?:propose|introduce|present|demonstrate|show|achieve|improve|reduce|enable|outperform|evaluate|develop|measure|detect|predict|repair|prevent|protect)\\b", re.I)
METHOD = re.compile(r"\\b(?:using|through|via|with|based on|by combining|by applying)\\b", re.I)

def extract(signal):
    if not isinstance(signal, dict):
        raise ValueError("signal must be an object")
    title = str(signal.get("title") or "").strip()[:300]
    abstract = str(signal.get("description") or "").strip()[:2500]
    if not title:
        return None
    sentences = [s.strip() for s in SPLIT.split(abstract) if len(s.strip()) >= 25]
    claim = next((s for s in sentences if CLAIM.search(s)), None)
    method = next((s for s in sentences if METHOD.search(s)), None)
    evidence = claim or (sentences[0] if sentences else title)
    # Do not invent a measured result or assert the source is correct.
    return {
        "title": title,
        "source_excerpt": evidence[:450],
        "method_excerpt": (method or "")[:450],
        "research_question": "Can the central claim in this source be independently reproduced: " + title + "?",
        "falsifiable_prediction": "A separately implemented test reproduces a measurable outcome described by the source; otherwise record inconclusive or failed.",
        "derivation_method": "bounded_sentence_extraction_not_semantic_model",
        "independent_validation": False,
        "requires_domain_specific_test": True,
    }
