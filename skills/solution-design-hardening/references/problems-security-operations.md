# Security monitoring and operations - problem playbook

Use [security assessment guidance](SECURITY-ASSESSMENT.md) and [standards mappings](SECURITY-STANDARDS.md). These are defensive investigation leads; confirm trust boundaries, reachability and effective controls. Use only authorized isolated tests with synthetic data.

## SDP-220 - Missing security audit coverage

- **Failure:** Security-relevant actions cannot be attributed or investigated.
- **Detection:** Trace authentication, access denials, grant changes and administrative actions to audit events.
- **Remediation and safeguards:** Record actor, action, target, outcome and correlation with minimal sensitive data; durable audit intent where required.
- **Verification:** Exercise synthetic security actions; verify attributable records and no secrets; cross-reference SDP-157.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-221 - Audit trail tampering

- **Failure:** Unauthorized actors can alter or remove security evidence.
- **Detection:** Inspect audit write/delete privileges, retention, integrity and independent access.
- **Remediation and safeguards:** Separate audit authority, restrict deletion, use append-only or tamper-evident controls appropriate to risk.
- **Verification:** Attempt modification through low-privilege test identity; deny or detect tampering; authorized retention works.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-222 - Security alerting gap

- **Failure:** Abuse or control failure does not trigger actionable notification.
- **Detection:** Inspect detection rules, ownership, severity, routing and delivery failure handling.
- **Remediation and safeguards:** Define monitored security signals, thresholds, escalation and test alert delivery; avoid noisy alerts without ownership.
- **Verification:** Emit synthetic security event and verify alert arrives at test sink within target; deduplication works.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-223 - Error information disclosure

- **Failure:** Failures reveal internal implementation or sensitive values to callers.
- **Detection:** Inspect exception handlers, debug responses, API errors and error correlation.
- **Remediation and safeguards:** Return sanitized error contracts, maintain restricted diagnostics and correlation; never expose secret or stack details publicly.
- **Verification:** Trigger synthetic failure with marker; response contains safe error only and authorized log supports diagnosis.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-224 - Security configuration drift

- **Failure:** Effective controls diverge from approved baseline unnoticed.
- **Detection:** Inspect policy version, environment overrides, runtime evidence and ownership.
- **Remediation and safeguards:** Continuously validate effective controls, review changes and alert on unauthorized deviations.
- **Verification:** Change disposable policy and verify drift detected; approved change reconciles with audit trail.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-225 - Emergency credential response gap

- **Failure:** Compromised credentials cannot be revoked or isolated within required time.
- **Detection:** Inspect emergency revocation paths, ownership, dependency caches and runbooks.
- **Remediation and safeguards:** Define emergency rotation/revocation and containment with tested dependencies and communication; preserve service recovery.
- **Verification:** Run tabletop and synthetic credential revocation exercise; measure propagation and recovery gaps.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

