# Authentication and identity - problem playbook

Use [security assessment guidance](SECURITY-ASSESSMENT.md) and [standards mappings](SECURITY-STANDARDS.md). These are defensive investigation leads; confirm trust boundaries, reachability and effective controls. Use only authorized isolated tests with synthetic data.

Read only the problem files you need. Every problem below uses this decision rule:

- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

| ID | Problem | Guidance |
|---|---|---|
| SDP-161 | Authentication bypass | [SDP-161](problems/SDP-161.md) |
| SDP-162 | Session fixation | [SDP-162](problems/SDP-162.md) |
| SDP-163 | Session theft and unsafe cookies | [SDP-163](problems/SDP-163.md) |
| SDP-164 | Credential stuffing and brute force | [SDP-164](problems/SDP-164.md) |
| SDP-165 | Token validation failure | [SDP-165](problems/SDP-165.md) |
| SDP-166 | Token revocation gap | [SDP-166](problems/SDP-166.md) |
| SDP-167 | OAuth and OIDC binding failure | [SDP-167](problems/SDP-167.md) |
| SDP-168 | Account enumeration | [SDP-168](problems/SDP-168.md) |
| SDP-169 | Unsafe account recovery | [SDP-169](problems/SDP-169.md) |
| SDP-170 | Workload identity impersonation | [SDP-170](problems/SDP-170.md) |
