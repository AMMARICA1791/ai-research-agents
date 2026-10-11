"""Verify exact quoted passages against supplied, locally archived source texts.

This establishes text presence, NOT scientific entailment or source authenticity.
No network requests, PDF parsing, or model-based judgments are performed.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from research.evidence_claims import validate_claims


def _hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify_passages(payload: dict, source_dir: str | Path) -> dict:
    validate_claims(payload)
    root = Path(source_dir).resolve()
    sources = payload.get("source_texts")
    if not isinstance(sources, list) or len(sources) > 100:
        raise ValueError("Missing or invalid source text manifest")
    indexed = {}
    for item in sources:
        if not isinstance(item, dict) or not isinstance(item.get("doi"), str):
            raise ValueError("Invalid source text record")
        doi = item["doi"]
        if doi in indexed:
            raise ValueError("Duplicate source text DOI")
        name = item.get("file")
        expected = item.get("sha256")
        if not isinstance(name, str) or not name.endswith(".txt") or Path(name).name != name:
            raise ValueError("Source file must be a local flat .txt filename")
        if not isinstance(expected, str) or len(expected) != 64 or any(c not in "0123456789abcdef" for c in expected):
            raise ValueError("Invalid source text digest")
        path = (root / name).resolve()
        if not path.is_relative_to(root) or not path.is_file() or path.is_symlink():
            raise ValueError("Unsafe or missing source text")
        data = path.read_bytes()
        if len(data) > 2_000_000 or _hash(data) != expected:
            raise ValueError("Source text digest mismatch or size limit exceeded")
        indexed[doi] = data.decode("utf-8")
    findings = []
    for claim in payload["claims"]:
        for link in claim["evidence"]:
            doi = link["doi"]
            quote = link.get("quote")
            if not isinstance(quote, str) or not quote.strip() or len(quote) > 2000:
                raise ValueError("Evidence requires an exact nonempty quote")
            if doi not in indexed:
                raise ValueError("Evidence source text is not in manifest")
            matched = quote in indexed[doi]
            findings.append({
                "claim_id": claim["id"],
                "doi": doi,
                "locator": link["locator"],
                "quote_exact_match": matched,
                "scientific_support_verified": False,
                "review_required": True,
            })
    return {
        "status": "local_text_quote_screening",
        "findings": findings,
        "exact_match_count": sum(x["quote_exact_match"] for x in findings),
        "total_links": len(findings),
        "scientific_support_verified": False,
        "source_authenticity_verified": False,
    }


def main(argv=None) -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Verify cited quotes in locally archived UTF-8 texts")
    parser.add_argument("--input", required=True)
    parser.add_argument("--source-dir", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    result = verify_passages(json.loads(Path(args.input).read_text(encoding="utf-8")), args.source_dir)
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2, ensure_ascii=False, sort_keys=True)
        stream.write("\n")
    print(json.dumps({"exact_match_count": result["exact_match_count"], "total_links": result["total_links"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
