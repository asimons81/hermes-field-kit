# Example: tests pass, but the requested behavior is incomplete

## Change Review

Post-build review of `feature/export` against issue #42 and the branch merge base.

## Disposition

`CHANGES REQUIRED`

## Review Target

`feature/export` compared with its merge base against `main`.

## Intent

`BLOCKER`: issue #42 requires authenticated users to download both JSON and CSV exports. The diff implements JSON only.

## Repository

No blocking repository-rule violation found. The implementation reuses the existing export module and error contract.

## Verification

Observed unit and integration tests pass for JSON export. No CSV behavior exists to validate.

## Blockers

- Missing CSV export required by issue #42.

## Non-Blocking Findings

None.

## Not Verified

Browser download behavior was not exercised in the available environment.

## Recommended Next Action

Implement the missing CSV path at the same export seam, add behavior coverage, then rerun this review against the same fixed point.
