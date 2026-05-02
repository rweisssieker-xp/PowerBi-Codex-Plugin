---
name: powerbi-system-object-dictionaries
description: Use when Power BI work needs deeper system-specific object dictionaries for SAP S/4HANA, SAP BW, Dynamics, Salesforce, Oracle, Infor, IFS, ServiceNow, Manhattan, SAP EWM, or QMS platforms.
---

# Power BI System Object Dictionaries

Provide source-system object dictionaries as candidate maps for validation.

## Output Contract

- System, module, business process, object family, technical object candidates, key fields, date/status fields, and relationships.
- Extraction path candidates: native connector, API, CDS/OData, SQL replica, BW query, lakehouse, or warehouse.
- Known customizations, extension points, and validation checks.
- Mapping confidence and required metadata evidence.

## Checks

- Treat dictionary entries as candidates, not guaranteed customer truth.
- Include version and module assumptions.
