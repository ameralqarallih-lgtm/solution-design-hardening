# Integration Operations — problem playbook

Signals are investigation leads, not findings. Confirm the business invariant and actual runtime guarantees. Tests are proposals until executed in an isolated environment. Use the simplest sufficient safeguard; do not introduce a pattern merely because it is listed.

## SDP-112 — Webhook authenticity failure

- **Failure:** Forged or replayed callbacks change business state.
- **Detection:** Webhook accepts unsigned body or lacks event dedupe.
- **Remediation and safeguards:** Verify raw body signature and context; enforce replay policy and durable event ID.
- **Verification:** Tamper body and replay valid callback; reject forged and avoid duplicate effect.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-113 — Unbounded deduplication state

- **Failure:** Inbox or idempotency records grow without a lifecycle.
- **Detection:** Inbox/dedupe grows indefinitely or cleanup breaks guarantees.
- **Remediation and safeguards:** Retention based on supported horizon; archive or durable uniqueness.
- **Verification:** Generate sustained load and replay near boundary; size bounded without lost protection.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-114 — Outbox relay backlog

- **Failure:** Committed intents accumulate without timely publication.
- **Detection:** Outbox relay lag invisible or unbounded polling batch.
- **Remediation and safeguards:** Monitor oldest pending age, bound batch/concurrency and retry; safe recovery.
- **Verification:** Disable broker then restore; backlog drains without starving DB.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-115 — Unsafe dead-letter replay

- **Failure:** Bulk redrive reintroduces poison messages or duplicate effects.
- **Detection:** DLQ redrive repeats effects or poison loop.
- **Remediation and safeguards:** Inspect reason, fix cause, preserve ID, throttle and authorize redrive.
- **Verification:** Replay mixed corrected/poison/already-applied events; valid only progress safely.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-116 — Cancellation ambiguity

- **Failure:** Client cancellation is treated as proof that a remote operation stopped.
- **Detection:** Cancellation treated as proof of remote rollback.
- **Remediation and safeguards:** Separate cancellation request from confirmed outcome; reconcile stable operation.
- **Verification:** Cancel after remote commit; final status reflects committed effect.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-117 — Graceful shutdown failure

- **Failure:** Termination interrupts work before commit or acknowledgment.
- **Detection:** Shutdown stops workers mid-effect and acknowledges work.
- **Remediation and safeguards:** Drain admission; bounded grace; durable checkpoints and redelivery.
- **Verification:** Terminate during processing; no loss, stale ownership or duplicate effect.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-118 — Readiness-induced overload

- **Failure:** Health or readiness transitions remove capacity and overload surviving replicas.
- **Detection:** Probe ties readiness of all replicas to shared slow dependency.
- **Remediation and safeguards:** Separate startup/liveness/readiness; bound checks and model degraded capacity.
- **Verification:** Slow shared dependency; avoid restart/removal cascade while routing safely.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-119 — Missing recovery signals

- **Failure:** Failures accumulate silently despite healthy process metrics.
- **Detection:** Only CPU/uptime monitored while invariant errors accumulate.
- **Remediation and safeguards:** Measure business discrepancies, oldest backlog and recovery outcomes; actionable alerts.
- **Verification:** Inject stuck outbox or reconciliation mismatch; alert fires with useful context.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-120 — Cross-tenant state leakage

- **Failure:** Shared cache, dedupe or job keys collide across tenants.
- **Detection:** Cache/inbox/job identifiers omit tenant or access scope.
- **Remediation and safeguards:** Scope identity and authorization consistently across layers.
- **Verification:** Use same local ID in two tenants; no data/effect crosses boundary.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-121 — Unsafe reconciliation overwrite

- **Failure:** Repair jobs overwrite valid newer or in-flight state.
- **Detection:** Repair job blindly overwrites current record from old snapshot.
- **Remediation and safeguards:** Match stable external identity, compare versions and age; audit correction.
- **Verification:** Concurrent valid update during reconciliation; repair skips conflict.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-122 — Unbounded fan-out

- **Failure:** A request launches excessive parallel downstream work.
- **Detection:** Unbounded gather/parallel loop launches downstream calls.
- **Remediation and safeguards:** Bound per-request and global concurrency; enforce deadlines and cancellation.
- **Verification:** Large fan-out input; active calls bounded and partial failure handled.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-123 — Dependency contract drift

- **Failure:** External provider changes fields or semantics relied on by consumers.
- **Detection:** External response shape or meaning changes silently.
- **Remediation and safeguards:** Validate boundary contracts and semantics; quarantine invalid data.
- **Verification:** Replay changed provider payload; safe rejection or compatible handling.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-124 — Object cleanup race

- **Failure:** Cleanup deletes an object that is being finalized or reused.
- **Detection:** Age-only cleanup deletes object during finalization.
- **Remediation and safeguards:** Conditional lifecycle claim, grace and versioned deletion; recheck ownership.
- **Verification:** Pause finalization across cleanup; live reference not deleted.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.
