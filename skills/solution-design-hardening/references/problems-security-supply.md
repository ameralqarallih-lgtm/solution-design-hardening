# Software supply chain — problem playbook

Use [security assessment guidance](SECURITY-ASSESSMENT.md) and [standards mappings](SECURITY-STANDARDS.md). These are defensive investigation leads; confirm trust boundaries, reachability and effective controls. Use only authorized isolated tests with synthetic data.

## SDP-213 — Vulnerable dependency exposure

- **Failure:** A known vulnerable dependency is reachable in application or deployment.
- **Detection:** Inspect resolved dependency and image inventory, advisories, reachability and vendor fixes.
- **Remediation and safeguards:** Use authorized SCA, update or mitigate affected versions, document exceptions and retest compatibility.
- **Verification:** Verify resolved version and applicable advisory after fix; test affected behavior, not just manifest edit.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-214 — Dependency confusion

- **Failure:** A resolver retrieves an unintended package from an untrusted namespace or registry.
- **Detection:** Inspect registry configuration, private scope mapping and resolution policy.
- **Remediation and safeguards:** Pin trusted registries and namespaces; lock dependency resolution and verify package integrity.
- **Verification:** Use isolated fake registry metadata; verify resolver policy selects only approved source.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-215 — Artifact integrity failure

- **Failure:** Deployment accepts modified or unverified binaries/images.
- **Detection:** Inspect digest pinning, artifact signatures and admission verification; distinguish identity from authenticity.
- **Remediation and safeguards:** Verify signatures or attestations against trusted identities, pin immutable digests and enforce policy at promotion.
- **Verification:** Modify synthetic artifact or use untrusted signing identity; reject; approved artifact accepted.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-216 — Untrusted CI execution

- **Failure:** Untrusted contributions can execute with privileged pipeline context.
- **Detection:** Inspect triggers, workflow permissions, checkout source, script execution and secret access.
- **Remediation and safeguards:** Separate untrusted builds from privileged release jobs, use minimal token permissions and approved promotion.
- **Verification:** Use a synthetic untrusted contribution context; assert no release credentials or write authority are available.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-217 — Pipeline credential leakage

- **Failure:** Build credentials are exposed in logs, caches, artifacts or long-lived tokens.
- **Detection:** Inspect token lifetime, scopes, masking and artifact boundaries without revealing values.
- **Remediation and safeguards:** Prefer short-lived workload identity, isolated credentials, redaction and restricted artifact access.
- **Verification:** Run synthetic marker through isolated build; verify no disclosure and credential expires or is revoked.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-218 — Missing build provenance

- **Failure:** An artifact cannot be traced to approved source and build process.
- **Detection:** Inspect attestations, SBOM, builder identity, source commit and artifact digest linkage.
- **Remediation and safeguards:** Generate and verify provenance and dependency inventory at controlled build/promotion; keep trust policy independent.
- **Verification:** Check synthetic attestation subject, builder and commit; reject mismatched artifact or untrusted builder.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-219 — Unsupported component lifecycle

- **Failure:** Runtime or dependency no longer receives required security fixes.
- **Detection:** Compare deployed versions to vendor support lifecycle and ownership.
- **Remediation and safeguards:** Maintain lifecycle inventory, upgrade path and time-bounded risk acceptance for unsupported components.
- **Verification:** Verify deployed version and support evidence; rehearse upgrade and regression tests.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

