SOURCE_EXCERPT = 'Article URL: https://substack.norabble.com/p/ai-safety-is-all-hands-on-deck Comments URL: https://news.ycombinator.com/item?id=50220831 Points: 2 # Comments: 0'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
