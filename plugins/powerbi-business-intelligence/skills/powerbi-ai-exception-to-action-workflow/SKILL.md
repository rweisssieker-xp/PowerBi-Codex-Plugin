---
name: powerbi-ai-exception-to-action-workflow
description: Use when KPI exceptions, anomalies, delays, risks, or threshold breaches must be converted into prioritized actions with owner, cause, impact, due date, and retest condition.
---

# Power BI AI Exception-to-Action Workflow

Use this skill to close the loop between analytics and operations.

## Workflow Fields

- Exception type, severity, source KPI, time window, and affected entity.
- Root-cause hypothesis, evidence, and confidence.
- Owner role, action recommendation, due date, expected impact, and priority.
- Retest condition and success metric.
- Escalation path when owner or evidence is missing.

## Output Requirements

- Produce an action table suitable for Power BI, Planner, Jira, ServiceNow, SAP Workflow, or CRM handoff.
- Do not recommend action without evidence or owner routing.

