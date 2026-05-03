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

## Process Use Case Matrix

### en-US

Each process chain should have at least one concrete Power BI use case that a Process Owner can request without translating the work into BI-expert language first.

| Process | Process Owner use case | Power BI output | Decision enabled |
|---|---|---|---|
| Lead2Order | Identify where qualified demand leaks before booked order. | Funnel conversion, SLA aging, quote leakage, owner action cockpit. | Reassign owners, remove qualification/quote bottlenecks, shift budget to high-conversion channels. |
| Order2Cash | Find why orders are stuck before delivery, billing, or cash collection. | Backlog, ATP, OTIF, billing block, AR aging, exception cockpit. | Prioritize blocked orders, release billing issues, reduce overdue cash. |
| Source2Contract | Detect sourcing events and supplier contracts with cycle-time or compliance risk. | Sourcing pipeline, contract aging, compliance exceptions, supplier risk view. | Escalate legal/procurement loops and reduce contract value at risk. |
| Procure2Pay | Explain invoice blocks, GR/IR aging, and supplier payment delays. | PO, goods receipt, invoice block, payment, discount capture cockpit. | Fix blocked invoices, protect discounts, reduce supplier escalations. |
| Forecast2Plan | Compare demand signals to forecast and inventory targets. | Forecast accuracy, bias, S&OP gap, target inventory bridge. | Rebalance demand plan, inventory targets, and supply priorities. |
| Plan2Produce | Identify why production orders miss schedule, yield, or cost targets. | Production order aging, capacity, yield, variance, quality loss cockpit. | Re-sequence production, resolve capacity constraints, reduce scrap. |
| Make2Stock / Make2Order / Engineer2Order | Compare manufacturing strategy performance across inventory, milestones, and customer commitments. | Strategy cockpit for stock cover, lead time, WIP, milestone adherence. | Choose where to decouple, expedite, or redesign planning rules. |
| Idea2Launch / Engineer2Release | Track product development delay, engineering changes, and release readiness. | Gate status, change backlog, launch risk, ramp-up readiness. | Escalate late gates, unblock engineering changes, protect launch dates. |
| Maintain2Operate | Reduce downtime by finding maintenance backlog and reliability drivers. | Work order, PM compliance, downtime cost, MTBF/MTTR cockpit. | Prioritize preventive work and high-risk assets. |
| Issue2Resolution | Find customer issues and warranty cases that breach SLA or repeat. | Issue aging, warranty cost, repeat issue, corrective action cockpit. | Escalate overdue cases and attack repeat root causes. |
| Record2Report | Control month-end close, reconciliations, and late postings. | Close task, journal, reconciliation, control exception cockpit. | Remove close blockers and reduce audit findings. |
| Hire2Retire | Track workforce capacity, absence, skills, and safety impact. | Workforce availability, skill gap, absence, shift and safety cockpit. | Plan staffing, training, and safety interventions. |
| Market2Lead | Determine which campaigns create qualified leads, not only volume. | Campaign ROI, MQL/SQL conversion, CAC, lead velocity. | Shift marketing spend to sources that convert. |
| Lead2Quote / Configure2Quote | Find quote and configuration errors delaying commercial response. | Quote cycle, configuration error, approval aging, discount leakage. | Fix product/configuration rules and approval bottlenecks. |
| Quote2Contract | Identify legal or commercial loops delaying signed contracts. | Contract cycle, redline loops, term deviations, value at risk. | Escalate contract clauses and reduce time-to-signature. |
| Contract2Revenue | Find contracted value that is not ready for billing or revenue recognition. | Billing readiness, revenue leakage, deferred revenue, renewal risk. | Fix missing billing data and protect revenue timing. |
| Demand2Supply | Explain shortages, lost sales, and ATP/CTP failures. | Forecast-to-supply gap, shortage value, ATP/CTP, lost sales. | Allocate constrained supply and trigger mitigation actions. |
| S&OP / IBP2Execution | Compare approved plan to operational execution. | Plan adherence, constrained gap, capacity overload, inventory target adherence. | Reconcile plan assumptions and operational constraints. |
| Design2Cost / Design2Source | Detect designs that miss cost or sourcing targets. | Target cost variance, part reuse, single-source exposure. | Redesign parts, qualify suppliers, reduce cost risk. |
| Engineer2Order / Project2Cash | Control project milestones, margin, WIP, and cash exposure. | Milestone adherence, project margin, WIP, billing and cash cockpit. | Escalate late milestones and protect project cash flow. |
| Dock2Stock | Reduce inbound warehouse delay from dock arrival to available stock. | ASN, goods receipt, inspection aging, putaway backlog, blocked stock. | Remove receiving/quality bottlenecks and release stock. |
| Pick2Pack2Ship | Improve outbound warehouse execution and cut-off adherence. | Pick accuracy, wave adherence, pack backlog, shipment cut-off misses. | Reprioritize waves and prevent late shipments. |
| Return2Disposition | Reduce returns aging and maximize recovery value. | Return reason, disposition aging, resale/scrap/rework value. | Route returns faster and recover more value. |
| Complaint2CAPA | Control complaint aging, CAPA effectiveness, and repeat defects. | Complaint rate, CAPA aging, repeat defect, cost of poor quality. | Escalate overdue CAPAs and stop recurring defects. |
| Nonconformance2Disposition | Reduce blocked value, rework, and supplier quality defects. | Defect rate, blocked stock value, rework cost, supplier PPM. | Decide disposition and supplier corrective actions. |
| Incident2Action | Ensure incidents create timely corrective actions. | Incident severity, response time, overdue action, risk heatmap. | Escalate overdue safety/compliance actions. |
| Asset2Reliability | Improve asset availability and reliability economics. | OEE, downtime cost, MTBF, MTTR, PM compliance. | Prioritize assets for maintenance and investment. |
| InstalledBase2ServiceRevenue | Grow service revenue from installed base coverage and renewals. | Attach rate, SLA adherence, service margin, renewal opportunity. | Target upsell, renewal, and service improvement actions. |
| SupplierOnboarding2Risk | Control supplier readiness, audits, and risk exposure. | Qualification status, audit score, ESG risk, onboarding aging. | Approve, block, or remediate supplier onboarding. |
| Control2Evidence | Prove controls and remediation with audit-ready evidence. | Control effectiveness, evidence coverage, SoD violations, remediation aging. | Close audit gaps and assign remediation owners. |
| Close2Report / Plan2Perform | Explain close delays and planning variance. | Close cycle, late postings, reconciliation breaks, forecast variance. | Resolve close blockers and improve planning assumptions. |
| Data2Insight2Action | Track whether insights become actions and value. | Insight adoption, action conversion, decision latency, realized value. | Improve decision speed and action accountability. |

### de-DE

Jede Prozesskette braucht mindestens einen konkreten Power-BI-Use-Case, den ein Process Owner anfordern kann, ohne die Arbeit zuerst in BI-Expertensprache zu uebersetzen.

| Prozess | Process-Owner-Use-Case | Power-BI-Ergebnis | Ermoeglichte Entscheidung |
|---|---|---|---|
| Lead2Order | Erkennen, wo qualifizierte Nachfrage vor dem gebuchten Auftrag verloren geht. | Funnel Conversion, SLA Aging, Quote Leakage, Owner Action Cockpit. | Owner neu zuweisen, Qualification-/Quote-Bottlenecks entfernen, Budget auf starke Channels verschieben. |
| Order2Cash | Verstehen, warum Auftraege vor Lieferung, Faktura oder Zahlung haengen. | Backlog, ATP, OTIF, Billing Block, AR Aging, Exception Cockpit. | Blockierte Auftraege priorisieren, Billing Issues loesen, overdue Cash reduzieren. |
| Source2Contract | Sourcing Events und Lieferantenvertraege mit Cycle-Time- oder Compliance-Risiko finden. | Sourcing Pipeline, Contract Aging, Compliance Exceptions, Supplier Risk View. | Legal-/Procurement-Schleifen eskalieren und Contract Value at Risk reduzieren. |
| Procure2Pay | Invoice Blocks, GR/IR Aging und Lieferantenzahlungsverzug erklaeren. | PO-, Goods-Receipt-, Invoice-Block-, Payment- und Discount-Capture-Cockpit. | Blockierte Rechnungen loesen, Skonti sichern, Lieferanteneskalationen reduzieren. |
| Forecast2Plan | Demand Signals gegen Forecast und Inventory Targets pruefen. | Forecast Accuracy, Bias, S&OP Gap, Target Inventory Bridge. | Demand Plan, Inventory Targets und Supply Priorities neu ausrichten. |
| Plan2Produce | Ursachen fuer verfehlte Produktionsplaene, Yield- oder Cost-Ziele finden. | Production Order Aging, Capacity, Yield, Variance, Quality Loss Cockpit. | Produktion umplanen, Capacity Constraints loesen, Scrap reduzieren. |
| Make2Stock / Make2Order / Engineer2Order | Fertigungsstrategie nach Bestand, Milestones und Kundencommitments vergleichen. | Strategy Cockpit fuer Stock Cover, Lead Time, WIP, Milestone Adherence. | Entkopplung, Expediting oder Planungsregeln anpassen. |
| Idea2Launch / Engineer2Release | Produktentwicklungsverzug, Engineering Changes und Release Readiness verfolgen. | Gate Status, Change Backlog, Launch Risk, Ramp-up Readiness. | Spaete Gates eskalieren, Engineering Changes unblocken, Launch-Termine schuetzen. |
| Maintain2Operate | Downtime durch Maintenance Backlog und Reliability Drivers reduzieren. | Work Order, PM Compliance, Downtime Cost, MTBF/MTTR Cockpit. | Praeventive Arbeiten und Risikoanlagen priorisieren. |
| Issue2Resolution | Kundenprobleme und Warranty Cases mit SLA-Bruch oder Wiederholung finden. | Issue Aging, Warranty Cost, Repeat Issue, Corrective Action Cockpit. | Ueberfaellige Faelle eskalieren und wiederkehrende Ursachen abstellen. |
| Record2Report | Monatsabschluss, Reconciliations und Late Postings steuern. | Close Task, Journal, Reconciliation, Control Exception Cockpit. | Close Blocker entfernen und Audit Findings reduzieren. |
| Hire2Retire | Workforce Capacity, Absence, Skills und Safety Impact verfolgen. | Workforce Availability, Skill Gap, Absence, Shift und Safety Cockpit. | Staffing, Training und Safety Interventions planen. |
| Market2Lead | Kampagnen identifizieren, die qualifizierte Leads statt nur Volumen erzeugen. | Campaign ROI, MQL/SQL Conversion, CAC, Lead Velocity. | Marketing Spend auf konvertierende Quellen verschieben. |
| Lead2Quote / Configure2Quote | Quote- und Konfigurationsfehler finden, die Commercial Response verzoegern. | Quote Cycle, Configuration Error, Approval Aging, Discount Leakage. | Produkt-/Konfigurationsregeln und Approval Bottlenecks verbessern. |
| Quote2Contract | Legal- oder Commercial-Loops identifizieren, die Vertragsabschluss verzoegern. | Contract Cycle, Redline Loops, Term Deviations, Value at Risk. | Vertragsklauseln eskalieren und Time-to-Signature reduzieren. |
| Contract2Revenue | Vertragswert finden, der noch nicht faktura- oder revenue-ready ist. | Billing Readiness, Revenue Leakage, Deferred Revenue, Renewal Risk. | Fehlende Billing-Daten korrigieren und Revenue Timing sichern. |
| Demand2Supply | Shortages, Lost Sales und ATP/CTP-Fehler erklaeren. | Forecast-to-Supply Gap, Shortage Value, ATP/CTP, Lost Sales. | Begrenzte Supply allokieren und Mitigation Actions starten. |
| S&OP / IBP2Execution | Genehmigten Plan mit operativer Ausfuehrung vergleichen. | Plan Adherence, Constrained Gap, Capacity Overload, Inventory Target Adherence. | Planannahmen und operative Constraints abgleichen. |
| Design2Cost / Design2Source | Designs erkennen, die Cost- oder Sourcing-Ziele verfehlen. | Target Cost Variance, Part Reuse, Single-Source Exposure. | Teile redesignen, Lieferanten qualifizieren, Kostenrisiko reduzieren. |
| Engineer2Order / Project2Cash | Projektmilestones, Margin, WIP und Cash Exposure steuern. | Milestone Adherence, Project Margin, WIP, Billing und Cash Cockpit. | Spaete Milestones eskalieren und Projekt-Cashflow schuetzen. |
| Dock2Stock | Inbound-Warehouse-Verzug von Dock Arrival bis verfuegbarem Bestand reduzieren. | ASN, Goods Receipt, Inspection Aging, Putaway Backlog, Blocked Stock. | Receiving-/Quality-Bottlenecks entfernen und Bestand freigeben. |
| Pick2Pack2Ship | Outbound-Warehouse-Ausfuehrung und Cut-off Adherence verbessern. | Pick Accuracy, Wave Adherence, Pack Backlog, Shipment Cut-off Misses. | Waves neu priorisieren und Late Shipments vermeiden. |
| Return2Disposition | Returns Aging reduzieren und Recovery Value maximieren. | Return Reason, Disposition Aging, Resale/Scrap/Rework Value. | Returns schneller routen und Wert rueckgewinnen. |
| Complaint2CAPA | Complaint Aging, CAPA Effectiveness und Repeat Defects steuern. | Complaint Rate, CAPA Aging, Repeat Defect, Cost of Poor Quality. | Ueberfaellige CAPAs eskalieren und Wiederholfehler stoppen. |
| Nonconformance2Disposition | Blocked Value, Rework und Supplier Quality Defects reduzieren. | Defect Rate, Blocked Stock Value, Rework Cost, Supplier PPM. | Disposition und Supplier Corrective Actions entscheiden. |
| Incident2Action | Sicherstellen, dass Incidents zeitnahe Corrective Actions erzeugen. | Incident Severity, Response Time, Overdue Action, Risk Heatmap. | Ueberfaellige Safety-/Compliance-Actions eskalieren. |
| Asset2Reliability | Asset Availability und Reliability Economics verbessern. | OEE, Downtime Cost, MTBF, MTTR, PM Compliance. | Assets fuer Maintenance und Investitionen priorisieren. |
| InstalledBase2ServiceRevenue | Service Revenue aus Installed Base Coverage und Renewals steigern. | Attach Rate, SLA Adherence, Service Margin, Renewal Opportunity. | Upsell-, Renewal- und Service-Verbesserungen anstossen. |
| SupplierOnboarding2Risk | Supplier Readiness, Audits und Risk Exposure steuern. | Qualification Status, Audit Score, ESG Risk, Onboarding Aging. | Supplier freigeben, blockieren oder remediieren. |
| Control2Evidence | Controls und Remediation audit-ready nachweisen. | Control Effectiveness, Evidence Coverage, SoD Violations, Remediation Aging. | Audit Gaps schliessen und Remediation Owner zuweisen. |
| Close2Report / Plan2Perform | Close Delays und Planning Variance erklaeren. | Close Cycle, Late Postings, Reconciliation Breaks, Forecast Variance. | Close Blocker loesen und Planannahmen verbessern. |
| Data2Insight2Action | Nachverfolgen, ob Insights zu Actions und Wert fuehren. | Insight Adoption, Action Conversion, Decision Latency, Realized Value. | Entscheidungsgeschwindigkeit und Action Accountability verbessern. |

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
