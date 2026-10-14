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
