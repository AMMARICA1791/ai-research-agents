SOURCE_EXCERPT = 'Article URL: https://faillearnrepeat.net/blog/from-swe-to-ai-research/ Comments URL: https://news.ycombinator.com/item?id=50222088 Points: 1 # Comments: 0'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
