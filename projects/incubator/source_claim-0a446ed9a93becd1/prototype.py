SOURCE_EXCERPT = 'Article URL: https://www.uxness.in/2026/08/top-ux-conferences-to-attend-in-2027.html Comments URL: https://news.ycombinator.com/item?id=50225094 Points: 3 # Comments: 0'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
