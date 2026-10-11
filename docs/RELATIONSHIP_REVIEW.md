# Evidence-to-claim relationship review

This is a **human-in-the-loop** logical relationship audit, not an automatic entailment model.

```sh
python -m research.relationship_review --input results/claims-with-reviews.json --source-dir private-archive --output results/relationship-audit.json
python -m pytest -q tests/test_relationship_review.py
```

Add `relationship_reviews` to the JSON accepted by `research.source_passage_verification`. Each reviewed item references `claim_id`, `doi`, and `locator` from the existing evidence link, and sets `review_status: "reviewed"`, `relation` (one of `supports`, `contradicts`, `insufficient`, `out_of_scope`), nonempty `rationale`, and a reviewer identifier. Missing reviews remain `pending`. A pending record must not assert any relation, rationale or reviewer.

Review cannot be accepted if the exact quoted passage is absent from the archived text. A quote match is still **not** proof of scientific support, authenticity, or semantic entailment. The machine never infers a relation: all decisions are explicitly supplied by reviewers and remain open to scientific challenge. Output always reports `machine_entailment_verified: false` and `scientific_support_verified: false`.

The next research stage may add a *non-authoritative* model-assisted triage layer with confidence calibration and blinded human evaluation. That work requires a defined evaluation dataset and must not silently promote model suggestions to scientific facts.
