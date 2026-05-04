"""Build Power BI source capability and process source-routing artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "data" / "industry_process_catalog.json"
MATRIX_PATH = ROOT / "data" / "powerbi_source_capability_matrix.json"
ROUTING_ROOT = ROOT / "outputs" / "source-routing"


CONNECTOR_CATEGORIES = [
    {
        "category": "File",
        "connectors": [
            {"name": "Excel Workbook", "function": "Excel.Workbook", "modes": ["Import"], "gateway": True, "folding": False, "productionUse": True},
            {"name": "Text/CSV", "function": "Csv.Document", "modes": ["Import"], "gateway": True, "folding": False, "productionUse": True},
            {"name": "XML", "function": "Xml.Tables", "modes": ["Import"], "gateway": True, "folding": False, "productionUse": True},
            {"name": "JSON", "function": "Json.Document", "modes": ["Import"], "gateway": True, "folding": False, "productionUse": True},
            {"name": "Folder", "function": "Folder.Files", "modes": ["Import"], "gateway": True, "folding": False, "productionUse": True},
            {"name": "PDF", "function": "Pdf.Tables", "modes": ["Import"], "gateway": True, "folding": False, "productionUse": True},
            {"name": "Parquet", "function": "Parquet.Document", "modes": ["Import"], "gateway": True, "folding": False, "productionUse": True},
            {"name": "SharePoint Folder", "function": "SharePoint.Files", "modes": ["Import"], "gateway": False, "folding": False, "productionUse": True},
        ],
    },
    {
        "category": "Database",
        "connectors": [
            {"name": "SQL Server database", "function": "Sql.Database", "modes": ["Import", "DirectQuery"], "gateway": True, "folding": True, "productionUse": True},
            {"name": "Access database", "function": "Access.Database", "modes": ["Import"], "gateway": True, "folding": False, "productionUse": True},
            {"name": "SQL Server Analysis Services database", "function": "AnalysisServices.Database", "modes": ["Import", "LiveConnection"], "gateway": True, "folding": "n/a", "productionUse": True},
            {"name": "Oracle database", "function": "Oracle.Database", "modes": ["Import", "DirectQuery"], "gateway": True, "folding": True, "productionUse": True},
            {"name": "IBM Db2 database", "function": "DB2.Database", "modes": ["Import", "DirectQuery"], "gateway": True, "folding": True, "productionUse": True},
            {"name": "IBM Informix database", "function": "Informix.Database", "modes": ["Import"], "gateway": True, "folding": True, "productionUse": False, "status": "Beta"},
            {"name": "IBM Netezza", "function": "Netezza.Database", "modes": ["Import"], "gateway": True, "folding": True, "productionUse": True},
            {"name": "MySQL database", "function": "MySQL.Database", "modes": ["Import", "DirectQuery"], "gateway": True, "folding": True, "productionUse": True},
            {"name": "PostgreSQL database", "function": "PostgreSQL.Database", "modes": ["Import", "DirectQuery"], "gateway": True, "folding": True, "productionUse": True},
            {"name": "Sybase database", "function": "Sybase.Database", "modes": ["Import"], "gateway": True, "folding": True, "productionUse": True},
            {"name": "Teradata database", "function": "Teradata.Database", "modes": ["Import", "DirectQuery"], "gateway": True, "folding": True, "productionUse": True},
            {"name": "SAP HANA database", "function": "SapHana.Database", "modes": ["Import", "DirectQuery"], "gateway": True, "folding": True, "productionUse": True},
            {"name": "SAP Business Warehouse Application Server", "function": "SapBusinessWarehouse.Cubes", "modes": ["Import", "DirectQuery"], "gateway": True, "folding": "source-dependent", "productionUse": True},
            {"name": "SAP Business Warehouse Message Server", "function": "SapBusinessWarehouse.Cubes", "modes": ["Import", "DirectQuery"], "gateway": True, "folding": "source-dependent", "productionUse": True},
            {"name": "Amazon Redshift", "function": "AmazonRedshift.Database", "modes": ["Import", "DirectQuery"], "gateway": False, "folding": True, "productionUse": True},
            {"name": "Impala", "function": "Impala.Database", "modes": ["Import", "DirectQuery"], "gateway": True, "folding": True, "productionUse": True},
            {"name": "Google BigQuery", "function": "GoogleBigQuery.Database", "modes": ["Import", "DirectQuery"], "gateway": False, "folding": True, "productionUse": True},
            {"name": "Vertica", "function": "Vertica.Database", "modes": ["Import"], "gateway": True, "folding": True, "productionUse": True},
            {"name": "Snowflake", "function": "Snowflake.Databases", "modes": ["Import", "DirectQuery"], "gateway": False, "folding": True, "productionUse": True},
            {"name": "Essbase", "function": "Essbase.Cubes", "modes": ["Import"], "gateway": True, "folding": "source-dependent", "productionUse": True},
            {"name": "Amazon Athena", "function": "AmazonAthena.Databases", "modes": ["Import", "DirectQuery"], "gateway": False, "folding": True, "productionUse": True},
            {"name": "MariaDB", "function": "MariaDB.Contents", "modes": ["Import"], "gateway": True, "folding": True, "productionUse": True},
            {"name": "MarkLogic", "function": "MarkLogic.Database", "modes": ["Import"], "gateway": True, "folding": True, "productionUse": True},
            {"name": "MongoDB Atlas SQL", "function": "MongoDBAtlasODBC.Database", "modes": ["Import", "DirectQuery"], "gateway": False, "folding": True, "productionUse": True},
            {"name": "Denodo", "function": "Denodo.Contents", "modes": ["Import", "DirectQuery"], "gateway": True, "folding": True, "productionUse": True},
            {"name": "Dremio Software", "function": "Dremio.Databases", "modes": ["Import", "DirectQuery"], "gateway": True, "folding": True, "productionUse": True},
            {"name": "Dremio Cloud", "function": "DremioCloud.Databases", "modes": ["Import", "DirectQuery"], "gateway": False, "folding": True, "productionUse": True},
            {"name": "Exasol", "function": "Exasol.Database", "modes": ["Import", "DirectQuery"], "gateway": True, "folding": True, "productionUse": True},
            {"name": "ClickHouse", "function": "ClickHouse.Database", "modes": ["Import", "DirectQuery"], "gateway": True, "folding": True, "productionUse": False, "status": "Beta"},
            {"name": "ODBC", "function": "Odbc.DataSource", "modes": ["Import", "DirectQuery"], "gateway": True, "folding": "driver-dependent", "productionUse": True},
            {"name": "OLE DB", "function": "OleDb.DataSource", "modes": ["Import"], "gateway": True, "folding": "provider-dependent", "productionUse": True},
        ],
    },
    {
        "category": "Microsoft Fabric",
        "connectors": [
            {"name": "Power BI semantic models", "function": "AnalysisServices.Database", "modes": ["LiveConnection", "DirectQuery"], "gateway": False, "folding": "n/a", "productionUse": True},
            {"name": "Dataflows", "function": "PowerPlatform.Dataflows", "modes": ["Import"], "gateway": False, "folding": False, "productionUse": True},
            {"name": "Warehouses", "function": "Sql.Database", "modes": ["Import", "DirectQuery"], "gateway": False, "folding": True, "productionUse": True},
            {"name": "Lakehouses", "function": "Lakehouse.Contents", "modes": ["Import", "Direct Lake", "DirectQuery"], "gateway": False, "folding": True, "productionUse": True},
            {"name": "KQL Databases", "function": "Kusto.Contents", "modes": ["Import", "DirectQuery"], "gateway": False, "folding": True, "productionUse": True},
        ],
    },
    {
        "category": "Power Platform",
        "connectors": [
            {"name": "Dataverse", "function": "CommonDataService.Database", "modes": ["Import", "DirectQuery"], "gateway": False, "folding": True, "productionUse": True},
            {"name": "Dataflows", "function": "PowerPlatform.Dataflows", "modes": ["Import"], "gateway": False, "folding": False, "productionUse": True},
            {"name": "Power BI dataflows (Legacy)", "function": "PowerBI.Dataflows", "modes": ["Import"], "gateway": False, "folding": False, "productionUse": True},
        ],
    },
    {
        "category": "Azure",
        "connectors": [
            {"name": "Azure SQL Database", "function": "Sql.Database", "modes": ["Import", "DirectQuery"], "gateway": False, "folding": True, "productionUse": True},
            {"name": "Azure Synapse Analytics SQL", "function": "Sql.Database", "modes": ["Import", "DirectQuery"], "gateway": False, "folding": True, "productionUse": True},
            {"name": "Azure Analysis Services database", "function": "AnalysisServices.Database", "modes": ["Import", "LiveConnection"], "gateway": False, "folding": "n/a", "productionUse": True},
            {"name": "Azure Database for PostgreSQL", "function": "PostgreSQL.Database", "modes": ["Import", "DirectQuery"], "gateway": False, "folding": True, "productionUse": True},
            {"name": "Azure Blob Storage", "function": "AzureStorage.Blobs", "modes": ["Import"], "gateway": False, "folding": False, "productionUse": True},
            {"name": "Azure Table Storage", "function": "AzureStorage.Tables", "modes": ["Import"], "gateway": False, "folding": False, "productionUse": True},
            {"name": "Azure Cosmos DB v1", "function": "DocumentDB.Contents", "modes": ["Import"], "gateway": False, "folding": False, "productionUse": True},
            {"name": "Azure Cosmos DB v2", "function": "CosmosDB.Database", "modes": ["Import", "DirectQuery"], "gateway": False, "folding": True, "productionUse": True},
            {"name": "Azure Data Explorer (Kusto)", "function": "Kusto.Contents", "modes": ["Import", "DirectQuery"], "gateway": False, "folding": True, "productionUse": True},
            {"name": "Azure Data Lake Storage Gen2", "function": "AzureStorage.DataLake", "modes": ["Import", "Direct Lake"], "gateway": False, "folding": False, "productionUse": True},
            {"name": "Azure HDInsight (HDFS)", "function": "Hdfs.Files", "modes": ["Import"], "gateway": True, "folding": False, "productionUse": True},
            {"name": "Azure HDInsight Spark", "function": "Spark.Tables", "modes": ["Import", "DirectQuery"], "gateway": True, "folding": True, "productionUse": True},
            {"name": "HDInsight Interactive Query", "function": "Hive LLAP", "modes": ["Import", "DirectQuery"], "gateway": True, "folding": True, "productionUse": True},
            {"name": "Azure Cost Management", "function": "AzureCostManagement.Contents", "modes": ["Import"], "gateway": False, "folding": False, "productionUse": True},
            {"name": "Azure Resource Graph", "function": "AzureResourceGraph.Contents", "modes": ["Import"], "gateway": False, "folding": False, "productionUse": True},
            {"name": "Azure Databricks", "function": "Databricks.Catalogs", "modes": ["Import", "DirectQuery"], "gateway": False, "folding": True, "productionUse": True},
        ],
    },
    {
        "category": "Online Services",
        "connectors": [
            {"name": "SharePoint Online List", "function": "SharePoint.Tables", "modes": ["Import"], "gateway": False, "folding": False, "productionUse": True},
            {"name": "Exchange Online", "function": "Exchange.Contents", "modes": ["Import"], "gateway": False, "folding": False, "productionUse": True},
            {"name": "Dynamics 365", "function": "OData.Feed", "modes": ["Import"], "gateway": False, "folding": "service-dependent", "productionUse": True},
            {"name": "Business Central", "function": "Dynamics365BusinessCentral.Contents", "modes": ["Import"], "gateway": False, "folding": "service-dependent", "productionUse": True},
            {"name": "Salesforce Objects", "function": "Salesforce.Data", "modes": ["Import"], "gateway": False, "folding": "service-dependent", "productionUse": True},
            {"name": "Salesforce Reports", "function": "Salesforce.Reports", "modes": ["Import"], "gateway": False, "folding": False, "productionUse": True},
            {"name": "ServiceNow", "function": "ServiceNow.Tables", "modes": ["Import"], "gateway": False, "folding": "service-dependent", "productionUse": True},
            {"name": "Google Analytics", "function": "GoogleAnalytics.Accounts", "modes": ["Import"], "gateway": False, "folding": False, "productionUse": True},
            {"name": "Adobe Analytics", "function": "AdobeAnalytics.Cubes", "modes": ["Import"], "gateway": False, "folding": False, "productionUse": True},
            {"name": "GitHub", "function": "Web.Contents", "modes": ["Import"], "gateway": False, "folding": False, "productionUse": True},
            {"name": "Smartsheet", "function": "Smartsheet.Tables", "modes": ["Import"], "gateway": False, "folding": False, "productionUse": True},
            {"name": "Zendesk", "function": "Zendesk.Tables", "modes": ["Import"], "gateway": False, "folding": False, "productionUse": True},
        ],
    },
    {
        "category": "Other",
        "connectors": [
            {"name": "Web", "function": "Web.Contents", "modes": ["Import"], "gateway": False, "folding": False, "productionUse": True},
            {"name": "OData", "function": "OData.Feed", "modes": ["Import"], "gateway": True, "folding": "service-dependent", "productionUse": True},
            {"name": "REST API", "function": "Web.Contents", "modes": ["Import"], "gateway": True, "folding": False, "productionUse": True},
            {"name": "Hadoop/HDFS", "function": "Hdfs.Files", "modes": ["Import"], "gateway": True, "folding": False, "productionUse": True},
            {"name": "Spark", "function": "Spark.Tables", "modes": ["Import", "DirectQuery"], "gateway": True, "folding": True, "productionUse": True},
            {"name": "R script", "function": "R.Execute", "modes": ["Import"], "gateway": True, "folding": False, "productionUse": True},
            {"name": "Python script", "function": "Python.Execute", "modes": ["Import"], "gateway": True, "folding": False, "productionUse": True},
            {"name": "Blank query", "function": "let ... in ...", "modes": ["Import"], "gateway": "depends", "folding": "depends", "productionUse": True},
            {"name": "Custom connector", "function": "Extension.Contents", "modes": ["Import", "DirectQuery"], "gateway": "depends", "folding": "connector-dependent", "productionUse": True},
        ],
    },
]


DOMAIN_DEFAULTS = {
    "Commercial": ["Salesforce Objects", "Dynamics 365", "Dataverse", "OData", "SQL Server database", "Snowflake", "Lakehouses", "REST API"],
    "Procurement": ["SAP HANA database", "SAP Business Warehouse Application Server", "OData", "Oracle database", "SQL Server database", "Dataverse", "REST API"],
    "Supply Chain": ["SAP HANA database", "SQL Server database", "Oracle database", "Snowflake", "Azure Synapse Analytics SQL", "Lakehouses", "REST API"],
    "Manufacturing": ["SAP HANA database", "SQL Server database", "Oracle database", "Spark", "Azure Data Explorer (Kusto)", "Databricks", "REST API"],
    "Engineering": ["OData", "REST API", "SQL Server database", "Oracle database", "Dataverse", "SharePoint Folder", "Parquet"],
    "Maintenance": ["SQL Server database", "Oracle database", "OData", "REST API", "Azure Data Explorer (Kusto)", "Dataverse"],
    "Service": ["Salesforce Objects", "Dynamics 365", "ServiceNow", "Dataverse", "OData", "REST API", "SQL Server database"],
    "Finance": ["SAP HANA database", "SAP Business Warehouse Application Server", "SQL Server database", "Oracle database", "Snowflake", "Power BI semantic models", "Dataflows"],
    "Workforce": ["OData", "REST API", "SQL Server database", "Dataverse", "Excel Workbook", "SharePoint Folder"],
    "Warehouse": ["SQL Server database", "Oracle database", "SAP HANA database", "OData", "REST API", "Snowflake"],
    "Quality": ["SQL Server database", "Oracle database", "OData", "REST API", "Dataverse", "SharePoint Folder"],
    "EHS": ["Dataverse", "SQL Server database", "OData", "REST API", "SharePoint Online List"],
    "Projects": ["SQL Server database", "Oracle database", "OData", "Power BI semantic models", "Snowflake"],
    "Governance": ["Power BI semantic models", "Dataflows", "Dataverse", "Azure Resource Graph", "REST API", "Excel Workbook"],
    "Analytics": ["Power BI semantic models", "Dataflows", "Lakehouses", "Warehouses", "SQL Server database", "REST API"],
}


SYSTEM_KEYWORDS = {
    "ERP": ["SAP HANA database", "SAP Business Warehouse Application Server", "OData", "SQL Server database", "Oracle database"],
    "CRM": ["Salesforce Objects", "Dynamics 365", "Dataverse", "OData", "REST API"],
    "CPQ": ["Salesforce Objects", "Dynamics 365", "OData", "REST API"],
    "CLM": ["OData", "REST API", "SharePoint Online List", "SQL Server database"],
    "WMS": ["SQL Server database", "Oracle database", "OData", "REST API"],
    "TMS": ["OData", "REST API", "SQL Server database"],
    "MES": ["SQL Server database", "Azure Data Explorer (Kusto)", "Spark", "REST API"],
    "QMS": ["SQL Server database", "Dataverse", "OData", "REST API"],
    "EAM": ["SQL Server database", "Oracle database", "OData", "REST API"],
    "CMMS": ["SQL Server database", "OData", "REST API"],
    "HCM": ["OData", "REST API", "SQL Server database"],
    "EPM": ["Power BI semantic models", "Dataflows", "SQL Server database", "Oracle database"],
    "GRC": ["Dataverse", "SQL Server database", "OData", "REST API"],
    "PLM": ["OData", "REST API", "SQL Server database", "SharePoint Folder"],
    "IBP": ["SAP HANA database", "OData", "SQL Server database", "Snowflake"],
    "Historian": ["Azure Data Explorer (Kusto)", "SQL Server database", "Spark", "REST API"],
    "Data Warehouse": ["SQL Server database", "Snowflake", "Azure Synapse Analytics SQL", "Google BigQuery", "Databricks"],
}


def connector_lookup() -> dict[str, dict[str, object]]:
    lookup: dict[str, dict[str, object]] = {}
    for category in CONNECTOR_CATEGORIES:
        for connector in category["connectors"]:
            enriched = dict(connector)
            enriched["category"] = category["category"]
            lookup[str(connector["name"])] = enriched
    return lookup


def ordered_unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def route_process(process: dict[str, object], lookup: dict[str, dict[str, object]]) -> dict[str, object]:
    names: list[str] = []
    names.extend(DOMAIN_DEFAULTS.get(str(process["domain"]), []))
    for source_system in process.get("sourceSystems", []):
        source_text = str(source_system)
        for keyword, connector_names in SYSTEM_KEYWORDS.items():
            if keyword.lower() in source_text.lower():
                names.extend(connector_names)
    names.extend(["Excel Workbook", "Text/CSV", "Folder", "SharePoint Folder", "Web", "OData", "REST API", "Custom connector"])
    names = ordered_unique([name for name in names if name in lookup])
    primary = names[:8]
    return {
        "processId": process["processId"],
        "processName": process["name"],
        "domain": process["domain"],
        "sourceSystems": process["sourceSystems"],
        "productionSourceRouting": [
            {
                "connector": name,
                "category": lookup[name]["category"],
                "powerQueryFunction": lookup[name]["function"],
                "supportedModes": lookup[name]["modes"],
                "gatewayRequired": lookup[name]["gateway"],
                "queryFolding": lookup[name]["folding"],
                "productionUse": lookup[name]["productionUse"],
            }
            for name in primary
        ],
        "fallbackPatterns": [
            {
                "connector": name,
                "category": lookup[name]["category"],
                "powerQueryFunction": lookup[name]["function"],
                "supportedModes": lookup[name]["modes"],
                "gatewayRequired": lookup[name]["gateway"],
                "queryFolding": lookup[name]["folding"],
                "productionUse": lookup[name]["productionUse"],
            }
            for name in names[8:]
        ],
        "requiredSourceDecisions": [
            "native connector",
            "Import / DirectQuery / Direct Lake / live connection / composite mode",
            "gateway and credential owner",
            "privacy level",
            "query folding expectation",
            "incremental refresh design",
            "schema drift handling",
            "data quality and reconciliation totals",
        ],
    }


def write_matrix() -> None:
    payload = {
        "version": "2026-05-04",
        "basis": [
            "Power BI Desktop Get Data categories",
            "Power Query connector capabilities",
            "Production routing must prefer native connectors over demo CSV extracts",
        ],
        "sourceCategories": CONNECTOR_CATEGORIES,
        "coverageRule": "All process packs must declare demo CSV routing and production native-source routing. Demo CSV is not a substitute for production source connectivity.",
    }
    MATRIX_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_routing() -> None:
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    lookup = connector_lookup()
    routes = [route_process(process, lookup) for process in catalog["processes"]]
    ROUTING_ROOT.mkdir(parents=True, exist_ok=True)
    (ROUTING_ROOT / "process_source_routing.json").write_text(json.dumps({"routes": routes}, indent=2) + "\n", encoding="utf-8")
    with (ROUTING_ROOT / "process_source_routing.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["ProcessID", "ProcessName", "Domain", "Connector", "Category", "Modes", "PowerQueryFunction"])
        writer.writeheader()
        for route in routes:
            for connector in route["productionSourceRouting"]:
                writer.writerow(
                    {
                        "ProcessID": route["processId"],
                        "ProcessName": route["processName"],
                        "Domain": route["domain"],
                        "Connector": connector["connector"],
                        "Category": connector["category"],
                        "Modes": "; ".join(connector["supportedModes"]),
                        "PowerQueryFunction": connector["powerQueryFunction"],
                    }
                )
    (ROUTING_ROOT / "README.md").write_text(
        "# Power BI Source Routing\n\n"
        "Production source-routing recommendations for all industrial process packs.\n\n"
        "- `process_source_routing.json`: full process-to-connector routing map.\n"
        "- `process_source_routing.csv`: flat routing index for Power BI ingestion.\n\n"
        "Demo CSV folders are included for repeatable offline testing. Production implementations must replace demo routing with validated native Power BI / Power Query connectors according to `data/powerbi_source_capability_matrix.json`.\n",
        encoding="utf-8",
    )


def main() -> int:
    write_matrix()
    write_routing()
    print("generated Power BI source capability matrix and process routing")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
