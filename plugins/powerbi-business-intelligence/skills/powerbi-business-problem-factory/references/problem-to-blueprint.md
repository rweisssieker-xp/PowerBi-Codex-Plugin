# Problem to Blueprint Patterns

## Universal Blueprint

| Layer | Required Output |
| --- | --- |
| Outcome | Business decision, owner, target behavior |
| Source | Systems, connector, refresh, security, reconciliation source |
| Model | Facts, dimensions, grain, relationships, RLS |
| Measures | KPI definitions, DAX names, validation totals |
| Report | Overview, drivers, flow/cohort, exceptions, detail |
| Delivery | PBIP/PBIX notes, deployment, runbook, support owner |

## Problem Families

- Churn: customer, material, employee, supplier, subscription, product usage.
- Variance: FiCO, cost center, profit center, budget, forecast, margin.
- Risk: credit, supplier, SLA, compliance, operational, inventory, project.
- Flow: sales funnel, order-to-cash, procure-to-pay, case lifecycle, production.
- Aging: receivables, payables, backlog, stock, opportunities, tickets.
- Optimization: inventory, routing, utilization, pricing, service capacity.

## Visual Logic

- Use KPI cards only for top-level outcomes.
- Use waterfall for variance and financial bridges.
- Use cohort matrices and retention curves for churn.
- Use Pareto for root causes.
- Use scatter for risk and prioritization.
- Use exception tables for action ownership.

