SOURCE_EXCERPT = "You too can get rich quick in real estate --- details in this book; only $49.95. If there really was a sure fire way to get rich quick, why sell books to the public? Why not keep it to yourself and apply it to make money? The same applies to AI. If it was really all that, they wouldn't be selling tokens to the public. They would be forming corporate partnerships, building products and conquering markets --- starting with the financial markets. Th"
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
