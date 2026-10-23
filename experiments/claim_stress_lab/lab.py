"""Claim Stress Lab: deterministic evidence perturbation, not semantic truth verification.

Usage: python -m experiments.claim_stress_lab.lab --input examples.json
Input is a JSON array of {"id", "claim", "quote", "source_text", "source_url"}.
No network, LLM, or external dependencies. Never publishes decisions.
"""
import argparse
import json
import re
from pathlib import Path

_WORD = re.compile(r"\b[\w]+\b", re.UNICODE)
_NUMBER = re.compile(r"(?<!\w)[+-]?\d+(?:[.,]\d+)?%?(?!\w)")


def tokens(value):
    return set(w.casefold() for w in _WORD.findall(value))


def evaluate(record):
    """Detect mechanically weak citations and test robustness to evidence removal.

    This is intentionally a diagnostic heuristic. A high score never proves entailment.
    """
    claim = record["claim"]
    quote = record["quote"]
    source = record["source_text"]
    if not all(isinstance(record.get(k), str) for k in
               ("claim", "quote", "source_text", "source_url")):
        raise ValueError("All evidence fields must be strings")
    quote_present = bool(quote.strip()) and quote in source
    claim_words = tokens(claim)
    quote_words = tokens(quote)
    overlap = len(claim_words & quote_words) / max(1, len(claim_words))
    claim_numbers = set(_NUMBER.findall(claim))
    quote_numbers = set(_NUMBER.findall(quote))
    unsupported_numbers = sorted(claim_numbers - quote_numbers)
    # Ablation: remove exactly the originally cited occurrence, not every matching phrase.
    ablated = source.replace(quote, "", 1) if quote_present else source
    residual_overlap = len(claim_words & tokens(ablated)) / max(1, len(claim_words))
    flags = []
    if not quote_present:
        flags.append("QUOTE_NOT_VERBATIM_IN_SOURCE")
    if unsupported_numbers:
        flags.append("CLAIM_NUMBERS_ABSENT_FROM_QUOTE")
    if overlap < 0.35:
        flags.append("LOW_CLAIM_QUOTE_LEXICAL_OVERLAP")
    if quote_present and residual_overlap >= overlap:
        flags.append("ABLATION_DOES_NOT_REDUCE_LEXICAL_SUPPORT")
    return {
        "id": record.get("id"),
        "source_url": record["source_url"],
        "quote_present": quote_present,
        "claim_quote_overlap": round(overlap, 3),
        "ablated_source_overlap": round(residual_overlap, 3),
        "unsupported_claim_numbers": unsupported_numbers,
        "flags": flags,
        "semantic_accuracy": None,
        "publication_allowed": False,
        "review_required": True,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    records = json.loads(args.input.read_text(encoding="utf-8"))
    if not isinstance(records, list):
        parser.error("Input must be a JSON array")
    results = [evaluate(record) for record in records]
    output = json.dumps({"schema_version": 1, "results": results},
                        indent=2, ensure_ascii=False)
    if args.output:
        args.output.write_text(output + "\n", encoding="utf-8")
    else:
        print(output)


if __name__ == "__main__":
    main()
