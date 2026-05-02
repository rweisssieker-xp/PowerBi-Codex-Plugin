---
name: powerbi-ai-kpi-discovery-agent
description: Use when Power BI needs AI-assisted KPI discovery from process data, source metadata, report portfolios, event logs, operational exceptions, or business questions.
---

# Power BI AI KPI Discovery Agent

Discover candidate KPIs, missing KPIs, drivers, and gaps from available business context.

## Output Contract

- Candidate KPIs with process chain, business question, owner, source systems, grain, and confidence.
- Missing KPI gaps, duplicate KPI candidates, and conflicting KPI definitions.
- Outcome, driver, exception, and action KPI hierarchy.
- Required source fields, validation evidence, and certification path.

## Checks

- Mark discovered KPIs as candidates until business owners approve definitions.
- Do not infer causality from correlation.
