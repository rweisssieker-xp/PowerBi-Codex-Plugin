---
name: powerbi-modelling
description: Design, review, and harden generic Power BI semantic models. Use for star schemas, fact/dimension grain, relationships, DAX catalogs, calculation groups, field parameters, RLS/OLS, incremental refresh, aggregations, composite models, DirectQuery, Direct Lake, Fabric, and model documentation for any business domain.
---

# Power BI Modelling

Use this skill when source queries are known or a Power BI model must be designed or reviewed.

## Workflow

1. Define the business process and fact grain before visuals or DAX.
2. Separate facts, dimensions, bridges, snapshots, and accumulating snapshots.
3. Use conformed dimensions for date, organization, customer, product/material, account, geography, owner, status, scenario, currency, and source system where relevant.
4. Define explicit measures with business meaning, numerator, denominator, date basis, exclusions, and reconciliation source.
5. Design RLS/OLS and sensitivity labels early for customer, employee, supplier, finance, and regulated data.
6. Specify refresh: import, DirectQuery, Direct Lake, incremental refresh, gateway, dataflows, deployment pipelines, and failure checks.
7. Produce model documentation: tables, relationships, measures, refresh, security, validation, assumptions, and known risks.

## References

- Load `references/model-patterns.md` for model architecture and relationship rules.
- Load `references/business-domain-catalog.md` for common facts, dimensions, and measures by domain.

## Assets

- `assets/semantic-model-spec-template.md`: model specification template.
- `assets/measure-catalog-template.csv`: DAX backlog planning template.

## Scripts

- `scripts/new_semantic_model_spec.py`: Generate a semantic model starter spec.

