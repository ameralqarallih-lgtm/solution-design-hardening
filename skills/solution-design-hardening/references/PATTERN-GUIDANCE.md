# Pattern selection and verification guide

Use the repository catalog for the complete problem inventory. These rules supplement it with implementation cautions and checks. Adapt to the actual stack and business requirements.

| Area | Implementation guidance | Verification |
|---|---|---|
| Financial ledger | Post balanced entries atomically per currency; use exact monetary representation, immutable postings and reversals; enforce spending invariants separately. | Unbalanced posting rejected; concurrent spending cannot exceed available funds; reconcile balances. |
| Duplicate charge / submission | Scope idempotency keys to tenant and operation; atomically claim keys; compare request fingerprint; persist outcome; propagate stable keys to external providers. Reconcile unknown outcomes rather than blindly retrying. | Concurrent same-key calls produce one effect; changed payload rejected; crash after external success is recoverable. |
| Concurrency | Prefer constraints and atomic conditional updates; select isolation based on invariants; retry conflicts only within bounds. Distributed locks need lease/fencing protections at the protected resource. | Lost updates, write skew, double reservation and expired-lock-owner writes are prevented. |
| Outbox / inbox | Persist outgoing event in the same transaction as business data; publish with confirmation; mark sent after confirmation. Atomically deduplicate incoming messages with local state changes; external effects need separate idempotency. | Crash before publish and after publish/before marking sent; duplicate delivery; rollback produces no event. |
| Saga / workflows | Persist state; define legal transitions, idempotent steps, compensation, timeouts and manual recovery. Compensation is not a database rollback. | Crash between steps, failed compensation, duplicate callbacks, replay and restart. |
| Cache consistency | Commit authoritative write first; invalidate with durable intent when necessary; guard against stale refill with versions or suitable coordination. TTL bounds freshness only under stated assumptions. Bypass cache for correctness-critical reads if needed. | Concurrent refill/invalidation, missed invalidation, replica lag and cache outage. |
| Cache overload | Coalesce misses within the required scope; add randomized TTL, bounded negative caching, warming and controlled fallback. Avoid serving stale values beyond allowed freshness. | Concurrent hot-key expiration and mass expiration do not overload database; cache outage remains bounded. |
| Retries / cascading failure | Set end-to-end deadlines, bounded retries with jitter and retry budgets; honor downstream guidance; use circuit breakers, bulkheads and admission control. Avoid independent retries at every layer. | Simulate slow/unavailable dependency; measure bounded request amplification and recovery. |
| Messaging | Use durable delivery, confirmation and post-commit acknowledgment; define ordering scope, sequence/version checks, bounded retries and DLQ replay procedures. Do not claim end-to-end exactly-once without proof. | Duplicate/out-of-order messages, poison events, broker outage, replay and schema compatibility. |
| APIs | Use conditional updates, operation IDs, async status endpoints, stable pagination, quotas and bounded fan-out when appropriate. Scope authorization and cache keys correctly. | Concurrent updates, timeout ambiguity, repeated requests, pagination changes and overload. |
| Jobs / scheduling | Persist checkpoints; define overlap and misfire policy; use ownership leases and idempotent effects. Do not assume one scheduler instance. | Multi-replica execution, lease loss, worker crash, missed schedules and restart. |
| Files / object storage | Stage uploads, verify checksums and completion, finalize metadata using explicit states, reconcile orphaned objects and missing references. Enforce tenant-level access and safe cleanup. | Crash between storage and DB writes, interrupted upload, concurrent overwrite and unauthorized access. |
| Database replication / partition | Route correctness-critical reads appropriately; use supported quorum/failover and fencing mechanisms; bound connection use. | Read-after-write under lag, failover, stale primary and connection exhaustion. |

## Pattern selection principles

- Prefer a single local transaction where it can enforce the required invariant; introduce distributed coordination only when necessary.
- An outbox provides durable publication intent, not automatic exactly-once delivery or instantaneous consistency.
- A cache invalidation strategy must explicitly address concurrent stale fills and failed invalidations; adding Redis alone does not solve either.
- A retry policy must consider side effects and total end-to-end time, not just attempt count.
- Avoid blanket application of CQRS, event sourcing, distributed locks or microservices. Justify complexity using actual requirements.
- Keep migrations compatible with old and new application versions during rolling deployments; use expand/contract where applicable. Do not promise rollback of irreversible business effects; use forward repair or compensation as appropriate.

## Additional correctness rules

- Monetary amounts need explicit currency, rounding and overflow rules; balance each currency independently. Reversal entries retain original references.
- Choose operation IDs stable across retries; do not derive them solely from payload when two legitimate operations can have identical inputs. Deterministic entity IDs are appropriate only when business identity is genuinely deterministic; freeze namespaces and test across clients.
- Idempotency retention must cover the actual retry/replay horizon, or a durable business constraint must prevent later duplicates. Treat in-progress and unknown external outcomes explicitly.
- For multi-writer systems, define conflict semantics per invariant; last-writer-wins can discard valid changes and cannot safely enforce financial limits. Do not infer global ordering from timestamps.
- Validate external contract fields used by the application, verify callback authenticity, and retain only necessary redacted audit evidence. Reconcile discrepancies using stable external references and conditional, auditable corrections.
- Cancellation or timeout is not proof that external work stopped. Resume from durable state and distinguish compensation from rollback.
