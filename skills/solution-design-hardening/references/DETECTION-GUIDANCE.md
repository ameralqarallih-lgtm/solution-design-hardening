# Detection playbook

Signals are investigation leads, not defects by themselves. Trace all writers, constraints, actual isolation levels and deployment topology before assigning a finding. Use the catalog IDs in reports.

| Scope | Look for | Disprove or verify |
|---|---|---|
| SDP-001–010, 101–104 | Check-then-charge, read-modify-write balance, floating point amounts, mutable ledger, expired dedupe keys | Inspect unique constraints, transaction scope and provider keys; force concurrent duplicates and timeout after provider success |
| SDP-011–022 | In-flight reader refills an older version after committed update and invalidation, missed invalidation, synchronized TTL, unbounded fallback, tenant-free keys | Reproduce reader-load, writer-commit, writer-invalidate, reader-refill. Check the version at fill time. Also test tolerated stale windows, outages and hot-key expiration. |
| SDP-023–037 | DB save then publish, separate dedupe and commit, low isolation for multi-row invariants, read replicas after writes, unbounded pools | Confirm actual transaction enlistment and DB engine semantics; crash at commit/publish boundary; test write skew with separate connections |
| SDP-038–053 | Nested retries, missing deadlines, unlimited queues, local locks in multi-replica deployment, lease without enforced fencing | Confirm actual effective retry policy and topology; measure attempts and resource limits; pause owner until lease expires then resume |
| SDP-054–068 | Ack before commit, unstable event IDs, blind replay, no ordering checks, unlimited redelivery | Verify broker semantics and local transaction boundaries; kill worker before ack; replay out of order and duplicate |
| SDP-069–080 | Non-idempotent POST retry, blind updates, unbounded fan-out, offset pagination on mutable rows | Check operation contract and uniqueness; concurrent conditional update; test cursor with inserts and deletes |
| SDP-081–091 | In-memory job progress, scheduler per replica, non-atomic claim, external side effects before checkpoint | Test two workers, lease loss, crash after side effect and compensation failure |
| SDP-092–100 | Object upload and metadata save without recoverable state, cleanup by age alone, unchecked signed URLs | Crash between writes; test finalize/cleanup race and tenant authorization |
| SDP-105–111 | Timestamp-only conflict resolution, tombstone expiry, rebuild without catch-up, incompatible DDL, blind backfill, mismatched restore, CDC offset loss | Test mixed versions, delayed replay, concurrent backfill and recovery from expired offsets |
| SDP-112–124 | Unverified callbacks, indefinite dedupe growth, stale outbox, blind redrive, cancellation assumed final, abrupt termination, expensive probes, missing business signals, tenant-free keys, blind repair, unbounded fan-out, provider drift, unsafe cleanup | Exercise forged/duplicate callback, paused relay, shutdown, bounded overload, tenant isolation, concurrent repair and cleanup |

## Investigation method

1. Identify invariant and authority (database constraint, aggregate, external provider, etc.).
2. Locate all entry points, retries, writers and consumers, including administrative or batch paths.
3. Draw the smallest sequence of operations; insert a crash or competing write between each non-atomic step.
4. Verify effective safeguards, including runtime configuration, DB uniqueness, transaction propagation, broker acknowledgment and deployment replicas.
5. Record a minimal counterexample or explain why the existing safeguard is sufficient. If evidence is unavailable, mark Requires Verification.

In a short scenario, put the fact and required invariant next to each finding. Describe the failed execution in the order the scenario gives. If a commit precedes publication, test a stop after commit and before publication. Verify that durable event intent remains available on restart and replay produces one business effect.

## False-positive controls

- Two constrained writes within one local transaction can preserve a local invariant. Verify the actual transaction scope and constraint or rollback behavior. Escalate the design only if evidence shows a separate effect or boundary.
- An outbox is unnecessary when no durable cross-boundary publication is required. Best-effort telemetry is not a transactional business event.
- A cache may legitimately serve stale display data within an agreed window; correctness-critical authorization or balance checks differ.
- A local lock can protect an in-memory per-process counter or registry. Verify local thread behavior. A scanner hit or a multi-replica deployment does not establish a shared invariant.
- A naturally idempotent assignment may still trigger non-idempotent notifications or audit effects; inspect the whole operation.
- No finding solely because a named pattern or dependency is absent. Do not claim a mitigation from a library import alone.
