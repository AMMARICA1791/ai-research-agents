# Research infrastructure integration — first bounded vertical slice

This experimental command connects **Crossref metadata discovery → deterministic evidence ledger → persistent SQLite memory → source-linked JSON report**. It does not claim literature review, independent agents, scientific contradiction detection, or verified scientific conclusions.

## Reproduce

With an existing valid public Crossref discovery JSON:

```sh
python -m research.integration_pipeline --input results/research-explorer/records.json --db results/research-memory.sqlite3 --output results/research-integration/report.json
python -m pytest -q tests/test_research_integration.py
```

Or perform live public metadata discovery:

```sh
python -m research.integration_pipeline --question "open weight model evaluation"
```

The offline command does not fetch from the internet. The live command contacts only Crossref through the existing bounded discovery implementation. Do not enter confidential research questions. Output includes original provider endpoint, retrieval timestamp, response digest, evidence-ledger digest, and explicit unverified status. A second run against the same database can show **changes in bibliographic metadata** for a DOI, not scientific disagreement.

## Release gates still outstanding

- End-to-end CI and review for this PR; no automatic merge.
- Failure recovery, backups, migration and secure multi-user storage.
- Structured scientific claims, independent source review, contradictions with evidence, actual agent attribution, and reproducible model experiments.
- Production interface and end-to-end independent reproducibility.

This is the **first integrated research infrastructure slice**, not completion of the entire research center.
