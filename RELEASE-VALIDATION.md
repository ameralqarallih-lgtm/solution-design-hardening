# v0.7.0 release validation

Preparation environment: Python 3.13, no Docker executable or Docker socket, no installed PostgreSQL/Redis/RabbitMQ client libraries. The repository was built from the v0.6.0 GitHub archive, not from a live GitHub checkout.

| Check | Result |
|---|---|
| `python tools/validate.py` | Passed: metadata, links, 160 sequential IDs, complete playbook coverage, 40 evaluation cases, 17 scanner rule mappings |
| `python -m unittest discover -s evals -v` | Passed: 22 tests, including all 17 scanner positive fixtures, negative controls and output filtering |
| `python -m compileall -q integration` | Passed: integration Python syntax |
| `python -m unittest discover -s integration -v` (outside lab) | 0 tests executed; 4 classes skipped as intended by isolation guard |
| Compare prior catalog, playbooks, capability and product references | Passed: unchanged byte-for-byte |
| YAML parse and static lab checks | Passed: internal network declaration; no published service ports or host mounts in supplied Compose file |
| PostgreSQL, Redis, RabbitMQ default integration lab | Not run (12 tests defined) |
| SQL Server optional integration lab | Not run (3 tests defined; explicit license acceptance required) |
| GitHub Actions execution | Not run here |
| AI coding-agent benchmark | Not run (40 cases defined) |

No runtime service guarantee is claimed from these checks. Compose runtime behavior, image availability, dependency compatibility, and all service assertions must be verified in the target lab. No multi-node or multi-region failure injection is provided in this milestone. GitHub publication and licensing attribution remain the repository owner's responsibility. See [lab instructions](integration/README.md).
