SOURCE_EXCERPT = 'Article URL: https://playgama.ai/play/xl6duef7p3 Comments URL: https://news.ycombinator.com/item?id=50223798 Points: 2 # Comments: 0'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
