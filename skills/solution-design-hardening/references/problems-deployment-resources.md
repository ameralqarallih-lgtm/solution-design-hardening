# Deployment Resources — problem playbook

Signals are investigation leads, not findings. Confirm the business invariant and actual runtime guarantees. Tests are proposals until executed in an isolated environment. Use the simplest sufficient safeguard; do not introduce a pattern merely because it is listed.

## SDP-137 — Configuration drift

- **Failure:** Replicas use incompatible safety settings.
- **Detection:** Replica configuration differs on consistency-critical settings.
- **Remediation and safeguards:** Version config and validate invariants on startup; compare live configuration safely.
- **Verification:** Start mismatched replicas; invalid config rejected or explicitly quarantined.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-138 — Incompatible rollback

- **Failure:** Old application cannot handle migrated data.
- **Detection:** Rollback deploys old binary after irreversible schema/data change.
- **Remediation and safeguards:** Maintain compatibility window or forward-fix plan; verify rollback preconditions.
- **Verification:** Apply migration then run supported rollback; no corrupt reads/writes.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-139 — Migration lock contention

- **Failure:** DDL blocks live workload.
- **Detection:** DDL holds blocking lock during normal traffic.
- **Remediation and safeguards:** Plan engine-specific online operations or controlled downtime; bound lock waits.
- **Verification:** Run migration with representative concurrent traffic; lock impact within budget.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-140 — Concurrent migration execution

- **Failure:** Multiple replicas apply schema changes concurrently.
- **Detection:** Every replica runs migration independently at startup.
- **Remediation and safeguards:** Single coordinated migration owner and versioned history; enforce safe startup.
- **Verification:** Start replicas simultaneously; migration executes safely once in effect.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-141 — Thread pool starvation

- **Failure:** Blocking work exhausts execution threads.
- **Detection:** Blocking I/O or sync waits exhaust request execution threads.
- **Remediation and safeguards:** Use asynchronous I/O where appropriate; bound blocking pools and work.
- **Verification:** Slow I/O under concurrency; thread use bounded and healthy requests progress.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-142 — Resource handle leak

- **Failure:** Failure paths retain connections or streams.
- **Detection:** Connections/streams not disposed on exceptions or cancellation.
- **Remediation and safeguards:** Structured cleanup and bounded lifetimes; monitor open handles.
- **Verification:** Repeat failed/canceled operations; handle counts return to baseline.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-143 — Unbounded memory growth

- **Failure:** Accumulated state or tasks exhaust memory.
- **Detection:** Unbounded collection or in-flight tasks grow under sustained load.
- **Remediation and safeguards:** Bound queues, caches and retained results; apply backpressure and eviction.
- **Verification:** Run sustained load; memory stabilizes and overload handled.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-144 — Autoscaling feedback mismatch

- **Failure:** Scaling signal ignores actual bottleneck.
- **Detection:** Autoscaler reacts to CPU while queue age or dependency saturation dominates.
- **Remediation and safeguards:** Use workload-appropriate signals and downstream capacity caps; stabilize scaling.
- **Verification:** Burst queue workload with low CPU; scale safely and drain backlog.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-145 — Cancellation resource leak

- **Failure:** Canceled requests leave expensive work running.
- **Detection:** Timeout cancels caller but expensive work continues consuming capacity.
- **Remediation and safeguards:** Propagate cooperative cancellation; isolate bounded noncancelable tasks; track actual completion.
- **Verification:** Cancel many slow operations; active resources return within declared bound.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.
