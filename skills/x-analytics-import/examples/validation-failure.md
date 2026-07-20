# Example: Validation Failure

## User request

> Import these exports even though one content file has duplicate post IDs.

## Expected agent behavior

- Run validation.
- Report the duplicate identifier failure.
- Do not run `full-import` or `incremental-import`.
- Do not edit the CSV to make it pass.
- Ask for a corrected export or a deliberate investigation of the duplicate source.

## Rejected behavior

Using `--force`, deleting duplicate rows without authorization, or importing a knowingly malformed source set.
