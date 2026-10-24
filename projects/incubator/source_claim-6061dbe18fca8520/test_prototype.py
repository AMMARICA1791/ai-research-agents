import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('I could never get used to FreeCAD, so I built my own. It turns out Claude is really good at using it. Loböle is a parametric B-Rep CAD built on OpenCASCADE and Vulkan, with sketches, assemblies, drawings, FEM and CAM. The GUI, Python scripts and AI agents all go through the same commands, so an agent can do anything you can in the GUI. The engine, watch and bicycle in the README were each built by Claude writing a script against it. Comments URL:'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
