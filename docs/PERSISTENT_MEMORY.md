# Persistent research memory — experimental Phase 1

This is a **local SQLite evidence snapshot store**, not an autonomous research agent, semantic retrieval engine, verified literature review or production knowledge service. It only ingests the existing bounded, validated Crossref metadata reports via `research.evidence_ledger.build_ledger`. It uses Python's standard library and no credentials or network access.

## Reproduce (Python 3.11+)

Generate a public report using the existing [scholarly discovery](SCHOLARLY_DISCOVERY.md) procedure. Then run:

```sh
python -m research.persistent_memory --db results/research-memory.sqlite3 ingest --input results/scholarly-discovery/records.json
python -m research.persistent_memory --db results/research-memory.sqlite3 history --doi 10.1234/example
python -m pytest -q tests/test_persistent_memory.py
```

Replace the example DOI with one returned by the discovery report. Re-ingesting the exact report is idempotent. A new observation of the same DOI is stored as a separate immutable snapshot, preserving its UTC retrieval time and source response digest. Queries are exact DOI lookups and use SQL parameters. Data stays in the chosen local database file; it is **not** automatically synced between GitHub Actions runs or devices.

## Limits and next gates

- The ledger SHA-256 is an integrity identifier, **not** a signature or scientific validation.
- Only metadata and explicit `scientific_claim_verified: false` status are persisted. No paper content is reviewed.
- Database backup, retention, access control, multi-user synchronization, schema migration, corruption recovery, and independent scientific review are **not implemented**.
- Use only public, non-sensitive research questions and evidence. Never commit local SQLite databases containing private material.
- Run CI, review code and test recovery from database failures before merging this experimental branch into `main`.
