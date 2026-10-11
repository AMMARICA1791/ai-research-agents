# Governance

The repository owner retains all project, licensing, release, commercial, funding and merge decisions. Technical help from AI assistants and external contributors does not make an assistant a co-owner, legal representative, or equity holder.

## Decision flow
1. State a problem, expected behavior and reproducible evidence.
2. Develop a narrow candidate and a regression test in a separate branch.
3. Run the complete test suite; separate mocked, synthetic and real-model evidence.
4. Review the changes and limitations; human approval before merging.
5. Record a testable result rather than an unsupported capability claim.

Pull requests must use the [evidence-first PR template](.github/PULL_REQUEST_TEMPLATE.md) to disclose the exact scope, provenance, reproducible checks, negative results and remaining uncertainty. CI success alone is not human approval; maintainers can defer or reject unsupported capability claims.

External contributions may be reviewed under [Apache-2.0](LICENSE) and [CONTRIBUTING.md](CONTRIBUTING.md). Contributors retain rights in their original contributions; submitting a patch does not assign copyright to the owner. Maintainers must reject material submitted without adequate redistribution rights. Non-sensitive bug reports and feedback are welcome.

An eventual paid product is a possibility, not an existing business or revenue commitment. Licensing, commercial terms and contributor policies require transparent owner approval.