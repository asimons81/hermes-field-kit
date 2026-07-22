# Safety and Authority

- Back up the target before any import.
- Never display or include secrets in the ordinary migration archive.
- Never activate an imported session database blindly.
- Stage and verify archives outside live Hermes directories.
- Reject path traversal, absolute archive paths, hash mismatches, and unexpected files.
- Import cron jobs disabled and gateway configuration inactive until reviewed.
- Stop on integrity failures and preserve rollback artifacts.

## Approval boundary

The skill may recommend a mutation, but it must not perform one until the user separately and explicitly approves the exact action after reviewing the report.
