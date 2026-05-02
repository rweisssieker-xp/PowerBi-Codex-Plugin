---
name: powerbi-ai-autonomous-remediation-agent
description: Use when Power BI issues need AI-generated remediation plans for refresh failures, DAX bugs, model defects, RLS gaps, performance problems, source drift, or documentation failures.
---

# Power BI AI Autonomous Remediation Agent

Create safe remediation plans for BI defects.

## Output Contract

- Issue, evidence, impacted assets, severity, business impact, and likely cause.
- Fix plan for source, Power Query, model, DAX, RLS, performance, refresh, documentation, or deployment.
- Tests, rollback plan, owner approvals, and release gate.
- Automation level: recommend, draft, execute with approval, or block.

## Checks

- Do not execute destructive changes without approval.
- Always include validation and rollback.
