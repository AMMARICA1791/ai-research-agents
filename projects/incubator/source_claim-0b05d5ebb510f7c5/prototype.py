SOURCE_EXCERPT = 'Consensus uses GPT-5 and OpenAI’s Responses API to power a multi-agent research assistant that reads, analyzes, and synthesizes evidence in minutes—helping over 8 million researchers accelerate scientific discovery.'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
