# Claim Stress Lab — Decision gate

## Current evidence
- Software tests and a four-case **synthetic** baseline exercise the implementation.
- Two planted mechanical defects and two nondefective controls are **not** a scientific benchmark.
- 100% synthetic precision/recall (if CI confirms it) must never be described as real-world performance.
- Existing F-002 remains open. This project cannot repair missing independent semantic reviews.

## Before promoting beyond draft
1. Confirm the Claim Stress Lab workflow and Verify MVP are green on the **same current head commit**.
2. Run an independently curated, legally usable set of at least 30 source–claim–original-quote triples, including unsupported paraphrases, contradictory negations, false numerical claims, and supported paraphrases.
3. Blindly label the set before viewing tool flags. Record label provenance, denominator, TP/FP/FN/TN, precision, recall, and the number of unreviewable cases.
4. Compare against a simpler baseline: exact quote presence alone. Demonstrate improvement on the **same** cases, with uncertainty acknowledged.
5. Explicitly list false alarms and missed errors. If no measurable gain appears, archive as a negative experiment instead of merging into the core pipeline.

No autonomous publication, semantic truth score, or scientific novelty claim is authorized by this gate.

## Known adversarial blind spots
The synthetic probes in `adversarial_probes.py` show why lexical overlap cannot establish semantic entailment: a negation reversal and an association-to-causation leap can both pass the narrow mechanical checks. These are documented limitations, not independently sourced performance estimates. The evaluation must include such cases with separately recorded semantic labels; mechanical and semantic metrics must never be conflated.

## Gate status after official dataset acquisition (2026-10-23)

- **PASS — acquisition:** official AVeriTeC dev split, 500 claims, source SHA-256
  `499793726b4a5406780928a3d9dedc48d6dd53de778f22437d129cacdb08e300`;
  audited and sampled in GitHub Actions run 77.
- **PASS — software checks on acquisition commit:** Claim Stress Lab 77,
  Verify MVP 296.
- **OPEN — independent evaluation:** AVeriTeC's human claim-verdict labels
  are **not** independent labels of verbatim-quote defects. No 30 independently
  adjudicated source–claim–quote triples exist in this experiment.
- **OPEN — comparative evidence:** no real-data paired baseline comparison,
  uncertainty intervals, or audited FP/FN cases.
- **DECISION: HOLD.** Do not merge the experimental PR, publish an accuracy
  claim, or imply that downloading real claims validates quote detection.

The CI acquisition job now fails visibly if both sources are inaccessible,
rather than silently passing with a skipped real-data step. Temporary network
failure does not change the scientific decision gate.
