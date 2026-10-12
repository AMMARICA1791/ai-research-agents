# Changelog

This file records demonstrated experimental milestones. Historical draft marketing materials do not describe present capabilities.

## Consolidated development summary — commits 39–63 (2026-10-11)

1. **Discovery and provenance:** Hardened Crossref metadata validation and connected source-linked evidence ledgers, DOI/year checks, and reproducible discovery reports; metadata is not full-text proof.
2. **Durable research records:** Added versioned SQLite evidence snapshots, integrity/fault-injection tests, verified backup/restore, and fail-closed recovery checks.
3. **Claims and verification:** Added source-linked claims, conservative conflict screening, archived-text exact-quote checks, human claim–evidence adjudication, and optional AI entailment triage; quote matching does not prove scientific truth.
4. **Measured model evaluation:** Built per-class precision/recall/F1 and confusion matrices, a public SciFact gold-label adapter, and CI evaluations comparing pretrained NLI models (including the 338-rationale sample comparison); benchmark results do not imply general research autonomy.
5. **Bounded case studies:** Documented Factory300 access/cost limitations and public crypto literature, then registered the cosmic-iron research protocol, audited discovery references, and recorded the gap between manual paper review and automated full-text evidence extraction.

**Consolidation note:** These are five workstreams across 25 numbered commits (39–63 inclusive), not 25 independently shipped capabilities. Experimental iterations should be grouped in release notes; Git history is preserved. The separate draft PR #44 excerpt pilot is unmerged and has not passed its quality gate.

## Unreleased — research explorer after the experimental baseline

- Started the **non-code** research-and-exploration pillar with bounded public Crossref scholarly metadata discovery and source provenance.
- The collector returns bibliographic **candidates**, not verified scientific claims, complete paper reviews, AI reasoning, or model benchmarks. The published `v0.1.0-experimental` tag remains unchanged.

## [0.1.0-experimental] — 2026-10-11

**Experimental research baseline; not production-ready.** The [full scope and evidence](docs/RELEASE_0.1.0_EXPERIMENTAL.md) document verified behavior, limitations, and the reproducibility process. A release exists only once the corresponding GitHub release and tag are actually published.

### Demonstrated
- Deterministic seven-stage research **orchestration**; these stages are **not seven independent AI agents**.
- Bounded Python AST inspection and conservative dependency relationships.
- Count-based, sanitized research observations between runs.
- Optional open-weight local Qwen/Ollama inference; no paid LLM API required for the standard demonstration.
- A genuinely model-authored, narrowly pre-selected fix for the GitHub URL parser, independently tested and owner-merged as [PR #17](https://github.com/AMMARICA1791/ai-research-agents/pull/17).
- Read-only analysis of an external **public** Python repository, with bounded download/extraction and evidence-linked human-review suggestions; source code is not executed or changed.
- Reproducible [three-command demo](DEMO.md), regression suite and GitHub Actions CI.

### Explicit nonclaims
No generic autonomous bug discovery or repair, independent seven-agent reasoning network, production-grade security auditing, hosted commercial offering, existing enterprise support, or demonstrated performance on unseen real-world repair tasks. Synthetic experiments do not establish general model accuracy. Failure reports must be preserved, not hidden.

### Licensing and provenance
The repository is licensed under [Apache-2.0](LICENSE). External software dependencies and contributor-owned material keep their own applicable rights; see [NOTICE](NOTICE) and [CONTRIBUTING.md](CONTRIBUTING.md).

### Archive cleanup
Removed obsolete `archive/commercial-drafts/` documents and mock pricing pages **from the active branch** to avoid false enterprise and licensing claims. The historical files may remain accessible in earlier Git commits; this is not a confidential-data deletion.
