# Adaptive security capability discovery

These capability families extend the existing [identity and security profile](technology/capabilities/identity-and-security.md). They are not product support lists or assertions that a particular feature is enabled. Apply [version verification](technology/VERSION-VERIFICATION.md) to each boundary and each deployment. Use relevant playbooks for detailed safeguards.

| Capability family | Discover and verify | Evidence / isolated verification |
|---|---|---|
| Identity and session | Authentication authority, token type, issuer, audience, session rotation, MFA, recovery and revocation guarantees | Resolved protocol/library version, provider policy, synthetic identity and revocation tests |
| Policy and delegated authority | Policy decisions, enforcement point, tenant/ownership scope, service and background identity, default/failure behavior | Effective grants and actual operation paths; positive and negative actor tests plus policy outage |
| Input and execution isolation | Parser/serializer/renderer semantics, data-to-code boundaries, network fetch policy, upload lifecycle | Installed library and configuration; inert marker tests, mock destination and bounded resources |
| Cryptography and data lifecycle | Data classes, trust roots, key roles, algorithms, randomness, rotation, revocation, retention, backup access | Version-specific approved primitives, effective policy, synthetic key rotation, wrong identity and authorized restore |
| Workload and network security | Runtime identity, service-to-service auth, egress/ingress, broker ACLs, container privileges, management surfaces | Effective runtime policies; allowed and denied synthetic workload operations, not merely manifest intent |
| Supply chain | Dependency resolution, registry trust, artifact digest/provenance, build permissions, vulnerability management | Resolved inventory, verified attestations, isolated CI permissions and advisory applicability |
| Operational security | Audit intent and retention, access to diagnostics, alert delivery, drift and emergency credential response | Synthetic audit events and redaction markers, independent evidence protection, tabletop revocation exercise |
| AI and agent control | Model/provider data paths, untrusted instructions, retrieval ACLs, tool/server identity, action authority, budgets and memory scope | Host-enforced authorization tests with mock tools, separate principals, bounded execution and synthetic documents |

For unknown technologies, discover these contracts from actual code, installed APIs, version-appropriate authoritative documentation and authorized tests. Record Unknown, Documented, Configured, Verified or Unsupported at the applicable scope. A documented feature alone does not establish enforcement. If required evidence is absent, recommend verification or a safe conditional plan; do not invent settings or migrate a product merely because it lacks a profile. Existing technology-specific profiles remain optional.
