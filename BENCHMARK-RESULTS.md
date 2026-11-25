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

Adjudicate the safety flags and safe controls, exercise a second live model and native skill activation, and record acceptance criteria before promoting a stable release. The complete local review packet, raw responses, and diagnostic attempts are retained outside the tracked source.
