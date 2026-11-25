# Solution Design Hardening

**Build software that survives concurrency, failures, and scale.**

A technology-independent Agent Skill for assessing and fixing transactional and distributed-system correctness problems. The catalog contains 124 failure scenarios, including duplicate charges, stale caches, dual writes, retry storms, lost messages, concurrency conflicts, and unsafe recovery.

## Install

After publishing this repository, replace `OWNER` with its GitHub owner:

```sh
npx skills add OWNER/solution-design-hardening --skill solution-design-hardening
```

Alternatively, copy `skills/solution-design-hardening/` into your agent's supported skill directory (for example `.claude/skills/` or `.agents/skills/` where supported). Check your agent's documentation. The skill uses the open [Agent Skills format](https://agentskills.io/specification); compatibility with individual agent releases has not been tested.

## Use

- **Assess:** Use solution-design-hardening to assess the entire repository and produce a prioritized remediation plan. Do not edit product code.
- **Implement:** Use solution-design-hardening to implement approved remediation tasks and verify their acceptance criteria.
- **Review:** Review these changes using solution-design-hardening; report evidence-backed correctness risks.
- **Design:** Apply relevant solution-design-hardening safeguards while implementing this feature.

Full assessments generate `SOLUTION-DESIGN-ASSESSMENT.md` and `SOLUTION-DESIGN-REMEDIATION-PLAN.md`. Focused work loads only relevant references. Existing project catalogs are respected and cross-mapped to the bundled baseline.

## Scope

The original 100 problems retain stable IDs SDP-001–100. The release adds 24 scenarios covering financial edge cases, migration and replication, external integrations, operational recovery, and tenant isolation. Patterns are options, not mandatory architecture ingredients.

## Repository

- `skills/solution-design-hardening/SKILL.md`: agent instructions
- `references/` inside the skill: catalog, detection, pattern and operations guidance
- `assets/` inside the skill: assessment and remediation templates
- `evals/`: evaluation scenarios and rubric
- `tools/validate.py`: offline package validation
- `SOURCE-REVIEW.md`: external references and review limitations

## Validation and limitations

Run `python3 tools/validate.py` from the repository root. This checks package structure, catalog IDs, internal links and evaluation mappings; it does not measure model effectiveness. The evaluation cases are supplied for future agent runs. No model benchmark or production certification is claimed. The skill cannot guarantee discovery of every defect or substitute for engineering review and runtime tests.

## License

MIT (proposed for the initial public release; repository owner should confirm rights and licensing before publishing). No external skill text is bundled.
