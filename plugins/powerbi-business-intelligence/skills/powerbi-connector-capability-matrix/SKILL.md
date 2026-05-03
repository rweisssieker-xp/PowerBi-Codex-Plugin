---
name: powerbi-connector-capability-matrix
description: Use when selecting Power BI data-source connectors and comparing Import, DirectQuery, Direct Lake, incremental refresh, gateway, SSO, folding, privacy, and refresh limitations.
---

# Power BI Connector Capability Matrix

Choose connector and storage mode based on capability, data volume, security, and latency.

## Output Contract

- Source type and connector candidates.
- Capability matrix: Import, DirectQuery, Direct Lake, composite, folding, incremental refresh, gateway, SSO, OAuth, service principal, and privacy level.
- Recommended pattern with tradeoffs, blockers, fallback, and validation.
- Refresh, performance, and security implications.

## Required Coverage

Cover the full Power BI Desktop / Power Query source universe by category, then narrow to the requested source:

- File: Excel Workbook, Text/CSV, XML, JSON, Folder, PDF, Parquet, SharePoint Folder.
- Database: SQL Server, Access, SSAS, Oracle, IBM Db2/Informix/Netezza, MySQL, PostgreSQL, Sybase, Teradata, SAP HANA, SAP BW application/message server, Amazon Redshift/Athena, Impala, BigQuery, Vertica, Snowflake, Essbase, AtScale, MariaDB, MarkLogic, MongoDB Atlas SQL, Denodo, Dremio, Exasol, ClickHouse, InterSystems, KX/Kyvos, ODBC/OLE DB and other certified/preview database connectors.
- Microsoft Fabric: Power BI semantic models, Dataflows, Warehouses, Lakehouses, KQL databases.
- Power Platform: Dataverse, Dataflows, legacy CDS/dataflows where relevant.
- Azure: Azure SQL, Synapse SQL/workspace, Azure Analysis Services, Azure PostgreSQL, Blob, Table Storage, Cosmos DB, Data Explorer/Kusto, ADLS Gen2, HDInsight, Azure Cost Management, Azure Resource Graph, Databricks and related Azure connectors.
- Online Services/SaaS: SharePoint Online, Exchange, Dynamics 365/Business Central/Customer Insights, Salesforce, Google Analytics, Adobe, ServiceNow, GitHub, Smartsheet, Zendesk and other Power Query-supported SaaS connectors.
- Other: Web, OData, REST APIs via Web.Contents, R/Python scripts, blank query, Hadoop/HDFS, Spark, custom connectors, ODBC/OLE DB, and certified third-party connectors.

When Microsoft adds, removes, renames, or marks connectors as Preview/Beta, follow current Microsoft Learn connector documentation and mark uncertainty explicitly.

## Source Mode Decision

- Use native connector M for production PBIP/TMDL, PBIX design, dataflows, and Fabric implementations.
- Use embedded `DATATABLE` only for isolated smoke tests, reproducible demos, or when Power BI Desktop PBIP preview validation blocks external query-source partitions.
- Document the selected mode as `native_connector`, `replicated_lakehouse`, `semantic_model_live`, `direct_query`, `direct_lake`, or `demo_embedded`.

## Checks

- Verify connector capabilities against current Microsoft documentation when exact behavior matters.
- Do not assume folding for custom SQL, APIs, or complex transformations.
- For Excel specifically, prefer the native Excel Workbook connector and document whether the path is local/network, SharePoint, OneDrive, or folder-combine.
