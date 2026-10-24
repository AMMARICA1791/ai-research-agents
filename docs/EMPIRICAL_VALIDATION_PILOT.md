# Empirical validation track — pilot phase

## Why this exists
The external technical review found that successful scaffold unit tests were being confused with scientific results. This track separates engineering checks from empirical comparison. **No scientific replication has yet been completed by this module.**

## Required before an empirical run
1. Select one publicly accessible paper with a numeric claim and a legally usable dataset.
2. Freeze the exact claim, metric definition, expected numeric value, absolute tolerance, dataset SHA-256, software commit, environment, random seeds, and exclusion criteria **before** observing outcomes.
3. Use an independent implementation and independent evaluation data where appropriate; a model-written test of its own model-written function is not evidence.
4. Record at least three repeated measurements, with raw outputs and run metadata.
5. Run `experiments/empirical_validation/protocol.py` on the frozen protocol, measurement JSON list and dataset bytes. The comparison cannot establish scientific validity by itself.
6. Preserve disagreements and failures. Human review must assess confounders, methodology and interpretation.
7. A successor must cite an observed result and specify which experimental choice changes **because of** that result.

## Status and guardrails
- The module implements a data-integrity check and a predeclared numeric comparison. It does **not** retrieve a paper, generate an experiment, run a scientific model, or reproduce any published claim.
- The unit tests use **synthetic demonstration data**, never represent them as research findings.
- Automatic publication of new radar scaffold branches is paused; signal collection and artifacts remain active.
- Avoid expanding feed count or heuristic council scoring until at least one end-to-end independently reproducible empirical study is complete.

## Reviewer questions
Can an independent researcher rerun the same study? Were the criteria frozen before seeing results? Does the conclusion follow from the measured evidence? Did the next experiment change because of documented evidence?
