# Power BI Data Source Patterns

Power BI can use many source families. Do not assume one connector; first classify the source and its operational constraints.

## Source Families

- Files and folders: Excel, CSV, JSON, XML, Parquet, PDF extracts, SharePoint/OneDrive folders.
- Databases: SQL Server, Azure SQL, PostgreSQL, MySQL, Oracle, DB2, Snowflake, BigQuery, Redshift, Dataverse, Access.
- Analytics stores: Fabric Lakehouse/Warehouse, OneLake, ADLS, Synapse, Spark, Delta/Parquet, semantic models.
- SaaS and business apps: Salesforce, Dynamics, SAP, ServiceNow, Jira, Zendesk, Google Analytics, Marketo, HubSpot, custom OData.
- APIs: REST, GraphQL via custom Power Query, OData feeds, web pages, paginated APIs.
- Streaming/manual: Power BI streaming datasets, push datasets, dataflows, manual Excel inputs.

## Selection Rules

- Prefer import mode for performance and transformation control when latency allows.
- Use DirectQuery for large governed models where source performance and query folding are proven.
- Use Direct Lake when Fabric/OneLake is the governed source and semantic model size demands it.
- Use composite models only when ownership, latency, and security boundaries are clear.
- Keep credentials out of source files; document gateway, tenant, privacy levels, and refresh identity.

