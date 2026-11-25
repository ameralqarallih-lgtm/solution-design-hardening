# Data protection and cryptography - problem playbook

Use [security assessment guidance](SECURITY-ASSESSMENT.md) and [standards mappings](SECURITY-STANDARDS.md). These are defensive investigation leads; confirm trust boundaries, reachability and effective controls. Use only authorized isolated tests with synthetic data.

Read only the problem files you need. Every problem below uses this decision rule:

- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

| ID | Problem | Guidance |
|---|---|---|
| SDP-193 | Hardcoded secrets | [SDP-193](problems/SDP-193.md) |
| SDP-194 | Secret exposure in artifacts and history | [SDP-194](problems/SDP-194.md) |
| SDP-195 | Unprotected sensitive storage | [SDP-195](problems/SDP-195.md) |
| SDP-196 | Cleartext sensitive transport | [SDP-196](problems/SDP-196.md) |
| SDP-197 | Disabled TLS certificate validation | [SDP-197](problems/SDP-197.md) |
| SDP-198 | Weak password storage | [SDP-198](problems/SDP-198.md) |
| SDP-199 | Unsafe cryptographic primitive or mode | [SDP-199](problems/SDP-199.md) |
| SDP-200 | Cryptographic nonce reuse | [SDP-200](problems/SDP-200.md) |
| SDP-201 | Predictable security tokens | [SDP-201](problems/SDP-201.md) |
| SDP-202 | Key lifecycle and rotation failure | [SDP-202](problems/SDP-202.md) |
| SDP-203 | Sensitive data lifecycle mismatch | [SDP-203](problems/SDP-203.md) |
