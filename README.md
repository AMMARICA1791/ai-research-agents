# AI Research Agents

> **Project navigation:** [Experiment index](experiments/README.md) · [Portfolio organization and migration plan](docs/PROJECT_PORTFOLIO.md). Experimental branches are not merged products.

**Evidence-first, free-first AI research for reproducible experiments, open-weight models and verifiable engineering.**

> **Seven coordinated pipeline stages, NOT seven independent thinking AI agents.** This laboratory is experimental; human review remains mandatory.

> **Open for external project-wide review:** [Read the public project tour](docs/PROJECT_SHOWCASE.md) · [Share a criticism or research idea — Issue #54](https://github.com/AMMARICA1791/ai-research-agents/issues/54). The project is an experimental prototype, **not** a validated autonomous research institute.

> **Community call — 2 volunteer reviewers needed:** We are recruiting two independent human reviewers to evaluate **15 real Qwen news answers**, checking whether each **model-cited quotation** actually supports the answer. No coding, fees, paid APIs or prior affiliation required; reviewers must read the original English excerpts and work separately. **[Volunteer in Issue #52](https://github.com/AMMARICA1791/ai-research-agents/issues/52)**. Open call: English · العربية · Português · Español · Français. The model's semantic accuracy has **not** been established.

We are building a reproducible Python research lab that inspects source, records bounded findings, proposes narrowly scoped changes with open-weight models, and tests those changes before human review.

> **Experimental research software, not a commercial service or fully autonomous developer.** We demonstrated one AI-generated fix to a pre-scoped real repository bug. This does not establish general bug discovery or repair ability.

## See the evidence
- [AI-written change merged by owner — PR #17](https://github.com/AMMARICA1791/ai-research-agents/pull/17): an actual GitHub URL host-spoofing bug fixed by Qwen2.5-Coder 1.5B.
- [AI generation and testing run](https://github.com/AMMARICA1791/ai-research-agents/actions/runs/38120082970). Its generation and test jobs passed, while automated PR creation was blocked by GitHub permissions; the review PR was opened separately from the AI-written branch.
- [Bounded synthetic benchmark](.github/workflows/research-evidence.yml): 8 artificial labeled cases; scores do not imply production accuracy.
- [Live local model research](.github/workflows/no-key-local-llm.yml): Ollama/Qwen without a paid API key.
- [Scope and limitations](docs/PROJECT_SCOPE.md).

## Reproduce the research — 3 commands, no model API keys

[Start here: DEMO.md](DEMO.md). The bundled demo uses Python 3.11+ and **does not run live Qwen inference**.

### GitHub-only viewer experience

**[View the Public Proof Tour on GitHub](https://github.com/AMMARICA1791/ai-research-agents/actions/workflows/public-demo.yml)** — open the latest **successful run** and read its **Summary**. Anyone can inspect the public run without installing software. Only maintainers with repository write access can use **Run workflow**; outside developers can clone or fork the repository to rerun it. Downloading an artifact through the GitHub website requires signing in. No paid AI API key is needed.

The demo independently rechecks 8 synthetic scanner cases, a synthetic red/green fix, and the historical real-source GitHub URL regression corrected in **[PR #17](https://github.com/AMMARICA1791/ai-research-agents/pull/17)**. **It does not rerun Qwen or discover new bugs**: the original model-authored patch is preserved in PR #17. See [the one-minute guide](docs/PUBLIC_DEMO.md) and [GitHub discovery setup](docs/GITHUB_DISCOVERY_SETUP.md).

## First research-and-exploration experiment beyond code analysis

The **[Public Scholarly Research Discovery](.github/workflows/scholarly-discovery.yml)** workflow retrieves a bounded set of **real Crossref bibliographic metadata** for a public research topic, records DOI links, a UTC retrieval timestamp, a response digest and explicit uncertainty. It **does not read or judge papers, rank scientific quality, use an LLM, or invent conclusions**. The result is a source inventory—the first step toward the wider research center, not a fully independent research agent. [Evidence protocol and limitations](docs/SCHOLARLY_DISCOVERY.md).

## Inspect a public Python repository without executing it

**Experimental capability:** enter a canonical public GitHub URL and receive bounded static Python AST findings, plus an **evidence-linked human review queue** with fixed P1–P3 order, proposed validation steps, and links to the exact inspected commit. No outside source is executed; no paid model API is needed.

- [Read-only public repository audit workflow](.github/workflows/public-repo-audit.yml) — maintainers can run it on GitHub Actions; anyone can view completed public runs.
- [How it works and its safety/coverage limits](docs/PUBLIC_REPO_AUDIT.md), including the [manual review queue](docs/REVIEW_QUEUE.md).
- Example public project: [pallets/itsdangerous](https://github.com/pallets/itsdangerous). A pattern finding is a review hint, not proof of a security defect.

This is **static evidence gathering, not autonomous patch creation or an external security certification**.

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

**Not implemented:** generic autonomous software repair, secure execution of arbitrary external code, a hosted commercial product, or a public contributor service. The broader research-center pillars remain future milestones.

The [experimental baseline release notes](docs/RELEASE_0.1.0_EXPERIMENTAL.md) document successes **and** failures; experimental means no stable production guarantee.

## Help shape the project
Read [Roadmap](ROADMAP.md), [Contributing](CONTRIBUTING.md), [Governance](GOVERNANCE.md), [Security](SECURITY.md), and [Code of conduct](CODE_OF_CONDUCT.md).

**License:** [Apache License, Version 2.0](LICENSE). The owner approved it for this repository on 11 October 2026. Original copyright remains with the respective authors; see the [attribution notice](NOTICE), [trademark guidance](TRADEMARKS.md) and [rights explained](docs/LICENSING_DECISION.md). The license permits commercial reuse and derivatives subject to its conditions, **not** exclusive control of the public code. Contributors can now submit original or lawfully authorized changes under the documented contribution policy.

Languages: [Arabic](README.ar.md) · [Portuguese](README.pt-BR.md) · [Spanish](README.es.md) · [Chinese](README.zh-CN.md). All four translations include an October 2026 current-scope update; consult this English page for the full capability inventory.

**North star:** every claim about AI coding should be backed by inspectable source changes, reproducible tests, and honest failure reports.

## Honest demo recording status

A screen recording has **not yet been captured or independently reviewed**. Do not represent a scripted or simulated clip as a live execution. To record one, check out a named commit, capture a continuous terminal session running the three commands in [DEMO.md](DEMO.md), and preserve any failures on screen. Check the resulting files and video before linking the real recording here. The public [proof workflow](.github/workflows/public-demo.yml) provides inspectable run evidence in the meantime.

The [historical baseline record](VERIFIED_RELEASE.md) identifies its exact source commit and separates previously reported tests from unverified checks on newer commits.
