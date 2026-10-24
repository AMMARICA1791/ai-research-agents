SOURCE_EXCERPT = 'Article URL: https://github.com/Aldyernesto/shotstash Comments URL: https://news.ycombinator.com/item?id=50221460 Points: 2 # Comments: 0'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
