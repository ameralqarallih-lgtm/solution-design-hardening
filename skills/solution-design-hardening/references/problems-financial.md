# Financial — problem playbook

Signals are investigation leads, not findings. Confirm the business invariant and actual runtime guarantees. Tests are proposals until executed in an isolated environment. Use the simplest sufficient safeguard; do not introduce a pattern merely because it is listed.

## SDP-001 — Duplicate Charge

- **Failure:** A customer is charged multiple times due to retries or network failures.
- **Detection:** Charge called before durable operation claim; retry uses new provider key.
- **Remediation and safeguards:** Persist unique scoped operation and request hash; reuse provider key; reconcile unknown outcomes.
- **Verification:** Lose provider response after charge and retry concurrently; assert one provider charge and one ledger effect.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-002 — Inconsistent Financial Balance

- **Failure:** Money is deducted from one account without being credited to another.
- **Detection:** Debit and credit committed separately or unbalanced journal allowed.
- **Remediation and safeguards:** Post balanced entries atomically per currency; enforce posting invariant and reversal semantics.
- **Verification:** Crash between legs; assert neither posts or both post and journal balances.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-003 — Double Spending

- **Failure:** The same available balance is spent through concurrent transactions.
- **Detection:** Balance read then unconditional debit.
- **Remediation and safeguards:** Conditional debit or serializable locked invariant check in same transaction.
- **Verification:** Two spends exceeding combined balance; only admissible spend commits.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-004 — Lost Update

- **Failure:** Two transactions update the same record, overwriting each other's changes.
- **Detection:** Read-modify-write without version predicate.
- **Remediation and safeguards:** Compare version on update; reject conflict or recompute safely.
- **Verification:** Two readers update same version; no silent overwrite.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-005 — Partial Transaction Failure

- **Failure:** Some operations succeed while others fail.
- **Detection:** Multiple durable effects with no recovery state.
- **Remediation and safeguards:** Use local transaction if possible; otherwise durable saga with idempotent compensation.
- **Verification:** Fail each step after prior commit; recover or compensate to valid state.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-006 — Uncertain Transaction Status

- **Failure:** A payment succeeds, but the client receives a timeout.
- **Detection:** Timeout mapped to definitive payment failure.
- **Remediation and safeguards:** Persist unknown outcome and query provider by stable reference before retry.
- **Verification:** Drop successful provider response; reconcile without second payment.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-007 — Financial Record Manipulation

- **Failure:** Historical financial transactions are modified or deleted.
- **Detection:** Posted journal editable via ordinary CRUD.
- **Remediation and safeguards:** Restrict updates and deletes; append reversal with actor and reason; audit privileged access.
- **Verification:** Attempt edit/delete via API and DB role; reversal preserves history.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-008 — Balance Calculation Drift

- **Failure:** Stored balances become inconsistent with transaction history.
- **Detection:** Stored balance independently changed from journal.
- **Remediation and safeguards:** Derive or atomically maintain projection; compare ledger totals and repair conditionally.
- **Verification:** Inject projection drift; reconciliation detects and repairs without changing journal.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-009 — Concurrent Resource Reservation

- **Failure:** Multiple users reserve the same seat, room or inventory item.
- **Detection:** Availability check separated from reservation write.
- **Remediation and safeguards:** Enforce capacity or exclusivity in authoritative transaction; unique slot or conditional decrement.
- **Verification:** Competing clients claim last slot; at most one succeeds.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-010 — Abandoned Reservation

- **Failure:** Reserved resources are never released after an incomplete transaction.
- **Detection:** Expired reservations never release or release confirmed reservation.
- **Remediation and safeguards:** Versioned reservation state and expiry transition; conditional release.
- **Verification:** Race expiry with confirmation; capacity restored exactly once only if expired.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.
