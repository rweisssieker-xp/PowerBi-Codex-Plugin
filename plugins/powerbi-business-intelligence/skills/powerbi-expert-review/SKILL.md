---
name: powerbi-expert-review
description: Review existing Power BI reports, PBIX/PBIP projects, semantic model specs, DAX, Power Query, report pages, RLS, refresh design, and governance to find issues normally caught by senior Power BI experts.
---

# Power BI Expert Review

Use this skill when the user wants to reduce dependency on many Power BI experts by standardizing review quality.

## Review Priorities

1. Business correctness: KPI definitions, grain, filters, date basis, exclusions.
2. Model correctness: facts, dimensions, relationships, cardinality, ambiguity, many-to-many, role-playing dates.
3. DAX quality: explicit measures, context handling, time intelligence, performance, naming, folders.
4. Power Query and source design: folding, incremental refresh, privacy levels, gateway, credentials, schema drift.
5. Report UX: page purpose, slicer consistency, visual choice, drillthrough, exception workflows.
6. Security and governance: RLS/OLS, sensitivity, workspace, certification, deployment, ownership.
7. Validation: source totals, row counts, financial reconciliation, RLS test users, refresh monitoring.

## Output Requirements

- Lead with findings ordered by severity.
- Use concrete evidence from files, specs, DAX, or model descriptions when available.
- Separate blockers, high-risk issues, maintainability issues, and improvement opportunities.
- End with a short remediation checklist.

## Assets

- `assets/review-checklist.md`: reusable review checklist.

