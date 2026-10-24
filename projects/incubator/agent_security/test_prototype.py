import unittest
from prototype import evaluate
class PrototypeTests(unittest.TestCase):
    def test_denies_unapproved(self):
        self.assertFalse(evaluate({"explicit_approval": False, "trusted_origin": "user"}))
    def test_allows_approved(self):
        self.assertTrue(evaluate({"explicit_approval": True, "trusted_origin": "user"}))
if __name__ == "__main__":
    unittest.main()
