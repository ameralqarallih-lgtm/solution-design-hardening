# Api — problem playbook

Signals are investigation leads, not findings. Confirm the business invariant and actual runtime guarantees. Tests are proposals until executed in an isolated environment. Use the simplest sufficient safeguard; do not introduce a pattern merely because it is listed.

## SDP-069 — Duplicate API Submission

- **Failure:** Users submit the same request multiple times.
- **Detection:** Repeated POST creates multiple records.
- **Remediation and safeguards:** Scoped idempotency or durable business uniqueness; request fingerprint.
- **Verification:** Repeat and concurrently submit same operation; one record/effect.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-070 — Timeout Ambiguity

- **Failure:** A client cannot determine whether a timed-out operation completed.
- **Detection:** Timeout interpreted as failure and new operation created.
- **Remediation and safeguards:** Return stable operation ID and status endpoint; reconcile uncertain result.
- **Verification:** Drop response after commit; query resolves original result.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-071 — Long-Running Request

- **Failure:** Operations exceed HTTP or gateway timeout limits.
- **Detection:** HTTP request holds resources through long job.
- **Remediation and safeguards:** Durable enqueue and 202/status contract; idempotent submit and worker.
- **Verification:** Disconnect client and restart API; job completes or reports durable failure.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-072 — Concurrent API Updates

- **Failure:** Multiple clients overwrite the same resource.
- **Detection:** PUT/PATCH ignores resource version.
- **Remediation and safeguards:** ETag/If-Match or equivalent compare-and-swap; surface conflict.
- **Verification:** Two clients edit same version; second gets conflict instead of silent overwrite.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-073 — API Request Flooding

- **Failure:** Excessive requests overwhelm backend services.
- **Detection:** No bounded request admission or per-identity quotas.
- **Remediation and safeguards:** Rate and concurrency limits at relevant scope; explicit retry guidance.
- **Verification:** Burst per identity and across identities; capacity and fairness maintained.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-074 — N+1 Request Problem

- **Failure:** Retrieving a collection generates an additional request for every item.
- **Detection:** Loop issues one query/RPC per item.
- **Remediation and safeguards:** Batch or eager load with bounded page size; inspect query counts.
- **Verification:** Increase item count; calls scale by batches not individual items.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-075 — Overfetching

- **Failure:** APIs return unnecessary data.
- **Detection:** Endpoint returns unused or sensitive fields by default.
- **Remediation and safeguards:** Projection and explicit authorized response contract.
- **Verification:** Compare payload size and fields for representative clients; no restricted fields.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-076 — Underfetching

- **Failure:** Clients require multiple API calls to retrieve related information.
- **Detection:** Client must issue many sequential dependent requests.
- **Remediation and safeguards:** Compose or batch required data with bounded fan-out.
- **Verification:** Measure network calls and latency; failure semantics remain explicit.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-077 — Pagination Drift

- **Failure:** Records are skipped or duplicated when data changes between page requests.
- **Detection:** Offset pages shift under concurrent insert/delete.
- **Remediation and safeguards:** Stable unique ordering and keyset cursor; snapshot if complete enumeration required.
- **Verification:** Insert/delete between pages; no unintended duplicates or omissions under contract.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-078 — Request Replay Attack

- **Failure:** Previously valid requests are maliciously resubmitted.
- **Detection:** Signed or authenticated action can be replayed.
- **Remediation and safeguards:** Bind signature to method/body/context; enforce nonce/window and durable uniqueness where needed.
- **Verification:** Replay valid request within and outside window; unauthorized repeat rejected.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-079 — Partial Bulk Operation Failure

- **Failure:** Some items succeed while others fail.
- **Detection:** Batch retries repeat successful items or hides partial results.
- **Remediation and safeguards:** Item-level durable identities and status; explicit atomic or partial contract.
- **Verification:** Fail midway then retry batch; successful items not repeated.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-080 — API Fan-Out Failure

- **Failure:** An aggregated response fails because one dependency is unavailable.
- **Detection:** Parallel aggregation fails whole response on optional dependency.
- **Remediation and safeguards:** Classify required/optional dependencies; bound fan-out and return explicit partial state.
- **Verification:** Fail optional and mandatory dependencies separately; contract matches policy.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.
