SOURCE_EXCERPT = 'Article URL: https://www.shuffle-on.com/ Comments URL: https://news.ycombinator.com/item?id=50223151 Points: 2 # Comments: 0'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
