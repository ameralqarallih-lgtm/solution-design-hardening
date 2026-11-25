# Api - problem playbook

Signals are investigation leads, not findings. Confirm the business invariant and actual runtime guarantees. Tests are proposals until executed in an isolated environment. Use the simplest sufficient safeguard; do not introduce a pattern merely because it is listed.

Read only the problem files you need. Every problem below uses this decision rule:

- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

| ID | Problem | Guidance |
|---|---|---|
| SDP-069 | Duplicate API Submission | [SDP-069](problems/SDP-069.md) |
| SDP-070 | Timeout Ambiguity | [SDP-070](problems/SDP-070.md) |
| SDP-071 | Long-Running Request | [SDP-071](problems/SDP-071.md) |
| SDP-072 | Concurrent API Updates | [SDP-072](problems/SDP-072.md) |
| SDP-073 | API Request Flooding | [SDP-073](problems/SDP-073.md) |
| SDP-074 | N+1 Request Problem | [SDP-074](problems/SDP-074.md) |
| SDP-075 | Overfetching | [SDP-075](problems/SDP-075.md) |
| SDP-076 | Underfetching | [SDP-076](problems/SDP-076.md) |
| SDP-077 | Pagination Drift | [SDP-077](problems/SDP-077.md) |
| SDP-078 | Request Replay Attack | [SDP-078](problems/SDP-078.md) |
| SDP-079 | Partial Bulk Operation Failure | [SDP-079](problems/SDP-079.md) |
| SDP-080 | API Fan-Out Failure | [SDP-080](problems/SDP-080.md) |
