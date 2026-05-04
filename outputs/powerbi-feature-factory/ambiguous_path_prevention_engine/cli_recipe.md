# Ambiguous-Path Prevention Engine CLI Recipe

Check model relationships for ambiguity before Power BI Desktop load.

## Commands

```powershell
python scripts\powerbi_expert_factory.py validate --project <pbip-folder>
```

## Acceptance Checks

- no fact-to-fact relationship
- no alternate active relationship path
