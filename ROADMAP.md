# Research commons roadmap

A direction of work, not a delivery schedule or promise of global uniqueness.

## Foundation (current milestone)
- [x] Basic source inspection and bounded evidence.
- [x] Model-backed research experiments with local open-weight Qwen.
- [x] A narrowly pre-scoped model-generated real repository fix, owner-merged as PR #17.
- [x] Full `tests/` suite in CI, including the security regression.
- [x] Document contribution rules, security, governance, and current limitations.
- [x] **Repository owner approved Apache-2.0**, and the canonical license and attribution notices are published.
- [x] Add relevant GitHub topics for discoverability.
- [ ] Replace the generic GitHub About description; this requires repository settings access.
- [ ] Publish and validate the `v0.1.0-experimental` prerelease only after full release gates pass.

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
