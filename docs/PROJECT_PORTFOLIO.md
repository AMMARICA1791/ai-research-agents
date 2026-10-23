# Research portfolio and repository organization

Updated: 2026-10-23. This is an organizational index, not a validation certificate.

## Mission
Anticipate future technical needs before they become mainstream; convert falsifiable hypotheses into runnable experiments. Commercial outcomes are not prerequisites for prototyping. Claims of worldwide novelty require evidence and remain provisional.

## Three layers
1. **Core research lab** (this repository's existing `lab/`, `agents/`, `tests/`, documentation and demos). Preserve current behavior and evidence.
2. **Radar infrastructure** (`experiments/rapid_project_radar/` plus `.github/workflows/rapid-*`). Collects public signals, handles dispatched events and emits *bounded template artifacts*. Not a 24/7 hosted service, not a general autonomous coding agent.
3. **Independent experiments** (draft branches and PRs listed in [experiments/README.md](../experiments/README.md)). Separate repositories may be created after independent scope and ownership are established.

## Operational statuses
- **IDEA**: hypothesis only.
- **SCAFFOLD**: runnable template; no evidence it solves the proposed problem.
- **PROTOTYPE**: implementation and tests; claims bounded by actual results.
- **REVIEW**: independent prior-art, security and evidence review.
- **VALIDATED**: named reproducible evaluation with clear acceptance criteria.
- **ARCHIVED**: paused or superseded; keep records.

No experiment is implicitly VALIDATED by appearing in this portfolio.

## Radar lifecycle
Signal -> deduplicate -> future scenario -> hypothesis -> prior-art screening -> isolated scaffold -> reproducible test -> draft review -> independent repository when warranted.

The existing code implements **only parts** of this lifecycle. In particular, continuous push ingestion requires a configured external sender, the current hypothesis engine uses fixed templates, and no automatic independent repository creation exists.

## Safety and repository governance
- Protect `main` with reviews and required checks where supported.
- Grant workflows minimum permissions. Use separate credentials only if justified, and never expose tokens in reports.
- Do not promote external source text into executable instructions.
- No automatic deployment, purchase, external messaging, or destructive changes.
- Preserve evidence, source links, commit history, licensing and attribution.
- Do not delete or rename historical branches merely to make the branch count smaller.

## Migration sequence
1. Inventory and label existing projects (**this document and the experiment index**).
2. Verify each experimental PR's tests and evidence; fix failures before promoting.
3. Decide which projects warrant standalone repositories, and move each with preserved history.
4. Extract the radar into its own repository only after its workflows and source dependencies are inventoried.
5. Connect event sources, prior-art screening and sandboxed code generation with explicit boundaries.

## Repository audit — 2026-10-23

Compared `main` with all six experiment branches using GitHub compare API.
All six branches are **diverged** from `main` (13 commits behind at audit time).
PR #57 is 52 commits ahead; PR #58 is 7 ahead; PR #59 is 4 ahead;
PR #60 is 5 ahead; PR #61 is 4 ahead; PR #62 is 4 ahead.
The comparison is historical/structural evidence, **not** a passing test report.

### Important cleanup finding
PR #62 was closed without merging on 2026-10-23, and is redundant as an integration PR: its four radar files were
already independently installed on `main`, followed by newer radar components.
Do **not** merge PR #62 as if it were a new radar installation. Preserve it as
historical review context until formally closed or annotated.

### Isolation findings
PRs #57–#61 add their own experiment directories and CI workflows relative
to the common ancestor. Do not merge them in bulk; first review the changed
files and current CI independently. Their shared `behind_by` count does not
by itself prove a merge conflict.

### Required verification before reorganization
- Run offline unit tests for radar and each branch.
- Check workflows and logs, not only green commit decorations.
- Verify scheduled radar and event intake actually execute.
- Check topic-specific generated prototypes; current scaffolds are generic.
- Keep branch histories and attribution when extracting repositories.

## Verified CI evidence — 2026-10-23

The GitHub Actions runs associated with the **last inspected branch-head commits** returned `status=completed` and `conclusion=success` for each experiment's own workflow and the repository-wide Verify MVP workflow:

| PR | Experiment workflow | Verify MVP |
| --- | --- | --- |
| #57 Claim Stress Lab | [Run 39931984359](https://github.com/AMMARICA1791/ai-research-agents/actions/runs/39931984359) | [Run 39931984362](https://github.com/AMMARICA1791/ai-research-agents/actions/runs/39931984362) |
| #58 Web Action Trust Lab | [Run 40029092630](https://github.com/AMMARICA1791/ai-research-agents/actions/runs/40029092630) | [Run 40029092616](https://github.com/AMMARICA1791/ai-research-agents/actions/runs/40029092616) |
| #59 Evidence Drift Watch | [Run 40029509245](https://github.com/AMMARICA1791/ai-research-agents/actions/runs/40029509245) | [Run 40029509393](https://github.com/AMMARICA1791/ai-research-agents/actions/runs/40029509393) |
| #60 Research Gap Radar | [Run 40029518464](https://github.com/AMMARICA1791/ai-research-agents/actions/runs/40029518464) | [Run 40029518483](https://github.com/AMMARICA1791/ai-research-agents/actions/runs/40029518483) |
| #61 Agent Market Gap Register | [Run 40030136829](https://github.com/AMMARICA1791/ai-research-agents/actions/runs/40030136829) | [Run 40030136925](https://github.com/AMMARICA1791/ai-research-agents/actions/runs/40030136925) |

This establishes passing **configured CI checks at those commits only**. It does not verify full threat models, real-market utility, global novelty, human adjudication or current merge readiness. No independent tests were rerun in this audit.

### Promotion decisions
- **#57 HOLD**: independent adjudication remains required.
- **#58–#61 EXPERIMENTAL**: CI passed, but domain-specific validation remains incomplete.
- **#62 REDUNDANT FOR INTEGRATION**: main already contains radar components; avoid merging older radar files.
- **Radar on main: UNVERIFIED RUNTIME**: scheduled/event-triggered live operation and artifact production still need run-level confirmation.
\n## Operations runbook\n\nSee [Radar operations](RADAR_OPERATIONS.md) for workflows, manual verification, source-event configuration, and known runtime limits.\n