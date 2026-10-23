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

## Lightweight mirror and reproducible selection

A public mirror offers the development JSON directly (approximately 1.79 MB):
https://huggingface.co/chenxwh/AVeriTeC/resolve/main/data/dev.json

The mirror is a fallback, **not automatically authenticated as byte-identical**
to the official GitHub dataset. Preserve its downloaded SHA-256 and provenance,
and compare with the official release if available. Do not commit the raw
third-party dataset into this repository.

After obtaining the file, produce a deterministic, claim-verdict-stratified
sample manifest with its source-file SHA-256:

```sh
python -m experiments.claim_stress_lab.averitec_audit --input /path/to/dev.json
python -m experiments.claim_stress_lab.averitec_sample --input /path/to/dev.json --count 30 --seed 20261022 --output averitec_sample_manifest.json
```

This selection deliberately balances claim verdict categories, **not** quote
defects. The 30 indices are candidates for independent human review, not 30
verified citations. Keep the manifest and source fingerprint alongside any
subsequent evaluation report.

No local download was completed during this work session. The offline tools
are prepared but have not produced real-dataset results.

## Sampling interpretation (mandatory)

The seeded round-robin procedure **oversamples minority claim-verdict
categories** by design. It is useful for stress testing but **not a
representative prevalence estimate** of the AVeriTeC development set.
The manifest now reports both population and selected verdict counts and
sets `sample_is_population_representative: false`. Do not extrapolate
unweighted sample precision, false-positive rates, or defect prevalence to
the full dataset. For prevalence estimation, use an independently labeled
probability sample with documented inclusion probabilities and suitable
weights, and report uncertainty.

## Verified live acquisition (2026-10-23)

GitHub Actions Claim Stress Lab run **77**, job
`optional-real-data-acquisition`, successfully downloaded the **official**
AVeriTeC development JSON directly from
`https://raw.githubusercontent.com/MichSchli/AVeriTeC/main/data/dev.json`.

- HTTP acquisition succeeded; 1,785,475 bytes, **500** claim records.
- Source SHA-256: `499793726b4a5406780928a3d9dedc48d6dd53de778f22437d129cacdb08e300`.
- The audit and deterministic 30-index selection both completed successfully.
- GitHub artifact `averitec-audit-and-sample` (ID `12490772392`)
  was uploaded in run `39929282127`, expiring 2026-10-30.
- Both the Claim Stress Lab (run 77) and Verify MVP (run 296) checks passed.
- **No independent quote-defect labels were obtained**; therefore no
  real-world precision, recall, semantic-accuracy or defect-detection
  performance is established.

This supersedes the earlier note that the data could not be downloaded.
The GitHub-hosted runner solved the network acquisition barrier; it did
not solve the independent labeling/semantic validation barrier.
