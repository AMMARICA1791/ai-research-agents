SOURCE_EXCERPT = 'Article URL: https://torrentfreak.com/ai-assisted-paper-on-z-library-cites-a-torrentfreak-article-that-doesnt-exist/ Comments URL: https://news.ycombinator.com/item?id=50220204 Points: 56 # Comments: 17'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
