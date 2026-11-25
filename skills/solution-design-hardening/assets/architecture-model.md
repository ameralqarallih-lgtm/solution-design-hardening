# Solution architecture model

Scope / revision / date / environments / evidence sources / exclusions / authorization:

## Component inventory

| CMP ID | Component / role | Repository path / deployment unit | Owner / data authority | Technology and version | Status / evidence |
|---|---|---|---|---|---|

## Dependency and data-flow map

| FLOW ID | Source → target | Dependency type / data or effect | Transaction relation | Identity / trust crossing | Timeout, retry and recovery ownership | Evidence / unknowns |
|---|---|---|---|---|---|---|

Optional diagram: label declared build edges separately from supported runtime flows, include external/unknown nodes, do not expose secrets.

## Business operations and failure boundaries

| OP ID / step | Component / entry point | Action / durable effect | Commit or authorization boundary | Failure before / after | Replay, compensation, reconciliation | Evidence |
|---|---|---|---|---|---|---|

Record normal, duplicate, failure, cancellation and recovery branches separately. Do not infer execution order from source line order.

## Business invariants and enforcement

| INV ID | Safety / liveness requirement | Scope / owner | Enforcement / bypass paths | Consistency / freshness / recovery target | Evidence / missing requirements | Verification |
|---|---|---|---|---|---|---|

Use the [threat model](threat-model.md) for protected assets, trust and threat details; reference FLOW IDs instead of duplicating data.

## Root-cause correlation

| RC ID | Shared mechanism / confidence | FND IDs | INV / FLOW IDs | SDP IDs | Evidence per path / distinct residual risks | REM / verification task |
|---|---|---|---|---|---|---|

## Coverage and unresolved evidence

Operations reviewed / excluded / blocked; unknown edges, unverified deployment assumptions, missing ownership and requirements; evidence collection date and change invalidation; task references. Model completeness is not catalog coverage or proof of runtime correctness.
