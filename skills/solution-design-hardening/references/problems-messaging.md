# Messaging - problem playbook

Signals are investigation leads, not findings. Confirm the business invariant and actual runtime guarantees. Tests are proposals until executed in an isolated environment. Use the simplest sufficient safeguard; do not introduce a pattern merely because it is listed.

Read only the problem files you need. Every problem below uses this decision rule:

- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

| ID | Problem | Guidance |
|---|---|---|
| SDP-054 | Message Loss | [SDP-054](problems/SDP-054.md) |
| SDP-055 | Duplicate Message | [SDP-055](problems/SDP-055.md) |
| SDP-056 | Out-of-Order Messages | [SDP-056](problems/SDP-056.md) |
| SDP-057 | Poison Message | [SDP-057](problems/SDP-057.md) |
| SDP-058 | Message Replay Side Effects | [SDP-058](problems/SDP-058.md) |
| SDP-059 | Consumer Lag | [SDP-059](problems/SDP-059.md) |
| SDP-060 | Message Schema Incompatibility | [SDP-060](problems/SDP-060.md) |
| SDP-061 | Eventual Consistency Window | [SDP-061](problems/SDP-061.md) |
| SDP-062 | Ghost Event | [SDP-062](problems/SDP-062.md) |
| SDP-063 | Missing Event | [SDP-063](problems/SDP-063.md) |
| SDP-064 | Event Processing Loop | [SDP-064](problems/SDP-064.md) |
| SDP-065 | Premature Acknowledgment | [SDP-065](problems/SDP-065.md) |
| SDP-066 | Event Notification Failure | [SDP-066](problems/SDP-066.md) |
| SDP-067 | Oversized Message | [SDP-067](problems/SDP-067.md) |
| SDP-068 | Event Choreography Complexity | [SDP-068](problems/SDP-068.md) |
