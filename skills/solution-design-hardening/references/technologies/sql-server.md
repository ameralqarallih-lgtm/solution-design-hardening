# SQL Server

Related baseline problems: SDP-002, SDP-003, SDP-004, SDP-025, SDP-028, SDP-029, SDP-139.

## Detection
Inspect check-then-update SQL, NOLOCK on authoritative reads, rowversion predicates, transaction duration, indexes and deadlock handling.

## Implementation
Use UPDATE ... WHERE balance >= @amount and inspect affected rows; put balanced ledger entries and dedupe records in one transaction. Use rowversion for optimistic checks and serializable or deliberate locking for cross-row invariants; retry deadlock victims only at safe boundaries.

## Pitfalls / counterexamples
READ COMMITTED SNAPSHOT is statement-level snapshot; SNAPSHOT can allow write skew. NOLOCK is not a safe solution for correctness-critical reads. rowversion is not a timestamp.

## Verification
Use two SQL connections with controlled barriers; check affected rows, deadlock recovery and invariant preservation; measure migration locks on representative data.

## Upstream reference
[Official documentation](https://learn.microsoft.com/en-us/sql/relational-databases/sql-server-transaction-locking-and-row-versioning-guide). Confirm installed versions and provider capabilities before selecting APIs. This is guidance, not a tested integration.
