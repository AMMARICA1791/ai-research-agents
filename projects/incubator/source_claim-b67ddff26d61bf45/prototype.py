SOURCE_EXCERPT = 'Article URL: https://deallocatedobjects.com/posts/making-my-blog-readable-by-ai-agents Comments URL: https://news.ycombinator.com/item?id=50225443 Points: 1 # Comments: 0'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
