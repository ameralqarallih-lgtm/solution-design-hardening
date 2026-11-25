# Software supply chain - problem playbook

Use [security assessment guidance](SECURITY-ASSESSMENT.md) and [standards mappings](SECURITY-STANDARDS.md). These are defensive investigation leads; confirm trust boundaries, reachability and effective controls. Use only authorized isolated tests with synthetic data.

Read only the problem files you need. Every problem below uses this decision rule:

- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

| ID | Problem | Guidance |
|---|---|---|
| SDP-213 | Vulnerable dependency exposure | [SDP-213](problems/SDP-213.md) |
| SDP-214 | Dependency confusion | [SDP-214](problems/SDP-214.md) |
| SDP-215 | Artifact integrity failure | [SDP-215](problems/SDP-215.md) |
| SDP-216 | Untrusted CI execution | [SDP-216](problems/SDP-216.md) |
| SDP-217 | Pipeline credential leakage | [SDP-217](problems/SDP-217.md) |
| SDP-218 | Missing build provenance | [SDP-218](problems/SDP-218.md) |
| SDP-219 | Unsupported component lifecycle | [SDP-219](problems/SDP-219.md) |
