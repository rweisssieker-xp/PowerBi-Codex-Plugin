---
name: powerbi-ai-hallucination-guard
description: Use when AI/KI answers about Power BI, KPIs, DAX, source systems, reports, or process causes must be checked against metadata, KPI catalogs, tests, source totals, or accepted evidence.
---

# Power BI AI Hallucination Guard

Use this skill before accepting generated AI answers.

## Checks

- Does the answer cite retrieved artifacts or verified metadata?
- Does KPI logic match certified contracts?
- Do DAX/Power Query outputs have tests?
- Are source totals or reconciliation checks available?
- Are assumptions labeled?
- Does the answer overstate causality?

## Output Requirements

- Return accepted, conditional, or rejected.
- Include failed checks, missing evidence, and required remediation.

