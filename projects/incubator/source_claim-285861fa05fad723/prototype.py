SOURCE_EXCERPT = 'Article URL: https://www.technologyreview.com/2026/10/22/1146103/the-foundations-of-scalable-ai/ Comments URL: https://news.ycombinator.com/item?id=50220098 Points: 2 # Comments: 0'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
