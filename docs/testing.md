# Testing

Hermes Field Kit tests skills as behavior contracts and tests its validator as an enforcement contract.

## Repository checks

```bash
python scripts/validate.py
python -m unittest discover -s tests -v
```

The first command validates the checkout. The second creates isolated temporary repositories and proves that valid tap layouts pass while malformed or unsafe layouts fail.

## Validator contract coverage

The self-tests cover:

- Valid minimal tap skill
- Nested category layout
- Missing `SKILL.md`
- Catalog entry without a directory
- Skill directory without a catalog entry
- Mismatched path, category, and version
- Invalid frontmatter
- Missing behavior tests
- Duplicate catalog names
- Secret-like content
- Unsupported supporting paths

## Skill validation layers

### Level 0: repository integrity

Checks required files, JSON, immediate-child tap layout, catalog consistency, naming, frontmatter, required sections, supporting paths, test cases, and common secret patterns.

### Level 1: activation

Positive-trigger cases show when the skill should load. Negative-trigger cases show when it should stay out of the way.

### Level 2: workflow behavior

Behavior cases assert observable disciplines rather than exact prose.

### Level 3: regression

Regression cases capture previously observed failures.

## Manual evaluation

Before acceptance, run the skill in a fresh Hermes session against every committed case, an unseen realistic case, an ambiguous boundary case, and each platform where behavior differs. Also confirm the skill is discoverable from the repository tap.
