# Research evidence ledger — experimental prototype

This module converts an existing, bounded Crossref metadata inventory into a deterministic, source-linked JSON ledger. It does **not** fetch papers, validate scientific claims, run an AI model, or execute external code.

## Reproduce

First run the [scholarly discovery](SCHOLARLY_DISCOVERY.md) command to create a metadata inventory, then:

```sh
python -m research.evidence_ledger --input results/scholarly-discovery/records.json --output results/scholarly-discovery/evidence-ledger.json
python -m pytest -q tests/test_evidence_ledger.py
```

Each entry contains DOI, source response digest, and an explicit unreviewed status. The overall ledger digest is a deterministic SHA-256 over canonical JSON excluding the digest itself. This is an **integrity identifier**, not a digital signature or proof of the original publisher's accuracy.

The module rejects missing provenance, non-UTC timestamps, inconsistent counts, duplicate DOIs and invalid records. It is not a general knowledge memory system; versioned storage, verification against provider responses, and independent review are later gates. Public artifacts must contain only non-sensitive topics.
