import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('We just open-sourced 1,300+ 3D models. That&apos;s 39 GB of 3D files, free to download on Hugging Face. http://huggingface.co/datasets/scenario-labs/3d-collection &gt; Hitem3D, Meshy, Rodin, Tripo, Claude Opus 5.5 3D and GPT-6 Astra 3D, all run on Scenario &gt; every example ships its input image, prompt and exact settings &gt; GLB up to 8K textures, native Blender files from Opus and Astra, CC BY 4.0 Media'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
