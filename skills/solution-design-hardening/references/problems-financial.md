# Financial - problem playbook

Signals are investigation leads, not findings. Confirm the business invariant and actual runtime guarantees. Tests are proposals until executed in an isolated environment. Use the simplest sufficient safeguard; do not introduce a pattern merely because it is listed.

Read only the problem files you need. Every problem below uses this decision rule:

- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

| ID | Problem | Guidance |
|---|---|---|
| SDP-001 | Duplicate Charge | [SDP-001](problems/SDP-001.md) |
| SDP-002 | Inconsistent Financial Balance | [SDP-002](problems/SDP-002.md) |
| SDP-003 | Double Spending | [SDP-003](problems/SDP-003.md) |
| SDP-004 | Lost Update | [SDP-004](problems/SDP-004.md) |
| SDP-005 | Partial Transaction Failure | [SDP-005](problems/SDP-005.md) |
| SDP-006 | Uncertain Transaction Status | [SDP-006](problems/SDP-006.md) |
| SDP-007 | Financial Record Manipulation | [SDP-007](problems/SDP-007.md) |
| SDP-008 | Balance Calculation Drift | [SDP-008](problems/SDP-008.md) |
| SDP-009 | Concurrent Resource Reservation | [SDP-009](problems/SDP-009.md) |
| SDP-010 | Abandoned Reservation | [SDP-010](problems/SDP-010.md) |
