# Assessment and planning output

Load for Comprehensive assessments, for remediation plans, or when the user requests assessment documents. Track batches in the [coverage register](../assets/coverage-register.md).

## Catalog coverage

For a repository-wide assessment, read the repository's `SOLUTION-DESIGN-PROBLEMS.md` (locate it if necessary). If missing, use [the bundled catalog](SOLUTION-DESIGN-PROBLEMS.md). Assess every repository catalog entry and every bundled entry not already represented; map equivalent entries rather than duplicate findings. Preserve bundled SDP IDs; assign project-only IDs with a separate prefix. Read [detection guidance](DETECTION-GUIDANCE.md) for relevant failure modes. For focused work, consult only the relevant sections and related failure modes; do not claim full repository coverage.

## Assessment and planning output

For a full assessment, create or update these files in the repository (respect existing documentation conventions):

- `SOLUTION-ARCHITECTURE-MODEL.md`: component, dependency, transaction, invariant and trust-boundary model with evidence and unresolved links (may be embedded in the assessment to respect repository conventions).
- `SOLUTION-DESIGN-ASSESSMENT.md`: every catalog problem with a stable ID, applicability, status, evidence, severity, recommended mitigation, and linked finding/task IDs. Include additional findings separately.
- `SOLUTION-DESIGN-REMEDIATION-PLAN.md`: prioritized tasks with linked problems, implementation steps, affected components/files, dependencies, schema/configuration changes, acceptance criteria, tests, rollout and rollback guidance.

Use statuses: Fully Addressed, Partially Addressed, Not Addressed, Incorrectly Addressed, Not Applicable, Requires Verification. Justify non-applicability and verification gaps. Fully Addressed requires evidence of correct coverage and appropriate verification. Severity: Critical, High, Medium, Low, based on actual impact. Use stable IDs and consolidate duplicate findings without dropping catalog coverage.

For focused changes, a concise finding and fix summary is sufficient unless the user requests documents. For large assessments, persist progress and resume without losing previously recorded evidence.

## Templates

- [Assessment template](../assets/assessment.md), [remediation template](../assets/remediation.md), and [verification template](../assets/verification.md): use for full assessments.
- [Architecture model](../assets/architecture-model.md), [threat model](../assets/threat-model.md), [technology inventory](../assets/technology-inventory.md) and [coverage register](../assets/coverage-register.md).
