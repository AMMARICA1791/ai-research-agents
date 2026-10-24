SOURCE_EXCERPT = 'OpenAI explains how we strengthened containment for frontier model training and evaluation, including offline environments and high-compute red-teaming.'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
