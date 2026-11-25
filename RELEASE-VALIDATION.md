# v0.10.0 release validation

Built from the supplied v0.9.0 GitHub archive, not a live checkout. This release introduces benchmark tooling and context routing. It does not claim measured model effectiveness or production guarantees.

| Check | Result |
|---|---|
| `python tools/validate.py` | Passed: 235 sequential IDs, 24 playbooks, internal links, 66 scenario cases, 27 scanner rules, 16 labeled cases, 8 activation probes, reference routing |
| `python -m unittest discover -s evals -v` | Passed: 61 tests (45 inherited, 16 new benchmark/context tests) |
| Inherited references and cases | Passed: all 67 reference files and 66 scenario cases unchanged byte-for-byte |
| Benchmark plan and adapter tests | Passed: deterministic paired plans, identical prompts, optional competitor, isolated temporary input workspace, response-only review packet, snapshot tamper detection, timeout and malformed output handling |
| Report and context tests | Passed: precision/recall, negative controls, incomplete pairs, unknown usage, safety override, invalid grades, activation unknowns, selective routing |
| End-to-end CLI smoke test | Passed with synthetic adapter only; no model invoked, no actual grades or usage |
| Documentation charts | Five local SVG charts parsed as XML; Markdown relative links validated. GitHub rendering not independently tested |
| Infrastructure lab | 15 test definitions inherited; not executed (Docker unavailable) |
| Actual coding-agent benchmark | Not run; no agent adapter or model credentials configured |
| Remote GitHub publication and Actions | Not run; remote repository not modified |

The benchmark runner is a generic adapter interface, not an agent-specific integration or OS security sandbox. External execution is explicitly opt-in and can incur costs. Host isolation, subprocess-tree termination, permissions, budgets and fresh-session enforcement are adapter/operator responsibilities. Reviewer blinding is best-effort; responses may reveal condition. Gold labels cover 16 of 66 cases only; results depend on independent human grading and representative case selection. Activation and token data require actual host evidence. Complete-pair summaries can be biased by missing results. No statistical superiority or formal security compliance is claimed. Context routing measures selected UTF-8 file sizes, not model token savings. The proposed MIT licensing and attribution remain subject to owner confirmation.
