# Messaging — problem playbook

Signals are investigation leads, not findings. Confirm the business invariant and actual runtime guarantees. Tests are proposals until executed in an isolated environment. Use the simplest sufficient safeguard; do not introduce a pattern merely because it is listed.

## SDP-054 — Message Loss

- **Failure:** A message disappears before successful processing.
- **Detection:** Non-durable publish or ack before durable effect.
- **Remediation and safeguards:** Use appropriate broker durability, confirms and consumer commit ordering.
- **Verification:** Kill producer/broker/consumer at each boundary; required message is recovered.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-055 — Duplicate Message

- **Failure:** A message is delivered more than once.
- **Detection:** Consumer assumes each delivery is unique.
- **Remediation and safeguards:** Use stable event ID and atomic deduplication; handle retention horizon.
- **Verification:** Redeliver before and after ack; one intended effect.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-056 — Out-of-Order Messages

- **Failure:** Events arrive in an incorrect sequence.
- **Detection:** Consumer applies arrival order without version check.
- **Remediation and safeguards:** Partition by aggregate where supported; version/gap handling based on event semantics.
- **Verification:** Deliver versions 3,1,2; state does not regress or lose required deltas.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-057 — Poison Message

- **Failure:** A message repeatedly fails and blocks processing.
- **Detection:** Permanent failure repeatedly requeues same message.
- **Remediation and safeguards:** Classify permanent errors; bounded attempts and quarantine with metadata.
- **Verification:** Send malformed message; healthy traffic progresses and poison quarantined.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-058 — Message Replay Side Effects

- **Failure:** Reprocessing historical messages triggers duplicate business operations.
- **Detection:** Replay path invokes live emails/payments indiscriminately.
- **Remediation and safeguards:** Separate projection replay from external effects; retain business dedupe.
- **Verification:** Replay historical events; read model rebuilds without resending effects.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-059 — Consumer Lag

- **Failure:** Consumers cannot process incoming messages fast enough.
- **Detection:** Consumer throughput below arrival rate or partition bottleneck.
- **Remediation and safeguards:** Measure oldest age and lag; scale within partition and downstream capacity.
- **Verification:** Sustain burst then recover; backlog drains within objective.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-060 — Message Schema Incompatibility

- **Failure:** New message formats break existing consumers.
- **Detection:** Producer removes required field or changes meaning.
- **Remediation and safeguards:** Version contracts; tolerant readers where safe; test old/new combinations.
- **Verification:** Run old consumer against new producer and reverse; compatible semantics preserved.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-061 — Eventual Consistency Window

- **Failure:** Different services temporarily represent different business states.
- **Detection:** UI or downstream assumes async update immediately visible.
- **Remediation and safeguards:** Expose pending state and freshness; authoritative validation for strict rules.
- **Verification:** Delay consumer; user sees pending not false completion; eventual convergence.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-062 — Ghost Event

- **Failure:** An event is published for a database transaction that subsequently rolls back.
- **Detection:** Event published before local commit.
- **Remediation and safeguards:** Persist event in transaction and publish only committed intent.
- **Verification:** Force rollback after event creation; no externally visible ghost event.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-063 — Missing Event

- **Failure:** A database transaction succeeds without publishing its corresponding event.
- **Detection:** Required event only sent after commit in request path.
- **Remediation and safeguards:** Atomic outbox or suitable committed-log CDC; monitor delivery age.
- **Verification:** Terminate immediately after commit; event eventually delivered.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-064 — Event Processing Loop

- **Failure:** Services trigger each other's events indefinitely.
- **Detection:** Consumers republish same trigger indefinitely.
- **Remediation and safeguards:** Define event ownership and causation; avoid feedback on no-op; bounded guard.
- **Verification:** Inject initiating event; chain terminates without suppressing valid subsequent events.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-065 — Premature Acknowledgment

- **Failure:** A consumer acknowledges a message before processing completes.
- **Detection:** Ack or offset commit precedes database commit.
- **Remediation and safeguards:** Acknowledge after durable outcome; handle duplicate delivery after commit.
- **Verification:** Crash before and after commit; no loss or repeated effect.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-066 — Event Notification Failure

- **Failure:** Subscribers miss notifications while offline.
- **Detection:** Ephemeral subscription used for required offline notification.
- **Remediation and safeguards:** Durable subscription or resumable log with retention and catch-up.
- **Verification:** Disconnect subscriber across publication; required notifications recovered.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-067 — Oversized Message

- **Failure:** Large message payloads overload the messaging infrastructure.
- **Detection:** Large payload approaches broker or consumer memory limits.
- **Remediation and safeguards:** Claim check with protected immutable object, checksum and retention tied to consumption.
- **Verification:** Send maximum payload and delayed retry; object remains available and verified.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-068 — Event Choreography Complexity

- **Failure:** Business workflows become difficult to track across multiple events.
- **Detection:** Distributed workflow has no visible progress or ownership.
- **Remediation and safeguards:** Persist orchestration state or explicit choreography contracts and tracing.
- **Verification:** Fail intermediate step; operator can locate and recover workflow.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.
