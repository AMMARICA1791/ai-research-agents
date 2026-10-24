SOURCE_EXCERPT = 'Article URL: https://www.polygon.com/super-mario-bros-shigeru-miyamoto-ai-order-culture-japan-award-nintendo/ Comments URL: https://news.ycombinator.com/item?id=50220182 Points: 2 # Comments: 0'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
