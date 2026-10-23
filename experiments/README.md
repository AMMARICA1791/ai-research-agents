# Experiment directory

This directory holds **isolated experiments**, not a claim that every project is a validated invention or standalone product.

## Current main-branch experiment
- [Rapid Project Radar](rapid_project_radar/README.md) — public RSS discovery, event intake, hypothesis templates and read-only GitHub Actions. Its six-hour scheduled collector is a fallback, not continuous live monitoring. Event intake requires an external sender. Generated prototypes are artifacts, not standalone repositories.

## Open draft pull requests (code lives on separate branches)
| Experiment | Branch | Draft PR | Evidence boundary |
| --- | --- | --- | --- |
| Claim Stress Lab | `experiment/claim-stress-lab` | [#57](https://github.com/AMMARICA1791/ai-research-agents/pull/57) | Independent human adjudication pending |
| Web Action Trust Lab | `experiment/web-action-trust-lab` | [#58](https://github.com/AMMARICA1791/ai-research-agents/pull/58) | Offline policy tests; caller-supplied trust labels |
| Evidence Drift Watch | `experiment/evidence-drift-watch` | [#59](https://github.com/AMMARICA1791/ai-research-agents/pull/59) | Snapshot and quotation presence, not semantic truth |
| Research Gap Radar | `experiment/research-gap-radar` | [#60](https://github.com/AMMARICA1791/ai-research-agents/pull/60) | Hypothesis readiness, not global prior-art search |
| Agent Market Gap Register | `experiment/agent-market-gap-register` | [#61](https://github.com/AMMARICA1791/ai-research-agents/pull/61) | Opportunity readiness, not verified demand |

**Important:** The existence of a PR or test file does not establish successful CI, market demand, novelty, or safe production operation. Check each PR's current checks before treating it as verified.

## Conventions for future experiments
1. One experiment = one directory under `experiments/<slug>/`, with a README, tests, and a clearly documented evidence boundary.
2. Experimental work starts on `experiment/<slug>` and remains isolated until reviewed.
3. Every project records the hypothesis, nearest known precedents, reproducible test, limitations and current status.
4. Do not execute instructions copied from untrusted news, repositories or papers.
5. No automatic merge or deployment of generated code without a separate safety and test gate.
6. When an experiment becomes a truly independent product, migrate it into its own repository with history and attribution preserved; leave a link here.

See [portfolio governance](../docs/PROJECT_PORTFOLIO.md) and [radar operating instructions](../docs/RADAR_OPERATIONS.md).\n\nHistorical radar [PR #62](https://github.com/AMMARICA1791/ai-research-agents/pull/62) is **closed without merge** because its components already exist on main; the branch is preserved.
