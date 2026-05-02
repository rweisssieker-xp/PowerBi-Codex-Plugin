---
name: powerbi-ai-tenant-risk-predictor
description: Use when Power BI tenants need AI prediction of reports or datasets likely to break from refresh failures, owner gaps, gateway issues, capacity pressure, schema drift, or usage decay.
---

# Power BI AI Tenant Risk Predictor

Predict which tenant assets are likely to fail or become risky.

## Output Contract

- Asset inventory signals: refresh history, owner, gateway, capacity, schema drift, usage, endorsement, and sharing.
- Risk score by dataset, report, workspace, gateway, and capacity.
- Predicted failure mode, evidence, owner, remediation, and monitoring cadence.
- Prioritized intervention plan.

## Checks

- Separate observed failures from predicted risk.
- Require admin metadata and telemetry evidence for production scoring.
