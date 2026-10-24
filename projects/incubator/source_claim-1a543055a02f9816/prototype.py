SOURCE_EXCERPT = 'OpenAI and Poland’s NASK are partnering on AI safety, security, and technical research to strengthen safeguards and support a more resilient digital ecosystem.'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
