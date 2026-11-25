# v0.9.0 release validation

Built from the supplied v0.8.0 GitHub archive, not a live checkout. This release adds evidence-based architecture modeling and two optional offline helpers. No production or third-party systems were contacted.

| Check | Result |
|---|---|
| `python tools/validate.py` | Passed: 235 sequential IDs, complete 24-playbook coverage, internal links, 66 agent scenarios, 27 scanner mappings, security crosswalk coverage, sample architecture model |
| `python -m unittest discover -s evals -v` | Passed: 45 tests (30 inherited, 15 new architecture and correlation tests) |
| Previous reference comparison | Passed: all 66 inherited Markdown reference files byte-for-byte unchanged, including the catalog, playbooks and security/technology references |
| Candidate inventory fixture | Passed: polyglot and nested manifests, local declared dependencies, deterministic output, unresolved references, bounded file scope, secret-name and symlink exclusions, candidate-only grouping |
| Model validation fixture | Passed: explicit shared mechanisms and invariants, unknown trust/transaction links, missing evidence, dangling/duplicate IDs, task dependency cycles, unmapped findings |
| `python tools/architecture.py examples --max-files 100` | Passed: CLI smoke test |
| `python tools/correlate.py examples/architecture-model.json` | Passed: synthetic example with two findings and two task waves |
| Integration Python syntax | Passed: compilation only |
| Default real-service lab (12 tests) | Not run: Docker unavailable |
| Optional SQL Server lab (3 tests) | Not run: Docker unavailable; explicit EULA acceptance needed |
| Real identity-provider, browser, multi-region, network and agent security verification | Not run |
| Actual coding-agent benchmark | Not run (66 scenarios defined) |
| GitHub Actions and remote publication | Not run; remote repository not modified |

The new discovery helper is static and heuristic, with local dependency extraction limited to .NET project references and npm local directory references. It does not derive a runtime call graph, verify transaction scopes or infer business requirements. The correlation helper validates the structure of analyst-supplied relationships, not their truth. Paths and architecture metadata can be sensitive. Local tests are not production guarantees or evidence of model effectiveness. Existing standards mappings remain advisory, not formal compliance. The proposed MIT licensing and attribution remain subject to owner confirmation.
