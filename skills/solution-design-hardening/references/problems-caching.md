# Caching - problem playbook

Signals are investigation leads, not findings. Confirm the business invariant and actual runtime guarantees. Tests are proposals until executed in an isolated environment. Use the simplest sufficient safeguard; do not introduce a pattern merely because it is listed.

## SDP-011 - Stale Data

- **Failure:** Cache contains an outdated version of database records.
- **Detection:** TTL exceeds freshness requirement or critical decisions use cached state.
- **Remediation and safeguards:** Specify freshness; invalidate after commit; authoritative recheck for critical decisions.
- **Verification:** Update source and measure visibility bound; stale display never authorizes invalid write.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-012 - Dual Write Problem

- **Failure:** Database update succeeds, but cache update fails, or vice versa.
- **Detection:** Cache and DB writes independently succeed.
- **Remediation and safeguards:** Commit DB first; durable invalidation intent if required; versioned cache protocol.
- **Verification:** Fail cache call after DB commit; eventual invalidation within declared bound.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-013 - Cache Stampede (Thundering Herd)

- **Failure:** Multiple requests simultaneously regenerate an expired cache entry.
- **Detection:** Every miss independently loads same expensive key.
- **Remediation and safeguards:** Coalesce by scoped key; bound waiters and fallback; coordinate across replicas if needed.
- **Verification:** Expire hot key under parallel load; measure bounded source fetches.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-014 - Cache Avalanche

- **Failure:** Large numbers of cached records expire simultaneously.
- **Detection:** Bulk population sets identical expiry timestamps.
- **Remediation and safeguards:** Jitter expiry and refresh gradually while respecting maximum staleness.
- **Verification:** Expire representative key population; source load stays within capacity.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-015 - Cache Penetration

- **Failure:** Requests for nonexistent records repeatedly reach the database.
- **Detection:** Repeated absent keys trigger expensive reads.
- **Remediation and safeguards:** Bound negative cache TTL and size; invalidate on create; rate limit adversarial misses.
- **Verification:** Flood absent keys then create one; load bounded and new record visible.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-016 - Cache Breakdown

- **Failure:** A frequently accessed cache key expires, overwhelming the database.
- **Detection:** Hot key refresh blocks or floods source.
- **Remediation and safeguards:** Singleflight and permitted stale serving with hard freshness bound.
- **Verification:** Expire busiest key with slow source; latency and load stay bounded.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-017 - Hot Key Problem

- **Failure:** One cache key receives disproportionately high traffic.
- **Detection:** One partition or cache key saturates server.
- **Remediation and safeguards:** Replicate immutable reads or use local cache with invalidation; avoid splitting authoritative counters unsafely.
- **Verification:** Skew load to one key; check throughput and freshness.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-018 - Cache Poisoning

- **Failure:** Incorrect or malicious data is stored in the cache.
- **Detection:** Cache key omits representation or trusted authorization dimensions.
- **Remediation and safeguards:** Canonicalize key inputs; validate cacheable responses; isolate private data.
- **Verification:** Vary host/header/tenant inputs; unauthorized or corrupted response never reused.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-019 - Cache Invalidation Race

- **Failure:** A concurrent request repopulates the cache with outdated data.
- **Detection:** Reader fetches old DB version then writes after invalidation.
- **Remediation and safeguards:** Use generation/version comparison atomic at cache or coordinate reads/writes; retain invalidation watermark.
- **Verification:** Pause old reader until writer commits and invalidates; old value cannot repopulate past bound.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-020 - Cold Cache Problem

- **Failure:** Application startup generates excessive database requests.
- **Detection:** All replicas start with empty caches and full traffic.
- **Remediation and safeguards:** Gradual admission, bounded warming, source capacity budget.
- **Verification:** Restart replicas together; database stays within connection and latency limits.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-021 - Cache Dependency Failure

- **Failure:** Cache outage causes database overload.
- **Detection:** Cache error falls back to unlimited database calls.
- **Remediation and safeguards:** Bound fallback concurrency; shed optional work; preserve authoritative correctness.
- **Verification:** Disable cache under load; DB remains healthy and overload responses are controlled.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-022 - Cache Memory Exhaustion

- **Failure:** Cached data consumes all available memory.
- **Detection:** Unbounded keys or large values consume cache memory.
- **Remediation and safeguards:** Set capacity, eviction and item limits; separate durable coordination data from evictable cache.
- **Verification:** Generate high-cardinality keys; memory bounded and critical state preserved.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.
