# Injection and untrusted content — problem playbook

Use [security assessment guidance](SECURITY-ASSESSMENT.md) and [standards mappings](SECURITY-STANDARDS.md). These are defensive investigation leads; confirm trust boundaries, reachability and effective controls. Use only authorized isolated tests with synthetic data.

## SDP-179 — SQL injection

- **Failure:** Untrusted values alter database query semantics.
- **Detection:** Trace request data into raw SQL, interpolation and dynamic identifiers; ORM alone is not proof.
- **Remediation and safeguards:** Bind parameters for values and allowlist identifiers; avoid constructing SQL from untrusted strings.
- **Verification:** Use synthetic metacharacter inputs and verify they remain data; inspect query binding and permitted sorting.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-180 — NoSQL query injection

- **Failure:** Untrusted structures become database operators or filters.
- **Detection:** Trace request objects into document queries and aggregation operators.
- **Remediation and safeguards:** Validate typed inputs, construct filters server-side and allowlist permitted operators.
- **Verification:** Pass unexpected nested operators as synthetic input; reject without widening results.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-181 — Command injection

- **Failure:** Untrusted values alter operating-system command execution.
- **Detection:** Trace input into shell execution, argument construction and interpreter calls.
- **Remediation and safeguards:** Avoid shell execution; use constrained direct APIs and validated arguments, with least privilege.
- **Verification:** Mock execution and verify untrusted text remains one inert argument or is rejected; no external commands needed.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-182 — Cross-site scripting

- **Failure:** Untrusted content is interpreted as active browser code.
- **Detection:** Inspect HTML rendering, unsafe DOM sinks, rich text and templating contexts.
- **Remediation and safeguards:** Use context-aware output encoding and vetted sanitization for intended HTML; CSP is defense in depth.
- **Verification:** Render synthetic marker content in browser test; verify inert text and permitted formatting.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-183 — Server-side request forgery

- **Failure:** Untrusted destinations cause server requests across restricted network boundaries.
- **Detection:** Trace URLs, redirects, DNS resolution and user-controlled connectors; inspect egress policy.
- **Remediation and safeguards:** Use approved destinations or isolated fetch service, enforce address policy after resolution and redirects, bound response size/time.
- **Verification:** Use local fake allowed and denied destinations; verify denied requests never reach the target, including redirects.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-184 — Cross-site request forgery

- **Failure:** A browser sends an authenticated state change without user intent.
- **Detection:** Identify ambient cookie credentials and state-changing routes, including GET and alternate methods.
- **Remediation and safeguards:** Use anti-forgery controls appropriate to credential mode, origin validation and safe HTTP semantics; do not rely solely on CORS.
- **Verification:** Submit a synthetic cross-origin state change with ambient session; reject; intended request succeeds.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-185 — Unsafe XML processing

- **Failure:** XML parsing resolves external resources or expands input unexpectedly.
- **Detection:** Inspect parser options, DTD/entity resolution and size/depth limits.
- **Remediation and safeguards:** Disable unneeded external entities and DTDs; use safe parser configuration and resource limits.
- **Verification:** Use isolated parser tests with fake resolver and bounded input; external resolution never occurs.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-186 — Unsafe deserialization

- **Failure:** Untrusted serialized data constructs unexpected objects or executes behavior.
- **Detection:** Trace untrusted payloads into native object deserializers and polymorphic type selection.
- **Remediation and safeguards:** Use data-only serialization and explicit schema/type allowlists; verify integrity when appropriate.
- **Verification:** Supply unsupported synthetic type and malformed data; reject without invoking constructors or side effects.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-187 — Path traversal and archive extraction

- **Failure:** Untrusted paths escape authorized directories or overwrite unrelated files.
- **Detection:** Inspect joins, canonicalization, symlinks, archive entry paths and race windows.
- **Remediation and safeguards:** Use trusted roots, safe path resolution and symlink-aware filesystem primitives; reject unsafe archive entries.
- **Verification:** In temporary directories test outside-root and symlink cases; confirm permitted files still work.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-188 — Template injection

- **Failure:** Untrusted content is interpreted as template source.
- **Detection:** Trace user content into template compilation or dynamic expression evaluation.
- **Remediation and safeguards:** Use trusted templates with data-only bindings; sandbox only as additional control.
- **Verification:** Render synthetic expression-like input as text; confirm no interpreter action occurs.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-189 — Unsafe redirect

- **Failure:** Untrusted destination redirects users outside intended trust boundary.
- **Detection:** Inspect return URLs, login callbacks and redirect handling.
- **Remediation and safeguards:** Use local paths or explicit trusted destinations; normalize and validate before redirecting.
- **Verification:** Verify external and malformed destination rejected; legitimate local return works.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-190 — HTTP parser disagreement

- **Failure:** Intermediaries disagree on request boundaries or normalization.
- **Detection:** Review gateway/backend HTTP versions, framing validation and normalization contracts.
- **Remediation and safeguards:** Reject ambiguous framing at ingress, align parser behavior and patch intermediaries.
- **Verification:** Use authorized isolated proxy fixtures with malformed framing; verify rejection and no downstream request ambiguity.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-191 — Unsafe file upload

- **Failure:** Untrusted files become executable, public or resource-exhausting content.
- **Detection:** Inspect content validation, object naming, serving headers, storage isolation and scan workflow.
- **Remediation and safeguards:** Allowlist business-required types, verify content, enforce limits, store outside executable paths and quarantine when needed.
- **Verification:** Use benign mismatched-type and oversized fixtures; verify no execution or public access before approval.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-192 — Unsafe upstream API consumption

- **Failure:** Third-party responses bypass validation or inject unsafe data into local actions.
- **Detection:** Trace external response parsing, schema validation, redirects and trusted fields.
- **Remediation and safeguards:** Validate external data against explicit contracts, bound resources and enforce local authorization before effects.
- **Verification:** Mock malformed and out-of-policy upstream data; verify rejected or quarantined without state corruption.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

