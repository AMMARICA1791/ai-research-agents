SOURCE_EXCERPT = 'Article URL: https://rentry.co/themis-docket-e61b189e37 Comments URL: https://news.ycombinator.com/item?id=50222576 Points: 4 # Comments: 0'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
