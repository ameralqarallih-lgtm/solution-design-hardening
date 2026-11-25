# ASP.NET Core / EF Core / resilience

Related baseline problems: SDP-001, SDP-004, SDP-023, SDP-035, SDP-039, SDP-141.

## Detection
Inspect SaveChanges boundaries, execution strategies, concurrency tokens, scoped DbContext lifetimes, hosted service cancellation and stacked HTTP resilience handlers.

## Implementation
Use a unique scoped operation key and business write in one local transaction; configure a concurrency token and handle DbUpdateConcurrencyException by re-reading and re-evaluating the invariant. Execute explicit transactions inside the configured execution strategy when needed; never repeat external effects inside a database retry delegate. Bound HttpClient deadlines and retries; use async I/O and pass cancellation tokens.

## Pitfalls / counterexamples
A unique index violation is provider-specific, not necessarily DbUpdateConcurrencyException. An in-memory lock or scoped service does not coordinate replicas. A successful SaveChanges does not guarantee external publication.

## Verification
Run two independent DbContexts against the actual database; inject a crash after commit, verify outbox recovery and use a fake provider with a stable idempotency key.

## Upstream reference
[Official documentation](https://learn.microsoft.com/en-us/ef/core/saving/concurrency). Confirm installed versions and provider capabilities before selecting APIs. This is guidance, not a tested integration.
