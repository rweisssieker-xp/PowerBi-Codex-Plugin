---
name: powerbi-source-system-gap-detector
description: Use when required Power BI KPIs cannot be built because source fields, history, keys, ownership, quality, status semantics, or process events are missing or unreliable.
---

# Power BI Source System Gap Detector

Find gaps between required analytics and available source data.

## Output Contract

- Required KPI and process event inventory.
- Available source fields and missing fields.
- Gap type: missing, low quality, wrong grain, no history, manual-only, unclear semantics, delayed replication, or no owner.
- Workaround, remediation, business impact, and delivery risk.
- Data owner action plan and retest criteria.

## Checks

- Separate true source gaps from warehouse modelling gaps.
- Flag when a KPI should be blocked rather than approximated.
