SOURCE_EXCERPT = 'arXiv:2601.15322v4 Announce Type: replace Abstract: Replaying a financial agent requires specifying the conditions of a rerun, preserving its execution record, and deciding which parts of its behavior to compare. We introduce the Determinism-Faithfulness Assurance Harness (DFAH), a framework and practical protocol for organizing these choices. The framework distinguishes comparisons of final decisions, tool-name sets, and ordered tool names, whil'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
