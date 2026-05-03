# Contributing

## en-US

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
- Put repository-level guides as Markdown files in the repository root (see `DOCUMENTATION.md` for the index).
- For substantial artifacts, maintain aligned `en-US` and `de-DE` versions.

## Validation Before PR

Run:

```powershell
python -m json.tool .agents/plugins/marketplace.json > $null
python -m json.tool plugins/powerbi-business-intelligence/.codex-plugin/plugin.json > $null
(Get-ChildItem plugins/powerbi-business-intelligence/skills -Recurse -Filter SKILL.md | Measure-Object).Count
```

Also search for accidental vendor-specific leftovers or sensitive data before committing.

## de-DE

## Contribution Scope

Beitraege sollen die Power BI Expert-Replacement-Schicht verbessern durch:

- Neue oder verbesserte Codex Skills.
- Bessere Quellsystem-Mappings.
- Bessere KPI Contracts.
- Bessere Prozesskettenabdeckung.
- Bessere Validierungs-, Governance- und Dokumentationsmuster.
- Bessere Beispiele und Tests.

## Skill Guidelines

Jeder Skill soll:

- Ein gueltiges `SKILL.md` mit YAML-Frontmatter nutzen.
- Die Beschreibung mit `Use when` beginnen.
- Wiederverwendbares Verhalten beschreiben, keine einmaligen Projektnotizen.
- Klare Triggerbedingungen enthalten.
- Erwartete Outputs definieren.
- Validierung und typische Fallen enthalten, wo relevant.
- Keine Secrets, tenant-spezifischen Daten oder kundensensitiven Details speichern.

## Documentation Guidelines

- GitHub-Doku kurz und navigierbar halten.
- Tiefe plugin-spezifische Details unter `plugins/powerbi-business-intelligence/docs` pflegen.
- Repository-weite Guides als Markdown im Repo-Root pflegen (Index in `DOCUMENTATION.md`).
- Fuer wesentliche Artefakte abgestimmte `en-US`- und `de-DE`-Versionen pflegen.

## Validation Before PR

Ausfuehren:

```powershell
python -m json.tool .agents/plugins/marketplace.json > $null
python -m json.tool plugins/powerbi-business-intelligence/.codex-plugin/plugin.json > $null
(Get-ChildItem plugins/powerbi-business-intelligence/skills -Recurse -Filter SKILL.md | Measure-Object).Count
```

Vor dem Commit ausserdem nach versehentlichen vendor-spezifischen Resten oder sensiblen Daten suchen.
