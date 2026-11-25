# Telemetry and audit pipelines capability profile

Related catalog ranges (starting points, not exhaustive): SDP-119, 135, 146–148, 157.

## Discover and verify
Inspect sampling, cardinality, queues, context propagation, redaction, audit durability and export failure.
Record exact version/edition, client version, deployment topology, configured values and evidence. Separate documented support from effective configuration and observed behavior. Mark unknowns Requires Verification.

## Implementation decisions
Separate business audit from best-effort telemetry; bound export resources; monitor invariant violations and recovery lag.
Prefer the existing primitive if it meets the invariant; otherwise record alternatives, compatibility, failure boundaries and residual risk.

## Counterexamples and limits
Trace sampling cannot prove complete audit coverage; synchronous exporters may cascade failures.
Do not assume capabilities solely from product category or a bundled profile.

## Verification
Disable exporter, generate high-cardinality inputs, trace replay; verify bounded impact and durable required audit.
Use isolated environments and record commands, versions, expected and actual outcomes. If unavailable, define the test without claiming it passed.
