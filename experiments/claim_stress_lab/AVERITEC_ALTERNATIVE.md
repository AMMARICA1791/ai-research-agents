# Alternate corpus: AVeriTeC (no Wikipedia archive)

Official project: https://github.com/MichSchli/AVeriTeC
Official dataset: https://fever.ai/dataset/averitec.html
Repository development split: `data/dev.json`.

AVeriTeC is a better **small-file acquisition fallback** when FEVER's
1.7 GB Wikipedia archive cannot be obtained. It provides real-world claims,
human claim-level verdicts, questions, answers, and evidence links.
The dataset is licensed CC BY-NC 4.0 (noncommercial; check conditions).

Once the official `data/dev.json` file is locally available:

```sh
python -m experiments.claim_stress_lab.averitec_audit --input /path/to/dev.json
```

The audit reports claim labels and evidence-link coverage. It does **not**
verify source page contents, extract verbatim quotes, or map `Refuted` to
`defect_label`. Those would be scientifically invalid substitutions.
Before using Claim Stress Lab, archive permitted source text, identify the
exact quote being audited, and obtain separately reviewed quote-defect labels.

The GitHub connector located the official `data/dev.json` file but did not
return its body; direct file download from this runtime failed DNS resolution.
Thus no real-data sample or empirical score has been processed here yet.
