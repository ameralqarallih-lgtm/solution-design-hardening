# Durable orchestration capability profile

Related catalog ranges (starting points, not exhaustive): SDP-081–091, 116, 155.

## Discover and verify
Verify persisted history, activity delivery semantics, deterministic replay, versioning, cancellation and compensation.
Record exact version/edition, client version, deployment topology, configured values and evidence. Separate documented support from effective configuration and observed behavior. Mark unknowns Requires Verification.

## Implementation decisions
Make activities idempotent; persist operation identity and handle uncertain outcomes; version long-running workflows.
Prefer the existing primitive if it meets the invariant; otherwise record alternatives, compatibility, failure boundaries and residual risk.

## Counterexamples and limits
A durable workflow does not make an external side effect atomic.
Do not assume capabilities solely from product category or a bundled profile.

## Verification
Crash after external success before activity completion; replay and verify no duplicate effect.
Use isolated environments and record commands, versions, expected and actual outcomes. If unavailable, define the test without claiming it passed.
