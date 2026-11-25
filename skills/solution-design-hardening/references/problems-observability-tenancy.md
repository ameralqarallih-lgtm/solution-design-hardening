# Observability Tenancy - problem playbook

Signals are investigation leads, not findings. Confirm the business invariant and actual runtime guarantees. Tests are proposals until executed in an isolated environment. Use the simplest sufficient safeguard; do not introduce a pattern merely because it is listed.

Read only the problem files you need. Every problem below uses this decision rule:

- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

| ID | Problem | Guidance |
|---|---|---|
| SDP-146 | Metrics cardinality explosion | [SDP-146](problems/SDP-146.md) |
| SDP-147 | Telemetry backpressure | [SDP-147](problems/SDP-147.md) |
| SDP-148 | Broken trace propagation | [SDP-148](problems/SDP-148.md) |
| SDP-149 | Tenant migration race | [SDP-149](problems/SDP-149.md) |
| SDP-150 | Background tenant context loss | [SDP-150](problems/SDP-150.md) |
