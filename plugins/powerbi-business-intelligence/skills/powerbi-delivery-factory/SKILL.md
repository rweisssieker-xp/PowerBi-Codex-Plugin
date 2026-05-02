---
name: powerbi-delivery-factory
description: Generate complete Power BI delivery packs that replace ad hoc expert handoffs. Use for report specs, semantic model specs, DAX catalogs, query plans, validation plans, deployment checklists, maintenance runbooks, and acceptance criteria.
---

# Power BI Delivery Factory

Use this skill when the output should be a complete implementation package instead of advice.

## Delivery Pack Contents

1. `POWERBI_REPORT_SPEC.md`
2. `SEMANTIC_MODEL_SPEC.md`
3. `QUERY_EXTRACTION_PLAN.md`
4. `DAX_MEASURE_CATALOG.csv`
5. `VALIDATION_PLAN.md`
6. `RLS_SECURITY_SPEC.md`
7. `DEPLOYMENT_CHECKLIST.md`
8. `MAINTENANCE_RUNBOOK.md`

## Workflow

1. Start from a business problem, data source, or existing report.
2. Select domain pack and modelling pattern.
3. Generate the delivery pack with assumptions separated from confirmed facts.
4. Include review gates for business owner, data owner, security owner, and Power BI owner.
5. Make outputs implementation-ready for fewer, more focused experts.

## Scripts

- `scripts/new_delivery_pack.py`: Create a complete folder-based delivery pack.

