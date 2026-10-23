# Radar operations and verification

Updated: 2026-10-23.

## Components on main
| Workflow | Trigger | Actual function |
| --- | --- | --- |
| [Rapid Project Radar](../.github/workflows/rapid-project-radar.yml) | Schedule every six hours; manual dispatch; push/PR | Pull bounded public RSS signals; run tests; upload JSON artifact |
| [Rapid Radar Event Intake](../.github/workflows/rapid-radar-event.yml) | `repository_dispatch` event `rapid_news_signal`; manual dispatch | Validate incoming metadata; upload inert proposal artifact |
| [Rapid Radar Anticipatory Prototypes](../.github/workflows/rapid-radar-anticipate.yml) | Successful completion of Rapid Project Radar; manual dispatch | Re-fetch feeds and create generic runnable template artifacts |

## Important operating limits
- The system is **not** always-on. GitHub Actions schedules may be delayed; event-driven latency depends on the upstream sender.
- No webhook listener or external sender is configured by these files alone.
- No autonomous creation of independent repositories, branches, PRs, or topic-specific AI code exists.
- Hypothesis scaffolds share a generic authorization example across topics; they are **not** evidence of topic-specific implementations.
- Each external source is untrusted data, not executable instructions.
- Workflow permissions are read-only; no token should be placed in source files or artifacts.

## Verification checklist (maintainer)
1. Open **Actions → Rapid Project Radar → Run workflow**.
2. Inspect the latest run's conclusion, step logs and `rapid-radar-report` artifact.
3. Open **Actions → Rapid Radar Anticipatory Prototypes → Run workflow**.
4. Inspect `anticipatory-projects` artifact; distinguish generated template from working domain solution.
5. Open **Actions → Rapid Radar Event Intake → Run workflow** with a harmless HTTPS test URL and title. Inspect the `radar-event-proposal` artifact.
6. Confirm at least one scheduled run after the workflow was added to the default branch. Do not infer this from the presence of cron syntax.
7. Only after verification, configure an authenticated upstream publisher for `repository_dispatch` if immediate events are required. Store credentials in an external secret store, never commit them.
8. Protect `main` and require appropriate checks before any new code-generation or write-permission workflow is enabled.

The GitHub connector available during this audit did not expose a way to list default-branch workflow runs or dispatch new ones. Therefore **live radar operation has not been verified** here.

## Redundant historical PR
[PR #62](https://github.com/AMMARICA1791/ai-research-agents/pull/62) was closed **without merging** on 2026-10-23. The main branch already contains its radar files and subsequent additions. The historical branch remains intact.

## Future separation
Keep the radar as its own independently deployable system only after live tests and dependencies are audited. Extract other experiments individually while retaining their commit histories and attribution. Do not mass-merge or delete branches to simplify the UI.
