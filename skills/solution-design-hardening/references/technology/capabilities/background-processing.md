# Workers and schedulers capability profile

Related catalog ranges (starting points, not exhaustive): SDP-081–091, 117, 150, 155.

## Discover and verify
Check job claim atomicity, lease expiry, heartbeat, retry/misfire policy, tenant context and time zone semantics.
Record exact version/edition, client version, deployment topology, configured values and evidence. Separate documented support from effective configuration and observed behavior. Mark unknowns Requires Verification.

## Implementation decisions
Use durable claims and checkpoints; reject expired owners at the protected resource; bound retries.
Prefer the existing primitive if it meets the invariant; otherwise record alternatives, compatibility, failure boundaries and residual risk.

## Counterexamples and limits
A singleton scheduler does not guarantee exactly-once execution.
Do not assume capabilities solely from product category or a bundled profile.

## Verification
Run two workers, expire one lease and resume it; test restart and daylight-saving transitions.
Use isolated environments and record commands, versions, expected and actual outcomes. If unavailable, define the test without claiming it passed.
