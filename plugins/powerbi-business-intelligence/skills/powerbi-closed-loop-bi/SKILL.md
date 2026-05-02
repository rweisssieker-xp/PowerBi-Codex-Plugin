---
name: powerbi-closed-loop-bi
description: Use when Power BI insights should create or update downstream actions in systems such as Jira, Azure DevOps, Planner, Teams, CRM, ServiceNow, SAP workflows, maintenance orders, or task lists.
---

# Power BI Closed Loop BI

Use this skill when insights must return to business processes.

## Loop Pattern

- Detect exception or recommendation.
- Assign owner and due date.
- Create task/ticket/action in target system.
- Track status, aging, resolution, and business outcome.
- Feed results back into KPI and model.

## Output Requirements

- Include trigger, target system, payload fields, approval rules, deduplication, audit trail, and feedback metrics.
- Do not automate writeback into operational systems without owner approval and access control.

