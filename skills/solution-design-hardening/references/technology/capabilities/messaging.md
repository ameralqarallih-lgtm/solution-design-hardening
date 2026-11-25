# Queues and pub/sub capability profile

Related catalog ranges (starting points, not exhaustive): SDP-023–024, 054–068, 113–115.

## Discover and verify
Verify durable publication, routing, acknowledgment scope, redelivery, visibility/lease timeout, retention and dead-letter policy.
Record exact version/edition, client version, deployment topology, configured values and evidence. Separate documented support from effective configuration and observed behavior. Mark unknowns Requires Verification.

## Implementation decisions
Persist intent atomically, deduplicate effects, acknowledge after durable commit; bound retries and redrive.
Prefer the existing primitive if it meets the invariant; otherwise record alternatives, compatibility, failure boundaries and residual risk.

## Counterexamples and limits
Publisher confirmation does not prove consumer completion; broker deduplication may expire.
Do not assume capabilities solely from product category or a bundled profile.

## Verification
Crash after publish and after consumer commit before ack; replay; check one business effect and no lost intent.
Use isolated environments and record commands, versions, expected and actual outcomes. If unavailable, define the test without claiming it passed.
