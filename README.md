# AI Research Agents

**Evidence-first experiments for free-first AI coding agents.**

We are building a reproducible Python research lab that inspects source, records bounded findings, proposes narrowly scoped changes with open-weight models, and tests those changes before human review.

> **Experimental research software, not a commercial service or fully autonomous developer.** We demonstrated one AI-generated fix to a pre-scoped real repository bug. This does not establish general bug discovery or repair ability.

## Try the verified demo in one minute

**[View the Public Proof Tour on GitHub](https://github.com/AMMARICA1791/ai-research-agents/actions/workflows/public-demo.yml)** — open the latest **successful run** and read its **Summary**. Anyone can inspect the public run without installing software. Only maintainers with repository write access can use **Run workflow**; outside developers can clone or fork the repository to rerun it. Downloading an artifact through the GitHub website requires signing in. No paid AI API key is needed.

The demo independently rechecks 8 synthetic scanner cases, a synthetic red/green fix, and the historical real-source GitHub URL regression corrected in **[PR #17](https://github.com/AMMARICA1791/ai-research-agents/pull/17)**. **It does not rerun Qwen or discover new bugs**: the original model-authored patch is preserved in PR #17. See [the one-minute guide](docs/PUBLIC_DEMO.md) and [GitHub discovery setup](docs/GITHUB_DISCOVERY_SETUP.md).

## See the evidence
- [AI-written change merged by owner — PR #17](https://github.com/AMMARICA1791/ai-research-agents/pull/17): an actual GitHub URL host-spoofing bug fixed by Qwen2.5-Coder 1.5B.
- [AI generation and testing run](https://github.com/AMMARICA1791/ai-research-agents/actions/runs/38120082970). Its generation and test jobs passed, while automated PR creation was blocked by GitHub permissions; the review PR was opened separately from the AI-written branch.
- [Bounded synthetic benchmark](.github/workflows/research-evidence.yml): 8 artificial labeled cases; scores do not imply production accuracy.
- [Live local model research](.github/workflows/no-key-local-llm.yml): Ollama/Qwen without a paid API key.
- [Scope and limitations](docs/PROJECT_SCOPE.md).

## Run the scanner

Python 3.11+ and internet for package installation:

```sh
git clone https://github.com/AMMARICA1791/ai-research-agents.git
cd ai-research-agents
python -m pip install -r requirements.txt
python -m pytest -q tests/
python -m lab.cli mission --repo . --goal "Inspect our laboratory for evidence-backed improvements"
python main.py
```

Local UI: http://127.0.0.1:8000. Windows users can use their normal Python environment. The basic scanner does not need an LLM key.

**Repository maintainers on a tablet:** Open GitHub **Actions → Research Lab - Persistent Missions → Run workflow**. Use non-sensitive goals only: public Actions artifacts can contain report details. See [QUICKSTART.md](QUICKSTART.md).

## What is implemented?
- AST inspection and conservative dependency mapping.
- Seven **pipeline stages**, not seven separate thinking AI agents.
- Sanitized aggregate memory on the `lab-memory` branch.
- Optional real Qwen review of aggregate counts, plus strictly bounded patch trials.
- Human-reviewed candidate changes, full `tests/` CI suite, and experiment artifacts.

**Not implemented:** generic autonomous software repair, secure execution of arbitrary external code, a hosted commercial product, or a public contributor service.

## Help shape the project
Read [Roadmap](ROADMAP.md), [Contributing](CONTRIBUTING.md), [Governance](GOVERNANCE.md), [Security](SECURITY.md), and [Code of conduct](CODE_OF_CONDUCT.md).

**License:** [Apache License, Version 2.0](LICENSE). The owner approved it for this repository on 11 October 2026. Original copyright remains with the respective authors; see the [attribution notice](NOTICE), [trademark guidance](TRADEMARKS.md) and [rights explained](docs/LICENSING_DECISION.md). The license permits commercial reuse and derivatives subject to its conditions, **not** exclusive control of the public code. Contributors can now submit original or lawfully authorized changes under the documented contribution policy.

Languages: [Arabic](README.ar.md) · [Portuguese](README.pt-BR.md) · [Spanish](README.es.md) · [Chinese](README.zh-CN.md). Some translations cover older phases; this page is the up-to-date capability summary.

**North star:** every claim about AI coding should be backed by inspectable source changes, reproducible tests, and honest failure reports.