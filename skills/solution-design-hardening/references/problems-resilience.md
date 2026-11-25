# Resilience — problem playbook

Signals are investigation leads, not findings. Confirm the business invariant and actual runtime guarantees. Tests are proposals until executed in an isolated environment. Use the simplest sufficient safeguard; do not introduce a pattern merely because it is listed.

## SDP-038 — Retry Storm

- **Failure:** Multiple services continuously retry failed requests, overwhelming the system.
- **Detection:** Fixed frequent retries during outage.
- **Remediation and safeguards:** Bound attempts and deadline, jitter backoff and budget; respect retry hints.
- **Verification:** Outage with many clients; retry traffic bounded and desynchronized.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-039 — Retry Amplification

- **Failure:** Each layer of a distributed system independently retries the same operation.
- **Detection:** SDK, service and gateway each independently retry.
- **Remediation and safeguards:** Inventory retry layers; designate owner and propagate deadline/budget.
- **Verification:** Inject failures; count actual downstream attempts against end-to-end budget.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-040 — Cascading Failure

- **Failure:** Failure of one service causes other dependent services to fail.
- **Detection:** Downstream latency exhausts upstream resources.
- **Remediation and safeguards:** Timeouts, circuit breaker and isolated pools; bounded recovery probes.
- **Verification:** Fail dependency under traffic; unrelated endpoints remain available.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-041 — Thundering Herd

- **Failure:** Many clients simultaneously request the same resource.
- **Detection:** Many clients reconnect or refresh simultaneously.
- **Remediation and safeguards:** Jitter schedules, coalesce work and admit bounded concurrency.
- **Verification:** Trigger simultaneous reconnect; peak work stays within limit.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-042 — Slow Dependency

- **Failure:** A slow downstream service consumes upstream resources.
- **Detection:** No timeout or each hop resets full timeout.
- **Remediation and safeguards:** Propagate remaining deadline; cancel cooperative work; bound noncancelable tasks.
- **Verification:** Slow leaf service; upstream releases resources within budget.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-043 — Resource Starvation

- **Failure:** One workload consumes resources needed by other workloads.
- **Detection:** Long-running jobs share all threads/connections with interactive requests.
- **Remediation and safeguards:** Separate bounded pools/queues and reserve critical capacity.
- **Verification:** Saturate batch work; interactive latency remains within target.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-044 — Backpressure Problem

- **Failure:** Producers generate requests faster than consumers can process them.
- **Detection:** Producer enqueues without bounded capacity or demand control.
- **Remediation and safeguards:** Bound queue and in-flight work; propagate overload or durable buffering policy.
- **Verification:** Producer exceeds consumer capacity; memory bounded and overload explicit.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-045 — Head-of-Line Blocking

- **Failure:** A slow request blocks subsequent requests.
- **Detection:** Slow item blocks unrelated items in same queue.
- **Remediation and safeguards:** Partition by required order scope; isolate slow workloads; retain per-key ordering.
- **Verification:** Block one key; unrelated keys progress without reordering same key.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-046 — Distributed Lock Expiration

- **Failure:** A lock expires while its original owner is still performing an operation.
- **Detection:** Lease expires while holder continues writing.
- **Remediation and safeguards:** Use monotonic fencing checked by protected resource; otherwise atomic resource operation.
- **Verification:** Pause holder beyond expiry; newer holder writes; old write rejected.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-047 — Zombie Process

- **Failure:** A previously disconnected service resumes operating with outdated authority.
- **Detection:** Former leader resumes after losing authority.
- **Remediation and safeguards:** Validate epoch on every protected effect; revoke or fence stale authority.
- **Verification:** Suspend old process and elect replacement; resume old process; no stale effects.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-048 — Network Partition

- **Failure:** Distributed components cannot communicate with each other.
- **Detection:** Partition behavior unspecified or unsafe availability preference.
- **Remediation and safeguards:** Define invariant-specific quorum and degraded behavior; reconcile permitted divergent writes.
- **Verification:** Partition network; minority cannot violate strong invariant; heal and verify.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-049 — Clock Skew

- **Failure:** Different servers have inconsistent system clocks.
- **Detection:** Wall-clock comparisons determine ownership or causal order.
- **Remediation and safeguards:** Use monotonic elapsed timers, authoritative lease service or logical versions.
- **Verification:** Jump clocks forward/back; deadlines and ordering remain valid.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-050 — Single Point of Failure

- **Failure:** Failure of a single component disables the entire system.
- **Detection:** Critical dependency has no redundant recovery path.
- **Remediation and safeguards:** Match redundancy and recovery design to RTO/RPO; verify failure domains.
- **Verification:** Remove single component; measure service recovery and data loss.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-051 — Noisy Neighbor

- **Failure:** One tenant negatively affects other tenants.
- **Detection:** One tenant consumes shared quota/pool.
- **Remediation and safeguards:** Per-tenant admission and fair scheduling with global cap.
- **Verification:** Flood one tenant; others retain service within agreed limits.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-052 — Overload Collapse

- **Failure:** Increased workload reduces the system's overall processing capacity.
- **Detection:** Queue growth increases latency and retry feedback.
- **Remediation and safeguards:** Admission control, bounded work and early shedding.
- **Verification:** Ramp above sustainable capacity; goodput does not collapse and system recovers.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-053 — Failover Storm

- **Failure:** Multiple workloads simultaneously fail over to secondary resources.
- **Detection:** All clients fail over to undersized standby at once.
- **Remediation and safeguards:** Reserve failover capacity; jitter reconnect and throttle migration.
- **Verification:** Simulate primary outage; standby remains within safe capacity.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.
