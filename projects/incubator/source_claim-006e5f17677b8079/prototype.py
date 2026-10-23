SOURCE_EXCERPT = 'arXiv:2602.06232v2 Announce Type: replace-cross Abstract: Game balancing is a longstanding challenge requiring repeated playtesting, expert intuition, and extensive manual tuning. We introduce RuleSmith, a framework that couples multi-agent LLM self-play with surrogate-based optimization over a parameterized rule space. As a proof of concept, we build CivMini, a simplified civilization-style game with two asymmetric factions governed by 12 tunabl'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
