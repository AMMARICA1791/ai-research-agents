SOURCE_EXCERPT = "arXiv:2604.04978v3 Announce Type: replace-cross Abstract: Claude Code's auto mode is the first deployed permission system for AI coding agents, using a two-stage transcript classifier to gate dangerous tool calls. Anthropic reports a 0.4% false positive rate and 17% false negative rate on production traffic. We present the first independent evaluation of this system on deliberately ambiguous authorization scenarios, i.e., tasks where the user's i"
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
