# Published skills

Hermes tap discovery expects every skill directly beneath `skills/`:

```text
skills/<skill-name>/
├── SKILL.md
├── README.md
├── examples/
└── tests/
    └── cases.json
```

Do not insert category folders. Categories belong in `metadata.hermes.category` and `catalog.json`.

## Available

### x-analytics-import

A private-by-default workflow for validating, normalizing, importing, and comparing X Analytics CSV exports. It includes an executable standard-library importer, synthetic regression fixtures, baseline and recurring-run recipes, robust statistics, idempotent manifests, and privacy guards.

Do not add a skill without the admission evidence required by the root README.
