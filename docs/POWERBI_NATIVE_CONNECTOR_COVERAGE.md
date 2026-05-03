# Power BI Native Connector Coverage

## en-US

The plugin must treat native Power BI / Power Query connectivity as the default for real implementations. Synthetic `DATATABLE` output is only a test fixture strategy for offline PBIP smoke tests or Power BI Desktop preview limitations.

### Connector Coverage Scope

The connector catalog follows the Power BI Desktop Get Data categories and the Power Query connector list:

- File: Excel Workbook, Text/CSV, XML, JSON, Folder, PDF, Parquet, SharePoint Folder, OneDrive/SharePoint-hosted files.
- Database: SQL Server, Access, SQL Server Analysis Services, Oracle, IBM Db2/Informix/Netezza, MySQL, PostgreSQL, Sybase, Teradata, SAP HANA, SAP BW application/message server, Amazon Redshift/Athena, Impala, Google BigQuery, Vertica, Snowflake, Essbase, AtScale, MariaDB, MarkLogic, MongoDB Atlas SQL, Denodo, Dremio, Exasol, ClickHouse, ODBC/OLE DB, and certified/preview database connectors.
- Microsoft Fabric: Power BI semantic models, Dataflows, Warehouse, Lakehouse, KQL Database.
- Power Platform: Dataverse, Dataflows, legacy CDS/dataflows when required.
- Azure: Azure SQL, Synapse SQL/workspace, Azure Analysis Services, Azure Database for PostgreSQL, Blob Storage, Table Storage, Cosmos DB, Data Explorer/Kusto, ADLS Gen2, HDInsight, Azure Cost Management, Azure Resource Graph, Databricks.
- Online Services and SaaS: SharePoint Online, Exchange, Dynamics 365, Business Central, Customer Insights, Salesforce, ServiceNow, Google Analytics, Adobe, GitHub, Smartsheet, Zendesk, and other Power Query-supported services.
- Other: Web, OData, REST through `Web.Contents`, Hadoop/HDFS, Spark, R/Python scripts, blank query, custom connectors, gateway-backed sources, and replicated export patterns.

### Excel Native Pattern

For Excel, generate native M:

```powerquery
let
    Source = Excel.Workbook(File.Contents(ExcelPath), null, true),
    Raw = Source{[Item = SheetOrTableName, Kind = SourceKind]}[Data],
    PromotedHeaders = Table.PromoteHeaders(Raw, [PromoteAllScalars = true]),
    Typed = Table.TransformColumnTypes(PromotedHeaders, TypeMap, Culture)
in
    Typed
```

For SharePoint or OneDrive-hosted Excel files, use `SharePoint.Files` or `SharePoint.Contents` and pass the binary `[Content]` to `Excel.Workbook`.

### Required Decisions

Every source design must state:

- Native connector function.
- Import, DirectQuery, Direct Lake, live connection, composite, or embedded demo mode.
- Gateway requirement.
- Authentication and credential owner.
- Privacy level.
- Query folding expectation.
- Incremental refresh approach.
- Schema drift and data quality controls.
- Reconciliation totals.
- Known connector limitations and Preview/Beta status.

## de-DE

Das Plugin muss fuer echte Implementierungen native Power BI / Power Query Konnektivitaet als Standard verwenden. Synthetische `DATATABLE`-Ausgaben sind nur fuer Offline-Demos, reproduzierbare Smoke-Tests oder PBIP-Preview-Limitierungen erlaubt.

### Abdeckung

Die Quellenabdeckung folgt den Power BI Desktop Get-Data-Kategorien und der Power Query Connector-Liste:

- Datei: Excel Workbook, Text/CSV, XML, JSON, Folder, PDF, Parquet, SharePoint Folder, OneDrive-/SharePoint-Dateien.
- Datenbanken: SQL Server, Access, SQL Server Analysis Services, Oracle, IBM Db2/Informix/Netezza, MySQL, PostgreSQL, Sybase, Teradata, SAP HANA, SAP BW Application/Message Server, Amazon Redshift/Athena, Impala, Google BigQuery, Vertica, Snowflake, Essbase, AtScale, MariaDB, MarkLogic, MongoDB Atlas SQL, Denodo, Dremio, Exasol, ClickHouse, ODBC/OLE DB und zertifizierte/Preview-Connectoren.
- Microsoft Fabric: Power BI Semantic Models, Dataflows, Warehouse, Lakehouse, KQL Database.
- Power Platform: Dataverse, Dataflows, Legacy CDS/Dataflows falls erforderlich.
- Azure: Azure SQL, Synapse SQL/Workspace, Azure Analysis Services, Azure Database for PostgreSQL, Blob Storage, Table Storage, Cosmos DB, Data Explorer/Kusto, ADLS Gen2, HDInsight, Azure Cost Management, Azure Resource Graph, Databricks.
- Online Services und SaaS: SharePoint Online, Exchange, Dynamics 365, Business Central, Customer Insights, Salesforce, ServiceNow, Google Analytics, Adobe, GitHub, Smartsheet, Zendesk und weitere Power Query Services.
- Sonstige: Web, OData, REST ueber `Web.Contents`, Hadoop/HDFS, Spark, R/Python Scripts, Blank Query, Custom Connectors, Gateway-Quellen und replizierte Exportmuster.

### Excel-Regel

Excel wird nativ gelesen, nicht als CSV-Ersatz und nicht als eingebettete Produktionsdaten. Fuer lokale oder Netzwerkdateien gilt `Excel.Workbook(File.Contents(...), null, true)`. Fuer SharePoint/OneDrive wird die Datei ueber `SharePoint.Files` oder `SharePoint.Contents` als Binary geladen und danach an `Excel.Workbook` uebergeben.

### Pflichtentscheidungen

Jedes Quellendesign muss Connector, Modus, Gateway, Authentifizierung, Privacy Level, Query Folding, Refresh, Schema Drift, Datenqualitaet, Abstimmwerte und Connector-Limitationen dokumentieren.

## References

- [Data sources in Power BI Desktop](https://learn.microsoft.com/en-us/power-bi/connect-data/desktop-data-sources)
- [Power Query connectors](https://learn.microsoft.com/en-us/power-query/connectors/)
