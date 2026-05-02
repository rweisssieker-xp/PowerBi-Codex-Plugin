---
name: powerbi-auto-semantic-model-builder
description: Use when metadata should be converted into Power BI semantic model candidates, including facts, dimensions, relationships, measures, RLS, TMDL, PBIP skeletons, or certified dataset designs.
---

# Power BI Auto Semantic Model Builder

Use this skill after metadata discovery or when a model must be generated from source inventory.

## Build Pattern

1. Classify tables as facts, dimensions, bridges, snapshots, helper tables, or staging.
2. Infer grain, keys, date roles, measures, and relationship candidates.
3. Apply business process context and master data mapping.
4. Generate model spec, measure starter catalog, RLS candidates, and TMDL/PBIP skeleton plan.
5. Mark low-confidence inferences for expert review.

## Output Requirements

- Include confidence per table, relationship, and measure.
- Separate generated candidates from verified model design.
- Require data contract and validation before certification.

