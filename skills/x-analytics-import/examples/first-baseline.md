# Example: First Baseline

## User request

> Use these overview and content exports to establish my first private X analytics baseline. A current video export is also available.

## Expected agent behavior

1. Resolve exact file paths and confirm they belong to one export run.
2. Run `inspect`.
3. Run `validate-only` and stop on errors.
4. Run `dry-run` and confirm zero writes.
5. Run `full-import` into a directory outside every repository.
6. Verify all artifacts and manifest hashes.
7. Run `incremental-import` with the same files.
8. Confirm the status is `already_imported`.
9. Report filenames, statuses, import ID, artifact paths, partial-day result, idempotency, and warnings without exposing exact metrics.

## Success condition

One completed baseline exists, duplicate protection is proven, and no raw CSV was copied.
