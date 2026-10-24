SOURCE_EXCERPT = 'Article URL: https://www.lesswrong.com/posts/ywrgeAPMn83FxzFBk/how-could-the-us-and-china-verifiably-slow-ai Comments URL: https://news.ycombinator.com/item?id=50222975 Points: 1 # Comments: 0'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
