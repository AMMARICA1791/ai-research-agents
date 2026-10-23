import unittest
from experiments.evidence_drift_watch.lab import inspect

class DriftTests(unittest.TestCase):
    def test_lost_quote(self):
        r=inspect("A claim is supported","A claim is disputed",["supported"])
        self.assertTrue(r["changed"])
        self.assertTrue(r["quote_checks"][0]["lost"])
        self.assertIsNone(r["semantic_validity"])
        self.assertFalse(r["publication_allowed"])
    def test_whitespace_only(self):
        r=inspect("hello  world","hello world",["hello world"])
        self.assertTrue(r["changed"])
        self.assertFalse(r["normalized_changed"])
        self.assertFalse(r["quote_checks"][0]["lost"])
    def test_same_snapshot(self):
        self.assertFalse(inspect("a","a",[])["changed"])
    def test_invalid_quotes(self):
        with self.assertRaises(ValueError): inspect("a","b",[""])
