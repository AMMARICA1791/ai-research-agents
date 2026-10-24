SOURCE_EXCERPT = 'Article URL: https://www.theatlantic.com/technology/2026/10/the-safe-internet-is-shrinking/689130/ Comments URL: https://news.ycombinator.com/item?id=50224973 Points: 3 # Comments: 0'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
