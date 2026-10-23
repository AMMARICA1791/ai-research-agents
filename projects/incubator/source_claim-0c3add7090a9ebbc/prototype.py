SOURCE_EXCERPT = 'arXiv:2610.04906v4 Announce Type: replace-cross Abstract: Work agents operate over digital artifacts to execute professional knowledge-intensive work, requiring training environments that support long-horizon interaction and trustworthy verification. However, hand-crafted environments incur prohibitive engineering overhead that prevents environment scaling, whereas synthesis methods sacrifice workspace complexity, realism, or grounded verifiabili'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
