# Financial Extensions - problem playbook

Signals are investigation leads, not findings. Confirm the business invariant and actual runtime guarantees. Tests are proposals until executed in an isolated environment. Use the simplest sufficient safeguard; do not introduce a pattern merely because it is listed.

Read only the problem files you need. Every problem below uses this decision rule:

- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

| ID | Problem | Guidance |
|---|---|---|
| SDP-101 | Monetary rounding drift | [SDP-101](problems/SDP-101.md) |
| SDP-102 | Currency mixing | [SDP-102](problems/SDP-102.md) |
| SDP-103 | Idempotency retention gap | [SDP-103](problems/SDP-103.md) |
| SDP-104 | Concurrent idempotency claim | [SDP-104](problems/SDP-104.md) |
