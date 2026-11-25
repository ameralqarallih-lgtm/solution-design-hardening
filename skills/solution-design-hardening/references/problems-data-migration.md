# Data Migration - problem playbook

Signals are investigation leads, not findings. Confirm the business invariant and actual runtime guarantees. Tests are proposals until executed in an isolated environment. Use the simplest sufficient safeguard; do not introduce a pattern merely because it is listed.

Read only the problem files you need. Every problem below uses this decision rule:

- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

| ID | Problem | Guidance |
|---|---|---|
| SDP-105 | Multi-writer conflict | [SDP-105](problems/SDP-105.md) |
| SDP-106 | Tombstone resurrection | [SDP-106](problems/SDP-106.md) |
| SDP-107 | Projection rebuild inconsistency | [SDP-107](problems/SDP-107.md) |
| SDP-108 | Mixed-version deployment | [SDP-108](problems/SDP-108.md) |
| SDP-109 | Backfill race | [SDP-109](problems/SDP-109.md) |
| SDP-110 | Restore inconsistency | [SDP-110](problems/SDP-110.md) |
| SDP-111 | CDC retention gap | [SDP-111](problems/SDP-111.md) |
