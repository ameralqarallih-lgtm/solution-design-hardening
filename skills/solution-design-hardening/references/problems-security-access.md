# Authorization and business-flow security - problem playbook

Use [security assessment guidance](SECURITY-ASSESSMENT.md) and [standards mappings](SECURITY-STANDARDS.md). These are defensive investigation leads; confirm trust boundaries, reachability and effective controls. Use only authorized isolated tests with synthetic data.

Read only the problem files you need. Every problem below uses this decision rule:

- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

| ID | Problem | Guidance |
|---|---|---|
| SDP-171 | Object-level authorization failure | [SDP-171](problems/SDP-171.md) |
| SDP-172 | Function-level authorization failure | [SDP-172](problems/SDP-172.md) |
| SDP-173 | Unsafe property binding | [SDP-173](problems/SDP-173.md) |
| SDP-174 | Unauthorized property disclosure | [SDP-174](problems/SDP-174.md) |
| SDP-175 | Fail-open authorization | [SDP-175](problems/SDP-175.md) |
| SDP-176 | Privilege administration abuse | [SDP-176](problems/SDP-176.md) |
| SDP-177 | Sensitive business-flow abuse | [SDP-177](problems/SDP-177.md) |
| SDP-178 | Unsafe cross-origin trust | [SDP-178](problems/SDP-178.md) |
