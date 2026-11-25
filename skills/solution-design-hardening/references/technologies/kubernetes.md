# Kubernetes

Related baseline problems: SDP-081, SDP-117, SDP-118, SDP-137, SDP-140, SDP-144.

## Detection
Inspect replicas, CronJobs, migration init containers, readiness/liveness probes, termination grace and scaling policies.

## Implementation
Use durable job identities and idempotent handlers; coordinate migrations through an explicit deployment step. Drain on shutdown, stop intake, finish or abandon safely; use readiness for traffic eligibility and liveness for unrecoverable local failures. Size downstream capacity before scaling.

## Pitfalls / counterexamples
CronJob concurrency policy is not global exactly-once execution. A Lease does not fence writes without enforcement. PodDisruptionBudget does not protect all outage types.

## Verification
Run in a disposable cluster; terminate workers during commit and replay, test rolling mixed versions and measure readiness-related capacity loss.

## Upstream reference
[Official documentation](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/). Confirm installed versions and provider capabilities before selecting APIs. This is guidance, not a tested integration.
