---
name: powerbi-automated-schema-drift-alerts
description: Use when source changes should automatically alert impacts on Power Query, semantic models, DAX, report visuals, data contracts, tests, and documentation.
---

# Power BI Automated Schema Drift Alerts

Alert schema changes with downstream impact.

## Output Contract

- Drift event, source object, changed field/type/status/API, timestamp, and owner.
- Impacted queries, models, measures, visuals, contracts, tests, and reports.
- Severity, required fix, owner, communication, and release gate.

## Checks

- Include false-positive suppression and approved-change handling.
