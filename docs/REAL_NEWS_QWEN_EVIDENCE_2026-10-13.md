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

## What remains unproven / next acceptance gate

- **Human-reviewed gold labels** for the five archived article excerpts and 15 questions: direct correctness, justified inference, unsupported-answer rejection, and citation entailment.
- **Correct refusal signaling** across all five negative controls (currently 1/5 exact format).
- **Publisher diversity** and reproducibility beyond this one sample and date.
- Long-term robustness to page HTML changes, failed feeds, prompt injection, and timeouts.

Do not describe this pilot as an accurate autonomous news analyst until those acceptance criteria are met. The raw evidence remains in the workflow artifacts linked above, subject to GitHub's short artifact retention; this document preserves **aggregate findings**, not verbatim copyrighted article contents.
