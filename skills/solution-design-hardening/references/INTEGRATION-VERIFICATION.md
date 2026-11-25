# Integration verification and controlled failure injection

Use this reference for correctness-critical remediation and runtime verification. This is technology-independent; do not require Docker, a specific database or the repository's example lab if the actual application uses different infrastructure.

## Verification and completion

For correctness-critical changes, use [integration verification and controlled failure injection](INTEGRATION-VERIFICATION.md). Select actual infrastructure from capability evidence, establish fault boundaries, and distinguish executed tests from illustrative or blocked tests. The optional repository lab and candidate scanner are not prerequisites or proof of product correctness.

For concurrency tests, coordinate competing operations using barriers or controlled scheduling rather than sleep-based timing. Exercise real database constraints and isolation in disposable environments when permitted. Test both vulnerable and corrected paths; record environment, commands and actual outcomes. A static finding can be confirmed by a demonstrable counterexample, but a proposed fix is not verified until appropriate evidence exists. Review code changes against invariants and distinguish runtime tests from static checks.

- Test business invariants under concurrent execution and duplicate requests/events.
- Test failure boundaries before and after commits, publishes, acknowledgments, cache updates, and external calls.
- Where relevant, test multiple instances, retries under load, cache expiration, worker crashes, and recovery/replay.
- Use isolated integration environments; mocks alone do not establish real database isolation or broker guarantees.
- Report executed commands and results; label unexecuted tests and unknown runtime assumptions explicitly.
- For a full assessment, reconcile counts against the catalog and ensure every unresolved applicable gap maps to a remediation or verification task. Do not implement until authorized.

## Derive a verification plan from the invariant

1. State the invariant and owner, the consistency scope, allowed staleness, delivery/replay window and recovery targets. Unknown requirements are verification gaps, not invented guarantees.
2. Map the operation timeline: validation, claim, transaction begin, business mutation, intent persistence, commit, remote send, remote acceptance, local receipt, acknowledgment and cleanup. Only include relevant steps. Mark every non-atomic boundary and point of irreversible external effect.
3. Discover actual products, versions, topology, isolation and client behavior via the adaptive technology workflow. Choose representative disposable infrastructure. A mock may demonstrate control flow but cannot establish real isolation, persistence, delivery, failover or locking.
4. Define a failing baseline or an explicit proof of the vulnerable interleaving. Add a negative control where the existing approach is valid. Then execute the corrected path at the identical fault point and assert durable business state, not just an HTTP success or log entry.
5. Coordinate concurrency with separate connections/processes and barriers, test hooks or deterministic scheduling. Poll only for asynchronous observation with a bounded deadline; do not use sleeps to guess the ordering of competing actions. Time-box hangs and retries. Record whether a failure reached the intended injection point.
6. Use the least disruptive fault: injected exception; process exit; connection loss; real service restart; then network partition or failover only if authorized and necessary. Distinguish each from the others. Never introduce test-only fault hooks in production paths without explicit design review.
7. Execute authorized tests; collect command, versions, topology, fault point, seed (if used), run count, exit status, invariant observations, artifacts and remaining scope. A skipped, blocked or unexecuted test is never a pass.

## Boundary-oriented test selection

| Boundary | Test idea | Assert after recovery |
|---|---|---|
| Before / after atomic commit | Interrupt process with transaction open, then immediately after successful commit | Atomic records absent or present together |
| After remote acceptance before local receipt | Simulate lost response; retry using same identity | No extra business effect; reconcile uncertain outcome |
| Broker confirm before local sent marker | Replay stable event identity | No permanent loss; duplicates are tolerated |
| Consumer durable commit before ack | Disconnect consumer, redeliver | Durable effect occurs once within dedupe scope |
| Cache fill after concurrent invalidation | Suspend old reader, commit writer, invalidate, resume | Required freshness guarantee holds; verify failover/eviction separately |
| Read before competing conditional write | Two clients read same starting state | Business capacity or version constraint is enforced |
| Lease expiration before old owner resumes | Pause old owner, acquire newer authority, resume | Protected resource rejects old authority |
| Retry under dependency overload | Inject bounded transient failures and observe aggregate attempts | Deadline, retry budget, admission limits respected |
| Mixed versions and migration | Run old/new versions with migration and rollback sequence | Compatible read/write, safe cutover and no data loss |
| Process shutdown and restart | Terminate worker at a checkpoint or pre-ack boundary | Work recovers without invalid state or duplicate effects |

## Safety and result classification

Use isolated environments with synthetic data and scoped credentials. No production endpoints, shared queues, customer records, cloud resource creation or destructive tests unless separately authorized. Do not download or start containers automatically merely because the skill was activated. Capture the exact scope of cleanup. Keep logs redacted; test identifiers and evidence must not expose secrets. Respect network access and resource budgets.

Record each experiment as **passed, failed, blocked, skipped, or not run**. A passing vulnerable baseline means the test successfully reproduced the defect; it does not mean the vulnerable code is acceptable. A corrected test proves only its asserted invariant, version, configuration, failure model and observed scope. Do not infer exactly-once delivery, production availability or a verified fix from a passing teaching fixture. If required infrastructure is unavailable, run appropriate safe local tests and leave the real guarantee Requires Verification.
