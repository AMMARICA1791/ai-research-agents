"""Fetch a compact public AVeriTeC JSON file with bounded time and size.

Acquisition is optional and never turns claim verdicts into quote labels.
"""
import argparse
import hashlib
import json
import urllib.request
from pathlib import Path

SOURCES = (
    "https://raw.githubusercontent.com/MichSchli/AVeriTeC/main/data/dev.json",
    "https://huggingface.co/chenxwh/AVeriTeC/resolve/main/data/dev.json",
)
MAX_BYTES = 12 * 1024 * 1024


def acquire(output, sources=SOURCES):
    failures = []
    for url in sources:
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "claim-stress-lab/0.1"})
            with urllib.request.urlopen(request, timeout=20) as response:
                if response.status != 200:
                    raise ValueError(f"HTTP {response.status}")
                data = response.read(MAX_BYTES + 1)
            if len(data) > MAX_BYTES:
                raise ValueError("Dataset exceeds configured size limit")
            records = json.loads(data)
            if not isinstance(records, list) or not records or not all(
                isinstance(row, dict) and isinstance(row.get("claim"), str) for row in records
            ):
                raise ValueError("Invalid AVeriTeC JSON records")
            output = Path(output)
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(data)
            return {"downloaded": True, "url": url, "bytes": len(data),
                    "sha256": hashlib.sha256(data).hexdigest(), "claims": len(records),
                    "independent_quote_defect_labels": False}
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            failures.append({"url": url, "error": type(exc).__name__})
    return {"downloaded": False, "failures": failures,
            "independent_quote_defect_labels": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = acquire(args.output)
    print(json.dumps(result, indent=2))
    if not result["downloaded"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
