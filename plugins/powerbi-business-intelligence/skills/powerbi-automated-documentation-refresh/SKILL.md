---
name: powerbi-automated-documentation-refresh
description: Use when Power BI documentation should be regenerated from current models, measures, sources, RLS, lineage, report pages, quality gates, and release changes.
---

# Power BI Automated Documentation Refresh

Keep documentation aligned with the live BI artifact.

## Output Contract

- Artifact scope, source of truth, changed elements, and documentation targets.
- Refreshed model, KPI, DAX, M, RLS, lineage, page, validation, operations, and owner docs.
- Drift findings where docs and implementation disagree.
- `en-US` and `de-DE` output.

## Checks

- Mark generated docs as requiring review when source metadata is incomplete.
