# Connector-Aware Source Interview CLI Recipe

Ask source-specific questions and route to native Power BI connectors and modes.

## Commands

```powershell
python scripts\build_powerbi_source_routing.py
```
```powershell
python scripts\powerbi_expert_factory.py feature-plan --process <processId>
```

## Acceptance Checks

- native connector declared
- gateway owner declared
- schema drift decision declared
