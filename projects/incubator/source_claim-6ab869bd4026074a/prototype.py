SOURCE_EXCERPT = 'Article URL: https://aitrendvideo.net Comments URL: https://news.ycombinator.com/item?id=50223635 Points: 1 # Comments: 1'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
