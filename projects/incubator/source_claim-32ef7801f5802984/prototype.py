SOURCE_EXCERPT = 'Bringing foundational models to the front lines of TB screening'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
