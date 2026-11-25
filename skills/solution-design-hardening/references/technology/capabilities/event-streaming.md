# Ordered event logs capability profile

Related catalog ranges (starting points, not exhaustive): SDP-054–068, 107, 111, 151–152.

## Discover and verify
Identify partition ordering, offset ownership, rebalance, retention, producer transactions and external sink boundaries.
Record exact version/edition, client version, deployment topology, configured values and evidence. Separate documented support from effective configuration and observed behavior. Mark unknowns Requires Verification.

## Implementation decisions
Use stable partition keys and version checks; coordinate checkpoints with effects and handle gaps.
Prefer the existing primitive if it meets the invariant; otherwise record alternatives, compatibility, failure boundaries and residual risk.

## Counterexamples and limits
Exactly-once within a broker does not extend automatically to external databases or APIs.
Do not assume capabilities solely from product category or a bundled profile.

## Verification
Force rebalance and replay around sink commit; test gaps and expired offsets.
Use isolated environments and record commands, versions, expected and actual outcomes. If unavailable, define the test without claiming it passed.
