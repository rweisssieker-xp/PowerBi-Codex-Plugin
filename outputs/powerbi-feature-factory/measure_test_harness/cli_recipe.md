# Measure Test Harness CLI Recipe

Attach test/reconciliation strategy to every generated KPI measure.

## Commands

```powershell
python scripts\powerbi_expert_factory.py feature-plan --process <processId>
```

## Acceptance Checks

- each KPI has DAX
- each KPI has expected-result strategy
