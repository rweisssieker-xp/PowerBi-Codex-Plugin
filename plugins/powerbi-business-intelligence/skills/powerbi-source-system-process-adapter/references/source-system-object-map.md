# Source System Object Map

## SAP-Oriented Candidate Objects

Treat these as candidates to verify in the target system, not guaranteed objects.

- Lead2Order: CRM lead/opportunity, CPQ quote, sales quotation, sales order header/item, pricing conditions.
- Order2Cash: sales order, schedule line, delivery, goods issue, billing document, AR open item, payment, dispute.
- Procure2Pay: purchase requisition, purchase order, schedule line, goods receipt, invoice receipt, vendor open item.
- Plan2Produce: material master, BOM, routing, work center, planned order, production order, confirmation, goods movement.
- Forecast2Plan: forecast, demand plan, PIR, MRP element, stock requirement, capacity requirement.
- Record2Report: universal journal, cost center, profit center, internal order, WBS, plan, allocation, closing tasks.
- Maintain2Operate: equipment, functional location, notification, maintenance order, task list, measurement document.
- Issue2Resolution: quality notification, inspection lot, defect, corrective action, service order, warranty claim.

## Non-SAP Object Families

- Salesforce: lead, account, opportunity, quote, order, case, entitlement.
- Dynamics: lead, opportunity, quote, sales order, invoice, customer, case.
- MES: production order, operation, machine event, downtime, scrap, rework, quality result.
- PLM: item, BOM, engineering change, release state, requirement, document.
- WMS/TMS: warehouse order, pick task, shipment, carrier event, delivery confirmation.
- Data lake/warehouse: curated fact and dimension tables, snapshots, slowly changing dimensions, bridge tables.

## Cross-System Key Risks

- Customer/account IDs differ between CRM and ERP.
- Material/product IDs differ between PLM, ERP, MES, and sales systems.
- Sales order, delivery, invoice, shipment, and payment flows are not always one-to-one.
- Plant, company code, profit center, and legal entity scopes may conflict.
- Currency, unit of measure, and fiscal calendar conversion must be explicit.

