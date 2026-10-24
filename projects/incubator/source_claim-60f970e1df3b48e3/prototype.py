SOURCE_EXCERPT = 'Naive byte-range caching can waste gigabytes of origin bandwidth on small requests. We rebuilt our cache architecture in Pingora to coordinate partial fetches automatically, cutting R2 p99 latency in half.'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
