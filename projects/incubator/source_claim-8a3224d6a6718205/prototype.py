SOURCE_EXCERPT = 'Article URL: https://mantid.dev Comments URL: https://news.ycombinator.com/item?id=50220773 Points: 1 # Comments: 1'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
