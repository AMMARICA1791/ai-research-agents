SOURCE_EXCERPT = 'arXiv:2610.30193v1 Announce Type: new Abstract: Retrieval-augmented generation (RAG) systems face security, privacy, and copyright risks including content leakage, source reconstruction, unauthorized access, data poisoning, and prompt injection. Yet RAG protection studies use incompatible evaluation metrics, datasets, and threat models. We present a systematic survey and human-coded evidence map of 118 full-text-confirmed RAG defense papers, orga'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
