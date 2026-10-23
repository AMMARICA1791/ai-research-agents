SOURCE_EXCERPT = "arXiv:2610.29010v1 Announce Type: new Abstract: Radiation treatment planning requires balancing competing objectives to satisfy clinical criteria while accommodating physicians' preferences. This study aims to develop an evidence-driven, multi-agent compound AI system that integrates DRL-based automated treatment planning with LLM-based conversational plan refinement for proton PBS therapy. A policy network trained using PPO first generates multi"
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
