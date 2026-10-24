SOURCE_EXCERPT = 'Article URL: https://hanzo.blog/2026-10-16-your-ai-is-planning-to-kill-you/ Comments URL: https://news.ycombinator.com/item?id=50226160 Points: 1 # Comments: 0'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
