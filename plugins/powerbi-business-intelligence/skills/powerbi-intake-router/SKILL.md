---
name: powerbi-intake-router
description: Classify Power BI requests and route them to the right delivery path. Use when a request may involve data sources, semantic models, DAX, UX, governance, performance, migration, Fabric architecture, portfolio cleanup, or business problem design.
---

# Power BI Intake Router

Use this skill as the front door for Power BI work.

## Routing Logic

1. Business outcome only -> `powerbi-business-problem-factory`.
2. Existing reports or many workspaces -> `powerbi-portfolio-rationalization`.
3. KPI disagreement -> `powerbi-kpi-governance`.
4. Reusable governed model -> `powerbi-certified-dataset-factory`.
5. Slow report, failed refresh, capacity issue -> `powerbi-performance-refresh-optimizer` or `powerbi-cost-capacity-optimizer`.
6. Fabric/architecture decision -> `powerbi-fabric-architecture-advisor`.
7. Legacy migration -> `powerbi-migration-factory`.
8. Delivery package required -> `powerbi-delivery-factory`.
9. Review request -> `powerbi-expert-review`.

## Output Requirements

- State the request type, likely root problem, recommended skill path, required inputs, and first artifact to produce.
- Do not jump to DAX or visuals before source, grain, KPI semantics, and ownership are clear.

