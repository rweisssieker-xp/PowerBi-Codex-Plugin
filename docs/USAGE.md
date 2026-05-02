# Usage Guide

## Recommended Prompt Shape

Use a prompt that includes business question, source systems, target audience, process scope, and expected output.

```text
Erstelle ein Power BI Cockpit fuer Order2Cash.
Quellsysteme: SAP S/4HANA SD/FI, Salesforce, SAP EWM, Snowflake.
Zielgruppe: CFO, COO, O2C Process Owner.
Output: KPI tree, semantic model, DAX catalog, report pages, validation, en-US/de-DE Doku.
```

## Common Workflows

### Business Problem to Blueprint

Use when the user has a business problem but no clear BI design.

Example:

```text
Warum verlieren wir Materialbestand durch Obsolescence, Scrap und Umlagerungen?
Erstelle ein Power BI Blueprint mit Quellen, Modell, KPIs und Cockpit.
```

### Source-System-Aware Process Analytics

Use when a question spans ERP, CRM, WMS, MES, QMS, EPM, or lakehouse data.

Example:

```text
Loese eine Quote2Contract Frage fuer Salesforce, SAP S/4HANA und DocuSign.
Zeige Bottlenecks, Legal Loops, Approval Aging und Contract Value at Risk.
```

### Governed Semantic Model

Use when report sprawl or KPI conflict needs consolidation.

Example:

```text
Konsolidiere 12 lokale Sales Reports in ein zertifiziertes Sales Semantic Model.
Beruecksichtige KPI-Konflikte, RLS, DAX Tests und Owner Acceptance.
```

### Quality Gate

Use before publishing, certifying, migrating, or handing over a report.

Example:

```text
Fuehre ein Power BI Quality Gate fuer dieses Modell durch:
KPI Definitionen, DAX, RLS, Refresh, Performance, Lineage, Dokumentation, UAT.
```

### AI-Native Delivery

Use when the plugin should orchestrate multiple BI expert roles.

Example:

```text
Fuehre einen autonomen BI Sprint fuer Dock2Stock durch.
Starte mit Intake, erstelle Data Contract, Modell, KPI Tree, Report Spec, Tests, Quality Gate und en-US/de-DE Doku.
```

## Expected Outputs

Depending on the request, the plugin can produce:

- Process and business scope.
- Source-system mapping and metadata assumptions.
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
- Bilingual documentation in `en-US` and `de-DE`.

## Prompt Anti-Patterns

Avoid prompts like:

```text
Mach ein Dashboard.
```

Better:

```text
Baue ein CFO Cockpit fuer Contract2Revenue.
Quellen: Salesforce Revenue Cloud, SAP FI/CO, Snowflake.
KPIs: Revenue Leakage, Deferred Revenue, Billing Readiness, Renewal Risk.
Output: KPI tree, Modell, DAX, Visuals, Validierung, en-US/de-DE Doku.
```
