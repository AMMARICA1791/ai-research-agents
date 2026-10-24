SOURCE_EXCERPT = 'Article URL: https://www.theregister.com/ai-and-ml/2026/10/02/arxiv-imposes-rate-limit-on-paper-submissions-to-stem-the-ai-slop-tide/5300899 Comments URL: https://news.ycombinator.com/item?id=50224571 Points: 1 # Comments: 0'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
