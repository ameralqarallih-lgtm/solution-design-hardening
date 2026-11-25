# Binary object services capability profile

Related catalog ranges (starting points, not exhaustive): SDP-092–100, 124, 156, 159.

## Discover and verify
Verify conditional operations, version identifiers, multipart completion, list/read consistency, retention and authorization.
Record exact version/edition, client version, deployment topology, configured values and evidence. Separate documented support from effective configuration and observed behavior. Mark unknowns Requires Verification.

## Implementation decisions
Use staged upload and explicit metadata state; reconcile independently durable writes; condition cleanup on version/state.
Prefer the existing primitive if it meets the invariant; otherwise record alternatives, compatibility, failure boundaries and residual risk.

## Counterexamples and limits
Object existence or listing is not proof of completed authorized upload; avoid assuming filesystem rename semantics.
Do not assume capabilities solely from product category or a bundled profile.

## Verification
Crash between upload and metadata commit; race finalization against cleanup; verify checksum and tenant isolation.
Use isolated environments and record commands, versions, expected and actual outcomes. If unavailable, define the test without claiming it passed.
