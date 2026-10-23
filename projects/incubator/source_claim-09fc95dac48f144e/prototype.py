SOURCE_EXCERPT = 'arXiv:2610.21449v2 Announce Type: replace Abstract: Large language models (LLMs) can reason over both structured measurements and free-text records, which makes them attractive for emergency department (ED) prediction. However, most existing LLMs still fall short of conventional ML methods like trees on EHR-based prediction tasks. Our controlled analysis traces this gap to two weaknesses: LLMs do not select informative features, and they misjudge'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
