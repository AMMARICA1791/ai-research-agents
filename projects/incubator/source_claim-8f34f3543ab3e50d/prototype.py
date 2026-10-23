SOURCE_EXCERPT = 'arXiv:2610.28655v1 Announce Type: cross Abstract: Publishers and funders increasingly ask authors to disclose how AI tools contributed to a piece of research. In computational work the repository is where an author or an auditor would look for the answer, and we ask what it can actually supply. We audit two single-investigator repositories by the same author in the same field, each carrying a different class of agent residue: a prescriptive trace'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
