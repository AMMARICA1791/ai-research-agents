# Contributing

> **Special short research contribution:** We currently seek **two independent human reviewers** for [15 Qwen news-answer citation checks — Issue #52](https://github.com/AMMARICA1791/ai-research-agents/issues/52). This voluntary evaluation needs English reading and evidence criticism, **not coding**. The original model quotation must be assessed; it must not be silently replaced by a better one. Please volunteer in the issue rather than submitting unrelated PRs. No independent semantic-accuracy result is claimed yet.


**Broader project feedback is welcome without coding:** Explore the [public project showcase](docs/PROJECT_SHOWCASE.md) and leave your perspective in [Issue #54](https://github.com/AMMARICA1791/ai-research-agents/issues/54). A structured [project feedback form](https://github.com/AMMARICA1791/ai-research-agents/issues/new/choose) is also available. This does **not** expand general bug-fix support to unrelated third-party repositories or waive research evidence requirements.

We value reproducible bug reports, test cases and honest results, including failed experiments.

**License:** This project is distributed under [Apache-2.0](LICENSE). By intentionally submitting an authorized contribution for inclusion in the project, you normally license that contribution under Apache-2.0 in accordance with Section 5, unless expressly stated otherwise or a separate agreement applies. You retain copyright in your own work; no assignment to the maintainer is presumed. Submit only material you own or are authorized to redistribute. See [NOTICE](NOTICE) and [licensing guidance](docs/LICENSING_DECISION.md).

## A strong report contains
1. Expected versus actual behavior.
2. A minimal, public and non-sensitive reproduction.
3. Python version and operating system, plus the GitHub workflow URL if applicable.
4. An automated assertion or test demonstrating the defect.
5. Boundaries and uncertainties: synthetic results are not production accuracy.

## Development and contribution requirements
- Keep each pull request focused on one issue.
- Run `python -m pytest -q tests/`, as CI does.
- Add a regression test that fails before the fix and passes afterward.
- Do not mark actual failures as skipped, disable checks, or use mocks to claim live AI inference.
- Never commit private source, secrets, credentials or personal data.
- Identify the origin and applicable licenses of any third-party material; model-generated text does not prove that redistribution rights exist.
- Clearly label model-written code, deterministic scripts and human-authored changes.
- Human review is mandatory before merging to `main`.

Do not disclose exploitable vulnerabilities publicly. See [security policy](SECURITY.md), [roadmap](ROADMAP.md), and [governance](GOVERNANCE.md).

## Current maintenance and support scope

This project is an experimental research laboratory, not a general-purpose repair service. At this stage, maintainers prioritize the eight documented synthetic test cases and the historical GitHub host-validation regression documented in PR #17. General bug-fix requests for unrelated external repositories are currently out of scope and may be closed without investigation.

Reports within scope should include a minimal, reproducible, non-sensitive example and a regression test. Acceptance of an issue or pull request is not a commitment to provide individual support, turnaround times, or production guarantees. Broader support may be reconsidered after the documented release and demonstration have been independently checked.
