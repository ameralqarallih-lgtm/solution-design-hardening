# Security monitoring and operations - problem playbook

Use [security assessment guidance](SECURITY-ASSESSMENT.md) and [standards mappings](SECURITY-STANDARDS.md). These are defensive investigation leads; confirm trust boundaries, reachability and effective controls. Use only authorized isolated tests with synthetic data.

Read only the problem files you need. Every problem below uses this decision rule:

- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

| ID | Problem | Guidance |
|---|---|---|
| SDP-220 | Missing security audit coverage | [SDP-220](problems/SDP-220.md) |
| SDP-221 | Audit trail tampering | [SDP-221](problems/SDP-221.md) |
| SDP-222 | Security alerting gap | [SDP-222](problems/SDP-222.md) |
| SDP-223 | Error information disclosure | [SDP-223](problems/SDP-223.md) |
| SDP-224 | Security configuration drift | [SDP-224](problems/SDP-224.md) |
| SDP-225 | Emergency credential response gap | [SDP-225](problems/SDP-225.md) |
