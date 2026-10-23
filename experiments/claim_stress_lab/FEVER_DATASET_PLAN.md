# FEVER dataset acquisition and label integrity

Source: https://fever.ai/dataset/fever.html

FEVER has 185,445 Wikipedia-derived claims and human claim-level labels
(`SUPPORTS`, `REFUTES`, `NOT ENOUGH INFO`). Its claim JSONL includes evidence
references as Wikipedia page names and sentence IDs, not the complete source
sentences. The separate June 2017 Wikipedia corpus is required to resolve them.

**Important:** A `REFUTES` claim label is NOT an independently judged defective
quotation. It must never be copied into `defect_label` for Claim Stress Lab.
A claim can be refuted by one source and accurately quoted from that source.

After separately downloading the official FEVER development JSONL according to
its terms, inspect the metadata offline:

```sh
python -m experiments.claim_stress_lab.fever_audit --input /path/to/dev.jsonl --limit 30
```

This returns counts and sentence references only, with
`ready_for_claim_stress_evaluation: false`. It does not access the network,
create synthetic quotes, or manufacture quote-level human judgments.

Before actual evaluation: obtain the legally usable matching Wikipedia snapshot,
resolve exact sentences, construct and archive source/quote pairs, obtain
**independent human labels for quote-level defects**, and only then run
`evaluate_dataset.py`. Record sample selection and exclusions.

Alternative real-world corpus: https://fever.ai/dataset/averitec.html .
AVeriTeC has web-source question-answer evidence, but its claim verdicts also
must not be treated as quote-level defect labels.
