import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('Thank you @SPARC_NA for interviewing arXiv for #OAWeek! arXiv&apos;s CEO chatted with SPARC about the cost of knowledge &amp; what it takes to operate an essential open infrastructure in today&apos;s rapidly changing research landscape. Read the full profile here: https://www.openaccessweek.org/theme-profiles/arxiv'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
