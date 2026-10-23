SOURCE_EXCERPT = 'arXiv:2609.17631v2 Announce Type: replace Abstract: AI-assisted claims can appear authoritative when evidence, analysis, human authorization, presentation, and correction history describe different states. We develop Publication Authority: an exact-state, non-transferable, single-use publication capability within PAC-2026 (Publication-Accountability Calculus), an AIJIM Protocol candidate. The evaluated specification version (SF-4) defines six non'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
