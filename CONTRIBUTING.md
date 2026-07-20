# Contributing

Hermes Field Kit is curated rather than exhaustive. Contributions are evaluated for usefulness, reproducibility, safety, and evidence of real use.

## Before opening a pull request

- Read the [design principles](docs/design-principles.md).
- Read the [skill specification](docs/skill-specification.md).
- Search existing issues and pull requests.
- For a new skill, open a **Skill proposal** issue first.
- Remove credentials, private data, personal analytics, unpublished material, and environment-specific identifiers.

## What qualifies as a skill contribution

A proposed skill must:

1. Solve a concrete, recurring task.
2. Have been used in a real workflow.
3. Change agent behavior in a useful and explainable way.
4. Include positive and negative trigger examples.
5. Include behavior-oriented test cases.
6. Document limitations, dependencies, and safety boundaries.
7. Pass `python scripts/validate.py`.

A generated collection, speculative prompt, or thin rewording of an existing skill will not be accepted.

## Repository changes

Specification, documentation, tooling, and governance improvements may be submitted without a skill proposal issue. Explain the problem, the chosen approach, and the validation performed.

## Development workflow

```bash
git clone https://github.com/asimons81/hermes-field-kit.git
cd hermes-field-kit
git switch -c <type>/<short-description>
python scripts/validate.py
```

Use focused branches such as:

- `docs/clarify-installation`
- `tooling/validate-frontmatter`
- `skill/social-media/example-name`

Prefer Conventional Commit-style subjects:

- `docs: clarify skill admission criteria`
- `feat: add catalog validation`
- `fix: reject mismatched catalog paths`

## Pull requests

A pull request should be small enough to review as one coherent change. Complete the pull-request checklist and include:

- What changed
- Why it changed
- Evidence or reproduction steps
- Validation performed
- Security or privacy considerations
- Follow-up work that is intentionally out of scope

## Skill review standard

Maintainers will check:

- Admission rule
- Trigger precision
- Hermes compatibility
- Reproducibility
- Test quality
- Progressive disclosure
- Safety and privacy
- Documentation
- Duplication with existing skills
- Catalog accuracy

Approval is editorial and technical. Passing automation is necessary but not sufficient.

## Licensing

By submitting a contribution, you agree that it may be distributed under the repository's Apache-2.0 license. Do not submit content you do not have the right to license.

## Conduct

Participation is governed by [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Questions

Use a GitHub issue for repository questions that would benefit future contributors. Use the security process for suspected credential or privacy exposure.
