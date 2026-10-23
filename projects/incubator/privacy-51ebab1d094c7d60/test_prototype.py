import unittest
from prototype import redact
class Tests(unittest.TestCase):
    def test_secret(self):
        self.assertNotIn("abcd123456", redact("token=abcd123456"))
    def test_email(self):
        self.assertEqual(redact("hello me@example.org"), "hello [REDACTED]")
