# PostgreSQL

Related baseline problems: SDP-003, SDP-004, SDP-028, SDP-029, SDP-103, SDP-140, SDP-160.

## Detection
Inspect ON CONFLICT targets, SELECT FOR UPDATE, isolation, long transactions and migrations.

## Implementation
Use scoped unique constraints and INSERT ... ON CONFLICT for atomic claims; compare payload fingerprint after a conflict. Use conditional updates or serializable transactions with bounded whole-transaction retry for SQLSTATE 40001; handle deadlocks separately.

## Pitfalls / counterexamples
Repeatable Read uses snapshot isolation and does not eliminate all serialization anomalies. Advisory locks require matching scope and connection lifecycle. CREATE INDEX CONCURRENTLY has special transaction restrictions.

## Verification
Run two real connections to reproduce write skew and serialization failures; check safe retry and lock/transaction age monitoring.

## Upstream reference
[Official documentation](https://www.postgresql.org/docs/current/transaction-iso.html). Confirm installed versions and provider capabilities before selecting APIs. This is guidance, not a tested integration.
