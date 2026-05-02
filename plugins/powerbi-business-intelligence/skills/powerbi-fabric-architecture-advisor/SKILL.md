---
name: powerbi-fabric-architecture-advisor
description: Advise on modern Power BI and Microsoft Fabric architecture. Use for Import vs DirectQuery vs Direct Lake, composite models, Dataflows, Lakehouse, Warehouse, OneLake, semantic model ownership, deployment pipelines, and medallion architecture decisions.
---

# Power BI Fabric Architecture Advisor

Use this skill when the core question is architecture rather than a single report.

## Decision Areas

- Storage: source system, dataflow, lakehouse, warehouse, semantic model, external warehouse.
- Mode: import, DirectQuery, Direct Lake, composite model, live connection.
- Transformation: Power Query, dataflow, SQL, Spark, notebook, warehouse view.
- Governance: workspace layout, deployment pipelines, sensitivity, lineage, endorsement.
- Scale: capacity, refresh windows, concurrency, model size, domain ownership.

## Output Requirements

- Recommend one target architecture and one fallback.
- Explain tradeoffs for latency, cost, skill demand, governance, performance, and operability.
- Include migration path from current state.

