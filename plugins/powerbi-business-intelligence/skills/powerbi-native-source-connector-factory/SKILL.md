---
name: powerbi-native-source-connector-factory
description: Use when a Power BI solution must generate native Power Query connector patterns for any Power BI-supported source, including Excel, files, databases, Fabric, Azure, Power Platform, SaaS, OData, REST, ODBC/OLE DB, semantic models, and custom connectors.
---

# Power BI Native Source Connector Factory

Use this skill whenever source access must be implemented, documented, or reviewed. The default is native Power BI / Power Query connectivity. Embedded demo data is allowed only when explicitly requested for offline tests or when a PBIP preview limitation blocks external query sources.

## Connector Families

- File: Excel Workbook, Text/CSV, XML, JSON, Folder, PDF, Parquet, SharePoint Folder, OneDrive/SharePoint-hosted files.
- Database: SQL Server, Access, SQL Server Analysis Services, Oracle, IBM Db2/Informix/Netezza, MySQL, PostgreSQL, Sybase, Teradata, SAP HANA, SAP BW application/message server, Amazon Redshift/Athena, Impala, Google BigQuery, Vertica, Snowflake, Essbase, AtScale, MariaDB, MarkLogic, MongoDB Atlas SQL, Denodo, Dremio, Exasol, ClickHouse, ODBC, OLE DB, and certified/preview database connectors.
- Microsoft Fabric: Power BI semantic models, Dataflows, Warehouse, Lakehouse, KQL Database.
- Power Platform: Dataverse, Dataflows, legacy CDS/dataflows when required.
- Azure: Azure SQL, Synapse SQL/workspace, Azure Analysis Services, Azure Database for PostgreSQL, Blob Storage, Table Storage, Cosmos DB, Data Explorer/Kusto, ADLS Gen2, HDInsight, Cost Management, Resource Graph, Databricks.
- Online Services and SaaS: SharePoint Online, Exchange, Dynamics 365, Business Central, Customer Insights, Salesforce, ServiceNow, Google Analytics, Adobe, GitHub, Smartsheet, Zendesk, and other Power Query-supported services.
- Other: Web, OData, REST via `Web.Contents`, Hadoop/HDFS, Spark, R/Python scripts, blank query, custom connectors, gateway-backed sources, and replicated export patterns.

## Required Output

- Source family, native connector function, authentication, gateway, privacy level, refresh mode, connection mode, and folding expectation.
- Power Query M template with parameters and no hardcoded secrets.
- Metadata discovery plan, schema drift controls, type conversion, incremental refresh design, and reconciliation checks.
- Fallback path when the exact source has no first-party connector: certified connector, ODBC/OLE DB, OData, REST, file export, dataflow, Fabric pipeline, or replicated warehouse/lakehouse.
- en-US and de-DE documentation notes for source assumptions, credential ownership, gateway dependency, limitations, and validation.

## Excel Native Driver Rule

For Excel, use native Power Query patterns:

```powerquery
let
    Source = Excel.Workbook(File.Contents(ExcelPath), null, true),
    Raw = Source{[Item = SheetOrTableName, Kind = SourceKind]}[Data],
    PromotedHeaders = Table.PromoteHeaders(Raw, [PromoteAllScalars = true]),
    Typed = Table.TransformColumnTypes(PromotedHeaders, TypeMap, Culture)
in
    Typed
```

- For SharePoint/OneDrive Excel files, use `SharePoint.Files` or `SharePoint.Contents`, filter the target file, then call `Excel.Workbook([Content], null, true)`.
- For folders, use `Folder.Files` or `SharePoint.Files`, a transform function, schema union/intersection logic, and file lineage columns.
- Do not convert `.xlsx` to CSV unless the user explicitly requests that architectural compromise.
- Do not embed Excel rows into TMDL `DATATABLE` for production outputs.

## Mode Decision

- `native_connector`: production Power Query connector code.
- `replicated_lakehouse`: source is staged into Fabric/Lakehouse/Warehouse before Power BI.
- `semantic_model_live`: connect to Power BI semantic model / SSAS / AAS with live or DirectQuery constraints.
- `direct_query`: source remains queried at runtime; validate supported transformations.
- `direct_lake`: Fabric Direct Lake pattern.
- `demo_embedded`: generated `DATATABLE` fixture for offline PBIP smoke tests only.

## Checks

- Verify exact connector support and Preview/Beta status against current Microsoft Learn docs when implementation depends on it.
- Never hardcode credentials, tokens, tenant IDs, passwords, or personal file paths in reusable artifacts.
- Flag unsupported DirectQuery or live-connection edits before generating model changes.
