# Data protection and cryptography - problem playbook

Use [security assessment guidance](SECURITY-ASSESSMENT.md) and [standards mappings](SECURITY-STANDARDS.md). These are defensive investigation leads; confirm trust boundaries, reachability and effective controls. Use only authorized isolated tests with synthetic data.

## SDP-193 - Hardcoded secrets

- **Failure:** Reusable credentials are embedded in code, images or defaults.
- **Detection:** Inspect references to secret sources, build layers and secret-scan results without exposing values.
- **Remediation and safeguards:** Use secret manager or injected scoped credentials; revoke exposed secrets and remove insecure defaults.
- **Verification:** Use synthetic credential marker and approved secret scanning; verify startup fails safely when required secret absent.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-194 - Secret exposure in artifacts and history

- **Failure:** Credentials persist in repository history, package or build output.
- **Detection:** Inspect authorized secret-scanning metadata and artifact contents using redaction.
- **Remediation and safeguards:** Revoke and rotate first; remove exposure from artifacts/history with coordinated owner approval; prevent recurrence.
- **Verification:** Verify old synthetic credential no longer authenticates and new artifacts contain no test marker.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-195 - Unprotected sensitive storage

- **Failure:** Sensitive data or snapshots are readable outside intended access boundary.
- **Detection:** Map data classification, storage, replicas, backups and key access; inspect effective encryption and ACLs.
- **Remediation and safeguards:** Apply appropriate encryption and restricted access, separate key authority and minimize retained data.
- **Verification:** In test storage verify access by unauthorized identity denied, encryption configured and authorized restore works.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-196 - Cleartext sensitive transport

- **Failure:** Sensitive data or credentials traverse untrusted links without protection.
- **Detection:** Map external and internal hops including proxy termination and broker/DB links.
- **Remediation and safeguards:** Use authenticated encryption in transit for relevant trust boundaries; enforce transport policy and secure downgrade handling.
- **Verification:** Inspect negotiated protocols in lab; reject disallowed plaintext and verify permitted TLS path.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-197 - Disabled TLS certificate validation

- **Failure:** A client trusts an unauthenticated endpoint.
- **Detection:** Inspect certificate callbacks, verify flags, trust stores and hostname checks.
- **Remediation and safeguards:** Validate certificate chain and hostname with approved trust anchors; provision internal CA rather than disabling checks.
- **Verification:** Use test certificates with wrong hostname and untrusted CA; reject both; intended certificate succeeds.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-198 - Weak password storage

- **Failure:** Password records can be recovered cheaply after a breach.
- **Detection:** Inspect password hashing API, cost parameters, salts and migration path without real credentials.
- **Remediation and safeguards:** Use maintained password hashing with suitable cost and unique salts; migrate legacy hashes safely.
- **Verification:** Verify synthetic password records differ by salt, cost is configured, and legacy migration preserves login.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-199 - Unsafe cryptographic primitive or mode

- **Failure:** Encryption or signatures do not provide the required security property.
- **Detection:** Inspect algorithm selection, mode, integrity, key sizes and protocol library use.
- **Remediation and safeguards:** Use approved authenticated encryption/signature protocols and reviewed libraries; avoid custom cryptography.
- **Verification:** Use known-answer tests and synthetic tampered ciphertext; reject tampering and verify interoperability.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-200 - Cryptographic nonce reuse

- **Failure:** A key is used with repeated nonces where uniqueness is required.
- **Detection:** Inspect nonce generation, counters, persistence and multi-writer/restart behavior.
- **Remediation and safeguards:** Use library-supported nonce policy appropriate to algorithm; ensure uniqueness per key across replicas and recovery.
- **Verification:** Test restart and concurrent encryption with synthetic keys; verify nonce policy and rotation limits.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-201 - Predictable security tokens

- **Failure:** Security-sensitive identifiers derive from predictable randomness.
- **Detection:** Inspect token, reset-link and nonce generation for noncryptographic random APIs.
- **Remediation and safeguards:** Use cryptographically secure randomness of appropriate entropy; do not use timestamps or ordinary PRNG for secrets.
- **Verification:** Inspect generation API and test expected size, uniqueness and lifecycle; statistical tests alone do not prove security.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-202 - Key lifecycle and rotation failure

- **Failure:** Expired or compromised keys remain trusted, or rotation breaks availability.
- **Detection:** Inspect key IDs, key overlap, retirement policy, re-encryption and emergency revocation.
- **Remediation and safeguards:** Use versioned keys, bounded overlap, rotation and revocation procedures; protect historical decrypt needs separately.
- **Verification:** Rotate synthetic keys across mixed versions; verify new writes, authorized old reads and revoked-signature rejection.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-203 - Sensitive data lifecycle mismatch

- **Failure:** Data survives beyond deletion or retention policy in copies or derived stores.
- **Detection:** Trace replicas, caches, analytics, exports, backups and legal holds; cross-reference SDP-156.
- **Remediation and safeguards:** Minimize copies, enforce retention and deletion propagation subject to documented legal holds and restore controls.
- **Verification:** Delete synthetic subject data; verify each applicable copy or documented retention exception, including restore behavior.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

