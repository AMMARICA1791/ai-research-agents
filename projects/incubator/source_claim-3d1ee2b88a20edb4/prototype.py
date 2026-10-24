SOURCE_EXCERPT = 'Article URL: https://www.construction-physics.com/p/reading-list-102426 Comments URL: https://news.ycombinator.com/item?id=50220547 Points: 1 # Comments: 0'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
