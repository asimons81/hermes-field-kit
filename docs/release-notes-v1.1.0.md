# Hermes Field Kit v1.1.0

Release date target: September 5, 2026

## Status

Release candidate. Pull-request static validation is green; fresh-profile Hermes runtime validation remains required before merge and publication.

## Headline

Field Kit 1.1.0 expands the kit from operational diagnosis into a fuller work loop:

```text
inspect -> diagnose -> plan -> execute -> verify -> hand off
```

The release adds three new experimental workflows and formally includes the three experimental skills added since 1.0.1.

## New experimental skills

### `hermes-session-handoff` 0.1.0

Produces a portable continuation packet for a fresh session, profile, machine, or compatible agent. It separates verified state from reported state, references authoritative artifacts, preserves decisions and blockers, identifies what must be re-verified, and ends with an exact launch prompt.

### `hermes-kanbanize` 0.1.0

Turns a settled conversation, plan, spec, or objective into a Hermes-native Kanban graph. It prefers complete vertical work slices, verifies blocking edges and the execution frontier, checks for duplicate work, reads persisted board state back, and keeps board creation separate from worker execution.

### `hermes-change-review` 0.1.0

Reviews completed work on three independent axes: Intent, Repository, and Verification. This prevents passing tests from hiding missing requirements, clean code from hiding the wrong implementation, or a plausible diff from turning into an unsupported completion claim.

## Experimental skills included since 1.0.1

- `dont-lie-to-me` 0.1.0
- `hermes-skill-consolidate` 0.1.0
- `what-have-we-done-today` 0.2.0

The resulting catalog contains thirteen stable skills and six experimental skills.

## Authoring contract improvements

The design guidance and authoring scaffold now sharpen:

- skill descriptions as precise routing pointers
- progressive disclosure for branch-specific or bulky reference material
- checkable completion criteria at each workflow phase
- executable Python contract tests for every published skill
- single-source-of-truth behavior rules
- environment/tool discovery instead of copying volatile facts into skills
- positive process instructions paired with explicit hard safety boundaries

## Validator hardening found during this release

The first 1.1.0 PR run exposed a Python-version discrepancy: the three new skills had JSON behavior cases but no executable `unittest` files. Python 3.13 correctly caused the hardening step to fail with zero discovered tests, while Python 3.11 allowed the old validator logic to treat `Ran 0 tests` as a pass.

The release branch now:

- adds deterministic executable contract tests for all three new skills
- requires every published skill to discover at least one executable contract test
- treats zero discovered tests as a release failure regardless of interpreter behavior
- includes an executable contract-test scaffold in the skill template
- runs `git diff --check` in pull-request CI

The corrected PR matrix passed Python 3.11 and 3.13 on both Ubuntu and Windows before this final CI hardening commit.

## Design lineage

This release was prompted by a review of Matt Pocock's MIT-licensed `mattpocock/skills` repository. The handoff, spec-to-ticket, and separate review-axis concepts were useful design inputs. Field Kit's implementations were independently written for Hermes Agent, preserve Field Kit's stricter publication contract, use Hermes-native Kanban concepts, and add evidence classification, hostile-content handling, mutation boundaries, behavior tests, and reproducibility requirements.

## Validation required before publication

Completed on the release branch:

- repository validator contract tests
- repository validation
- release-wave hardening validation
- catalog/frontmatter agreement
- hostile-content and privacy-oriented contract coverage
- pull-request CI on Python 3.11 and 3.13 across Ubuntu and Windows

Still required:

- final PR CI including the new `git diff --check` gate
- fresh disposable Hermes profile validation using the repository-qualified install flow
- post-merge validation against the exact merged commit
- annotated SemVer tag and verified non-draft GitHub release

Hermes Agent v0.21.0 (v2026.8.31) is the current upstream release at release-candidate preparation time. Compatibility will not be claimed until the fresh-profile validation step is actually observed.
