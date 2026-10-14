# Real-news Qwen 15-case review queue — initial analyst triage

**Status:** AI-assisted preliminary inspection of the [archived 2026-10-13/14 source+model artifact](https://github.com/AMMARICA1791/ai-research-agents/actions/runs/38498244857), **not human-reviewed gold labels** and **not a measure of factual accuracy**. The original artifact contains the model answers and 1,200-character source excerpts with SHA-256 evidence. It is subject to GitHub's short retention window.

Five articles were fetched, all from one publishing ecosystem (Google DeepMind; one redirected to the Google Developers Blog). Exactly three prompts were posed per retrieved excerpt. Case numbering follows the archived `results` list, starting at 1.

| Case | Source topic | Question | Mechanical observation | Preliminary semantic review issue |
| --- | --- | --- | --- | --- |
| 1 | Gemini 4 Argon Robotics | Direct | Exact quote; model URL matches | Main announcement restates publisher's own claims; not independently verified |
| 2 | Gemini 4 Argon Robotics | Inference | Exact quote; model URL matches | Quote is a page title/date and does **not** by itself justify the evaluation or performance claim |
| 3 | Gemini 4 Argon Robotics | Unanswerable | Model chose `NOT_IN_SOURCE`; source URL omitted | Correct absence decision, **invalid provenance envelope** |
| 4 | SynthID Bio | Direct | Exact quote; model URL matches | Quotation identifies the introduction; detailed physical-protein claims require a fuller supporting passage |
| 5 | SynthID Bio | Inference | Exact quote; model URL matches | Response mainly paraphrases publisher description; no independent inference established |
| 6 | SynthID Bio | Unanswerable | Model chose `NOT_IN_SOURCE`; nonempty unrelated quote | Correct absence decision, **invalid quote envelope** |
| 7 | Private AI Compute memory | Direct | Exact quote; model URL matches | Quote expresses a broad motivation; technical proposal appears elsewhere in excerpt |
| 8 | Private AI Compute memory | Inference | Exact quote; model URL matches | Generic quotation does not independently establish the claimed technical outcome |
| 9 | Private AI Compute memory | Unanswerable | Correct empty-quote and source-URL envelope | Literal refusal is supported by absence in *truncated excerpt* only |
| 10 | Double-blind evaluations | Direct | Exact quote; model URL matches | Selected quote is a student-exam analogy, not the announcement or protocol details |
| 11 | Double-blind evaluations | Inference | Exact quote; model URL matches | Selected quote is the same analogy and does not substantiate the inference |
| 12 | Double-blind evaluations | Unanswerable | Correct empty-quote and source-URL envelope | Literal refusal is supported by absence in *truncated excerpt* only |
| 13 | Gemini Robotics 2 | Direct | No exact quote match; model URL matches | **Withhold:** citation cannot be matched to the archived excerpt |
| 14 | Gemini Robotics 2 | Inference | No exact quote match; model URL matches | **Withhold:** citation cannot be matched to the archived excerpt; inference not established |
| 15 | Gemini Robotics 2 | Unanswerable | Correct empty-quote and source-URL envelope | Literal refusal is supported by absence in *truncated excerpt* only |

## What the table does and does not prove

- Source authenticity is limited to publicly retrieved and SHA-256-fingerprinted webpages; a publisher repeating a claim is **not independent corroboration**.
- A mechanically exact quote can be **irrelevant to the answer**; for example, a title or a generic analogy may match characters but cannot automatically support a detailed technical inference.
- For unanswerable questions, five model answers chose the `NOT_IN_SOURCE` token, but **only three** supplied the prescribed quote and URL envelope. The strict evaluation therefore failed correctly.
- A missing date-specific revenue figure in a *1,200-character excerpt* does not prove absence from the complete original article or wider universe.
- This is an **assistant-authored triage checklist**, not independently validated labeling. The existing `news_eval_template.json` still requires independent human review and answers grounded in archived source text.

## Acceptance before moving toward automated publication

1. Keep the source URL and SHA authoritative from the retrieval archive. Never replace it with model output.
2. Withhold unsupported quotes and malformed abstention envelopes; record the exact reason for review.
3. Request external human gold labels for semantic correctness and quote-to-claim entailment, not only literal matching.
4. Reproduce results across multiple source publishers and dates. No publication-readiness claim from this pilot alone.
