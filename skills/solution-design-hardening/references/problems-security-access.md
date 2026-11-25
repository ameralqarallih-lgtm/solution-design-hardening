# Authorization and business-flow security - problem playbook

Use [security assessment guidance](SECURITY-ASSESSMENT.md) and [standards mappings](SECURITY-STANDARDS.md). These are defensive investigation leads; confirm trust boundaries, reachability and effective controls. Use only authorized isolated tests with synthetic data.

## SDP-171 - Object-level authorization failure

- **Failure:** A valid caller accesses another principal's resource by identifier.
- **Detection:** Trace all object lookup, update, export and bulk paths including indirect references.
- **Remediation and safeguards:** Enforce ownership or explicit grants at the protected data operation; derive tenant from trusted context.
- **Verification:** Use two synthetic principals and test read, write, export and batch access across ownership; legitimate sharing works.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-172 - Function-level authorization failure

- **Failure:** A caller reaches privileged functions without required rights.
- **Detection:** Compare route and service policies for admin, alternative verbs, internal jobs and direct invocation.
- **Remediation and safeguards:** Deny by default; enforce permissions server-side at each privileged function and validate delegated authority.
- **Verification:** Exercise low and high privilege identities against each sensitive function, including alternate route.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-173 - Unsafe property binding

- **Failure:** Client-controlled fields alter protected attributes such as roles or owner IDs.
- **Detection:** Inspect generic model binding, patch handlers and ORM update objects.
- **Remediation and safeguards:** Allowlist writable properties by operation and policy; map explicit request types and derive server-owned fields.
- **Verification:** Submit synthetic protected and legitimate fields together; protected fields unchanged, permitted update works.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-174 - Unauthorized property disclosure

- **Failure:** An authorized object response exposes fields the caller cannot see.
- **Detection:** Trace serializers, projections, exports, error responses and GraphQL resolvers.
- **Remediation and safeguards:** Apply field-level read authorization and explicit projections; omit sensitive fields before serialization.
- **Verification:** Compare response schema for roles with different field grants, including export and nested data.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-175 - Fail-open authorization

- **Failure:** Policy errors or unavailable identity services permit access.
- **Detection:** Inspect exception handling, fallback policy, missing claims and defaults.
- **Remediation and safeguards:** Fail closed on protected operations when authority is uncertain; define separate public or degraded behavior.
- **Verification:** Inject policy timeout, malformed claim and unavailable service; protected actions denied and public routes work.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-176 - Privilege administration abuse

- **Failure:** Permission changes allow unauthorized escalation or bypass separation of duties.
- **Detection:** Inspect role/grant management, self-grant rules and delegated administration.
- **Remediation and safeguards:** Authorize grant creation and scope; enforce privilege ceilings and approval for high-impact grants; audit changes.
- **Verification:** Attempt synthetic self-escalation and out-of-scope grant; approved administrator grant succeeds.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-177 - Sensitive business-flow abuse

- **Failure:** Valid automated actions exhaust limited business resources or circumvent policy.
- **Detection:** Identify purchase, reservation, coupon and account workflows and per-principal business limits.
- **Remediation and safeguards:** Enforce business-specific quotas, state constraints and risk controls at authoritative boundary; avoid only IP limits.
- **Verification:** Simulate bounded concurrent legitimate-looking actions; verify quotas and accessibility of normal workflows.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-178 - Unsafe cross-origin trust

- **Failure:** Browser credentials or protected responses are exposed to untrusted origins.
- **Detection:** Inspect CORS allowlists, credential mode, origin reflection and proxy overrides.
- **Remediation and safeguards:** Allow only required origins, methods and headers; use explicit credential policy and keep server-side authorization.
- **Verification:** Verify trusted and untrusted synthetic origins with preflight and actual credentialed request.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

