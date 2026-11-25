# Identity and authorization systems capability profile

Related catalog ranges (starting points, not exhaustive): SDP-112, 120, 131–136, 150.

## Discover and verify
Identify token issuer/audience, delegated authority, policy version, revocation behavior, tenant scope and protected effect.
Record exact version/edition, client version, deployment topology, configured values and evidence. Separate documented support from effective configuration and observed behavior. Mark unknowns Requires Verification.

## Implementation decisions
Enforce authorization at actual effect; scope cache and idempotency keys; redact telemetry and validate delegation.
Prefer the existing primitive if it meets the invariant; otherwise record alternatives, compatibility, failure boundaries and residual risk.

## Counterexamples and limits
Authentication alone is not authorization; cached authorization can outlive revocation.
Do not assume capabilities solely from product category or a bundled profile.

## Verification
Revoke authorization between check and write; attempt cross-tenant replay and check logs for sensitive data.
Use isolated environments and record commands, versions, expected and actual outcomes. If unavailable, define the test without claiming it passed.
