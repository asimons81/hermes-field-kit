# Example: Clean Worktree but Failing CI

# Repository Readiness Audit

## Verdict

NOT READY

Goal: handoff
Audited repository: example-repo at `/work/example-repo`
Audited commit: `main` at `def5678`
Audit timestamp: 2026-07-22 14:00 America/Chicago

## Repository State

The working tree is clean and the current branch tracks the remote default
branch. This does not establish handoff readiness.

## Recent Work

The latest commit changed database migration and generated schema files.

## Pull Requests and Reviews

The implementation pull request is merged, but its latest required CI run
contains a failing migration verification job.

## Issues and Blockers

Blocker: required migration verification failed for the audited commit.

## CI and Tests

Local unit tests passed. Required CI job `migration-check` failed. Passing local
tests do not override the required CI failure.

## Documentation and Plan Alignment

The handoff guide claims migration verification passes, contradicting current
CI evidence.

## Risks and Warnings

None separate from the blocker.

## Not Verified

No additional platform-specific manual test was performed.

## Recommended Next Actions

Diagnose the migration job, update the handoff documentation after verification,
and rerun the audit. These recommendations do not authorize changes.

## Evidence Summary

Clean Git state was verified, but the required CI run for `def5678` failed and
the handoff guide is stale.
