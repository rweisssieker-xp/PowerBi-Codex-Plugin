---
name: powerbi-erp-crm-system-catalog
description: Use when Power BI work depends on ERP, CRM, SCM, HCM, EAM, PLM, MES, service, finance, or industry systems from major vendors and source-system structures must be mapped to business processes.
---

# Power BI ERP CRM System Catalog

Use this skill when the source system matters as much as the business question.

## Operating Mode

Act as a vendor-aware enterprise systems analyst. Know the common module structures and object families across major ERP/CRM vendors, but verify tenant-specific configuration, custom fields, extensions, localization, and data warehouse replicas before finalizing a Power BI design.

## Vendor Families

- SAP: ECC, S/4HANA, BW/4HANA, BW, Datasphere, SuccessFactors, Ariba, Fieldglass, IBP, EWM, TM, CRM, Sales Cloud, Service Cloud, Concur.
- Microsoft: Dynamics 365 Finance, Supply Chain, Sales, Customer Service, Field Service, Business Central, Dataverse.
- Salesforce: Sales Cloud, Service Cloud, CPQ, Revenue Cloud, Marketing Cloud, Data Cloud.
- Oracle: E-Business Suite, Fusion Cloud ERP, SCM, HCM, CX, NetSuite, JD Edwards, PeopleSoft, Siebel.
- Infor: LN, M3, CloudSuite Industrial/SyteLine, WMS, EAM.
- IFS: Cloud ERP, EAM, FSM, manufacturing, projects, service.
- Epicor, QAD, Sage, Unit4, Workday, ServiceNow, Jira, HubSpot, Zendesk, Shopify, Adobe Commerce.
- Manufacturing and industrial platforms: Siemens Teamcenter/Opcenter, PTC Windchill/ThingWorx, Dassault Enovia, Rockwell, AVEVA, OSIsoft PI, custom MES/SCADA/historians.

## Structure Pattern

For any source system, map:

1. Business process and module.
2. Header, item/line, schedule, status, condition, partner, text, attachment, and history objects.
3. Master data: customer, vendor/supplier, material/product, account, asset, employee, plant, site, organization.
4. Transaction facts and lifecycle events.
5. Document flow and cross-system keys.
6. Fiscal calendar, currency, unit of measure, language, legal entity, plant/site, and timezone.
7. Security model, tenant/client/company partitioning, and authorization filters.

## Output Requirements

- Provide candidate source objects by vendor family and process.
- Mark vendor object names as candidates until verified against metadata, APIs, CDS/views, warehouse tables, or exports.
- Include extraction path options: native connector, OData, REST, SQL view, CDS/entity, BW query, dataflow, lakehouse, warehouse, file export, API.
- Flag customization risks: custom tables, extensions, industry add-ons, partner fields, localized statuses, archived documents, deleted records, and late postings.

