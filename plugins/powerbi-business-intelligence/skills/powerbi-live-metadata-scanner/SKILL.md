---
name: powerbi-live-metadata-scanner
description: Use when Power BI or Fabric work needs live metadata discovery from tenants, semantic models, SQL, lakehouse, SAP, Salesforce, Dynamics, Snowflake, APIs, or files before design decisions.
---

# Power BI Live Metadata Scanner

Plan live metadata discovery before assuming source structure.

## Output Contract

- Target systems, access method, authentication owner, and scan scope.
- Objects, columns, measures, relationships, refresh settings, lineage, labels, owners, and usage signals to collect.
- Metadata risk findings: missing keys, unclear dates, duplicate measures, stale objects, missing owners, and sensitive fields.
- Follow-up actions for modelling, KPI governance, data contracts, RLS, and documentation.

## Checks

- Do not request or store secrets.
- Separate scan plan from actual source extraction.
