# Independent evaluation dataset protocol

The evaluation script `evaluate_dataset.py` is ready, but **no independent dataset has been collected or scored**.

Each JSON array item must contain `id`, `claim`, `quote`, `source_text`, `source_url`, and `defect_label` (boolean). The last field must be assigned by a reviewer **before** looking at program flags. `true` means a mechanical citation defect within the narrow scope being measured, not that the claim is semantically false.

Use at least 30 cases from accessible sources, with a documented sampling method, archived evidence and independent labeling notes. Include supported and unsupported examples; do not reuse the four synthetic development cases as validation. Keep sources legally usable. Run:

```sh
python -m experiments.claim_stress_lab.evaluate_dataset --input independently_labeled.json --output evaluation.json
```

Report both methods' TP/FP/FN/TN and precision/recall. Treat small samples as preliminary, inspect every false positive and false negative, and do not claim improvement without evidence. The script never approves publication.
