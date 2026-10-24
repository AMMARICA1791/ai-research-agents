SOURCE_EXCERPT = 'Article URL: https://botchelor.com/gate?from=%2Fagents Comments URL: https://news.ycombinator.com/item?id=50223284 Points: 1 # Comments: 0'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
