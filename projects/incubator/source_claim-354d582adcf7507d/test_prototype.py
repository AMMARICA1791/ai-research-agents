import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('arXiv:2609.20010v5 Announce Type: replace-cross Abstract: Cross-chain protocols enable applications to exchange messages across blockchains. Under point-to-point configurations, communication depends on a direct connection between the source and destination blockchains, limiting blockchain reachability and requiring additional configurations to connect more blockchains. To quantify this problem, this paper analyzes approximately 25 million mainne'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
