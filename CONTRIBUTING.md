# Contributing

Hermes Field Kit is curated rather than exhaustive. Contributions are evaluated for usefulness, reproducibility, safety, tap compatibility, and evidence of real use.

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
4. Live directly at `skills/<skill-name>/` so Hermes tap discovery can find it.
5. Include positive and negative trigger examples.
6. Include behavior-oriented test cases.
7. Document limitations, dependencies, and safety boundaries.
8. Pass both repository validation and validator self-tests.

A generated collection, speculative prompt, or thin rewording of an existing skill will not be accepted.

## Development workflow

```bash
git clone https://github.com/asimons81/hermes-field-kit.git
cd hermes-field-kit
git switch -c <type>/<short-description>
python scripts/validate.py
python -m unittest discover -s tests -v
```

Use focused branches such as:

- `docs/clarify-installation`
- `tooling/validate-frontmatter`
- `skill/example-name`

Prefer Conventional Commit-style subjects.

## Pull requests

A pull request should be one coherent change. Include:

- What changed and why
- Evidence or reproduction steps
- Validation performed
- Security or privacy considerations
- Follow-up work intentionally out of scope

## Skill review standard

Maintainers will check the admission rule, tap discovery, trigger precision, Hermes compatibility, reproducibility, test quality, progressive disclosure, safety, documentation, duplication, and catalog accuracy.

Passing automation is necessary but not sufficient.

## Licensing

By submitting a contribution, you agree that it may be distributed under the repository's Apache-2.0 license. Do not submit content you do not have the right to license.

## Conduct

Participation is governed by [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
