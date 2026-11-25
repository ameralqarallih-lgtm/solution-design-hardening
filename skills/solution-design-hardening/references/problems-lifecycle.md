# Lifecycle — problem playbook

Signals are investigation leads, not findings. Confirm the business invariant and actual runtime guarantees. Tests are proposals until executed in an isolated environment. Use the simplest sufficient safeguard; do not introduce a pattern merely because it is listed.

## SDP-151 — Mutable outbox payload

- **Failure:** Relay emits state different from committed event.
- **Detection:** Outbox contains references to mutable state and relay publishes newer content.
- **Remediation and safeguards:** Persist immutable event payload or versioned snapshot reference.
- **Verification:** Update aggregate before relay publishes; event matches committed version.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-152 — Event sequence gap

- **Failure:** Missing delta silently corrupts projection.
- **Detection:** Event sequence gaps ignored when consumer requires every delta.
- **Remediation and safeguards:** Detect missing sequence and buffer/recover from replay or snapshot.
- **Verification:** Deliver delta 3 without 2; no silent incorrect projection.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-153 — Idempotency scope collision

- **Failure:** Unrelated operations share dedupe identity.
- **Detection:** Idempotency key reused across operations or actor scopes.
- **Remediation and safeguards:** Scope by tenant, actor where required and operation; verify fingerprint.
- **Verification:** Reuse key across endpoints/actors; no incorrect result disclosure or suppression.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-154 — Reconnect storm

- **Failure:** Clients reconnect simultaneously after outage.
- **Detection:** Dependency reconnect loops bypass normal request retry budgets.
- **Remediation and safeguards:** Apply bounded jittered reconnect and connection admission.
- **Verification:** Restart dependency with many clients; handshake load stays bounded.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-155 — Schedule timezone ambiguity

- **Failure:** DST or timezone changes duplicate or skip work.
- **Detection:** Time-zone or daylight-saving schedule interpreted as fixed local offset.
- **Remediation and safeguards:** Store explicit zone and occurrence policy; use durable occurrence IDs.
- **Verification:** Test DST overlap/gap and timezone changes; intended occurrences run once in effect.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-156 — Incomplete deletion propagation

- **Failure:** Deleted data persists in uncontrolled copies.
- **Detection:** Deletion request removes primary data but retained copies remain indefinitely.
- **Remediation and safeguards:** Map replicas/backups/caches and retention/legal requirements; propagate deletion or restricted retention.
- **Verification:** Delete synthetic subject; verify active copies removed and retained copies governed.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-157 — Audit dual write

- **Failure:** Business mutation commits without required audit evidence.
- **Detection:** Business state changes but audit record can fail independently.
- **Remediation and safeguards:** Commit mandatory audit intent atomically with mutation; protect retention and access.
- **Verification:** Fail audit write; required mutation does not silently succeed without audit intent.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-158 — Distributed provider quota breach

- **Failure:** Independent replicas exceed shared provider limits.
- **Detection:** External provider rate limit ignored by workers and per-replica retries.
- **Remediation and safeguards:** Shared quota-aware admission; honor retry hints; bound retry and queue age.
- **Verification:** Inject provider 429 across replicas; aggregate rate stays within contract.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-159 — Claim-check retention mismatch

- **Failure:** Payload expires before supported replay.
- **Detection:** Object lifecycle policy expires payload before event replay horizon.
- **Remediation and safeguards:** Coordinate object retention with consumers and legal policy; detect missing payload.
- **Verification:** Replay near supported horizon; referenced payload remains available or explicit recovery path.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-160 — Long snapshot retention pressure

- **Failure:** Long transactions prevent cleanup of old versions or logs.
- **Detection:** Long transaction holds snapshot preventing vacuum/log truncation or exhausting version store.
- **Remediation and safeguards:** Bound transaction lifetime; stream/batch safely; monitor retained versions/log growth.
- **Verification:** Hold reader under writes; detect and mitigate retention pressure without violating snapshot needs.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.
