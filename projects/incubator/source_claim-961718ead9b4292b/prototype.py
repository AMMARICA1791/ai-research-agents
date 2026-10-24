SOURCE_EXCERPT = 'Article URL: https://www.optimallyirrational.com/p/will-ai-stop-us-getting-ripped-off Comments URL: https://news.ycombinator.com/item?id=50224591 Points: 1 # Comments: 0'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
