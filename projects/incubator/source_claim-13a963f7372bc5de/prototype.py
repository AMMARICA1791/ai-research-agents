SOURCE_EXCERPT = 'arXiv:2610.30645v1 Announce Type: cross Abstract: Quantum key distribution (QKD), whose security is derived from quantum mechanics rather than computational assumptions, is moving into standardization and commercial deployment. Yet its security guarantees rest on technically delicate proofs checked by hand. Formal verification closes this gap, establishing a two-factor assurance: unconditional security from physical principles, and machine-checke'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
