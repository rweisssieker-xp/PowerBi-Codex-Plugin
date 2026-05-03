# Release Process

## Release Readiness

A release is ready only when the repository evidence shows:

- JSON files parse.
- Skill frontmatter is valid.
- Local Markdown links resolve.
- Relevant tests pass.
- Generated PBIP/TMDL/PBIR artifacts pass executable factory validation when included.
- No secrets, tenant IDs, credentials, or customer-sensitive extracts are present.
- GitHub-facing root documentation is concise, navigable, and English-first.

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
