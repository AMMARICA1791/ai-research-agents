SOURCE_EXCERPT = 'OpenAI is strengthening ChatGPT Atlas against prompt injection attacks using automated red teaming trained with reinforcement learning. This proactive discover-and-patch loop helps identify novel exploits early and harden the browser agent’s defenses as AI becomes more agentic.'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
