SOURCE_EXCERPT = 'Article URL: https://stevekrouse.com/10x Comments URL: https://news.ycombinator.com/item?id=50221446 Points: 3 # Comments: 2'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
