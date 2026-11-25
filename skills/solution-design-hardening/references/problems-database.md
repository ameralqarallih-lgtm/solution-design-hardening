# Database - problem playbook

Signals are investigation leads, not findings. Confirm the business invariant and actual runtime guarantees. Tests are proposals until executed in an isolated environment. Use the simplest sufficient safeguard; do not introduce a pattern merely because it is listed.

Read only the problem files you need. Every problem below uses this decision rule:

- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

| ID | Problem | Guidance |
|---|---|---|
| SDP-023 | Dual Write (Database + Message Broker) | [SDP-023](problems/SDP-023.md) |
| SDP-024 | Duplicate Event Processing | [SDP-024](problems/SDP-024.md) |
| SDP-025 | Dirty Read | [SDP-025](problems/SDP-025.md) |
| SDP-026 | Non-Repeatable Read | [SDP-026](problems/SDP-026.md) |
| SDP-027 | Phantom Read | [SDP-027](problems/SDP-027.md) |
| SDP-028 | Write Skew | [SDP-028](problems/SDP-028.md) |
| SDP-029 | Database Deadlock | [SDP-029](problems/SDP-029.md) |
| SDP-030 | Race Condition | [SDP-030](problems/SDP-030.md) |
| SDP-031 | Replication Lag | [SDP-031](problems/SDP-031.md) |
| SDP-032 | Split-Brain | [SDP-032](problems/SDP-032.md) |
| SDP-033 | Database Hotspot | [SDP-033](problems/SDP-033.md) |
| SDP-034 | Cross-Database Transaction | [SDP-034](problems/SDP-034.md) |
| SDP-035 | Database Connection Exhaustion | [SDP-035](problems/SDP-035.md) |
| SDP-036 | Inconsistent Distributed Data | [SDP-036](problems/SDP-036.md) |
| SDP-037 | Orphaned Records | [SDP-037](problems/SDP-037.md) |
