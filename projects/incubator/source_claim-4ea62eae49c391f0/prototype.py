SOURCE_EXCERPT = 'Article URL: https://www.militarytimes.com/industry/techwatch/2026/10/23/us-air-force-wants-ai-to-assist-aerial-refueling/ Comments URL: https://news.ycombinator.com/item?id=50221226 Points: 2 # Comments: 1'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
