# Operational verification and safe migration

Define targets with owners; do not invent availability, freshness, throughput, RPO or RTO commitments.

| Boundary | Useful signals | Recovery checks |
|---|---|---|
| Payments and ledger | Unknown outcomes, imbalance count, reconciliation age, duplicate suppression | Compare provider IDs and amounts; use auditable reversals or correction entries |
| Outbox and inbox | Oldest pending age, pending count, publish failures, duplicates, retention | Pause relay, restart, replay safely; ensure dedupe survives allowed replay horizon |
| Cache | Hit ratio, origin load, invalidation lag, stale age, eviction | Test cache loss under bounded load and versioned refill |
| Dependency resilience | Attempt/original request ratio, timeouts, saturation, breaker state, rejected requests | Verify bounded retries, cancellation and gradual recovery |
| Jobs and workflows | Oldest pending age, lease expiration, stuck states, compensation failures | Restart workers and resume without duplicate side effects |
| Storage and replication | Orphan counts, missing object references, checksum failures, replica/CDC lag | Reconcile with grace periods and version checks; test restore consistency |

Correlate operations across HTTP, messages and jobs using non-secret IDs. Avoid sensitive payloads and unbounded metric labels. Define actionable alerts, ownership, and a recovery runbook for material risks.

## Rollout

- Establish baseline and regression tests; choose the smallest reversible change.
- For schema/contract evolution, expand first, deploy compatible readers/writers, backfill in bounded conditional batches, verify convergence, switch traffic, then contract after older versions and replay windows are retired.
- Do not introduce uncontrolled dual writes during a migration. Choose authoritative ownership and a recovery strategy for coexistence.
- Use measured rollout gates and explicit stop conditions. Test old/new version combinations and in-flight events.
- Distinguish code rollback, forward repair, restore and business compensation. Reverting binaries cannot undo external financial effects or destructive schema changes.
- Treat replay/redrive as a controlled operation: inspect cause, scope by tenant/entity/time, verify deduplication and retention, throttle and audit. Never perform production recovery without authorization.
