# Verdict Rules

## Decision Order

Apply these rules in order.

### 1. NOT READY

Return `NOT READY` when any blocker exists.

Blockers include:

- repository identity cannot be established
- unfinished merge, rebase, cherry-pick, revert, or unresolved conflict
- required test or validation command failed
- required CI check failed, timed out, was cancelled, or was skipped without an
  accepted exception
- requested changes or unresolved required review remain
- required work is open, unmerged, or absent from the audited branch
- material security warning remains unresolved
- required migration, generated file, lockfile, or environment contract is
  missing or contradictory
- critical documentation or plan claims contradict implementation for handoff,
  onboarding, or release work
- unexplained dirty state makes the stated goal unsafe
- an audit command unexpectedly modified the repository
- access to a critical surface required by the user's stated goal is unavailable
- evidence is materially contradictory and cannot be reconciled

### 2. READY WITH WARNINGS

Return `READY WITH WARNINGS` only when:

- no blockers exist
- the stated next step can safely proceed
- one or more non-blocking warnings or secondary unverifiable areas remain

Examples:

- local development can proceed, but remote branch freshness was not fetched
- optional platform CI was not available
- minor secondary documentation is stale
- cleanup debt or stale branches exist but do not affect the current branch
- tests pass but a non-required validation surface was unavailable

Important GitHub or CI access gaps may be warnings for local exploratory
development, but are blockers for claims such as "everything is merged",
"release ready", or "safe handoff" when those surfaces are essential.

### 3. READY

Return `READY` only when:

- zero blockers exist
- zero material warnings exist
- all readiness surfaces required for the stated goal were verified
- repository state is explainable
- required tests and CI passed for the relevant commit
- required reviews and merges are complete
- documentation and plans materially align
- no important area remains under Not Verified

## Distinctions

### Clean Worktree

A clean worktree means only that Git reported no modified, staged, or untracked
files under the checks performed. It does not prove:

- branch synchronization
- CI status
- test status
- review completion
- documentation accuracy
- release readiness

### Passing Tests

Passing tests prove only that the observed commands passed in the observed
environment. They do not prove:

- CI matrices or required checks passed
- pull requests are reviewed or merged
- documentation is current
- migrations and generated files are correct
- dependencies are secure
- release artifacts are ready

### Warnings versus Blockers

Use the user's stated next step as the boundary.

- A warning creates risk but does not prevent that next step.
- A blocker prevents the next step or makes a ready claim unsafe.
- When uncertain, explain the dependency explicitly rather than inflating the
  verdict.

## Deterministic Summary

```text
blockers > 0                                      => NOT READY
critical_unverified > 0                           => NOT READY
blockers == 0 and (warnings > 0 or unverified > 0) => READY WITH WARNINGS
blockers == 0 and warnings == 0 and unverified == 0 => READY
```
