# Resilience - problem playbook

Signals are investigation leads, not findings. Confirm the business invariant and actual runtime guarantees. Tests are proposals until executed in an isolated environment. Use the simplest sufficient safeguard; do not introduce a pattern merely because it is listed.

Read only the problem files you need. Every problem below uses this decision rule:

- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

| ID | Problem | Guidance |
|---|---|---|
| SDP-038 | Retry Storm | [SDP-038](problems/SDP-038.md) |
| SDP-039 | Retry Amplification | [SDP-039](problems/SDP-039.md) |
| SDP-040 | Cascading Failure | [SDP-040](problems/SDP-040.md) |
| SDP-041 | Thundering Herd | [SDP-041](problems/SDP-041.md) |
| SDP-042 | Slow Dependency | [SDP-042](problems/SDP-042.md) |
| SDP-043 | Resource Starvation | [SDP-043](problems/SDP-043.md) |
| SDP-044 | Backpressure Problem | [SDP-044](problems/SDP-044.md) |
| SDP-045 | Head-of-Line Blocking | [SDP-045](problems/SDP-045.md) |
| SDP-046 | Distributed Lock Expiration | [SDP-046](problems/SDP-046.md) |
| SDP-047 | Zombie Process | [SDP-047](problems/SDP-047.md) |
| SDP-048 | Network Partition | [SDP-048](problems/SDP-048.md) |
| SDP-049 | Clock Skew | [SDP-049](problems/SDP-049.md) |
| SDP-050 | Single Point of Failure | [SDP-050](problems/SDP-050.md) |
| SDP-051 | Noisy Neighbor | [SDP-051](problems/SDP-051.md) |
| SDP-052 | Overload Collapse | [SDP-052](problems/SDP-052.md) |
| SDP-053 | Failover Storm | [SDP-053](problems/SDP-053.md) |
