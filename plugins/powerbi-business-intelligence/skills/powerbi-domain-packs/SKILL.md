---
name: powerbi-domain-packs
description: Use reusable Power BI domain packs for common business areas, including Customer Churn, Material Churn, FiCO, Sales, Procurement, Supply Chain, Service, HR, Risk, Operations, and Executive Cockpits.
---

# Power BI Domain Packs

Use this skill when a report can be accelerated by a reusable business domain template.

## Workflow

1. Select the closest domain pack from `references/domain-pack-catalog.md`.
2. Adapt source systems, grain, dimensions, measures, pages, and RLS.
3. Remove unused KPIs instead of overbuilding.
4. Add source-specific connector and validation notes.
5. Produce a scoped implementation pack that can be reviewed by fewer senior Power BI experts.

## Output Requirements

- Include domain pack name, reusable model pattern, required source entities, core KPIs, report pages, and validation checks.
- State what must be verified with the business owner.
- Flag domains that require strict security, such as FiCO, HR, customer profitability, supplier contracts, and regulated operations.

## Assets

- `assets/domain-pack-catalog.csv`: machine-readable starter catalog.

