# Per-class scientific relation metrics

Run this **after** opt-in real model inference and independent human adjudication.

```sh
python -m research.ai_entailment_triage --input claims.json --source-dir private-archive --endpoint https://TRUSTED-PROVIDER/v1/chat/completions --model MODEL --output predictions.json
python -m research.per_class_metrics --input claims.json --source-dir private-archive --predictions predictions.json --output per-class-report.json
```

For each of `supports`, `contradicts`, `insufficient`, and `out_of_scope`, the report contains support count, predicted count, TP/FP/FN, precision, recall and F1. It also contains a full confusion matrix with an `abstain` column and total reviewed count/coverage.

Undefined metrics are JSON `null`, **not zero or 100%**. A synthetic unit-test score must not be represented as real-model performance. Without an external inference endpoint, a real model call and a representative independently reviewed benchmark, this module cannot produce defensible empirical scientific accuracy. The output explicitly marks scientific validity as not established.
