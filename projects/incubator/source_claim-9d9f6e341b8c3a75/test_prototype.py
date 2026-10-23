import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('arXiv:2610.28667v1 Announce Type: cross Abstract: Coding agents can now implement a specification, write and run tests, repair failures, and declare the result ready for release. When the same agentic system produces both the software and the evidence of its correctness, a passing test suite is no longer independent evidence: visible tests become an optimization target, code and tests may share one misinterpretation of the specification, and the '))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
