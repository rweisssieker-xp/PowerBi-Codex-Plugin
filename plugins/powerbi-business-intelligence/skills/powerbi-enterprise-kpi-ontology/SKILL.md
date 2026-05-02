---
name: powerbi-enterprise-kpi-ontology
description: Use when organizations need a machine-readable KPI ontology with synonyms, process mapping, owners, source systems, measures, DAX patterns, conflicts, lineage, and certification status.
---

# Power BI Enterprise KPI Ontology

Create a structured KPI knowledge layer for enterprise Power BI.

## Output Contract

- KPI ID, names, synonyms, language variants, owner, domain, process chain, and role relevance.
- Formula contract, source systems, model objects, DAX pattern, date basis, grain, and reconciliation source.
- Conflict relationships, dependencies, downstream reports, certification state, and retirement status.
- JSON/YAML-ready representation and `en-US`/`de-DE` glossary entries.

## Checks

- Keep local variants explicit.
- Link KPIs to data products and action owners.
