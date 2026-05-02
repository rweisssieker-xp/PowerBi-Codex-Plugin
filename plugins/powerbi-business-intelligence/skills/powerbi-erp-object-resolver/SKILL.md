---
name: powerbi-erp-object-resolver
description: Use when Power BI work needs vendor-aware ERP, CRM, SCM, HCM, EAM, PLM, MES, QMS, WMS, or finance object candidates, joins, APIs, CDS views, and validation paths.
---

# Power BI ERP Object Resolver

Resolve business concepts into likely source-system objects while treating all table, API, CDS, entity, and view names as candidates until metadata proves them.

## Output Contract

- System family and module.
- Business object candidates, technical object candidates, join keys, date fields, statuses, and history behavior.
- Extraction options: connector, OData/API, CDS/view, replication table, warehouse layer, file, or Dataflow.
- Validation: sample document trace, row counts, totals, status lifecycle, currency/unit/calendar, and data latency.

## Traps

- Never assume custom fields, append structures, extensions, or warehouse names.
- Separate operational posting dates from analytical reporting dates.
