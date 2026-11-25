# v0.8.0 release validation

Built from the supplied v0.7.0 GitHub archive, not a live GitHub checkout. The release focuses on defensive security hardening. No production or third-party system was probed.

| Check | Result |
|---|---|
| `python tools/validate.py` | Passed: 235 sequential IDs, 24 playbooks, internal links, 56 agent scenarios, 27 scanner mappings, security crosswalk coverage |
| `python -m unittest discover -s evals -v` | Passed: 30 tests, including 8 new local security tests, positive fixtures for every scanner rule, safe controls and output filtering |
| Prior catalog comparison | Passed: original 160 entries preserved as byte-for-byte prefix |
| Prior playbook and technology references | Passed: 50 files preserved byte-for-byte |
| `python -m compileall -q integration` | Passed: Python syntax only |
| Security standards | Official reference versions consulted; 92 candidate crosswalk entries (75 new and 17 legacy). Individual CWE and normative control mappings not independently exhaustively verified |
| Default PostgreSQL, Redis, RabbitMQ lab | Not run: Docker unavailable (12 tests defined) |
| Optional SQL Server lab | Not run (3 tests defined; explicit EULA acceptance required) |
| Real identity provider, browser, network, cryptographic and agent integration tests | Not run; local examples use synthetic SQLite or mock policies/tools |
| AI agent benchmark | Not run (56 cases defined) |
| GitHub Actions and publication | Not run; remote repository not modified |

The scanner is heuristic, not a complete static security analyzer. Tests prove only the specific exercised local behavior. No formal ASVS, CIS, SLSA or other compliance assessment was performed. The MIT licensing and copyright attribution remain subject to owner confirmation. See [standards reference](skills/solution-design-hardening/references/SECURITY-STANDARDS.md) and [lab instructions](integration/README.md).
