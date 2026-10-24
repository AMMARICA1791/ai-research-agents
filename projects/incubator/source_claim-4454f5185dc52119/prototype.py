SOURCE_EXCERPT = 'Article URL: https://medicalxpress.com/news/2026-10-ai-generalist-doctors-medical.html Comments URL: https://news.ycombinator.com/item?id=50220694 Points: 6 # Comments: 0'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
