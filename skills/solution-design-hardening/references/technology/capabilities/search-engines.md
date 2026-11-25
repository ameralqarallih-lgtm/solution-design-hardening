# Derived search indexes capability profile

Related catalog ranges (starting points, not exhaustive): SDP-017, 030, 035–037, 106–107, 152, 156.

## Discover and verify
Determine authoritative store, refresh latency, versioned indexing, tombstones, checkpoint and rebuild cutover semantics.
Record exact version/edition, client version, deployment topology, configured values and evidence. Separate documented support from effective configuration and observed behavior. Mark unknowns Requires Verification.

## Implementation decisions
Treat index as projection unless justified; enforce monotonic updates and deletion propagation; reconcile and rebuild safely.
Prefer the existing primitive if it meets the invariant; otherwise record alternatives, compatibility, failure boundaries and residual risk.

## Counterexamples and limits
Successful indexing acknowledgment may not imply immediate visibility or durable authoritative state.
Do not assume capabilities solely from product category or a bundled profile.

## Verification
Deliver older update after delete; rebuild while writes continue; check no resurrection and correct cutover.
Use isolated environments and record commands, versions, expected and actual outcomes. If unavailable, define the test without claiming it passed.
