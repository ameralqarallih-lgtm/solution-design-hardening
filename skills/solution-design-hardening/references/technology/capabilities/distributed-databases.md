# Replicated or partitioned data capability profile

Related catalog ranges (starting points, not exhaustive): SDP-028–037, 105–111, 125–130.

## Discover and verify
Identify partition key, consistency level, replica acknowledgment, conflict resolution, transaction scope, failover authority.
Record exact version/edition, client version, deployment topology, configured values and evidence. Separate documented support from effective configuration and observed behavior. Mark unknowns Requires Verification.

## Implementation decisions
Choose consistency per invariant; use conditional writes or consensus-backed primitives with correct scope; reconcile divergent data.
Prefer the existing primitive if it meets the invariant; otherwise record alternatives, compatibility, failure boundaries and residual risk.

## Counterexamples and limits
Quorum settings alone do not establish linearizability; multi-key atomicity may be unavailable.
Do not assume capabilities solely from product category or a bundled profile.

## Verification
Partition replicas, exercise competing writes and failover in a disposable environment; measure lost acknowledged writes.
Use isolated environments and record commands, versions, expected and actual outcomes. If unavailable, define the test without claiming it passed.
