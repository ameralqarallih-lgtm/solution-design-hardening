# Solution Design Problems and Recommended Patterns

Problems that a Solution Architect should anticipate when designing transactional, distributed, highly available enterprise applications.

## 1. Financial and transactional consistency

| ID | Design problem | Recommended solution / pattern |
|---|---|---|
| SDP-001 | **Duplicate Charge** – A customer is charged multiple times due to retries or network failures. | Idempotency Key, Unique Transaction ID |
| SDP-002 | **Inconsistent Financial Balance** – Money is deducted from one account without being credited to another. | Double-Entry Ledger, Atomic Transactions |
| SDP-003 | **Double Spending** – The same available balance is spent through concurrent transactions. | Pessimistic Locking, Serializable Transactions, Atomic Conditional Updates |
| SDP-004 | **Lost Update** – Two transactions update the same record, overwriting each other's changes. | Optimistic Locking, Versioning |
| SDP-005 | **Partial Transaction Failure** – Some operations succeed while others fail. | Saga Pattern, Compensating Transactions |
| SDP-006 | **Uncertain Transaction Status** – A payment succeeds, but the client receives a timeout. | Transaction Status Inquiry, Idempotency, Reconciliation |
| SDP-007 | **Financial Record Manipulation** – Historical financial transactions are modified or deleted. | Append-Only Ledger, Immutable Audit Trail |
| SDP-008 | **Balance Calculation Drift** – Stored balances become inconsistent with transaction history. | Ledger Reconciliation, Balance Verification |
| SDP-009 | **Concurrent Resource Reservation** – Multiple users reserve the same seat, room or inventory item. | Atomic Reservation, Distributed or Database Locking |
| SDP-010 | **Abandoned Reservation** – Reserved resources are never released after an incomplete transaction. | Reservation TTL, Expiration Worker, Compensating Transaction |

## 2. Caching problems

| ID | Design problem | Recommended solution / pattern |
|---|---|---|
| SDP-011 | **Stale Data** – Cache contains an outdated version of database records. | Cache Invalidation, TTL, CDC |
| SDP-012 | **Dual Write Problem** – Database update succeeds, but cache update fails, or vice versa. | Database as Source of Truth, Transactional Outbox, CDC-Based Invalidation |
| SDP-013 | **Cache Stampede (Thundering Herd)** – Multiple requests simultaneously regenerate an expired cache entry. | Singleflight, Request Coalescing, Locking |
| SDP-014 | **Cache Avalanche** – Large numbers of cached records expire simultaneously. | Randomized TTL, Staggered Expiration |
| SDP-015 | **Cache Penetration** – Requests for nonexistent records repeatedly reach the database. | Negative Caching, Bloom Filter |
| SDP-016 | **Cache Breakdown** – A frequently accessed cache key expires, overwhelming the database. | Singleflight, Stale-While-Revalidate |
| SDP-017 | **Hot Key Problem** – One cache key receives disproportionately high traffic. | Local Caching, Read Replication, Key Replication |
| SDP-018 | **Cache Poisoning** – Incorrect or malicious data is stored in the cache. | Input Validation, Secure Cache Key Design |
| SDP-019 | **Cache Invalidation Race** – A concurrent request repopulates the cache with outdated data. | Versioned Cache Entries, Conditional Cache Writes |
| SDP-020 | **Cold Cache Problem** – Application startup generates excessive database requests. | Cache Warming, Progressive Traffic Introduction |
| SDP-021 | **Cache Dependency Failure** – Cache outage causes database overload. | Controlled Fallback, Rate Limiting, Circuit Breaker |
| SDP-022 | **Cache Memory Exhaustion** – Cached data consumes all available memory. | Eviction Policies (LRU/LFU), Memory Limits |

## 3. Database and data consistency problems

| ID | Design problem | Recommended solution / pattern |
|---|---|---|
| SDP-023 | **Dual Write (Database + Message Broker)** – Database commits successfully, but the corresponding event is not published. | Transactional Outbox Pattern |
| SDP-024 | **Duplicate Event Processing** – The same event is delivered and processed multiple times. | Transactional Inbox Pattern, Idempotent Consumer |
| SDP-025 | **Dirty Read** – A transaction reads another transaction's uncommitted data. | Read Committed Isolation |
| SDP-026 | **Non-Repeatable Read** – Reading the same record twice produces different values within one transaction. | Repeatable Read Isolation |
| SDP-027 | **Phantom Read** – New records appear between repeated queries within a transaction. | Serializable Isolation |
| SDP-028 | **Write Skew** – Concurrent transactions independently satisfy conditions but collectively violate a business rule. | Serializable Isolation, Explicit Locking |
| SDP-029 | **Database Deadlock** – Transactions wait on each other's locks until interrupted. | Consistent Lock Ordering, Short Transactions, Controlled Retry |
| SDP-030 | **Race Condition** – The result depends on the execution order of concurrent operations. | Atomic Operations, Optimistic/Pessimistic Locking |
| SDP-031 | **Replication Lag** – A read replica returns outdated data after a successful write. | Read-Your-Writes Consistency, Primary Routing |
| SDP-032 | **Split-Brain** – Multiple database nodes incorrectly believe they are the primary. | Consensus, Quorum, Fencing Tokens |
| SDP-033 | **Database Hotspot** – Excessive transactions target a specific record or partition. | Partitioning, Sharding, Distributed Counters |
| SDP-034 | **Cross-Database Transaction** – A business transaction spans multiple independent databases. | Saga, Try-Confirm-Cancel (TCC), or 2PC where appropriate |
| SDP-035 | **Database Connection Exhaustion** – Requests consume all available database connections. | Connection Pooling, Backpressure, Concurrency Limits |
| SDP-036 | **Inconsistent Distributed Data** – Independent services maintain conflicting versions of business data. | Data Ownership, Eventual Consistency, Reconciliation |
| SDP-037 | **Orphaned Records** – Related records remain after incomplete operations or deletions. | Referential Integrity, Compensating Transactions, Cleanup Jobs |

## 4. Distributed system and resilience problems

| ID | Design problem | Recommended solution / pattern |
|---|---|---|
| SDP-038 | **Retry Storm** – Multiple services continuously retry failed requests, overwhelming the system. | Exponential Backoff, Jitter, Retry Budget |
| SDP-039 | **Retry Amplification** – Each layer of a distributed system independently retries the same operation. | Centralized Retry Policy, Single-Layer Retry |
| SDP-040 | **Cascading Failure** – Failure of one service causes other dependent services to fail. | Circuit Breaker, Bulkhead |
| SDP-041 | **Thundering Herd** – Many clients simultaneously request the same resource. | Request Coalescing, Jitter, Rate Limiting |
| SDP-042 | **Slow Dependency** – A slow downstream service consumes upstream resources. | Timeout, Deadline Propagation |
| SDP-043 | **Resource Starvation** – One workload consumes resources needed by other workloads. | Bulkhead, Resource Quotas |
| SDP-044 | **Backpressure Problem** – Producers generate requests faster than consumers can process them. | Bounded Queues, Flow Control |
| SDP-045 | **Head-of-Line Blocking** – A slow request blocks subsequent requests. | Parallel Processing, Separate Queues |
| SDP-046 | **Distributed Lock Expiration** – A lock expires while its original owner is still performing an operation. | Fencing Tokens, Lease Management |
| SDP-047 | **Zombie Process** – A previously disconnected service resumes operating with outdated authority. | Fencing Tokens, Epoch-Based Coordination |
| SDP-048 | **Network Partition** – Distributed components cannot communicate with each other. | Quorum, Consensus Protocols, Explicit Consistency Policies |
| SDP-049 | **Clock Skew** – Different servers have inconsistent system clocks. | Clock Synchronization, Logical Clocks |
| SDP-050 | **Single Point of Failure** – Failure of a single component disables the entire system. | Redundancy, Automatic Failover |
| SDP-051 | **Noisy Neighbor** – One tenant negatively affects other tenants. | Tenant Isolation, Quotas, Fair Scheduling |
| SDP-052 | **Overload Collapse** – Increased workload reduces the system's overall processing capacity. | Load Shedding, Admission Control |
| SDP-053 | **Failover Storm** – Multiple workloads simultaneously fail over to secondary resources. | Staggered Failover, Capacity Planning |

## 5. Messaging and event-driven architecture problems

| ID | Design problem | Recommended solution / pattern |
|---|---|---|
| SDP-054 | **Message Loss** – A message disappears before successful processing. | Durable Queues, Publisher Confirms, Consumer Acknowledgments |
| SDP-055 | **Duplicate Message** – A message is delivered more than once. | Idempotent Consumer, Inbox Pattern |
| SDP-056 | **Out-of-Order Messages** – Events arrive in an incorrect sequence. | Partition Keys, Sequence Numbers, Version Checking |
| SDP-057 | **Poison Message** – A message repeatedly fails and blocks processing. | Dead Letter Queue, Maximum Retry Limit |
| SDP-058 | **Message Replay Side Effects** – Reprocessing historical messages triggers duplicate business operations. | Replay-Aware Consumers, Idempotency |
| SDP-059 | **Consumer Lag** – Consumers cannot process incoming messages fast enough. | Consumer Scaling, Partitioning, Backpressure |
| SDP-060 | **Message Schema Incompatibility** – New message formats break existing consumers. | Schema Registry, Backward Compatibility |
| SDP-061 | **Eventual Consistency Window** – Different services temporarily represent different business states. | Pending States, Reconciliation, Consistency Boundaries |
| SDP-062 | **Ghost Event** – An event is published for a database transaction that subsequently rolls back. | Transactional Outbox |
| SDP-063 | **Missing Event** – A database transaction succeeds without publishing its corresponding event. | Transactional Outbox, CDC |
| SDP-064 | **Event Processing Loop** – Services trigger each other's events indefinitely. | Causation ID, Loop Detection, Explicit Event Ownership |
| SDP-065 | **Premature Acknowledgment** – A consumer acknowledges a message before processing completes. | Acknowledge After Durable Commit |
| SDP-066 | **Event Notification Failure** – Subscribers miss notifications while offline. | Durable Subscriptions, Event Replay |
| SDP-067 | **Oversized Message** – Large message payloads overload the messaging infrastructure. | Claim Check Pattern |
| SDP-068 | **Event Choreography Complexity** – Business workflows become difficult to track across multiple events. | Saga Orchestration, Workflow Engine |

## 6. API and request processing problems

| ID | Design problem | Recommended solution / pattern |
|---|---|---|
| SDP-069 | **Duplicate API Submission** – Users submit the same request multiple times. | Idempotency Key |
| SDP-070 | **Timeout Ambiguity** – A client cannot determine whether a timed-out operation completed. | Operation ID, Status Endpoint |
| SDP-071 | **Long-Running Request** – Operations exceed HTTP or gateway timeout limits. | Asynchronous Request-Reply Pattern |
| SDP-072 | **Concurrent API Updates** – Multiple clients overwrite the same resource. | ETag, If-Match, Optimistic Concurrency |
| SDP-073 | **API Request Flooding** – Excessive requests overwhelm backend services. | Token Bucket, Sliding Window Rate Limiting |
| SDP-074 | **N+1 Request Problem** – Retrieving a collection generates an additional request for every item. | Batching, DataLoader, Bulk APIs |
| SDP-075 | **Overfetching** – APIs return unnecessary data. | Field Projection, GraphQL |
| SDP-076 | **Underfetching** – Clients require multiple API calls to retrieve related information. | API Composition, BFF |
| SDP-077 | **Pagination Drift** – Records are skipped or duplicated when data changes between page requests. | Cursor/Keyset Pagination, Snapshot Consistency |
| SDP-078 | **Request Replay Attack** – Previously valid requests are maliciously resubmitted. | Nonce, Timestamp, Signed Requests |
| SDP-079 | **Partial Bulk Operation Failure** – Some items succeed while others fail. | Item-Level Results, Idempotent Batch Processing |
| SDP-080 | **API Fan-Out Failure** – An aggregated response fails because one dependency is unavailable. | Partial Responses, Timeouts, Graceful Degradation |

## 7. Workflow and background processing problems

| ID | Design problem | Recommended solution / pattern |
|---|---|---|
| SDP-081 | **Duplicate Scheduled Job** – Multiple application instances execute the same scheduled job. | Distributed Scheduler, Leader Election, Idempotent Jobs |
| SDP-082 | **Overlapping Job Execution** – A scheduled job starts before its previous execution finishes. | Job Concurrency Policy, Distributed Lock |
| SDP-083 | **Stuck Workflow** – A workflow remains indefinitely in an intermediate state. | Workflow Timeout, Watchdog, Escalation |
| SDP-084 | **Lost Job Progress** – A worker crashes before completing a long-running operation. | Checkpointing, Durable Execution |
| SDP-085 | **Partial Workflow Completion** – Early workflow steps succeed while later steps fail. | Saga, Compensation |
| SDP-086 | **Orphaned Background Job** – A crashed worker leaves a job marked as running. | Worker Heartbeat, Lease Expiration |
| SDP-087 | **Infinite Retry Loop** – A permanently failing operation is continuously retried. | Maximum Attempts, Dead Letter Queue |
| SDP-088 | **Job Starvation** – Low-priority jobs are never executed. | Priority Aging, Fair Scheduling |
| SDP-089 | **Missed Scheduled Execution** – A scheduled task is skipped during an outage. | Persistent Scheduler, Misfire Policy |
| SDP-090 | **Invalid State Transition** – A business entity moves into an invalid status. | Finite State Machine, State Transition Validation |
| SDP-091 | **Duplicate External Side Effect** – A workflow repeats an email, payment or external submission after recovery. | Idempotent Activities, External Operation Reference |

## 8. Storage and file management problems

| ID | Design problem | Recommended solution / pattern |
|---|---|---|
| SDP-092 | **Orphaned File** – A file is uploaded successfully, but its database record fails to save. | Staging Storage, Cleanup Worker, Compensation |
| SDP-093 | **Missing File** – A database record references a file that was never uploaded. | Pending Upload State, Upload Verification |
| SDP-094 | **Dual Write (Database + Object Storage)** – Database metadata and file storage become inconsistent. | Staged Upload, Saga, Reconciliation |
| SDP-095 | **Concurrent File Modification** – Multiple users overwrite the same file. | Object Versioning, Conditional Writes |
| SDP-096 | **Incomplete File Upload** – Network interruption leaves a partially uploaded file. | Multipart Upload, Resumable Upload |
| SDP-097 | **File Corruption** – Stored content differs from the original file. | Checksums, Integrity Verification |
| SDP-098 | **Duplicate File Storage** – Identical files consume unnecessary storage. | Content-Based Hashing, Deduplication |
| SDP-099 | **Unauthorized File Access** – Users access files belonging to other users or tenants. | Object-Level Authorization, Short-Lived Signed URLs |
| SDP-100 | **Deleted File Recovery** – Accidental deletion permanently removes important documents. | Soft Delete, Object Versioning, Retention Policies |

## 9. Financial correctness extensions

| ID | Design problem | Recommended solution / pattern |
|---|---|---|
| SDP-101 | **Monetary rounding drift** – Binary floating point or inconsistent rounding changes financial totals. | Exact decimal or minor units; currency-specific rounding and allocation invariants |
| SDP-102 | **Currency mixing** – Ledger entries or balances mix incompatible currencies. | Currency-aware amounts; per-currency balancing; explicit FX legs |
| SDP-103 | **Idempotency retention gap** – A delayed retry arrives after its deduplication key expires. | Retention aligned to replay horizon; durable business uniqueness |
| SDP-104 | **Concurrent idempotency claim** – Two requests both see an unused key before processing. | Atomic unique claim; payload fingerprint; durable outcome state |

## 10. Distributed data and migration extensions

| ID | Design problem | Recommended solution / pattern |
|---|---|---|
| SDP-105 | **Multi-writer conflict** – Independent writers overwrite concurrent changes. | Single writer or explicit conflict resolution; versions; domain-safe merges |
| SDP-106 | **Tombstone resurrection** – Delayed replication or replay recreates a deleted entity. | Versioned tombstones; retention aligned to replay horizon |
| SDP-107 | **Projection rebuild inconsistency** – A rebuilt read model loses concurrent changes or exposes incomplete state. | Checkpointed rebuild; catch-up; atomic cutover |
| SDP-108 | **Mixed-version deployment** – Old and new instances cannot share schemas or contracts. | Expand-contract migration; compatibility tests; staged rollout |
| SDP-109 | **Backfill race** – A migration backfill overwrites newer live writes. | Conditional versioned updates; resumable batches; reconciliation |
| SDP-110 | **Restore inconsistency** – Restoring one store replays side effects or diverges from other stores. | Coordinated recovery points; replay controls; reconciliation |
| SDP-111 | **CDC retention gap** – A connector resumes after its source log position is no longer available. | Lag monitoring; retained offsets; controlled resnapshot and reconciliation |

## 11. Integration and operational extensions

| ID | Design problem | Recommended solution / pattern |
|---|---|---|
| SDP-112 | **Webhook authenticity failure** – Forged or replayed callbacks change business state. | Signature verification; replay window; durable deduplication |
| SDP-113 | **Unbounded deduplication state** – Inbox or idempotency records grow without a lifecycle. | Retention policy tied to replay guarantees; archival; business uniqueness |
| SDP-114 | **Outbox relay backlog** – Committed intents accumulate without timely publication. | Oldest-age alerts; bounded batches; retry and recovery runbook |
| SDP-115 | **Unsafe dead-letter replay** – Bulk redrive reintroduces poison messages or duplicate effects. | Quarantine; inspected replay; rate limits; idempotency |
| SDP-116 | **Cancellation ambiguity** – Client cancellation is treated as proof that a remote operation stopped. | Durable operation state; status inquiry; explicit cancellation semantics |
| SDP-117 | **Graceful shutdown failure** – Termination interrupts work before commit or acknowledgment. | Drain; bounded shutdown; durable checkpoints; redelivery safety |
| SDP-118 | **Readiness-induced overload** – Health or readiness transitions remove capacity and overload surviving replicas. | Separate probes; bounded checks; rollout capacity; hysteresis |
| SDP-119 | **Missing recovery signals** – Failures accumulate silently despite healthy process metrics. | Business invariant metrics; queue age; reconciliation and alerting |
| SDP-120 | **Cross-tenant state leakage** – Shared cache, dedupe or job keys collide across tenants. | Tenant-scoped keys and authorization; isolation tests |
| SDP-121 | **Unsafe reconciliation overwrite** – Repair jobs overwrite valid newer or in-flight state. | External IDs; age thresholds; conditional corrections; audit trail |
| SDP-122 | **Unbounded fan-out** – A request launches excessive parallel downstream work. | Concurrency limits; deadlines; bounded batches |
| SDP-123 | **Dependency contract drift** – External provider changes fields or semantics relied on by consumers. | Boundary validation; contract tests; quarantine; compatibility monitoring |
| SDP-124 | **Object cleanup race** – Cleanup deletes an object that is being finalized or reused. | Ownership state; grace periods; conditional deletion; recheck references |

## 12. Multi-region and coordination

| ID | Design problem | Recommended solution / pattern |
|---|---|---|
| SDP-125 | **Multi-region failover data loss** – Async replication loses acknowledged writes on promotion. | RPO-aware promotion, fencing, reconciliation |
| SDP-126 | **Stale regional writer routing** – Clients continue writing through old regional connections. | Authority epoch, fenced routing |
| SDP-127 | **Unsafe failback** – Returning region overwrites newer active-region state. | Resynchronization, checkpointed cutover |
| SDP-128 | **Quorum loss** – Minority continues unsafe authoritative writes. | Consensus, quorum enforcement |
| SDP-129 | **Leader flapping** – Repeated elections prevent progress. | Election tuning, control-plane isolation |
| SDP-130 | **Lease renewal starvation** – Renewal cannot execute under workload saturation. | Isolated renewal, fencing |

## 13. Security and authorization correctness

| ID | Design problem | Recommended solution / pattern |
|---|---|---|
| SDP-131 | **Authorization TOCTOU** – Permission changes between check and effect. | Atomic authorization guard, revalidation |
| SDP-132 | **Authorization cache staleness** – Revoked permission remains effective. | Policy versioning, bounded invalidation |
| SDP-133 | **Token refresh race** – Concurrent refresh invalidates or overwrites credentials. | Serialized refresh, versioned replacement |
| SDP-134 | **Confused deputy** – Privileged service acts beyond caller authority. | Delegation validation, scoped credentials |
| SDP-135 | **Sensitive telemetry leakage** – Logs or dead letters expose sensitive payloads. | Redaction, restricted retention |
| SDP-136 | **Input resource amplification** – Small or malformed input induces disproportionate resource use. | Decoded size and complexity limits |

## 14. Deployment and resource engineering

| ID | Design problem | Recommended solution / pattern |
|---|---|---|
| SDP-137 | **Configuration drift** – Replicas use incompatible safety settings. | Versioned config, startup validation |
| SDP-138 | **Incompatible rollback** – Old application cannot handle migrated data. | Expand-contract, forward recovery |
| SDP-139 | **Migration lock contention** – DDL blocks live workload. | Engine-specific online migration, lock budgets |
| SDP-140 | **Concurrent migration execution** – Multiple replicas apply schema changes concurrently. | Coordinated migration owner |
| SDP-141 | **Thread pool starvation** – Blocking work exhausts execution threads. | Async I/O, bounded blocking pools |
| SDP-142 | **Resource handle leak** – Failure paths retain connections or streams. | Structured disposal, lifecycle metrics |
| SDP-143 | **Unbounded memory growth** – Accumulated state or tasks exhaust memory. | Bounded retention, backpressure |
| SDP-144 | **Autoscaling feedback mismatch** – Scaling signal ignores actual bottleneck. | Workload metrics, downstream limits |
| SDP-145 | **Cancellation resource leak** – Canceled requests leave expensive work running. | Cooperative cancellation, bounded execution |

## 15. Observability and tenant lifecycle

| ID | Design problem | Recommended solution / pattern |
|---|---|---|
| SDP-146 | **Metrics cardinality explosion** – Unbounded labels overload monitoring. | Bounded dimensions |
| SDP-147 | **Telemetry backpressure** – Unavailable exporter blocks application. | Bounded asynchronous export |
| SDP-148 | **Broken trace propagation** – Async work loses causal context. | Trace context propagation |
| SDP-149 | **Tenant migration race** – Writes lost during tenant relocation. | Checkpointed copy, fenced cutover |
| SDP-150 | **Background tenant context loss** – Worker applies operation to wrong tenant. | Persisted scope, authorization |

## 16. Additional messaging and lifecycle correctness

| ID | Design problem | Recommended solution / pattern |
|---|---|---|
| SDP-151 | **Mutable outbox payload** – Relay emits state different from committed event. | Immutable payload or versioned snapshot |
| SDP-152 | **Event sequence gap** – Missing delta silently corrupts projection. | Gap detection, replay |
| SDP-153 | **Idempotency scope collision** – Unrelated operations share dedupe identity. | Scoped key and fingerprint |
| SDP-154 | **Reconnect storm** – Clients reconnect simultaneously after outage. | Jittered reconnect, admission |
| SDP-155 | **Schedule timezone ambiguity** – DST or timezone changes duplicate or skip work. | Explicit zone and occurrence policy |
| SDP-156 | **Incomplete deletion propagation** – Deleted data persists in uncontrolled copies. | Retention-aware deletion propagation |
| SDP-157 | **Audit dual write** – Business mutation commits without required audit evidence. | Atomic audit intent |
| SDP-158 | **Distributed provider quota breach** – Independent replicas exceed shared provider limits. | Shared quota admission |
| SDP-159 | **Claim-check retention mismatch** – Payload expires before supported replay. | Coordinated retention |
| SDP-160 | **Long snapshot retention pressure** – Long transactions prevent cleanup of old versions or logs. | Bounded transactions, retention monitoring |
