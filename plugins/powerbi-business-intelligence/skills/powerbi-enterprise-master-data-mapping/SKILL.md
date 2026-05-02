---
name: powerbi-enterprise-master-data-mapping
description: Use when Power BI solutions need cross-system master data mapping for customers, suppliers, products, materials, accounts, assets, employees, plants, legal entities, cost centers, profit centers, projects, or hierarchies.
---

# Power BI Enterprise Master Data Mapping

Use this skill when a business question crosses ERP, CRM, PLM, MES, finance, service, or warehouse boundaries.

## Master Data Domains

- Customer/account/business partner.
- Supplier/vendor.
- Product/material/item/SKU.
- Asset/equipment/functional location.
- Employee/worker/operator/salesperson.
- Organization/legal entity/company code/plant/site/warehouse.
- Finance dimensions: GL account, cost center, profit center, project, WBS, internal order.
- Geography, channel, segment, product hierarchy, customer hierarchy, supplier hierarchy.

## Workflow

1. Identify the system of record and consuming systems for each master data domain.
2. Map natural keys, surrogate keys, alternate keys, and slowly changing attributes.
3. Resolve hierarchy ownership and effective dating.
4. Define bridge tables for many-to-many cross-system mapping.
5. Specify data quality checks: duplicates, missing keys, orphaned facts, conflicting names, inactive records.
6. Define RLS-relevant attributes and sensitivity constraints.

## Output Requirements

- Include mapping table design, hierarchy strategy, SCD handling, conflict rules, and validation checks.
- Do not join cross-system facts on names or descriptions when stable IDs are unavailable; create explicit mapping backlog items.

