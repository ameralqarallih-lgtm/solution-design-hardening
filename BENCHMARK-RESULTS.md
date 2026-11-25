# v1.0.0-RC1 benchmark results

The six-case Ollama pilot completed 36 requests and yielded 18 paired comparisons. The default infrastructure lab passed 12 tests. The model review exposed safety and false-alarm problems in both conditions. This record supports a prerelease and follow-up validation.

## Model pilot

| Setting | Value |
|---|---|
| Run date | 2026-11-25 |
| Provider | Ollama 0.40.15, local Chat Completions relay to `/api/chat` |
| Model | `qwen3:8b`, Q4_K_M, manifest SHA-256 `500a1f067a9f782620b40bee6f7b0c89e17ae61f686b92c24933e4ca4b2b8b41` |
| Cases | `duplicate-payment`, `local-transaction`, `outbox-crash`, `cache-race`, `object-scope` and `safe-local-lock` |
| Trials | Three per case per condition, seed 42 for condition order |
| Request parameters | Fresh requests, `think=false`, `num_ctx=16384`, `num_predict=512`, `temperature=0.3` |
| Skill condition | Fixed `SKILL.md`, detection guidance and pattern guidance from the v0.11.0 snapshot |
| Common instruction | Answer in at most 150 words. Use up to four short bullets for evidence, minimal safeguards and verification. Include uncertainty when the scenario omits evidence. |
| Review | 36 provisional Codex rubric grades from the response-only packet. Human adjudication is pending. |

| Result | Baseline | Skill guidance |
|---|---:|---:|
| Successful / planned | 18 / 18 | 18 / 18 |
| Mean score, out of 8 | 3.111 | 3.056 |
| Safety flags | 3 | 3 |
| True positive labels | 7 | 8 |
| False positive reports | 14 | 11 |
| Missed positive labels | 8 | 7 |
| Precision | 33.3% | 42.1% |
| Recall | 46.7% | 53.3% |
| Safe controls with a false alarm | 5 / 6 | 6 / 6 |
| Mean input tokens | 105.5 | 5,342.5 |
| Mean output tokens | 105.7 | 101.1 |
| Mean wall time | 5.49 s | 6.57 s |
| Output limits reached | 0 | 0 |

The mean paired score difference was −0.056 out of 8. The outbox scenario exposed recommendations that assumed a local transaction could make a database commit and broker publish atomic. All six responses for the process-local counter flagged the absence of cross-process coordination despite the stated local-only invariant. Treat these findings as provisional until another reviewer adjudicates the grades. This pilot covers one model and six synthetic cases. Provider billing and cache metrics were unavailable.

The exploratory outbox pair completed both requests. A separate diagnostic pilot stopped after 18 recorded responses hit the output cap. It was followed by a fresh run with the same concise-answer instruction in both conditions. The table above uses only the fresh run. The release runner now records API output-limit signals in the reports.

## Infrastructure

The default `integration/compose.yaml` lab ran in an isolated Compose project with Docker Engine 29.9.3 and Compose 5.7.1. All 12 PostgreSQL, Redis and RabbitMQ tests passed. The test services used PostgreSQL 17.11, Redis 7.4.12 and the RabbitMQ 4.1 image. The Python clients were psycopg 3.3.9, redis 6.4.0 and pika 1.5.0. The optional SQL Server profile remains pending.

## Release follow-up

Stable promotion requires the full 18-pair pilot on two live models, an independent review of the rubric decisions, and passing default infrastructure tests. The skill condition must show zero confirmed unsafe remedies and zero false alarms on the labeled safe controls in each pilot. Native skill activation also needs a trace-backed check. The complete local review packets, raw responses, and diagnostic attempts are retained outside the tracked source.

### Independent review and repeat pilots

A second reviewer graded the original 36 responses without condition labels or previous scores. The reviewers agreed on 31 of 36 safety overrides. The reconciled review records three unsafe remedies. It counts the payment branch that commits its local claim after a provider charge, the local transaction check that assumes pre-transaction validation ensures consistency, and the outbox answer that relies on a successful commit and reliable broker to cover the intervening crash. Four disputed alternatives reduced detection or remediation scores because they omitted guarantees or targeted a hypothetical reverse order. Both reviewers flagged all six local-counter responses for inventing a need for cross-process coordination.

The revised skill leads with the stated operation order and invariant scope. It makes a successful provider call followed by a lost response, a commit followed by an interrupted publish, and a stale cache fill after invalidation explicit. It also asks for a scoped non-finding when the stated local boundary already suffices.

| Run, 18 pairs each | Baseline score / 8 | Skill score / 8 | Unsafe remedies, baseline / skill | Safe-control false alarms, baseline / skill |
|---|---:|---:|---:|---:|
| Original Ollama pilot, reconciled review | 3.111 | 3.333 | 2 / 1 | 4 / 6 |
| First revised Ollama pilot | 1.944 | 5.000 | 7 / 5 | 4 / 0 |
| Final revised Ollama pilot | 2.611 | 4.333 | 5 / 7 | 4 / 0 |
| Codex CLI with `gpt-6.2-sol` and pre-follow-up guidance | 7.833 | 7.944 | 0 / 0 | 0 / 0 |

The two Ollama repeats used the original sampling settings and six labeled cases. Both cleared the skill condition's safe controls. The final repeat identified stale refill in all three skill responses for that case, and two proposed a version-aware fill test. The outbox and payment responses still claimed a local transaction could cover the independent effect, and one cache remedy still allowed the stale refill. The final candidate therefore missed the safety gate. Independent model grades remain provisional. Sampling and reviewer differences limit comparisons across runs.

The second live provider was Codex CLI `0.171.0-alpha.13.2` using the signed-in ChatGPT account. All 36 responses completed using the built-in fixed-prompt adapter and the same six cases, order seed and repeats. The Codex run used its own model and default generation settings. It detected all 15 labeled positive opportunities in each condition. Independent review recorded one overclaim about downstream invoice authorization under skill guidance.

### Native Codex activation

The [native adapter](evals/codex_native_adapter.py) completed eight installed-skill probes and eight baseline probes with the same Codex build and model in a read-only sandbox. The four irrelevant tasks had no observed skill reads. The four relevant tasks produced trace evidence of an attempted read of the installed `SKILL.md`. The Windows host rejected those commands, so their activation remains unknown. Repeating the outbox probe inside the project workspace produced the same rejection. A trace with successful file reads is still needed to verify native activation.
