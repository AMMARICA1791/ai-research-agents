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
