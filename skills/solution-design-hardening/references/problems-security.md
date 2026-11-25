# Security - problem playbook

Signals are investigation leads, not findings. Confirm the business invariant and actual runtime guarantees. Tests are proposals until executed in an isolated environment. Use the simplest sufficient safeguard; do not introduce a pattern merely because it is listed.

## SDP-131 - Authorization TOCTOU

- **Failure:** Permission changes between check and effect.
- **Detection:** Authorization checked before mutable ownership or permission changes.
- **Remediation and safeguards:** Authorize within guarded transaction or revalidate at effect; version relevant policy.
- **Verification:** Revoke access between check and write; protected action rejected.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-132 - Authorization cache staleness

- **Failure:** Revoked permission remains effective.
- **Detection:** Cached permission allows revoked user past policy bound.
- **Remediation and safeguards:** Version/invalidate authorization cache; fail closed for critical decisions.
- **Verification:** Revoke grant while cache warm; access denied within required bound.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-133 - Token refresh race

- **Failure:** Concurrent refresh invalidates or overwrites credentials.
- **Detection:** Concurrent token refresh overwrites newer token or triggers reuse detection.
- **Remediation and safeguards:** Serialize refresh per credential; atomic token version replacement; handle rotation semantics.
- **Verification:** Two workers refresh rotating token; stored token remains usable.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-134 - Confused deputy

- **Failure:** Privileged service acts beyond caller authority.
- **Detection:** Service uses privileged identity for user-controlled resource without delegation check.
- **Remediation and safeguards:** Validate caller authorization and target context; scoped service credentials.
- **Verification:** Low-privilege caller requests high-privilege resource through service; denied.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-135 - Sensitive telemetry leakage

- **Failure:** Logs or dead letters expose sensitive payloads.
- **Detection:** Sensitive payloads copied into logs, traces or DLQ without controls.
- **Remediation and safeguards:** Minimize/redact payload; restrict access and retention; use safe correlation IDs.
- **Verification:** Trigger failure with synthetic secret; search telemetry and quarantine for leakage.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-136 - Input resource amplification

- **Failure:** Small or malformed input induces disproportionate resource use.
- **Detection:** Unbounded user input induces huge query, decompression or allocation.
- **Remediation and safeguards:** Limit decoded size, depth, complexity and processing time before expensive work.
- **Verification:** Submit oversized/compressed input in sandbox; bounded resource use and rejection.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.
