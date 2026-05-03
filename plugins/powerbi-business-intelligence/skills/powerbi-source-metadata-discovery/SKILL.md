---
name: powerbi-source-metadata-discovery
description: Use when a Power BI solution needs metadata discovery for SAP, Salesforce, Dynamics/Dataverse, Power BI/Fabric, SQL databases, OData feeds, REST APIs, files, warehouses, lakehouses, or semantic models before designing reports.
---

# Power BI Source Metadata Discovery

Use this skill before committing to field names, tables, relationships, or extraction logic.

## Discovery Targets

- Power BI native connector source classes: File, Database, Microsoft Fabric, Power Platform, Azure, Online Services, and Other.
- Files: Excel Workbook through the native Excel connector, Text/CSV, XML, JSON, Folder, PDF, Parquet, SharePoint Folder, OneDrive/SharePoint-hosted files, and folder-combine patterns.
- SAP: CDS views, OData metadata, BW queries, Datasphere objects, replicated warehouse tables.
- Salesforce: objects, fields, relationships, picklists, record types.
- Dynamics/Dataverse: entities/tables, columns, option sets, relationships, security roles.
- Power BI/Fabric: workspaces, semantic models, tables, measures, lineage, refresh, endorsements.
- SQL/warehouse/lakehouse: schemas, tables, columns, data types, constraints, row counts, partitions.
- APIs/OData: metadata document, endpoints, pagination, filters, throttling, delta support.
- Generic connectors: Web, OData, ODBC, OLE DB, certified third-party connectors, custom connectors, R/Python script sources, and exported files from unsupported source products.

## Output Requirements

- Produce metadata inventory, candidate facts/dimensions, key candidates, quality concerns, and extraction options.
- Mark unknowns that block model design.
- State the exact Power BI / Power Query connector family, connection mode, gateway/credential need, folding expectation, and production fallback.
- For Excel sources, identify workbook path type, sheets/tables/named ranges, header rows, date/number culture, merged cells, hidden sheets, schema drift risk, and whether the source should be promoted into a governed lakehouse/warehouse before production use.
