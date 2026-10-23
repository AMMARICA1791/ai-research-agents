import unittest
from experiments.agent_market_gap_register.lab import inspect,evaluate

class MarketGapTests(unittest.TestCase):
    def test_complete_is_only_ready_for_discovery(self):
        row=dict(problem="Agents lack delegated approval",buyer="Web platform",
                 current_workaround="manual review",falsifiable_test="test ten workflows",
                 success_metric="false approvals below baseline",competitors="existing gateways",
                 evidence=[{"url":"https://www.w3.org/","observation":"Agent consent is discussed"}])
        r=inspect(row)
        self.assertTrue(r["ready_for_customer_discovery"])
        self.assertFalse(r["buyer_demand_verified"])
        self.assertFalse(r["novelty_verified"])
    def test_no_evidence(self):
        self.assertFalse(inspect({})["ready_for_customer_discovery"])
    def test_reject_non_https(self):
        r=inspect({"evidence":[{"url":"http://example.org","observation":"x"}]})
        self.assertEqual(r["evidence_count"],0)
    def test_invalid_evidence(self):
        with self.assertRaises(TypeError): inspect({"evidence":"url"})
    def test_empty_portfolio(self):
        self.assertEqual(evaluate([])["items"],[])
