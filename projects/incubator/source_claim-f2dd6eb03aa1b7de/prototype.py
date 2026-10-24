SOURCE_EXCERPT = 'Article URL: https://tylertringas.com/ai-legal/ Comments URL: https://news.ycombinator.com/item?id=50221750 Points: 1 # Comments: 0'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
