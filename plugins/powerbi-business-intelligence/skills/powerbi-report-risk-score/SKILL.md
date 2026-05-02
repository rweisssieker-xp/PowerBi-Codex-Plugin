---
name: powerbi-report-risk-score
description: Assign risk scores to Power BI reports, datasets, and delivery plans. Use for business risk, KPI risk, security risk, performance risk, refresh risk, maintenance risk, adoption risk, and portfolio prioritization.
---

# Power BI Report Risk Score

Use this skill when prioritizing reviews, remediation, or portfolio cleanup.

## Risk Categories

- Business risk: executive use, regulatory impact, financial decisions.
- KPI risk: unclear definitions, conflicting measures, no reconciliation.
- Security risk: PII, HR, finance, external sharing, missing RLS.
- Performance risk: slow visuals, large model, high cardinality, DirectQuery pressure.
- Refresh risk: gateway, API limits, non-folding queries, owner gaps.
- Maintenance risk: no owner, local PBIX, undocumented logic, stale source.
- Adoption risk: low usage, duplicate report, unclear audience.

## Output Requirements

- Score each category 0-5 and compute overall severity.
- Recommend keep, certify, refactor, retire, migrate, or investigate.

