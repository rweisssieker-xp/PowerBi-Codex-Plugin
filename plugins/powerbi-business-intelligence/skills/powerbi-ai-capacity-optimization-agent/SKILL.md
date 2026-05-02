---
name: powerbi-ai-capacity-optimization-agent
description: Use when Power BI or Fabric capacity needs AI recommendations for model splitting, aggregations, Direct Lake, Import, refresh windows, query reduction, and cost optimization.
---

# Power BI AI Capacity Optimization Agent

Optimize capacity, refresh, and query load.

## Output Contract

- Capacity, workspace, dataset, refresh, query, storage, and usage signals.
- Bottlenecks: refresh overlap, large model, expensive DAX, high concurrency, storage, DirectQuery pressure, or gateway.
- Optimization recommendations: aggregation, split, incremental refresh, Direct Lake/Import, schedule, partition, measure rewrite, or capacity change.
- Cost, risk, and validation plan.

## Checks

- Do not optimize cost by breaking SLA or certified report performance.
