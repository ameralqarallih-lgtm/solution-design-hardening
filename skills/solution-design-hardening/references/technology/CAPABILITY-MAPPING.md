# Capability mapping

A technology can implement multiple domains, and a single invariant can require multiple domains. Map the actual operation, not just product names. For each required guarantee record: operation and scope, authoritative owner, failure model, requirement, observed implementation, documented support, effective configuration, runtime test and remaining gaps. Use the inventory template. Never infer guarantee from category membership.

Status: **Unknown** (no sufficient evidence), **Documented** (version-specific documentation only), **Configured** (code/configuration supports claim but runtime unverified), **Verified** (appropriate observed test or equivalent proof within explicit scope), **Unsupported** (evidence shows required guarantee unavailable). These are capability evidence states, not assessment completion statuses. Conflicting evidence remains Unknown pending resolution.

## Capability index
- [Transactional Databases](capabilities/transactional-databases.md) - transactional data stores
- [Distributed Databases](capabilities/distributed-databases.md) - replicated or partitioned data
- [Caching](capabilities/caching.md) - derived caches
- [Messaging](capabilities/messaging.md) - queues and pub/sub
- [Event Streaming](capabilities/event-streaming.md) - ordered event logs
- [Workflow Engines](capabilities/workflow-engines.md) - durable orchestration
- [Background Processing](capabilities/background-processing.md) - workers and schedulers
- [Object Storage](capabilities/object-storage.md) - binary object services
- [Application Runtimes](capabilities/application-runtimes.md) - language runtimes and concurrency
- [Data Access](capabilities/data-access.md) - ORMs and database clients
- [Distributed Coordination](capabilities/distributed-coordination.md) - leases and consensus services
- [Container Orchestration](capabilities/container-orchestration.md) - replicated workload platforms
- [Serverless](capabilities/serverless.md) - event-triggered managed execution
- [Identity And Security](capabilities/identity-and-security.md) - identity and authorization systems
- [Api Management](capabilities/api-management.md) - gateways and API clients
- [Search Engines](capabilities/search-engines.md) - derived search indexes
- [Observability](capabilities/observability.md) - telemetry and audit pipelines

If no profile fits, derive a new capability checklist from the invariant and use [unknown technology](UNKNOWN-TECHNOLOGY.md). Optional [product profiles](../technologies/README.md) are accelerators, not a support boundary.
