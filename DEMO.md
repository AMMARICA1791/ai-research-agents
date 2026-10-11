# AI Research Agents — 3-command evidence demo

**Seven orchestration stages, not seven independently reasoning AI agents.** This is an experimental research laboratory, not an autonomous product.

Run from the repository root with **Python 3.11+**. No API key, Ollama, `pip install`, or paid service is required for these three bundled demonstrations.

```sh
python -m lab.public_demo --repo . --out results/public-demo
python -m lab.benchmark
python -m lab.autorepair
```

The first command writes `results/public-demo/evidence.json` and `SUMMARY.md`, and rechecks the eight synthetic static-analysis cases, a deterministic synthetic red/green repair, and the *already merged* real-repository GitHub host validation regression. The next two commands independently output the synthetic benchmark measurements and deterministic repair report.

**How to interpret this honestly:**
- **Synthetic scanner benchmark:** eight artificial examples with known labels, **not** an unseen real-world accuracy study.
- **Synthetic repair:** deterministic AST-guided proposed change; **not** code written by a language model.
- **Historical real-source repair:** Qwen2.5-Coder 1.5B originally proposed a bounded patch in [PR #17](https://github.com/AMMARICA1791/ai-research-agents/pull/17). This demo *re-tests* the before/after behavior but **does not rerun Qwen**.
- The results show bounded successes, not independent AI research or general autonomous software development.
- If a command fails, **keep the failure** and report the commit SHA, Python version, the exact command, and sanitized error output in an issue. Never remove or skip a failing test to make the demonstration appear successful.

Prefer GitHub-only access? [View the latest public proof-run summary](https://github.com/AMMARICA1791/ai-research-agents/actions/workflows/public-demo.yml). Viewing public completed runs requires no write access; **starting a new run in the original repository does**.

Our longer-term direction is broader than code repair: [research and exploration, specialized agents, experiments, comparative evaluation, persistent knowledge, engineering, and independent verification](ROADMAP.md). See [evidence limitations](docs/PROJECT_SCOPE.md), [release notes](docs/RELEASE_0.1.0_EXPERIMENTAL.md), and [contributing](CONTRIBUTING.md).
