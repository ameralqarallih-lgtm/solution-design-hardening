# Disposable infrastructure integration lab

These fixtures exercise real service APIs when run in Docker Compose. They are illustrative correctness experiments, not production implementations, compatibility certification or agent benchmark results. No container-backed tests were executed when preparing v0.7.0 (no Docker engine or client libraries were available). The workflow is supplied for reproducible execution, not represented as a successful CI run.

## Run the default lab

Requirements: Docker with Linux containers and Compose v2, internet access for the initial image pulls and dependency installation, sufficient local CPU and memory. Run from the repository root. Use a new, dedicated project name; never reuse a production Compose project name. The lab uses an internal network, no published ports, no host mounts, no external service URLs, and disposable fixture credentials. Do not enable `SDH_ISOLATED_LAB` outside this lab. The runner does not accept arbitrary endpoint overrides.

```sh
docker compose -p sdh-v070-lab -f integration/compose.yaml up --build --abort-on-container-exit --exit-code-from tests tests
```

Save the exit status and logs before cleanup. `0` means the selected test runner passed, not that all 235 problems are solved. A failed image pull, build or health check is a blocked test, not a product defect. The command executes 12 tests using PostgreSQL, Redis and RabbitMQ. CI runs the same lab on integration-file changes and manual dispatch.

Record the actual image IDs and dependency versions (ranges and image tags are not immutable pins):

```sh
docker compose -p sdh-v070-lab -f integration/compose.yaml images
docker compose -p sdh-v070-lab -f integration/compose.yaml run --rm --no-deps tests python -m pip freeze
```

When finished, remove only this disposable lab's containers and volumes:

```sh
docker compose -p sdh-v070-lab -f integration/compose.yaml down -v --remove-orphans
```

## Optional SQL Server lab

SQL Server Developer edition is a separate opt-in test target. Review [Microsoft's container deployment and license instructions](https://learn.microsoft.com/sql/linux/sql-server-linux-docker-container-deployment) first. It requires an appropriate license acceptance and an x86-64 Linux container host with adequate resources. Three tests cover local commit, rollback and stale rowversion rejection. The default CI lab does not run this optional service.

PowerShell, only after accepting the license terms:

```powershell
$env:SDH_ACCEPT_SQLSERVER_EULA = 'Y'
docker compose -p sdh-v070-sql -f integration/compose.yaml --profile sqlserver up --build --abort-on-container-exit --exit-code-from sqltests sqltests
# Capture exit status and logs before cleanup.
docker compose -p sdh-v070-sql -f integration/compose.yaml --profile sqlserver down -v --remove-orphans
Remove-Item Env:SDH_ACCEPT_SQLSERVER_EULA
```

On Bash use `export SDH_ACCEPT_SQLSERVER_EULA=Y` and unset it after cleanup. Do not use any real credentials. SQL Server is opt-in, not a mandatory technology.

## Failure experiments

| Service | Deliberate failure | Correctness assertion | Problem IDs |
|---|---|---|---|
| PostgreSQL | Child process terminates after business-only commit | Missing intent is reproduced | SDP-023, SDP-063 |
| PostgreSQL | Child terminates before or after atomic commit | Both rows absent or both durable | SDP-023, SDP-062, SDP-063 |
| PostgreSQL | Two connections read the last item before either updates | Unsafe path oversells; guarded update succeeds once | SDP-003, SDP-009, SDP-030 |
| Redis | Two clients interleave stale read and invalidation | Blind fill reintroduces old data; atomic generation check rejects it | SDP-019 |
| RabbitMQ + PostgreSQL | Connection closes after consumer DB commit, before ack | Redelivery occurs; unsafe effect duplicates; inbox effect remains once | SDP-024, SDP-055, SDP-065 |
| RabbitMQ | Mandatory confirmed publish to absent queue | Unroutable message is not treated as success | SDP-054, SDP-063 |
| RabbitMQ | Auto-ack followed by no business commit | Delivery is gone despite missing work | SDP-054, SDP-065 |
| RabbitMQ + PostgreSQL | Relay stops after broker confirm but before marking sent | Replay of stable ID leaves one durable effect | SDP-023, SDP-024, SDP-055 |
| SQL Server (optional) | Rollback/commit; stale rowversion | Atomic pair and rejected stale update | SDP-004, SDP-023 |

The Redis experiment uses real Redis commands but models the source-of-truth read; it does not prove cross-store atomicity, cache failover or eviction behavior. RabbitMQ connection-close tests are controlled disconnects, not broker crashes or network partitions. The relay gap is an explicit interruption boundary, not an OS kill of a relay process. PostgreSQL crash tests terminate an actual child client process, not the database server. Single-node lab results do not prove HA, multi-region guarantees or production throughput. No external payments are attempted.

Upstream semantics to check for the installed versions: [PostgreSQL isolation](https://www.postgresql.org/docs/17/transaction-iso.html), [Redis atomic scripting](https://redis.io/docs/latest/develop/interact/programmability/eval-intro/), [RabbitMQ acknowledgments and confirms](https://www.rabbitmq.com/docs/confirms), and [SQL Server rowversion](https://learn.microsoft.com/sql/t-sql/data-types/rowversion-transact-sql). Tags and dependencies should be pinned to reviewed digests/versions for repeatable benchmark campaigns. The sample tags and client ranges are not a security-audited lockfile.
