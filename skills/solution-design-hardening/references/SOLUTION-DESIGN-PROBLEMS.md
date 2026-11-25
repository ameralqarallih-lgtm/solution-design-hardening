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

## Security extension 1. Authentication and identity

| ID | Design problem | Recommended solution / pattern |
|---|---|---|
| SDP-161 | **Authentication bypass** – An unauthenticated caller reaches protected operations. | Require validated identity at every protected entry point; explicitly inventory public routes. |
| SDP-162 | **Session fixation** – A pre-authentication session remains usable as the authenticated session. | Rotate session identifiers on authentication and privilege changes; invalidate previous identifiers server-side. |
| SDP-163 | **Session theft and unsafe cookies** – Session credentials are exposed or reused outside intended context. | Use Secure, HttpOnly and context-appropriate SameSite cookies; limit lifetime, revoke sessions and prevent credential leakage. |
| SDP-164 | **Credential stuffing and brute force** – Repeated authentication attempts compromise accounts or deny service to victims. | Use risk-based per-account and per-source controls, MFA and recovery; avoid permanent attacker-triggered lockouts. |
| SDP-165 | **Token validation failure** – Untrusted or wrong-context tokens authenticate callers. | Use maintained protocol library; validate signature, allowed algorithms, issuer, audience, expiry and intended token type; reject untrusted keys. |
| SDP-166 | **Token revocation gap** – A revoked session or credential remains valid beyond policy. | Define revocation latency, short lifetimes and appropriate introspection or revocation state; avoid assuming self-contained tokens revoke instantly. |
| SDP-167 | **OAuth and OIDC binding failure** – A callback, authorization code or identity assertion is accepted for the wrong client or session. | Use authorization code flow with PKCE where applicable, exact redirect allowlist, session-bound state and OIDC nonce validation; use standard library. |
| SDP-168 | **Account enumeration** – Authentication or recovery reveals whether an account exists. | Use consistent outward responses, bounded attempts and asynchronous recovery where appropriate; avoid leaking account status. |
| SDP-169 | **Unsafe account recovery** – Recovery credentials allow unauthorized resets or repeat use. | Use high-entropy purpose-bound single-use tokens stored safely, atomic redemption, short expiry and post-reset session policy. |
| SDP-170 | **Workload identity impersonation** – A service accepts a spoofed workload identity or credentials from the wrong environment. | Use authenticated workload identities, short-lived credentials and explicit audience/environment trust; authorize each operation. |

## Security extension 2. Authorization and business-flow security

| ID | Design problem | Recommended solution / pattern |
|---|---|---|
| SDP-171 | **Object-level authorization failure** – A valid caller accesses another principal's resource by identifier. | Enforce ownership or explicit grants at the protected data operation; derive tenant from trusted context. |
| SDP-172 | **Function-level authorization failure** – A caller reaches privileged functions without required rights. | Deny by default; enforce permissions server-side at each privileged function and validate delegated authority. |
| SDP-173 | **Unsafe property binding** – Client-controlled fields alter protected attributes such as roles or owner IDs. | Allowlist writable properties by operation and policy; map explicit request types and derive server-owned fields. |
| SDP-174 | **Unauthorized property disclosure** – An authorized object response exposes fields the caller cannot see. | Apply field-level read authorization and explicit projections; omit sensitive fields before serialization. |
| SDP-175 | **Fail-open authorization** – Policy errors or unavailable identity services permit access. | Fail closed on protected operations when authority is uncertain; define separate public or degraded behavior. |
| SDP-176 | **Privilege administration abuse** – Permission changes allow unauthorized escalation or bypass separation of duties. | Authorize grant creation and scope; enforce privilege ceilings and approval for high-impact grants; audit changes. |
| SDP-177 | **Sensitive business-flow abuse** – Valid automated actions exhaust limited business resources or circumvent policy. | Enforce business-specific quotas, state constraints and risk controls at authoritative boundary; avoid only IP limits. |
| SDP-178 | **Unsafe cross-origin trust** – Browser credentials or protected responses are exposed to untrusted origins. | Allow only required origins, methods and headers; use explicit credential policy and keep server-side authorization. |

## Security extension 3. Injection and untrusted content

| ID | Design problem | Recommended solution / pattern |
|---|---|---|
| SDP-179 | **SQL injection** – Untrusted values alter database query semantics. | Bind parameters for values and allowlist identifiers; avoid constructing SQL from untrusted strings. |
| SDP-180 | **NoSQL query injection** – Untrusted structures become database operators or filters. | Validate typed inputs, construct filters server-side and allowlist permitted operators. |
| SDP-181 | **Command injection** – Untrusted values alter operating-system command execution. | Avoid shell execution; use constrained direct APIs and validated arguments, with least privilege. |
| SDP-182 | **Cross-site scripting** – Untrusted content is interpreted as active browser code. | Use context-aware output encoding and vetted sanitization for intended HTML; CSP is defense in depth. |
| SDP-183 | **Server-side request forgery** – Untrusted destinations cause server requests across restricted network boundaries. | Use approved destinations or isolated fetch service, enforce address policy after resolution and redirects, bound response size/time. |
| SDP-184 | **Cross-site request forgery** – A browser sends an authenticated state change without user intent. | Use anti-forgery controls appropriate to credential mode, origin validation and safe HTTP semantics; do not rely solely on CORS. |
| SDP-185 | **Unsafe XML processing** – XML parsing resolves external resources or expands input unexpectedly. | Disable unneeded external entities and DTDs; use safe parser configuration and resource limits. |
| SDP-186 | **Unsafe deserialization** – Untrusted serialized data constructs unexpected objects or executes behavior. | Use data-only serialization and explicit schema/type allowlists; verify integrity when appropriate. |
| SDP-187 | **Path traversal and archive extraction** – Untrusted paths escape authorized directories or overwrite unrelated files. | Use trusted roots, safe path resolution and symlink-aware filesystem primitives; reject unsafe archive entries. |
| SDP-188 | **Template injection** – Untrusted content is interpreted as template source. | Use trusted templates with data-only bindings; sandbox only as additional control. |
| SDP-189 | **Unsafe redirect** – Untrusted destination redirects users outside intended trust boundary. | Use local paths or explicit trusted destinations; normalize and validate before redirecting. |
| SDP-190 | **HTTP parser disagreement** – Intermediaries disagree on request boundaries or normalization. | Reject ambiguous framing at ingress, align parser behavior and patch intermediaries. |
| SDP-191 | **Unsafe file upload** – Untrusted files become executable, public or resource-exhausting content. | Allowlist business-required types, verify content, enforce limits, store outside executable paths and quarantine when needed. |
| SDP-192 | **Unsafe upstream API consumption** – Third-party responses bypass validation or inject unsafe data into local actions. | Validate external data against explicit contracts, bound resources and enforce local authorization before effects. |

## Security extension 4. Data protection and cryptography

| ID | Design problem | Recommended solution / pattern |
|---|---|---|
| SDP-193 | **Hardcoded secrets** – Reusable credentials are embedded in code, images or defaults. | Use secret manager or injected scoped credentials; revoke exposed secrets and remove insecure defaults. |
| SDP-194 | **Secret exposure in artifacts and history** – Credentials persist in repository history, package or build output. | Revoke and rotate first; remove exposure from artifacts/history with coordinated owner approval; prevent recurrence. |
| SDP-195 | **Unprotected sensitive storage** – Sensitive data or snapshots are readable outside intended access boundary. | Apply appropriate encryption and restricted access, separate key authority and minimize retained data. |
| SDP-196 | **Cleartext sensitive transport** – Sensitive data or credentials traverse untrusted links without protection. | Use authenticated encryption in transit for relevant trust boundaries; enforce transport policy and secure downgrade handling. |
| SDP-197 | **Disabled TLS certificate validation** – A client trusts an unauthenticated endpoint. | Validate certificate chain and hostname with approved trust anchors; provision internal CA rather than disabling checks. |
| SDP-198 | **Weak password storage** – Password records can be recovered cheaply after a breach. | Use maintained password hashing with suitable cost and unique salts; migrate legacy hashes safely. |
| SDP-199 | **Unsafe cryptographic primitive or mode** – Encryption or signatures do not provide the required security property. | Use approved authenticated encryption/signature protocols and reviewed libraries; avoid custom cryptography. |
| SDP-200 | **Cryptographic nonce reuse** – A key is used with repeated nonces where uniqueness is required. | Use library-supported nonce policy appropriate to algorithm; ensure uniqueness per key across replicas and recovery. |
| SDP-201 | **Predictable security tokens** – Security-sensitive identifiers derive from predictable randomness. | Use cryptographically secure randomness of appropriate entropy; do not use timestamps or ordinary PRNG for secrets. |
| SDP-202 | **Key lifecycle and rotation failure** – Expired or compromised keys remain trusted, or rotation breaks availability. | Use versioned keys, bounded overlap, rotation and revocation procedures; protect historical decrypt needs separately. |
| SDP-203 | **Sensitive data lifecycle mismatch** – Data survives beyond deletion or retention policy in copies or derived stores. | Minimize copies, enforce retention and deletion propagation subject to documented legal holds and restore controls. |

## Security extension 5. Distributed and infrastructure security

| ID | Design problem | Recommended solution / pattern |
|---|---|---|
| SDP-204 | **Unauthenticated internal service** – An internal endpoint trusts network location instead of identity. | Authenticate and authorize service calls at the protected boundary; use network controls as defense in depth. |
| SDP-205 | **Unrestricted network reachability** – A compromised workload can reach unrelated sensitive services. | Allow required flows explicitly, separate trust zones and verify policy enforcement by runtime/network provider. |
| SDP-206 | **Unauthorized message operations** – A client can publish, consume or administer unrelated queues or topics. | Separate producer/consumer identities and scope permissions to required destinations and operations. |
| SDP-207 | **Message integrity and trust failure** – A service accepts unauthenticated or altered messages as authoritative. | Authenticate transport and publisher where required; validate envelope, schema and authorization; sign payloads when end-to-end integrity needed. |
| SDP-208 | **Excessive workload privileges** – Runtime permissions exceed application needs, enabling unintended access. | Use least privilege, non-root where feasible, minimal capabilities and restricted mounts; document justified exceptions. |
| SDP-209 | **Exposed management surface** – Administrative or debug endpoints are reachable by unintended clients. | Restrict network and identity access, disable unnecessary endpoints, separate administration plane. |
| SDP-210 | **Insecure deployment defaults** – Unsafe defaults remain enabled in deployed environments. | Define secure baseline, validate on startup or admission and prevent unsafe production defaults. |
| SDP-211 | **Cross-environment credential reuse** – Development or staging credentials grant production access. | Separate accounts, trust roots and credential scopes by environment; restrict promotion workflows. |
| SDP-212 | **Stale API inventory** – Deprecated or shadow endpoints escape security policy and patching. | Maintain versioned inventory and retirement controls; apply security policy consistently to all reachable versions. |

## Security extension 6. Software supply chain

| ID | Design problem | Recommended solution / pattern |
|---|---|---|
| SDP-213 | **Vulnerable dependency exposure** – A known vulnerable dependency is reachable in application or deployment. | Use authorized SCA, update or mitigate affected versions, document exceptions and retest compatibility. |
| SDP-214 | **Dependency confusion** – A resolver retrieves an unintended package from an untrusted namespace or registry. | Pin trusted registries and namespaces; lock dependency resolution and verify package integrity. |
| SDP-215 | **Artifact integrity failure** – Deployment accepts modified or unverified binaries/images. | Verify signatures or attestations against trusted identities, pin immutable digests and enforce policy at promotion. |
| SDP-216 | **Untrusted CI execution** – Untrusted contributions can execute with privileged pipeline context. | Separate untrusted builds from privileged release jobs, use minimal token permissions and approved promotion. |
| SDP-217 | **Pipeline credential leakage** – Build credentials are exposed in logs, caches, artifacts or long-lived tokens. | Prefer short-lived workload identity, isolated credentials, redaction and restricted artifact access. |
| SDP-218 | **Missing build provenance** – An artifact cannot be traced to approved source and build process. | Generate and verify provenance and dependency inventory at controlled build/promotion; keep trust policy independent. |
| SDP-219 | **Unsupported component lifecycle** – Runtime or dependency no longer receives required security fixes. | Maintain lifecycle inventory, upgrade path and time-bounded risk acceptance for unsupported components. |

## Security extension 7. Security monitoring and operations

| ID | Design problem | Recommended solution / pattern |
|---|---|---|
| SDP-220 | **Missing security audit coverage** – Security-relevant actions cannot be attributed or investigated. | Record actor, action, target, outcome and correlation with minimal sensitive data; durable audit intent where required. |
| SDP-221 | **Audit trail tampering** – Unauthorized actors can alter or remove security evidence. | Separate audit authority, restrict deletion, use append-only or tamper-evident controls appropriate to risk. |
| SDP-222 | **Security alerting gap** – Abuse or control failure does not trigger actionable notification. | Define monitored security signals, thresholds, escalation and test alert delivery; avoid noisy alerts without ownership. |
| SDP-223 | **Error information disclosure** – Failures reveal internal implementation or sensitive values to callers. | Return sanitized error contracts, maintain restricted diagnostics and correlation; never expose secret or stack details publicly. |
| SDP-224 | **Security configuration drift** – Effective controls diverge from approved baseline unnoticed. | Continuously validate effective controls, review changes and alert on unauthorized deviations. |
| SDP-225 | **Emergency credential response gap** – Compromised credentials cannot be revoked or isolated within required time. | Define emergency rotation/revocation and containment with tested dependencies and communication; preserve service recovery. |

## Security extension 8. AI and agentic application security

| ID | Design problem | Recommended solution / pattern |
|---|---|---|
| SDP-226 | **Prompt injection trust-boundary failure** – Untrusted user or retrieved content influences privileged agent behavior. | Treat content as data; enforce independent tool authorization, constrained actions and output validation outside model; no prompt-only guarantee. |
| SDP-227 | **Excessive agent authority** – Agent credentials or tools exceed the requested task scope. | Use scoped tools, least privilege, explicit authorization and confirmation for high-impact actions; enforce in host. |
| SDP-228 | **RAG authorization bypass** – Retrieval returns documents the caller cannot access. | Enforce document-level authorization at retrieval and revalidate access where needed; scope indexes/caches by policy. |
| SDP-229 | **Agent memory isolation failure** – Persistent memory leaks data or instructions across tenant or task boundaries. | Scope memory to authorized identity/tenant and purpose, validate provenance and support deletion; avoid treating memory as trusted authority. |
| SDP-230 | **Knowledge and model input poisoning** – Untrusted ingestion corrupts knowledge or model inputs used for decisions. | Validate source and content, track provenance, quarantine untrusted updates and provide version rollback. |
| SDP-231 | **Unsafe model output execution** – Generated text becomes executable commands, code or privileged data without validation. | Treat outputs as untrusted data, schema-validate, use constrained APIs and sandbox approved execution; require authority separately. |
| SDP-232 | **Unbounded agent execution and cost** – Agent loops or tool fan-out exhaust budgets or trigger repeated effects. | Enforce host-level budgets, cancellation, concurrency limits and idempotent effects; stop safely and report incomplete work. |
| SDP-233 | **Untrusted tool or MCP integration** – A tool definition or result expands authority or sends data to unintended party. | Allowlist trusted servers/tools, verify identity and contracts, constrain egress and permissions; treat descriptions/results as untrusted. |
| SDP-234 | **AI sensitive output disclosure** – Model responses reveal sensitive information from context, tools or memory. | Minimize sensitive inputs, enforce retrieval permissions, validate output and apply provider/data retention policy; never rely only on filtering. |
| SDP-235 | **Agent-to-agent trust failure** – Peer messages are accepted as authoritative instructions without verified identity or delegation. | Authenticate peers, validate delegated scope and message schema, and independently authorize requested effects. |
