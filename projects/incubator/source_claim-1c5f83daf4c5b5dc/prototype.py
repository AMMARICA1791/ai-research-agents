SOURCE_EXCERPT = "Almost 100,000 Commerce.com domains now give AI agents real shopping tools through WebMCP on Cloudflare. Here's how we turned it on across every store at once, while keeping each merchant in control."
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
