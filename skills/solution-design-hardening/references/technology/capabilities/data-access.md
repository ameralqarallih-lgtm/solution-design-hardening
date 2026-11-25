# Orms and database clients capability profile

Related catalog ranges (starting points, not exhaustive): SDP-004, 023–037, 139–140.

## Discover and verify
Inspect unit-of-work scope, actual SQL, transaction enlistment, batching, retry delegates and connection lifecycle.
Record exact version/edition, client version, deployment topology, configured values and evidence. Separate documented support from effective configuration and observed behavior. Mark unknowns Requires Verification.

## Implementation decisions
Use database-enforced constraints, correct transaction scope and concurrency tokens; retry only safe whole units.
Prefer the existing primitive if it meets the invariant; otherwise record alternatives, compatibility, failure boundaries and residual risk.

## Counterexamples and limits
ORM annotations and transaction decorators may not cover alternate call paths or separate connections.
Do not assume capabilities solely from product category or a bundled profile.

## Verification
Inspect generated SQL; use actual engine to race updates and inject rollback; verify side effects are not repeated.
Use isolated environments and record commands, versions, expected and actual outcomes. If unavailable, define the test without claiming it passed.
