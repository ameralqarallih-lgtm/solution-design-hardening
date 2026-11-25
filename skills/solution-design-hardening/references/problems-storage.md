# Storage - problem playbook

Signals are investigation leads, not findings. Confirm the business invariant and actual runtime guarantees. Tests are proposals until executed in an isolated environment. Use the simplest sufficient safeguard; do not introduce a pattern merely because it is listed.

## SDP-092 - Orphaned File

- **Failure:** A file is uploaded successfully, but its database record fails to save.
- **Detection:** Object upload succeeds before metadata failure.
- **Remediation and safeguards:** Stage with ownership and expiry; reconcile unreferenced objects safely.
- **Verification:** Fail DB write after upload; orphan eventually reclaimed without deleting live object.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-093 - Missing File

- **Failure:** A database record references a file that was never uploaded.
- **Detection:** Metadata visible before object durable or verified.
- **Remediation and safeguards:** Pending state and verification before publish; repair missing references.
- **Verification:** Fail upload after metadata insert; no ready record points to missing object.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-094 - Dual Write (Database + Object Storage)

- **Failure:** Database metadata and file storage become inconsistent.
- **Detection:** DB and object operations assumed one transaction.
- **Remediation and safeguards:** Explicit staged lifecycle, idempotent finalize and reconciliation.
- **Verification:** Fail every boundary; live metadata and object converge safely.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-095 - Concurrent File Modification

- **Failure:** Multiple users overwrite the same file.
- **Detection:** Unconditional overwrite of shared object key.
- **Remediation and safeguards:** Immutable versioned key or conditional write on expected version.
- **Verification:** Two writers update same object; no silent overwrite.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-096 - Incomplete File Upload

- **Failure:** Network interruption leaves a partially uploaded file.
- **Detection:** Partial upload exposed as complete or abandoned indefinitely.
- **Remediation and safeguards:** Multipart completion verification, resumable state and abort cleanup.
- **Verification:** Interrupt upload then resume; only complete verified object becomes visible.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-097 - File Corruption

- **Failure:** Stored content differs from the original file.
- **Detection:** No end-to-end integrity check or assumes ETag is checksum.
- **Remediation and safeguards:** Use explicit checksum appropriate to provider and verify on transfer/restore.
- **Verification:** Corrupt payload; integrity check rejects or flags it.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-098 - Duplicate File Storage

- **Failure:** Identical files consume unnecessary storage.
- **Detection:** Dedup deletes shared object on one reference removal.
- **Remediation and safeguards:** Content identity with tenant/privacy scope; reference lifecycle and race-safe GC.
- **Verification:** Two records reference same content; delete one; other remains readable.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-099 - Unauthorized File Access

- **Failure:** Users access files belonging to other users or tenants.
- **Detection:** Object URL or key accepted without authorization.
- **Remediation and safeguards:** Authorize resource/tenant on access; short scoped signed URL; private storage.
- **Verification:** Request another tenant's key and expired URL; access denied as required.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.

## SDP-100 - Deleted File Recovery

- **Failure:** Accidental deletion permanently removes important documents.
- **Detection:** Permanent deletion without retention or restore verification.
- **Remediation and safeguards:** Versioning/soft delete consistent with retention/privacy; tested recovery.
- **Verification:** Delete object and restore within policy; verify content and access controls.
- **Decision:** Confirm reachability, existing constraints and the required guarantee before reporting a defect; document any remaining uncertainty.
