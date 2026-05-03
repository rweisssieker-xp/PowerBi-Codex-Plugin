# Release Process

## en-US

## Release Readiness

A release is ready only when the repository evidence shows:

- JSON files parse.
- Skill frontmatter is valid.
- Local Markdown links resolve.
- Substantial docs include `en-US` and `de-DE`.
- Relevant tests pass.
- Generated PBIP/TMDL/PBIR artifacts pass the executable factory validation when included.
- No secrets, tenant IDs, credentials, or customer-sensitive extracts are present.

## Recommended Checks

```powershell
python -m unittest tests\test_powerbi_expert_factory.py -v
python scripts\powerbi_expert_factory.py validate --project outputs\powerbi-order2cash-pbip\Order2Cash_NativeExcel --out outputs\powerbi-order2cash-pbip\expert_factory_validation.json
git diff --check
```

## Version Notes

Release notes should explain:

- New or changed skills.
- New or changed process packs.
- Validator and schema changes.
- Documentation and governance changes.
- Known limitations and planned expert-agent capabilities.

## de-DE

## Release Readiness

Ein Release ist erst bereit, wenn die Repository-Evidence zeigt:

- JSON-Dateien sind parsebar.
- Skill-Frontmatter ist gueltig.
- Lokale Markdown-Links funktionieren.
- Wesentliche Dokumentation enthaelt `en-US` und `de-DE`.
- Relevante Tests bestehen.
- Generierte PBIP/TMDL/PBIR-Artefakte bestehen die Executable-Factory-Validierung, wenn sie enthalten sind.
- Keine Secrets, Tenant IDs, Credentials oder kundensensitiven Extrakte sind enthalten.

## Empfohlene Checks

```powershell
python -m unittest tests\test_powerbi_expert_factory.py -v
python scripts\powerbi_expert_factory.py validate --project outputs\powerbi-order2cash-pbip\Order2Cash_NativeExcel --out outputs\powerbi-order2cash-pbip\expert_factory_validation.json
git diff --check
```

## Release Notes

Release Notes sollen erklaeren:

- Neue oder geaenderte Skills.
- Neue oder geaenderte Process Packs.
- Validator- und Schema-Aenderungen.
- Dokumentations- und Governance-Aenderungen.
- Bekannte Grenzen und geplante Expert-Agent-Faehigkeiten.

