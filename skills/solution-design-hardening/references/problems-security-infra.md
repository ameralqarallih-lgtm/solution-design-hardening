# Distributed and infrastructure security - problem playbook

Use [security assessment guidance](SECURITY-ASSESSMENT.md) and [standards mappings](SECURITY-STANDARDS.md). These are defensive investigation leads; confirm trust boundaries, reachability and effective controls. Use only authorized isolated tests with synthetic data.

Read only the problem files you need. Every problem below uses this decision rule:

- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

| ID | Problem | Guidance |
|---|---|---|
| SDP-204 | Unauthenticated internal service | [SDP-204](problems/SDP-204.md) |
| SDP-205 | Unrestricted network reachability | [SDP-205](problems/SDP-205.md) |
| SDP-206 | Unauthorized message operations | [SDP-206](problems/SDP-206.md) |
| SDP-207 | Message integrity and trust failure | [SDP-207](problems/SDP-207.md) |
| SDP-208 | Excessive workload privileges | [SDP-208](problems/SDP-208.md) |
| SDP-209 | Exposed management surface | [SDP-209](problems/SDP-209.md) |
| SDP-210 | Insecure deployment defaults | [SDP-210](problems/SDP-210.md) |
| SDP-211 | Cross-environment credential reuse | [SDP-211](problems/SDP-211.md) |
| SDP-212 | Stale API inventory | [SDP-212](problems/SDP-212.md) |
