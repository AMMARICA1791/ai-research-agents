# Real-news Qwen evidence — 2026-10-13 (Brazil) / 2026-10-14 UTC

## Scope and evidence standard

This is a **bounded empirical pilot**, not a benchmark accuracy claim or independent news verification. No paid API key was used. Five authentic public AI-related posts from one publisher (Google DeepMind, one redirecting to Google Developers) were retrieved using public HTTPS. For each retrieved source, three questions were asked: one direct, one cautious inference, and one deliberately unanswerable negative control. The HTML response bytes were SHA-256 fingerprinted, and a 1,200-character source excerpt was archived per source.

Because the five texts belong to one publishing ecosystem, the experiment does **not** establish cross-publisher performance or independent corroboration.

## Reproducible runs

| Run | Commit | Model | Retrieval | Model replies | Verbatim quote matches | Observations |
| --- | --- | --- | --- | --- | --- | --- |
| [First real-source run](https://github.com/AMMARICA1791/ai-research-agents/actions/runs/38496643606) | ab8b351 | qwen2.5:0.5b | 5/5 | 15/15 | 0 | Four excerpts were dominated by webpage navigation; invalid input quality for source analysis. |
| [After article-body fix](https://github.com/AMMARICA1791/ai-research-agents/actions/runs/38497144306) | 8023ea0 | qwen2.5:0.5b | 5/5 | 15/15 | 0 | Five archived excerpts now began with article content, not site navigation; negative controls returned the literal NOT_IN_SOURCE 5/5. |
| [Strict citation gate, larger local model](https://github.com/AMMARICA1791/ai-research-agents/actions/runs/38497551247) | 233f7cf | qwen2.5:1.5b | 5/5 | 15/15 | 9/10 answerable cases | 15/15 valid JSON; 15/15 exact source-URL copies; only 1/5 exact NOT_IN_SOURCE refusal labels. |

| [Strict negative-control gate](https://github.com/AMMARICA1791/ai-research-agents/actions/runs/38498244857) | 9571f32 | qwen2.5:1.5b | 5/5 | 15/15 | 8/10 answerable cases | **FAIL_CLOSED**: 15/15 valid JSON; 14/15 exact source URLs; **5/5 answers chose NOT_IN_SOURCE**, but only **3/5** met the full abstention+empty-quote+URL contract. |

The other four negative controls in the third run did **not** invent an income figure; three had an empty JSON answer and one returned an unrelated source-state code. These are **not counted as correctly labeled refusals**. All 15 third-run outputs were JSON objects, but JSON validity and source URL copying do not demonstrate semantic correctness. A 9/10 literal quote-match result means only that a model-provided quote is present in the archived text, **not** that the accompanying answer is entailed by the quote.

## CI regression evidence

The third run's code commit 233f7cf also passed [Verify MVP](https://github.com/AMMARICA1791/ai-research-agents/actions/runs/38497551258): **303 tests passed, one warning**. Earlier changes established four narrow news-evaluation regression tests in GitHub Actions. Subsequent work fixed real-page body selection and added three offline tests covering article landmarks and navigation exclusion.

## Source set

- https://deepmind.google/blog/gemini-4-argon-for-robotics/
- https://deepmind.google/blog/introducing-synthid-bio/
- https://deepmind.google/blog/advancing-private-ai-compute-with-secure-server-side-memory/
- https://deepmind.google/blog/piloting-the-worlds-first-double-blind-ai-evaluations/
- https://deepmind.google/blog/gemini-robotics-2-brings-whole-body-intelligence-to-robots/

## What is established

1. GitHub Actions fetched five genuine public HTML pages, extracted substantive news excerpts after a documented extraction fix, stored SHA-256 content hashes, and ran actual local Ollama/Qwen inference.
2. The 1.5B model returned structured answers for all 15 questions and provided exactly matched source excerpts for 9 of 10 answerable cases.
3. The negative-control formatting standard **was not met** by the 1.5B model: only one explicit correct abstention label out of five.
4. Model response success, literal quotes, and exact URLs **do not imply** factual truth, semantic entailment, question-answer accuracy, independence of evidence, or readiness for automatic publication.


## Follow-up gate: distinguish absence judgment from safe output contract

The fourth run, on [commit 9571f32](https://github.com/AMMARICA1791/ai-research-agents/commit/9571f32882bdc9d1ecc8047f4ca6ec0f95ece5e3), added a stricter test and archived an **unlabeled** 15-question human review template. The runner reported **failure**, deliberately, because the strict contract was not met. Inspecting the raw archived JSON established the following separate metrics:

- **Absence decision:** 5/5 model answer fields contained the exact token `NOT_IN_SOURCE`.
- **Strict abstention envelope:** 3/5 had the correct answer token, an empty quote, and exact URL simultaneously. The other two had (1) an empty source URL and (2) an unrelated verification-status string in the quote field.
- **Answerable excerpts:** 8/10 model quotations matched the archived excerpt exactly (versus 9/10 in the earlier run).
- **Source URLs:** 14/15 model-generated URLs exactly matched archived source URLs. **JSON valid:** 15/15.
- **Overall:** No semantic/entailment score, no human-reviewed gold labels, and no automatic-publication approval.

This distinction prevents a mistaken reading of the failure: the model recognized that the revenue information was absent in all five cases, but did not always obey the structured provenance contract. **The source reader must remain the authority for the source URL**; the model's echo must never overwrite it. Incorrect or missing quotation evidence should be withheld and flagged for human review instead of being silently accepted or rewritten as a model success.

The [workflow artifact for the failed run](https://github.com/AMMARICA1791/ai-research-agents/actions/runs/38498244857) retains the sources, raw responses, and an unfilled human-gold-label template. The template is **not** itself a completed evaluation dataset; no semantic answer-accuracy percentage is justified yet.


## Source-anchored quarantine replay — 2026-10-13 (Brazil), run 38499262620

On commit `a1f83e49`, [Real-News Qwen Evidence Probe](https://github.com/AMMARICA1791/ai-research-agents/actions/runs/38499262620) fetched **5/5** real pages, received **15/15** model replies in valid JSON, and found **9/10** exact literal quotations in answerable cases. The Qwen quality step remained **red**, correctly: only **12/15** echoed model URLs matched the archived source URLs, and **1/5** unanswerable records satisfied the entire token + empty-quote + URL contract. All five negative-control model `answer` fields chose `NOT_IN_SOURCE`; that does **not** repair the malformed provenance envelopes.

Crucially, the *new, separately executed* **Audit provenance and quarantine unsupported answers** step **passed even though the quality gate failed**. Its archived `news_audit.json` reported:

| Replay audit result | Count |
| --- | ---: |
| Source records matched by archived URL and SHA-256 | 5 |
| Model responses audited against source archive | 15 |
| Matching literal quotes for answerable cases | 9 |
| Strict abstention envelopes | 1 |
| Quarantined as invalid evidence | 5 |
| Review-only quote cases | 9 |
| Model source URL mismatches | 3 |
| Automatically publishable answers | **0** |

The five quarantined cases were **three** missing/mismatched model URLs on abstentions, **one** nonempty quote for missing evidence, and **one** unmatchable quote on a direct answer. The auditor **did not** use a model-supplied URL as authoritative and **did not** invent a replacement quote. Raw model answers, archived source hashes, the human review template (still unfilled), and audit outcomes are available in the downloadable workflow artifact while GitHub retains it.

This **proves mechanical quarantining and provenance handling**, not semantic entailment, independent fact checking, or suitability for unattended news publishing. The [15-case preliminary triage](REAL_NEWS_QWEN_15_CASE_TRIAGE.md) describes an *earlier* run; it is an assistant-authored checklist rather than independent human ground truth.

## What remains unproven / next acceptance gate

- **Human-reviewed gold labels** for the five archived article excerpts and 15 questions: direct correctness, justified inference, unsupported-answer rejection, and citation entailment.
- **Strict structured abstention** across all five negative controls (latest run: 1/5 complete format, although 5/5 answered NOT_IN_SOURCE; stochastic variability remains).
- **Publisher diversity** and reproducibility beyond this one sample and date.
- Long-term robustness to page HTML changes, failed feeds, prompt injection, and timeouts.

Do not describe this pilot as an accurate autonomous news analyst until those acceptance criteria are met. The raw evidence remains in the workflow artifacts linked above, subject to GitHub's short artifact retention; this document preserves **aggregate findings**, not verbatim copyrighted article contents.
