# Security - problem playbook

Signals are investigation leads, not findings. Confirm the business invariant and actual runtime guarantees. Tests are proposals until executed in an isolated environment. Use the simplest sufficient safeguard; do not introduce a pattern merely because it is listed.

Read only the problem files you need. Every problem below uses this decision rule:

- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

| ID | Problem | Guidance |
|---|---|---|
| SDP-131 | Authorization TOCTOU | [SDP-131](problems/SDP-131.md) |
| SDP-132 | Authorization cache staleness | [SDP-132](problems/SDP-132.md) |
| SDP-133 | Token refresh race | [SDP-133](problems/SDP-133.md) |
| SDP-134 | Confused deputy | [SDP-134](problems/SDP-134.md) |
| SDP-135 | Sensitive telemetry leakage | [SDP-135](problems/SDP-135.md) |
| SDP-136 | Input resource amplification | [SDP-136](problems/SDP-136.md) |
