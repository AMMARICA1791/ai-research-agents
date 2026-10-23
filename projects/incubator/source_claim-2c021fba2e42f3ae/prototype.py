SOURCE_EXCERPT = 'arXiv:2609.22486v2 Announce Type: replace-cross Abstract: Large language models (LLMs) increasingly ground their answers in proprietary data and live web content through both single-shot retrieval-augmented generation (RAG) and multi-turn agentic search. Yet the web path they use was built for human readers: search services return URLs and snippets ranked by generic relevance, and content delivery networks (CDNs) cache URL-addressed objects witho'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
