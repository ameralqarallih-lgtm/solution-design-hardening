# Solution Design Hardening

**Build secure software that survives concurrency, failures, threats, and scale.**

![Release](https://img.shields.io/badge/release-v0.9.0-blue) ![License](https://img.shields.io/badge/license-MIT-blue) ![Problems](https://img.shields.io/badge/failure%20scenarios-235-teal) ![Agent Skills](https://img.shields.io/badge/format-Agent%20Skills-purple)

An open-source, evidence-driven AI coding skill for discovering, preventing, fixing and verifying architectural correctness and security problems in transactional, distributed and highly available applications. Designed for solution architects, backend engineers, platform engineers and coding agents.

[Quick start](#quick-start) · [Coverage](#coverage) · [Architectural Intelligence](#architectural-intelligence-v090) · [Examples](#examples) · [Validation](#validation-and-evaluation) · [Roadmap](#roadmap)

## Why this skill exists

A system may pass ordinary functional tests and still charge customers twice, lose committed events, overwrite newer data, or collapse under retries. Architecture hardening means reasoning about business invariants across real transaction boundaries, concurrent requests, external dependencies, crashes and recovery — not simply checking that a design pattern or library is present.

| Failure scenario | Example mitigation | What must be verified |
|---|---|---|
| Duplicate payment | Durable idempotency and provider reconciliation | Concurrent retries produce one business effect |
| Inconsistent ledger | Atomic balanced postings | Debits and credits balance per currency |
| Database + broker dual write | Transactional outbox | Committed event intent survives interruption |
| Duplicate event processing | Transactional inbox | Replay produces no extra local effect |
| Stale cache refill | Generation-aware cache writes | Older reads cannot defeat invalidation |
| Retry storm | Bounded retries, jitter, deadlines | Downstream load stays within capacity |
| Expired distributed lock | Resource-enforced fencing | Obsolete owners cannot write |
| Mixed-version deployments | Expand-contract migration | Both versions work during rollout |

## Quick start

Install from GitHub with the Skills CLI (requires Node.js/npm):

```sh
npx skills add ameralqarallih-lgtm/solution-design-hardening --skill solution-design-hardening
```

The command assumes this repository and version have been published. To install manually, copy `skills/solution-design-hardening/` into your agent's supported skills directory, such as `.claude/skills/` or `.agents/skills/` where supported. Consult your agent's documentation. The skill uses the [Agent Skills open format](https://agentskills.io/specification); individual agent versions have not yet been compatibility tested.

### Assess an existing codebase

```text
Use solution-design-hardening to assess the entire codebase against the
problem catalog. Provide an evidence-based assessment and prioritized
remediation plan. Do not modify source code.
```

### Implement approved fixes

```text
Use solution-design-hardening to implement the approved remediation tasks.
Follow dependencies, preserve business behavior, and verify failure cases.
```

### Prevent defects while developing or reviewing

```text
Apply solution-design-hardening to this feature or code review.
Identify applicable invariants and failure boundaries; avoid unnecessary patterns.
```

## How it works

```mermaid
flowchart LR
    A[Discover architecture] --> B[Identify invariants and failure boundaries]
    B --> C[Assess evidence and applicability]
    C --> D[Prioritize remediation]
    D --> E{Implementation authorized?}
    E -->|No| F[Assessment and plan]
    E -->|Yes| G[Implement minimal sufficient fix]
    G --> H[Verify concurrency and recovery]
    H --> I[Report residual risks]
```

The agent loads only the relevant problem playbooks and technology guides for focused work. Full assessments cover the bundled baseline plus distinct project-specific problems, cross-mapping duplicates. The skill does not require all patterns to be implemented.

## Coverage

235 stable problem IDs, 24 domain playbooks, 17 technology capability profiles, eight cross-cutting security capability families, 12 optional product profiles, and 66 scenario-based agent evaluation cases.

| Domain | Problem IDs |
|---|---|
| Financial and transactional correctness | SDP-001–010, SDP-101–104 |
| Caching | SDP-011–022 |
| Databases and consistency | SDP-023–037 |
| Resilience and distributed coordination | SDP-038–053, SDP-125–130 |
| Messaging | SDP-054–068 |
| APIs | SDP-069–080 |
| Workflows | SDP-081–091 |
| Object storage | SDP-092–100 |
| Data migration | SDP-105–111 |
| Integration and operations | SDP-112–124 |
| Security | SDP-131–136 |
| Deployment and resources | SDP-137–145 |
| Observability and tenancy | SDP-146–150 |
| Lifecycle | SDP-151–160 |
| Authentication and identity | SDP-161–170 |
| Authorization and business-flow security | SDP-171–178 |
| Injection and untrusted content | SDP-179–192 |
| Data protection and cryptography | SDP-193–203 |
| Distributed and infrastructure security | SDP-204–212 |
| Software supply chain | SDP-213–219 |
| Security monitoring and operations | SDP-220–225 |
| AI and agentic application security | SDP-226–235 |

Browse the [full problem catalog](skills/solution-design-hardening/references/SOLUTION-DESIGN-PROBLEMS.md), [core skill](skills/solution-design-hardening/SKILL.md), and [technology guides](skills/solution-design-hardening/references/technologies/README.md).

### Architectural Intelligence (v0.9.0)

Move from individual pattern detection to evidence-backed understanding of complete business operations. Discover components and declared dependencies, trace actual call paths, map transaction and trust boundaries, identify invariant owners and correlate findings only when their common failure mechanism is supported by evidence.

```mermaid
flowchart TD
    A[Repository and deployment evidence] --> B[Component and dependency candidates]
    B --> C[Semantic trace of business operations]
    C --> D[Transaction boundaries and invariants]
    C --> E[Trust boundaries and authorization]
    D --> F[Evidence-backed findings]
    E --> F
    F --> G[Explicit root causes and independent risks]
    G --> H[Dependency-aware remediation and verification]
```

| New capability | What it does | What it does not prove |
|---|---|---|
| Candidate component inventory | Groups project directories and assigns source locations | Actual deployment topology |
| Declared dependencies | Resolves local .NET project and npm file/link references | Runtime call graph or shared transaction |
| Boundary signals | Locates 12 families of likely operations | Call order, authorization or durability |
| Business invariant and trust mapping | Agent traces effects, owners, constraints and permissions | Unobserved requirements or guarantees |
| Root-cause correlation | Links analyst-supported mechanisms to multiple findings | Automatic causal inference from co-location |
| Task dependency validation | Rejects dangling references and cycles, reports task waves | Approval, priority or successful remediation |

Try the optional offline helpers from the repository root:

```sh
python tools/architecture.py /path/to/repository > architecture-candidates.json
python tools/correlate.py examples/architecture-model.json
```

The first command produces candidates, the second validates an illustrative analyst-authored model. See [architecture tooling](tools/ARCHITECTURE.md) and [architectural intelligence guidance](skills/solution-design-hardening/references/ARCHITECTURAL-INTELLIGENCE.md). Full assessments include an architecture model (or an equivalent section in the assessment); focused tasks trace only relevant paths. The skill remains technology-independent even when no automated parser exists.

### Comprehensive Security Hardening (v0.8.0)

Security is integrated into the same evidence-driven architecture assessment, not a separate plugin or a product-specific checklist. The release preserves the original 160 entries and adds 75 security scenarios. It covers authentication, resource/function/property authorization, input-to-interpreter boundaries, data and cryptographic protection, workload and network trust, software supply chain, security operations, and AI/agent permissions and data isolation.

| Example security failure | Minimum safeguard | Verification |
|---|---|---|
| Object authorization failure | Enforce ownership or grants at the actual operation | Two principals: denied cross-owner and allowed own-object access |
| Fail-open authorization | Deny protected effects on policy failure | Inject timeout; permitted normal path still works |
| Token validation failure | Verify intended issuer, audience, type, signature and expiry | Invalid token rejected; valid token accepted |
| Unsafe property binding | Allowlist writable fields | Attempt protected-field change; allowed field updates |
| Supply chain integrity | Verify trusted provenance and artifact identity | Reject mismatched artifact and unapproved builder |
| Prompt injection / excessive agency | Enforce authority outside model context | Mock untrusted instruction cannot trigger unauthorized effect |

Start with [security assessment](skills/solution-design-hardening/references/SECURITY-ASSESSMENT.md), [adaptive security capabilities](skills/solution-design-hardening/references/SECURITY-CAPABILITIES.md), [standards traceability](skills/solution-design-hardening/references/SECURITY-STANDARDS.md) and the [threat model template](skills/solution-design-hardening/assets/threat-model.md). Mappings reference OWASP Top 10:2025, API Top 10:2023 and candidate CWE IDs; ASVS 5.0.0, GenAI/Agentic 2026, SSDF, SLSA, CIS and ATT&CK are separate verification inputs. Category-level coverage does not certify compliance.

```text
Use solution-design-hardening to assess security across this codebase.
Map trust boundaries, actors and protected assets; identify applicable
security problems with evidence and propose prioritized remediation.
Do not modify code or probe external/production systems.
```

Local security fixtures use synthetic principals and SQLite or mock policy/tool calls. They reproduce missing object scoping and unsafe property binding, and verify scoped fixes, parameter binding, sequential token redemption, fail-closed policy and external tool authorization. They do not validate a real identity provider, web server, cryptographic protocol or agent model. See [security reporting](SECURITY.md) for responsible disclosure.

### Adaptive Technology Intelligence

**No fixed supported-technology list.** Discover the stack dynamically, identify the capabilities required by the business invariant, verify version and configuration, then select the simplest supported implementation. Unlisted or proprietary technologies follow the same workflow; unverifiable guarantees remain open verification tasks.

```mermaid
flowchart TD
    A[Business invariant] --> B[Discover component and versions]
    B --> C[Map required capabilities]
    C --> D[Load relevant capability profile]
    D --> E{Optional product profile exists?}
    E -->|Yes| F[Consult product profile]
    E -->|No| G[Inspect installed APIs and official docs]
    F --> H[Verify version and effective configuration]
    G --> H
    H --> I{Sufficient evidence?}
    I -->|Yes| J[Design and test proportionate fix]
    I -->|No| K[Requires Verification]
```

| Layer | Responsibility |
|---|---|
| Universal problems | 235 stable failure scenarios and 24 playbooks |
| Discovery | Component-specific manifest, dependency, configuration and topology evidence |
| Capability mapping | 17 reusable technology-independent domains |
| Product profiles | 12 optional accelerators, not prerequisites |
| Verification | Separate declared, resolved and deployed versions; verify effective guarantees |

The [capability index](skills/solution-design-hardening/references/technology/CAPABILITY-MAPPING.md) includes databases, caching, messaging, streaming, workflows, workers, storage, runtimes, data access, coordination, orchestration, serverless, identity, APIs, search and observability. Existing profiles for .NET, Java, Node.js, Python, SQL Server, PostgreSQL, MongoDB, Redis, RabbitMQ, Kafka, Kubernetes and S3-compatible storage remain available. None is a claim of tested product compatibility.

**Example:** An unfamiliar queue with a `complete()` API is not assumed to behave like RabbitMQ. The agent verifies acknowledgment, durability and replay semantics and tests the failure boundary after the consumer commit. If it cannot establish those guarantees, it records Requires Verification rather than inventing an API or recommending unnecessary migration.

Use the [technology inventory template](skills/solution-design-hardening/assets/technology-inventory.md) for traceable evidence. Optional manifest discovery:

```sh
python tools/discover.py /path/to/repository
```

The helper is offline and read-only. It recognizes selected manifest filenames and limited toolchain version metadata; it does not resolve dependencies, inspect deployed services or prove capabilities. Missing signals do not imply an unsupported stack.

## Examples

### Example finding: database and broker dual write

**Evidence:** the order is committed before publishing its required event. A process interruption between these steps leaves a committed order without a durable event intent.

**Proposed fix:** persist an immutable event intent in the same transaction as the order. A relay publishes the intent; a duplicate-safe consumer handles redelivery. Monitor relay backlog and reconcile failures.

**Verification:** interrupt before the atomic commit; verify both records roll back. Interrupt after commit; verify intent remains recoverable. Interrupt after broker acceptance but before recording delivery; verify repeated delivery has no duplicate business effect.

See [assessment example](examples/assessment-example.md) and [executable fixtures](evals/fixtures/transactions.py). The latter uses SQLite for local atomicity demonstrations, not a real broker.

### Assessment outputs

- `SOLUTION-ARCHITECTURE-MODEL.md`: component, dependency, business operation, invariant and trust-boundary evidence (or an equivalent section in the assessment).
- `SOLUTION-DESIGN-ASSESSMENT.md`: status, evidence, severity and recommended mitigation for every problem.
- `SOLUTION-DESIGN-REMEDIATION-PLAN.md`: prioritized tasks, dependencies, affected code, acceptance criteria, tests and rollout guidance.

Assessment-only requests do not authorize product code changes. Unsupported runtime claims must be marked Requires Verification.

## Validation and evaluation

Requires Python 3.10+; no third-party Python dependencies for the included tools.

```sh
python tools/validate.py
python -m unittest discover -s evals -v
python tools/scan.py /path/to/repository
```

The scanner is a small read-only heuristic helper with 27 candidate rules; its results are **not confirmed defects**. It does not print source lines or secret values. Review candidate locations manually and use the relevant playbook. It is not a full static analyzer.

The executable suite demonstrates vulnerable and corrected outbox, inbox, cache, object access and property binding paths, plus bounded security teaching examples, and checks scanner and scoring behavior. The cache example is a deterministic model, not a Redis integration. GitHub Actions runs the local checks on pushes and pull requests.

For agent comparisons, use the [evaluation protocol](evals/README.md) and `python tools/score.py results.json` to aggregate human-reviewed paired trials. Do not expose expected answers to the evaluated agent. No actual cross-agent benchmark scores have been generated yet.

### Infrastructure integration lab (v0.7.0)

The repository includes an opt-in [disposable Docker Compose lab](integration/README.md) for real PostgreSQL, Redis and RabbitMQ tests, plus an optional SQL Server target. These are examples of verifying capabilities, not a closed list of supported products. The skill's [integration verification guide](skills/solution-design-hardening/references/INTEGRATION-VERIFICATION.md) applies to any stack.

| Layer | Scope | Status at release preparation |
|---|---|---|
| Offline structural checks | 235 IDs, playbooks, links, 66 evaluation cases, scanner mappings | Passed |
| Offline executable suite | 45 tests, including all 27 scanner signals and safe controls | Passed |
| Default infrastructure lab | 12 tests: real database process exits, reservations, Redis stale refill, RabbitMQ redelivery, relay replay | Not run; Docker unavailable |
| Optional SQL Server lab | 3 tests: atomic commit/rollback and stale rowversion rejection | Not run; requires explicit EULA acceptance |
| Actual agent benchmarks | 66 candidate scenarios | Not run |

To run the default lab in a dedicated disposable project (requires Docker/Compose):

```sh
docker compose -p sdh-v070-lab -f integration/compose.yaml up --build --abort-on-container-exit --exit-code-from tests tests
```

See the [release validation report](RELEASE-VALIDATION.md). Follow the [lab instructions](integration/README.md) for recording versions, cleanup, optional SQL Server and experiment limitations. CI includes a dedicated integration workflow. Local unit tests remain dependency-free. The scanner is heuristic, line-based and may miss cross-file or multi-line risks; a hit is never a confirmed defect. No technology is unsupported merely because a scanner rule or fixture is absent.

## Roadmap

| Release | Milestone | Status |
|---|---|---|
| v0.1.0 | 100-problem baseline | Complete |
| v0.2.0 | Stable IDs, assessment methodology, evaluation cases | Complete |
| v0.3.0 | 160 problems and targeted playbooks | Complete |
| v0.4.0 | Technology-specific guides | Included in v0.5.0 |
| v0.5.0 | Initial executable fixtures, heuristic scanner, evaluation scoring | Complete |
| v0.6.0 | Adaptive Technology Intelligence | Complete |
| v0.7.0 | Real-service integration lab, expanded detection and fault injection | Implemented; infrastructure run pending |
| v0.8.0 | Comprehensive Security Hardening | Implemented; local checks passed |
| v0.9.0 | Architectural Intelligence: dependency, transaction, invariant and trust-boundary mapping | Current release candidate; local checks passed |
| v0.10.0 | Cross-agent benchmarks and context optimization | Planned |
| v1.0.0 | Validated effectiveness, compatibility, community feedback | Planned |

## Contributing

Report reproducible failure scenarios, propose targeted safeguards and add negative controls. Preserve stable problem IDs, avoid duplicate entries, and run local validation before opening a pull request. See [CONTRIBUTING.md](CONTRIBUTING.md) and [source review](SOURCE-REVIEW.md).

## Limitations and license

This is an instructional skill, not a certification, automated proof system or guarantee of production reliability. Real infrastructure behavior, correctness targets and provider versions must be independently validated. MIT license; repository owner should confirm copyright and licensing rights before publication. See [LICENSE](LICENSE).
