# Evaluation and benchmarking

## What is actually measured?

- **66 scenario-based agent evaluations** in `cases.json` (answers in `expected` are for independent reviewers only).
- **16 manually labeled scenario cases**, including five safe controls, in `gold-findings.json`; only these cases have precision/recall labels. Other cases use the qualitative rubric.
- **8 separate activation probes** in `activation-cases.json`: four relevant and four unrelated tasks.
- Local executable tests check tools and synthetic failure fixtures, not model performance. The [infrastructure lab](../integration/README.md) is separate.

Live fixed-prompt pilots have run on local Ollama and Codex CLI; see [benchmark results](../BENCHMARK-RESULTS.md). Human adjudication, trace-backed native activation and a paired comparison of the RC2 adaptive context remain pending. The built-in runner and custom adapter protocol share the paired experiment format and evaluation rubric.

## Built-in benchmark commands

Run from the repository root with Python 3.10+. Start with the zero-model-call smoke test.

```sh
python tools/benchmark.py doctor
python tools/benchmark.py evaluate benchmark-runs/smoke --agent mock --cases outbox-crash
```

The smoke test creates one baseline response and one skill response, a grading template and three report files. The results are labeled synthetic.

| Agent argument | Provider or CLI | Model access and configuration |
|---|---|---|
| `codex` | Codex CLI | Install `codex` on PATH and sign in. |
| `claude-code` | Claude Code CLI | Install `claude` on PATH and sign in or configure its supported authentication. |
| `copilot` | GitHub Copilot CLI | Install `copilot` on PATH and sign in or set a supported GitHub token. |
| `ollama` | Ollama Chat Completions | Start the local server and choose a model from `ollama list`. Default URL `http://127.0.0.1:11434/v1`. |
| `litellm` | LiteLLM Chat Completions | Use the served model alias. Default URL `http://127.0.0.1:4000/v1`. If protected, pass `--api-key-env LITELLM_API_KEY`. |
| `lm-studio` | LM Studio Chat Completions | Start the local server and use a served model ID. Default URL `http://127.0.0.1:1234/v1`. |
| `openai` | OpenAI Chat Completions | Set `OPENAI_API_KEY` and select a Chat Completions model. |
| `openai-compatible` | Other Chat Completions endpoint | Set `--base-url` or `OPENAI_BASE_URL` and, if needed, `--api-key-env`. |

API base URLs point to the API prefix, typically ending in `/v1`. The runner appends `/chat/completions`. Use `--api-key-env` with an environment variable name. Use HTTPS for remote credentialed endpoints.

`doctor` checks CLI versions, required flags, and available local login or credential signals. For a live connectivity check, pass `--probe --allow-external-execution` with one agent and model. A live probe sends one short request and can incur charges. For example, in PowerShell set `$env:BENCHMARK_MODEL` to an accessible Codex model before running the following commands.

```powershell
python tools/benchmark.py doctor --agent codex --model "$env:BENCHMARK_MODEL" --probe --allow-external-execution
python tools/benchmark.py evaluate benchmark-runs/codex-pilot --agent codex --model "$env:BENCHMARK_MODEL" --suite pilot --trials 3 --allow-external-execution
```

`pilot` selects six cases, including two safe controls. `scenario` selects all 66 cases. Pass `--cases` to select specific IDs. For reproducibility, pin the model and CLI version where possible, choose the trial count and seed in advance, and use the same case set for each agent. `--config` accepts a JSON object with `agent`, `model`, `base_url`, `api_key_env`, `suite`, `cases`, `trials`, `seed`, `timeout`, `settings` and the optional judge fields `judge_model`, `judge_base_url` and `judge_api_key_env`. Command-line values override the config. Keep key values in environment variables.

Built-in scenario runs supply the same scenario text to both conditions. By default (`--context-mode fixed_prompt_guidance`) the skill condition also receives `SKILL.md`, `DETECTION-GUIDANCE.md` and `PATTERN-GUIDANCE.md` from the hashed snapshot, as in the RC1 pilot. `--context-mode core` sends only `SKILL.md`, the Level 1 core. Routed problem files are never added, because choosing them per case would leak the expected problem IDs. The reference set is the same for all cases, and a resumed experiment must keep its context mode. Host-native discovery and the effects of the full reference library require separately configured custom-adapter experiments. CLI attempts use fresh temporary workspaces and restrictive tool settings. Run on a dedicated test account or isolated host when you need to control managed configuration, inherited permissions and subprocesses.

### Resume and retry

```sh
python tools/benchmark.py evaluate benchmark-runs/codex-pilot --resume --allow-external-execution
python tools/benchmark.py evaluate benchmark-runs/codex-pilot --resume --retry-failed --retries 1 --allow-external-execution
```

Resume uses the saved experiment configuration and skips completed attempts. `--retry-failed` reopens failed runs while preserving their prior attempts. `--retries N` permits up to N additional attempts for a retryable transport failure during the invocation. Authentication and invalid configuration stop the run with an actionable status. Because retries can affect results, apply the same pre-registered retry policy when comparing experiments and inspect coverage for each condition.

### Grade and report

Pass `--judge-model` to grade successful responses using a different model through a Chat Completions endpoint. For a CLI agent the judge uses the OpenAI endpoint by default. For an API agent it uses that agent's endpoint. Use `--judge-base-url` and `--judge-api-key-env` to select a separate endpoint and its key. Judge calls receive the scenario, expected behavior, gold labels when available, and the response. The review packet omits the condition assignment. The response can still reveal skill use.

Automated grades are saved to `grades.provisional.json`. For manual grading or adjudication, work from `grades.template.json` and `review.json`, save completed rows in `grades.json` and remove unfilled rows. A human grade takes precedence for its run ID. Refresh the reports as follows.

```sh
python tools/benchmark_report.py benchmark-runs/codex-pilot
```

The Markdown and JSON reports distinguish human from provisional model grades, show missing pairs, and include available host-reported tokens, elapsed wall time and provider-reported USD cost for evaluated attempts. Missing billing data appears as unavailable. The SVG charts execution coverage and includes paired scores when grades exist. Run `compare` after completing two or more experiments with matching cases, trials, seed and skill snapshot.

```sh
python tools/benchmark.py compare benchmark-runs/comparison benchmark-runs/codex-pilot benchmark-runs/claude-pilot
```

Provider command and API references. [Codex non-interactive mode](https://developers.openai.com/codex/noninteractive) · [Claude Code CLI](https://code.claude.com/docs/en/cli-reference) · [GitHub Copilot CLI](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference) · [OpenAI Chat Completions](https://developers.openai.com/api/reference/resources/chat) · [Ollama compatibility](https://docs.ollama.com/api/openai-compatibility) · [LiteLLM Gateway](https://docs.litellm.ai/docs/proxy/quick_start) · [LM Studio Chat Completions](https://lmstudio.ai/docs/developer/openai-compat/chat-completions)

## Custom adapter and independent review protocol

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

Produces `report.json`, `report.md` and `report.svg`. Omit the grades argument for an execution-only report or to use the default grade files if present. Inspect planned, attempted, successful and graded counts, complete/incomplete pairs, paired mean delta, wins/ties/losses, rubric means, safety violations, micro precision/recall, safe-control false-alarm rate, and matched token/wall-time metrics. Precision = TP/(TP+FP); recall = TP/(TP+FN). Zero denominators and missing metrics are N/A. Scores use complete pairs; failed/missing attempts are reported separately and may bias complete-pair averages. Metrics do not establish causality or statistical superiority. Report uncertainty, repeated-case dependence, selection bias and reviewer agreement separately. The JSON report retains hashes/settings; publish only sanitized results and actual environment details. Do not publish raw traces or private content without review.

### 5. Evaluate activation separately

```sh
python tools/benchmark.py prepare benchmark-runs/activation --agent my-agent-version --model my-model-version --settings "fresh sessions; host discovery enabled" --suite activation --trials 3
python tools/benchmark.py run benchmark-runs/activation --allow-external-execution --adapter python /absolute/path/to/your_adapter.py
```

Use the same adapter configured for the host's normal automatic discovery, not forced skill activation. Save `[]` in an empty grade JSON file and run `benchmark_report.py` with that file to report activation metrics without quality grading. Unknown/missing activation remains separately counted. Activation results are adapter-reported and require independent trace review. Do not infer activation merely because a response mentions a pattern. The relevance labels are deliberately simple probes, not a complete production relevance taxonomy.

For a signed-in Codex CLI with the model below available, use the included [native adapter](codex_native_adapter.py). It installs the snapshot under `.agents/skills` in a fresh work directory and records the CLI trace. A successful recorded read of the installed skill body counts as activation. A rejected or failed read counts as unknown. A completed turn with no matching read is reported as no observed activation under this adapter. Arguments after `--adapter` go to the adapter: its `--timeout` (default 180 seconds) stops the Codex probe, and the runner's own `--timeout` before `--adapter` should be longer so the adapter can report the result.

```sh
python tools/benchmark.py prepare benchmark-runs/activation-codex --agent codex --model gpt-6.2-sol --settings "native discovery with a read-only sandbox" --suite activation --trials 1
python tools/benchmark.py run benchmark-runs/activation-codex --timeout 200 --allow-external-execution --adapter python evals/codex_native_adapter.py --model gpt-6.2-sol --timeout 180 --trace-dir benchmark-runs/activation-codex/trace.private
python tools/benchmark_report.py benchmark-runs/activation-codex
```

## Release regression and context optimization

Repeat a fixed suite against each tagged version using the same procedure and compare matched runs. Use `python tools/context.py --mode focused SDP-023 SDP-024 SDP-171` to inspect the routed files and their estimated tokens (characters / 4); estimates are not model tokens and not measured savings. Read all related references needed for correctness. The core skill must preserve full assessment coverage and safety while reducing unnecessary loading.

To measure the RC2 adaptive context with and without optimization, run the same pilot against an RC1 snapshot and the current skill. Use the same model, settings, cases, trials and seed, and `--context-mode core` for both. Each experiment pairs a baseline with one skill snapshot. Compare the skill conditions' input tokens, scores, safety flags, safe-control false alarms and labeled recall. The activation suite checks that the unchanged description still activates on relevant tasks only. The local regression `test_context_routing.py` checks that every problem stays routable and that the guidance never limits reading, and `test_knowledge.py` fails if any pre-RC2 guidance statement disappears from the skill tree.

The older `python tools/score.py results.json` paired rubric summarizer remains supported for existing evaluation records (see v0.9.0 history). It does not provide the expanded v0.10.0 metrics.
