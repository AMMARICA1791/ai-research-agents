# External Iris validation: eligibility gate

The repeated holdout workflow proposed external validation because its observed minimum accuracy was 0.9333, above the frozen 0.90 decision threshold.

**External validation is not yet performed.** A mirror of the 150 classic Iris rows, a shuffled copy, or a random split of the same dataset does not qualify as independent evidence. The corrected scikit-learn Iris copy and the UCI classic Iris archive have overlapping underlying observations and cannot be treated as independent cohorts.

## Acceptance requirements

1. Independent specimen collection, documented collection dates, measurement protocol and provenance.
2. Species labels for setosa, versicolor and virginica and four compatible centimeter-valued features; no duplicated classic Iris records.
3. Immutable downloadable source, licensing/redistribution permissions, checksum, and overlap check against the training data.
4. Freeze model weights and preprocessing trained on the original 120 samples before reading external labels; no fitting or threshold tuning on external data.
5. Report per-species counts, accuracy, confusion matrix, uncertainty and distribution shifts; report missingness and excluded records.
6. Do not publish a performance claim if no eligible independent dataset is available.

## Next action

Seek a verifiably independently collected dataset, or redesign the experiment to study a different dataset with an explicit independent test cohort. Until then the status is **BLOCKED_PENDING_EXTERNAL_DATASET**, not a pass. This restriction protects against dataset leakage and fabricated external validity.
