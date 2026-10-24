SOURCE_EXCERPT = 'Article URL: https://www.ndw.jp/nintendo-interview-261023/ Comments URL: https://news.ycombinator.com/item?id=50220413 Points: 1 # Comments: 0'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
