---
name: powerbi-natural-language-verified-report
description: Turn natural-language business questions into verified Power BI report designs. Use when users ask questions like why customers churn, what drives margin, where inventory risk exists, or which process bottlenecks matter, and the answer must include data readiness, KPI validity, model design, DAX, visuals, and validation.
---

# Power BI Natural Language to Verified Report

Use this skill when the user gives a business question instead of a report specification.

## Workflow

1. Translate the question into business outcome, decision action, grain, segments, and date basis.
2. Check whether required data entities, keys, history, and security attributes are likely available.
3. Define KPI contracts and validation sources before visuals.
4. Produce source plan, semantic model, DAX catalog, page design, RLS, and reconciliation tests.
5. Mark the report as verified only when assumptions, data readiness, KPI logic, and acceptance checks are explicit.

## Output Requirements

- Include "verified", "blocked", or "conditional" readiness status.
- Separate natural-language answer intent from build artifacts.
- State which facts must be proven against actual source metadata.

