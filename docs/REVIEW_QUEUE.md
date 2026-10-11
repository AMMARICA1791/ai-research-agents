# Evidence-linked review queue for public code audits

The public GitHub audit produces a **deterministic review sequence** from known Python AST heuristics. Every suggested human check links to the exact Git commit and file/line examined. Nothing is executed or changed in the audited repository.

## From a public GitHub Actions run

Open [Read-Only Public Repository Audit](https://github.com/AMMARICA1791/ai-research-agents/actions/workflows/public-repo-audit.yml) and inspect the latest successful run. The run Summary lists up to five suggested manual reviews; the downloadable JSON artifact contains a bounded queue with up to twelve reviews. Running the workflow in the original repository requires write access, but anyone may view public run Summaries.

## What is a priority?

- P1 — parsing error: verify whether a Python file is truly invalid within its context.
- P2 — direct dynamic execution call, silent exception handler, or possible import cycle: review the software's intended behavior and surrounding code.
- P3 — missing tests in the selected files, undecodable Python source or an audit limit: first check whether scan coverage explains the observation.

This **fixed ordering is a review convenience only**. It does not measure exploitability, likelihood, business impact or confidence. It may produce false positives, and absence of findings is not a clean bill of health.

## What exactly is stored?

Each work order records:
- A stable ID derived from the public repository, pinned commit SHA, rule and location.
- Scanner rule, scanner severity, and a deterministic P1/P2/P3 review order.
- A public GitHub blob link to a file/line at the inspected SHA (or repository tree for a missing-tests finding).
- A fixed explanation and a suggested verification check to conduct **outside this auditor**, with no executable script supplied.
- `pending_human_verification` and `fix_generated=false`.

Source lines, detected secrets, full prompts and model output are **not** included in work orders. The existing scan report may contain public repository file names and paths; do not use this workflow on private code.

## Boundaries and next gate

This capability does **not** create patches, open pull requests against others' repositories, or run their tests. The next research task should validate individual false positive rates against independently reviewed, permissioned examples before making claims about automated software engineering quality. Read [audit constraints](PUBLIC_REPO_AUDIT.md) and [research scope](PROJECT_SCOPE.md).
