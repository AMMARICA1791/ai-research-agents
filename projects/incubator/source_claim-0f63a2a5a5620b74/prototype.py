SOURCE_EXCERPT = 'Article URL: https://news.ycombinator.com/ Comments URL: https://news.ycombinator.com/item?id=50223294 Points: 1 # Comments: 0'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
