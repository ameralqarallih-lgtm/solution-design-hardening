# Language runtimes and concurrency capability profile

Related catalog ranges (starting points, not exhaustive): SDP-038–053, 141–145.

## Discover and verify
Identify process/thread/event-loop model, cancellation, memory ownership, synchronization and resource disposal.
Record exact version/edition, client version, deployment topology, configured values and evidence. Separate documented support from effective configuration and observed behavior. Mark unknowns Requires Verification.

## Implementation decisions
Bound concurrency and queues; propagate deadlines; release resources on failure; keep cross-process invariants at shared authority.
Prefer the existing primitive if it meets the invariant; otherwise record alternatives, compatibility, failure boundaries and residual risk.

## Counterexamples and limits
Async does not imply parallel or nonblocking; local mutexes do not protect other replicas.
Do not assume capabilities solely from product category or a bundled profile.

## Verification
Saturate worker pool; cancel in-flight tasks; measure queue size, handles and recovery.
Use isolated environments and record commands, versions, expected and actual outcomes. If unavailable, define the test without claiming it passed.
