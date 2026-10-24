SOURCE_EXCERPT = 'Article URL: https://homepage.farm/ai.html Comments URL: https://news.ycombinator.com/item?id=50220640 Points: 5 # Comments: 0'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
