SOURCE_EXCERPT = 'Article URL: https://github.com/sevenboxlabs/sevenbox Comments URL: https://news.ycombinator.com/item?id=50225322 Points: 2 # Comments: 0'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
