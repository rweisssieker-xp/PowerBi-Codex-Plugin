---
name: powerbi-industrial-process-intelligence
description: Understand and solve Power BI analytics questions for industrial companies across all main end-to-end processes, including Lead2Order, Order2Cash, Procure2Pay, Source2Contract, Forecast2Plan, Plan2Produce, Make2Stock, Engineer2Order, Idea2Launch, Record2Report, Hire2Retire, Issue2Resolution, Maintain2Operate, and Supply Chain Control Tower.
---

# Power BI Industrial Process Intelligence

Use this skill when the business context is an industrial company, manufacturer, plant network, machinery business, discrete manufacturing, process manufacturing, automotive supplier, industrial service organization, or equipment producer.

## Operating Mode

Act as an industrial enterprise BI architect. Translate process questions into source-system-aware Power BI solutions. Do not treat sales, finance, production, supply chain, service, procurement, engineering, and maintenance as isolated dashboards when the question crosses process boundaries.

## Main Process Map

- Lead2Order: lead, account, opportunity, quote, configuration, pricing, approval, order intake.
- Order2Cash: sales order, ATP, delivery, shipment, billing, receivables, disputes, cash.
- Source2Contract: supplier discovery, qualification, sourcing event, contract, price condition, compliance.
- Procure2Pay: requisition, purchase order, confirmation, goods receipt, invoice receipt, payment.
- Forecast2Plan: demand signal, forecast, S&OP, capacity plan, inventory target, constrained plan.
- Plan2Produce: planned order, production order, BOM, routing, capacity, confirmation, yield, variance.
- Make2Stock / Make2Order / Engineer2Order: manufacturing strategy, order coupling, inventory, engineering changes, project milestones.
- Idea2Launch / Engineer2Release: idea, product requirement, design, change order, release, ramp-up.
- Maintain2Operate: asset, work order, preventive maintenance, breakdown, spare parts, downtime.
- Issue2Resolution: customer issue, warranty claim, quality notification, corrective action, service order.
- Record2Report: journal, controlling, cost center, profit center, asset accounting, consolidation, close.
- Hire2Retire: workforce, shifts, skills, training, absence, safety, productivity.

## Workflow

1. Identify the end-to-end process, process variant, plant/company scope, and decision owner.
2. Translate the business question into process events, fact grain, lifecycle states, dimensions, and KPIs.
3. Identify likely source systems and the system of record per process step.
4. Map source-system objects through `powerbi-source-system-process-adapter`.
5. Define semantic model, DAX, report pages, drill paths, RLS, and validation.
6. Include cross-process joins only when keys, timing, and ownership are proven.

## Output Requirements

- Include process scope, source systems, source objects, model grain, KPIs, page pattern, validation, and risks.
- Separate "system of record" from "reporting replica", "data lake", and "manual enrichment".
- Flag common industrial traps: document flow breaks, unit-of-measure conversion, currency, fiscal calendar, plant/company code mismatch, BOM/routing versioning, partial deliveries, returns, backorders, consignment, subcontracting, intercompany, and late postings.

