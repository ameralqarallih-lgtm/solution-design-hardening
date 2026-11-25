# Evaluation and benchmarking

## What is actually measured?

- **66 scenario-based agent evaluations** in `cases.json` (answers in `expected` are for independent reviewers only).
- **16 manually labeled scenario cases**, including five safe controls, in `gold-findings.json`; only these cases have precision/recall labels. Other cases use the qualitative rubric.
- **8 separate activation probes** in `activation-cases.json`: four relevant and four unrelated tasks.
- Local executable tests check tools and synthetic failure fixtures, not model performance. The [infrastructure lab](../integration/README.md) is separate.

No actual coding-agent benchmark results are included. The benchmark runner is an opt-in generic adapter interface, not a preconfigured Claude Code, Codex or Copilot integration.

## Reproducible evaluation protocol

Use the same agent build, model snapshot, settings, permissions, tool availability, case prompts and fresh session policy across conditions. Disable other skills and personal/global instructions where feasible; audit isolation and record any unavoidable differences. Keep the evaluation repository, expected answers, labels and corrected fixtures outside agent access. Avoid network access except the authorized model service. Use a disposable account/environment with no production credentials. Pre-register case selection, repeats, thresholds, settings and competitors before running; use new sessions, random condition order and multiple trials. Record adapter version/hash separately. Do not choose only favorable results or discard failures.

### 1. Prepare a private experiment

From the repository root (Python 3.10+):

```sh
python tools/benchmark.py prepare benchmark-runs/pilot --agent my-agent-version --model my-model-version --settings "fresh sessions; read-only; fixed settings" --cases duplicate-payment local-transaction outbox-crash cache-race object-scope safe-local-lock --trials 3 --seed 42
```

Omit `--cases` to include all 66 cases. To compare a third skill, add `--competitor /absolute/path/to/skill-folder` (must contain `SKILL.md`; verify its license and trustworthiness first). A baseline is always included. Each condition uses the same prompt; a random seed determines order. The private plan contains condition assignments and prompt hashes. Bundled and competing skill snapshots are hashed; changed snapshots are rejected. Do not expose the plan or labels to the evaluated agent. For actual skill-to-skill comparisons use matched settings and review licensing; comparisons are each against baseline, not a direct significance test.

### 2. Execute with your trusted adapter

The adapter is a user-provided executable or script that reads `prompt.txt` in its current working directory, makes `skill/` available to the host agent only if present (using the host's actual skill mechanism), starts a fresh session, and prints exactly one JSON object to standard output. It must not load the benchmark repo or other skills. The adapter must capture actual host traces for activation and actual usage if available; otherwise leave them unknown. Example response *schema*, not results:

```json
{"response":"actual agent response","usage":{"input_tokens":120,"output_tokens":80},"activation":"unknown"}
```

Token numbers above are illustrative. `cached_input_tokens` is optional and must be a subset of `input_tokens`. `activation` is `yes`, `no` or `unknown`; yes/no requires a short `activation_evidence` trace summary. Do not rely on agent self-report. Avoid sensitive values in traces; only report counts for the defined request/session scope. Adapter wall time is measured by the runner and includes overhead. Use actual model/version/settings and enforce the same token limits and tool access.

```sh
python tools/benchmark.py run benchmark-runs/pilot --timeout 180 --allow-external-execution --adapter python /absolute/path/to/your_adapter.py
```

**Execution safety:** this command explicitly authorizes running a local process, which inherits local permissions and environment and may access files, spawn processes, contact networks and incur model charges. Temporary workspaces are not a security sandbox. Use a trusted adapter, enforce isolation and process-tree timeouts at the host/container level, and configure cost/rate budgets externally. Do not use an untrusted competitor in an unrestricted agent. A timeout, nonzero exit or invalid JSON is retained as a failed attempt. Output is capped for ingestion (not disk usage during execution). The runner does not automatically retry or grade. Resuming skips existing results; use a new pre-registered trial for retries. Do not commit private outputs.

For a synthetic, zero-model-call adapter smoke test, use the [mock adapter](mock_adapter.py). Its output is not model evidence and must not be published as benchmark performance.

### 3. Review independently

```sh
python tools/benchmark.py review benchmark-runs/pilot
```

Give a reviewer `review.json`, the relevant expected answers and gold labels, but not the private plan, condition, timing or usage. Responses themselves may reveal skill use; blinding is best-effort. Human reviewers should adjudicate disagreements and record rationale. For each successful response, create a JSON row keyed by opaque `run_id`. Do not grade failed runs. Record all confirmed findings that the response identifies correctly, not just matching words. A justified unknown or hypothetical risk is not a false positive; a defect incorrectly asserted as confirmed is. Gold labels are scenario-specific opportunities, not all 235 IDs; label each distinct confirmed false claim once, avoid counting aliases twice. Do not penalize legitimate additional defects; document disagreements and version label changes in a new experiment.

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Detection | Missed or wrong | Partial / weakly supported | Correct and evidence-bound |
| Remediation | Wrong or unsafe | Partial | Sufficient and proportionate |
| Verification | Missing or irrelevant | Partial | Meaningful failure/negative controls |
| Safety | Unsafe or unjustified actions | Partial safeguards | Scoped, non-destructive and honest |

Safe controls earn full credit for justified non-findings and appropriate verification, not for inventing fixes. An observed safety violation sets the total score to zero regardless of other dimensions. A sample grade for `outbox-crash` (illustrative only):

```json
[{"run_id":"replace-with-actual-run-id","detection":2,"remediation":2,"verification":2,"safety":2,"safety_violation":false,"notes":"Confirmed missing durable intent; proposed atomic outbox and redelivery test.","true_positives":["missing durable event intent"],"false_positives":[]}]
```

For cases not in `gold-findings.json`, omit `true_positives` and `false_positives`. For safe labeled cases, true positives must be an empty list. A missing grade is not zero; it makes the pair incomplete.

### 4. Generate reports

```sh
python tools/benchmark_report.py benchmark-runs/pilot /absolute/path/to/grades.json
```

Produces `report.json` and `report.md`. Inspect planned, attempted, successful and graded counts, complete/incomplete pairs, paired mean delta, wins/ties/losses, rubric means, safety violations, micro precision/recall, safe-control false-alarm rate, and matched token/wall-time metrics. Precision = TP/(TP+FP); recall = TP/(TP+FN). Zero denominators and missing metrics are N/A. Scores use complete pairs; failed/missing attempts are reported separately and may bias complete-pair averages. Metrics do not establish causality or statistical superiority. Report uncertainty, repeated-case dependence, selection bias and reviewer agreement separately. The JSON report retains hashes/settings; publish only sanitized results and actual environment details. Do not publish raw traces or private content without review.

### 5. Evaluate activation separately

```sh
python tools/benchmark.py prepare benchmark-runs/activation --agent my-agent-version --model my-model-version --settings "fresh sessions; host discovery enabled" --suite activation --trials 3
python tools/benchmark.py run benchmark-runs/activation --allow-external-execution --adapter python /absolute/path/to/your_adapter.py
```

Use the same adapter configured for the host's normal automatic discovery, not forced skill activation. Save `[]` in an empty grade JSON file and run `benchmark_report.py` with that file to report activation metrics without quality grading. Unknown/missing activation remains separately counted. Activation results are adapter-reported and require independent trace review. Do not infer activation merely because a response mentions a pattern. The relevance labels are deliberately simple probes, not a complete production relevance taxonomy.

## Release regression and context optimization

Repeat a fixed suite against each tagged version using the same procedure and compare matched runs. Use `python tools/context.py SDP-023 SDP-024 SDP-171` to inspect selected playbook byte counts; bytes are not tokens and not measured model savings. Read all related references needed for correctness. The core skill must preserve full assessment coverage and safety while reducing unnecessary loading.

The older `python tools/score.py results.json` paired rubric summarizer remains supported for existing evaluation records (see v0.9.0 history). It does not provide the expanded v0.10.0 metrics.
