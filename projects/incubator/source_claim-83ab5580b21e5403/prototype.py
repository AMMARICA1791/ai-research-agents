SOURCE_EXCERPT = 'Article URL: https://github.com/tensemem/tensemem Comments URL: https://news.ycombinator.com/item?id=50221670 Points: 1 # Comments: 0'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
