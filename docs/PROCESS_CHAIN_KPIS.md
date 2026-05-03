# Process Chain KPIs

<!-- bilingual-doc-header -->
## en-US Documentation

This document lists industrial process chains, KPI themes, report page patterns, and validation expectations for process analytics packs.

## de-DE Dokumentation

Dieses Dokument listet industrielle Prozessketten, KPI-Themen, Reportseitenmuster und Validierungserwartungen fuer Process-Analytics-Packs.

<!-- /bilingual-doc-header -->


The plugin treats process chains as Power BI data products, not isolated dashboards. Each chain should define source systems, case IDs, lifecycle events, KPI contracts, semantic model grain, validation, and actions.

## de-DE Kurzfassung

Das Plugin macht Prozessketten als Power BI KPI-Produkte sichtbar, nicht als einzelne Dashboards. Jede Prozesskette braucht Quellsysteme, Case IDs, Events, KPI-Vertraege, Modell-Grain, Validierung, Verantwortliche und konkrete Massnahmen.

## Main Industrial Chains

| Chain | Typical focus |
|---|---|
| Lead2Order | Opportunity, quote, configuration, pricing, approval, order intake |
| Order2Cash | Sales order, ATP, delivery, billing, receivables, disputes, cash |
| Source2Contract | Supplier discovery, sourcing, contract, compliance |
| Procure2Pay | Requisition, purchase order, goods receipt, invoice, payment |
| Forecast2Plan | Demand signal, forecast, S&OP, inventory targets |
| Plan2Produce | Production order, BOM, routing, capacity, yield, variance |
| Make2Stock / Make2Order / Engineer2Order | Manufacturing strategy, coupling, inventory, milestones |
| Idea2Launch / Engineer2Release | Product idea, design, change, release, ramp-up |
| Maintain2Operate | Asset, work order, preventive maintenance, downtime |
| Issue2Resolution | Customer issue, warranty, quality notification, corrective action |
| Record2Report | Journal, controlling, consolidation, close |
| Hire2Retire | Workforce, shifts, skills, absence, safety, productivity |

## Additional KPI Visibility Chains

| Chain | KPI examples |
|---|---|
| Market2Lead | MQL, SQL, campaign ROI, CAC, lead velocity, conversion rate |
| Lead2Quote / Configure2Quote | quote cycle time, configuration error rate, discount leakage, approval aging |
| Quote2Contract | contract cycle time, legal loops, term deviations, value at risk |
| Contract2Revenue | billing readiness, revenue leakage, deferred revenue, renewal risk |
| Demand2Supply | forecast accuracy, ATP/CTP, shortage value, lost sales |
| S&OP / IBP2Execution | plan adherence, constrained gap, capacity overload, inventory target adherence |
| Design2Cost / Design2Source | target cost variance, single-source exposure, part reuse |
| Engineer2Order / Project2Cash | milestone adherence, project margin, WIP, cash exposure |
| Dock2Stock | dock-to-stock time, GR accuracy, inspection aging, blocked stock |
| Pick2Pack2Ship | pick accuracy, lines per hour, wave adherence, cut-off misses |
| Return2Disposition | return rate, disposition aging, resale rate, scrap rate, recovery value |
| Complaint2CAPA | complaint rate, CAPA aging, repeat defect rate, cost of poor quality |
| Nonconformance2Disposition | defect rate, blocked value, rework cost, supplier PPM |
| Incident2Action | incident rate, severity, response time, overdue actions |
| Asset2Reliability | OEE, MTBF, MTTR, downtime cost, PM compliance |
| InstalledBase2ServiceRevenue | attach rate, SLA adherence, service margin, renewal opportunity |
| SupplierOnboarding2Risk | qualification status, audit score, ESG risk, supplier risk exposure |
| Control2Evidence | control effectiveness, evidence coverage, SoD violations, remediation closure |
| Close2Report / Plan2Perform | close cycle, late postings, reconciliation breaks, forecast variance |
| Data2Insight2Action | insight adoption, action conversion, decision latency, value realized |

## Standard Page Pattern

Every process-chain cockpit should include:

- Executive overview.
- Process flow or funnel.
- Bottleneck and aging view.
- Exception list.
- Root-cause matrix.
- Financial impact bridge.
- Owner/action backlog.
- Drillthrough to case-level evidence.

## Standard Validation

- Source control totals.
- Case-level sample tracing.
- Timestamp and timezone checks.
- Unit, currency, and fiscal calendar validation.
- KPI contract sign-off.
- RLS/OLS validation.
- Business owner acceptance.
