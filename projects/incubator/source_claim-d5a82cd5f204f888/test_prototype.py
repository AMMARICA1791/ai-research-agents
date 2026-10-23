import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('arXiv:2610.29504v1 Announce Type: cross Abstract: Time series foundation models (TSFMs) perform unevenly across forecasting tasks. Recent work uses agentic model orchestration (AMO) to select or combine TSFMs, often outperforming individual forecasters. Yet these gains may reflect stronger or more complementary candidates rather than better orchestration. To disentangle these effects, we introduce FairAMO, a controlled evaluation protocol with fr'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
