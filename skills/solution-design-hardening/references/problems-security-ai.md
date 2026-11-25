# AI and agentic application security — problem playbook

Use [security assessment guidance](SECURITY-ASSESSMENT.md) and [standards mappings](SECURITY-STANDARDS.md). These are defensive investigation leads; confirm trust boundaries, reachability and effective controls. Use only authorized isolated tests with synthetic data.

## SDP-226 — Prompt injection trust-boundary failure

- **Failure:** Untrusted user or retrieved content influences privileged agent behavior.
- **Detection:** Trace prompts, retrieval, tool routing and policy enforcement; distinguish content from authority.
- **Remediation and safeguards:** Treat content as data; enforce independent tool authorization, constrained actions and output validation outside model; no prompt-only guarantee.
- **Verification:** Use harmless synthetic conflicting instruction; verify prohibited mock action is denied by external policy.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-227 — Excessive agent authority

- **Failure:** Agent credentials or tools exceed the requested task scope.
- **Detection:** Inspect tool permissions, delegated identity, approval gates and execution context.
- **Remediation and safeguards:** Use scoped tools, least privilege, explicit authorization and confirmation for high-impact actions; enforce in host.
- **Verification:** With mock tools request out-of-scope write; deny without side effect; authorized bounded action succeeds.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-228 — RAG authorization bypass

- **Failure:** Retrieval returns documents the caller cannot access.
- **Detection:** Trace index ingestion ACLs, retrieval filters, caches and source permission changes.
- **Remediation and safeguards:** Enforce document-level authorization at retrieval and revalidate access where needed; scope indexes/caches by policy.
- **Verification:** Use two synthetic principals and private/public documents; no unauthorized content in retrieval or generated result.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-229 — Agent memory isolation failure

- **Failure:** Persistent memory leaks data or instructions across tenant or task boundaries.
- **Detection:** Inspect memory keys, ownership, retention and retrieval authorization; cross-reference SDP-120.
- **Remediation and safeguards:** Scope memory to authorized identity/tenant and purpose, validate provenance and support deletion; avoid treating memory as trusted authority.
- **Verification:** Store synthetic private marker; other principal cannot retrieve it; deletion respects policy.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-230 — Knowledge and model input poisoning

- **Failure:** Untrusted ingestion corrupts knowledge or model inputs used for decisions.
- **Detection:** Inspect ingestion source identity, approvals, provenance and change/recovery controls.
- **Remediation and safeguards:** Validate source and content, track provenance, quarantine untrusted updates and provide version rollback.
- **Verification:** Insert synthetic unapproved document; verify it is quarantined and approved version remains available.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-231 — Unsafe model output execution

- **Failure:** Generated text becomes executable commands, code or privileged data without validation.
- **Detection:** Trace model output into interpreters, rendering, queries and tools.
- **Remediation and safeguards:** Treat outputs as untrusted data, schema-validate, use constrained APIs and sandbox approved execution; require authority separately.
- **Verification:** Feed harmless malformed output to mock executor; verify rejection and no execution outside sandbox.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-232 — Unbounded agent execution and cost

- **Failure:** Agent loops or tool fan-out exhaust budgets or trigger repeated effects.
- **Detection:** Inspect recursion, tool-call count, deadlines, token and financial quotas.
- **Remediation and safeguards:** Enforce host-level budgets, cancellation, concurrency limits and idempotent effects; stop safely and report incomplete work.
- **Verification:** Use mock loop and failing tool; verify hard limits and no additional external effects after stop.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-233 — Untrusted tool or MCP integration

- **Failure:** A tool definition or result expands authority or sends data to unintended party.
- **Detection:** Inspect tool discovery, provenance, server trust, scoped credentials and data routing.
- **Remediation and safeguards:** Allowlist trusted servers/tools, verify identity and contracts, constrain egress and permissions; treat descriptions/results as untrusted.
- **Verification:** Use mock untrusted tool metadata and result; no new permission or unauthorized data transmission occurs.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-234 — AI sensitive output disclosure

- **Failure:** Model responses reveal sensitive information from context, tools or memory.
- **Detection:** Map input data classification, model provider, retrieval, output and telemetry paths.
- **Remediation and safeguards:** Minimize sensitive inputs, enforce retrieval permissions, validate output and apply provider/data retention policy; never rely only on filtering.
- **Verification:** Use synthetic confidential marker across roles and tool results; unauthorized output absent and allowed use preserved.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-235 — Agent-to-agent trust failure

- **Failure:** Peer messages are accepted as authoritative instructions without verified identity or delegation.
- **Detection:** Inspect agent protocol, sender identity, message integrity and authority propagation.
- **Remediation and safeguards:** Authenticate peers, validate delegated scope and message schema, and independently authorize requested effects.
- **Verification:** Use mock peer with wrong identity or scope; reject action; legitimate delegated request succeeds.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

