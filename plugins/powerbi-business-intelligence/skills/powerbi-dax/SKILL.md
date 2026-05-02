---
name: powerbi-dax
description: Create, review, standardize, and validate generic Power BI DAX measures for finance, sales, customer churn, material churn, supply chain, service, HR, risk, operations, and executive dashboards.
---

# Power BI DAX

Use this skill after the semantic model grain is known and before visuals are finalized.

## Workflow

1. Define each measure with business meaning, grain, date basis, filters, exclusions, and validation source.
2. Prefer explicit measures; do not rely on implicit visual aggregations.
3. Keep time intelligence tied to a marked, conformed `DimDate`.
4. Use disconnected parameter tables and field parameters only when they improve the report workflow.
5. Validate every measure against source totals, extracts, or agreed reconciliation queries.

## Assets

- `assets/business-measure-patterns.dax`: reusable DAX starter patterns for common business problems.

## Scripts

- `scripts/new_dax_measure_pack.py`: Generate a starter DAX pack from a measure catalog CSV.

