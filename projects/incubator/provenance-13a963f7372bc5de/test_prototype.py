import unittest
from prototype import snapshot, drift
class Tests(unittest.TestCase):
    def test_quote_disappears(self):
        old = snapshot("Research supports claim", "supports claim")
        self.assertTrue(drift(old, "Research updated", "supports claim")["quote_disappeared"])
    def test_no_change(self):
        old = snapshot("stable", "stable")
        self.assertFalse(drift(old, "stable", "stable")["content_changed"])
