import unittest
from prototype import validate
class Tests(unittest.TestCase):
    def test_unknown_rejected(self):
        self.assertFalse(validate({"type":"run_shell","params":{"cmd":"echo hi"}}))
    def test_known_accepted(self):
        self.assertTrue(validate({"type":"summarize","params":{"text":"hello"}}))
