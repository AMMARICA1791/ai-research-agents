SOURCE_EXCERPT = 'Article URL: https://www.uxness.in/2026/10/ux-research-for-ai-products-ai-native-research-lifecycle.html Comments URL: https://news.ycombinator.com/item?id=50221693 Points: 1 # Comments: 0'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
