---
name: powerbi-process-chain-kpi-visibility
description: Use when industrial enterprise questions require Power BI KPI visibility across additional end-to-end process chains, micro-processes, cross-system handoffs, and action-oriented management cockpits.
---

# Power BI Process Chain KPI Visibility

Use this skill when a business question is broader than a single report and needs KPI visibility across a complete process chain, cross-system handoffs, bottlenecks, owners, and actions.

## Operating Mode

Act as a process-chain KPI architect. Convert each chain into a Power BI data product with process events, source systems, KPI contracts, semantic model grain, root-cause dimensions, visuals, validation, action routing, and aligned `en-US` and `de-DE` documentation.

## Required Output

- Process chain, business owner, decision cadence, scope, and target action.
- Source systems, likely objects, event grain, keys, timestamps, lifecycle states, and handoff points.
- KPI tree with leading indicators, lagging indicators, SLA/thresholds, financial impact, and owner.
- Power BI model pattern: facts, dimensions, date roles, bridge tables, many-to-many risks, RLS, and refresh mode.
- Visual pattern: executive overview, flow/funnel, bottlenecks, aging, exception list, root-cause matrix, cohort/segment view, drillthrough, and action backlog.
- Validation: source reconciliation, control totals, unit/currency/calendar checks, sample cases, and business sign-off.
- Documentation: create matching `en-US` and `de-DE` artifact documentation for substantial outputs.

## Process Chain KPI Catalog

| Process chain | Core business question | Typical source systems | KPI examples |
|---|---|---|---|
| Market2Lead | Which marketing activities create qualified pipeline? | CRM, CDP, marketing automation, web analytics, consent systems | MQL, SQL, campaign ROI, CAC, lead velocity, conversion rate, lead aging |
| Lead2Quote / Configure2Quote | How efficiently do we turn demand into valid commercial offers? | CRM, CPQ, pricing, product catalog, ERP material/customer master | quote cycle time, configuration error rate, discount leakage, approval aging, win/loss by quote reason |
| Quote2Contract | Where do offers stall before legally binding business? | CRM, CLM, document management, e-signature, ERP sales | contract cycle time, legal loop count, approval bottlenecks, term deviations, contract value at risk |
| Contract2Revenue | Are contracts converted into billable, recognized revenue without leakage? | CLM, ERP SD/FI, billing, subscription, revenue recognition | billing readiness, revenue leakage, deferred revenue, renewal risk, credit memo rate |
| Demand2Supply | Can supply satisfy real demand at acceptable service and cost? | CRM/order book, ERP, APS, MRP, SCM, supplier portals | forecast accuracy, demand volatility, ATP/CTP, shortage value, lost sales, supply risk |
| S&OP / IBP2Execution | Does the approved plan translate into operational execution? | EPM/IBP, APS, ERP, MES, WMS, finance planning | plan adherence, constrained gap, scenario delta, capacity overload, inventory target adherence |
| Design2Cost / Design2Source | Are product designs costable, sourcable, and manufacturable? | PLM, CAD/BOM, ERP costing, sourcing, supplier risk | target cost variance, design-to-cost gap, single-source exposure, part reuse, sourcing readiness |
| Engineer2Order / Project2Cash | Are project/ETO orders profitable, on schedule, and cash-positive? | PLM, project systems, ERP PS/CO/SD, time, procurement | milestone adherence, project margin, change order value, WIP, cash exposure, delivery risk |
| Dock2Stock | How fast and cleanly does inbound material become usable stock? | WMS/WHS, ERP MM, QM/QMS, supplier ASN, yard systems | dock-to-stock time, GR accuracy, inspection aging, putaway backlog, blocked stock |
| Pick2Pack2Ship | What limits outbound warehouse productivity and shipping reliability? | WMS/WHS, TMS, carrier APIs, ERP SD, automation/scanners | pick accuracy, lines per hour, wave adherence, pack errors, cut-off misses, ship-on-time |
| Return2Disposition | What happens to returned material, cash, and recovery value? | CRM/service, ERP SD/MM/FI, WMS, QMS, repair systems | return rate, disposition aging, resale rate, scrap rate, credit value, recovery value |
| Complaint2CAPA | Which complaints drive quality cost and repeat failures? | CRM, QMS, SAP QM, EHS, service, warranty | complaint rate, CAPA aging, repeat defect rate, cost of poor quality, effectiveness check |
| Nonconformance2Disposition | How do internal/supplier defects affect inventory, delivery, and cost? | QMS, SAP QM, MES, ERP MM/PP, supplier quality | defect rate, blocked value, rework cost, scrap cost, supplier PPM, disposition lead time |
| Incident2Action | Are EHS, security, IT, and operational incidents closed with durable actions? | EHS, ITSM, SIEM, QMS, maintenance, workflow/RPA | incident rate, severity, response time, action closure, repeat incident rate, overdue actions |
| Asset2Reliability | Which assets constrain uptime, throughput, quality, and maintenance cost? | EAM/CMMS, MES, SCADA, historian, ERP PM, spare parts | OEE, MTBF, MTTR, downtime cost, PM compliance, maintenance backlog, spare risk |
| InstalledBase2ServiceRevenue | Is installed base converted into profitable service and aftermarket revenue? | FSM, CRM, ERP service, warranty, IoT, contract systems | attach rate, SLA adherence, service margin, spare parts revenue, renewal opportunity, warranty cost |
| SupplierOnboarding2Risk | Are suppliers qualified, compliant, and performance-ready before spend scales? | SRM, procurement, risk platforms, QMS, ESG, ERP vendor master | onboarding lead time, qualification status, audit score, ESG risk, supplier risk exposure |
| Control2Evidence | Can controls, audit findings, and evidence be proven without manual expert effort? | GRC, audit, identity, workflow, DMS, ERP/FI | control effectiveness, evidence coverage, finding aging, SoD violations, remediation closure |
| Close2Report / Plan2Perform | Does finance close fast, reconcile cleanly, and explain performance? | ERP FI/CO, consolidation, EPM, treasury, tax, data warehouse | close cycle, late postings, reconciliation breaks, forecast variance, working capital, EBIT bridge |
| Data2Insight2Action | Do BI insights lead to accountable action and measurable value? | Power BI/Fabric, ticketing, workflow, CRM, ERP, telemetry | insight adoption, action conversion, decision latency, value realized, stale report rate, owner coverage |

## Design Pattern

1. Select the chain and decide whether it is macro E2E, operational micro-chain, governance chain, or analytics-to-action chain.
2. Define the canonical case ID, event timestamp, owner, status, value field, and blocking reason before designing visuals.
3. Identify the system of record per event. Do not merge source replicas until keys, status definitions, and timing semantics are validated.
4. Build a KPI tree from outcome KPI to driver KPI to exception KPI to action KPI.
5. Create a semantic model with event fact, current-state fact, value fact, owner dimension, organization dimension, product/material/customer/supplier dimensions, and role-playing date dimensions.
6. Add process-mining compatibility when events have case ID, activity, timestamp, and lifecycle variant.
7. Add closed-loop action routing for every exception KPI: owner, due date, impact, recommended action, and retest condition.

## Common Source-System Traps

- CRM and ERP disagree on customer, quote, opportunity, order, contract, and revenue status.
- CPQ configuration versions are overwritten and cannot explain historical margin leakage without snapshots.
- WMS/WHS timestamps use operational local time while ERP uses posting date, document date, or fiscal period.
- QM/QMS severity, defect, complaint, nonconformance, and CAPA taxonomies are inconsistent across plants.
- PLM engineering BOM, ERP manufacturing BOM, and service BOM are not aligned by validity date.
- EPM plan versions and ERP actuals use different hierarchies, calendars, currencies, and consolidation scopes.
- Tickets and actions are closed administratively but not effectiveness-tested against the originating KPI.
