# Example: Recurring Refresh

## User request

> Process my newest X analytics exports and tell me what changed since the previous import.

## Expected agent behavior

1. Identify the newest matching export set by exact path, date range, and modification time.
2. Run `inspect`, `validate-only`, and `dry-run`.
3. Run `incremental-import` only when the gates pass.
4. Stop cleanly when the source set is already imported.
5. When a new snapshot is created, compare it with the previous completed snapshot.
6. Use overlapping dates and matched post IDs.
7. Separate new posts, removed posts, post types, lanes, and outliers.
8. Report confidence and sample size; keep exact sensitive values local unless requested.

## Success condition

The source set is represented exactly once and the comparison does not confuse rolling-window changes with matched-period changes.
