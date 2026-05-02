---
name: powerbi-ai-semantic-model-refactor-agent
description: Use when AI should identify weak Power BI semantic models, poor relationships, mixed grain, ambiguous measures, snowflaking, many-to-many risks, or refactor paths into governed star schemas.
---

# Power BI AI Semantic Model Refactor Agent

Refactor weak semantic models into governed star-schema candidates.

## Output Contract

- Current-state findings: tables, grain, relationships, measures, security, performance, and lineage.
- Target-state model: facts, dimensions, bridge tables, role-playing dates, measures, RLS, and refresh mode.
- Migration steps, breaking changes, test plan, and owner acceptance.
- Risk score and certification readiness delta.

## Checks

- Preserve business meaning and validated KPI contracts.
- Do not collapse incompatible grains into one fact table.
