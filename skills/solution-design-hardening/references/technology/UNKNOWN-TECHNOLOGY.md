# Unknown or proprietary technology

Missing profiles are normal, not a reason to skip a problem. Establish the invariant and needed guarantees independently of the product. Identify its actual role using call sites, contracts, configuration and deployment evidence. Use generic capability guidance or derive a capability checklist if no domain fits.

Consult installed interfaces, versioned official docs, or user-provided sanitized evidence; verify semantics with isolated tests when authorized. Compare required atomicity, consistency, ordering, durability, failure and recovery behavior to what is established. If guarantees are absent, use an existing authoritative primitive, redesign the boundary, or propose a justified dependency only after evaluating alternatives. If semantics cannot be established, report the specific gap and block only the affected unsafe implementation, not the entire assessment.

Example: a custom queue exposes `send()` and `complete()`. Names do not establish durability, redelivery or acknowledgment semantics. Trace commit/complete ordering; request delivery and retention contract; test crash after commit before completion. Until verified, mark the queue-dependent guarantee Requires Verification. Do not substitute RabbitMQ assumptions or recommend a migration just because its profile exists.
