# AI-assisted evidence-to-claim triage (experimental)

The assistant proposes one of `supports`, `contradicts`, `insufficient`, or `out_of_scope` for each exact-matched quotation. It **never** changes the human annotation or verifies scientific truth. Missing quotations produce abstentions. Human-reviewed annotations from `relationship_reviews` are the only reference labels accepted for scoring.

## Offline scoring (no AI service needed)

```sh
python -m research.ai_entailment_triage --input claims.json --source-dir private-archive --predictions model-suggestions.json --output evaluation.json
python -m pytest -q tests/test_ai_entailment_triage.py
```

Outputs include `reviewed_count`, `correct_count`, `accuracy`, `coverage` and item-level comparisons. With zero independently reviewed labels, accuracy is **null**, not 100%. A passing unit test with synthetic examples **does not measure real-world model accuracy**.

## Optional real model inference

```sh
export RESEARCH_LLM_API_KEY='YOUR_SECRET'
python -m research.ai_entailment_triage --input claims.json --source-dir private-archive --endpoint https://YOUR-TRUSTED-PROVIDER/v1/chat/completions --model YOUR-MODEL --output model-suggestions.json
```

Requires an explicit HTTPS endpoint and API key; makes no network calls by default. Never commit private research texts, secrets, or model responses containing confidential material. The API receives each claim, scope and quoted passage. Use only a trusted provider with appropriate data rights.

## Evaluation requirements

For any meaningful scientific benchmark: use independently annotated, representative and blinded human-reviewed cases, record reviewer disagreements, evaluate each label separately (precision/recall/confusion matrix), stratify by domain, report sample size and abstentions, and avoid training/evaluation leakage. A reviewer label is not an infallible ground truth. This first release adds the reproducible scoring harness, **not a validated benchmark dataset**. No real-model accuracy number is claimed.
