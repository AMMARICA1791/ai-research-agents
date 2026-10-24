SOURCE_EXCERPT = 'Article URL: https://www.axios.com/2026/10/23/ai-economic-research-analysis Comments URL: https://news.ycombinator.com/item?id=50225125 Points: 1 # Comments: 0'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
