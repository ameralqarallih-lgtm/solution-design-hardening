# Lifecycle - problem playbook

Signals are investigation leads, not findings. Confirm the business invariant and actual runtime guarantees. Tests are proposals until executed in an isolated environment. Use the simplest sufficient safeguard; do not introduce a pattern merely because it is listed.

Read only the problem files you need. Every problem below uses this decision rule:

- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

| ID | Problem | Guidance |
|---|---|---|
| SDP-151 | Mutable outbox payload | [SDP-151](problems/SDP-151.md) |
| SDP-152 | Event sequence gap | [SDP-152](problems/SDP-152.md) |
| SDP-153 | Idempotency scope collision | [SDP-153](problems/SDP-153.md) |
| SDP-154 | Reconnect storm | [SDP-154](problems/SDP-154.md) |
| SDP-155 | Schedule timezone ambiguity | [SDP-155](problems/SDP-155.md) |
| SDP-156 | Incomplete deletion propagation | [SDP-156](problems/SDP-156.md) |
| SDP-157 | Audit dual write | [SDP-157](problems/SDP-157.md) |
| SDP-158 | Distributed provider quota breach | [SDP-158](problems/SDP-158.md) |
| SDP-159 | Claim-check retention mismatch | [SDP-159](problems/SDP-159.md) |
| SDP-160 | Long snapshot retention pressure | [SDP-160](problems/SDP-160.md) |
