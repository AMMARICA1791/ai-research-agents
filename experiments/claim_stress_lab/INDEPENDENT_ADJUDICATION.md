# Independent source–claim–quote adjudication sheet

**Purpose:** prevent AVeriTeC's *claim verdict* from being misused as a
*quote-defect* ground truth. This sheet is a protocol, not labeled results.

## One row per reviewed triple

Required fields:

- `case_id`: stable local identifier
- `source_url`: accessible primary evidence URL
- `source_snapshot_sha256`: hash of locally retained evidence text
- `claim_text`: exact claim under evaluation
- `quoted_text`: exact proposed verbatim quote, or empty if none
- `source_contains_quote`: true/false, established against snapshot
- `quote_supports_claim`: true/false/null (null when unreviewable)
- `defect_label`: true/false/null (null when unreviewable)
- `defect_type`: one of `none`, `missing_quote`, `number`,
  `negation`, `causality`, `unsupported`, `other`, `unreviewable`
- `annotator_id`: stable pseudonymous identifier
- `annotated_at_utc`: ISO 8601 timestamp
- `independent_of_model_output`: true/false
- `notes`: justification with specific source passage

**Do not** infer defect labels from AVeriTeC verdicts or from lab flags.

## Procedure

1. Freeze the deterministic sample manifest, its seed, and source SHA-256
   before any model output is shown to reviewers.
2. Resolve each source URL and archive the source text with its SHA-256.
   Record failed retrievals as **unreviewable** rather than negative cases.
3. Two reviewers independently assess each claim and proposed quote
   **without seeing the lab's predictions**. Preserve both original labels.
4. Adjudicate disagreements, documenting the final decision and reason.
5. Lock the reviewed dataset before evaluating the lab or exact-quote baseline.
6. Report counts, TP/FP/FN/TN, precision, recall, and explicit failure
   examples for **both** methods on exactly the same reviewable cases.
   Report unreviewable cases separately; do not silently exclude them.
7. If labels are not independent, or sources cannot be reproduced, mark
   the experiment inconclusive. Keep PR #57 in draft.

## Data rights and privacy

Keep original dataset licensing and attribution; avoid republishing large
third-party text or personal data in GitHub artifacts. Use source URLs,
fingerprints, and small excerpts where legally permitted.

**Current status:** no completed independently adjudicated cases; no
real-world performance claim is justified.
