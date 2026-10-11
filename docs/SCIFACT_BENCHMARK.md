# SciFact: public human-annotated scientific benchmark

Source: https://github.com/allenai/scifact

The SciFact **development** split provides expert-annotated SUPPORT/CONTRADICT rationale sentence indices. Do not use the unlabeled test split to claim measured accuracy. Download the original corpus and claims using the upstream instructions:

```sh
git clone https://github.com/allenai/scifact.git
cd scifact
./script/download-data.sh
cd ..
python -m research.scifact_benchmark --claims scifact/data/claims_dev.jsonl --corpus scifact/data/corpus.jsonl --cases-output scifact-dev-cases.json
```

Each exported case contains a claim, exact rationale sentence(s), upstream gold label and document ID. For external model predictions, provide a JSONL file with `{"case_id":"...","relation":"supports"}` or `contradicts`, `insufficient`, `out_of_scope`, or null (abstain).

```sh
python -m research.scifact_benchmark --claims scifact/data/claims_dev.jsonl --corpus scifact/data/corpus.jsonl --cases-output scifact-dev-cases.json --predictions model-predictions.jsonl --report-output scifact-results.json
```

Reports include per-class precision/recall/F1, confusion matrix, accuracy and coverage. SciFact does **not** directly provide independently adjudicated `insufficient` and `out_of_scope` rationale labels; these remain out of scope for gold-class performance. Do not mislabel absent evidence as human-adjudicated negative evidence. No actual model inference, external endpoint credentials or measured performance is supplied by this adapter. The synthetic unit tests only validate software logic.
