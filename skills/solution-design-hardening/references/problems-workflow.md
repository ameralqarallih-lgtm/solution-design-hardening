# Workflow - problem playbook

Signals are investigation leads, not findings. Confirm the business invariant and actual runtime guarantees. Tests are proposals until executed in an isolated environment. Use the simplest sufficient safeguard; do not introduce a pattern merely because it is listed.

## SDP-081 - Duplicate Scheduled Job

- **Failure:** Multiple application instances execute the same scheduled job.
- **Detection:** Every replica runs same cron effect.
- **Remediation and safeguards:** Durable job occurrence identity; coordinated scheduler or idempotent execution.
- **Verification:** Start two replicas for same occurrence; one intended effect.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-082 - Overlapping Job Execution

- **Failure:** A scheduled job starts before its previous execution finishes.
- **Detection:** Scheduler starts new run while old run holds resources.
- **Remediation and safeguards:** Explicit overlap policy, bounded concurrency and fenced ownership if needed.
- **Verification:** Pause first run past next schedule; overlap follows policy safely.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-083 - Stuck Workflow

- **Failure:** A workflow remains indefinitely in an intermediate state.
- **Detection:** Workflow pending forever without timeout or owner.
- **Remediation and safeguards:** Durable deadlines, watchdog, escalation and repair path.
- **Verification:** Suppress completion event; workflow reaches explicit recoverable state.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-084 - Lost Job Progress

- **Failure:** A worker crashes before completing a long-running operation.
- **Detection:** Progress only in memory or checkpoint before effect.
- **Remediation and safeguards:** Durable checkpoint consistent with effect or replay-safe operation.
- **Verification:** Crash between effect and checkpoint; resume without loss/duplication.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-085 - Partial Workflow Completion

- **Failure:** Early workflow steps succeed while later steps fail.
- **Detection:** Later step fails after earlier business commitment.
- **Remediation and safeguards:** Persist step outcomes; idempotent compensation or forward recovery.
- **Verification:** Fail each step and compensation; recovery remains possible and auditable.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-086 - Orphaned Background Job

- **Failure:** A crashed worker leaves a job marked as running.
- **Detection:** Job marked running indefinitely after worker death.
- **Remediation and safeguards:** Heartbeat/lease and safe reclaim with fencing where effects require it.
- **Verification:** Kill worker; replacement resumes and stale worker cannot corrupt state.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-087 - Infinite Retry Loop

- **Failure:** A permanently failing operation is continuously retried.
- **Detection:** All failures retried forever.
- **Remediation and safeguards:** Classify errors; attempt/time limits and quarantine/manual escalation.
- **Verification:** Permanent error reaches terminal state; transient error recovers within budget.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-088 - Job Starvation

- **Failure:** Low-priority jobs are never executed.
- **Detection:** Continuous high-priority work prevents low-priority execution.
- **Remediation and safeguards:** Fair scheduling, aging or reserved capacity.
- **Verification:** Flood high priority; low priority progresses within defined bound.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-089 - Missed Scheduled Execution

- **Failure:** A scheduled task is skipped during an outage.
- **Detection:** In-memory scheduler loses occurrence during outage.
- **Remediation and safeguards:** Persist schedule and occurrence IDs; explicit misfire policy.
- **Verification:** Stop scheduler across scheduled time; catch-up or skip per documented policy.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-090 - Invalid State Transition

- **Failure:** A business entity moves into an invalid status.
- **Detection:** Status freely assignable without transition guard.
- **Remediation and safeguards:** State machine and atomic expected-state/version transition.
- **Verification:** Race incompatible transitions; only allowed transition commits.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-091 - Duplicate External Side Effect

- **Failure:** A workflow repeats an email, payment or external submission after recovery.
- **Detection:** Activity retry uses new external identifier each time.
- **Remediation and safeguards:** Stable external operation ID, provider idempotency or inquiry/reconciliation.
- **Verification:** Crash after provider effect; resume without duplicate effect.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.
