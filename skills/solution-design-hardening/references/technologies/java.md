# Java / Spring / JPA

Related baseline problems: SDP-004, SDP-023, SDP-029, SDP-039, SDP-142.

## Detection
Inspect @Transactional proxy boundaries, self-invocation, rollback rules, async executors, JPA version fields and connection pools.

## Implementation
Keep transaction ownership in an invoked service boundary; use @Version or database constraints and conditional updates. Persist outbox rows with business state. Explicitly configure rollback for relevant checked exceptions; use bounded executors and a single retry owner.

## Pitfalls / counterexamples
A self-invoked transactional method may bypass proxy advice; flush is not commit; retries must start a fresh transaction when the previous transaction is invalid.

## Verification
Use separate transactions and real database integration tests; force rollback and process interruption; assert business and outbox rows are atomic.

## Upstream reference
[Official documentation](https://docs.spring.io/spring-framework/reference/data-access/transaction.html). Confirm installed versions and provider capabilities before selecting APIs. This is guidance, not a tested integration.
