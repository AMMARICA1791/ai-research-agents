SOURCE_EXCERPT = 'This system card outlines the comprehensive safety measures implemented for GPT‑5.1-CodexMax. It details both model-level mitigations, such as specialized safety training for harmful tasks and prompt injections, and product-level mitigations like agent sandboxing and configurable network access.'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
