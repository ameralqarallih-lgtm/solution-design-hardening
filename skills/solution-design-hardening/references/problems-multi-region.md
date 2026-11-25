# Multi Region - problem playbook

Signals are investigation leads, not findings. Confirm the business invariant and actual runtime guarantees. Tests are proposals until executed in an isolated environment. Use the simplest sufficient safeguard; do not introduce a pattern merely because it is listed.

Read only the problem files you need. Every problem below uses this decision rule:

- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

| ID | Problem | Guidance |
|---|---|---|
| SDP-125 | Multi-region failover data loss | [SDP-125](problems/SDP-125.md) |
| SDP-126 | Stale regional writer routing | [SDP-126](problems/SDP-126.md) |
| SDP-127 | Unsafe failback | [SDP-127](problems/SDP-127.md) |
| SDP-128 | Quorum loss | [SDP-128](problems/SDP-128.md) |
| SDP-129 | Leader flapping | [SDP-129](problems/SDP-129.md) |
| SDP-130 | Lease renewal starvation | [SDP-130](problems/SDP-130.md) |
