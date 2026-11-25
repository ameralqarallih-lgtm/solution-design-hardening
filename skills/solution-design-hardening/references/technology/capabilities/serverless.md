# Event-triggered managed execution capability profile

Related catalog ranges (starting points, not exhaustive): SDP-038–053, 069–091, 154, 158.

## Discover and verify
Verify trigger redelivery, execution deadline, concurrency cap, instance reuse, cancellation and provider quotas.
Record exact version/edition, client version, deployment topology, configured values and evidence. Separate documented support from effective configuration and observed behavior. Mark unknowns Requires Verification.

## Implementation decisions
Persist progress and operation identity; coordinate shared quota; bound fan-out and use durable handoff.
Prefer the existing primitive if it meets the invariant; otherwise record alternatives, compatibility, failure boundaries and residual risk.

## Counterexamples and limits
Warm instance memory is neither durable nor shared; timeout does not prove external failure.
Do not assume capabilities solely from product category or a bundled profile.

## Verification
Replay trigger, exhaust concurrency in test environment, interrupt after external acceptance; reconcile.
Use isolated environments and record commands, versions, expected and actual outcomes. If unavailable, define the test without claiming it passed.
