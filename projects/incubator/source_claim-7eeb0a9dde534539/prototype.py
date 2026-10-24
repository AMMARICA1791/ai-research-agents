SOURCE_EXCERPT = 'Open and Emergent Problems in Agentic Privacy and Security: A Contextual Angle'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
