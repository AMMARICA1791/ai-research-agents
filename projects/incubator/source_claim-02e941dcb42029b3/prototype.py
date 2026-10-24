SOURCE_EXCERPT = 'Article URL: https://arxiv.org/abs/2610.29162 Comments URL: https://news.ycombinator.com/item?id=50223647 Points: 2 # Comments: 0'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
