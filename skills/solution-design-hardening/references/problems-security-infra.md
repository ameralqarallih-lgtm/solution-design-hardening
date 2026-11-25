# Distributed and infrastructure security - problem playbook

Use [security assessment guidance](SECURITY-ASSESSMENT.md) and [standards mappings](SECURITY-STANDARDS.md). These are defensive investigation leads; confirm trust boundaries, reachability and effective controls. Use only authorized isolated tests with synthetic data.

## SDP-204 - Unauthenticated internal service

- **Failure:** An internal endpoint trusts network location instead of identity.
- **Detection:** Trace direct service access bypassing gateway, internal DNS and alternative ports.
- **Remediation and safeguards:** Authenticate and authorize service calls at the protected boundary; use network controls as defense in depth.
- **Verification:** Use isolated clients with wrong or absent identity; denied even inside network, approved client succeeds.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-205 - Unrestricted network reachability

- **Failure:** A compromised workload can reach unrelated sensitive services.
- **Detection:** Inspect ingress/egress policies, firewall defaults and actual topology.
- **Remediation and safeguards:** Allow required flows explicitly, separate trust zones and verify policy enforcement by runtime/network provider.
- **Verification:** From disposable workloads verify allowed and denied flows; avoid probing production networks.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-206 - Unauthorized message operations

- **Failure:** A client can publish, consume or administer unrelated queues or topics.
- **Detection:** Inspect broker identities, namespace ACLs and per-operation grants.
- **Remediation and safeguards:** Separate producer/consumer identities and scope permissions to required destinations and operations.
- **Verification:** Use disposable broker accounts; unauthorized publish/consume/admin operations denied.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-207 - Message integrity and trust failure

- **Failure:** A service accepts unauthenticated or altered messages as authoritative.
- **Detection:** Inspect message provenance, broker trust and integrity across forwarding boundaries.
- **Remediation and safeguards:** Authenticate transport and publisher where required; validate envelope, schema and authorization; sign payloads when end-to-end integrity needed.
- **Verification:** Use synthetic altered and wrong-provenance messages; verify no business effect and controlled quarantine.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-208 - Excessive workload privileges

- **Failure:** Runtime permissions exceed application needs, enabling unintended access.
- **Detection:** Inspect service accounts, container user, capabilities, host mounts and cloud IAM.
- **Remediation and safeguards:** Use least privilege, non-root where feasible, minimal capabilities and restricted mounts; document justified exceptions.
- **Verification:** Verify deployed test policy and denial of unneeded operation without disrupting legitimate workload.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-209 - Exposed management surface

- **Failure:** Administrative or debug endpoints are reachable by unintended clients.
- **Detection:** Inventory management, metrics, debug and control-plane endpoints and access paths.
- **Remediation and safeguards:** Restrict network and identity access, disable unnecessary endpoints, separate administration plane.
- **Verification:** Verify unauthorized lab client cannot access management endpoints; authorized operator can.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-210 - Insecure deployment defaults

- **Failure:** Unsafe defaults remain enabled in deployed environments.
- **Detection:** Inspect effective configuration for debug mode, default accounts, permissive policies and omitted security settings.
- **Remediation and safeguards:** Define secure baseline, validate on startup or admission and prevent unsafe production defaults.
- **Verification:** Test configuration variants; unsafe production profile rejected while explicit isolated development mode works.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-211 - Cross-environment credential reuse

- **Failure:** Development or staging credentials grant production access.
- **Detection:** Inspect issuer, secret scope, deployment identities and environment mapping.
- **Remediation and safeguards:** Separate accounts, trust roots and credential scopes by environment; restrict promotion workflows.
- **Verification:** Use synthetic staging identity against production-like policy; deny; intended environment identity allowed.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-212 - Stale API inventory

- **Failure:** Deprecated or shadow endpoints escape security policy and patching.
- **Detection:** Compare deployed routes, gateway inventory, docs and ownership.
- **Remediation and safeguards:** Maintain versioned inventory and retirement controls; apply security policy consistently to all reachable versions.
- **Verification:** Compare authorized route export to inventory; verify retired test endpoint is unreachable.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

