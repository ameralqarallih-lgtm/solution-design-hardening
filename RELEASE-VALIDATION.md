# v1.0.0-RC2 release validation

## RC2 local checks

The Windows validation run used Python 3.12.10. No model or infrastructure runs were made for RC2.

| Check | Result |
|---|---|
| `python tools/validate.py` | Passed for 235 sequential IDs, 235 problem files with required fields and valid Related IDs, 24 domain indexes with one shared decision rule, a problem index and detection guidance covering every ID, the core's required headings, internal links, 66 scenario cases, 27 scanner rules, 16 labeled cases, 8 activation probes and reference routing. |
| `python -m unittest discover -s evals -v` | 96 tests collected, 95 passed, and 1 skipped because this Windows environment could not create symlinks. |
| Knowledge preservation | All 3,150 normalized statements from the pre-change skill tree (commit `4f17361`) are present. Two reviewed edits: the template list gained a missing comma, and the "Additional reference material" heading became "Supporting expertise (Level 4)". |
| Context estimates | Core 2,481 estimated tokens, previously 4,461. The focused route for SDP-023, SDP-024 and SDP-171 is 5,027, previously 7,989. The fixed pilot context is 6,701, previously 7,297. These figures are characters divided by four, not measured model tokens. |
| Benchmark context mode | Mock-agent tests confirm that `--context-mode core` sends only `SKILL.md`, records the mode, and rejects a mode change on resume. |
| Pending | A paired live comparison of RC1 and RC2 context, human adjudication, trace-backed native activation and the optional SQL Server lab. |

No size or token limit is enforced on the skill or on what an agent reads. Completeness and correctness take precedence over context size. The always-loaded core keeps all safety, invariant, workflow, safeguard and correctness-gate guidance.

## v1.0.0-RC1 release validation

The Windows validation run used Python 3.12 and Codex CLI `0.171.0-alpha.13.2` for command-line checks. The local empirical results and exact model settings are recorded in [Benchmark results](BENCHMARK-RESULTS.md).

| Check | Result |
|---|---|
| `python tools/validate.py` | Passed for 235 sequential IDs, 24 playbooks, internal links, 66 scenario cases, 27 scanner rules, 16 labeled cases, 8 activation probes and reference routing. |
| `python -m unittest discover -s evals` | 79 tests collected, 78 passed, and 1 skipped because this Windows environment could not create symlinks. |
| Inherited files | SHA-256 comparison matched all 77 reference, skill asset and evaluation-data files from the supplied archive. |
| Built-in CLI and HTTP adapters | Fixtures exercised parsing, usage and cost, API output limits, authentication errors and preflight. The latest local Codex preflight reported a login. |
| End-to-end benchmark | The synthetic adapter produced two responses, the review packet, grading template, and Markdown, JSON and valid SVG reports. |
| Grading and recovery | Tests exercised unavailable and invalid grades, human overrides, failed-attempt history, resume, retry, reconciliation in reports and matching experiment summaries. |
| Live model requests | 36 scored-pilot responses from local Ollama with 18 complete pairs and 36 provisional Codex grades. Native activation and additional live adapters are pending. |
| Infrastructure lab | All 12 default tests passed using PostgreSQL, Redis and RabbitMQ. Three optional SQL Server tests remain pending. |
| Stable promotion | Pending adjudication of the safety flags and safe-control errors and broader live-provider coverage. |

The built-in pilot evaluates fixed prompt guidance. Use a trace-capable custom adapter for native skill activation. Model grades are provisional and review packets can reveal the condition through response content. Precision and recall apply to the 16 labeled cases. Incomplete pairs and retry outcomes can affect comparisons. Validate live provider behavior and infrastructure before deciding whether to promote the release candidate.
