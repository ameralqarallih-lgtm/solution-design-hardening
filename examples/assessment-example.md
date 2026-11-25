# Example assessment (illustrative)

Scope: synthetic order application with one database and external broker. No actual customer or production data.

| Finding | Problems | Status | Severity | Evidence | Remediation |
|---|---|---|---|---|---|
| FND-001 | SDP-023, SDP-063 | Not Addressed | High (illustrative) | `evals/fixtures/transactions.py`, `vulnerable_order`: separate commits | REM-001 |
| FND-002 | SDP-024, SDP-055 | Not Addressed | High (illustrative) | `vulnerable_consumer`: repeated inserts | REM-002 |

REM-001: save business row and immutable event intent in one transaction. Verify rollback and recoverable intent. Add a confirmed relay in a real broker environment; test interruption after publish and before recording delivery.

REM-002: use a durable unique consumer-scoped inbox key in the same transaction as local effect. Verify concurrent duplicate deliveries; acknowledge after commit in the actual broker integration. Ensure dedupe retention covers replay.

This is a focused assessment, not a full 235-problem coverage claim. Severity depends on the real business impact. SQLite fixtures demonstrate local transaction behavior only.
