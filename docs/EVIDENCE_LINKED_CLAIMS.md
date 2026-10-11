# Evidence-linked claims and conflict candidates

This **experimental** layer accepts a JSON object with `schema_version: 1`, a digest-linked evidence `ledger`, and up to 100 explicitly entered `claims`. Each claim has a stable ID, proposition, comparison scope, review status (`unreviewed` or `human_reviewed`), and 1–20 evidence links (DOI, locator, stance: `supports`, `refutes`, or `unclear`).

```sh
python -m research.evidence_claims --input results/claims.json --output results/conflict-candidates.json
python -m pytest -q tests/test_evidence_claims.py
```

The scanner flags **candidate** conflicts only when explicit support and refutation refer to the same normalized proposition and comparison scope. Title, author, date and other bibliographic metadata differences are **not** classified as scientific conflicts. Different population/time scopes are not conflated.

## Scientific limitations

- All stances and locators are **user-supplied annotations**. The software does not read papers, validate the quoted passage, establish causality, compare statistical uncertainty, or authenticate source metadata.
- A DOI in the ledger is only a bibliographic identifier, **not proof** of a claim. A stored digest detects local changes, **not provenance authenticity**.
- A candidate must be reviewed by a domain expert before describing it as a verified scientific contradiction. The output always marks `scientific_contradiction_verified: false`.
- This first slice is a deterministic, bounded foundation for later provenance validation, full-text passage verification, semantic equivalence, and human adjudication.
