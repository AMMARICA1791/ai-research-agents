import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from experiments.claim_stress_lab.acquire_averitec import acquire


class AcquisitionTests(unittest.TestCase):
    def test_all_sources_unavailable_does_not_create_fake_dataset(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / "dev.json"
            with patch("experiments.claim_stress_lab.acquire_averitec.urllib.request.urlopen",
                       side_effect=OSError("offline")):
                report = acquire(target, sources=("https://example.org/a", "https://example.org/b"))
            self.assertFalse(report["downloaded"])
            self.assertEqual(len(report["failures"]), 2)
            self.assertFalse(target.exists())

    def test_valid_json_is_saved(self):
        data = json.dumps([{"claim": "Test", "label": "Supported"}]).encode()
        class FakeResponse:
            status = 200
            def __enter__(self):
                return self
            def __exit__(self, *args):
                return False
            def read(self, size):
                return data
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / "dev.json"
            with patch("experiments.claim_stress_lab.acquire_averitec.urllib.request.urlopen",
                       return_value=FakeResponse()):
                report = acquire(target, sources=("https://example.org/test",))
            self.assertTrue(report["downloaded"])
            self.assertEqual(json.loads(target.read_text())[0]["claim"], "Test")
            self.assertFalse(report["independent_quote_defect_labels"])


if __name__ == "__main__":
    unittest.main()
