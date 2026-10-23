import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from experiments.claim_stress_lab.verify_fever_files import verify


class FeverIntegrityTests(unittest.TestCase):
    def test_corrupt_or_unrelated_bytes_fail_integrity(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "paper_dev.jsonl"
            path.write_bytes(b"not the official dataset")
            result = verify(path)
        self.assertFalse(result["integrity_ok"])
        self.assertFalse(result["scientific_validation"])

    def test_known_matching_checksum_passes_byte_identity_only(self):
        sample = b"local synthetic fixture"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "paper_dev.jsonl"
            path.write_bytes(sample)
            with patch.dict("experiments.claim_stress_lab.verify_fever_files.EXPECTED_MD5",
                            {"paper_dev.jsonl": hashlib.md5(sample).hexdigest()}):
                result = verify(path)
        self.assertTrue(result["integrity_ok"])
        self.assertFalse(result["scientific_validation"])

    def test_unknown_filename_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "untrusted.jsonl"
            path.write_bytes(b"anything")
            with self.assertRaises(ValueError):
                verify(path)


if __name__ == "__main__":
    unittest.main()
