# MongoDB

Related baseline problems: SDP-004, SDP-023, SDP-030, SDP-036, SDP-105.

## Detection
Inspect read-modify-write across documents, unique indexes, sessions, write concern and retryable transaction callbacks.

## Implementation
Prefer atomic single-document conditional updates where the invariant fits. Use unique indexes and supported multi-document transactions when necessary; persist outbox data within the transaction. Verify shard-key constraints on uniqueness.

## Pitfalls / counterexamples
Transaction callbacks may be retried; never place an external effect inside them. Majority acknowledgment and read concern do not automatically provide every desired cross-client consistency guarantee.

## Verification
Use a disposable replica set with independent clients; inject transaction abort and ambiguous commit; check durable state and dedupe.

## Upstream reference
[Official documentation](https://www.mongodb.com/docs/manual/core/transactions/). Confirm installed versions and provider capabilities before selecting APIs. This is guidance, not a tested integration.
