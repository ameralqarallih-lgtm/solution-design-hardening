# Redis

Related baseline problems: SDP-011, SDP-013, SDP-019, SDP-046, SDP-120.

## Detection
Inspect GET/SET races, cache key scope, TTL distribution, lock expiry, eviction policy and fallback concurrency.

## Implementation
Use tenant-scoped keys and atomic Lua or equivalent conditional operations for generation-checked cache fills. Preserve invalidation watermarks for the full race horizon; bound fallback and coalesce misses. Use fencing enforced by the authoritative resource for lease-based writes.

## Pitfalls / counterexamples
SET NX PX alone does not fence expired owners; eviction can remove a watermark; Redis Cluster multi-key scripts require compatible hash slots. Cache TTL is not an authorization guarantee.

## Verification
Pause a reader after database read, invalidate with a newer generation, resume and assert stale fill rejected; test cache loss and concurrent replicas.

## Upstream reference
[Official documentation](https://redis.io/docs/latest/develop/). Confirm installed versions and provider capabilities before selecting APIs. This is guidance, not a tested integration.
