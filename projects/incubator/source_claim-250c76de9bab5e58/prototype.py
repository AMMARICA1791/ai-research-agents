SOURCE_EXCERPT = 'Article URL: https://kouh.me/ai-text-detector Comments URL: https://news.ycombinator.com/item?id=50220254 Points: 5 # Comments: 7'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
