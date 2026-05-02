---
name: powerbi-source-system-process-adapter
description: Map industrial process questions to source systems and source objects for Power BI. Use for SAP ECC/S4HANA, SAP BW, SAP Datasphere, Salesforce, Dynamics, Oracle, Infor, IFS, Siemens Teamcenter, Windchill, MES, SCADA, historian, WMS, TMS, ServiceNow, Jira, Excel, data lakes, warehouses, and custom APIs.
---

# Power BI Source System Process Adapter

Use this skill after the industrial process and business question are known.

## Source-System Families

- ERP: SAP ECC/S4HANA, Oracle EBS/Cloud, Microsoft Dynamics 365, Infor, IFS.
- CRM/CPQ: Salesforce, Dynamics Sales, SAP Sales Cloud, CPQ tools.
- Planning: SAP IBP/APO, Kinaxis, Blue Yonder, Anaplan, Excel planning.
- Manufacturing/MES: SAP PP/DS, Siemens Opcenter, PTC, Rockwell, custom MES.
- PLM/Engineering: Teamcenter, Windchill, SAP PLM, Enovia.
- Warehouse/Logistics: EWM, WM, Manhattan, Blue Yonder WMS, TMS, carrier portals.
- Finance/Controlling: SAP FI/CO, Group Reporting, Oracle Financials, consolidation tools.
- Service/Quality: ServiceNow, SAP QM/CS, Salesforce Service, warranty systems.
- Data platforms: SAP BW, Datasphere, Fabric, Synapse, Snowflake, Databricks, SQL Server, lakehouse, data warehouse.

For broad vendor/module catalogs, load `powerbi-erp-crm-system-catalog`.
For cross-system keys and harmonized dimensions, load `powerbi-enterprise-master-data-mapping`.

## Mapping Workflow

1. Identify source of record per process step.
2. Determine extraction path: connector, CDS view, OData, SQL view, BW query, API, file, lakehouse, warehouse.
3. Map source objects to facts and dimensions.
4. Identify document flow keys, master data keys, calendar, currency, unit, plant/company code, and status semantics.
5. Define reconciliation against source transactions, standard reports, or finance totals.
6. Flag source-specific limitations: authorization, delta extraction, deleted records, late postings, and text/status localization.

## Output Requirements

- Include source system, object family, extraction method, grain, keys, delta strategy, validation report, and risks.
- Do not assume SAP table or CDS names are present; mark them as candidates until confirmed.
