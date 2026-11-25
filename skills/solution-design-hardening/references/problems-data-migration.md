# Data Migration — problem playbook

Signals are investigation leads, not findings. Confirm the business invariant and actual runtime guarantees. Tests are proposals until executed in an isolated environment. Use the simplest sufficient safeguard; do not introduce a pattern merely because it is listed.

## SDP-105 — Multi-writer conflict

- **Failure:** Independent writers overwrite concurrent changes.
- **Detection:** Independent regions/services overwrite by wall-clock last writer.
- **Remediation and safeguards:** Single writer or domain-approved merge with causal/version tracking.
- **Verification:** Concurrent conflicting updates under partition; resolution meets invariant.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-106 — Tombstone resurrection

- **Failure:** Delayed replication or replay recreates a deleted entity.
- **Detection:** Deletion metadata removed before delayed updates expire.
- **Remediation and safeguards:** Versioned tombstones retained across replay horizon; reject older writes.
- **Verification:** Delete then replay old create; entity stays deleted.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-107 — Projection rebuild inconsistency

- **Failure:** A rebuilt read model loses concurrent changes or exposes incomplete state.
- **Detection:** Projection rebuilt from snapshot without concurrent catch-up.
- **Remediation and safeguards:** Consistent snapshot/checkpoint, catch-up and atomic cutover.
- **Verification:** Write during rebuild; new projection matches authoritative state at cutover.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-108 — Mixed-version deployment

- **Failure:** Old and new instances cannot share schemas or contracts.
- **Detection:** Schema/contract change breaks old live instances.
- **Remediation and safeguards:** Expand-contract; test old/new readers and writers and rollback compatibility.
- **Verification:** Run mixed versions through migration; both operate until contract phase.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-109 — Backfill race

- **Failure:** A migration backfill overwrites newer live writes.
- **Detection:** Backfill overwrites values changed after scan.
- **Remediation and safeguards:** Conditional versioned updates, resumable bounded batches.
- **Verification:** Pause backfill then update live row; backfill cannot overwrite newer value.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-110 — Restore inconsistency

- **Failure:** Restoring one store replays side effects or diverges from other stores.
- **Detection:** Stores restored to incompatible points or replay effects uncontrolled.
- **Remediation and safeguards:** Document recovery dependencies, aligned checkpoints and reconciliation; isolate replay effects.
- **Verification:** Restore disposable stores with skewed checkpoints; reconcile before reopening writes.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-111 — CDC retention gap

- **Failure:** A connector resumes after its source log position is no longer available.
- **Detection:** CDC offset older than retained log.
- **Remediation and safeguards:** Monitor retention headroom; stop unsafe resume; controlled resnapshot with catch-up.
- **Verification:** Expire source offset; recovery detects gap and rebuilds without silent loss.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.
