# Context strategy and assessment continuity

Reduce irrelevant context without reducing correctness. Select scope and operating mode first. A small focused task does not require reading all 235 problem descriptions or building a full repository model. A full assessment does require coverage of every bundled entry and distinct project entry; work in bounded batches rather than truncating the catalog.

Design principle: separate the size of the available knowledge from the size of the loaded knowledge. The catalog can grow without increasing the context of an ordinary focused task. Never reduce the catalog or remove guidance to save tokens.

## Knowledge levels

| Level | Content | Where |
|---|---|---|
| 0 | Skill name and activation description | `SKILL.md` frontmatter |
| 1 | Core rules, depth modes and routing | `SKILL.md` |
| 2 | Problem IDs, domains, applicability and families | [problem index](PROBLEM-INDEX.md) and the domain indexes |
| 3 | One problem: failure, detection, remediation, verification, related IDs | `problems/SDP-NNN.md` |
| 4 | Supporting expertise: technology, security, architecture, verification, operations | references listed below |

Levels decide where knowledge lives, not how much may be read. There is no size or token limit on what an agent reads: load every problem file, reference and source path needed to find all applicable problems and verify them. Completeness and correctness always take precedence over context size. `tools/context.py` reports character-based size estimates for information only.

## Execution depth

Depth is independent of the operating mode (assess, implement, design/review). Choose a depth that covers every applicable trigger. When in doubt, choose the deeper mode. Report the depth used and what was excluded.

| Depth | Purpose | Loads at least | Relative context |
|---|---|---|---|
| Lightweight | Routine development with no trigger | Level 1; escalate as soon as a trigger, an unknown guarantee or a possible problem appears; give a scoped non-finding only when the stated boundary suffices | Very low |
| Focused | A specific problem or risk | + Level 2 route and every applicable Level 3 file; check their Related IDs and expand whenever evidence shows a shared boundary | Low |
| Standard | Feature design and implementation | + detection and pattern guidance, all problems on the changed path and their Related IDs | Moderate |
| Deep | Complex cross-component, security, migration or recovery change | + relevant Level 4 references: architecture, security, technology capabilities, integration verification, operations | High |
| Comprehensive | Entire solution assessment | Every catalog ID in bounded batches, assessment output and a persistent [coverage register](../assets/coverage-register.md) | Very high, checkpointed |

Escalate to at least Focused when the work touches money or another external effect, durable messaging, cross-process or multi-replica invariants, authentication, authorization or another trust boundary, schema or data migration, or caching of authoritative data. Escalate further when evidence reveals another boundary, a security exposure or an unknown guarantee. Never stop reading, skip a problem or skip a verification step because of context size; if a context window fills, checkpoint and resume.

## Supporting expertise (Level 4)

- [Detection guidance](DETECTION-GUIDANCE.md): code signals, counterexamples and failure tests.
- [Pattern guidance](PATTERN-GUIDANCE.md): implementation cautions and checks per area.
- [Operational and migration guidance](OPERATIONS.md): signals, rollout, replay and recovery.
- [Architectural intelligence](ARCHITECTURAL-INTELLIGENCE.md), [security assessment](SECURITY-ASSESSMENT.md), [technology discovery](technology/DISCOVERY.md), [integration verification](INTEGRATION-VERIFICATION.md) and [assessment output](ASSESSMENT-OUTPUT.md).

## Select references deliberately

1. Discover the changed or requested business paths, their invariant owners, trust crossings, transaction/effect boundaries and relevant technology capabilities.
2. Use the catalog index to select initial problem IDs. Read their domain playbooks; expand to related problems as evidence reveals shared dependencies, retries, async side effects, lifecycle or security boundaries. Do not assume initial selection is exhaustive.
3. Load capability guidance before optional product-specific profiles. Check versions, configuration and topology when relevant. Use security/threat-model and architecture references for cross-boundary risks, and integration verification for correctness-critical changes.
4. Keep compact evidence records (paths, symbols, commit/version, status, unknowns) and avoid repeatedly re-reading unchanged references or huge logs. Do not include raw secrets or unnecessary personal data.
5. For a full assessment, checkpoint the assessed IDs, covered components and paths, findings, pending verification and next ranges. Revalidate evidence after relevant code changes. No skipped ID is silently treated as not applicable.

## Quality guardrails

- Re-open source and relevant guidance if a summary omits a correctness-critical detail. Context budgeting never authorizes an unsafe fix or omission of an applicable security check.
- Distinguish read files from actually verified implementation paths. For focused work report exclusions; for full work report coverage and incomplete paths.
- Optional reference routing helpers are not required for the standalone skill. Byte counts describe selected reference size, not measured model tokens, cache costs, or context actually consumed.
- Do not optimize away negative controls, crash/replay verification, migration safety or uncertainty reporting.

## Evaluation

Compare equivalent tasks in independent fresh sessions, with identical model/settings, prompts and permissions. Record tool traces and actual input/output token counts when available. Treat activation as unknown without host evidence. Do not infer effectiveness from reference size or from local fixture tests. Preserve quality and safety when optimizing context; a smaller prompt is not necessarily a better result.
