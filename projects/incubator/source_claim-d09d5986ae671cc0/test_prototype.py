import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('Using a single Nano Banana image and Blender MCP, Gemini 4 Argon built a 3D Gothic cathedral in @Antigravity. It iterates on the geometry, textures, and lighting to create the finished scene. Media'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
