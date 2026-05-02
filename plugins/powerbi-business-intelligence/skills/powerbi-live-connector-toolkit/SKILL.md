---
name: powerbi-live-connector-toolkit
description: Use when Power BI work needs live connector planning or metadata access for SAP OData/CDS, Salesforce, Dataverse, SQL, Fabric, Power BI REST, Snowflake, Databricks, APIs, or enterprise warehouses.
---

# Power BI Live Connector Toolkit

Use this skill when the next step should be source-system interrogation rather than assumptions.

## Connector Targets

- SAP OData/CDS/BW/Datasphere metadata.
- Salesforce objects, fields, relationships, picklists.
- Dataverse tables, columns, relationships, option sets.
- SQL Server, Oracle, PostgreSQL, Snowflake, Databricks schemas.
- Fabric workspaces, warehouses, lakehouses, semantic models.
- Power BI REST APIs for workspaces, datasets, reports, refresh, lineage.

## Output Requirements

- Identify credentials, endpoint, auth mode, metadata command/API, expected artifact, and security constraints.
- Never embed credentials; use environment variables, approved secret stores, or platform credential storage.
- Return a metadata discovery plan when live access is unavailable.

