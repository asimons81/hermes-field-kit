## Summary

Describe the change and the problem it solves.

## Evidence

For a skill contribution, explain the recurring workflow, practical use, and what was generalized or removed for public release.

## Validation

- [ ] `python scripts/validate.py`
- [ ] `python -m unittest discover -s tests -v`
- [ ] Changed documentation reviewed
- [ ] Examples and fixtures checked for private data
- [ ] No credentials or environment-specific secrets committed

## Skill checklist

Complete for new or changed skills. Otherwise mark not applicable.

- [ ] A Skill proposal issue exists
- [ ] Admission rule is satisfied
- [ ] Skill lives directly at `skills/<skill-name>/`
- [ ] `SKILL.md` follows the specification
- [ ] Positive and negative triggers are documented
- [ ] Tests cover activation and behavior
- [ ] Limitations and safety boundaries are documented
- [ ] Catalog metadata matches source
- [ ] Skill version changed according to SemVer
- [ ] Tap discovery and a fresh Hermes session were tested

## Scope

List follow-up work intentionally excluded from this pull request.

## Security and privacy

Describe tool permissions, data handling, publishing, filesystem, account, or consequential-action considerations.
