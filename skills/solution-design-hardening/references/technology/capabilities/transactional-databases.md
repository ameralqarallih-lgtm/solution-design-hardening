# Transactional data stores capability profile

Related catalog ranges (starting points, not exhaustive): SDP-023–037, 001–010.

## Discover and verify
Identify isolation, transaction scope, uniqueness enforcement, conditional writes, retry behavior and replication routing.
Record exact version/edition, client version, deployment topology, configured values and evidence. Separate documented support from effective configuration and observed behavior. Mark unknowns Requires Verification.

## Implementation decisions
Enforce invariants in one authoritative commit where possible; handle serialization failures by retrying the entire safe transaction.
Prefer the existing primitive if it meets the invariant; otherwise record alternatives, compatibility, failure boundaries and residual risk.

## Counterexamples and limits
A transaction API does not establish isolation across independent stores; snapshot isolation may permit write skew.
Do not assume capabilities solely from product category or a bundled profile.

## Verification
Race two writers at a barrier; crash before and after commit; assert invariant and read freshness.
Use isolated environments and record commands, versions, expected and actual outcomes. If unavailable, define the test without claiming it passed.
