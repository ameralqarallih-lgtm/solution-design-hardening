# Gateways and api clients capability profile

Related catalog ranges (starting points, not exhaustive): SDP-038–053, 069–080, 116, 122–123, 158.

## Discover and verify
Trace timeouts/retries at every hop, idempotency forwarding, quotas, request limits and version compatibility.
Record exact version/edition, client version, deployment topology, configured values and evidence. Separate documented support from effective configuration and observed behavior. Mark unknowns Requires Verification.

## Implementation decisions
Assign retry ownership, propagate deadlines, validate contracts, scope keys and bound admission.
Prefer the existing primitive if it meets the invariant; otherwise record alternatives, compatibility, failure boundaries and residual risk.

## Counterexamples and limits
Gateway timeout or cancellation does not imply downstream rollback; independent retry policies multiply.
Do not assume capabilities solely from product category or a bundled profile.

## Verification
Inject lost response, overload and partial fan-out failure; count actual attempts and business effects.
Use isolated environments and record commands, versions, expected and actual outcomes. If unavailable, define the test without claiming it passed.
