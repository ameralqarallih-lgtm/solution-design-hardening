# Problem index (Level 2)

Route from observed signals to problem IDs, then load only the matching domain index and problem files. Each problem file (`problems/SDP-NNN.md`, Level 3) holds Failure, Detection, Remediation and safeguards, Verification and Related IDs; its domain index holds the shared decision rule.

## Problem-specific playbooks (load selectively)

Use the catalog to select applicable IDs, then read the corresponding playbook before confirming a finding or designing a fix. For full assessments process the ranges in batches; record covered paths and unresolved evidence, not just checked boxes. For focused work load only relevant ranges. The catalog is a baseline, not an exhaustive safety guarantee. Follow [context strategy](CONTEXT-STRATEGY.md) to select and expand relevant references, checkpoint full assessments, and avoid repeated loading without losing evidence or security coverage.

Here, "playbook" means the domain index plus the selected problem files. Then check the **Related** IDs and the families below before excluding adjacent risks.

## Domains

- SDP-001–010: [Financial](problems-financial.md) - charges, balances, ledgers, reservations
- SDP-011–022: [Caching](problems-caching.md) - cache fill, invalidation, TTL, fallback load, keys
- SDP-023–037: [Database](problems-database.md) - commit then publish, isolation, replicas, locks, pools
- SDP-038–053: [Resilience](problems-resilience.md) - retries, deadlines, queues, leases, replicas, partitions
- SDP-054–068: [Messaging](problems-messaging.md) - acknowledgment, event identity, ordering, replay, redelivery
- SDP-069–080: [API](problems-api.md) - POST retries, conditional updates, fan-out, pagination
- SDP-081–091: [Workflow](problems-workflow.md) - schedulers, job claims, progress, side effects before checkpoint
- SDP-092–100: [Storage](problems-storage.md) - object plus metadata writes, cleanup, signed URLs
- SDP-101–104: [Financial Extensions](problems-financial-extensions.md) - rounding, currency, idempotency retention and claims
- SDP-105–111: [Data Migration](problems-data-migration.md) - conflict resolution, tombstones, DDL, backfill, restore, CDC
- SDP-112–124: [Integration Operations](problems-integration-operations.md) - callbacks, dedupe state, relay, redrive, shutdown, tenancy, repair
- SDP-125–130: [Multi Region](problems-multi-region.md) - failover, failback, quorum, leadership, leases
- SDP-131–136: [Security](problems-security.md) - authorization timing and caching, token refresh, deputies, telemetry, input size
- SDP-137–145: [Deployment Resources](problems-deployment-resources.md) - config drift, rollback, migrations, threads, handles, memory, scaling
- SDP-146–150: [Observability Tenancy](problems-observability-tenancy.md) - metric labels, telemetry export, tracing, tenant context
- SDP-151–160: [Lifecycle](problems-lifecycle.md) - outbox payloads, sequence gaps, key scope, schedules, deletion, audit, quotas, retention
- SDP-161–170: [Authentication and identity](problems-security-identity.md) - sessions, cookies, tokens, OAuth/OIDC, recovery, workload identity
- SDP-171–178: [Authorization and business-flow security](problems-security-access.md) - object, function and property access, fail-open, grants, CORS
- SDP-179–192: [Injection and untrusted content](problems-security-input.md) - SQL, NoSQL, shell, HTML, SSRF, CSRF, XML, deserialization, paths, uploads
- SDP-193–203: [Data protection and cryptography](problems-security-data.md) - secrets, storage, transport, TLS, hashing, crypto, keys, retention
- SDP-204–212: [Distributed and infrastructure security](problems-security-infra.md) - internal auth, network reach, brokers, privileges, management surfaces
- SDP-213–219: [Software supply chain](problems-security-supply.md) - dependencies, registries, artifacts, CI, provenance, lifecycle
- SDP-220–225: [Security monitoring and operations](problems-security-operations.md) - audit, alerting, error disclosure, drift, emergency revocation
- SDP-226–235: [AI and agentic application security](problems-security-ai.md) - prompt injection, agent authority, RAG, memory, tools/MCP, cost

## Cross-domain families

A finding in one member often shares a root cause with the others. Check the relevant members before excluding them; shared membership alone does not establish causation.

| Family | Problems |
|---|---|
| Commit and publish boundary (dual write) | SDP-012, SDP-023, SDP-054, SDP-063, SDP-094, SDP-114, SDP-151, SDP-157 |
| Duplicate effects and idempotency | SDP-001, SDP-024, SDP-055, SDP-058, SDP-069, SDP-081, SDP-091, SDP-103, SDP-104, SDP-113, SDP-153 |
| Ambiguous outcome after timeout or cancellation | SDP-006, SDP-070, SDP-116 |
| Concurrent updates to shared state | SDP-003, SDP-004, SDP-009, SDP-028, SDP-030, SDP-072, SDP-095 |
| Stale reads and freshness | SDP-011, SDP-019, SDP-031, SDP-061, SDP-126, SDP-132 |
| Retries, herds and overload | SDP-013, SDP-038, SDP-039, SDP-041, SDP-052, SDP-053, SDP-087, SDP-118, SDP-154 |
| Locks, leases and fencing | SDP-032, SDP-046, SDP-047, SDP-082, SDP-129, SDP-130 |
| Authorization at the point of effect | SDP-099, SDP-131, SDP-132, SDP-134, SDP-171, SDP-172, SDP-175, SDP-228 |
| Tenant isolation | SDP-120, SDP-149, SDP-150, SDP-229 |
| Mixed versions and migrations | SDP-060, SDP-108, SDP-109, SDP-138, SDP-139, SDP-140 |
| Replay and recovery | SDP-058, SDP-110, SDP-111, SDP-115 |
