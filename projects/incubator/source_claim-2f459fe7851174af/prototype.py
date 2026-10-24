SOURCE_EXCERPT = 'Article URL: https://medium.com/@ivan_43200/i-built-a-saas-with-ai-two-months-later-i-have-zero-active-users-1e93436a5b39 Comments URL: https://news.ycombinator.com/item?id=50223278 Points: 2 # Comments: 0'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
