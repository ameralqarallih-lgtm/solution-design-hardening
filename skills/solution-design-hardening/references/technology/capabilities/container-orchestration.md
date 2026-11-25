# Replicated workload platforms capability profile

Related catalog ranges (starting points, not exhaustive): SDP-050–053, 081–091, 117–118, 137–145.

## Discover and verify
Inspect replica count, rollout policy, probes, disruption budget, resource limits, termination and persistent volume topology.
Record exact version/edition, client version, deployment topology, configured values and evidence. Separate documented support from effective configuration and observed behavior. Mark unknowns Requires Verification.

## Implementation decisions
Drain work safely; separate readiness and liveness; budget downstream capacity and verify mixed-version compatibility.
Prefer the existing primitive if it meets the invariant; otherwise record alternatives, compatibility, failure boundaries and residual risk.

## Counterexamples and limits
A single replica declaration does not guarantee one active worker during rollout or failover.
Do not assume capabilities solely from product category or a bundled profile.

## Verification
Terminate workers mid-commit; roll mixed versions; test dependency outage and recovery under load.
Use isolated environments and record commands, versions, expected and actual outcomes. If unavailable, define the test without claiming it passed.
