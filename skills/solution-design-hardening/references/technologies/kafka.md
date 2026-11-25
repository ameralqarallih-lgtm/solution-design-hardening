# Apache Kafka

Related baseline problems: SDP-024, SDP-056, SDP-058, SDP-059, SDP-060, SDP-152.

## Detection
Inspect partition keys, offset commit ordering, consumer rebalances, schema compatibility and producer transaction settings.

## Implementation
Key by aggregate where order matters; validate sequence and detect gaps. For database effects, commit durable inbox and business state before offset advancement. Use Kafka transactions for supported Kafka-to-Kafka boundaries only.

## Pitfalls / counterexamples
Kafka exactly-once semantics do not make arbitrary external database or payment effects exactly once. Committing a later offset can skip earlier unfinished records.

## Verification
Force rebalance and crash between database commit and offset commit; verify duplicate-safe replay and no skipped offsets; test incompatible schemas.

## Upstream reference
[Official documentation](https://kafka.apache.org/documentation/). Confirm installed versions and provider capabilities before selecting APIs. This is guidance, not a tested integration.
