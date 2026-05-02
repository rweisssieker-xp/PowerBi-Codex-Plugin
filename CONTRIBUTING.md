# Contributing

## Contribution Scope

Contributions should improve the Power BI expert-replacement layer through:

- New or improved Codex skills.
- Better source-system mappings.
- Better KPI contracts.
- Better process-chain coverage.
- Better validation, governance, and documentation patterns.
- Better examples and tests.

## Skill Guidelines

Each skill should:

- Use a valid `SKILL.md` with YAML frontmatter.
- Start the description with `Use when`.
- Focus on reusable behavior, not one-off project notes.
- Include clear trigger conditions.
- Define expected outputs.
- Include validation and common traps where relevant.
- Avoid storing secrets, tenant-specific data, or customer-sensitive details.

## Documentation Guidelines

- Keep GitHub docs concise and navigable.
- Put deep plugin-specific details under `plugins/powerbi-business-intelligence/docs`.
- Put repository-level docs under `docs`.
- For substantial artifacts, maintain aligned `en-US` and `de-DE` versions.

## Validation Before PR

Run:

```powershell
python -m json.tool .agents/plugins/marketplace.json > $null
python -m json.tool plugins/powerbi-business-intelligence/.codex-plugin/plugin.json > $null
(Get-ChildItem plugins/powerbi-business-intelligence/skills -Recurse -Filter SKILL.md | Measure-Object).Count
```

Also search for accidental vendor-specific leftovers or sensitive data before committing.
