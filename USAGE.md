# Usage Guide

Use the plugin when you want to turn a business or process question into governed Power BI delivery artifacts.

## Recommended Prompt Shape

Include:

- Business question.
- Process scope.
- Source systems.
- Target audience.
- Expected output.
- Validation expectations.

Example:

```text
Create an Order2Cash Power BI cockpit.
Sources: SAP S/4HANA SD/FI, Salesforce, SAP EWM, Snowflake.
Audience: CFO, COO, O2C Process Owner.
Output: KPI tree, semantic model, DAX catalog, report pages, validation plan, and release evidence.
```

## Common Workflows

### Business Problem To Blueprint

Use this when the business problem is clear but the BI design is not.

```text
Why are we losing material value through obsolescence, scrap, and transfers?
Create a Power BI blueprint with sources, model, KPIs, and cockpit pages.
```

### Source-Aware Process Analytics

Use this when a question spans ERP, CRM, WMS, MES, QMS, EPM, APIs, files, or lakehouse data.

```text
Build a Quote2Contract analytics design for Salesforce, SAP S/4HANA, and DocuSign.
Show bottlenecks, approval aging, legal loops, and contract value at risk.
```

### Governed Semantic Model

Use this when report sprawl or KPI conflict needs consolidation.

```text
Consolidate 12 local sales reports into one certified sales semantic model.
Include KPI conflict handling, RLS, DAX tests, and owner acceptance.
```

### Quality Gate

Use this before publishing, certifying, migrating, or handing over a report.

```text
Run a Power BI quality gate for this model:
KPI definitions, DAX, RLS, refresh, performance, lineage, documentation, and UAT.
```

## Expected Outputs

Depending on the request, the plugin can produce:

- Business and process scope.
- Source-system mapping.
- KPI contracts.
- Semantic model design.
- DAX measure catalog.
- Power Query extraction design.
- Report page layout.
- RLS/OLS and governance model.
- Refresh and gateway pattern.
- Validation and reconciliation plan.
- Quality gate checklist.
- Delivery runbook.
