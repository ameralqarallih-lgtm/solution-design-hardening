# Contributing

Open an issue describing a concrete failure scenario, business invariant, reproduction and suggested mitigation. Include counterexamples to prevent false positives. Add new IDs at the end; never renumber existing IDs. Keep the core skill concise and put detailed guidance in references. Include an evaluation case for material changes. Run `python3 tools/validate.py`. Do not submit credentials, proprietary code, personal data, or production logs. Contributions must be authorized for distribution under the repository license.

## Adaptive technology contributions

Prefer capability-level guidance over duplicating product-specific instructions. Optional product profiles must identify applicable versions, authoritative documentation, configuration prerequisites, guarantee scope, counterexamples and verification tests. Include an unknown-stack or negative-control evaluation where relevant. Do not imply a product profile is mandatory or tested unless actual results are supplied.

## Integration contributions

Use [isolated integration experiments](integration/README.md) with synthetic data, bounded deadlines, negative controls and explicit evidence. Run `python -m unittest discover -s evals -v` before a pull request. Never mark an unexecuted infrastructure test as passed. Preserve capability-first design; new product fixtures are optional and must not become support prerequisites.

## Security contributions

Use synthetic data, local or explicitly authorized isolated targets, and both denied and permitted test cases. Do not submit secret values, exploit traces against real services or private code. Keep mappings versioned and advisory; cite upstream documentation and distinguish tested controls from suggested requirements. Report suspected project vulnerabilities via [responsible disclosure](SECURITY.md).

## Architecture tooling contributions

Keep candidate discovery distinct from analyst-supported evidence. Add negative controls, unresolved-link tests, scope/secret-output tests and dependency-cycle tests for any model or parser changes. Preserve schema compatibility or document migration. Never infer a root cause from proximity alone. See [architecture tooling](tools/ARCHITECTURE.md).
