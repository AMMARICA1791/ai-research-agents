# Research commons roadmap

A direction of work, not a delivery schedule or promise of global uniqueness.

## Foundation (current milestone)
- [x] Basic source inspection and bounded evidence.
- [x] Model-backed research experiments with local open-weight Qwen.
- [x] A narrowly pre-scoped model-generated real repository fix, owner-merged as PR #17.
- [x] Full `tests/` suite in CI, including the security regression.
- [x] Document contribution rules, security, governance, and current limitations.
- [x] **Repository owner approved Apache-2.0**, and the canonical license and attribution notices are published.
- [ ] Update GitHub repository topics and description after verifying maintainer access.

## Earn community trust (next)
- [x] One-click evidence tour on GitHub Actions, with independent synthetic and historical real-source regression tests.
- [x] Bounded read-only audit of another public GitHub Python repository, without running its code or needing a paid model API.
- [ ] Public interactive hosted demo; GitHub Actions audit is currently maintainer-triggered and is not a hosted service.
- [ ] Independent external user reproduces one research result.
- [x] Evidence-linked, fixed-rule review ordering for external public-repository findings (human validation mandatory).
- [ ] An unseen-task benchmark with successes *and* failures.
- [ ] Confine any third-party code execution to an isolated environment without write permissions.
- [ ] Contribution onboarding and automated checks for documentation links.

## Research platform (later)
- [ ] Evidence ledger linking each proposal to source commit, model and checks.
- [ ] Meaningful comparisons of different models on identical tasks.
- [ ] Audited community-contributed benchmarks.
- [ ] Community-maintained workflows that avoid paid API requirements where possible.

## Commercial exploration (only after validation)
Evaluate private project integrations, managed execution and support once users prove the tool saves them time. No pricing or income claims before product-market evidence.

**North star:** a developer can reproduce what was changed, why the change passed, and what remains uncertain.