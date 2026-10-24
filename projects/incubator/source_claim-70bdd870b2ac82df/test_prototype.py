import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches("Cloudflare's new post-quantum GeoKey Manager protects geographically fenced decryption keys from harvest now, decrypt later attacks. Learn how we redesigned our cryptography stack to support strict data sovereignty in a post-quantum world."))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
