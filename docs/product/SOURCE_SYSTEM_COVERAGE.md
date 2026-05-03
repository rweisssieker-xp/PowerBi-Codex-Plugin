# Source System Coverage

<!-- bilingual-doc-header -->
## en-US Documentation

This document describes source-system coverage across ERP, CRM, industrial systems, finance, planning, data platforms, documents, workflow, and security tools.

## de-DE Dokumentation

Dieses Dokument beschreibt die Quellsystemabdeckung fuer ERP, CRM, industrielle Systeme, Finance, Planning, Datenplattformen, Dokumente, Workflow und Security-Tools.

<!-- /bilingual-doc-header -->


The plugin is source-system-aware. It does not assume that every customer uses the same tables, APIs, extensions, or warehouse naming conventions. Source objects are candidate mappings until validated against metadata.

Native Power BI / Power Query connector use is mandatory for real implementations. The plugin may generate embedded demo data only for offline test fixtures. See [Power BI Native Connector Coverage](POWERBI_NATIVE_CONNECTOR_COVERAGE.md).

## de-DE Kurzfassung

Das Plugin kennt typische ERP-, CRM-, Industrie-, QM-, WHS-, Finance-, Planning-, Compliance-, Datenplattform- und Integrationssysteme. Konkrete Tabellen, APIs, Views und Felder gelten immer nur als Kandidaten, bis sie gegen Kunden-Metadaten, Quellsysteme oder replizierte Daten validiert wurden.

Fuer echte Implementierungen muessen native Power BI / Power Query Connectoren genutzt werden. Eingebettete Demo-Daten sind nur fuer Offline-Testartefakte erlaubt. Siehe [Power BI Native Connector Coverage](POWERBI_NATIVE_CONNECTOR_COVERAGE.md).

## ERP and CRM

- SAP ECC, SAP S/4HANA, SAP BW/4HANA, SAP Datasphere.
- Microsoft Dynamics 365 Finance, Supply Chain, Sales, Customer Service, Field Service, Business Central, Dataverse.
- Salesforce Sales Cloud, Service Cloud, Revenue Cloud, Field Service.
- Oracle Fusion Cloud ERP, EBS, NetSuite.
- Infor, IFS, Epicor, QAD, Sage, Workday.
- ServiceNow, HubSpot, Zendesk.

## Industrial Systems

- MES, SCADA, historians, IoT platforms.
- PLM and engineering platforms: Siemens, PTC, Dassault and related CAD/BOM sources.
- EAM/CMMS and maintenance systems.
- WMS/WHS: SAP EWM/WM, Manhattan, Blue Yonder, Koerber, Infor WMS, Oracle WMS, Dynamics WHS.
- TMS and logistics visibility: project44, FourKites, Transporeon, Shippeo, Descartes, carrier APIs.

## Quality, Warehouse, and Compliance

- QM/QMS/EHS: SAP QM/EHS, ETQ, MasterControl, TrackWise, Intelex, Sphera, Enablon, Veeva Quality, LIMS.
- ESG: SAP Sustainability Control Tower, Microsoft Sustainability Manager, Workiva ESG, EcoVadis, Persefoni.
- GRC/audit/tax: SAP GRC, AuditBoard, Workiva, Diligent, Vertex, Avalara, ONESOURCE.

## Finance, Planning, and Revenue

- EPM and planning: SAP SAC/BPC, Anaplan, Board, OneStream, Oracle EPM, Workday Adaptive, Jedox, Pigment, Tagetik.
- Treasury: Kyriba, SAP Treasury, Serrala, TIS, Coupa Treasury, banking APIs, EBICS, SWIFT.
- Subscription and revenue: Zuora, Chargebee, Stripe Billing, Salesforce Revenue Cloud, SAP BRIM, Oracle Revenue Management.

## Data Platforms and Integration

- Microsoft Fabric, Power BI semantic models, Lakehouse, Warehouse, Dataflows.
- Snowflake, Databricks, BigQuery, Redshift, Synapse, Teradata, Exasol.
- Azure Data Factory, Fabric Data Factory, Informatica, Talend, Fivetran, Matillion, dbt, Airbyte, Boomi, MuleSoft, Celigo, SSIS.
- Data quality and observability: Great Expectations, Soda, Monte Carlo, Bigeye, Anomalo, dbt tests, Deequ.

## Document, Workflow, and Security

- ECM and documents: SharePoint, OpenText, DocuWare, M-Files, Hyland OnBase, Box, Google Drive.
- OCR/IDP: ABBYY, Kofax, OpenText VIM, Basware, Esker, Rossum, Azure AI Document Intelligence.
- Low-code and workflow: Power Apps, Power Automate, UiPath, Automation Anywhere, Blue Prism, Nintex, Camunda, Appian, Pega.
- Identity and access: Entra ID, Okta, Ping Identity, SailPoint, CyberArk, BeyondTrust, Saviynt.

## Validation Rule

Never rely on vendor memory alone. Validate:

- Object names.
- Field semantics.
- Key uniqueness.
- Date meaning.
- Status lifecycle.
- Currency and unit logic.
- Company, plant, warehouse, and fiscal calendar scope.
- Replication latency and transformation rules.
