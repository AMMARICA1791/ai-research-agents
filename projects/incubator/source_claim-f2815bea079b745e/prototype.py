SOURCE_EXCERPT = 'Article URL: https://app.enclave.ai/threat-feed Comments URL: https://news.ycombinator.com/item?id=50222559 Points: 2 # Comments: 0'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
