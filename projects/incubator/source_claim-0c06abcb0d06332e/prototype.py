SOURCE_EXCERPT = 'W3C launches a Patent Advisory Group (PAG) to resolve issues in the event a patent has been disclosed that may be essential, but is not available under the W3C Royalty-Free licensing terms.'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
