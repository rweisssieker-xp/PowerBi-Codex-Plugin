---
name: powerbi-automated-powerquery-review
description: Use when Power Query/M needs automated review for folding, types, nulls, duplicates, pagination, incremental refresh, gateway, privacy, and error handling.
---

# Power BI Automated Power Query Review

Review extraction logic before refresh failures appear.

## Output Contract

- Query inventory, connector, source, transformations, folding status, parameters, and refresh mode.
- Findings for types, nulls, duplicates, pagination, schema drift, privacy levels, gateway, and errors.
- Performance and reliability recommendations.
- Test plan and blocking issues.

## Checks

- Treat broken folding on large sources as high risk.
- Never recommend hardcoded secrets.
