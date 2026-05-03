---
name: powerbi-ai-native-source-router
description: Use when each source table or query must be routed to the correct native Power Query connector pattern, including Excel, CSV, Folder, SharePoint, SQL, Fabric, OData, REST, SaaS, ODBC/OLE DB, or embedded demo mode.
---

# Power BI AI Native Source Router

Use this skill when source access must be generated or reviewed.

## Routing Rules

- Prefer first-party/native Power Query connectors for production.
- Use `Excel.Workbook` for Excel workbook sheets and tables.
- Use `Csv.Document` for CSV files.
- Use `Folder.Files` or `SharePoint.Files` for file collections.
- Use database connectors for SQL/Fabric/Snowflake/Databricks and similar systems.
- Use `OData.Feed` or `Web.Contents` only when native service connectors are not suitable.
- Use embedded `DATATABLE` only for offline demos and smoke-test fixtures.

## Output Requirements

- For every table: source family, connector function, path/endpoint pattern, auth, gateway, privacy, refresh mode, folding expectation, and fallback.
- Flag missing source objects before generating M.

