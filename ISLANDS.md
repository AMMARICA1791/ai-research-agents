# Open project islands

Each directory in [projects/incubator](projects/incubator) is an independent **island**. Islands share a repository, but **not** a runtime, dependency environment, or release approval. Each has its own README, executable prototype, test suite, and optional evidence and council review.

## Explore and reproduce

1. Choose one island under `projects/incubator/<island-id>/`.
2. Read its README and hypothesis. Treat generated claims as unverified.
3. Run its tests locally: `cd projects/incubator/<island-id> && python -m unittest discover -s . -p 'test_*.py' -v`.
4. Report a reproducible failure using the **Island bug report** issue template, including island ID, expected/actual behavior, command, traceback, and proposed fix.
5. Submit a narrowly scoped pull request that changes only that island. Keep regression tests alongside fixes. Cross-island changes require explicit rationale.

## Public collaboration

Failures are welcome evidence. Do not post secrets, private datasets, access tokens, or identifying personal information in issues. Never run an untrusted island with production credentials. Maintainers and external contributors may propose changes; merges must pass checks and respect repository protections.

## Automation

The **Island Health Check** workflow runs each island's tests independently, reports pass/fail per island in its job summary, and creates or updates a GitHub issue for failing islands. A failed island does not stop checks of others. The workflow does not deploy or execute prototypes with elevated privileges.

Automated radar generation and merge are separate from public bug triage. No claim is made that the council is an autonomous repair agent unless a verified repair workflow exists.
