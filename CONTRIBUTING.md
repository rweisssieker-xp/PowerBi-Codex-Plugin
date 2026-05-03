# Contributing

Contributions should improve the Power BI Expert-Replacement Factory through better skills, source-system mappings, KPI contracts, process-chain coverage, validation, governance, examples, tests, or documentation.

## Contribution Scope

Good contributions usually fit one of these areas:

- New or improved Codex skills.
- Better Power BI semantic modeling, DAX, Power Query/M, report design, or governance patterns.
- Better source-system and process-pack mappings.
- Better executable validation, schemas, templates, or evidence.
- Better documentation, examples, and tests.

## Skill Guidelines

Each skill should:

- Use a valid `SKILL.md` with YAML frontmatter.
- Start the description with `Use when`.
- Focus on reusable behavior, not one-off project notes.
- Include clear trigger conditions and expected outputs.
- Include validation and common traps where relevant.
- Avoid storing secrets, tenant-specific data, or customer-sensitive details.

## Documentation Guidelines

- Keep GitHub-facing root documentation concise and navigable.
- Keep deep planning or internal notes under `docs/internal/`.
- Keep plugin-specific details under `plugins/powerbi-business-intelligence/`.
- Use English for GitHub-standard root files.
- Use bilingual sections for substantial product artifacts when needed.

## Validation Before PR

Run the relevant checks before opening a pull request:

```powershell
python -m unittest tests\test_powerbi_expert_factory.py -v
python -m json.tool .agents/plugins/marketplace.json > $null
python -m json.tool plugins/powerbi-business-intelligence/.codex-plugin/plugin.json > $null
```

Also search for accidental secrets, credentials, tenant IDs, customer extracts, or confidential screenshots before committing.
