SOURCE_EXCERPT = 'arXiv:2610.30307v1 Announce Type: cross Abstract: AI coding agents could change whether organizations buy software or build the functionality they need. We focus on organizations and professional buyers whose domain knowledge can help them specify and evaluate tools for their work. We define the software substitution frontier as the functions customers could build and maintain at an acceptable standard for less than buying them. Using public data'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
