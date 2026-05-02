# Business Question Examples

## Customer Churn

Question: Which customers are likely to churn next period and what revenue is at risk?
Source: CRM accounts, contracts, invoices, product usage, support tickets.
Model: customer-period fact, customer dimension, product dimension, date, segment, churn reason.

## Material Churn

Question: Which materials are slow moving, obsolete, or creating working-capital risk?
Source: ERP material master, stock snapshots, goods movements, purchase orders, forecast.
Model: material-location-period fact, movement fact, material, plant, supplier, date.

## FiCO

Question: Where do actuals differ from plan and which cost/profit centers drive variance?
Source: GL line items, controlling documents, plan data, company code, cost center, profit center.
Model: journal fact, plan fact, account, cost center, profit center, fiscal date, scenario.

