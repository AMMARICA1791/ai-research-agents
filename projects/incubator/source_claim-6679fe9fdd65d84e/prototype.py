SOURCE_EXCERPT = 'arXiv:2607.20491v4 Announce Type: replace Abstract: When a financial agent repeats its decision, how much does that tell us about the actions behind it? DFAH-Bench examines this question through replay experiments, a controlled test of omitted tool calls, and banking tasks with authorization checks. Across 570 eligible prospective replay episodes, decisions agreed at rates of 94-95%, while tool paths, including inputs and results, agreed at 45-52'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
