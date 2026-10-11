# Security policy

This is experimental research software, **not** a professional security auditing service. There is no production-support guarantee or SLA.

## Report suspected vulnerabilities privately

Do not publish exploit steps, tokens, private code or personal information in a public GitHub issue. If GitHub private vulnerability reporting is enabled, open **Security → Report a vulnerability** on the repository. If it is not enabled, the owner must establish a private reporting contact before detailed disclosures can be accepted.

Non-sensitive bugs belong in the public bug report form.

## Safeguards and limits

- GitHub Actions logs and artifacts on a public repository may be accessible to others.
- Never place secrets or private datasets in mission inputs.
- Model-produced patches are untrusted and require narrow code checks, testing, and human review.
- Never execute untrusted project code with repository write tokens.
- Third-party packages and remote installation scripts may introduce supply-chain risks; no blanket audit is claimed.
- The `lab-memory` branch contains allowlisted aggregates, not a secret store.
- Automatic merge into `main` is not part of this project.

## External repository inspection boundary

The **current read-only public Python repository inspection path** fetches bounded source content and analyzes Python syntax/AST; it does **not intentionally execute the inspected repository's code**. This is a scope statement for that inspection path, **not** a guarantee that the whole project or every dependency is immune to remote code execution or other vulnerabilities. Running third-party installation scripts, test suites, or other tools is outside this read-only boundary and requires separate isolation and security review. Report a concrete exploit privately through the disclosure process above.

## Supported releases

No production release is supported yet. Security improvements are reviewed through pull requests.