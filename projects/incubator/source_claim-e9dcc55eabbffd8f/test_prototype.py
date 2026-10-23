import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('arXiv:2610.31130v1 Announce Type: cross Abstract: Offline tests can fail to reveal whether an agent update will remain safe after deployment. We operationalize this post-audit mirage using matched safe and harmful lifecycles that expose identical verifier-visible evidence while an isolated scorer records opposite deployment truth. Our theorem applies standard observational-equivalence and indistinguishability ideas to this executable audit bounda'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
