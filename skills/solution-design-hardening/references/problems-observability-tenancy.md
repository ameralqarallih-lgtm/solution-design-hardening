# Observability Tenancy — problem playbook

Signals are investigation leads, not findings. Confirm the business invariant and actual runtime guarantees. Tests are proposals until executed in an isolated environment. Use the simplest sufficient safeguard; do not introduce a pattern merely because it is listed.

## SDP-146 — Metrics cardinality explosion

- **Failure:** Unbounded labels overload monitoring.
- **Detection:** Unbounded unique labels create metrics cardinality explosion.
- **Remediation and safeguards:** Use bounded label dimensions; put IDs in logs/traces with retention.
- **Verification:** Generate unique request IDs; metric series count remains bounded.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-147 — Telemetry backpressure

- **Failure:** Unavailable exporter blocks application.
- **Detection:** Synchronous telemetry export blocks business requests or buffers indefinitely.
- **Remediation and safeguards:** Use bounded async export and explicit drop policy; isolate mandatory audit trail.
- **Verification:** Disable telemetry backend; service remains available and loss observable.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-148 — Broken trace propagation

- **Failure:** Async work loses causal context.
- **Detection:** Trace context dropped across asynchronous boundaries or reused incorrectly.
- **Remediation and safeguards:** Propagate trace/correlation and causation context; validate trust boundaries.
- **Verification:** Follow request through broker and worker; trace links correct without cross-request mix.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-149 — Tenant migration race

- **Failure:** Writes lost during tenant relocation.
- **Detection:** Tenant-specific data moves during active writes with no cutover protocol.
- **Remediation and safeguards:** Use versioned routing, checkpointed copy and fenced cutover; reconcile.
- **Verification:** Write during tenant move; all acknowledged changes present in new location.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-150 — Background tenant context loss

- **Failure:** Worker applies operation to wrong tenant.
- **Detection:** Shared bulk operation ignores tenant context on background execution.
- **Remediation and safeguards:** Persist tenant identity and reauthorize scope; enforce partition/row filters.
- **Verification:** Run batch for two tenants with matching IDs; effects isolated.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.
