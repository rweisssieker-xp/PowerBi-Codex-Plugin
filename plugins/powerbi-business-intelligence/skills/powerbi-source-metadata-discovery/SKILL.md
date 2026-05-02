---
name: powerbi-source-metadata-discovery
description: Use when a Power BI solution needs metadata discovery for SAP, Salesforce, Dynamics/Dataverse, Power BI/Fabric, SQL databases, OData feeds, REST APIs, files, warehouses, lakehouses, or semantic models before designing reports.
---

# Power BI Source Metadata Discovery

Use this skill before committing to field names, tables, relationships, or extraction logic.

## Discovery Targets

- SAP: CDS views, OData metadata, BW queries, Datasphere objects, replicated warehouse tables.
- Salesforce: objects, fields, relationships, picklists, record types.
- Dynamics/Dataverse: entities/tables, columns, option sets, relationships, security roles.
- Power BI/Fabric: workspaces, semantic models, tables, measures, lineage, refresh, endorsements.
- SQL/warehouse/lakehouse: schemas, tables, columns, data types, constraints, row counts, partitions.
- APIs/OData: metadata document, endpoints, pagination, filters, throttling, delta support.
- Files: schema drift, encoding, folder conventions, header quality, archival rules.

## Output Requirements

- Produce metadata inventory, candidate facts/dimensions, key candidates, quality concerns, and extraction options.
- Mark unknowns that block model design.

