# Research scope: evidence before claims

**Goal:** build reproducible, free-first research tools for verifying code improvements proposed by open-weight AI models.

## Verified
- Read-only Python AST inspection for a narrow group of rule patterns.
- Reproducible integration tests and an eight-case **synthetic** benchmark.
- A sanitized count-based research journal on `lab-memory`.
- Real local Qwen/Ollama inference on aggregate findings.
- A narrowly scoped, genuine model-generated patch to `web/app.py` correcting spoofed GitHub URLs, independently tested and merged by the owner in [PR #17](https://github.com/AMMARICA1791/ai-research-agents/pull/17).

## Not yet demonstrated
- Autonomous discovery and repair of unknown bugs in arbitrary programs.
- Safe execution of unrelated third-party repositories with write credentials.
- Seven independently thinking LLM agents (most pipeline stages are deterministic).
- Production-quality detection accuracy from the synthetic benchmark.
- Automated GitHub Actions PR creation under current repository permission settings.
- A commercial service, an external developer community, or unique global novelty.

## Evidence labels
Distinguish *mocked*, *synthetic real execution*, *live local model*, *real repository patch*, and *unseen task benchmark*. Report failures as well as successes. Require human review before merging AI-generated code.

The owner adopted [Apache License 2.0](../LICENSE) in October 2026. This permits commercial reuse subject to the license conditions; the original authors retain their respective copyrights. See [rights and limitations](LICENSING_DECISION.md).