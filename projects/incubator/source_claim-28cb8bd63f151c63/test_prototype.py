import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('arXiv:2610.30307v1 Announce Type: cross Abstract: AI coding agents could change whether organizations buy software or build the functionality they need. We focus on organizations and professional buyers whose domain knowledge can help them specify and evaluate tools for their work. We define the software substitution frontier as the functions customers could build and maintain at an acceptable standard for less than buying them. Using public data'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
