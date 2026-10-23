SOURCE_EXCERPT = 'Learn how OpenAI protects user data when AI agents open links, preventing URL-based data exfiltration and prompt injection with built-in safeguards.'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
