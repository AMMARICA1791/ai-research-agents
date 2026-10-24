SOURCE_EXCERPT = 'Article URL: https://www.barrons.com/articles/ai-chip-stocks-cybersecurity-crowdstrike-palo-alto-056aaea8 Comments URL: https://news.ycombinator.com/item?id=50223705 Points: 1 # Comments: 0'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
