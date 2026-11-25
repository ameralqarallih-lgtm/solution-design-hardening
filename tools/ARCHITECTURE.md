# Offline architecture tooling

Two optional standard-library Python helpers support v0.9.0. They do not need to be installed to use the agent skill. They do not contact networks, execute project code, build dependencies, or write to the inspected repository. Run only in an authorized workspace; generated paths and metadata may be sensitive. Do not publish reports without review.

## Candidate inventory

```sh
python tools/architecture.py /path/to/repository --max-files 20000 > architecture-candidates.json
```

Candidate components are project directories identified by common manifest names; files are assigned to the nearest such directory, otherwise to a root placeholder. Multiple projects in one directory can be grouped. Only explicit .NET project references and npm local `file:`/`link:` directory references are currently resolved to inventoried project manifests. A dependency is declared, not a verified network edge. Other languages and deployment formats need manual tracing. Unknown targets are reported without exposing raw reference values.

Twelve signal families identify likely boundaries: transaction start, commit, rollback, publish, acknowledgment, external call, cache, authorization, input entry, background entry, tenant context and constraints. Existing 27 scanner rules provide candidate risk locations. Signals are line-based, may occur in comments, tests or unrelated code, and do not prove actual behavior or sequence. Same-file risk clusters are investigation hints only. The agent should combine results with `discover.py` and semantic inspection using the skill's architectural guidance. The tool does not infer runtime topology, call graphs, invariant ownership, trust crossings or root causes.

The inventory skips symlinks, hidden and common generated directories and selected secret-named files/directories; reads only selected formats up to 1 MiB and limits successfully inspected files. It reports truncation and selected skips; unlisted file types and excluded directories are not counted as inspected. File paths are emitted, not source lines or raw dependency strings. The helper is intended for a stable local checkout, not an adversarially modified filesystem or a secret scanner. Review limitations before sharing output.

## Analyst-authored model and correlation

```sh
python tools/correlate.py examples/architecture-model.json
```

Create a separate JSON model after validating candidate signals and tracing actual operations. The [synthetic example](../examples/architecture-model.json) shows the version 1 interchange structure. It is optional and does not replace the human-readable architecture, assessment or remediation plan. Top-level arrays are required (empty arrays allowed):

| Array | Required fields beyond unique `id` |
|---|---|
| `components` | `name`, `status`, `evidence_ids` when supported |
| `evidence` | `kind` (source/config/test/runtime/documentation/requirement), `locator` (sanitized reference) |
| `flows` | `source`, `target` component IDs, `effect`, `failure_boundary`, `trust_crossing` (yes/no/unknown), `transaction_relation` (same-local/separate/unknown/not-applicable), `status`, evidence |
| `invariants` | `requirement`, `scope`, `enforcement`, `owner` (component ID or null if unknown), `status`, evidence; optional `flow_ids` |
| `root_causes` | `mechanism`, `status`, evidence |
| `findings` | `problem_ids` (bundled SDP IDs), `component_ids`, `severity` (Critical/High/Medium/Low/Unknown), `status`, evidence; optional `flow_ids`, `invariant_ids`, `root_cause_ids` |
| `tasks` | `kind` (remediation/verification), `finding_ids`, `acceptance`; optional `depends_on` |

Use `schema_version: 1` at the top level. All IDs must be unique across the model. Model status is `candidate`, `supported`, or `unknown`; supported records require evidence references. The supported status is an analyst claim, not validated truth. Use `unknown` where evidence is missing. An optional project-specific extension can be maintained in the Markdown assessment; this initial JSON helper checks bundled SDP IDs only.

The tool rejects duplicate IDs, dangling references, unsupported enumerations, missing evidence for supported records and dependency cycles. It reports shared invariant and explicit shared-root-cause groups separately, unassigned findings, unknown trust/transaction relations, and topological waves based only on declared task dependencies. Waves are not a priority decision or authorization. It never promotes a candidate to a confirmed finding, infers causation, validates evidence accuracy, or claims a fix is verified. No raw evidence locators are included in the summary.
