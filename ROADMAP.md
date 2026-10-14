# Research commons roadmap

A direction of work, not a delivery schedule or promise of global uniqueness.

## Two complementary pillars (status is evidence-based, not a percentage)

| Pillar | Current verified scope | Not yet demonstrated |
| --- | --- | --- |
| **A — Code Intelligence** | Bounded AST/dependency inspection, synthetic benchmark, historical scoped Qwen fix evidence, read-only public GitHub Python audit | General autonomous repair, unseen-task accuracy, safe execution of arbitrary external projects |
| **B — Research Center** | Bounded Crossref metadata discovery and source-linked evidence ledger | Scientific literature review, independent specialist-agent team, controlled live model comparisons, independent research verification, shared production-grade knowledge service |

These pillars complement rather than replace each other. Crossref metadata is **bibliographic discovery**, not proof of scientific conclusions. Experimental persistent memory is developed separately and must pass its own review and CI gates before being counted as merged capability. Completion percentages are deliberately omitted because no validated scoring rubric exists.

## Foundation (current milestone)
- [x] Basic source inspection and bounded evidence.
- [x] Model-backed research experiments with local open-weight Qwen.
- [x] A narrowly pre-scoped model-generated real repository fix, owner-merged as PR #17.
- [x] Full `tests/` suite in CI, including the security regression.
- [x] Document contribution rules, security, governance, and current limitations.
- [x] **Repository owner approved Apache-2.0**, and the canonical license and attribution notices are published.
- [x] Add relevant GitHub topics for discoverability.
- [x] Replace the generic GitHub About description with a concrete, evidence-first summary; confirmed from current public repository metadata on 2026-10-14.
- [x] Publish the **experimental**, non-production [`v0.1.0-experimental` prerelease](https://github.com/AMMARICA1791/ai-research-agents/releases/tag/v0.1.0-experimental); published on 2026-10-11. This is a tagged historical baseline, **not** a production-quality certification or a re-test of later `main` commits.

## Public external feedback (active)
- [x] Publish an honest [public project showcase](docs/PROJECT_SHOWCASE.md) with evidence, non-goals and reproduction routes.
- [x] Invite researchers, developers and nontechnical reviewers to [discuss the project as a whole in Issue #54](https://github.com/AMMARICA1791/ai-research-agents/issues/54).
- [ ] Obtain an independent external critique and respond to its evidence or counterexamples.
- [ ] Obtain two independent human semantic reviews of the Qwen news pilot; [volunteers wanted](https://github.com/AMMARICA1791/ai-research-agents/issues/52).
- [ ] Capture a continuous, independently checkable demonstration video; do **not** label a simulated recording as proof.

## Earn community trust (next)
- [x] One-click evidence tour on GitHub Actions, with independent synthetic and historical real-source regression tests.
- [x] Bounded read-only audit of another public GitHub Python repository, without running its code or needing a paid model API.
- [ ] Public interactive hosted demo; GitHub Actions audit is currently maintainer-triggered and is not a hosted service.
- [ ] Independent external user reproduces one research result.
- [x] Evidence-linked, fixed-rule review ordering for external public-repository findings (human validation mandatory).
- [ ] An unseen-task benchmark with successes *and* failures.
- [ ] Confine any third-party code execution to an isolated environment without write permissions.
- [ ] Contribution onboarding and automated checks for documentation links.

## Next focus after baseline freeze — restore the research mission

- [x] **First non-code exploration source:** retrieve bounded public Crossref bibliographic metadata with DOI links, source digest and UTC provenance; **not yet a literature review**.
- [ ] **Research and exploration:** gather reproducible, independently reviewed evidence from multiple permissioned sources beyond code analysis.
- [ ] **Actual specialist roles:** run measurable, clearly attributed model/tool contributions rather than rename deterministic stages as agents.
- [ ] **Experiments and comparisons:** evaluate open models on identical disclosed tasks, including unsuccessful results.
- [ ] **Cumulative knowledge:** store versioned, source-linked conclusions and uncertainty, not merely counts.
- [ ] **Engineering and independent validation:** only bounded, reviewable proposals with test evidence and explicit human decisions.

## Research platform (later)
- [ ] Evidence ledger linking each proposal to source commit, model and checks.
- [ ] Meaningful comparisons of different models on identical tasks.
- [ ] Audited community-contributed benchmarks.
- [ ] Community-maintained workflows that avoid paid API requirements where possible.

## Commercial exploration (only after validation)
Evaluate private project integrations, managed execution and support once users prove the tool saves them time. No pricing or income claims before product-market evidence.

**North star:** a developer can reproduce what was changed, why the change passed, and what remains uncertain.

## Next research pillars — evidence-gated development

1. **Research discovery:** extend the bounded Crossref source inventory only after testing missing DOI, duplicate records, rate limits, malformed metadata and offline failures. Do not turn metadata into scientific conclusions.
2. **Specialist agent attribution:** record which model or deterministic tool performed each operation, with version, input scope and human approval; do not rename orchestration stages as independent agents.
3. **Comparable experiments:** define a frozen task set, identical budgets and failure-inclusive reporting before comparing open-weight models. Synthetic scores must remain clearly labeled.
4. **Versioned knowledge:** store source URL/DOI, retrieval UTC, digest, confidence and invalidation conditions; do not silently overwrite historical evidence.
5. **Engineering and safety:** retain read-only external inspection, no arbitrary third-party code execution, minimal permissions, bounded downloads and mandatory review for proposed patches.
6. **Independent verification:** test exact candidate SHAs in CI, preserve negative findings and publish a failure-aware evidence ledger before any release claim.

**Promotion rule:** each pillar advances only with a reproducible test, recorded limitations, and a reviewed change. These are planned work items, not claims of completed implementation.
