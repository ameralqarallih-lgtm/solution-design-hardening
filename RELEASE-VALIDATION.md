# v0.11.0 release validation

v0.11.0 builds on the supplied v0.10.0 release archive. The Windows validation run used Python 3.12 and the local Codex CLI `0.171.0-alpha.13.2` for command-line checks.

| Check | Result |
|---|---|
| `python tools/validate.py` | Passed for 235 sequential IDs, 24 playbooks, internal links, 66 scenario cases, 27 scanner rules, 16 labeled cases, 8 activation probes and reference routing. |
| `python -m unittest discover -s evals` | 78 tests collected, 77 passed, and 1 skipped because this Windows environment could not create symlinks. The suite includes 17 new benchmark regressions. |
| Inherited files | SHA-256 comparison matched all 77 reference, skill asset and evaluation-data files from the supplied archive. |
| Built-in CLI and HTTP adapters | Synthetic fixtures exercised response parsing, usage and cost, authentication errors and adapter preflight. The installed Codex CLI accepted the startup flags and reported signed-out status. |
| End-to-end benchmark | The synthetic adapter produced two responses, the review packet, grading template, and Markdown, JSON and valid SVG reports. |
| Grading and recovery | Tests exercised unavailable and invalid grades, human overrides, failed-attempt history, resume, retry, reconciliation in reports and matching experiment summaries. |
| Live agent and judge requests | Pending. Local Claude Code and Copilot CLIs were unavailable, and local Codex was signed out. HTTP coverage used a local fixture. |
| Infrastructure lab | 15 test definitions retained. Docker was unavailable on PATH for this run. |
| Publication | Local release candidate. GitHub publishing and release tagging require maintainer approval. |

The built-in pilot evaluates fixed prompt guidance. Use a trace-capable custom adapter for native skill activation. Model grades are provisional and review packets can reveal the condition through response content. Precision and recall apply to the 16 labeled cases. Incomplete pairs and retry outcomes can affect comparisons. Validate live provider behavior and infrastructure before deciding whether to promote the release candidate.
