---
name: powerbi-ai-model-graph-validator
description: Use when a Power BI semantic model relationship graph must be checked for ambiguous paths, fact-to-fact chains, wrong filter direction, unsupported topology, DirectQuery/OLAP limitations, or certification risk.
---

# Power BI AI Model Graph Validator

Use this skill before publishing or opening generated TMDL models.

## Validation Areas

- Star-schema topology: facts filter to dimensions through many-to-one relationships.
- Ambiguous paths between facts and dimensions.
- Fact-to-fact relationships and accidental bridge paths.
- Many-to-many risk and bridge-table requirements.
- Active/inactive relationship strategy and role-playing dates.
- Cross-filter direction and bidirectional filter risks.
- Unsupported DirectQuery, composite model, or live/OLAP edits.

## Output Requirements

- Include relationship inventory, invalid paths, severity, and remediation.
- Mark models as `pass`, `pass-with-risk`, or `fail`.

