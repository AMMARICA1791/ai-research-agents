"""Verify official FEVER file integrity using published Zenodo MD5 checksums.

Checksums verify file bytes, not scientific validity or independent labels.
"""
import argparse
import hashlib
import json
from pathlib import Path

ZENODO_RECORD = "https://zenodo.org/records/4925954"
EXPECTED_MD5 = {
    "paper_dev.jsonl": "0343eb51f4ca70ee91df152ac559034a",
    "paper_test.jsonl": "2f2c122972f77af033f43574e2039093",
    "shared_task_dev.jsonl": "4eecc1018b3d2bd46089ca36d886f439",
    "shared_task_dev_public.jsonl": "64e6caa55826df21fcb8fcc70d9d5905",
    "shared_task_test.jsonl": "490f59afb5123620ac37f78572cd0528",
    "train.jsonl": "2216e2f367e223bf3e593a119222d99d",
    "wiki-pages.zip": "ed8bfd894a2c47045dca61f0c8dc4c07",
}


def verify(path):
    path = Path(path)
    expected = EXPECTED_MD5.get(path.name)
    if expected is None:
        raise ValueError("Unrecognized FEVER filename; cannot verify against Zenodo manifest")
    digest = hashlib.md5()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    actual = digest.hexdigest()
    return {"file": path.name, "source": ZENODO_RECORD, "expected_md5": expected,
            "actual_md5": actual, "integrity_ok": actual == expected,
            "scientific_validation": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", type=Path)
    args = parser.parse_args()
    reports = [verify(path) for path in args.files]
    print(json.dumps(reports, indent=2))
    if not all(report["integrity_ok"] for report in reports):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
