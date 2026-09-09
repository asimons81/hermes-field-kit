# Example: repository work moving to a fresh session

## Handoff Outcome

`HANDOFF WITH GAPS`

## Continuation Objective

Finish the pending feature review and prepare the pull request for merge.

## Verified State

- `VERIFIED DONE`: feature branch exists at commit `abc1234`.
- `VERIFIED DONE`: repository tests observed passing at that commit.

## Reported or Unverified State

- `REPORTED DONE`: the previous session said staging was manually tested, but no current staging evidence is available.

## Decisions Already Made

- Keep the existing persistence layer.
- Do not introduce a second scheduler.

## Active Work and Blockers

- `IN PROGRESS`: compare the implementation with issue #42.
- `UNKNOWN`: current staging behavior.

## Authoritative Artifacts

- Issue #42
- `docs/feature-spec.md`
- commit `abc1234`

## What Must Be Re-Verified

- staging behavior
- current CI status if the branch moved

## First Next Action

Read issue #42 and compare it with the diff from the merge base to `abc1234`.

## Fresh-Session Prompt

Continue the feature review for issue #42. Treat `docs/feature-spec.md` and commit `abc1234` as the primary artifacts. The test result at `abc1234` was verified, but staging was only reported as tested, so re-verify staging before any merge recommendation. Preserve the decision to keep the existing persistence layer and avoid a second scheduler. First, compare issue #42 against the branch diff and list any missing behavior or scope creep.
