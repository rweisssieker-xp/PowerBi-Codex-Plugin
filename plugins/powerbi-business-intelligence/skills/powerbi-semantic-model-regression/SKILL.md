---
name: powerbi-semantic-model-regression
description: Use when Power BI semantic model versions need diff, regression, breaking-change detection, changed measures, changed relationships, deleted fields, downstream impact, or release validation.
---

# Power BI Semantic Model Regression

Use this skill before model release or certified dataset changes.

## Diff Areas

- Added, removed, renamed tables and columns.
- Added, removed, changed measures and calculation groups.
- Relationship cardinality, direction, active/inactive status.
- RLS/OLS role changes.
- Hidden/visible field changes.
- Data type, format string, summarization, display folder changes.
- Downstream reports, pages, visuals, and users impacted.

## Output Requirements

- Classify changes as safe, warning, breaking, or blocked.
- Include regression tests and rollback plan for breaking or high-risk changes.

