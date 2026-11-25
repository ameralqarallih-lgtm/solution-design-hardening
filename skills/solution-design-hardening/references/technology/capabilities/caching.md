# Derived caches capability profile

Related catalog ranges (starting points, not exhaustive): SDP-011–022, 132.

## Discover and verify
Identify local versus shared caches, TTL, invalidation ordering, atomic compare-and-set, key scope and fallback capacity.
Record exact version/edition, client version, deployment topology, configured values and evidence. Separate documented support from effective configuration and observed behavior. Mark unknowns Requires Verification.

## Implementation decisions
Specify freshness and enforce monotonic versions or invalidation watermarks where required; bound miss amplification.
Prefer the existing primitive if it meets the invariant; otherwise record alternatives, compatibility, failure boundaries and residual risk.

## Counterexamples and limits
TTL alone does not prevent stale refill; local singleflight does not coordinate replicas.
Do not assume capabilities solely from product category or a bundled profile.

## Verification
Pause stale reader before refill, commit writer, resume reader; test cache outage and expiry burst.
Use isolated environments and record commands, versions, expected and actual outcomes. If unavailable, define the test without claiming it passed.
