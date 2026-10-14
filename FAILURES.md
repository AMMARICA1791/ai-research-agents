# Documented Research Failures

This file records observed capability gaps and failed experiments without presenting them as scientific conclusions. A failed quality gate is evidence of an unmet requirement, not proof that the research question is false.

## F-001 — Manual paper review did not become automated full-text evidence extraction

**Status:** Open — not resolved or scientifically validated.

**Objective:** Move from manually inspecting an original astrophysics paper about stellar nucleosynthesis and cosmic iron to reproducible, automated extraction of source-grounded hypotheses, methods, evidence, findings, and limitations.

**Observed result:** The cosmic-iron research notes documented a manually reviewed primary paper; Crossref discovery supplied bibliographic metadata, not the paper's full text. The [merged PR #44](https://github.com/AMMARICA1791/ai-research-agents/pull/44) pilot ran on a **synthetic, explicitly labeled excerpt**, not an ingested full scientific paper. GitHub confirms PR #44 was merged on **2026-10-13**, but merging the experimental code **did not resolve** the original scientific-quality failure. Its local Qwen 0.5B output failed the exact-quotation quality gate: an earlier run matched **1/5**, and a later run matched **0/5** required fields. Offline validator tests passing did not establish model extraction quality.

**Evidence:**
- [Cosmic iron research notes](docs/IRON_COSMIC_ORIGIN_RESEARCH_01.md) — manual review, with automated evidence collection still pending.
- [Merged PR #44](https://github.com/AMMARICA1791/ai-research-agents/pull/44) — synthetic source-grounded excerpt pilot; merged 2026-10-13. **Not** proof of validated full-text scientific analysis.
- [Failed pilot run 38193743815](https://github.com/AMMARICA1791/ai-research-agents/actions/runs/38193743815) — `MATCHED_QUOTATIONS=0/5`, `EVIDENCE_QUALITY_GATE_FAILED`.

**Boundary:** Literal quote matching verifies only that text appears at a cited source line. It does **not** establish that a claim follows from that quote, that the source is scientifically correct, or that the system has read the full paper. Synthetic-fixture extraction is not evidence of real-paper competence.

**Next acceptance criteria:** Ingest a permitted, traceable primary-source text with document/page or section provenance; extract claims with verbatim quotations; independently verify offsets and assess claim–evidence entailment; publish reproducible successes **and failures**. Do not mark this resolved on a green synthetic test alone.

**Release impact:** The experimental pilot is now present in `main`, but the original outcome remains a **documented failure**. Do not claim automated full-paper evidence extraction, verified scientific accuracy, or closure of F-001 until real primary-source extraction with independently reviewed evidence passes its own acceptance criteria.

## F-002 — Live AI-news model fails strict evidence and abstention gate

**Status:** Open — no validated semantic accuracy or automatic news publication.

**Objective:** Given permissioned public news excerpts, produce 15 source-bounded Qwen answers whose **original model quotations** support the claims, cite the archived original source consistently, and refuse five deliberately unanswerable requests with a strict response envelope.

**Observed result:** The archived [live run 38500177379](https://github.com/AMMARICA1791/ai-research-agents/actions/runs/38500177379) retrieved **5/5** actual publisher articles (all within the **Google / DeepMind publisher ecosystem**) and obtained **15/15** structured Qwen replies. **9/10** answerable model quotations exactly matched the short excerpts, but **only 1/5** negative controls met the complete abstention format. The strict model-quality step **failed on purpose**, while the mechanical archive audit and preparation of a **15-case, unlabelled** semantic human-review packet succeeded. No independent reviewers have supplied semantic labels. The later [run 38501243397](https://github.com/AMMARICA1791/ai-research-agents/actions/runs/38501243397) also finished with a failed experiment workflow; do not transfer the earlier numerical counts to that separate run without reviewing its artifacts.

**Evidence:**
- [Chronological real-news experiment report](docs/REAL_NEWS_QWEN_EVIDENCE_2026-10-13.md) — observed results, provenance and failure thresholds.
- [Assistant-authored preliminary triage of 15 cases](docs/NEWS_SEMANTIC_REVIEW_TRIAGE_RUN_38500177379.md) — **not** independent human annotations.
- [Review protocol](docs/NEWS_SEMANTIC_REVIEW_PROTOCOL.md), [mechanical audit](research/news_probe_audit.py) and [review packet builder](research/news_semantic_review.py).
- [Citation-integrity regression PR #51](https://github.com/AMMARICA1791/ai-research-agents/pull/51): enforces review of Qwen's **actual original quote**, not a better human-substituted quote. Passing these tests proves integrity of the checker, **not the model's factual or semantic correctness**.

**Boundary:** Exact matching of a quoted string is **not** evidence that the quote entails the model's answer; absence from a 1,200-character excerpt does not imply absence from the full article. Five same-publisher sources cannot establish cross-publisher reliability. A reviewer ID supplied in JSON does not authenticate reviewer independence.

**Next acceptance criteria:** Obtain two genuinely independent human judgments on all 15 cases (and adjudicate disagreements); assess original citation-to-answer entailment; expand to diverse permitted publishers in separately documented experiments; rerun quality gates until the structured abstention and provenance requirements actually pass; preserve red runs and evidence. **No automatic publication and no invented accuracy percentage**.

**Release impact:** F-002 is intentionally unresolved. A successful GitHub Actions software test or public showcase does **not** close it.
