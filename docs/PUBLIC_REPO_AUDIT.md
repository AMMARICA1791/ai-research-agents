# Read-only audit of public GitHub Python repositories

This experimental cross-project tool accepts a **public** GitHub repository, resolves a branch/tag to an exact commit SHA, downloads a bounded archive, and performs **static Python AST analysis** in a temporary workspace.

**The inspected repository's Python programs are not imported, installed, compiled, tested or executed.** No model inference is used during this audit.

## Run from GitHub (maintainer or collaborator with write access)

Open [Read-Only Public Repository Audit](https://github.com/AMMARICA1791/ai-research-agents/actions/workflows/public-repo-audit.yml) and select **Run workflow**. Enter a public repo URL and optional branch/tag; HEAD means default branch.

Public sample: https://github.com/pallets/itsdangerous

The finished run's Summary identifies scanned files, finding counts and exact commit SHA. Download the JSON artifact for finding details. **Public visitors can view existing runs but need repository write permission to start a run in our repository.** They can fork the public project and run their own copies if GitHub Actions is enabled.

## Local Python 3.11+ example

Install requests==2.32.2, then execute:

    python -m lab.public_repo_audit --repo-url https://github.com/pallets/itsdangerous --ref HEAD --output results/public-repo-audit.json

Only canonical HTTPS repository URLs are accepted, with no query, authentication or subpaths.

## Honest limits

- No paid LLM, automatic patch, imported code, or execution of external repositories.
- Findings are **heuristic review hints**, not independently proven vulnerabilities.
- Only a bounded selection of allowed files is inspected. Entry count, archive byte size, decompressed bytes, filename, symlink and redirect restrictions apply.
- The ZIP can be truncated by scan limits and this is reported; large archives are rejected.
- The analysis includes source file/line evidence for syntax errors, dynamic execution calls, silent exception handlers, missing tests, and conservative import-cycle detection.
- A commit SHA pins the revision, enabling others to repeat the review. GitHub archives can differ in ZIP metadata.

This work supports the longer-term evidence-first research lab, but **does not yet create a general autonomous repair agent**.

Read [project scope](PROJECT_SCOPE.md) and [contribution guidelines](../CONTRIBUTING.md).
