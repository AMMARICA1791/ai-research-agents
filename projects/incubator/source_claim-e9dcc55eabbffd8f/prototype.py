SOURCE_EXCERPT = 'arXiv:2610.31130v1 Announce Type: cross Abstract: Offline tests can fail to reveal whether an agent update will remain safe after deployment. We operationalize this post-audit mirage using matched safe and harmful lifecycles that expose identical verifier-visible evidence while an isolated scorer records opposite deployment truth. Our theorem applies standard observational-equivalence and indistinguishability ideas to this executable audit bounda'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
