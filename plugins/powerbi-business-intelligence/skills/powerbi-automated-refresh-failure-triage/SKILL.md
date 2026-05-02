---
name: powerbi-automated-refresh-failure-triage
description: Use when Power BI refresh failures need automated classification, root-cause grouping, owner routing, fix plans, SLA impact, and communication.
---

# Power BI Automated Refresh Failure Triage

Turn refresh failures into routed remediation.

## Output Contract

- Failed asset, workspace, owner, gateway, data source, error, time, SLA, and impacted reports.
- Failure class: credentials, gateway, source unavailable, schema drift, timeout, capacity, privacy, query error, or service incident.
- Fix plan, owner, ETA, communication, and retest.

## Checks

- Separate transient incidents from recurring defects.
