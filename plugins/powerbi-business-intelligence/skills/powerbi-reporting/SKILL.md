---
name: powerbi-reporting
description: Build, review, and validate generic Power BI reports and dashboards from any supported data source. Use for report requirements, data ingestion, semantic models, DAX, Power Query, PBIP/PBIR, RLS, refresh, governance, page layouts, visual selection, validation, and business problems such as churn, FiCO, sales, supply chain, service, HR, risk, and operations.
---

# Power BI Reporting

## Operating Mode

Act as a senior Power BI architect. Convert business questions into data-source plans, star schemas, explicit KPI definitions, DAX measures, governed report pages, and validation checks.

Load only the references needed for the task:

- `references/data-sources.md` for supported source families and ingestion patterns.
- `references/business-problem-patterns.md` for reusable analytic solutions.
- `references/report-design.md` for page layouts and visual choices.
- `references/validation-governance.md` for RLS, privacy, refresh, deployment, and acceptance tests.

## Workflow

1. Identify business outcome, decision owner, grain, time logic, and required actions.
2. Identify source family: file, folder, database, warehouse, lakehouse, Fabric, Power Platform, SaaS, API, OData, SAP, streaming, or manual input.
3. Define facts, dimensions, relationships, measures, RLS, refresh, and reconciliation source.
4. Design report pages with compact decision workflows, not decorative dashboards.
5. Validate numbers against source totals and document assumptions, exclusions, latency, and security.

## Output Requirements

- Include source plan, model layout, DAX measure list, page layout, filters, RLS, refresh, deployment, and validation notes.
- Treat connector names, tables, columns, and credentials as environment-specific until verified.
- Flag PII, financial sensitivity, row-level security gaps, and gateway/licensing dependencies.

## Assets

- `assets/core-measures.dax`: reusable DAX starter patterns.
- `assets/powerquery-connector-patterns.pq`: Power Query connector snippets.

## Scripts

- `scripts/generate_powerbi_pack.py`: Generate Power Query, DAX, TMDL skeleton, report spec, and maintenance runbook from CSV table/measure specs.
- `scripts/new_powerbi_report_spec.py`: Generate a business-problem report specification.

## Runtime Executor

When the user asks to generate or improve a complete Power BI report/model package, prefer:

```powershell
python scripts\powerbi_expert_factory.py report-package --process <process-id> --sources "<source description>" --goal "<report goal>" --out outputs\report-packages\<process-id>
```
