# Workflow - problem playbook

Signals are investigation leads, not findings. Confirm the business invariant and actual runtime guarantees. Tests are proposals until executed in an isolated environment. Use the simplest sufficient safeguard; do not introduce a pattern merely because it is listed.

Read only the problem files you need. Every problem below uses this decision rule:

- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

| ID | Problem | Guidance |
|---|---|---|
| SDP-081 | Duplicate Scheduled Job | [SDP-081](problems/SDP-081.md) |
| SDP-082 | Overlapping Job Execution | [SDP-082](problems/SDP-082.md) |
| SDP-083 | Stuck Workflow | [SDP-083](problems/SDP-083.md) |
| SDP-084 | Lost Job Progress | [SDP-084](problems/SDP-084.md) |
| SDP-085 | Partial Workflow Completion | [SDP-085](problems/SDP-085.md) |
| SDP-086 | Orphaned Background Job | [SDP-086](problems/SDP-086.md) |
| SDP-087 | Infinite Retry Loop | [SDP-087](problems/SDP-087.md) |
| SDP-088 | Job Starvation | [SDP-088](problems/SDP-088.md) |
| SDP-089 | Missed Scheduled Execution | [SDP-089](problems/SDP-089.md) |
| SDP-090 | Invalid State Transition | [SDP-090](problems/SDP-090.md) |
| SDP-091 | Duplicate External Side Effect | [SDP-091](problems/SDP-091.md) |
