# Design Principles

## Field-tested over fashionable

A skill must come from repeated real use. Popularity, novelty, and prompt cleverness are not substitutes for evidence.

## Trust over volume

The repository has no target number of skills. A small catalog that users can understand and verify is more valuable than a huge directory of unknown quality.

## Process predictability

A useful skill changes the agent's process in a repeatable way. It should define triggers, steps, completion criteria, and failure boundaries. Generic advice that does not alter behavior should be removed.

## Trigger precision

The description and `When to Use` section must make activation useful. Counter-triggers are equally important because a skill that loads for the wrong task consumes attention and can degrade results.

## Progressive disclosure

Keep always-needed instructions in `SKILL.md`. Move bulky references, platform-specific branches, templates, and scripts into supporting files that the skill can consult when needed.

## Reproducibility

A stranger should be able to install the skill, provide the documented inputs, and observe the intended discipline. Claims must be framed as behavior, not guaranteed business outcomes.

## Sanitization by design

Public skills contain reusable logic. Private overlays contain personal voice notes, analytics, credentials, endpoints, and unpublished strategy. The repository must never blur those layers.

## Safe defaults

A skill should not silently perform consequential actions, expose secrets, overwrite user data, or assume authorization. It must make approval boundaries and irreversible steps explicit.

## Maintenance is subtraction

Skills accumulate stale instructions easily. Improvements should replace weaker guidance rather than layer new prose on top of it. Shorter and sharper is often a successful revision.
