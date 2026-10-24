SOURCE_EXCERPT = 'Article URL: https://twitter.com/rynorhn/status/2113757656498196605 Comments URL: https://news.ycombinator.com/item?id=50224890 Points: 2 # Comments: 0'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
