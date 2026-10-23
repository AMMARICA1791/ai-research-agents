import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('arXiv:2610.21449v2 Announce Type: replace Abstract: Large language models (LLMs) can reason over both structured measurements and free-text records, which makes them attractive for emergency department (ED) prediction. However, most existing LLMs still fall short of conventional ML methods like trees on EHR-based prediction tasks. Our controlled analysis traces this gap to two weaknesses: LLMs do not select informative features, and they misjudge'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
