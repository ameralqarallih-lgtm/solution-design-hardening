# Leases and consensus services capability profile

Related catalog ranges (starting points, not exhaustive): SDP-046–049, 125–130.

## Discover and verify
Verify lock ownership, lease renewal, fencing token monotonicity, quorum behavior and resource enforcement.
Record exact version/edition, client version, deployment topology, configured values and evidence. Separate documented support from effective configuration and observed behavior. Mark unknowns Requires Verification.

## Implementation decisions
Use established coordination primitives; validate fencing at every protected write.
Prefer the existing primitive if it meets the invariant; otherwise record alternatives, compatibility, failure boundaries and residual risk.

## Counterexamples and limits
A lease alone does not stop paused clients from writing after expiry.
Do not assume capabilities solely from product category or a bundled profile.

## Verification
Pause owner until lease expires, let successor write, resume old owner; assert stale write rejected.
Use isolated environments and record commands, versions, expected and actual outcomes. If unavailable, define the test without claiming it passed.
