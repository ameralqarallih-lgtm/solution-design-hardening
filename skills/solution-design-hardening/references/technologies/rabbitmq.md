# RabbitMQ

Related baseline problems: SDP-023, SDP-024, SDP-054, SDP-055, SDP-057, SDP-065, SDP-115.

## Detection
Inspect auto-ack, ack ordering, publisher confirms, unroutable messages, queue durability, prefetch and redrive.

## Implementation
Persist intent before publishing; use confirms and handle unroutable messages explicitly. Commit inbox and business mutation before ack; use stable message IDs and bounded prefetch/retries. Quarantine poison messages and authorize redrive.

## Pitfalls / counterexamples
Publisher confirms do not prove consumer processing. Durable queue declarations alone do not establish message persistence or routing. Redelivery is normal.

## Verification
Kill relay after broker acceptance but before marking sent; kill consumer after commit but before ack; verify one business effect and eventual progress.

## Upstream reference
[Official documentation](https://www.rabbitmq.com/docs/confirms). Confirm installed versions and provider capabilities before selecting APIs. This is guidance, not a tested integration.
