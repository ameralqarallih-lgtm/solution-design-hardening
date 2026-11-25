# Caching - problem playbook

Signals are investigation leads, not findings. Confirm the business invariant and actual runtime guarantees. Tests are proposals until executed in an isolated environment. Use the simplest sufficient safeguard; do not introduce a pattern merely because it is listed.

Read only the problem files you need. Every problem below uses this decision rule:

- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

| ID | Problem | Guidance |
|---|---|---|
| SDP-011 | Stale Data | [SDP-011](problems/SDP-011.md) |
| SDP-012 | Dual Write Problem | [SDP-012](problems/SDP-012.md) |
| SDP-013 | Cache Stampede (Thundering Herd) | [SDP-013](problems/SDP-013.md) |
| SDP-014 | Cache Avalanche | [SDP-014](problems/SDP-014.md) |
| SDP-015 | Cache Penetration | [SDP-015](problems/SDP-015.md) |
| SDP-016 | Cache Breakdown | [SDP-016](problems/SDP-016.md) |
| SDP-017 | Hot Key Problem | [SDP-017](problems/SDP-017.md) |
| SDP-018 | Cache Poisoning | [SDP-018](problems/SDP-018.md) |
| SDP-019 | Cache Invalidation Race | [SDP-019](problems/SDP-019.md) |
| SDP-020 | Cold Cache Problem | [SDP-020](problems/SDP-020.md) |
| SDP-021 | Cache Dependency Failure | [SDP-021](problems/SDP-021.md) |
| SDP-022 | Cache Memory Exhaustion | [SDP-022](problems/SDP-022.md) |
