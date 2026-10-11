# v0.1.0-experimental — research baseline

**Status:** experimental prerelease, not a stable product, hosted website, security certification, or commercial service.

**Purpose:** establish a frozen, reproducible baseline for an evidence-first and free-first AI research laboratory. The center's intended disciplines include research/exploration, specialized agents, experiments and comparisons, reusable knowledge, engineering and independent verification; the release demonstrates only a subset.

## Repeat the evidence

From repository root, with Python 3.11+ and no paid API:

```sh
python -m lab.public_demo --repo . --out results/public-demo
python -m lab.benchmark
python -m lab.autorepair
```

Detailed explanation: [DEMO.md](../DEMO.md). For the comprehensive full test suite after installing `requirements.txt`, run `python -m pytest -q tests/`. GitHub Actions checks the entire test directory on each change.

### Positive evidence

1. A bundled eight-case **synthetic** static-analysis benchmark with known labels.
2. A bounded synthetic deterministic fail-closed repair that fails its regression before the change and passes afterward.
3. The historical real-source GitHub URL parser vulnerability repaired by a local **Qwen2.5-Coder 1.5B** proposal, independently checked and human-merged in [PR #17](https://github.com/AMMARICA1791/ai-research-agents/pull/17). The demo rechecks the merged behavior; **it does not call a model again**.
4. A **read-only** scan of a separate public repository (e.g. `pallets/itsdangerous`), pinned to a Git commit, with deterministic human review candidates. No third-party project source is executed or modified.
5. Reproducible CI and explicit rejection of malformed model patches, archive redirects, spoofed GitHub URLs, path traversal, and oversized input within covered tests.

### Negative evidence and limitations

- A previous Qwen trial **failed the strict AST gate**. It was rejected rather than published. A subsequent trial succeeded on the same narrowly prespecified task; this is *not* a general model success-rate estimate.
- The successful AI-generated patch was pushed as a branch, but GitHub Actions **could not create the PR** under the repository's permission policy; an authorized connected account created the PR and a human approved the merge.
- Seven stages mostly coordinate deterministic tools; they are **not seven individually reasoning language models**.
- The synthetic precision/recall results **cannot** be extrapolated to unfamiliar production repositories.
- The public audit identifies heuristics **not proven security vulnerabilities**. An unseen research task benchmark and expert-reviewed failure inventory are future work.
- Research memory is sanitized summary counts rather than a persistent learned research knowledge graph.
- Costs are not guaranteed zero: public GitHub Actions runners have resource and platform usage limits. Model experiments may download sizeable weights; the three-command demo does not.
- Maintainers have not certified outside code ownership or dependency provenance for all historical files. The Apache-2.0 license applies to this project's rights, not to unrelated third-party dependencies.
- No external community replication, production service, customers or paid offering is demonstrated.

## Release acceptance gates

- [ ] No stale public marketing/pricing drafts in the active branch.
- [ ] No erroneous MIT or enterprise-ready claim in active launch docs.
- [ ] Three-command demo reproducible without paid or installed LLM services.
- [ ] Full pytest suite and live web-server smoke tests pass on the tagged commit.
- [ ] Public GitHub tag/release actually created (not inferred from this document).

These boxes are a checklist for the release process, **not assertions that checks have already passed**. The release automation must fail closed before tagging when validation fails.

## After this release

Return to the comprehensive research-center disciplines: source-based exploration; actual specialist model/tool contributions; comparable experiments and negative findings; reusable verifiable knowledge; bounded engineering; independent evaluation. Avoid mistaking Python auditing for the whole research mission.

[Research scope](PROJECT_SCOPE.md) · [Roadmap](../ROADMAP.md) · [Contributing](../CONTRIBUTING.md) · [License](../LICENSE)
