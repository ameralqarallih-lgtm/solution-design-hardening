# Deployment Resources - problem playbook

Signals are investigation leads, not findings. Confirm the business invariant and actual runtime guarantees. Tests are proposals until executed in an isolated environment. Use the simplest sufficient safeguard; do not introduce a pattern merely because it is listed.

Read only the problem files you need. Every problem below uses this decision rule:

- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

| ID | Problem | Guidance |
|---|---|---|
| SDP-137 | Configuration drift | [SDP-137](problems/SDP-137.md) |
| SDP-138 | Incompatible rollback | [SDP-138](problems/SDP-138.md) |
| SDP-139 | Migration lock contention | [SDP-139](problems/SDP-139.md) |
| SDP-140 | Concurrent migration execution | [SDP-140](problems/SDP-140.md) |
| SDP-141 | Thread pool starvation | [SDP-141](problems/SDP-141.md) |
| SDP-142 | Resource handle leak | [SDP-142](problems/SDP-142.md) |
| SDP-143 | Unbounded memory growth | [SDP-143](problems/SDP-143.md) |
| SDP-144 | Autoscaling feedback mismatch | [SDP-144](problems/SDP-144.md) |
| SDP-145 | Cancellation resource leak | [SDP-145](problems/SDP-145.md) |
