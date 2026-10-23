SOURCE_EXCERPT = 'arXiv:2609.20010v5 Announce Type: replace-cross Abstract: Cross-chain protocols enable applications to exchange messages across blockchains. Under point-to-point configurations, communication depends on a direct connection between the source and destination blockchains, limiting blockchain reachability and requiring additional configurations to connect more blockchains. To quantify this problem, this paper analyzes approximately 25 million mainne'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
