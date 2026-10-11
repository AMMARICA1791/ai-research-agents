# Original source passage verification — bounded first phase

This module checks that an **exact quotation** cited by a claim appears in a supplied local UTF-8 text archive and that the archive bytes match a declared SHA-256 digest.

```sh
python -m research.source_passage_verification --input results/claims-with-source-texts.json --source-dir private-archive --output results/quote-checks.json
python -m pytest -q tests/test_source_passage_verification.py
```

Input extends the existing evidence-linked claims JSON with `source_texts`, an array of `{"doi": "...", "file": "paper.txt", "sha256": "<64 lowercase hex>"}`. Each claim evidence link adds an exact `quote`. Files must be local flat `.txt` filenames (UTF-8, max 2 MB each), not URLs or paths outside the archive.

**Scientific boundary:** Exact text presence is not proof that a source is authentic, peer reviewed, or that its conclusions support a proposition. Even an exact quote can be misleading when removed from context. This module never labels scientific support as verified and never asserts a real scientific contradiction. Human review of the full methods, results, population and uncertainty remains required.

The first phase does not fetch papers, parse PDFs, validate DOI-to-file provenance, verify quotations in a trusted publisher edition, assess entailment, or detect paraphrases. Keep licensed or private full texts outside public GitHub repositories.
