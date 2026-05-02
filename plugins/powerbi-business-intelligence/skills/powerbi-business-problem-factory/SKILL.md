---
name: powerbi-business-problem-factory
description: Convert any business problem into a complete Power BI implementation blueprint. Use for customer churn, material churn, FiCO, working capital, margin, procurement, sales, supply chain, service, HR, risk, compliance, operations, and executive decision cockpits.
---

# Power BI Business Problem Factory

Use this skill when the user describes a business outcome instead of a technical Power BI task.

## Operating Mode

Act as a BI solution architect who reduces the need for multiple Power BI specialists by turning vague business requests into repeatable implementation blueprints.

## Workflow

1. Classify the problem domain and decision owner.
2. Define the decision action: reduce risk, increase revenue, lower cost, improve service, protect cash, improve compliance, or prioritize work.
3. Define fact grain, lifecycle states, time basis, segments, and required drill paths.
4. Select relevant domain pack patterns from `references/problem-to-blueprint.md`.
5. Produce a Power BI blueprint: source plan, semantic model, DAX catalog, report pages, RLS, validation, deployment, and runbook.

## Output Requirements

- Include a one-page executive blueprint and a build-ready technical section.
- State assumptions explicitly when source systems, fields, or KPI definitions are unknown.
- Prefer reusable patterns over bespoke design unless the business process requires it.
- Include validation and reconciliation from the start.

## Scripts

- `scripts/new_business_problem_blueprint.py`: Generate a starter blueprint for a named business problem.

