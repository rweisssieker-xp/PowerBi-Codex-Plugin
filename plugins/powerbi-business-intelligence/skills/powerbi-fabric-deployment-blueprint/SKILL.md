---
name: powerbi-fabric-deployment-blueprint
description: Use when Power BI solutions require a Fabric deployment blueprint covering workspaces, Lakehouse, Warehouse, Dataflows, semantic models, pipelines, Git, capacity, security, and release flow.
---

# Power BI Fabric Deployment Blueprint

Design the target deployment topology for enterprise Power BI and Fabric assets.

## Output Contract

- Workspace topology by domain, environment, security boundary, and lifecycle.
- Lakehouse/Warehouse/Dataflow/Semantic Model/Report/Notebook/Pipeline placement.
- Deployment pipeline, Git branch strategy, capacity, gateway, sensitivity labels, and access model.
- Operational runbook: refresh, monitoring, rollback, incident handling, and ownership.

## Checks

- Separate dev/test/prod and sandbox/certified zones.
- Align cost and capacity design with expected refresh and query load.
