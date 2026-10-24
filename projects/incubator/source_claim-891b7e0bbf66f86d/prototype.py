SOURCE_EXCERPT = 'Fast, focused, low-cost decisions for any application.'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
