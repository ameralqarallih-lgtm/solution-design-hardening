# Storage - problem playbook

Signals are investigation leads, not findings. Confirm the business invariant and actual runtime guarantees. Tests are proposals until executed in an isolated environment. Use the simplest sufficient safeguard; do not introduce a pattern merely because it is listed.

Read only the problem files you need. Every problem below uses this decision rule:

- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

| ID | Problem | Guidance |
|---|---|---|
| SDP-092 | Orphaned File | [SDP-092](problems/SDP-092.md) |
| SDP-093 | Missing File | [SDP-093](problems/SDP-093.md) |
| SDP-094 | Dual Write (Database + Object Storage) | [SDP-094](problems/SDP-094.md) |
| SDP-095 | Concurrent File Modification | [SDP-095](problems/SDP-095.md) |
| SDP-096 | Incomplete File Upload | [SDP-096](problems/SDP-096.md) |
| SDP-097 | File Corruption | [SDP-097](problems/SDP-097.md) |
| SDP-098 | Duplicate File Storage | [SDP-098](problems/SDP-098.md) |
| SDP-099 | Unauthorized File Access | [SDP-099](problems/SDP-099.md) |
| SDP-100 | Deleted File Recovery | [SDP-100](problems/SDP-100.md) |
