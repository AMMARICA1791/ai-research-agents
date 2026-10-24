SOURCE_EXCERPT = 'Article URL: https://github.com/Lucki74/draggy Comments URL: https://news.ycombinator.com/item?id=50220255 Points: 1 # Comments: 0'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
