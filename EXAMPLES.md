# Examples

<!-- bilingual-doc-header -->
## en-US Documentation

This document provides example prompts and expected outputs for common Power BI delivery scenarios such as churn, SAP FiCO, Dock2Stock, Complaint2CAPA, and Control2Evidence.

## de-DE Dokumentation

Dieses Dokument enthaelt Beispielprompts und erwartete Ergebnisse fuer typische Power-BI-Szenarien wie Churn, SAP FiCO, Dock2Stock, Complaint2CAPA und Control2Evidence.

<!-- /bilingual-doc-header -->


## Customer Churn

```text
Erstelle ein Power BI Customer Churn Cockpit.
Quellen: Salesforce, SAP S/4HANA, Snowflake.
Output: Datenmodell, Churn-KPIs, DAX, Segmentierung, Treiberanalyse, Validierung, en-US/de-DE Doku.
```

Expected output:

- Churn KPI contract.
- Customer cohort model.
- Revenue and contract history.
- Driver views by segment, product, region, service quality, price, and usage.
- Action list for retention owners.

## Process Owner Use Cases

For at least one use case per supported process chain, see [Process Chain KPIs](PROCESS_CHAIN_KPIS.md#process-use-case-matrix). The matrix defines the Process Owner question, expected Power BI output, and the decision each cockpit should enable in `en-US` and `de-DE`.

## SAP FiCO

```text
Plane ein Power BI Reporting fuer SAP FiCO.
Scope: Kostenstellen, Profit Center, Plan/Ist, Working Capital, Monatsabschluss.
Output: Modell, KPIs, DAX, Close2Report Cockpit, Validierung.
```

Expected output:

- FI/CO source mapping.
- Fiscal calendar and currency logic.
- P&L, balance sheet, cost center, profit center, and working-capital KPIs.
- Close process and reconciliation evidence.

## Dock2Stock

```text
Baue ein Dock2Stock Data Product.
Quellen: SAP EWM, SAP MM, SAP QM, Lieferanten-ASN.
Zeige GR Accuracy, Inspection Aging, Putaway Backlog und Blocked Stock.
```

Expected output:

- Inbound event fact.
- Supplier, material, plant, warehouse, batch, and inspection dimensions.
- Bottleneck view from ASN to goods receipt to inspection to putaway.
- Exception action backlog.

## Complaint2CAPA

```text
Erstelle ein Complaint2CAPA Cockpit.
Quellen: Veeva Quality, SAP QM, Salesforce Service.
Output: Complaint Rate, CAPA Aging, Wiederholfehler, Cost of Poor Quality, Effectiveness Check.
```

Expected output:

- Complaint, nonconformance, CAPA, defect, and customer dimensions.
- Aging and recurrence analysis.
- Quality cost bridge.
- CAPA owner and overdue actions.

## Control2Evidence

```text
Erzeuge ein Control2Evidence Cockpit fuer Audit und Compliance.
Quellen: SAP GRC, AuditBoard, Entra ID, SharePoint.
Output: Control Effectiveness, Evidence Coverage, SoD Violations, Remediation Aging.
```

Expected output:

- Control and evidence model.
- Finding and remediation workflow.
- Owner-based RLS.
- Audit-ready evidence pack.
