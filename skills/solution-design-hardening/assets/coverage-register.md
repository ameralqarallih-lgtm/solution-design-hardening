# Assessment coverage register

Use in Comprehensive mode. Process the catalog in bounded batches and update this register after each batch so work can resume in a fresh context without re-reading assessed ranges. `python tools/assessment_coverage.py <this file>` (optional) reports missing IDs and the next batch.

## Scope

| Field | Value |
|---|---|
| Repository revision / snapshot | |
| Catalog source | Repository `SOLUTION-DESIGN-PROBLEMS.md` or bundled catalog |
| Project-only ID prefix | |
| Excluded paths and reasons | |

## Batch log

| Batch | ID range | Components and paths covered | Date | Revalidate if changed |
|---|---|---|---|---|
| 1 | SDP-001-SDP-022 | | | |

## Coverage

One row per catalog ID. Status is one of: Fully Addressed, Partially Addressed, Not Addressed, Incorrectly Addressed, Not Applicable, Requires Verification. No ID is skipped silently; justify Not Applicable.

| ID | Status | Evidence (file, symbol) | Finding / task ID | Unknowns |
|---|---|---|---|---|
| SDP-001 | | | | |

## Next batch

- Next ID range:
- Pending verification:
- Evidence to revalidate after code changes:
