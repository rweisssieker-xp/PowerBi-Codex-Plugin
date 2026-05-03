---
name: powerbi-powerquery-code-generator
description: Use when Power BI work needs Power Query M designs or code for APIs, SAP OData, SQL, files, pagination, incremental refresh, schema drift, error handling, typing, and folding.
---

# Power BI Power Query Code Generator

Generate Power Query/M extraction designs with refresh reliability and governance.

## Output Contract

- Connector, authentication pattern, gateway need, query folding expectation, privacy level, and refresh mode.
- M query structure, parameters, pagination, retry/error handling, type conversion, schema drift handling, and incremental refresh fields.
- Validation: row count, duplicate keys, null checks, source totals, freshness, and folding diagnostics.
- Security and PII handling notes.

## Native Connector Rule

- Prefer the native Power BI / Power Query connector function for the requested source. Do not replace real sources with embedded `DATATABLE` data except for offline demos, smoke tests, or explicitly requested synthetic fixtures.
- For Excel workbooks, generate native Power Query using `Excel.Workbook(File.Contents(path), null, true)` for local/network files, `SharePoint.Files` / `SharePoint.Contents` for SharePoint-hosted files, or the appropriate OneDrive/SharePoint connector path. Do not parse `.xlsx` as CSV and do not embed workbook rows into TMDL for production output.
- For folders of Excel/CSV/Parquet files, use `Folder.Files` or `SharePoint.Files` with file filters, schema-drift handling, and a typed transform function.
- For relational systems, use the native connector where available: `Sql.Database`, `Oracle.Database`, `PostgreSQL.Database`, `MySQL.Database`, `Snowflake.Databases`, `GoogleBigQuery.Database`, `Redshift.Database`, `Teradata.Database`, `SapHana.Database`, or the documented equivalent.
- For SAP, prefer released CDS/OData/BW/HANA connectors over direct table scraping unless the architecture explicitly uses replicated SAP tables in a warehouse/lakehouse.
- For REST/OData/SaaS, use `OData.Feed` or `Web.Contents` with pagination, throttling, retry, and credential-safe parameterization.
- For Fabric, Lakehouse, Warehouse, Dataflows, Dataverse, Azure, and Power BI semantic models, preserve the intended connection mode and document Import, DirectQuery, Direct Lake, live connection, or composite constraints.

## Checks

- Prefer foldable source-side filters for large sources.
- Never hardcode secrets in M.
- If a requested source is not available as a first-party Power BI connector, produce the closest supported Power Query path: ODBC/OLE DB, REST API, OData, generic web, file export, dataflow, Fabric pipeline, or replicated warehouse/lakehouse pattern.
