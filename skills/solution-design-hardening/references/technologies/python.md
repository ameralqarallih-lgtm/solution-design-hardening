# Python / FastAPI / Django / SQLAlchemy

Related baseline problems: SDP-004, SDP-023, SDP-030, SDP-035, SDP-141.

## Detection
Inspect async endpoints using blocking clients, session sharing across tasks, transaction context boundaries and process-local locks.

## Implementation
Use a session per request/task as appropriate; use transaction context managers and database constraints. Keep blocking work bounded and outside the event loop. Use durable workers for work that must survive process exit.

## Pitfalls / counterexamples
An asyncio.Lock is process-local; background callbacks are not a durable queue; SQLite tests do not prove production database isolation.

## Verification
Use independent sessions against the production database engine in a disposable environment; cancel requests and assert sessions are closed and committed effects recoverable.

## Upstream reference
[Official documentation](https://docs.sqlalchemy.org/en/20/orm/session_basics.html). Confirm installed versions and provider capabilities before selecting APIs. This is guidance, not a tested integration.
