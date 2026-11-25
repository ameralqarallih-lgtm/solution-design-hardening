# Financial Extensions - problem playbook

Signals are investigation leads, not findings. Confirm the business invariant and actual runtime guarantees. Tests are proposals until executed in an isolated environment. Use the simplest sufficient safeguard; do not introduce a pattern merely because it is listed.

## SDP-101 - Monetary rounding drift

- **Failure:** Binary floating point or inconsistent rounding changes financial totals.
- **Detection:** Binary float used for money or inconsistent rounding boundaries.
- **Remediation and safeguards:** Use exact decimal/minor units; explicit rounding and allocation residual rules.
- **Verification:** Split amount across items and recombine; totals equal approved amount.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-102 - Currency mixing

- **Failure:** Ledger entries or balances mix incompatible currencies.
- **Detection:** Amounts summed without currency dimension.
- **Remediation and safeguards:** Currency-aware types and per-currency posting; explicit FX legs and rates.
- **Verification:** Attempt mixed-currency sum/post; reject or convert by authorized rule.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-103 - Idempotency retention gap

- **Failure:** A delayed retry arrives after its deduplication key expires.
- **Detection:** Dedupe TTL shorter than replay/retry horizon.
- **Remediation and safeguards:** Align retention or durable business uniqueness beyond TTL.
- **Verification:** Replay after expiry but within supported horizon; no duplicate effect.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-104 - Concurrent idempotency claim

- **Failure:** Two requests both see an unused key before processing.
- **Detection:** Non-atomic check then claim of operation key.
- **Remediation and safeguards:** Unique scoped atomic claim, payload hash and durable outcome; handle in-progress.
- **Verification:** Concurrent same-key requests and mismatched payload; one claim and mismatch rejected.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.
