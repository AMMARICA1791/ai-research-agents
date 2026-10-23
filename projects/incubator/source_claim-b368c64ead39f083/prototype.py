SOURCE_EXCERPT = "arXiv:2604.24920v4 Announce Type: replace-cross Abstract: Agentic systems now act with user secrets for APIs, messaging platforms, and cloud services. Today's agent runtimes typically implement authorization by exposure: enabling action means placing a reusable secret, or a reusable artifact derived from it, inside the runtime, so a transient prompt-injection or tool-side compromise becomes durable account compromise. Existing defenses cover adja"
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
