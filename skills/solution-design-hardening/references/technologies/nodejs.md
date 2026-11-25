# Node.js / TypeScript

Related baseline problems: SDP-030, SDP-035, SDP-044, SDP-122, SDP-143.

## Detection
Inspect Promise.all over unbounded collections, missing awaits, process-local locks, ORM transaction handles and unhandled cancellation.

## Implementation
Pass the same transaction client through all local writes; use bounded concurrency and AbortSignal where supported. Move CPU-heavy work away from the event loop; enforce uniqueness at the store.

## Pitfalls / counterexamples
Single-threaded JavaScript does not prevent interleaving across awaits or processes. Promise rejection does not cancel sibling work automatically.

## Verification
Run concurrent requests across two processes; interrupt between awaited calls; assert bounded active work and a single committed effect.

## Upstream reference
[Official documentation](https://nodejs.org/api/globals.html). Confirm installed versions and provider capabilities before selecting APIs. This is guidance, not a tested integration.
