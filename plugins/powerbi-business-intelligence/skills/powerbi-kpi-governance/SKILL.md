---
name: powerbi-kpi-governance
description: Define, compare, standardize, and govern Power BI KPIs. Use for KPI conflicts, duplicate measures, semantic disagreements, numerator/denominator/date-basis issues, metric certification, and business owner acceptance.
---

# Power BI KPI Governance

Use this skill when multiple reports or teams define the same KPI differently.

## Workflow

1. Inventory KPI names, DAX expressions, report usage, owner, source, date basis, filters, and exclusions.
2. Detect conflicts: same name different logic, different name same logic, implicit measures, unclear denominators, inconsistent fiscal calendar, currency mismatch.
3. Define certified KPI contract: business definition, owner, grain, numerator, denominator, date role, exclusions, DAX, validation source.
4. Create deprecated KPI mappings and migration notes.
5. Publish accepted KPI catalog for certified datasets and self-service guardrails.

## Output Requirements

- Include conflict findings and a target KPI contract.
- Flag financial, customer, HR, and compliance KPIs for owner approval before certification.

## Assets

- `assets/kpi-contract-template.csv`: KPI governance template.

