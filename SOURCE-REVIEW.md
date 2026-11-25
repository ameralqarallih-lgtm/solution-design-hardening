# Source review and design rationale

Review date: 2026-11-25. Guidance is independently expressed; no third-party skill files or code are redistributed.

| Reference | Review scope | Design influence |
|---|---|---|
| [Microsoft distributed systems](https://github.com/microsoft/amplifier-bundle-systems-design/blob/main/skills/system-type-distributed/SKILL.md) | Relevant source sections | Conflict semantics and failover authority |
| [mblode distributed correctness](https://github.com/mblode/agent-skills/blob/main/skills/codebase-architecture/references/distributed-correctness.md) | Relevant source sections | Stable identities, restart safety, reconciliation |
| [magnus919 backend engineering](https://github.com/magnus919/agent-skills) | Repository skill descriptions | Migration coexistence and engineering boundaries |
| [bjornjee distributed systems](https://verified-skill.com/skills/bjornjee/skills/distributed-systems) | Registry-rendered skill text; upstream source not independently confirmed | Operational signals and bounded work |
| [wshobson architecture patterns](https://www.skills.sh/wshobson/agents/architecture-patterns) | Registry summary and visible excerpt | Domain ownership and test boundaries |
| [robsonrung architecture review](https://www.skills.sh/robsonrung/rar-skills/architecture-review) | Registry excerpt | Safe review scope and proportionate changes |
| [Agent Skills specification](https://agentskills.io/specification) | Format requirements | Metadata and progressive references |

This is a qualitative review, not an exhaustive comparison or performance benchmark. No claim of uniqueness, affiliation, or endorsement is made. The extension catalog and evaluation cases are original synthesis of common engineering failure modes. Existing safeguards are retained where appropriate rather than duplicated. Source links are references, not runtime dependencies.

## v0.3.0

Independently authored extensions build on v0.2.0. Packaging follows the [Agent Skills specification](https://agentskills.io/specification) and [official repository](https://github.com/agentskills/agentskills). No additional third-party skill text incorporated.

## v0.8.0 security sources

The original playbooks were expanded with independently written defensive guidance. See [security standards](skills/solution-design-hardening/references/SECURITY-STANDARDS.md) for versioned official sources and limitations. No third-party standard text or code is redistributed as part of the new guidance; risk labels and identifiers are references. Individual candidate CWE and normative control applicability require assessment-time verification.
