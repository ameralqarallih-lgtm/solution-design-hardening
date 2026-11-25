# Database — problem playbook

Signals are investigation leads, not findings. Confirm the business invariant and actual runtime guarantees. Tests are proposals until executed in an isolated environment. Use the simplest sufficient safeguard; do not introduce a pattern merely because it is listed.

## SDP-023 — Dual Write (Database + Message Broker)

- **Failure:** Database commits successfully, but the corresponding event is not published.
- **Detection:** Database commit and broker publish separate operations.
- **Remediation and safeguards:** Write outbox in same local transaction; relay with confirmations and idempotent consumer.
- **Verification:** Crash before publish and after broker confirm before mark; event eventually processed once in effect.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-024 — Duplicate Event Processing

- **Failure:** The same event is delivered and processed multiple times.
- **Detection:** Consumer dedupe check separate from mutation.
- **Remediation and safeguards:** Unique inbox claim and business mutation in one transaction; external effects separately protected.
- **Verification:** Deliver identical event concurrently and after crash; one business mutation.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-025 — Dirty Read

- **Failure:** A transaction reads another transaction's uncommitted data.
- **Detection:** READ UNCOMMITTED or equivalent reads drive decisions.
- **Remediation and safeguards:** Use committed isolation or stronger as invariant requires; inspect engine settings.
- **Verification:** Hold uncommitted update then roll back; reader never acts on dirty value.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-026 — Non-Repeatable Read

- **Failure:** Reading the same record twice produces different values within one transaction.
- **Detection:** Repeated reads assume stable row under read committed.
- **Remediation and safeguards:** Use suitable repeatable snapshot or lock; check engine semantics.
- **Verification:** Update between reads; transaction observes required stable view or detects conflict.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-027 — Phantom Read

- **Failure:** New records appear between repeated queries within a transaction.
- **Detection:** Range count used for invariant without predicate protection.
- **Remediation and safeguards:** Serializable/predicate lock or materialized constraint; retry serialization failures.
- **Verification:** Concurrent inserts into checked range; invariant survives.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-028 — Write Skew

- **Failure:** Concurrent transactions independently satisfy conditions but collectively violate a business rule.
- **Detection:** Disjoint writes depend on shared snapshot predicate.
- **Remediation and safeguards:** Serializable isolation or lock shared invariant row; verify actual engine behavior.
- **Verification:** Two transactions independently pass predicate; at least one aborts if combined invalid.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-029 — Database Deadlock

- **Failure:** Transactions wait on each other's locks until interrupted.
- **Detection:** Opposite lock acquisition order or long transactions.
- **Remediation and safeguards:** Order locks consistently; shorten transaction; retry whole safe transaction after deadlock.
- **Verification:** Force opposing lock order; bounded recovery without duplicate external effects.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-030 — Race Condition

- **Failure:** The result depends on the execution order of concurrent operations.
- **Detection:** Shared mutable state or check-then-act across threads/processes.
- **Remediation and safeguards:** Use authoritative atomic operation or correctly scoped synchronization.
- **Verification:** Force competing interleaving; invariant holds across processes.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-031 — Replication Lag

- **Failure:** A read replica returns outdated data after a successful write.
- **Detection:** Post-write read routed to lagging replica.
- **Remediation and safeguards:** Route consistency-sensitive read to primary or wait for commit watermark.
- **Verification:** Delay replica apply; caller sees own write or explicit pending state.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-032 — Split-Brain

- **Failure:** Multiple database nodes incorrectly believe they are the primary.
- **Detection:** Two primaries accept writes after partition.
- **Remediation and safeguards:** Quorum-backed leadership and fencing at storage; define minority behavior.
- **Verification:** Partition old primary then promote new; stale primary cannot commit.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-033 — Database Hotspot

- **Failure:** Excessive transactions target a specific record or partition.
- **Detection:** Single row/partition serialized under skewed workload.
- **Remediation and safeguards:** Measure contention; partition only if invariants allow; batch or redesign allocation.
- **Verification:** Skew traffic and inspect lock waits; correctness unchanged at target load.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-034 — Cross-Database Transaction

- **Failure:** A business transaction spans multiple independent databases.
- **Detection:** Independent DB commits assumed atomic.
- **Remediation and safeguards:** Prefer one ownership boundary; otherwise saga/TCC or justified supported 2PC with recovery.
- **Verification:** Crash between database commits; recover to defined valid state.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-035 — Database Connection Exhaustion

- **Failure:** Requests consume all available database connections.
- **Detection:** Connections held across remote calls or unbounded pool per replica.
- **Remediation and safeguards:** Shorten scope; cap total pools and admission; dispose on error.
- **Verification:** Saturate dependency and scale replicas; connection count bounded and recovery occurs.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-036 — Inconsistent Distributed Data

- **Failure:** Independent services maintain conflicting versions of business data.
- **Detection:** Multiple services mutate same logical field without authority.
- **Remediation and safeguards:** Assign owner; version events and reconcile derived copies.
- **Verification:** Apply delayed conflicting update; owner wins by defined policy.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-037 — Orphaned Records

- **Failure:** Related records remain after incomplete operations or deletions.
- **Detection:** Child created without valid parent or deletion leaves dangling references.
- **Remediation and safeguards:** Foreign keys where local; durable lifecycle and reconciliation across boundaries.
- **Verification:** Fail parent/child lifecycle halfway; no invalid live child remains.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.
