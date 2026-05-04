# Visual Binding Compiler CLI Recipe

Verify report-page specs bind only to generated fields and measures.

## Commands

```powershell
python scripts\powerbi_expert_factory.py validate --project <pbip-folder>
```

## Acceptance Checks

- all columns exist
- all measures exist
- visual count reported
