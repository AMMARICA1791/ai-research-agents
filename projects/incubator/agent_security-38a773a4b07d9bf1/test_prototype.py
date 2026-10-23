import unittest
from prototype import evaluate
class Tests(unittest.TestCase):
    def test_denies_untrusted(self):
        self.assertFalse(evaluate({"explicit_approval": True, "trusted_origin": "web"}))
    def test_allows_approved(self):
        self.assertTrue(evaluate({"explicit_approval": True, "trusted_origin": "user"}))
