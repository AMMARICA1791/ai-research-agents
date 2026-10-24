import json
import tempfile
import unittest
from pathlib import Path
from experiments.rapid_project_radar.anticipate import generate

class EverySignalProjectTests(unittest.TestCase):
    def test_untagged_signal_gets_project(self):
        with tempfile.TemporaryDirectory() as directory:
            result = generate({"signals": [
                {"id": "abcdef0123456789", "title": "Unclassified research",
                 "url": "https://example.org/research",
                 "signal": {"score": 0, "topics": {}}}
            ]}, directory)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]["topic"], "signal_trace")
            project = Path(result[0]["path"])
            self.assertTrue((project / "test_prototype.py").exists())
            self.assertEqual(json.loads((project / "hypothesis.json").read_text())["source_url"],
                             "https://example.org/research")

if __name__ == "__main__":
    unittest.main()
