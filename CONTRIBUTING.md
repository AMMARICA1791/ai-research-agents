# Contributing

We value reproducible bug reports, test cases and honest results, including failed experiments.

**Licensing hold:** this public repository does not yet have an approved open-source license. Please start with non-sensitive issues, benchmark ideas and documentation suggestions. Do not submit third-party source code or redistribution-dependent patches until the owner approves licensing terms.

## A strong report contains
1. Expected versus actual behavior.
2. A minimal, public and non-sensitive reproduction.
3. Python version and operating system, plus the GitHub workflow URL if applicable.
4. An automated assertion or test demonstrating the defect.
5. Boundaries and uncertainties: synthetic results are not production accuracy.

## After the licensing decision
- Keep each pull request focused on one issue.
- Run `python -m pytest -q tests/`, as CI does.
- Add a regression test that fails before the fix and passes afterward.
- Do not mark actual failures as skipped, disable checks, or use mocks to claim live AI inference.
- Never commit private source, secrets, credentials or personal data.
- Clearly label model-written code, deterministic scripts and human-authored changes.
- Human review is mandatory before merging to `main`.

Do not disclose exploitable vulnerabilities publicly. See [security policy](SECURITY.md), [roadmap](ROADMAP.md), and [governance](GOVERNANCE.md).