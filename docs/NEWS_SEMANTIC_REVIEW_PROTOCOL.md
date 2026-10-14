# Semantic entailment review protocol (15 real-news cases)

**Current status: unreviewed.** This stage prepares an independent review of Qwen's answers, not synthetic "gold labels" or an automatic factual-accuracy claim. Evaluation concerns **only the archived 1,200-character excerpt**, not the full article or independent real-world truth.

## Inputs and provenance

From GitHub Actions, download the `real-news-qwen-evidence` ZIP (the workflow keeps it for 7 days). It includes publisher excerpts, raw Qwen responses, source SHA-256 hashes, mechanical audit, and a new `news_semantic_review_packet.json` with all 15 source-linked cases. Do **not commit the packet**: it contains publisher text. The original archived URL and hash, rather than the model's echoed link, establish provenance.

A packet can be created even after a **red** model-quality run, to enable diagnosis. The packet contains no human conclusions and no semantic score.

## Independent assessment

Two actual reviewers must independently examine each case **before** seeing one another's judgments. For direct answers and inferences the labels are:

- **SUPPORTED:** The *specific quoted passage* supports every material assertion in the answer; publisher claims are attributed, not treated as independently proven facts.
- **PARTIAL:** Some material claims are grounded, but the quote is incomplete, the answer overreaches, or certainty is inflated.
- **UNSUPPORTED:** The quote does not support the central answer, even when quoted accurately.
- **INSUFFICIENT_CONTEXT:** The archived excerpt does not permit a reasoned judgment.

For unanswerable cases: **CORRECT_ABSTENTION**, **INCORRECT_ABSTENTION**, or **INSUFFICIENT_CONTEXT**. Correctness is scoped to absence/presence of the precise requested information in the excerpt only. It does **not** claim the information is absent from the full publication.

Every entry needs a reviewer ID, case ID, label, and a substantive reason. A SUPPORTED or PARTIAL judgment must include a supporting quote present verbatim in the archived excerpt. This exact-string check is an input-integrity measure, **not semantic verification**.

## Review file and command

Create a private `reviews.json` containing two records per case Q01–Q15. This is a **format illustration, not a gold label**:

```json
{
  "reviews": [
    {
      "case_id": "Q01",
      "reviewer_id": "reviewer-one",
      "label": "UNSUPPORTED",
      "rationale": "Example only: the quoted title does not substantiate the specific numerical claim.",
      "supporting_quote": ""
    }
  ]
}
```

Run:

```sh
python -m research.news_semantic_review --packet news_semantic_review_packet.json --reviews reviews.json --output review_consistency.json
```

The program checks formatting, source-quote presence, repeated reviewer IDs, two-reviewer coverage, and disagreements requiring adjudication. **It cannot authenticate the human identities or independence**. It deliberately returns `semantic_accuracy: null` and `publication_allowed: false` even when both reviewers agree. No self-certification or fabricated scoring.

## Prioritized cases and exit

The [initial 15-case triage](REAL_NEWS_QWEN_15_CASE_TRIAGE.md) identifies examples where quotation is valid text but *semantically irrelevant*: cases 10 and 11 quote a student-exam analogy rather than evidence for the evaluation protocol. In the latest live pilot, five responses also required mechanical quarantine. These remain review tasks, not human gold labels.

Do not describe the model as validated until real independent reviewers have assessed all 15 cases, adjudicated conflicts, and checked citation-to-claim relevance. Future cross-publisher sampling is a separate milestone; a 15-case, one-publisher sample cannot justify a general accuracy claim.
