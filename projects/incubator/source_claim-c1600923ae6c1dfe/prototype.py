SOURCE_EXCERPT = 'Article URL: https://ricuicui.com/articles/navigateur-porte-entree-agents-ia Comments URL: https://news.ycombinator.com/item?id=50222824 Points: 2 # Comments: 0'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
