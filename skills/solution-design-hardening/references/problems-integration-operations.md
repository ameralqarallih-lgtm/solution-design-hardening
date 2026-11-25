# Integration Operations - problem playbook

Signals are investigation leads, not findings. Confirm the business invariant and actual runtime guarantees. Tests are proposals until executed in an isolated environment. Use the simplest sufficient safeguard; do not introduce a pattern merely because it is listed.

Read only the problem files you need. Every problem below uses this decision rule:

- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

| ID | Problem | Guidance |
|---|---|---|
| SDP-112 | Webhook authenticity failure | [SDP-112](problems/SDP-112.md) |
| SDP-113 | Unbounded deduplication state | [SDP-113](problems/SDP-113.md) |
| SDP-114 | Outbox relay backlog | [SDP-114](problems/SDP-114.md) |
| SDP-115 | Unsafe dead-letter replay | [SDP-115](problems/SDP-115.md) |
| SDP-116 | Cancellation ambiguity | [SDP-116](problems/SDP-116.md) |
| SDP-117 | Graceful shutdown failure | [SDP-117](problems/SDP-117.md) |
| SDP-118 | Readiness-induced overload | [SDP-118](problems/SDP-118.md) |
| SDP-119 | Missing recovery signals | [SDP-119](problems/SDP-119.md) |
| SDP-120 | Cross-tenant state leakage | [SDP-120](problems/SDP-120.md) |
| SDP-121 | Unsafe reconciliation overwrite | [SDP-121](problems/SDP-121.md) |
| SDP-122 | Unbounded fan-out | [SDP-122](problems/SDP-122.md) |
| SDP-123 | Dependency contract drift | [SDP-123](problems/SDP-123.md) |
| SDP-124 | Object cleanup race | [SDP-124](problems/SDP-124.md) |
