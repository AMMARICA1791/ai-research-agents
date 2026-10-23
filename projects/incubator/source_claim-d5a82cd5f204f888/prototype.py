SOURCE_EXCERPT = 'arXiv:2610.29504v1 Announce Type: cross Abstract: Time series foundation models (TSFMs) perform unevenly across forecasting tasks. Recent work uses agentic model orchestration (AMO) to select or combine TSFMs, often outperforming individual forecasters. Yet these gains may reflect stronger or more complementary candidates rather than better orchestration. To disentangle these effects, we introduce FairAMO, a controlled evaluation protocol with fr'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
