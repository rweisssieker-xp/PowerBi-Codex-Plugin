---
name: powerbi-data-quality-rule-library
description: Use when Power BI data products need reusable data quality rules by process, including customers, materials, units, inventory, GRIR, CAPA, ATP, invoices, orders, and master data.
---

# Power BI Data Quality Rule Library

Apply reusable quality checks by process and source system.

## Rule Families

- Master data: missing customer/material/supplier, invalid hierarchy, inactive owner.
- Finance: currency mismatch, late posting, unreconciled balances, GR/IR aging.
- Supply chain: negative stock, UoM mismatch, ATP mismatch, blocked stock, stale forecast.
- Quality: overdue CAPA, duplicate complaint, missing disposition, invalid severity.
- Sales/service: orphan orders, missing contracts, stale opportunities, SLA breach.

## Output Contract

- Rule ID, process, source fields, severity, threshold, owner, test query pattern, and remediation route.
