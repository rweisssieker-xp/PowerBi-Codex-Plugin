---
name: powerbi-data-readiness-scoring
description: Score whether data sources are ready for Power BI implementation. Use for data completeness, key quality, history, grain, source ownership, PII, refreshability, query folding, schema stability, and KPI suitability.
---

# Power BI Data Readiness Scoring

Use this skill before building a report or certified dataset.

## Scoring Dimensions

- Source ownership and access.
- Entity completeness and required fields.
- Key quality and relationship viability.
- Historical coverage and date consistency.
- Grain clarity and duplicates.
- KPI suitability and reconciliation source.
- PII/sensitivity/security readiness.
- Refreshability, gateway, folding, pagination, throttling.
- Schema stability and change management.

## Output Requirements

- Score each dimension 0-5 and classify overall status as ready, conditional, blocked, or unknown.
- Include remediation actions needed before report build.

