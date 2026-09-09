# Hermes Field Kit v1.1.0

Release date target: September 5, 2026

## Status

Release candidate. Pull-request static validation is green; fresh-profile Hermes runtime validation was observed and recorded below (pinned raw-URL lifecycle, Hermes v0.21.1). Post-merge steps — validation against the exact merged commit, annotated tag, and the published release — remain.

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

## Fresh-profile runtime validation (observed)

Validated on 2026-09-09 with Hermes Agent v0.21.1 (2026.9.7, install method git, local revision c076d653 with one carried commit) on Arch Linux, against pre-merge release-branch head daa74b756cd318854a8840b7a365c0eb98c5ec64.

Pinned raw-URL review install (`https://raw.githubusercontent.com/asimons81/hermes-field-kit/daa74b7.../skills/hermes-session-handoff/SKILL.md`) into a fresh disposable profile:

- Fetch, quarantine, and security scan succeeded. Verdict SAFE; decision ALLOWED (community source, safe verdict); scanner skills-guard-v2, scan provenance fresh, rules none.
- Installed files: SKILL.md only. A pinned raw-URL install intentionally carries the single SKILL.md, not the full bundle (tests, examples, references). Consumers who need the complete skill directory should clone or copy per docs/installation.md.
- `hermes skills check` reported `up_to_date` against the pinned revision — the v0.19.0 `update_available` false-positive quirk documented in docs/installation.md did not reproduce on v0.21.1.
- `hermes skills uninstall` removed the skill cleanly and a subsequent `skills list` confirmed absence.

The repository-qualified identifier path (`asimons81/hermes-field-kit/hermes-session-handoff`) was also attempted on v0.21.1: the fetch stalled after `Fetching:` with no install, quarantine entry, or error surfaced. 1.1.0 therefore claims the pinned raw-URL lifecycle only; registry-path compatibility remains untested on this Hermes version and keeps the existing caveat in docs/installation.md.

Post-merge steps still required: validation against the exact merged commit, annotated SemVer tag, and a non-draft GitHub release published from this file.