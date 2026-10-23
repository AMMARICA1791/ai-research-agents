SOURCE_EXCERPT = 'arXiv:2610.28667v1 Announce Type: cross Abstract: Coding agents can now implement a specification, write and run tests, repair failures, and declare the result ready for release. When the same agentic system produces both the software and the evidence of its correctness, a passing test suite is no longer independent evidence: visible tests become an optimization target, code and tests may share one misinterpretation of the specification, and the '
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
