SOURCE_EXCERPT = 'Article URL: https://www.youtube.com/watch?v=NyOeLB0WVNE Comments URL: https://news.ycombinator.com/item?id=50224121 Points: 3 # Comments: 3'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
