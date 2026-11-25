# Multi Region — problem playbook

Signals are investigation leads, not findings. Confirm the business invariant and actual runtime guarantees. Tests are proposals until executed in an isolated environment. Use the simplest sufficient safeguard; do not introduce a pattern merely because it is listed.

## SDP-125 — Multi-region failover data loss

- **Failure:** Async replication loses acknowledged writes on promotion.
- **Detection:** Async cross-region replica promoted before required commits arrive.
- **Remediation and safeguards:** Define RPO and promotion watermark; fence former writer; reconcile missing transactions.
- **Verification:** Delay replication and lose primary; measure actual loss against RPO.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-126 — Stale regional writer routing

- **Failure:** Clients continue writing through old regional connections.
- **Detection:** Region failover relies on stale DNS/client connections to previous writer.
- **Remediation and safeguards:** Use authority epoch at protected resource; drain stale endpoints and verify routing.
- **Verification:** Keep old connection alive during promotion; stale writes rejected.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-127 — Unsafe failback

- **Failure:** Returning region overwrites newer active-region state.
- **Detection:** Failback copies older region snapshot over newer active data.
- **Remediation and safeguards:** Resynchronize from active authority; verify divergence and cutover checkpoint.
- **Verification:** Write after failover then fail back; all accepted writes retained.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-128 — Quorum loss

- **Failure:** Minority continues unsafe authoritative writes.
- **Detection:** Quorum lost but minority elects leader or accepts authoritative writes.
- **Remediation and safeguards:** Use established consensus implementation; stop unsafe writes without quorum.
- **Verification:** Remove majority; no conflicting commit; restore quorum and progress.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-129 — Leader flapping

- **Failure:** Repeated elections prevent progress.
- **Detection:** Leadership rapidly changes due to short timeouts or overload.
- **Remediation and safeguards:** Tune election and heartbeat to measured delays; isolate control traffic; avoid unsafe custom consensus.
- **Verification:** Inject latency and pauses; leadership stabilizes without multiple writers.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-130 — Lease renewal starvation

- **Failure:** Renewal cannot execute under workload saturation.
- **Detection:** Lease renewals depend on blocked worker pool.
- **Remediation and safeguards:** Isolate renewal resources; check authority at effect; stop on uncertain renewal.
- **Verification:** Starve worker pool; expired holder cannot commit.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.
